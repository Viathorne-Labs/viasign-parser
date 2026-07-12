# Production Deployment Gate

- **Status:** Inert service creation approved; public activation blocked
- **Last reviewed:** 2026-07-13
- **Applies to:** The public `viasign-parser` HTTP service

Render in Singapore is the selected provider and region. The provider-specific
facts and blockers are recorded in `docs/RENDER_HOSTING_DECISION.md`. On
2026-07-13 the repository owner approved one inert Blueprint sync and service
creation. That decision does not authorize DNS changes, production CORS,
website connection, maintenance-mode removal, visitor traffic, or submissions.

This gate is separate from the public-source release gate. Passing source
review does not authorize hosting, and passing hosting review does not authorize
publishing new linguistic rules or data.

## Allowed topology

```text
browser on an approved viathorne-web origin
    -> HTTPS public API origin
    -> edge request controls
    -> public viasign-parser artifact
    -> review-required response
```

The deployed artifact must be built only from this public repository. It must
not mount, import, call, or share a network, volume, credential, dataset, log
sink, or runtime identity with private ViaSign, Temple Console, motion, review,
or community-data systems.

## Frozen application boundary

Only these runtime routes may return a non-404 response:

```text
GET  /healthz
GET  /v1/meta
POST /v1/parse
```

Interactive documentation, runtime OpenAPI, translation, motion, avatar,
upload, feedback, corpus, review-administration, and private-source routes are
disabled. OpenAPI may still be generated offline for tests and release review.

Every parse response must use schema `viasign.parser.response.v1`, contract
`1.1.0`, `status=review_required`, `review_required=true`, and
`motion_ready=false`. The service returns `Cache-Control: no-store` on parse
responses and `X-Content-Type-Options: nosniff` on public responses.

The V0.1 surface analyzer may return only closed source-text categories. It must
not return submitted text, tokens, names, fragments, SgSL order, glosses,
identity fields, motion, or avatar data.

## Required controls before any public activation

### Artifact and process

- Build from a clean, reviewed public commit and record the exact commit hash.
- Generate the release path-and-hash manifest and complete provenance review.
- Lock runtime dependencies and complete dependency-license, secret, binary,
  private-path, and vulnerability scans.
- Run the complete test suite in the same artifact that will be deployed.
- Run as a non-root process with a read-only filesystem and no persistent volume.
- Provide no private repository, cloud-storage, database, model, or internal API
  credentials to the service.

The locked Python runtime license and vulnerability review is recorded in
`docs/THIRD_PARTY_DEPENDENCY_REVIEW.md`. It passed after upgrading Starlette to
the release containing all five fixes found by the initial audit. The local
arm64 and Linux amd64 container vulnerability, secret, configuration, and
runtime smoke review also passed and is recorded in
`docs/CONTAINER_SECURITY_REVIEW.md`. Both scans remain time-bounded and must be
repeated against the exact release artifact.

### Edge policy

- Require HTTPS and redirect or reject plaintext traffic.
- Accept only `GET`, `POST`, and required CORS `OPTIONS`; reject other methods.
- Reject request bodies above 4 KiB at the first application boundary. Render
  does not expose a Blueprint field for this edge limit, so do not describe it
  as provider-edge enforcement. The typed contract still enforces 1,000 text
  characters.
- Enforce the three-second application deadline below the website's five-second
  client timeout. Render's much longer platform maximum is not the safety
  control.
- Preserve the documented anonymous limit of 60 parse requests per minute per
  network identity with a burst of 20. Its shared-network accessibility impact
  and fail-closed behavior are recorded in `docs/RATE_LIMIT_POLICY.md`.
- Return plain, non-identifying `413`, `429`, and `5xx` responses without input,
  stack traces, local paths, or private operational details.
- Do not cache `POST /v1/parse` requests or responses.

The application now enforces a 4 KiB parse-body ceiling, a three-second
fail-closed parse deadline, and a transient, single-instance per-network token
bucket as defense in depth. Render does not expose equivalent Blueprint edge
fields, so the limitation and stop conditions are recorded in
`docs/EDGE_AND_OPERATIONS_POLICY.md`. Horizontal scaling remains blocked because
the in-memory counters are intentionally not shared or persisted.

### Origin policy

- The frozen production values are recorded in
  `docs/ORIGIN_AND_CSP_POLICY.md`: the only website origin is
  `https://www.viathorne.com` and the only API origin is
  `https://api.viathorne.com`. They are approved configuration targets, not
  active deployment settings.
- Set `VIASIGN_CORS_ORIGINS` to the exact HTTPS production and deliberately
  approved preview origins only.
- Never use `*`, reflected origins, credentials, URL paths, or non-local HTTP
  origins.
- Treat CORS as a browser boundary, not authentication or abuse prevention.

### Logging and retention

- Do not log request bodies, normalized input, response bodies, candidate
  glosses, warning text, query strings, or URL-encoded input.
- Do not send parser submissions to analytics, tracing, replay, error-reporting,
  training, benchmarks, or feedback systems.
- If operational logs are required, restrict them to timestamp, route template,
  method, status, duration class, edge request ID, and coarse rate-limit events.
- Record the hosting provider's unavoidable IP and network-log behavior, access
  controls, region, retention period, deletion process, and incident contact.
- Align the website privacy notice with the recorded provider behavior before
  allowing visitor submissions.

For the selected Pro workspace, Render documents HTTP request metadata and a
14-day dashboard retention period. Uvicorn access logs are disabled to avoid a
second copy. Sentence text must remain in the body and must never be printed.
The website Privacy notice has been prepared with these provider-specific
limits, but the production API value remains unset and visitor submissions are
still blocked.

### Monitoring and incident response

- Monitor health, error rate, latency, rate-limit events, and invariant failures
  without capturing parser input or output.
- Treat any loss of schema, contract, review, motion, route, provenance, or
  logging boundaries as a release-blocking incident.
- Document a one-step rollback that disables the website API origin and a
  service rollback to the last reviewed artifact.

The monitoring signals, conservative stop conditions, activation order, and
configuration-aware rollback sequence are frozen in
`docs/EDGE_AND_OPERATIONS_POLICY.md`. The separately approved inert service now
exists; available live evidence and the still-blocked health, domain, rollback,
and human-review items are recorded in
`docs/INERT_RENDER_SERVICE_AUDIT_V1.md`.

## Review gates

V1 will not use a remote Render preview: its separate public hostname would not
be protected by Netlify access control or CORS. Pre-release review remains local.
The following evidence must be recorded before any public activation can accept
test submissions:

- [x] Repository owner approved the published V2 source artifact and the inert
  Render host configuration.
- [ ] Security and privacy review approves the complete edge, logging, and
  retention policy; the origin/CSP and privacy-notice preparation is recorded.
- [ ] Website and API contract-version checks pass together.
- [ ] Unavailable, timeout, malformed, incompatible, uncertain, and unsupported
  states pass end-to-end checks.
- [ ] Keyboard, zoom/reflow, reduced-motion, contrast, and screen-reader checks
  pass on the final local candidate and are repeated after activation if one is
  separately approved.
- [ ] Deaf/SgSL reviewers approve the claims, examples, and review language.
- [ ] A short, consent-led pilot plan defines audience, duration, feedback path,
  moderation, incident owner, and stop conditions.
- [x] A separate approval for inert service creation is recorded; public
  activation remains separately blocked.

Until every activation item is satisfied, the furthest approved cloud state is
one inert service in maintenance mode with empty CORS, no DNS change, and no
website connection.
