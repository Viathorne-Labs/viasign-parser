"""Audit public release paths for binary, secret, and local-boundary leaks."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

if __package__:
    from scripts.release_manifest import (
        MANIFEST_RELATIVE_PATH,
        ROOT,
        collect_release_files,
    )
else:
    from release_manifest import MANIFEST_RELATIVE_PATH, ROOT, collect_release_files


FORBIDDEN_BINARY_SUFFIXES = frozenset(
    {
        ".7z",
        ".avi",
        ".db",
        ".doc",
        ".docx",
        ".gif",
        ".gz",
        ".jpeg",
        ".jpg",
        ".m4a",
        ".mkv",
        ".mov",
        ".mp3",
        ".mp4",
        ".onnx",
        ".pdf",
        ".png",
        ".ppt",
        ".pptx",
        ".safetensors",
        ".sqlite",
        ".tar",
        ".wav",
        ".webm",
        ".webp",
        ".xls",
        ".xlsx",
        ".zip",
    }
)
LOCAL_PATH_PATTERNS = (
    re.compile("/" + r"Users/[^\s'\"`]+"),
    re.compile("/" + r"home/[^\s'\"`]+"),
    re.compile(r"[A-Za-z]:\\Users\\[^\s'\"`]+"),
    re.compile(r"(?:file|vscode)://", re.IGNORECASE),
)
SECRET_PATTERNS = (
    ("private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b")),
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("render_key", re.compile(r"\brnd_[A-Za-z0-9_-]{20,}\b")),
    (
        "assigned_secret",
        re.compile(
            r"(?i)\b(?:api[_-]?key|password|secret|token)\b\s*[:=]\s*"
            r"['\"][^'\"\s]{8,}['\"]"
        ),
    ),
)
FORBIDDEN_IMPORT_ROOTS = frozenset(
    {
        "SGSL_AI_DEV",
        "TempleConsole",
        "motion_engine_avatar",
        "sgsl",
    }
)


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    path: str
    detail: str


def _python_import_roots(text: str, path: Path) -> set[str]:
    try:
        tree = ast.parse(text, filename=path.as_posix())
    except SyntaxError:
        return set()
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".", 1)[0])
    return roots


def audit_release_candidate(root: Path = ROOT) -> tuple[Finding, ...]:
    findings: list[Finding] = []
    release_paths = list(collect_release_files(root))
    if (root / MANIFEST_RELATIVE_PATH).is_file():
        release_paths.append(MANIFEST_RELATIVE_PATH)

    for relative in release_paths:
        path = root / relative
        label = relative.as_posix()
        content = path.read_bytes()

        if relative.suffix.lower() in FORBIDDEN_BINARY_SUFFIXES:
            findings.append(Finding("forbidden_binary_type", label, relative.suffix))
        if b"\x00" in content:
            findings.append(Finding("nul_byte", label, "file contains a NUL byte"))
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            findings.append(Finding("non_utf8", label, "file is not UTF-8 text"))
            continue

        for pattern in LOCAL_PATH_PATTERNS:
            if match := pattern.search(text):
                findings.append(Finding("local_path", label, match.group(0)))
        for code, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(Finding(code, label, "credential-shaped value"))

        if relative.suffix == ".py":
            forbidden = _python_import_roots(text, relative) & FORBIDDEN_IMPORT_ROOTS
            for import_root in sorted(forbidden):
                findings.append(Finding("private_import", label, import_root))

    return tuple(findings)


def main() -> None:
    findings = audit_release_candidate()
    if findings:
        for finding in findings:
            print(f"{finding.code}: {finding.path}: {finding.detail}")
        raise SystemExit(1)
    file_count = len(collect_release_files())
    if (ROOT / MANIFEST_RELATIVE_PATH).is_file():
        file_count += 1
    print(
        "Release-boundary audit passed: "
        f"{file_count} allowlisted UTF-8 files, no credential-shaped values, "
        "local paths, binary payloads, or private imports."
    )


if __name__ == "__main__":
    main()
