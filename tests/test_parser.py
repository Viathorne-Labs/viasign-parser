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
        "Assign a sign-name.",
        "Generate name signs.",
        "Assign sign names.",
        "Create a namesign.",
        "Invent my signname.",
        "What is a name sign?",
        "How are sign names discussed?",
        "What is a name–sign?",
        "Is name_sign different?",
        "How do I sign my name?",
        "What is my name in sign language?",
        "Explain a Singapore Sign Language name.",
        "How should my name be signed?",
        "What are names in SgSL?",
        "What is a name’s sign?",
        "Tell me which sign people use for my name.",
        "My name as an SgSL sign.",
        "They are signing my name.",
        "This sign is used when naming me.",
    ],
)
def test_name_sign_related_input_is_unsupported(text: str) -> None:
    result = parse_public(text)
    assert result.outcome == "unsupported"
    assert result.analysis is None
    assert result.input.model_dump() == {"mode": "natural"}
    assert result.warnings[0].code == "cultural_topic_not_supported"
    assert result.unsupported_reasons[0].code == "name_sign_boundary_blocked"
    assert result.review_required is True
    assert result.motion_ready is False


@pytest.mark.parametrize(
    "text",
    [
        "Please sign the form.",
        "A signature is required.",
    ],
)
def test_unrelated_uses_of_sign_remain_uncertain(text: str) -> None:
    result = parse_public(text)
    assert result.outcome == "uncertain"
    assert result.input.model_dump() == {"mode": "natural"}
    assert result.analysis is not None


def test_name_and_sign_lexical_cooccurrence_fails_closed_conservatively() -> None:
    result = parse_public("The sign names the room.")
    assert result.outcome == "unsupported"
    assert result.analysis is None


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
