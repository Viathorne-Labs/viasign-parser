# Viathorne Web Integration Boundary

## Purpose

The public website may let Deaf users, SgSL learners, reviewers, developers,
and other visitors test the public ViaSign parser. The browser-facing path must
remain completely separate from private ViaSign development systems.

```text
viathorne-web
    -> public HTTPS API boundary
    -> public FastAPI service
    -> public viasign-parser package
    -> review-required response
```

The website must never call, import, mount, proxy, or expose the private ViaSign
repository, Temple Console, private datasets, review storage, motion engine, or
internal development API.

## User-facing truth

The testing interface must say clearly:

- this is an early experimental natural-English surface analyzer
- output is not final or fluent SgSL translation
- every result requires review
- motion and avatar output are unavailable
- the tool is unsuitable for emergency, legal, medical, or certified use
- unsupported and uncertain output is expected

The interface must show `outcome`, warnings, `review_required`, and
`motion_ready` without hiding them behind a developer panel.

## Privacy

- Do not ask users to enter private, sensitive, identifying, legal, medical, or
  emergency information.
- Do not persist input or parser output by default.
- Do not echo the submitted sentence in API success or error responses.
- Do not place input text in analytics, error tracking, access logs, or URLs.
- Do not use submissions to train, benchmark, or expand the parser without a
  separate informed-consent flow.
- A future feedback form must be optional and distinct from parsing.

## Deployment boundary

- Keep API credentials and deployment secrets out of browser code.
- Permit CORS only for explicit production and preview origins.
- Apply TLS, request limits, timeouts, and abuse controls at the deployment
  edge, and preserve the application rate limit in
  `docs/RATE_LIMIT_POLICY.md`.
- Keep the user's text in the form after `429`, announce the plain-language
  status, and do not require repeated typing while `Retry-After` elapses.
- Return public contract errors without stack traces or private paths.
- Pin the website to an explicit API contract version.

The website must reject responses unless the schema is
`viasign.parser.response.v1`, the contract is `1.1.0`, and the review and motion
invariants remain literal. For ordinary analysis it accepts only the four
closed surface categories, `sign_aware_form=null`, and an empty candidate-gloss
list. It must reject response fields containing submitted text, extracted
tokens, names, or fragments. The complete hosting checklist is in
`docs/PRODUCTION_DEPLOYMENT_GATE.md`.

The service reads:

```text
VIASIGN_HOST
VIASIGN_PORT
VIASIGN_CORS_ORIGINS
VIASIGN_ACCESS_LOG
VIASIGN_TRUST_RENDER_PROXY
```

Local defaults bind to `127.0.0.1:8000` and allow only the Astro development
origins at `localhost:4321` and `127.0.0.1:4321`. Production origins must be
listed explicitly. Wildcards, URL paths, query strings, fragments, and embedded
credentials are rejected.

## Accessibility boundary

The tester must be keyboard accessible, screen-reader understandable, usable at
high zoom, and clear without relying on color alone. Status text should use
plain language alongside machine codes.

Deaf-first review applies to the interaction design and claims, not only to the
parser's eventual linguistic rules.
