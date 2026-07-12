# Render Hosting Decision

- **Status:** Inert service live; public activation blocked
- **Recorded:** 2026-07-13
- **Provider:** Render
- **Owner-reported workspace plan:** Pro
- **Planned service region:** Singapore
- **Planned service instance:** Starter, one public web service

The repository owner approved one inert Blueprint sync and service creation on
2026-07-13. That approval is limited to the checked-in configuration:
maintenance mode on, empty CORS, automatic deploys off, one Starter instance,
and no website connection or DNS change. It does not approve production CORS,
maintenance-mode removal, visitor traffic, or submissions.

The inert service now runs exact public merge commit
`e8ca6a688c6905fba1f2f02646b665623f0c689e`. The live configuration, isolation,
logs, metrics surface, notifications, and remaining evidence gaps are recorded
in `docs/INERT_RENDER_SERVICE_AUDIT_V1.md`. The service remains in maintenance
mode with empty CORS and no website or DNS connection.

## Why Render fits this stage

Render supports Python and FastAPI web services, Docker deployments, managed
TLS, custom domains, health checks, DDoS protection, and rollback. Singapore is
a supported service region. The service region cannot be changed after service
creation, so `singapore` is explicit in `render.yaml`.

Official references:

- https://render.com/docs/web-services
- https://render.com/docs/deploy-fastapi
- https://render.com/docs/regions
- https://render.com/docs/blueprint-spec

## Planned boundary

```text
Netlify-hosted viathorne-web
    -> HTTPS api.viathorne.com
    -> Render public web service in Singapore
    -> public viasign-parser container only
```

The Render service has no database, persistent disk, private repository mount,
private ViaSign credential, Temple Console connection, model service, review
store, or analytics integration.

The checked-in Blueprint intentionally uses:

- `autoDeployTrigger: off`
- maintenance mode enabled
- CORS disabled with an empty origin list
- no PR preview generation
- exactly one service instance
- `api.viathorne.com` as the only planned custom domain
- a disabled default `onrender.com` subdomain after the custom domain is active
- a health check at `/healthz`
- an image-level health check against `/healthz`
- a non-root Docker runtime
- one pinned runtime dependency set
- disabled Uvicorn access logs and server header

These defaults make an accidental initial deployment unusable to the website.
They are not substitutes for explicit deployment approval.

## Local artifact verification

The candidate image was built locally from the pinned Python base-image digest
and `requirements.lock`. A running container was verified to:

- run as numeric user and group `10001:10001`
- keep application source and dependencies root-owned and non-writable by the
  runtime user
- expose port `10000` with no Uvicorn access log or server header
- return `200` from `/healthz` and `/v1/meta`
- return an uncertain parse result with `review_required=true` and
  `motion_ready=false`
- return `413 request_too_large` above the 4 KiB body ceiling
- return a fail-closed `503 parse_timeout` without releasing buffered output
  when the three-second parse deadline is exceeded
- return `404` from `/docs`
- return the configured local CORS origin and `Cache-Control: no-store`
- pass `pip check` with no broken runtime requirements

The final pinned Alpine image was scanned locally with Trivy 0.72.0 across all
vulnerability severities, embedded secrets, and Dockerfile configuration. It
reported zero operating-system or Python-package vulnerabilities, no secret
findings, and zero configuration failures. The evidence and the rejected
Debian-base candidates are recorded in
`docs/CONTAINER_SECURITY_REVIEW.md`.

This is local arm64 and Linux amd64 artifact evidence only. It is not a Render
deployment result, and it must be repeated against the exact approved release
image before deployment.

## Pro logging facts

Render documents that Pro workspaces retain dashboard logs for 14 days and add
an HTTP request log for each request arriving from the public internet. The
documented fields include method, status, requested URL/path, host, and Render
request ID. Application output is also collected from stdout and stderr.

ViaSign therefore keeps sentence text in the JSON body only, never the URL, and
disables Uvicorn access logs to avoid duplicating client and request metadata in
application logs. Code must never print request bodies, normalized sentences,
responses, candidate glosses, or warning text.

Official reference: https://render.com/docs/logging

The website Privacy notice now describes Render's planned technical request
processing and 14-day dashboard-log retention. This wording does not enable
submissions or authorize deployment.

## Public-access limitation

Render web services and Render PR previews receive public URLs. A Pro preview
environment is disposable deployment infrastructure, not access control.
Protecting the Netlify website also does not protect the separate Render URL,
and CORS does not stop non-browser requests. V1 therefore rejects remote Render
previews and keeps pre-release human review local.

Render provides automatic DDoS protection, but its public documentation does
not provide the per-client pilot quota required by ViaSign's deployment gate.
The application therefore implements the privacy-preserving, single-instance
policy in `docs/RATE_LIMIT_POLICY.md`. No preview or public parser traffic is
approved until the remaining access-control, privacy, and human-review gates
are complete.

Official references:

- https://render.com/docs/preview-environments
- https://render.com/docs/ddos-protection

## Custom domain and TLS

The intended production name is `api.viathorne.com`. The inert Blueprint may
register it in Render because disabling the default Render subdomain requires a
custom domain. This gate does not authorize a DNS change, so the name must not
route public traffic yet.
Render automatically manages TLS for custom domains and redirects their HTTP
traffic to HTTPS. The Blueprint disables the default `onrender.com` address once
the custom domain is active; live verification must confirm it returns `404`
without reaching the application.

Official references:

- https://render.com/docs/custom-domains
- https://render.com/docs/tls

## Remaining blockers

- [x] Publish the reviewed repository artifact at
  `https://github.com/Viathorne-Labs/viasign-parser`, commit `e9e2f94`.
- [x] Pin the Python base image by multi-platform digest, build it locally, and
  pass the local container smoke boundary.
- [x] Complete the local container vulnerability, secret, and configuration
  scan; repeat against the exact release artifact as recorded in
  `docs/CONTAINER_SECURITY_REVIEW.md`.
- [x] Complete dependency-license and vulnerability review of
  `requirements.lock`; evidence is in `docs/THIRD_PARTY_DEPENDENCY_REVIEW.md`.
- [x] Select and locally verify a per-network rate limit and accessible `429`
  behavior; evidence and limitations are in `docs/RATE_LIMIT_POLICY.md`.
- [x] Reject remote Render previews for V1; pre-release accessibility and
  Deaf/SgSL review remains local as recorded in
  `docs/EDGE_AND_OPERATIONS_POLICY.md`.
- [x] Prepare website privacy wording for Render and the 14-day request logs;
  the tester remains disabled.
- [x] Freeze the exact CORS and Content Security Policy values in
  `docs/ORIGIN_AND_CSP_POLICY.md`; activation remains blocked.
- [x] Record Render's body-limit and timeout gaps, add a three-second fail-closed
  application deadline, and freeze monitoring, stop, and rollback procedures in
  `docs/EDGE_AND_OPERATIONS_POLICY.md`.
- [ ] Complete live domain, health, notification, metric, log, and rollback
  evidence. The exact internal health response is verified; custom-domain TLS
  and rollback remain unavailable or separately blocked.
- [ ] Complete assistive-technology and Deaf/SgSL review.
- [x] Record explicit approval for one inert Blueprint sync and service
  creation; activation remains unapproved.

Until those items are complete, maintenance mode and empty CORS must remain.
