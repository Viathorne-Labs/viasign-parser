# Container Security Review

- **Status:** Local image scan passed; repeat against the exact release image
- **Reviewed:** 2026-07-12
- **Docker Engine:** 29.6.1
- **Scanner:** Trivy 0.72.0
- **Image:** `viasign-parser:render-gate`
- **Platforms tested:** Linux arm64 and Linux amd64
- **Base:** `python:3.13-alpine`
- **Base digest:**
  `sha256:399babc8b49529dabfd9c922f2b5eea81d611e4512e3ed250d75bd2e7683f4b0`

This is local, time-bounded security evidence. It does not approve repository
publication, a Render deploy, public traffic, or linguistic correctness.

## Base selection

The first pinned `python:3.13-slim-bookworm` candidate produced 21
High/Critical operating-system findings in the current Trivy database. A
newer Debian 13 slim candidate produced 20. Both were rejected for this
artifact.

The official Python 3.13 Alpine candidate was then pinned by multi-platform
digest. It preserves Python 3.13 while reducing the final image's operating-
system package surface.

## Recorded scan result

The rebuilt final image was scanned across all vulnerability severities and
for embedded secrets. Trivy reported:

- zero Alpine operating-system vulnerabilities
- zero Python-package vulnerabilities
- no secret findings
- zero Dockerfile misconfiguration failures across 27 checks

The initial configuration scan identified one Low finding because the image
did not define a container health check. A minimal local `/healthz` probe was
added, and the final configuration scan passed.

Scanner reference:

- https://trivy.dev/docs/latest/target/container_image/

## Runtime smoke result

The native arm64 image and the cross-built Linux amd64 image required by
Render's prebuilt-image path both built and scanned cleanly. Both images were
run locally and verified to:

- reach Docker health status `healthy`
- run as numeric user and group `10001:10001`
- keep the copied application source non-writable by the runtime user
- pass `pip check`
- return `200` from health, metadata, and parse routes
- preserve `review_required=true` and `motion_ready=false`
- return `404` from `/docs`
- return `413 request_too_large` above the 4 KiB body ceiling
- return `Cache-Control: no-store` on parse and oversize responses
- omit the Uvicorn `Server` header

No test container remains running.

After the anonymous pilot limiter was added, both platform images were rebuilt
and rescanned for vulnerabilities, embedded secrets, and image configuration.
The scans remained clean. A Render-proxy-mode container smoke test also passed
the `503`, burst-20, `429`, separate-client, and `413` boundaries.

After the three-second parse deadline was added, the native Linux arm64 image
was rebuilt again. Its health, metadata, uncertain parse, non-root runtime, and
fail-closed `413` smoke checks passed. The timeout path passed a focused API
test. This rebuild did not replace the required fresh multi-platform scan and
runtime review against the eventual release commit.

After the raw-input no-echo boundary was added, fresh Linux arm64 and Linux
amd64 images were rebuilt and rescanned. Both scans again reported zero
operating-system and Python-package vulnerabilities and no embedded-secret
findings; the repository configuration scan reported zero Dockerfile
misconfigurations. Runtime smoke tests on both architectures confirmed that
successful, unsupported, malformed, and validation-error responses do not
return the submitted sentence, while the safety invariants, non-root runtime,
disabled documentation route, and fail-closed `413` boundary remain intact.

After the clean-room surface analyzer and contract `1.1.0` were added, fresh
Linux arm64 and Linux amd64 images were rebuilt. Runtime smoke checks confirmed
the four closed surface categories, no sign-aware form or candidate glosses,
no submitted-value echo, the name-sign block, generic validation errors,
non-root UID `10001`, disabled documentation, and fail-closed `413` behavior.
Trivy 0.72.0 refreshed its database and again reported zero Alpine and
Python-package vulnerabilities for both images, no embedded-secret finding,
and zero Dockerfile misconfigurations.

## Release rule

Immediately before any deployment:

1. Build from the reviewed public commit and the pinned base digest.
2. Scan the exact release image with a freshly updated vulnerability database.
3. Scan all severities, secrets, and image configuration.
4. Repeat the runtime smoke boundary.
5. Stop on any unreviewed finding or safety-invariant failure.

Render architecture reference:

- https://render.com/docs/deploying-an-image#image-requirements

The scan must still be repeated against the exact image produced by the
approved release commit. Local architecture coverage does not substitute for
post-deployment verification.
