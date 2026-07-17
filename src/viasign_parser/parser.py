"""Minimal clean-room public surface analyzer.

This module intentionally implements no SgSL grammar rules. It exposes visible
uncertainty for ordinary input and blocks recognized name-sign-related input
without producing plausible-looking linguistic output.
"""

from __future__ import annotations

import re
import unicodedata

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


PARSER_VERSION = "0.2.1"
RULESET_VERSION = "public-surface-only-v1"

_NAME_SIGN_COMPOUND_PATTERN = re.compile(
    r"\b(?:name[\W_]*signs?|sign[\W_]*names?)\b"
)
_NAME_WORD_PATTERN = re.compile(r"\bnam(?:e(?:s|d|['’]s)?|ing)\b")
_SIGN_CONTEXT_PATTERN = re.compile(r"\b(?:sign(?:s|ed|ing)?|sgsl)\b")


def _provenance() -> ContractProvenance:
    return ContractProvenance(
        parser_id="viasign-parser",
        parser_version=PARSER_VERSION,
        ruleset_version=RULESET_VERSION,
        contract_version=CONTRACT_VERSION,
    )


def _mentions_name_sign(text: str) -> bool:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    if _NAME_SIGN_COMPOUND_PATTERN.search(normalized):
        return True
    return bool(
        _NAME_WORD_PATTERN.search(normalized)
        and _SIGN_CONTEXT_PATTERN.search(normalized)
    )


def parse_public(text: str) -> UncertainResponse | UnsupportedResponse:
    """Return a contract-valid result without inferring unreviewed grammar."""

    normalized_text = ParseRequest(text=text).text
    input_metadata = InputMetadata(mode="natural")

    if _mentions_name_sign(normalized_text):
        return UnsupportedResponse(
            schema_version=SCHEMA_VERSION,
            outcome="unsupported",
            status="review_required",
            input=input_metadata,
            analysis=None,
            warnings=[
                ContractWarning(
                    code="cultural_topic_not_supported",
                    message=(
                        "The public parser does not analyze, create, assign, "
                        "or propose name signs."
                    ),
                    field="request.text",
                    review_state="review_required",
                )
            ],
            unsupported_reasons=[
                UnsupportedReason(
                    code="name_sign_boundary_blocked",
                    message=(
                        "Name-sign topics require appropriate human and community "
                        "processes."
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
