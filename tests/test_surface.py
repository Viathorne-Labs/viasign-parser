from __future__ import annotations

import pytest

from viasign_parser.surface import analyze_surface


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "Which lantern is displayed?",
            {
                "sentence_kind": "question",
                "question_kind": "wh",
                "question_category": "which",
                "negation_cue": "absent",
            },
        ),
        (
            "Would the paper bridge hold?",
            {
                "sentence_kind": "question",
                "question_kind": "yes_no",
                "question_category": "none",
                "negation_cue": "absent",
            },
        ),
        (
            "Maybe the painted door?",
            {
                "sentence_kind": "question",
                "question_kind": "unknown",
                "question_category": "none",
                "negation_cue": "absent",
            },
        ),
        (
            "The copper kite is not available.",
            {
                "sentence_kind": "statement",
                "question_kind": "not_applicable",
                "question_category": "none",
                "negation_cue": "present",
            },
        ),
        (
            "No lantern",
            {
                "sentence_kind": "unknown",
                "question_kind": "not_applicable",
                "question_category": "none",
                "negation_cue": "ambiguous",
            },
        ),
        (
            "A quiet paper garden",
            {
                "sentence_kind": "unknown",
                "question_kind": "not_applicable",
                "question_category": "none",
                "negation_cue": "absent",
            },
        ),
    ],
)
def test_surface_categories_are_deterministic(
    text: str,
    expected: dict[str, str],
) -> None:
    assert analyze_surface(text).model_dump() == expected


@pytest.mark.parametrize(
    ("question_word", "category"),
    [
        ("What", "what"),
        ("Who", "who"),
        ("Whose", "whose"),
        ("Why", "why"),
        ("How", "how"),
        ("Where", "where"),
        ("Which", "which"),
        ("When", "when"),
    ],
)
def test_generic_question_categories_are_closed(
    question_word: str,
    category: str,
) -> None:
    result = analyze_surface(f"{question_word}?")

    assert result.sentence_kind == "question"
    assert result.question_kind == "wh"
    assert result.question_category == category


def test_surface_analysis_never_contains_submitted_values() -> None:
    submitted_text = "Why isn't private-token-72 visible?"

    serialized = analyze_surface(submitted_text).model_dump_json()

    assert "private-token-72" not in serialized
    assert "visible" not in serialized
