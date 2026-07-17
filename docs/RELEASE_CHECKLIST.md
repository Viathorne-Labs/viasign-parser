# Public Release Checklist

The reviewed V2 source is public, the local-tester safety update has separate
source-publication approval, and the 2026-07-17 deployment evidence has separate
publication approval. The one-time `d88bc266` inert-deployment authorization
was consumed; no additional deployment or provider change and no public
activation are approved.

## Source

- [x] Every candidate path appears in the deterministic path-and-SHA-256
  manifest.
- [x] The published history was created only from manifest-listed paths and did
  not copy the private or candidate `.git` object stores.
- [x] No excluded package, import, asset, document, or generated file is present
  in the local candidate.
- [x] No migrated private code is shipped; future migrations remain blocked by
  the provenance gate.
- [x] Repository owner approved the exact manifest used for the published V2
  source checkpoint.
- [x] The current local-tester candidate hashes received separate review as part
  of the source-publication approval recorded for parser PR #4 on 2026-07-17;
  the earlier approval did not carry over.

## Language data

- [x] All fixtures are independently authored for structural contract testing.
- [x] No private lesson or community material is present in the candidate.
- [ ] Broader Deaf/SgSL community review has checked the public claims and
  limitations.
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

- [x] The exact parser `0.2.1` source at `d88bc266` passes 137 tests and the
  rebuilt Linux arm64 and Linux amd64 images pass the runtime smoke boundary.
- [x] Local browser-assisted tester evidence covers uncertain, prohibited,
  unavailable, contract, focus, and reflow boundaries as recorded in
  `docs/LOCAL_TESTER_REVIEW_V1.md`.
- [x] The completed `viathorne-web` representative manual accessibility baseline
  is credited for the shared shell and disabled tester boundary; it is not
  repeated for this parser-only correction.
- [x] The enabled tester's bounded human check covers keyboard navigation,
  Safari VoiceOver ready/checking/final and revealed-result phrases, native 200
  percent zoom, and increased contrast with a safe result visible.
- [x] Repository-owner review of the enabled flow's privacy wording, prototype
  limits, Deaf/SgSL positioning, and licensing boundary is complete; broader
  community review remains separate.
- [x] Secret, local-path, binary, private-import, provenance, dependency, and
  exact `0.2.1` arm64/amd64 container scans pass for the local candidate.
- [x] Dependency versions are locked for the candidate.
- [x] Runtime dependency licenses and notices are recorded and the exact `0.2.1`
  lock passed the 2026-07-17 refresh.

## Publication

- [x] README, API, and website candidate text do not claim that the current
  public parser implements SgSL grammar, translation, or motion.
- [x] Apache-2.0 text, current SPDX metadata, NOTICE, packaged license files, and
  trademark boundaries remain unchanged from the approved V1 scope.
- [x] Repository owner completed `docs/OWNER_REVIEW_PACKET_V2.md` explicitly.
- [x] A separate explicit source-publication approval was recorded and commit
  `e9e2f94b2b3f5e22c9be4a29026e00f3b9ffb693` was published.
- [x] The local tester safety correction and bounded accessibility review
  evidence received separate source-publication approval on 2026-07-17 for
  parser PR #4.
- [x] Parser PR #4 merged into public `main` at
  `d88bc2664628135a04ee4961866fea2380e1343d`.

## Hosting

Source release did not authorize hosting. On 2026-07-13, the repository owner
separately approved one inert Blueprint sync and service creation with
maintenance mode on, empty CORS, automatic deploys off, no DNS change, and no
website connection.

- [x] Inert Blueprint sync and service creation approved.
- [x] The reconciled public source was published before the sync and exact merge
  commit `e8ca6a688c6905fba1f2f02646b665623f0c689e` was deployed.
- [ ] Full live domain, health, notification, metric, log, and rollback evidence
  is captured from the inert service. The internal health response is verified;
  the remaining domain, rollback, and human-review limits are recorded in
  `docs/INERT_RENDER_SERVICE_AUDIT_V1.md`.
- [x] The post-sync inert-service audit checkpoint received separate
  publication approval.
- [x] The approved checkpoint is merged into public `main` at
  `842a9ad820e4ac919fb88371a3ab9199ebc74a79`.
- [x] The internal-health evidence received separate publication approval.
- [x] The approved internal-health evidence is merged into public `main` at
  `aeca8bedadf16655fea34726bb3db9e780ba0f07`.
- [x] The 2026-07-17 read-only provider refresh and exact parser `0.2.1` local
  deployment-candidate checks are complete.
- [x] The 2026-07-17 provider-refresh and exact-image evidence received explicit
  publication approval without authorizing a Render update or activation.
- [x] Deployment-evidence PR #5 merged into public `main` at
  `d6c59f7c0c9b1e00aad2b73e42cebfb38ff2d172`.
- [x] A later, separate provider-mutation approval authorized exactly hook
  regeneration plus **Deploy a specific commit** for
  `d88bc2664628135a04ee4961866fea2380e1343d`, with no other provider or
  activation change. That two-action authorization is consumed and permits no
  additional provider mutation.
- [x] After that approval, the deploy hook was regenerated through the
  dashboard; neither the old nor new value was invoked as a test or recorded.
- [x] After rotation, the inert service was updated from parser `0.2.0` using
  **Deploy a specific commit**, never **Deploy latest commit**. The live event
  showed the exact commit while maintenance mode, empty CORS, disabled
  auto-deploys, unresolved DNS, disabled Render subdomain, and website
  disconnection remained unchanged.
- [x] The exact post-deployment evidence received separate publication approval
  without authorizing any DNS, CORS, website, maintenance, traffic, or public
  activation change.
- [ ] Before any website connection, the website pins the exact production API
  and page origins and validates the complete `429` contract without rendering
  free-form server text.
- [ ] Production CORS, website connection, maintenance-mode removal, public
  traffic, and submissions receive separate explicit approvals.
