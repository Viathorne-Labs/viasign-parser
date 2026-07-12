from pathlib import Path


BANNED_SOURCE_MARKERS = (
    "SGSL_AI_DEV",
    "motion_engine_avatar",
    "runtime.sign_event_loop",
    "sgsl.sgsl_parser",
    "teacher_mode",
)


def test_public_package_has_no_private_source_markers() -> None:
    package_root = Path(__file__).parents[1] / "src" / "viasign_parser"
    source = "\n".join(
        path.read_text(encoding="utf-8") for path in package_root.glob("*.py")
    )
    for marker in BANNED_SOURCE_MARKERS:
        assert marker not in source

