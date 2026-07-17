"""Build or verify the deterministic public release-candidate manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_RELATIVE_PATH = Path("provenance/v1/release-candidate-manifest.json")

PUBLIC_TOP_LEVEL_FILES = frozenset(
    {
        ".dockerignore",
        ".env.example",
        ".gitignore",
        "AGENTS.md",
        "ARCHITECTURE.md",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "Dockerfile",
        "LICENSE",
        "NOTICE",
        "README.md",
        "ROADMAP.md",
        "SECURITY.md",
        "pyproject.toml",
        "render.yaml",
        "requirements.lock",
    }
)
PUBLIC_DIRECTORIES = frozenset(
    {
        "contracts",
        "docs",
        "provenance",
        "scripts",
        "src",
        "tests",
    }
)
LOCAL_ONLY_DIRECTORIES = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "build",
        "dist",
    }
)
LOCAL_ONLY_NAMES = frozenset({".DS_Store"})
LOCAL_ONLY_SUFFIXES = frozenset({".pyc", ".pyo"})
LOCAL_ONLY_NAME_ENDINGS = (".local.md",)


class ReleaseBoundaryError(RuntimeError):
    """Raised when a local path is not accounted for by the public boundary."""


def _is_local_only(path: Path) -> bool:
    return (
        any(part in LOCAL_ONLY_DIRECTORIES or part == "__pycache__" for part in path.parts)
        or path.name in LOCAL_ONLY_NAMES
        or path.suffix in LOCAL_ONLY_SUFFIXES
        or path.name.endswith(LOCAL_ONLY_NAME_ENDINGS)
    )


def collect_release_files(root: Path = ROOT) -> tuple[Path, ...]:
    """Return every public file and fail on unaccounted workspace content."""

    release_files: list[Path] = []
    unaccounted: list[str] = []

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if _is_local_only(relative):
            continue
        if relative == MANIFEST_RELATIVE_PATH:
            continue
        if path.is_symlink():
            raise ReleaseBoundaryError(f"release candidate contains symlink: {relative}")
        if not path.is_file():
            continue

        top_level = relative.parts[0]
        if len(relative.parts) == 1:
            allowed = relative.name in PUBLIC_TOP_LEVEL_FILES
        else:
            allowed = top_level in PUBLIC_DIRECTORIES

        if allowed:
            release_files.append(relative)
        else:
            unaccounted.append(relative.as_posix())

    if unaccounted:
        rendered = ", ".join(unaccounted)
        raise ReleaseBoundaryError(f"unaccounted workspace files: {rendered}")
    return tuple(release_files)


def build_manifest(root: Path = ROOT) -> dict[str, object]:
    files: list[dict[str, object]] = []
    total_bytes = 0
    for relative in collect_release_files(root):
        content = (root / relative).read_bytes()
        total_bytes += len(content)
        files.append(
            {
                "path": relative.as_posix(),
                "sha256": hashlib.sha256(content).hexdigest(),
                "bytes": len(content),
            }
        )

    return {
        "manifest_version": "viasign.public-release-manifest.v1",
        "candidate_id": "viasign-parser-public-0.2.1-deployment-evidence-candidate",
        "snapshot_date": "2026-07-17",
        "status": "deployment_candidate_evidence_publication_authorized",
        "hash_algorithm": "sha256",
        "root": ".",
        "manifest_self_path": MANIFEST_RELATIVE_PATH.as_posix(),
        "manifest_self_hashed": False,
        "publication_authorized": True,
        "source_publication_authorized": True,
        "deployment_evidence_publication_authorized": True,
        "deployment_authorized": False,
        "inert_service_creation_authorized": True,
        "inert_service_created": True,
        "public_activation_authorized": False,
        "review_gates": {
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
        },
        "reviewed_deployment_source": {
            "repository": "https://github.com/Viathorne-Labs/viasign-parser",
            "branch": "main",
            "commit": "d88bc2664628135a04ee4961866fea2380e1343d",
            "parser_version": "0.2.1",
            "authorized_on": "2026-07-17",
        },
        "live_inert_service": {
            "commit": "e8ca6a688c6905fba1f2f02646b665623f0c689e",
            "parser_version": "0.2.0",
            "last_verified_on": "2026-07-17",
            "health_verified": True,
            "maintenance_mode": True,
            "cors_origins": "",
            "auto_deploy": False,
            "render_subdomain": "disabled",
            "custom_domain_status": "waiting_for_dns",
        },
        "deployment_candidate": {
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
        },
        "required_invariants": {
            "review_required": True,
            "motion_ready": False,
        },
        "summary": {
            "file_count": len(files),
            "total_bytes": total_bytes,
        },
        "files": files,
    }


def render_manifest(root: Path = ROOT) -> str:
    return json.dumps(build_manifest(root), indent=2, sort_keys=True) + "\n"


def check_manifest(root: Path = ROOT) -> None:
    manifest_path = root / MANIFEST_RELATIVE_PATH
    if not manifest_path.is_file():
        raise ReleaseBoundaryError(f"missing manifest: {MANIFEST_RELATIVE_PATH}")
    expected = render_manifest(root)
    actual = manifest_path.read_text(encoding="utf-8")
    if actual != expected:
        raise ReleaseBoundaryError(
            "release manifest is stale; regenerate and review it before release"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the checked-in manifest instead of printing a candidate",
    )
    arguments = parser.parse_args()
    if arguments.check:
        check_manifest()
        print("Release manifest check passed.")
        return
    print(render_manifest(), end="")


if __name__ == "__main__":
    main()
