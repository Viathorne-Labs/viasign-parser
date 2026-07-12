from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError
from pydantic import ValidationError as PydanticValidationError

from scripts.export_contracts import generated_contracts
from viasign_parser.contracts import PUBLIC_RESPONSE_ADAPTER


ROOT = Path(__file__).parents[1]
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "v1"
CONTRACT_ROOT = ROOT / "contracts" / "v1"
POSITIVE_GROUPS = ("valid", "uncertain", "unsupported")


def _load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _fixture_paths(*groups: str) -> list[Path]:
    return sorted(
        path
        for group in groups
        for path in (FIXTURE_ROOT / group).glob("*.json")
    )


@pytest.mark.parametrize("fixture_path", _fixture_paths(*POSITIVE_GROUPS))
def test_positive_fixtures_match_typed_contract(fixture_path: Path) -> None:
    payload = _load(fixture_path)
    response = PUBLIC_RESPONSE_ADAPTER.validate_python(payload)
    serialized = PUBLIC_RESPONSE_ADAPTER.dump_python(response, mode="json")
    assert serialized == payload


@pytest.mark.parametrize("fixture_path", _fixture_paths("invalid"))
def test_invalid_fixtures_fail_typed_contract(fixture_path: Path) -> None:
    with pytest.raises(PydanticValidationError):
        PUBLIC_RESPONSE_ADAPTER.validate_python(_load(fixture_path))


def test_committed_json_schemas_match_generated_contracts() -> None:
    for filename, generated_schema in generated_contracts().items():
        assert _load(CONTRACT_ROOT / filename) == generated_schema


@pytest.mark.parametrize("fixture_path", _fixture_paths(*POSITIVE_GROUPS))
def test_positive_fixtures_match_json_schema(fixture_path: Path) -> None:
    schema = _load(CONTRACT_ROOT / "parser-response.schema.json")
    Draft202012Validator(schema).validate(_load(fixture_path))


@pytest.mark.parametrize("fixture_path", _fixture_paths("invalid"))
def test_invalid_fixtures_fail_json_schema(fixture_path: Path) -> None:
    schema = _load(CONTRACT_ROOT / "parser-response.schema.json")
    with pytest.raises(JsonSchemaValidationError):
        Draft202012Validator(schema).validate(_load(fixture_path))


def test_response_schema_contains_literal_safety_invariants() -> None:
    schema_text = (CONTRACT_ROOT / "parser-response.schema.json").read_text(
        encoding="utf-8"
    )
    assert '"review_required"' in schema_text
    assert '"const": true' in schema_text
    assert '"motion_ready"' in schema_text
    assert '"const": false' in schema_text


def test_response_schema_contains_no_submitted_text_field() -> None:
    schema = _load(CONTRACT_ROOT / "parser-response.schema.json")
    input_metadata = schema["$defs"]["InputMetadata"]

    assert input_metadata["properties"] == {
        "mode": {
            "enum": ["natural", "source_gloss", "unknown"],
            "title": "Mode",
            "type": "string",
        }
    }
    assert input_metadata["required"] == ["mode"]
    assert input_metadata["additionalProperties"] is False


def test_request_schema_is_strict_and_bounded() -> None:
    schema = _load(CONTRACT_ROOT / "parse-request.schema.json")
    assert schema["additionalProperties"] is False
    text_schema = schema["properties"]["text"]
    assert text_schema["maxLength"] == 1_000
    assert text_schema["minLength"] == 1
    assert "pattern" in text_schema
