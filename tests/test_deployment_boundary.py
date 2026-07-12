from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]


def test_container_is_non_root_and_copies_only_public_runtime_source() -> None:
    dockerfile = (REPOSITORY_ROOT / "Dockerfile").read_text(encoding="utf-8")

    assert "USER 10001:10001" in dockerfile
    assert "COPY src ./src" in dockerfile
    assert "COPY --chown" not in dockerfile
    assert "COPY ." not in dockerfile
    assert "--no-access-log" in dockerfile
    assert "--no-server-header" in dockerfile
    assert "HEALTHCHECK" in dockerfile
    assert "http://127.0.0.1:10000/healthz" in dockerfile


def test_render_blueprint_is_inert_until_explicit_review() -> None:
    blueprint = (REPOSITORY_ROOT / "render.yaml").read_text(encoding="utf-8")

    assert "region: singapore" in blueprint
    assert "plan: starter" in blueprint
    assert "numInstances: 1" in blueprint
    assert 'autoDeployTrigger: "off"' in blueprint
    assert "domains:\n      - api.viathorne.com" in blueprint
    assert "renderSubdomainPolicy: disabled" in blueprint
    assert "enabled: true" in blueprint
    assert 'key: VIASIGN_CORS_ORIGINS\n        value: ""' in blueprint
    assert 'key: VIASIGN_TRUST_RENDER_PROXY\n        value: "true"' in blueprint
    assert "previews:" not in blueprint
    assert "disk:" not in blueprint
    assert "scaling:" not in blueprint


def test_production_origin_policy_is_exact_and_not_activated() -> None:
    policy = (REPOSITORY_ROOT / "docs/ORIGIN_AND_CSP_POLICY.md").read_text(
        encoding="utf-8"
    )
    blueprint = (REPOSITORY_ROOT / "render.yaml").read_text(encoding="utf-8")

    assert "https://www.viathorne.com" in policy
    assert "https://api.viathorne.com" in policy
    assert "connect-src 'self' https://api.viathorne.com" in policy
    assert "the apex origin `https://viathorne.com`" in policy
    assert "any `netlify.app`" in policy
    assert "wildcard, reflected, regex, suffix, or credentialed origins" in policy
    assert 'key: VIASIGN_CORS_ORIGINS\n        value: ""' in blueprint


def test_edge_and_operations_policy_keeps_public_activation_blocked() -> None:
    policy = (REPOSITORY_ROOT / "docs/EDGE_AND_OPERATIONS_POLICY.md").read_text(
        encoding="utf-8"
    )

    assert "V1 will not use a remote Render service preview" in policy
    assert "three-second total application deadline" in policy
    assert "approved one inert Blueprint" in policy
    assert "sync and service creation" in policy
    assert "Maintenance mode and empty CORS must remain" in policy
    assert "`review_required=true`" in policy
    assert "`motion_ready=false`" in policy


def test_runtime_lock_uses_exact_versions() -> None:
    lines = (REPOSITORY_ROOT / "requirements.lock").read_text(
        encoding="utf-8"
    ).splitlines()
    requirements = [line for line in lines if line and not line.startswith("#")]

    assert requirements
    assert all("==" in requirement for requirement in requirements)


def test_deployment_files_contain_no_private_source_markers() -> None:
    deployment_text = "\n".join(
        (REPOSITORY_ROOT / path).read_text(encoding="utf-8")
        for path in ("Dockerfile", "render.yaml", "requirements.lock")
    )

    for marker in ("SGSL_AI_DEV", "motion_engine_avatar", "TempleConsole"):
        assert marker not in deployment_text
