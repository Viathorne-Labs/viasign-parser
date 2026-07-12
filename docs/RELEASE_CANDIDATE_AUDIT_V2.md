# Release Candidate Audit V2

- **Status:** Owner-approved source published; hosting activation blocked
- **Reviewed:** 2026-07-13
- **Candidate:** `viasign-parser-public-v2-surface-published`
- **Parent clean commit:** `07c835ca279ea1792b29f53630062e816e3ec282`
- **Published commit:** `e9e2f94b2b3f5e22c9be4a29026e00f3b9ffb693`
- **Manifest:** `provenance/v1/release-candidate-manifest.json`

This audit covers the independently authored natural-English surface analyzer
and contract `1.1.0` published at
`https://github.com/Viathorne-Labs/viasign-parser`. Publication did not authorize
Render deployment, production CORS, public traffic, or linguistic claims.

## Change boundary

The V2 candidate adds closed sentence, question, question-category, and
negation-cue values. It advances the package and parser to `0.2.0` while keeping
schema family `viasign.parser.response.v1`.

The implementation returns no submitted text, token, name, fragment,
reconstructed text, sign-aware form, candidate gloss, SgSL order, motion, or
avatar data. `review_required=true` and `motion_ready=false` remain literal.

## Clean-room evidence

The private Parser V2 was reviewed only at capability level. No private source
file was edited, copied, imported, translated line by line, or added as a
dependency. The public analyzer and tests were authored independently from the
public behavioral boundary.

Private types, lexicon, benchmarks, examples, grammar notes, lesson-source
audits, source-gloss notation, sentence-specific branches, identity extraction,
motion, and avatar systems remain excluded.

## Verification record

The complete parser suite passes 105 tests, including generated-schema equivalence,
strict-category, no-echo, name-sign, API, deployment-boundary, clean-room, and
release tests. The first-party audit covers 70 allowlisted UTF-8 files and
reports no credential-shaped value, machine-local path, binary payload, private
import, or unaccounted candidate file.

The website passes Astro type checking, production build, internal-link,
automated accessibility, security-header, metadata, and discovery checks across
26 pages. A local real-browser flow rendered the four categories for ordinary
input and returned no analysis for blocked name-sign generation. Both flows
kept the review and motion-unavailable states visible.

The `0.2.0` source distribution and wheel build in an isolated environment,
declare Apache-2.0, and contain `LICENSE` and `NOTICE`. The exact dependency
lock passes `pip check` and `pip-audit` with no known vulnerability.

Fresh Linux arm64 and Linux amd64 images build from the pinned Alpine base.
Both run as UID `10001`, pass health, metadata, surface, unsupported,
validation, no-echo, `413`, and disabled-docs smoke checks. Trivy 0.72.0 with a
refreshed database reports zero Alpine and Python-package vulnerabilities for
both images, no embedded-secret finding, and zero Dockerfile
misconfigurations.

The deterministic manifest is regenerated after all documentation changes and
passes its exact check. Its SHA-256 fingerprint is reported outside this file so
recording the fingerprint cannot alter itself.

These checks demonstrate structural and operational consistency. They do not
prove SgSL correctness, accessibility approval, community approval, or
deployment safety.

## Remaining gates

- Publish this reconciled manifest and deployment record before creating cloud
  infrastructure.
- Create and verify only the separately approved inert Render service.
- Make later, separate decisions for DNS activation, production CORS, website
  connection, public traffic, and submissions.
