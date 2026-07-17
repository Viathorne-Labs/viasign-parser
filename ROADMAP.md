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
- [x] Block all recognized name-sign-related input with no analysis fallback.

## Stage 2C: Clean-room surface analyzer

- [x] Re-audit private Parser V2 at capability level without editing, copying,
  importing, or translating private files.
- [x] Define contract `1.1.0` with closed, non-verbatim natural-English surface
  categories.
- [x] Implement sentence, question, question-category, and negation-cue analysis
  independently from the public contract and new synthetic tests.
- [x] Keep SgSL order and gloss output unavailable.
- [x] Make the website reject free-form or extracted surface values.
- [ ] Obtain Deaf/SgSL and assistive-technology review before introducing any
  public SgSL-aware rule.

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
  advance the public contract pin to `1.1.0` for closed surface analysis.
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
- [x] Publish the reviewed V2 source and the disabled website tester boundary.
- [x] Record a separate owner decision approving one inert Blueprint sync and
  service creation without DNS, CORS, website, or maintenance-mode activation.
- [ ] Complete live Render health, domain, notification, metric, log, and
  rollback evidence. The first inert audit verified the exact live commit,
  isolation, maintenance state, configuration, clean startup logs, metrics
  surface, failure notifications, and exact internal health response;
  custom-domain TLS and rollback remain unavailable or blocked.
- [x] Verify the exact internal `/healthz` response while maintenance mode and
  empty CORS remained unchanged.
- [x] Record local browser-assisted evidence for the enabled tester's uncertain,
  name-sign, unavailable, contract, focus, and reflow boundaries in
  `docs/LOCAL_TESTER_REVIEW_V1.md`.
- [x] Credit the completed `viathorne-web` representative manual accessibility
  baseline instead of repeating its site-wide keyboard, zoom, VoiceOver,
  contrast, motion, focus, and reflow review.
- [x] Complete the enabled tester's bounded human accessibility check: keyboard
  navigation, Safari VoiceOver status/result phrases, native 200 percent zoom,
  and increased system contrast with a safe result visible.
- [x] Complete repository-owner review of the enabled flow's privacy wording,
  prototype limits, Deaf/SgSL positioning, and licensing boundary; keep broader
  community review separate.
- [x] Record the inert service-creation decision; keep public activation
  separately blocked.

## Stage 3: Public benchmark suite

- Replace private benchmark data with independently authored fixtures.
- Record fixture provenance.
- Add regression tests for name-sign safety and unknown input.
- Obtain broader Deaf/SgSL community review of claims and examples.

## Stage 4: Release review

- [x] Generate a deterministic local path-and-SHA-256 candidate manifest from an
  explicit public allowlist.
- [x] Run first-party and Trivy secret, binary, provenance, dependency-license,
  local-path, Dockerfile, container, and private-import scans; record the
  time-bounded evidence in `docs/RELEASE_CANDIDATE_AUDIT_V1.md`.
- [x] Obtain repository-owner approval of the initial safety-only candidate
  manifest and record it outside the immutable candidate.
- [x] Prepare the license, NOTICE/trademark, claims, privacy, and prototype-limit
  review packet without inferring owner approval.
- [x] Remove submitted text from the public response contract and replace
  default validation details with generic fail-closed errors; retain only
  non-sensitive input mode metadata.
- [x] Create and verify a clean public root commit from only manifest-listed paths;
  never copy the local `.git` object store.
- [x] Obtain repository-owner approval of the changed surface-analysis candidate.
- [x] Review the V2 documentation and publish the approved source at
  `https://github.com/Viathorne-Labs/viasign-parser`.
- [x] Publish the reconciled release before syncing the Render Blueprint; the
  first service deployed exact merge commit
  `e8ca6a688c6905fba1f2f02646b665623f0c689e`.
- [x] Obtain repository-owner approval to publish the post-sync inert-service
  audit checkpoint.
- [x] Merge the approved inert-service audit checkpoint into public `main` at
  `842a9ad820e4ac919fb88371a3ab9199ebc74a79`.
- [x] Obtain repository-owner approval to publish the internal-health evidence.
- [x] Merge the approved internal-health evidence into public `main` at
  `aeca8bedadf16655fea34726bb3db9e780ba0f07`.
- [ ] Obtain repository-owner approval before publishing the local tester safety
  correction and bounded accessibility review evidence.
