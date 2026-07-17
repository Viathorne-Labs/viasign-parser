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


def test_release_manifest_records_evidence_publication_and_blocks_deployment() -> None:
    check_manifest()
    manifest = json.loads((ROOT / MANIFEST_RELATIVE_PATH).read_text(encoding="utf-8"))
    generated = build_manifest()

    assert manifest == generated
    assert manifest["candidate_id"] == (
        "viasign-parser-public-0.2.1-deployment-evidence-candidate"
    )
    assert manifest["status"] == "deployment_candidate_evidence_publication_authorized"
    assert manifest["publication_authorized"] is True
    assert manifest["source_publication_authorized"] is True
    assert manifest["deployment_evidence_publication_authorized"] is True
    assert manifest["deployment_authorized"] is False
    assert manifest["inert_service_creation_authorized"] is True
    assert manifest["inert_service_created"] is True
    assert manifest["public_activation_authorized"] is False
    assert manifest["review_gates"] == {
        "repository_owner_deployment_evidence_publication": {
            "status": "complete",
            "recorded_on": "2026-07-17",
            "items_approved": 5,
        },
        "repository_owner_enabled_flow_wording": {
            "status": "complete",
            "recorded_on": "2026-07-17",
            "items_approved": 5,
        },
        "deaf_sgsl_community": "pending",
        "security_privacy_deployment": "pending",
        "website_defense_in_depth": "pending",
    }
    assert manifest["reviewed_deployment_source"] == {
        "repository": "https://github.com/Viathorne-Labs/viasign-parser",
        "branch": "main",
        "commit": "d88bc2664628135a04ee4961866fea2380e1343d",
        "parser_version": "0.2.1",
        "authorized_on": "2026-07-17",
    }
    assert manifest["live_inert_service"] == {
        "commit": "e8ca6a688c6905fba1f2f02646b665623f0c689e",
        "parser_version": "0.2.0",
        "last_verified_on": "2026-07-17",
        "health_verified": True,
        "maintenance_mode": True,
        "cors_origins": "",
        "auto_deploy": False,
        "render_subdomain": "disabled",
        "custom_domain_status": "waiting_for_dns",
    }
    assert manifest["deployment_candidate"] == {
        "source_commit": "d88bc2664628135a04ee4961866fea2380e1343d",
        "parser_version": "0.2.1",
        "reviewed_on": "2026-07-17",
        "provider_state_refreshed": True,
        "local_artifact_review": "complete",
        "deployment_update_authorized": False,
        "deployment_method": "specific_commit",
        "deploy_latest_commit_allowed": False,
        "deploy_hook_rotation_status": "pending",
        "arm64_image_id": (
            "sha256:61a6f7b9178b19d3dbc580702764a237b820a23be6a331e72acf582e3106f58d"
        ),
        "amd64_image_id": (
            "sha256:55f5a6b41791527e28c5a393061a2d13b79efa487f257be058d51dfb2b48219d"
        ),
    }
    assert manifest["required_invariants"] == {
        "review_required": True,
        "motion_ready": False,
    }
    assert manifest["summary"]["file_count"] == len(manifest["files"])


def test_release_candidate_has_no_boundary_findings() -> None:
    assert audit_release_candidate() == ()


