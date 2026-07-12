# Parser Response Contract V1

Status: prepublication contract 1.1.0 candidate; no SgSL rules

This contract defines public transport structure. It does not implement SgSL
grammar and does not make its synthetic examples linguistically authoritative.

## Shared invariants

Every response contains:

```json
{
  "schema_version": "viasign.parser.response.v1",
  "status": "review_required",
  "review_required": true,
  "motion_ready": false
}
```

These are literal schema constraints, not configurable defaults. A future
adapter must fail closed if a parser result violates them.

Every successful response also contains only non-sensitive request metadata:

```json
{
  "input": {
    "mode": "natural"
  }
}
```

The submitted sentence is intentionally absent. Invalid-request responses are
also generic and must not contain submitted values.

## Outcomes

### `draft`

The implementation recognized enough structure to return draft analysis. This
does not mean the analysis is correct, fluent, approved, or safe to use as a
translation.

### `uncertain`

The implementation returned draft analysis but has unresolved uncertainty.
At least one visible warning is required.

### `unsupported`

The implementation intentionally refused to analyze the request. It must return
`analysis: null`, at least one warning, and at least one unsupported reason.
This prevents plausible-looking fallback output.

### Invalid payloads

`invalid` is deliberately not a response outcome. A malformed request is
rejected by the transport boundary, and a response that violates the schema is
rejected by the adapter. Invalid fixtures prove that unsafe payloads cannot be
serialized as successful parser results.

## Analysis fields

Contract `1.1.0` exposes only:

- broad intent
- four closed natural-English surface categories
- an optional draft sign-aware form
- candidate gloss strings

The current parser fills only the surface categories:

```json
{
  "sentence_kind": "question",
  "question_kind": "wh",
  "question_category": "where",
  "negation_cue": "absent"
}
```

These values describe source-text form, not SgSL grammar. The schema permits no
tokens, names, fragments, reconstructed text, extracted identity, or free-form
surface value. The current implementation always keeps `sign_aware_form` null
and `candidate_glosses` empty.

Any future candidate glosses would be planning tokens, not verified signs or
motion commands, and would require a separate reviewed contract change.
No handshape, orientation, location, movement, contact, non-manual realization,
signer-space coordinate, or avatar field is permitted.

Warning field paths may refer to `request.text` to identify the request contract
field, but the corresponding value is never copied into the response.

## Provenance

Every response identifies its parser, implementation version, ruleset version,
and contract version. Provenance describes software lineage; it does not record
private source identity or reviewer personal information.

## Machine-readable artifacts

- `contracts/v1/parse-request.schema.json`
- `contracts/v1/parser-response.schema.json`

Regenerate them with:

```bash
python scripts/export_contracts.py
```

Committed schemas must remain byte-equivalent in structure to the authoritative
Pydantic model output checked by the test suite.
