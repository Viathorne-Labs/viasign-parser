# Public FastAPI Boundary

## Allowed routes

```text
GET  /healthz
GET  /v1/meta
POST /v1/parse
```

No translation, motion, avatar, corpus, upload, review-administration, or
private-source route is allowed. Runtime Swagger UI, ReDoc, and OpenAPI routes
are disabled; the schema remains available offline through `app.openapi()` for
tests and release review.

## Parse request

```json
{
  "text": "Where is the class?"
}
```

The request model:

- rejects unknown fields
- trims surrounding whitespace
- rejects empty text
- rejects control characters
- caps input at 1,000 characters
- does not let callers set review, readiness, parser, or input-mode fields

## Current response

The clean-room implementation contains safety behavior and a small
natural-English surface analyzer, but no SgSL grammar rules. Ordinary input
returns visible uncertainty:

```json
{
  "outcome": "uncertain",
  "status": "review_required",
  "input": {
    "mode": "natural"
  },
  "analysis": {
    "intent": "question",
    "surface": {
      "sentence_kind": "question",
      "question_kind": "wh",
      "question_category": "where",
      "negation_cue": "absent"
    },
    "sign_aware_form": null,
    "candidate_glosses": []
  },
  "review_required": true,
  "motion_ready": false
}
```

Name-sign generation requests return `unsupported`, at least one reason, and
`analysis: null`.

Neither successful nor unsupported responses echo the submitted sentence.
Surface analysis returns only closed categories; it never returns tokens,
names, fragments, or reconstructed text.
Malformed JSON, invalid fields, and invalid values return a generic
`422 invalid_request` response without submitted values or validation internals.

## Success invariant

Any future successful response must be schema-versioned and must contain the
literal values:

```json
{
  "status": "review_required",
  "review_required": true,
  "motion_ready": false
}
```

If either invariant is absent or changes, the adapter must return an internal
fail-closed error without exposing the unsafe parser payload.

HTTP `200` will mean that draft analysis was produced. It will never mean that
the output is correct, fluent, approved, translated, or motion-ready.

The frozen pre-implementation response contract is documented in
`docs/PARSER_RESPONSE_CONTRACT_V1.md` and exported as
`contracts/v1/parser-response.schema.json`.

## Privacy

The reference API does not persist requests or return submitted text in public
responses. Application logs must not include input text or full parser output.
The application provides a transient,
HMAC-keyed parse rate limit without logging or persisting the network address.
Provider DDoS protection, TLS, and retention controls remain deployment
boundaries. The complete policy is in `docs/RATE_LIMIT_POLICY.md`.

`POST /v1/parse` has a three-second application deadline. A timeout returns a
no-store `503 parse_timeout` with `review_required=true` and
`motion_ready=false`; no buffered parser response is released.

`POST /v1/parse` responses carry `Cache-Control: no-store`. Public responses
carry `X-Content-Type-Options: nosniff`.
