"""Independent, non-linguistic surface observations for natural English.

This module does not produce SgSL grammar, glosses, signs, or motion. Its
closed categories describe only obvious source-text form while avoiding any
verbatim text in the public response.
"""

from __future__ import annotations

import re

from .contracts import SurfaceAnalysis


_WORD_PATTERN = re.compile(r"[a-z]+(?:'[a-z]+)?", re.IGNORECASE)

_QUESTION_CATEGORIES = {
    "what": "what",
    "who": "who",
    "whose": "whose",
    "why": "why",
    "how": "how",
    "where": "where",
    "which": "which",
    "when": "when",
}

_YES_NO_OPENERS = frozenset(
    {
        "are",
        "can",
        "could",
        "did",
        "do",
        "does",
        "has",
        "have",
        "is",
        "should",
        "was",
        "were",
        "will",
        "would",
    }
)

_CLEAR_NEGATION_CUES = frozenset({"cannot", "never", "not"})
_AMBIGUOUS_NEGATION_CUES = frozenset({"no", "without"})


def analyze_surface(text: str) -> SurfaceAnalysis:
    """Return closed surface categories without returning submitted values."""

    words = [match.group(0).casefold() for match in _WORD_PATTERN.finditer(text)]
    first_word = words[0] if words else None
    ends_with_question_mark = text.rstrip().endswith("?")

    question_category = _QUESTION_CATEGORIES.get(first_word or "", "none")
    begins_with_yes_no_opener = first_word in _YES_NO_OPENERS
    looks_like_question = (
        ends_with_question_mark
        or question_category != "none"
        or begins_with_yes_no_opener
    )

    if looks_like_question:
        sentence_kind = "question"
        if question_category != "none":
            question_kind = "wh"
        elif begins_with_yes_no_opener:
            question_kind = "yes_no"
        else:
            question_kind = "unknown"
    elif text.rstrip().endswith((".", "!")):
        sentence_kind = "statement"
        question_kind = "not_applicable"
    else:
        sentence_kind = "unknown"
        question_kind = "not_applicable"

    has_clear_negation = any(
        word in _CLEAR_NEGATION_CUES or word.endswith("n't") for word in words
    )
    has_ambiguous_negation = any(
        word in _AMBIGUOUS_NEGATION_CUES for word in words
    )
    if has_clear_negation:
        negation_cue = "present"
    elif has_ambiguous_negation:
        negation_cue = "ambiguous"
    else:
        negation_cue = "absent"

    return SurfaceAnalysis(
        sentence_kind=sentence_kind,
        question_kind=question_kind,
        question_category=question_category,
        negation_cue=negation_cue,
    )
