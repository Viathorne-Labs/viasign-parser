from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).parents[1]
RECORD_PATH = ROOT / "provenance" / "v1" / "migration-candidates.json"


def _record() -> dict[str, object]:
    return json.loads(RECORD_PATH.read_text(encoding="utf-8"))


def test_provenance_record_covers_every_candidate() -> None:
    record = _record()
    candidates = record["candidates"]
    assert isinstance(candidates, list)
    assert {candidate["candidate_id"] for candidate in candidates} == {
        "package_marker",
        "parser_v2_implementation",
        "parser_v2_types",
        "lexicon",
        "runtime_demo",
    }


def test_private_candidates_are_not_approved_for_direct_copy() -> None:
    record = _record()
    candidates = record["candidates"]
    assert isinstance(candidates, list)
    for candidate in candidates:
        assert "approve_direct_copy" not in candidate["decision"]


def test_non_empty_candidates_keep_rights_confirmation_pending() -> None:
    record = _record()
    candidates = record["candidates"]
    assert isinstance(candidates, list)
    for candidate in candidates:
        if candidate["byte_count"]:
            assert candidate["rights_confirmation"] == "pending_owner_attestation"


def test_fingerprints_and_relative_paths_are_well_formed() -> None:
    record = _record()
    candidates = record["candidates"]
    assert isinstance(candidates, list)
    for candidate in candidates:
        assert re.fullmatch(r"[0-9a-f]{64}", candidate["sha256"])
        assert re.fullmatch(r"[0-9a-f]{40}", candidate["git_blob_sha1"])
        assert not candidate["source_relative_path"].startswith("/")


def test_record_does_not_contain_personal_or_absolute_source_identity() -> None:
    record_text = RECORD_PATH.read_text(encoding="utf-8")
    assert "/Users/" not in record_text
    assert "@" not in record_text
    privacy = _record()["privacy"]
    assert privacy == {
        "absolute_paths_recorded": False,
        "author_names_recorded": False,
        "author_emails_recorded": False,
        "private_content_embedded": False,
    }

