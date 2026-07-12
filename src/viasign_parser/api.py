"""Fail-closed FastAPI shell for the public ViaSign parser."""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from fastapi import APIRouter, FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from .api_models import ErrorResponse, HealthResponse, MetaResponse, ParseRequest
from .contracts import PUBLIC_RESPONSE_ADAPTER, PublicParserResponse
from .middleware import (
    PARSE_TIMEOUT_SECONDS,
    ParseBodyLimitMiddleware,
    ParseRateLimitMiddleware,
    ParseTimeoutMiddleware,
)
from .parser import parse_public
from .safety import UnsafeParserState, require_public_safety_invariants
from .settings import Settings, load_settings


router = APIRouter()


async def _add_public_response_headers(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    # Use the ASGI route path directly. Do not reconstruct security decisions
    # from the client-controlled Host header via request.url.
    if request.scope.get("path") == "/v1/parse":
        response.headers["Cache-Control"] = "no-store"
    return response


async def _safe_validation_error(
    _request: Request,
    _error: RequestValidationError,
) -> JSONResponse:
    """Reject invalid requests without echoing their submitted values."""

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": {
                "code": "invalid_request",
                "message": "The request did not match the public parser contract.",
                "review_required": True,
                "motion_ready": False,
            }
        },
    )


def create_app(
    settings: Settings | None = None,
    *,
    parse_timeout_seconds: float = PARSE_TIMEOUT_SECONDS,
) -> FastAPI:
    active_settings = settings or load_settings()
    application = FastAPI(
        title="ViaSign Parser",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        description=(
            "A review-required grammar-planning prototype. It is not a finished "
            "SgSL translator and does not produce motion or avatar output."
        ),
    )
    application.add_exception_handler(RequestValidationError, _safe_validation_error)
    application.add_middleware(ParseBodyLimitMiddleware)
    application.add_middleware(
        ParseRateLimitMiddleware,
        trust_render_proxy=active_settings.trust_render_proxy,
    )
    application.add_middleware(
        ParseTimeoutMiddleware,
        timeout_seconds=parse_timeout_seconds,
    )
    if active_settings.cors_origins:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=list(active_settings.cors_origins),
            allow_credentials=False,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["Content-Type"],
            max_age=600,
        )
    application.middleware("http")(_add_public_response_headers)
    application.include_router(router)
    return application


@router.get("/healthz", response_model=HealthResponse, tags=["service"])
def health() -> HealthResponse:
    return HealthResponse()


@router.get("/v1/meta", response_model=MetaResponse, tags=["service"])
def metadata() -> MetaResponse:
    return MetaResponse()


@router.post(
    "/v1/parse",
    response_model=PublicParserResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponse},
        status.HTTP_413_CONTENT_TOO_LARGE: {"model": ErrorResponse},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ErrorResponse},
    },
    tags=["grammar-planning"],
)
def parse_text(request: ParseRequest) -> PublicParserResponse:
    """Return clean-room draft structure or an explicit unsupported result."""

    result = parse_public(request.text)
    serialized = PUBLIC_RESPONSE_ADAPTER.dump_python(result, mode="json")
    try:
        require_public_safety_invariants(serialized)
    except UnsafeParserState as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "unsafe_parser_state",
                "message": "The parser result violated the public safety contract.",
                "review_required": True,
                "motion_ready": False,
            },
        ) from error
    return result


app = create_app()


def run() -> None:
    """Run the local development server."""

    import uvicorn

    settings = load_settings()
    uvicorn.run(
        "viasign_parser.api:app",
        host=settings.host,
        port=settings.port,
        access_log=settings.access_log,
    )
