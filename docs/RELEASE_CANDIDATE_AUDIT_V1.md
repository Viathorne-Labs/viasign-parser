# Release Candidate Audit V1

- **Status:** Local technical gate passed; owner approval and publication blocked
- **Reviewed:** 2026-07-12
- **Candidate:** `viasign-parser-public-v1-prepublication`
- **Hash algorithm:** SHA-256
- **Manifest:** `provenance/v1/release-candidate-manifest.json`

This record covers the exact local public candidate selected by
`scripts/release_manifest.py`. It does not approve a commit, remote repository,
publication, deployment, Render Blueprint sync, public traffic, or linguistic
correctness.

## Deterministic path boundary

The release manifest is generated only from explicit top-level files and the
public `contracts/`, `docs/`, `provenance/`, `scripts/`, `src/`, and `tests/`
trees. The generator fails on an unaccounted workspace file or any symlink.

The manifest excludes itself because a file cannot contain its own stable hash.
It also excludes local-only Git data, virtual environments, caches, build
output, bytecode, and operating-system metadata. Those exclusions are rules in
the generator rather than informal packaging instructions.

The tracked root `AGENTS.md`, `ARCHITECTURE.md`, and `ROADMAP.md` files are
public safety and sequencing evidence. Private or machine-specific coordination
notes use the ignored `*.local.md` convention and are excluded from the
candidate.

The resulting candidate contains only UTF-8 text source, configuration,
contracts, synthetic fixtures, tests, public documentation, and provenance
metadata. It contains no images, audio, video, PDFs, office documents, archives,
databases, model weights, compiled binaries, or private datasets.

## First-party boundary audit

`scripts/audit_release_candidate.py` checked every allowlisted candidate file
and reported no:

- credential-shaped values or private-key blocks
- machine-local absolute paths or editor file URIs
- NUL bytes or non-UTF-8 payloads
- forbidden binary, archive, media, database, or model extensions
- imports from private ViaSign, legacy SgSL, motion-avatar, or Temple Console
  modules

Private repository names that remain in `AGENTS.md`, clean-room tests, or
boundary documentation are explicit exclusion rules, not imports or runtime
dependencies.

## Independent scanner evidence

Trivy 0.72.0 refreshed its vulnerability database and scanned the candidate
filesystem for vulnerabilities, secrets, and Dockerfile misconfiguration. It
reported zero Dockerfile misconfigurations and no secret finding. Python runtime
packages are audited separately from the exact lock because Trivy does not
recognize the repository's custom `requirements.lock` filename as a Python
manifest.

Both Linux arm64 and Linux amd64 container candidates were rebuilt from the
pinned Python Alpine digest and scanned with Trivy across all severities and for
embedded secrets. Both reported:

- zero Alpine operating-system vulnerabilities
- zero Python-package vulnerabilities
- no embedded secret finding

The amd64 candidate also passed the current runtime smoke boundary: Docker
health, non-root UID `10001`, `pip check`, minimal metadata, uncertain parser
output, `review_required=true`, `motion_ready=false`, CORS, fail-closed `413`,
disabled runtime documentation, and omitted Uvicorn server header. No test
container remains running.

## Dependency and license evidence

The exact `requirements.lock` passed `pip check` and `pip-audit 2.9.0` with no
known vulnerability. `pip-licenses 5.5.0` reproduced the 13-package runtime
inventory recorded in `docs/THIRD_PARTY_DEPENDENCY_REVIEW.md`. Every installed
runtime distribution retained an upstream license or copying file inside the
container.

The candidate source distribution and wheel also built successfully in an
isolated environment. Wheel metadata contains `License-Expression: Apache-2.0`
and packages both `LICENSE` and `NOTICE` under its license-files directory.

Before owner approval, the response contract was privacy-minimized so it retains
only input mode metadata. Focused regression tests confirm that successful,
unsupported, malformed, and validation-error responses never echo submitted
text or invalid values.

These results are time-bounded. They must be repeated after any dependency,
base-image, source, contract, fixture, or deployment change and immediately
before an approved release.

## Provenance evidence

The fixture provenance file states that all seven JSON examples were
independently authored for structural contract tests. Provenance and clean-room
tests passed. No private implementation candidate, benchmark bank, lesson
material, review batch, teacher note, community submission, recording, or
source PDF is included.

The local Git repository has zero reachable commits, zero tracked index paths,
zero reflog entries, and no remote. Its excluded `.git` object store contains
loose unreachable setup residue. This audit did not inspect, publish, prune, or
alter that local object content. A future public repository must be created only
from the allowlisted manifest paths; the `.git` directory must never be copied
or uploaded.

## Remaining approval gates

- The repository owner has not yet approved the exact manifest.
- No clean public commit hash exists.
- Human license, trademark, claims, privacy, accessibility, and Deaf/SgSL review
  remains required where recorded in the release and deployment checklists.
- Scanner results must be repeated against the exact owner-approved commit and
  release image.
- Source release and Render deployment remain separate explicit decisions.

The candidate remains local and prepublication until all applicable unchecked
items in `docs/RELEASE_CHECKLIST.md` are complete and a separate release
approval is recorded.
