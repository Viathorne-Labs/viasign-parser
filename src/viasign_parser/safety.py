"""Fail-closed checks that future parser adapters must pass."""

from __future__ import annotations

from collections.abc import Mapping


class UnsafeParserState(RuntimeError):
    """Raised when a parser result violates the public safety contract."""


def require_public_safety_invariants(result: Mapping[str, object]) -> None:
    """Reject results that could be mistaken for approved or motion-ready data."""

    if result.get("review_required") is not True:
        raise UnsafeParserState("parser result must require review")
    if result.get("motion_ready") is not False:
        raise UnsafeParserState("parser result must not be motion-ready")
