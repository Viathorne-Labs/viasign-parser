"""Strict transport models for the public ViaSign API boundary."""

from __future__ import annotations

import unicodedata
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


MAX_INPUT_CHARACTERS = 1_000


class StrictModel(BaseModel):
    """Reject fields that the public contract does not define."""

    model_config = ConfigDict(extra="forbid")


class ParseRequest(StrictModel):
    """A single typed input for draft grammar planning."""

    text: str = Field(
        min_length=1,
        max_length=MAX_INPUT_CHARACTERS,
        pattern=r"^[^\x00-\x1f\x7f-\x9f]+$",
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("text must contain non-whitespace characters")
        if any(unicodedata.category(character) == "Cc" for character in stripped):
            raise ValueError("text must not contain control characters")
        return stripped


class HealthResponse(StrictModel):
    status: Literal["ok"] = "ok"


class MetaResponse(StrictModel):
    project: Literal["viasign-parser"] = "viasign-parser"
    api_version: Literal["v1"] = "v1"
    maturity: Literal["pre-alpha"] = "pre-alpha"
    parser_available: Literal[True] = True
    grammar_rules_available: Literal[False] = False
    parser_version: Literal["0.1.0"] = "0.1.0"
    ruleset_version: Literal["public-safety-only-v1"] = "public-safety-only-v1"
    review_required: Literal[True] = True
    motion_ready: Literal[False] = False


class ErrorDetail(StrictModel):
    code: str
    message: str
    review_required: Literal[True] = True
    motion_ready: Literal[False] = False


class ErrorResponse(StrictModel):
    detail: ErrorDetail
