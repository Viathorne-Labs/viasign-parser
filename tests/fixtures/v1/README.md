# Contract Fixture Provenance

All fixtures in this directory were independently authored for structural
contract testing in this clean public repository on 2026-07-12 and updated with
closed surface categories on 2026-07-13.

They were not copied from private ViaSign materials, lesson notes, teacher
feedback, community submissions, benchmark banks, recordings, or source PDFs.

These examples test JSON structure and fail-closed behavior. They are not
evidence that a grammar analysis is correct or fluent SgSL.

| Fixture | Purpose |
| --- | --- |
| `valid/draft_question.json` | Supported contract shape with no correctness claim |
| `uncertain/unrecognized_vocabulary.json` | Requires an explicit uncertainty warning |
| `unsupported/name_sign_generation.json` | Blocks culturally sensitive generation and returns no analysis |
| `invalid/motion_ready_true.json` | Rejects a motion-ready public response |
| `invalid/missing_review_required.json` | Rejects a response missing the review invariant |
| `invalid/uncertain_without_warning.json` | Rejects hidden uncertainty |
| `invalid/unsupported_with_analysis.json` | Rejects plausible-looking analysis for unsupported input |
| `invalid/surface_with_extracted_values.json` | Rejects extracted tokens or other free-form surface values |
