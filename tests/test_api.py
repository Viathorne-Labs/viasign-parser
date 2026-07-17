import time

import pytest
import viasign_parser.api as api_module
from fastapi.testclient import TestClient

from viasign_parser.api import app, create_app
from viasign_parser.middleware import (
    MAX_PARSE_BODY_BYTES,
    RATE_LIMIT_BURST,
    ParseRateLimitMiddleware,
)
from viasign_parser.settings import Settings


client = TestClient(app)


def test_health_is_minimal() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metadata_exposes_safety_boundary() -> None:
    response = client.get("/v1/meta")
    assert response.status_code == 200
    assert response.json() == {
        "project": "viasign-parser",
        "api_version": "v1",
        "maturity": "pre-alpha",
        "parser_available": True,
        "surface_analysis_available": True,
        "grammar_rules_available": False,
        "parser_version": "0.2.1",
        "ruleset_version": "public-surface-only-v1",
        "review_required": True,
        "motion_ready": False,
    }


def test_parse_returns_visible_uncertainty_without_grammar_output() -> None:
    response = client.post(
        "/v1/parse",
        json={"text": "Is the community room open?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["input"] == {"mode": "natural"}
    assert payload["outcome"] == "uncertain"
    assert payload["analysis"] == {
        "intent": "question",
        "surface": {
            "sentence_kind": "question",
            "question_kind": "yes_no",
            "question_category": "none",
            "negation_cue": "absent",
        },
        "sign_aware_form": None,
        "candidate_glosses": [],
    }
    assert payload["warnings"][0]["code"] == "sgsl_grammar_rules_unavailable"
    assert payload["review_required"] is True
    assert payload["motion_ready"] is False


@pytest.mark.parametrize(
    "text",
    [
        "Please create a name sign for me.",
        "Assign a sign-name.",
        "What is a name sign?",
        "Create a namesign.",
        "How do I sign my name?",
        "What is my name in SgSL?",
        "How should my name be signed?",
        "What are names in SgSL?",
        "Tell me which sign people use for my name.",
    ],
)
def test_parse_blocks_name_sign_related_input_without_analysis(text: str) -> None:
    response = client.post(
        "/v1/parse",
        json={"text": text},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["input"] == {"mode": "natural"}
    assert payload["outcome"] == "unsupported"
    assert payload["analysis"] is None
    assert payload["warnings"][0]["code"] == "cultural_topic_not_supported"
    assert payload["unsupported_reasons"][0]["code"] == (
        "name_sign_boundary_blocked"
    )
    assert payload["review_required"] is True
    assert payload["motion_ready"] is False
    assert text not in response.text


def test_parse_rejects_blank_text() -> None:
    response = client.post("/v1/parse", json={"text": "   "})
    assert response.status_code == 422


def test_parse_rejects_extra_fields() -> None:
    response = client.post(
        "/v1/parse",
        json={"text": "Hello", "motion_ready": True},
    )
    assert response.status_code == 422


def test_parse_responses_never_echo_submitted_text() -> None:
    submitted_text = "A private sample phrase 93Q?"

    response = client.post("/v1/parse", json={"text": submitted_text})

    assert response.status_code == 200
    assert response.json()["input"] == {"mode": "natural"}
    assert submitted_text not in response.text


def test_validation_errors_never_echo_submitted_values() -> None:
    submitted_text = "A private sample phrase with an invalid extra field"

    response = client.post(
        "/v1/parse",
        json={"text": submitted_text, "unexpected": submitted_text},
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": {
            "code": "invalid_request",
            "message": "The request did not match the public parser contract.",
            "review_required": True,
            "motion_ready": False,
        }
    }
    assert submitted_text not in response.text
    assert response.headers["cache-control"] == "no-store"


def test_malformed_json_error_never_echoes_request_content() -> None:
    submitted_content = '{"text":"private sample", invalid}'

    response = client.post(
        "/v1/parse",
        content=submitted_content,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "invalid_request"
    assert submitted_content not in response.text


def test_parse_rejects_control_characters() -> None:
    response = client.post("/v1/parse", json={"text": "Hello\nworld"})
    assert response.status_code == 422


def test_no_motion_or_translation_routes_exist() -> None:
    paths = set(app.openapi()["paths"])
    assert "/v1/translate" not in paths
    assert "/v1/motion" not in paths
    assert "/v1/avatar" not in paths


def test_only_allowlisted_runtime_routes_are_exposed() -> None:
    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404
    assert client.get("/openapi.json").status_code == 404


def test_parse_response_is_not_cacheable_or_sniffable() -> None:
    response = client.post("/v1/parse", json={"text": "Hello"})

    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"


def test_parse_cache_policy_does_not_depend_on_host_reconstructed_url() -> None:
    response = client.post(
        "/v1/parse",
        json={"text": "Hello"},
        headers={"Host": "testserver/not-the-route?ignored="},
    )

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert response.json()["review_required"] is True
    assert response.json()["motion_ready"] is False


def test_parse_rejects_body_larger_than_public_limit() -> None:
    response = client.post(
        "/v1/parse",
        content=b"x" * (MAX_PARSE_BODY_BYTES + 1),
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 413
    assert response.json() == {
        "detail": {
            "code": "request_too_large",
            "message": "The public parse request exceeded 4096 bytes.",
            "review_required": True,
            "motion_ready": False,
        }
    }
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"


def test_parse_timeout_is_accessible_and_fail_closed(monkeypatch) -> None:
    def slow_parse(_text: str):
        time.sleep(0.1)
        raise AssertionError("timed-out parser output must not be returned")

    monkeypatch.setattr(api_module, "parse_public", slow_parse)
    timeout_client = TestClient(
        create_app(
            Settings(
                host="127.0.0.1",
                port=8000,
                cors_origins=("http://localhost:4321",),
                access_log=False,
            ),
            parse_timeout_seconds=0.01,
        )
    )

    response = timeout_client.post(
        "/v1/parse",
        json={"text": "This result must never be shown"},
        headers={"Origin": "http://localhost:4321"},
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": {
            "code": "parse_timeout",
            "message": (
                "The service could not finish safely in time. "
                "Please try again later."
            ),
            "review_required": True,
            "motion_ready": False,
        }
    }
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["access-control-allow-origin"] == (
        "http://localhost:4321"
    )


def test_parse_openapi_exposes_contract_success_and_fail_closed_error() -> None:
    responses = app.openapi()["paths"]["/v1/parse"]["post"]["responses"]
    assert "200" in responses
    assert "422" in responses
    assert "429" in responses
    assert "500" in responses
    assert "503" in responses


def test_parse_rate_limit_returns_accessible_fail_closed_response() -> None:
    limited_client = TestClient(
        create_app(
            Settings(
                host="127.0.0.1",
                port=8000,
                cors_origins=("http://localhost:4321",),
                access_log=False,
            )
        )
    )

    for _ in range(RATE_LIMIT_BURST):
        response = limited_client.post(
            "/v1/parse",
            json={"text": "Hello"},
            headers={"Origin": "http://localhost:4321"},
        )
        assert response.status_code == 200

    response = limited_client.post(
        "/v1/parse",
        json={"text": "This must not be processed"},
        headers={"Origin": "http://localhost:4321"},
    )

    assert response.status_code == 429
    assert response.headers["retry-after"] == "1"
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["access-control-allow-origin"] == (
        "http://localhost:4321"
    )
    assert response.json() == {
        "detail": {
            "code": "rate_limit_exceeded",
            "message": (
                "Too many parse requests were received from this network. "
                "Please wait 1 second and try again. Your text was not processed."
            ),
            "review_required": True,
            "motion_ready": False,
        }
    }


def test_render_proxy_rate_limit_uses_first_forwarded_client_address() -> None:
    render_client = TestClient(
        create_app(
            Settings(
                host="0.0.0.0",
                port=10000,
                cors_origins=(),
                access_log=False,
                trust_render_proxy=True,
            )
        )
    )
    shared_proxy = "10.0.0.1"

    for _ in range(RATE_LIMIT_BURST):
        response = render_client.post(
            "/v1/parse",
            json={"text": "Hello"},
            headers={
                "X-Forwarded-For": f"203.0.113.10, {shared_proxy}",
            },
        )
        assert response.status_code == 200

    limited = render_client.post(
        "/v1/parse",
        json={"text": "Hello"},
        headers={"X-Forwarded-For": f"203.0.113.10, {shared_proxy}"},
    )
    other_client = render_client.post(
        "/v1/parse",
        json={"text": "Hello"},
        headers={"X-Forwarded-For": f"203.0.113.11, {shared_proxy}"},
    )

    assert limited.status_code == 429
    assert other_client.status_code == 200


def test_render_proxy_mode_fails_closed_without_valid_forwarded_address() -> None:
    render_client = TestClient(
        create_app(
            Settings(
                host="0.0.0.0",
                port=10000,
                cors_origins=(),
                access_log=False,
                trust_render_proxy=True,
            )
        )
    )

    missing = render_client.post("/v1/parse", json={"text": "Hello"})
    invalid = render_client.post(
        "/v1/parse",
        json={"text": "Hello"},
        headers={"X-Forwarded-For": "not-an-ip-address"},
    )

    assert render_client.get("/healthz").status_code == 200
    assert render_client.get("/v1/meta").status_code == 200

    for response in (missing, invalid):
        assert response.status_code == 503
        assert response.headers["cache-control"] == "no-store"
        assert response.json()["detail"] == {
            "code": "client_network_unavailable",
            "message": (
                "The service could not safely apply its request limit. "
                "Please try again later."
            ),
            "review_required": True,
            "motion_ready": False,
        }


def test_rate_limiter_stores_only_keyed_client_digests() -> None:
    limited_app = create_app(
        Settings(
            host="127.0.0.1",
            port=8000,
            cors_origins=(),
            access_log=False,
        )
    )
    limited_client = TestClient(limited_app)

    assert limited_client.post("/v1/parse", json={"text": "Hello"}).status_code == 200

    middleware = limited_app.middleware_stack
    while middleware is not None and not isinstance(
        middleware,
        ParseRateLimitMiddleware,
    ):
        middleware = getattr(middleware, "app", None)

    assert isinstance(middleware, ParseRateLimitMiddleware)
    assert middleware.buckets
    assert all(isinstance(key, bytes) and len(key) == 32 for key in middleware.buckets)
    assert all(b"testclient" not in key for key in middleware.buckets)


def test_local_website_origin_is_allowed() -> None:
    response = client.options(
        "/v1/parse",
        headers={
            "Origin": "http://localhost:4321",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:4321"
    assert response.headers.get("access-control-allow-credentials") is None


def test_unlisted_website_origin_is_denied() -> None:
    response = client.options(
        "/v1/parse",
        headers={
            "Origin": "https://unexpected.example",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_configured_app_factory_keeps_api_routes() -> None:
    configured_client = TestClient(
        create_app(
            Settings(
                host="127.0.0.1",
                port=8000,
                cors_origins=("https://www.viathorne.com",),
                access_log=False,
            )
        )
    )

    response = configured_client.get("/v1/meta")

    assert response.status_code == 200
    assert response.json()["review_required"] is True
    assert response.json()["motion_ready"] is False
