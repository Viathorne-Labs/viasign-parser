import pytest

from viasign_parser.safety import UnsafeParserState, require_public_safety_invariants


def test_accepts_only_review_required_non_motion_result() -> None:
    require_public_safety_invariants(
        {"review_required": True, "motion_ready": False}
    )


@pytest.mark.parametrize(
    "result",
    [
        {},
        {"review_required": False, "motion_ready": False},
        {"review_required": True, "motion_ready": True},
        {"review_required": 1, "motion_ready": 0},
    ],
)
def test_rejects_unsafe_or_ambiguous_results(result: dict[str, object]) -> None:
    with pytest.raises(UnsafeParserState):
        require_public_safety_invariants(result)

