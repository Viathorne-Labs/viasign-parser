# Repository Owner Review Packet V2

- **Status:** Owner approval recorded; source published
- **Reviewed:** 2026-07-13
- **Candidate:** `viasign-parser-public-v2-surface-published`
- **Exact file record:** `provenance/v1/release-candidate-manifest.json`
- **Parent clean commit:** `07c835ca279ea1792b29f53630062e816e3ec282`
- **Published commit:** `e9e2f94b2b3f5e22c9be4a29026e00f3b9ffb693`

This packet covers the clean-room natural-English surface analyzer added after
the initial safety-only candidate. It is a project review aid, not legal advice.
The repository owner approved all five source-review items on 2026-07-13, and a
later separate decision authorized publication under `Viathorne-Labs`. Those
decisions did not authorize Render deployment, production CORS, public traffic,
SgSL claims, or submissions.

## Change from the approved V1 candidate

The V1 owner decision approved only the initial safety-only snapshot. V2 adds an
independently authored surface analyzer and advances the public contract from
`1.0.0` to `1.1.0`.

For ordinary natural-English input, V2 may report only:

- sentence kind: statement, question, or unknown
- question kind: WH, yes/no, unknown, or not applicable
- one closed generic-English question category or none
- a present, absent, or ambiguous negation cue

The parser continues to return `sign_aware_form=null`, an empty
`candidate_glosses` list, `review_required=true`, and `motion_ready=false`.

## Clean-room and provenance review

The private Parser V2, private types, lexicon, benchmark bank, grammar notes,
lesson-source audits, and runtime demo remain blocked from direct copying.
Editing a private file would not erase its lineage, so no private file was
edited or migrated for this change.

The new public analyzer was implemented from the public behavior boundary and
independently authored synthetic tests. It does not reproduce private source
code, output structures, rule order, vocabulary, examples, benchmark
expectations, source-gloss notation, or sentence-specific branches.

## Claims and linguistic limits

V2 performs natural-English surface classification only. It does not implement
SgSL grammar, translation, gloss generation, sign-aware ordering, indexing,
topicalization, rhetorical-question planning, time-sign planning, location
planning, non-manual signals, sign parameters, motion, or avatar output.

Surface categories must not be described as correct SgSL analysis. Passing
tests demonstrate deterministic contract and safety behavior, not linguistic
correctness, fluency, accessibility approval, or community approval.

## Privacy review

The response contains only closed enumerated categories. It does not return the
submitted sentence, tokens, names, fragments, reconstructed text, inferred
identity fields, or extracted values. Malformed and validation-error responses
remain generic. The service still has no database, persistent volume, account,
feedback store, analytics SDK, training pipeline, or review store.

Sentence text remains briefly in request and process memory to calculate the
categories. Hosting-provider network metadata and retention remain separate
deployment limitations.

## License and brand boundary

The Apache-2.0 license and existing `NOTICE` continue to apply to the original
public software and documentation. They do not claim ownership of SgSL or
community knowledge and do not grant permission to present a fork as an
official ViaSign or Viathorne product.

## Review still required from others

Repository-owner approval cannot replace:

- Deaf/SgSL review before adding or claiming any SgSL-aware rule
- assistive-technology review of the final tester flow
- professional legal advice if required
- a separate source-publication decision
- a separate Render deployment and public-activation decision

## Owner decision record

The repository owner explicitly confirmed every item on 2026-07-13. The public
record omits personal signatures, contact details, and identity documents:

- [x] I approve the independently authored V0.1 natural-English surface-analysis
  scope and confirm that no private Parser V2 implementation is being released.
- [x] I approve contract `1.1.0`, including its closed categories, no-echo
  privacy boundary, and continued SgSL-output prohibition.
- [x] I approve the current public claims and limitations as accurate for a
  surface analyzer with no SgSL grammar rules.
- [x] I confirm that the Apache-2.0 and ViaSign/Viathorne brand-use decisions
  approved for V1 remain acceptable for this changed candidate.
- [x] I approve the final path-and-hash manifest as the only input to the
  V2 commit.

Record any decision in an ignored local file so the act of recording approval
does not change the approved candidate fingerprint. Do not add a personal email,
signature image, identity document, or reviewer identity to the public tree.

Approval of this packet authorized preparation of the clean V2 commit. A later
explicit decision authorized pushing and source publication. Neither source
decision authorized Render deployment, production CORS, public traffic, or
submissions; those remain separately gated.
