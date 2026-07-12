"""Validated environment settings for the public API service."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from urllib.parse import urlsplit


DEFAULT_CORS_ORIGINS = (
    "http://localhost:4321",
    "http://127.0.0.1:4321",
)


def _normalize_origin(value: str) -> str:
    candidate = value.strip().rstrip("/")
    parsed = urlsplit(candidate)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.netloc
        or parsed.path
        or parsed.query
        or parsed.fragment
        or parsed.username
        or parsed.password
    ):
        raise ValueError(f"invalid CORS origin: {value!r}")
    if parsed.scheme == "http" and parsed.hostname not in {
        "localhost",
        "127.0.0.1",
        "::1",
    }:
        raise ValueError("non-local CORS origins must use HTTPS")
    return candidate


def _parse_origins(value: str | None) -> tuple[str, ...]:
    if value is None:
        return DEFAULT_CORS_ORIGINS
    if not value.strip():
        return ()

    origins: list[str] = []
    for item in value.split(","):
        origin = _normalize_origin(item)
        if origin == "*":
            raise ValueError("wildcard CORS origins are not allowed")
        if origin not in origins:
            origins.append(origin)
    return tuple(origins)


def _parse_port(value: str | None) -> int:
    if value is None:
        return 8000
    try:
        port = int(value)
    except ValueError as error:
        raise ValueError("VIASIGN_PORT must be an integer") from error
    if not 1 <= port <= 65_535:
        raise ValueError("VIASIGN_PORT must be between 1 and 65535")
    return port


def _parse_boolean(name: str, value: str | None, default: bool) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be true or false")


@dataclass(frozen=True, slots=True)
class Settings:
    host: str
    port: int
    cors_origins: tuple[str, ...]
    access_log: bool
    trust_render_proxy: bool = False


def load_settings(environment: Mapping[str, str] | None = None) -> Settings:
    values = os.environ if environment is None else environment
    host = values.get("VIASIGN_HOST", "127.0.0.1").strip()
    if not host:
        raise ValueError("VIASIGN_HOST must not be empty")
    return Settings(
        host=host,
        port=_parse_port(values.get("VIASIGN_PORT")),
        cors_origins=_parse_origins(values.get("VIASIGN_CORS_ORIGINS")),
        access_log=_parse_boolean(
            "VIASIGN_ACCESS_LOG",
            values.get("VIASIGN_ACCESS_LOG"),
            False,
        ),
        trust_render_proxy=_parse_boolean(
            "VIASIGN_TRUST_RENDER_PROXY",
            values.get("VIASIGN_TRUST_RENDER_PROXY"),
            False,
        ),
    )
