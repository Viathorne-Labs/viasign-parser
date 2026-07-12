"""Minimal clean-room public surface analyzer.

This module intentionally implements no SgSL grammar rules. It exposes visible
uncertainty for ordinary input and blocks name-sign generation requests without
producing plausible-looking linguistic output.
"""

from __future__ import annotations

import re

from .api_models import ParseRequest
from .contracts import (
    CONTRACT_VERSION,
    SCHEMA_VERSION,
    ContractProvenance,
    ContractWarning,
    GrammarAnalysis,
    InputMetadata,
    UncertainResponse,
    UnsupportedReason,
    UnsupportedResponse,
)
from .surface import analyze_surface


PARSER_VERSION = "0.2.0"
RULESET_VERSION = "public-surface-only-v1"

_NAME_SIGN_PATTERN = re.compile(r"\bname[\s-]+sign\b", re.IGNORECASE)
_GENERATION_ACTIONS = frozenset(
    {
        "assign",
        "create",
        "generate",
        "give",
        "invent",
        "make",
    }
)
_WORD_PATTERN = re.compile(r"[a-z]+", re.IGNORECASE)


def _provenance() -> ContractProvenance:
    return ContractProvenance(
        parser_id="viasign-parser",
        parser_version=PARSER_VERSION,
        ruleset_version=RULESET_VERSION,
        contract_version=CONTRACT_VERSION,
    )


def _requests_name_sign_generation(text: str) -> bool:
    if not _NAME_SIGN_PATTERN.search(text):
        return False
    words = {word.casefold() for word in _WORD_PATTERN.findall(text)}
    return not words.isdisjoint(_GENERATION_ACTIONS)


def parse_public(text: str) -> UncertainResponse | UnsupportedResponse:
    """Return a contract-valid result without inferring unreviewed grammar."""

    normalized_text = ParseRequest(text=text).text
    input_metadata = InputMetadata(mode="natural")

    if _requests_name_sign_generation(normalized_text):
        return UnsupportedResponse(
            schema_version=SCHEMA_VERSION,
            outcome="unsupported",
            status="review_required",
            input=input_metadata,
            analysis=None,
            warnings=[
                ContractWarning(
                    code="cultural_action_not_supported",
                    message="The public parser does not create or assign name signs.",
                    field="request.text",
                    review_state="review_required",
                )
            ],
            unsupported_reasons=[
                UnsupportedReason(
                    code="name_sign_generation_blocked",
                    message=(
                        "Name-sign creation requires appropriate human and "
                        "community processes."
                    ),
                )
            ],
            review_required=True,
            motion_ready=False,
            provenance=_provenance(),
        )

    surface = analyze_surface(normalized_text)
    return UncertainResponse(
        schema_version=SCHEMA_VERSION,
        outcome="uncertain",
        status="review_required",
        input=input_metadata,
        analysis=GrammarAnalysis(
            intent=surface.sentence_kind,
            surface=surface,
            sign_aware_form=None,
            candidate_glosses=[],
        ),
        warnings=[
            ContractWarning(
                code="sgsl_grammar_rules_unavailable",
                message=(
                    "Surface categories are not SgSL grammar, translation, "
                    "or signing output."
                ),
                field="analysis",
                review_state="review_required",
            )
        ],
        review_required=True,
        motion_ready=False,
        provenance=_provenance(),
    )
