# Public Release Checklist

No public release is approved yet.

## Source

- [x] Every local candidate path appears in the deterministic path-and-SHA-256
  manifest; repository-owner approval remains open.
- [x] The candidate excludes `.git`; the future public repository must be
  created only from manifest-listed paths.
- [x] No excluded package, import, asset, document, or generated file is present
  in the local candidate.
- [x] No migrated private code is shipped; future migrations remain blocked by
  the provenance gate.
- [ ] Repository owner approves the exact candidate manifest.

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
  trademark boundaries pass the prepared review; owner approval remains open.
- [ ] Repository owner completes `docs/OWNER_REVIEW_PACKET_V1.md` explicitly.
- [ ] A separate explicit release approval has been recorded.

## Hosting

Source release does not authorize a hosted service. Before hosting, complete
every item in `docs/PRODUCTION_DEPLOYMENT_GATE.md` and record a separate explicit
deployment approval.
