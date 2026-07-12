import json
import tomllib

from scripts.audit_release_candidate import audit_release_candidate
from scripts.release_manifest import (
    MANIFEST_RELATIVE_PATH,
    ROOT,
    build_manifest,
    check_manifest,
    collect_release_files,
)


def test_release_candidate_contains_only_accounted_regular_files() -> None:
    paths = collect_release_files()

    assert paths
    assert len(paths) == len(set(paths))
    assert all((ROOT / path).is_file() for path in paths)
    assert all(not (ROOT / path).is_symlink() for path in paths)
    assert MANIFEST_RELATIVE_PATH not in paths
    assert {
        "AGENTS.md",
        "ARCHITECTURE.md",
        "ROADMAP.md",
    }.issubset({path.as_posix() for path in paths})


def test_private_local_markdown_notes_are_excluded(tmp_path) -> None:
    (tmp_path / "coordination.local.md").write_text(
        "private local note",
        encoding="utf-8",
    )

    assert collect_release_files(tmp_path) == ()


def test_release_manifest_is_exact_and_keeps_release_blocked() -> None:
    check_manifest()
    manifest = json.loads((ROOT / MANIFEST_RELATIVE_PATH).read_text(encoding="utf-8"))
    generated = build_manifest()

    assert manifest == generated
    assert manifest["publication_authorized"] is False
    assert manifest["deployment_authorized"] is False
    assert manifest["required_invariants"] == {
        "review_required": True,
        "motion_ready": False,
    }
    assert manifest["summary"]["file_count"] == len(manifest["files"])


def test_release_candidate_has_no_boundary_findings() -> None:
    assert audit_release_candidate() == ()


def test_package_uses_current_spdx_and_includes_public_notices() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = metadata["project"]

    assert project["license"] == "Apache-2.0"
    assert project["license-files"] == ["LICENSE", "NOTICE"]
    assert all(
        not classifier.startswith("License ::")
        for classifier in project["classifiers"]
    )


def test_changed_candidate_owner_review_remains_explicitly_unapproved() -> None:
    packet = (ROOT / "docs/OWNER_REVIEW_PACKET_V2.md").read_text(encoding="utf-8")

    assert "owner approval not yet recorded" in packet
    assert packet.count("- [ ] I ") == 5
    assert "does not authorize" in packet
