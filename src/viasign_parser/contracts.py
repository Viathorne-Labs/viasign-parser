"""Versioned public parser response contract.

These types define transport structure only. They do not implement SgSL
grammar and do not establish linguistic correctness.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field, TypeAdapter

from .api_models import StrictModel


SCHEMA_VERSION = "viasign.parser.response.v1"
CONTRACT_VERSION = "1.1.0"

InputMode = Literal["natural", "source_gloss", "unknown"]
Intent = Literal[
    "statement",
    "question",
    "self_introduction",
    "name_sign_request",
    "unknown",
]
SentenceKind = Literal["statement", "question", "unknown"]
QuestionKind = Literal["wh", "yes_no", "unknown", "not_applicable"]
QuestionCategory = Literal[
    "what",
    "who",
    "whose",
    "why",
    "how",
    "where",
    "which",
    "when",
    "none",
]
NegationCue = Literal["present", "absent", "ambiguous"]
CandidateGloss = Annotated[
    str,
    Field(min_length=1, max_length=100, pattern=r"^[A-Z0-9][A-Z0-9_()/-]*$"),
]


class InputMetadata(StrictModel):
    """Non-sensitive metadata about how the request was interpreted."""

    mode: InputMode


class ContractWarning(StrictModel):
    """Visible uncertainty or a public safety warning."""

    code: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    message: str = Field(min_length=1, max_length=500)
    field: str | None = Field(max_length=100)
    review_state: Literal["review_required"]


class UnsupportedReason(StrictModel):
    """A reason the public parser intentionally produced no analysis."""

    code: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    message: str = Field(min_length=1, max_length=500)


class SurfaceAnalysis(StrictModel):
    """Closed, non-verbatim observations about natural-English input."""

    sentence_kind: SentenceKind
    question_kind: QuestionKind
    question_category: QuestionCategory
    negation_cue: NegationCue


class GrammarAnalysis(StrictModel):
    """Draft grammar-planning fields, never approved translation output."""

    intent: Intent
    surface: SurfaceAnalysis
    sign_aware_form: str | None = Field(max_length=2_000)
    candidate_glosses: list[CandidateGloss] = Field(max_length=128)


class ContractProvenance(StrictModel):
    """Identifies the implementation and ruleset that produced a response."""

    parser_id: Literal["viasign-parser"]
    parser_version: str = Field(min_length=1, max_length=50)
    ruleset_version: str = Field(min_length=1, max_length=100)
    contract_version: Literal[CONTRACT_VERSION]


class ResponseBase(StrictModel):
    """Safety fields shared by every public response variant."""

    schema_version: Literal[SCHEMA_VERSION]
    status: Literal["review_required"]
    input: InputMetadata
    review_required: Literal[True]
    motion_ready: Literal[False]
    provenance: ContractProvenance


class DraftResponse(ResponseBase):
    """Structurally supported draft output that still requires human review."""

    outcome: Literal["draft"]
    analysis: GrammarAnalysis
    warnings: list[ContractWarning] = Field(max_length=128)


class UncertainResponse(ResponseBase):
    """Draft output with explicit unresolved uncertainty."""

    outcome: Literal["uncertain"]
    analysis: GrammarAnalysis
    warnings: list[ContractWarning] = Field(min_length=1, max_length=128)


class UnsupportedResponse(ResponseBase):
    """Fail-closed result with reasons and no grammar analysis."""

    outcome: Literal["unsupported"]
    analysis: Literal[None]
    warnings: list[ContractWarning] = Field(min_length=1, max_length=128)
    unsupported_reasons: list[UnsupportedReason] = Field(min_length=1, max_length=32)


PublicParserResponse = Annotated[
    DraftResponse | UncertainResponse | UnsupportedResponse,
    Field(discriminator="outcome"),
]

PUBLIC_RESPONSE_ADAPTER = TypeAdapter(PublicParserResponse)
