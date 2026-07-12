from __future__ import annotations

import pytest

from viasign_parser.settings import DEFAULT_CORS_ORIGINS, load_settings


def test_default_settings_are_local_only() -> None:
    settings = load_settings({})
    assert settings.host == "127.0.0.1"
    assert settings.port == 8000
    assert settings.cors_origins == DEFAULT_CORS_ORIGINS
    assert settings.access_log is False
    assert settings.trust_render_proxy is False


def test_explicit_origins_are_normalized_and_deduplicated() -> None:
    settings = load_settings(
        {
            "VIASIGN_HOST": "0.0.0.0",
            "VIASIGN_PORT": "9000",
            "VIASIGN_CORS_ORIGINS": (
                "https://www.viathorne.com/, https://preview.viathorne.com, "
                "https://www.viathorne.com"
            ),
            "VIASIGN_ACCESS_LOG": "true",
            "VIASIGN_TRUST_RENDER_PROXY": "true",
        }
    )
    assert settings.host == "0.0.0.0"
    assert settings.port == 9000
    assert settings.cors_origins == (
        "https://www.viathorne.com",
        "https://preview.viathorne.com",
    )
    assert settings.access_log is True
    assert settings.trust_render_proxy is True


def test_empty_origin_setting_disables_cross_origin_access() -> None:
    assert load_settings({"VIASIGN_CORS_ORIGINS": ""}).cors_origins == ()


@pytest.mark.parametrize(
    "origin",
    [
        "*",
        "javascript:alert(1)",
        "http://public.example",
        "https://example.com/path",
        "https://user:password@example.com",
    ],
)
def test_unsafe_origins_are_rejected(origin: str) -> None:
    with pytest.raises(ValueError):
        load_settings({"VIASIGN_CORS_ORIGINS": origin})


@pytest.mark.parametrize("port", ["zero", "0", "65536"])
def test_invalid_ports_are_rejected(port: str) -> None:
    with pytest.raises(ValueError):
        load_settings({"VIASIGN_PORT": port})


def test_invalid_access_log_setting_is_rejected() -> None:
    with pytest.raises(ValueError):
        load_settings({"VIASIGN_ACCESS_LOG": "sometimes"})


def test_invalid_render_proxy_setting_is_rejected() -> None:
    with pytest.raises(ValueError):
        load_settings({"VIASIGN_TRUST_RENDER_PROXY": "sometimes"})
