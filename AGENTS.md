# ViaSign Parser Repository Guidance

## Purpose

This repository is the clean public boundary for the ViaSign grammar-first
parser prototype. It must remain inspectable, review-required, Deaf-first, and
separate from private ViaSign source material.

Read `ARCHITECTURE.md` for durable component and trust boundaries and
`ROADMAP.md` for the verified implementation sequence before changing scope.
These files and this guidance are public safety documentation and should remain
tracked. Put genuinely private or machine-specific notes in a separate
`*.local.md` file, which is ignored and excluded from release evidence.

## Non-negotiable safety rules

- Treat every parser result as `review_required`.
- Keep `motion_ready` false in every public response.
- Fail closed if either invariant is missing or changes.
- Describe current output as natural-English surface analysis, never SgSL
  grammar or final translation.
- Do not analyze recognized name-sign-related input, and do not infer or
  generate name signs; return `unsupported` with no analysis.
- Never echo submitted sentence text in public success or error responses.
- Do not add motion, avatar, signer-space coordinates, or renderer output.
- Do not add private lesson material, teacher notes, community media, reviewer
  identities, source PDFs, or copied classroom examples.
- Add only independently authored, public-safe fixtures.

## Clean-room boundary

Only paths explicitly listed in `docs/PUBLIC_SOURCE_MANIFEST.md` may be
considered for later migration. Being listed does not replace provenance,
license, privacy, and human-review checks.

The V1 provenance gate blocks direct copying of every non-empty private
candidate. Stage 2 must be implemented from the public contract and cleared
public fixtures without line-by-line translation of private code.

Never import from or depend on:

- the private `SGSL_AI_DEV` checkout
- legacy parser or sign-plan modules
- `motion_engine_avatar`
- a future private linguistic-motion engine
- Temple Console internals
- private data or review directories

## API boundary

The public service exposes only health, metadata, and surface-analysis parse
routes. The current public parser contains safety behavior and closed
natural-English surface categories but no SgSL grammar rules: ordinary input
returns visible uncertainty, while prohibited generation requests return
unsupported with no analysis.

The API must not log input text, persist requests, or return submitted text in
its public response body.

`viathorne-web` may integrate only with this public API. It must never connect
browser users to private ViaSign code, data, review stores, or services.

## Implementation style

- Prefer small patches with focused tests.
- Keep request and response models strict and versioned.
- Reject extra request fields and invalid input.
- Preserve uncertainty explicitly.
- Update the manifest and boundary documentation with every scope change.

## Required checks

Run:

```bash
python -m pytest
```

Passing tests demonstrate structural consistency, not linguistic correctness.
