# Repository Owner Review Packet V1

- **Status:** Prepared; owner approval not yet recorded
- **Reviewed:** 2026-07-12
- **Candidate:** `viasign-parser-public-v1-prepublication`
- **Exact file record:** `provenance/v1/release-candidate-manifest.json`

This packet collects the human decisions needed before creating a clean public
commit. It is a project review aid, not legal advice. Completing this review does
not itself authorize repository publication, Render deployment, custom-domain
changes, production CORS, or public traffic.

## Technical evidence already complete

- The deterministic manifest checks every candidate path and SHA-256 digest.
- The candidate contains no private implementation, private Git history,
  benchmark bank, lesson material, community submission, reviewer identity,
  media, source PDF, database, model weight, or compiled binary.
- Clean-room, provenance, contract, safety, API, deployment-boundary, and release
  tests pass.
- First-party and Trivy secret, local-path, binary, private-import, dependency,
  Dockerfile, and multi-platform container checks pass.
- `review_required=true` and `motion_ready=false` remain mandatory.

Technical checks demonstrate structural consistency. They do not establish
linguistic correctness, legal advice, community approval, or deployment safety.

## License and notice review

The root `LICENSE` contains the complete Apache License 2.0 text; its normalized
text matches the official Apache copy. `pyproject.toml` uses the current SPDX
expression `Apache-2.0` and declares both `LICENSE` and `NOTICE` as distribution
license files.

No third-party code is vendored into the source candidate. The 13 locked runtime
dependencies retain their own permissive licenses and license files in the
container. Their exact inventory is recorded separately.

The `NOTICE` applies Apache-2.0 only to software and original documentation in
the distribution. It does not claim ownership of SgSL or community knowledge and
does not grant rights to use ViaSign or Viathorne names, logos, or branding as
trademarks.

Official references:

- https://www.apache.org/licenses/LICENSE-2.0
- https://www.apache.org/foundation/license-faq.html
- https://packaging.python.org/en/latest/specifications/license-expression/

## Public-claims review

The public parser currently implements safety behavior, strict contracts,
visible uncertainty, simple question-punctuation detection, and a block on
name-sign generation. It implements no public SgSL grammar rules, verified
glosses, translation, motion, avatar output, or linguistic benchmark.

The README and website describe SgSL-aware planning as future research rather
than a current public capability. Public tester copy states that it does not
translate, sign, or create motion. Passing tests must never be described as
proof of correct or fluent SgSL.

## Privacy and data review

The application has no database, persistent volume, analytics, tracing, replay,
training, benchmark-submission, feedback, or review store. It does not
intentionally log sentence text or parser output. Sentence text remains in the
request and short-lived process memory needed to answer it. Success,
unsupported, malformed, and validation-error responses never echo the sentence
or invalid submitted values.

The hosting plan separately discloses provider network metadata and retention,
keeps the sentence out of URLs, disables Uvicorn access logs, and preserves a
local-only review stage. No public API or production website connection is
enabled.

## Review still required from others

Repository-owner approval cannot replace:

- Deaf/SgSL review of claims, examples, intended audience, and limitations
- assistive-technology and accessibility review of the final user flow
- professional legal advice if the owner needs it
- a separate publication decision
- a separate Render deployment and public-activation decision

## Owner decision record

Leave every item unchecked until the repository owner explicitly confirms it:

- [ ] I confirm that the candidate's original public code and documentation may
  be distributed by Viathorne under Apache-2.0.
- [ ] I approve the `LICENSE`, `NOTICE`, SPDX metadata, and trademark boundary
  for this candidate, subject to obtaining professional advice if needed.
- [ ] I approve the current public claims and prototype limitations as accurate
  for a parser with no public SgSL grammar rules.
- [ ] I approve the recorded privacy boundary for the source candidate.
- [ ] I approve the exact path-and-hash manifest as the only input to a future
  clean public commit.

After explicit approval, record the decision date and approver role without
adding a personal email, signature image, or private identity document.

Approval of this packet authorizes only the next mechanical gate: preparing a
clean local public commit from manifest-listed files. It does not authorize
pushing, publishing, deploying, enabling production CORS, or accepting public
submissions.
