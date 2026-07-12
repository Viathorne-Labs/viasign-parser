"""Small ASGI guards for the public HTTP boundary."""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import ipaddress
import math
import secrets
import time
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send


MAX_PARSE_BODY_BYTES = 4_096
PARSE_TIMEOUT_SECONDS = 3.0
RATE_LIMIT_REQUESTS_PER_MINUTE = 60
RATE_LIMIT_BURST = 20
RATE_LIMIT_MAX_CLIENTS = 10_000
RATE_LIMIT_ENTRY_TTL_SECONDS = 600


@dataclass(slots=True)
class _RateBucket:
    tokens: float
    last_refill: float
    last_seen: float


class ParseRateLimitMiddleware:
    """Apply a transient, per-network token bucket to public parse requests."""

    def __init__(
        self,
        app: ASGIApp,
        *,
        trust_render_proxy: bool = False,
        clock: Callable[[], float] = time.monotonic,
        digest_key: bytes | None = None,
    ) -> None:
        self.app = app
        self.trust_render_proxy = trust_render_proxy
        self.clock = clock
        self.digest_key = digest_key or secrets.token_bytes(32)
        self.buckets: OrderedDict[bytes, _RateBucket] = OrderedDict()
        self.refill_per_second = RATE_LIMIT_REQUESTS_PER_MINUTE / 60

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if (
            scope["type"] != "http"
            or scope.get("method") != "POST"
            or scope.get("path") != "/v1/parse"
        ):
            await self.app(scope, receive, send)
            return

        client_address = self._client_address(scope)
        if client_address is None:
            response = JSONResponse(
                status_code=503,
                content={
                    "detail": {
                        "code": "client_network_unavailable",
                        "message": (
                            "The service could not safely apply its request limit. "
                            "Please try again later."
                        ),
                        "review_required": True,
                        "motion_ready": False,
                    }
                },
                headers={
                    "Cache-Control": "no-store",
                    "X-Content-Type-Options": "nosniff",
                },
            )
            await response(scope, receive, send)
            return

        now = self.clock()
        client_key = hmac.digest(
            self.digest_key,
            client_address.encode("utf-8"),
            hashlib.sha256,
        )
        retry_after = self._consume(client_key, now)
        if retry_after is not None:
            seconds_label = "second" if retry_after == 1 else "seconds"
            response = JSONResponse(
                status_code=429,
                content={
                    "detail": {
                        "code": "rate_limit_exceeded",
                        "message": (
                            "Too many parse requests were received from this "
                            f"network. Please wait {retry_after} {seconds_label} "
                            "and try again. Your text was not processed."
                        ),
                        "review_required": True,
                        "motion_ready": False,
                    }
                },
                headers={
                    "Retry-After": str(retry_after),
                    "Cache-Control": "no-store",
                    "X-Content-Type-Options": "nosniff",
                },
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)

    def _client_address(self, scope: Scope) -> str | None:
        if self.trust_render_proxy:
            for name, value in scope.get("headers", []):
                if name.lower() != b"x-forwarded-for":
                    continue
                first_address = value.decode("ascii", errors="ignore").split(",", 1)[0]
                candidate = first_address.strip()
                try:
                    return ipaddress.ip_address(candidate).compressed
                except ValueError:
                    return None
            return None

        client = scope.get("client")
        if not client or not client[0]:
            return None
        return str(client[0])

    def _consume(self, client_key: bytes, now: float) -> int | None:
        self._evict_stale(now)
        bucket = self.buckets.get(client_key)
        if bucket is None:
            if len(self.buckets) >= RATE_LIMIT_MAX_CLIENTS:
                self.buckets.popitem(last=False)
            self.buckets[client_key] = _RateBucket(
                tokens=RATE_LIMIT_BURST - 1,
                last_refill=now,
                last_seen=now,
            )
            return None

        elapsed = max(0.0, now - bucket.last_refill)
        bucket.tokens = min(
            RATE_LIMIT_BURST,
            bucket.tokens + elapsed * self.refill_per_second,
        )
        bucket.last_refill = now
        bucket.last_seen = now
        self.buckets.move_to_end(client_key)

        if bucket.tokens < 1:
            return max(
                1,
                math.ceil((1 - bucket.tokens) / self.refill_per_second),
            )

        bucket.tokens -= 1
        return None

    def _evict_stale(self, now: float) -> None:
        cutoff = now - RATE_LIMIT_ENTRY_TTL_SECONDS
        while self.buckets:
            first_key = next(iter(self.buckets))
            if self.buckets[first_key].last_seen > cutoff:
                return
            self.buckets.popitem(last=False)


class ParseBodyLimitMiddleware:
    """Buffer only the small public parse body and reject larger requests."""

    def __init__(self, app: ASGIApp, max_bytes: int = MAX_PARSE_BODY_BYTES) -> None:
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if (
            scope["type"] != "http"
            or scope.get("method") != "POST"
            or scope.get("path") != "/v1/parse"
        ):
            await self.app(scope, receive, send)
            return

        messages: list[Message] = []
        total_bytes = 0

        while True:
            message = await receive()
            messages.append(message)
            if message["type"] == "http.disconnect":
                break
            if message["type"] != "http.request":
                continue

            total_bytes += len(message.get("body", b""))
            if total_bytes > self.max_bytes:
                response = JSONResponse(
                    status_code=413,
                    content={
                        "detail": {
                            "code": "request_too_large",
                            "message": "The public parse request exceeded 4096 bytes.",
                            "review_required": True,
                            "motion_ready": False,
                        }
                    },
                    headers={
                        "Cache-Control": "no-store",
                        "X-Content-Type-Options": "nosniff",
                    },
                )
                await response(scope, receive, send)
                return

            if not message.get("more_body", False):
                break

        message_iterator = iter(messages)

        async def replay_receive() -> Message:
            return next(
                message_iterator,
                {"type": "http.disconnect"},
            )

        await self.app(scope, replay_receive, send)


class ParseTimeoutMiddleware:
    """Fail closed before the website's five-second request deadline."""

    def __init__(
        self,
        app: ASGIApp,
        timeout_seconds: float = PARSE_TIMEOUT_SECONDS,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("parse timeout must be greater than zero")
        self.app = app
        self.timeout_seconds = timeout_seconds

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if (
            scope["type"] != "http"
            or scope.get("method") != "POST"
            or scope.get("path") != "/v1/parse"
        ):
            await self.app(scope, receive, send)
            return

        buffered_messages: list[Message] = []

        async def buffered_send(message: Message) -> None:
            buffered_messages.append(message)

        try:
            await asyncio.wait_for(
                self.app(scope, receive, buffered_send),
                timeout=self.timeout_seconds,
            )
        except TimeoutError:
            response = JSONResponse(
                status_code=503,
                content={
                    "detail": {
                        "code": "parse_timeout",
                        "message": (
                            "The service could not finish safely in time. "
                            "Please try again later."
                        ),
                        "review_required": True,
                        "motion_ready": False,
                    }
                },
                headers={
                    "Cache-Control": "no-store",
                    "X-Content-Type-Options": "nosniff",
                },
            )
            await response(scope, receive, send)
            return

        for message in buffered_messages:
            await send(message)
