"""Minimal clean-room public parser implementation.

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


PARSER_VERSION = "0.1.0"
RULESET_VERSION = "public-safety-only-v1"

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

    surface_intent = "question" if normalized_text.endswith("?") else "unknown"
    return UncertainResponse(
        schema_version=SCHEMA_VERSION,
        outcome="uncertain",
        status="review_required",
        input=input_metadata,
        analysis=GrammarAnalysis(
            intent=surface_intent,
            sign_aware_form=None,
            candidate_glosses=[],
        ),
        warnings=[
            ContractWarning(
                code="public_grammar_rules_not_implemented",
                message=(
                    "The clean-room public ruleset does not yet produce "
                    "SgSL-aware grammar planning."
                ),
                field="analysis",
                review_state="review_required",
            )
        ],
        review_required=True,
        motion_ready=False,
        provenance=_provenance(),
    )
