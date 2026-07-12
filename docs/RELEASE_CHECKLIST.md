# Public Release Checklist

The reviewed V2 source is public. Hosting activation is not approved.

## Source

- [x] Every candidate path appears in the deterministic path-and-SHA-256
  manifest.
- [x] The published history was created only from manifest-listed paths and did
  not copy the private or candidate `.git` object stores.
- [x] No excluded package, import, asset, document, or generated file is present
  in the local candidate.
- [x] No migrated private code is shipped; future migrations remain blocked by
  the provenance gate.
- [x] Repository owner approved the exact V2 candidate manifest.

## Language data

- [x] All fixtures are independently authored for structural contract testing.
- [x] No private lesson or community material is present in the candidate.
- [ ] Deaf/SgSL review has checked the public claims and limitations.
- [x] Uncertainty remains visible and `review_required`.

## API

- [x] Requests reject extra fields and unsafe input.
- [x] Responses are schema-versioned.
- [x] Every success requires review and is not motion-ready.
- [x] No translation, motion, avatar, upload, or private-data endpoint exists.
- [x] Input text is not persisted or logged by default.
- [x] Success, unsupported, malformed, and validation-error responses do not
  echo submitted text or invalid values.
- [x] Surface analysis contains only closed categories and cannot contain
  tokens, names, fragments, reconstructed text, or extracted values.
- [x] The current implementation returns no sign-aware form or candidate gloss.

## Engineering

- [x] Tests pass locally and the rebuilt container passes the runtime smoke
  boundary; repeat against the exact approved release artifact.
- [x] Secret, local-path, binary, private-import, provenance, dependency, and
  container scans pass for the local candidate.
- [x] Dependency versions are locked for the candidate.
- [x] Runtime dependency licenses and notices are recorded; repeat the audit
  against the final release lock.

## Publication

- [x] README, API, and website candidate text do not claim that the current
  public parser implements SgSL grammar, translation, or motion.
- [x] Apache-2.0 text, current SPDX metadata, NOTICE, packaged license files, and
  trademark boundaries remain unchanged from the approved V1 scope.
- [x] Repository owner completed `docs/OWNER_REVIEW_PACKET_V2.md` explicitly.
- [x] A separate explicit source-publication approval was recorded and commit
  `e9e2f94b2b3f5e22c9be4a29026e00f3b9ffb693` was published.

## Hosting

Source release did not authorize hosting. On 2026-07-13, the repository owner
separately approved one inert Blueprint sync and service creation with
maintenance mode on, empty CORS, automatic deploys off, no DNS change, and no
website connection.

- [x] Inert Blueprint sync and service creation approved.
- [ ] Reconciled release and deployment records are published before the sync.
- [ ] Live domain, health, notification, metric, log, and rollback evidence is
  captured from the inert service.
- [ ] Production CORS, website connection, maintenance-mode removal, public
  traffic, and submissions receive separate explicit approvals.
