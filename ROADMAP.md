# ViaSign Parser Public Repository Roadmap

## Stage 0: Clean-room scaffold

- [x] Create a fresh local repository boundary.
- [x] Add public-only guidance and exclusions.
- [x] Add tracked public `AGENTS.md`, `ARCHITECTURE.md`, and `ROADMAP.md`
  coordination documents; reserve ignored `*.local.md` files for private notes.
- [x] Add a fail-closed FastAPI shell.
- [x] Add structural safety tests.
- [x] Complete provenance review for each migration candidate.
- [ ] Record repository-owner rights attestation for non-empty private candidates.

## Stage 1: Machine-readable parser contract

- [x] Define a versioned public response schema.
- [x] Require `review_required=true` and `motion_ready=false` as literal values.
- [x] Define explicit draft, uncertain, unsupported, and invalid states.
- [x] Add independently authored valid, uncertain, unsupported, and invalid fixtures.
- [x] Validate fixtures against both typed models and JSON Schema.

## Stage 2: Minimal public parser implementation

- [x] Implement from the public contract and cleared public fixtures; do not copy
  the private parser, type surface, lexicon, or runtime demo.
- [x] Preserve provenance and prototype limitations.
- [x] Connect the new public parser through a one-way contract adapter.
- [x] Keep all private, legacy, motion, and data dependencies impossible to import.
- [x] Return visible uncertainty while public SgSL grammar rules remain unavailable.
- [x] Block name-sign generation with no analysis fallback.

## Stage 2A: Public website integration preparation

- [x] Freeze the `viathorne-web -> public FastAPI -> public parser` boundary.
- [x] Document privacy, CORS, accessibility, and user-facing limitation rules.
- [x] Add deployable environment configuration without enabling public hosting.
- [x] Build and browser-check the accessible tester in `viathorne-web` against
  a local API first; keep production deployment gated.

## Stage 2B: Protected deployment preparation

- [x] Define the public artifact, route, CORS, logging, retention, edge,
  accessibility, review, rollout, and rollback gates.
- [x] Pin the website to response schema `viasign.parser.response.v1` and
  contract `1.0.0`.
- [x] Disable non-allowlisted runtime documentation routes and add no-store and
  nosniff response headers.
- [x] Select Render, Singapore, and document Pro request-log behavior and
  14-day retention without authorizing deployment.
- [x] Add and locally smoke-test an inert Render Blueprint, non-root container,
  pinned base image and runtime package lock, disabled Uvicorn access logs, and
  a 4 KiB application body limit.
- [x] Audit runtime dependency licenses and known vulnerabilities; upgrade the
  lock to the patched Starlette release and record reproducible evidence.
- [x] Reject vulnerable Debian base candidates, pin the clean scanned Alpine
  candidate, add an image health check, and pass local container vulnerability,
  secret, configuration, and runtime smoke checks.
- [x] Implement and document a transient per-network parse limit with
  privacy-preserving in-memory keys, accessible `429`, and fail-closed Render
  proxy handling.
- [x] Freeze the exact production website and API origins, add a strict website
  Content Security Policy, and prepare provider-specific privacy wording without
  enabling the API or production CORS.
- [x] Verify that Render exposes neither the required short request deadline nor
  a 4 KiB Blueprint edge rule; add a three-second fail-closed application
  deadline, keep early body rejection, freeze monitoring and rollback, and
  reject remote previews for V1.
- [ ] Capture live Render health, domain, notification, metric, log, and rollback
  evidence only after a separately approved inert Blueprint sync.
- [ ] Complete protected-preview privacy, assistive-technology, and Deaf/SgSL
  review.
- [ ] Record a separate explicit deployment decision.

## Stage 3: Public benchmark suite

- Replace private benchmark data with independently authored fixtures.
- Record fixture provenance.
- Add regression tests for name-sign safety and unknown input.
- Obtain Deaf/SgSL review of claims and examples.

## Stage 4: Release review

- [x] Generate a deterministic local path-and-SHA-256 candidate manifest from an
  explicit public allowlist.
- [x] Run first-party and Trivy secret, binary, provenance, dependency-license,
  local-path, Dockerfile, container, and private-import scans; record the
  time-bounded evidence in `docs/RELEASE_CANDIDATE_AUDIT_V1.md`.
- [ ] Obtain repository-owner approval of the exact candidate manifest.
- [x] Prepare the license, NOTICE/trademark, claims, privacy, and prototype-limit
  review packet without inferring owner approval.
- [x] Remove submitted text from the prepublication response contract and replace
  default validation details with generic fail-closed errors; retain only
  non-sensitive input mode metadata.
- [ ] Create and verify a clean public commit from only manifest-listed paths;
  never copy the local `.git` object store.
- Review documentation and OpenAPI descriptions.
- Publish only after an explicit release decision.