def test_local_tester_review_records_separate_source_only_authorization() -> None:
    review = (ROOT / "docs/LOCAL_TESTER_REVIEW_V1.md").read_text(encoding="utf-8")

    assert "human accessibility and repository-owner wording reviews complete" in review
    assert "broader reviews pending" in review
    assert "Human accessibility check:** 2026-07-17" in review
    assert "Repository-owner wording review:** 2026-07-17" in review
    assert "Source-publication approval:** 2026-07-17" in review
    assert "approved for\nsource publication in parser PR #4" in review
    assert "all recognized name-sign-related input is\nunsupported" in review
    assert "completed\nrepresentative `viathorne-web` accessibility baseline" in review
    assert "bounded human accessibility pass" in review
    assert "native 200 percent\nzoom" in review
    assert "Safari with VoiceOver read the\nrequested ready, checking" in review
    assert "unavailable-state VoiceOver path was not part of this human pass" in review
    assert "Keep the tester described as local and not publicly enabled" in review
    assert "limited natural-English surface analysis" in review
    assert "hosting providers may process technical\n   network metadata" in review
    assert "research toward future SgSL support" in review
    assert "Apache-2.0 permits use, modification, and redistribution" in review
    assert "is not broader Deaf/SgSL community\napproval" in review
    assert "separately approved source publication and merge of parser PR #4" in review
    assert "f12b2b9b4b16e89e9a92a544da0a7101af5d5e2f" in review
    assert "This approval is source-publication-only" in review
    assert "review_required=true" in review
    assert "motion_ready=false" in review
    assert "Public activation:** Blocked" in review
    assert "authorize source publication\nand merge of parser PR #4 only" in review
    assert "do not authorize a Render update" in review
    assert "visitor submissions, or public activation" in review


def test_source_approval_does_not_close_broader_or_deployment_review() -> None:
    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    checklist = (ROOT / "docs/RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
    deployment_gate = (ROOT / "docs/PRODUCTION_DEPLOYMENT_GATE.md").read_text(
        encoding="utf-8"
    )

    assert "[x] Complete repository-owner review" in roadmap
    assert "[x] Obtain repository-owner approval before publishing" in roadmap
    assert "[ ] Broader Deaf/SgSL community review" in checklist
    assert "[x] Repository-owner review of the enabled flow" in checklist
    assert "[x] The local tester safety correction" in checklist
    assert "[ ] Security and privacy deployment review" in deployment_gate
    assert "[ ] Broader Deaf/SgSL community reviewers" in deployment_gate
    assert "[ ] Website defense in depth pins" in deployment_gate
    assert "Exact published source commit `d88bc266` passed" in deployment_gate
    assert "[ ] A later, separate provider-mutation approval" in deployment_gate
    assert "public activation blocked" in deployment_gate


def test_exact_candidate_review_keeps_render_update_blocked() -> None:
    checklist = (ROOT / "docs/RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
    inert_audit = (ROOT / "docs/INERT_RENDER_SERVICE_AUDIT_V1.md").read_text(
        encoding="utf-8"
    )

    assert "exact parser `0.2.1` local" in checklist
    assert "[ ] After rotation, update the inert service" in checklist
    assert "evidence received explicit\n  publication approval" in checklist
    assert "regenerate the deploy hook" in checklist
    assert "Deploy a specific commit" in checklist
    assert "Deploy latest commit" in checklist
    assert "The live service still runs commit" in inert_audit
    assert "parser `0.2.0`" in inert_audit
    assert "Updating the\ninert service requires a separate explicit approval" in inert_audit
    assert "VIASIGN_CORS_ORIGINS` is the empty string" in inert_audit
    assert "must be\nregenerated before any later deployment update" in inert_audit
    assert "authorize no\nRender update" in (
        ROOT / "docs/CONTAINER_SECURITY_REVIEW.md"
    ).read_text(encoding="utf-8")


def test_package_uses_current_spdx_and_includes_public_notices() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = metadata["project"]

    assert project["license"] == "Apache-2.0"
    assert project["license-files"] == ["LICENSE", "NOTICE"]
    assert all(
        not classifier.startswith("License ::")
        for classifier in project["classifiers"]
    )


def test_changed_candidate_owner_review_records_source_approval_only() -> None:
    packet = (ROOT / "docs/OWNER_REVIEW_PACKET_V2.md").read_text(encoding="utf-8")

    assert "Owner approval recorded; source published" in packet
    assert packet.count("- [x] I ") == 5
    assert "did not authorize Render deployment" in packet
