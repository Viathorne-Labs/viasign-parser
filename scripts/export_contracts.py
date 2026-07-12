"""Generate committed JSON Schemas from the authoritative Pydantic models."""

from __future__ import annotations

import json
from pathlib import Path

from viasign_parser.api_models import ParseRequest
from viasign_parser.contracts import PUBLIC_RESPONSE_ADAPTER


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "contracts" / "v1"
JSON_SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"


def _document(schema_id: str, schema: dict[str, object]) -> dict[str, object]:
    return {
        "$schema": JSON_SCHEMA_DIALECT,
        "$id": schema_id,
        **schema,
    }


def generated_contracts() -> dict[str, dict[str, object]]:
    return {
        "parse-request.schema.json": _document(
            "urn:viathorne:viasign:parser:v1:parse-request",
            ParseRequest.model_json_schema(),
        ),
        "parser-response.schema.json": _document(
            "urn:viathorne:viasign:parser:v1:parser-response",
            PUBLIC_RESPONSE_ADAPTER.json_schema(),
        ),
    }


def main() -> None:
    CONTRACT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, schema in generated_contracts().items():
        output_path = CONTRACT_DIR / filename
        output_path.write_text(
            json.dumps(schema, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
