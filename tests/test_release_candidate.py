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


def test_release_manifest_records_consumed_inert_deployment_and_blocks_activation() -> None:
    check_manifest()
    manifest = json.loads((ROOT / MANIFEST_RELATIVE_PATH).read_text(encoding="utf-8"))
    generated = build_manifest()

    assert manifest == generated
    assert manifest["candidate_id"] == (
        "viasign-parser-public-0.2.1-inert-deployment-evidence-candidate"
    )
    assert manifest["status"] == "inert_deployment_evidence_publication_authorized"
    assert manifest["publication_authorized"] is True
    assert manifest["source_publication_authorized"] is True
    assert manifest["deployment_evidence_publication_authorized"] is True
    assert manifest["inert_deployment_evidence_publication_authorized"] is True
    assert manifest["deployment_authorized"] is False
    assert manifest["deployment_authorization"] == {
        "status": "consumed",
        "authorized_on": "2026-07-17",
        "authorized_commit": "d88bc2664628135a04ee4961866fea2380e1343d",
        "actions": [
            "regenerate_deploy_hook",
            "deploy_specific_commit",
        ],
        "additional_provider_changes_authorized": False,
    }
    assert manifest["inert_service_creation_authorized"] is True
    assert manifest["inert_service_created"] is True
    assert manifest["public_activation_authorized"] is False
    assert manifest["review_gates"] == {
        "repository_owner_inert_deployment": {
            "status": "complete",
            "recorded_on": "2026-07-17",
            "items_approved": 2,
        },
        "repository_owner_inert_deployment_evidence_publication": {
            "status": "complete",
            "recorded_on": "2026-07-17",
            "scope": "post_deployment_evidence_only",
        },
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
    assert manifest["published_deployment_evidence"] == {
        "repository": "https://github.com/Viathorne-Labs/viasign-parser",
        "branch": "main",
        "pull_request": 5,
        "commit": "d6c59f7c0c9b1e00aad2b73e42cebfb38ff2d172",
        "merged_on": "2026-07-17",
    }
    assert manifest["live_inert_service"] == {
        "commit": "d88bc2664628135a04ee4961866fea2380e1343d",
        "parser_version": "0.2.1",
        "deployment_id": "dep-d9d4kfn41pts73djkc20",
        "previous_live_commit": "e8ca6a688c6905fba1f2f02646b665623f0c689e",
        "last_verified_on": "2026-07-17",
        "health_verified": True,
        "metadata_verified": True,
        "maintenance_mode": True,
        "cors_origins": "",
        "auto_deploy": False,
        "pr_previews": False,
        "render_subdomain": "disabled",
        "render_subdomain_health_status": 404,
        "custom_domain_status": "waiting_for_dns",
        "website_tester_status": "not_configured",
    }
    assert manifest["deployment_candidate"] == {
        "source_commit": "d88bc2664628135a04ee4961866fea2380e1343d",
        "parser_version": "0.2.1",
        "reviewed_on": "2026-07-17",
        "provider_state_refreshed": True,
        "local_artifact_review": "complete",
        "deployment_update_authorized": False,
        "deployment_authorization_consumed": True,
        "deployment_method": "specific_commit",
        "deploy_latest_commit_allowed": False,
        "deploy_hook_rotation_status": "rotated_value_not_recorded",
        "deployment_id": "dep-d9d4kfn41pts73djkc20",
        "deployment_status": "live",
        "deployed_on": "2026-07-17",
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
    assert (
        "[x] A later, separate provider-mutation approval authorized"
        in deployment_gate
    )
    assert "is now consumed, permitting no additional provider" in deployment_gate
    assert "public activation blocked" in deployment_gate


def test_inert_deployment_evidence_keeps_public_activation_blocked() -> None:
    checklist = (ROOT / "docs/RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
    inert_audit = (ROOT / "docs/INERT_RENDER_SERVICE_AUDIT_V1.md").read_text(
        encoding="utf-8"
    )

    assert "exact parser `0.2.1` local" in checklist
    assert "[x] After rotation, the inert service was updated" in checklist
    assert "evidence received explicit\n  publication approval" in checklist
    assert "deploy hook was regenerated" in checklist
    assert "Deploy a specific commit" in checklist
    assert "Deploy latest commit" in checklist
    assert "authorization is consumed and permits no\n  additional provider mutation" in checklist
    assert "deployment `dep-d9d4kfn41pts73djkc20`" in inert_audit
    assert "parser_version=0.2.1" in inert_audit
    assert "review_required=true motion_ready=false" in inert_audit
    assert "separately approved publication of this post-deployment evidence" in inert_audit
    assert "does not authorize public activation or any provider change" in inert_audit
    assert "[x] The exact post-deployment evidence received separate" in checklist
    assert "VIASIGN_CORS_ORIGINS` is the empty string" in inert_audit
    assert "Neither the prior nor rotated\nhook value was copied, recorded, or invoked" in inert_audit
    assert "authorize no\nRender update" in (
        ROOT / "docs/CONTAINER_SECURITY_REVIEW.md"
    ).read_text(encoding="utf-8")


def test_durable_hosting_records_track_live_inert_artifact_and_rollback() -> None:
    edge_policy = (ROOT / "docs/EDGE_AND_OPERATIONS_POLICY.md").read_text(
        encoding="utf-8"
    )
    hosting_decision = (ROOT / "docs/RENDER_HOSTING_DECISION.md").read_text(
        encoding="utf-8"
    )
    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")

    for record in (edge_policy, hosting_decision):
        assert "d88bc2664628135a04ee4961866fea2380e1343d" in record
        assert "parser `0.2.1`" in record
        assert "e8ca6a688c6905fba1f2f02646b665623f0c689e" in record
        assert "rollback candidate" in record

    assert "exact live\n  parser `0.2.1` at `d88bc266`" in roadmap
    assert "rollback rehearsal to `e8ca6a6`" in roadmap


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
