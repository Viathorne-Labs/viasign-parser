from __future__ import annotations

import pytest

from viasign_parser.contracts import PUBLIC_RESPONSE_ADAPTER
from viasign_parser.parser import PARSER_VERSION, RULESET_VERSION, parse_public


def test_generic_question_is_uncertain_and_has_no_candidate_signing() -> None:
    result = parse_public("Is the community room open?")
    assert result.outcome == "uncertain"
    assert result.analysis.intent == "question"
    assert result.analysis.surface.model_dump() == {
        "sentence_kind": "question",
        "question_kind": "yes_no",
        "question_category": "none",
        "negation_cue": "absent",
    }
    assert result.analysis.sign_aware_form is None
    assert result.analysis.candidate_glosses == []
    assert result.warnings[0].code == "sgsl_grammar_rules_unavailable"


def test_generic_statement_reports_only_source_surface_categories() -> None:
    result = parse_public("A visitor waits near the garden.")
    assert result.outcome == "uncertain"
    assert result.analysis.intent == "statement"
    assert result.analysis.surface.model_dump() == {
        "sentence_kind": "statement",
        "question_kind": "not_applicable",
        "question_category": "none",
        "negation_cue": "absent",
    }
    assert result.analysis.sign_aware_form is None
    assert result.analysis.candidate_glosses == []


@pytest.mark.parametrize(
    "text",
    [
        "Please create a name sign for me.",
        "Can this tool assign a name-sign?",
        "Generate my name sign.",
    ],
)
def test_name_sign_generation_is_unsupported(text: str) -> None:
    result = parse_public(text)
    assert result.outcome == "unsupported"
    assert result.analysis is None
    assert result.input.model_dump() == {"mode": "natural"}
    assert result.unsupported_reasons[0].code == "name_sign_generation_blocked"


def test_name_sign_information_question_is_not_treated_as_generation() -> None:
    result = parse_public("What is a name sign?")
    assert result.outcome == "uncertain"
    assert result.input.model_dump() == {"mode": "natural"}
    assert result.analysis.intent == "question"
    assert result.analysis.surface.question_kind == "wh"
    assert result.analysis.surface.question_category == "what"


@pytest.mark.parametrize(
    "text",
    ["Is the community room open?", "Please create a name sign for me."],
)
def test_every_result_matches_contract_and_safety_literals(text: str) -> None:
    result = parse_public(text)
    payload = PUBLIC_RESPONSE_ADAPTER.dump_python(result, mode="json")
    PUBLIC_RESPONSE_ADAPTER.validate_python(payload)
    assert payload["review_required"] is True
    assert payload["motion_ready"] is False
    assert payload["provenance"]["parser_version"] == PARSER_VERSION
    assert payload["provenance"]["ruleset_version"] == RULESET_VERSION


def test_serialized_analysis_contains_categories_but_no_input_values() -> None:
    submitted_text = "Which private-shaped lantern is not visible?"

    result = parse_public(submitted_text)
    payload = PUBLIC_RESPONSE_ADAPTER.dump_python(result, mode="json")

    assert payload["analysis"]["surface"] == {
        "sentence_kind": "question",
        "question_kind": "wh",
        "question_category": "which",
        "negation_cue": "present",
    }
    assert submitted_text not in str(payload)
    assert "private-shaped" not in str(payload)
    assert "lantern" not in str(payload)
    assert "visible" not in str(payload)
