# Edge and Operations Policy

- **Status:** Inert service live; activation blocked; live evidence partial
- **Recorded:** 2026-07-13
- **Operational owner:** Repository owner
- **Public service model:** One stateless Render web-service instance

This record closes the configuration-design portion of the Render edge and
operations gate. On 2026-07-13 the repository owner approved one inert Blueprint
sync and service creation. That approval does not include DNS changes,
production CORS, website connection, maintenance-mode removal, remote previews,
public traffic, or submissions.

The approved inert service now runs exact reviewed parser commit
`d88bc2664628135a04ee4961866fea2380e1343d` at parser `0.2.1`. The prior
`e8ca6a688c6905fba1f2f02646b665623f0c689e` deployment is the unexercised
rollback candidate. The available live evidence and honest gaps are recorded in
`docs/INERT_RENDER_SERVICE_AUDIT_V1.md`.

## Provider findings and honest limits

Render documents that web-service HTTP responses may run for up to 100 minutes.
That platform maximum is not an appropriate ViaSign request deadline. The
current Blueprint specification also provides no per-service field for a 4 KiB
request-body limit or a shorter HTTP response deadline.

ViaSign must therefore not claim that Render enforces these two controls at its
edge. The public service instead applies both controls at the first application
boundary:

- `POST /v1/parse` has a three-second total application deadline, below the
  website's five-second client deadline.
- A timed-out request returns a no-store `503 parse_timeout` with
  `review_required=true` and `motion_ready=false`; buffered parser output is not
  sent.
- The per-network rate limiter runs before body parsing, and the body guard
  stops buffering and returns `413` as soon as input exceeds 4,096 bytes.
- The typed request contract separately limits text to 1,000 characters.

This protects application memory and keeps responses fail-closed, but it is not
an external web-application firewall. Render's platform DDoS protection remains
provider-managed. An exact release candidate must still be load-checked before
public activation, and unexpected oversized or slow traffic is a stop condition.

Official references:

- https://render.com/docs/render-vs-vercel-comparison
- https://render.com/docs/blueprint-spec
- https://render.com/docs/ddos-protection

## Review-access decision

V1 will not use a remote Render service preview or preview environment. Those
features create a separate public `onrender.com` URL; a shareable URL, CORS, or
Netlify site protection would not make the API private. Adding browser-visible
credentials or credentialed CORS would also weaken the frozen public boundary.

Pre-release browser, accessibility, and Deaf/SgSL wording review must therefore
remain local or take place through a directly supervised local build. No
sentence or reviewer identity is to be collected by the API for this review.

The production candidate declares only `api.viathorne.com` and disables the
default Render subdomain. Automatic previews remain absent. Maintenance mode,
empty CORS, and disabled automatic deploys remain the inert defaults.

Official references:

- https://render.com/docs/service-previews
- https://render.com/docs/preview-environments
- https://render.com/docs/custom-domains
- https://render.com/docs/maintenance-mode

## Monitoring without sentence capture

Before maintenance mode can be disabled, the service owner must configure
Render email notifications for deploy failure and unhealthy-service events.
The owner must verify that `/healthz` returns only `{"status":"ok"}` and that
Render's HTTP health check is active.

The initial pilot uses only provider-generated operational evidence:

- health and unhealthy/recovery events
- request volume grouped by status and host
- response-latency percentiles, especially p99
- CPU and memory usage
- deploy status and rollback availability
- technical request IDs when needed for an incident

No analytics, tracing, replay, error-reporting SDK, request-body logging, or
custom event containing input or parser output may be added. During an approved
short pilot, the owner checks the dashboard at activation, after 15 minutes,
and at least hourly while submissions remain enabled.

Official references:

- https://render.com/docs/health-checks
- https://render.com/docs/service-metrics
- https://render.com/docs/notifications
- https://render.com/docs/logging

## Stop conditions

Immediately disable submissions if any of these occur:

- a response loses the frozen schema, contract, parser ID,
  `review_required=true`, or `motion_ready=false`
- input or parser output appears in any log, metric, alert, or third-party tool
- the custom domain or Render subdomain behaves differently from the approved
  host policy
- repeated `5xx`, timeouts, oversized requests, or rate-limit events indicate
  abuse or unreliable service
- p99 response latency reaches two seconds during the small pilot
- memory remains above 80 percent of the selected instance limit
- an accessibility, privacy, security, or Deaf/SgSL reviewer requests a stop

These are conservative pilot stop conditions, not performance promises.

## Activation order

Each step requires evidence before the next:

1. Approve a clean public commit and repeat tests, dependency audit, provenance
   checks, and exact-image security scans.
2. Use the recorded approval to create one inert service with maintenance mode
   on, empty CORS, one instance, and automatic deploys off. Do not change DNS.
3. Verify `api.viathorne.com` TLS and HTTPS redirection, and verify the default
   `onrender.com` hostname returns `404` without reaching the application.
4. Verify health checks, failure notifications, metrics, request logs, region,
   instance type, and log retention in the live Render workspace.
5. Retain the completed bounded local accessibility and repository-owner
   wording evidence, complete broader Deaf/SgSL community review, and record a
   consent-led pilot plan with an incident owner and stop conditions.
6. In a separately reviewed change, set API CORS to exactly
   `https://www.viathorne.com`, configure the website's exact API origin, and
   re-run the website/API contract checks.
7. Record a final public-activation approval before disabling maintenance mode.

## Rollback order

Rollback is an operational sequence, not only a code rollback:

1. Remove the website's `PUBLIC_VIASIGN_API_URL` and redeploy the static site so
   the tester becomes disabled.
2. Enable Render maintenance mode immediately.
3. Restore empty API CORS and confirm the Render subdomain remains disabled.
4. If code caused the incident, roll back to the last recorded successful
   artifact. Render rollback does not replace current service configuration, so
   maintenance, CORS, domains, and notifications must be checked separately.
5. Confirm the website shows the unavailable state, the API is unreachable from
   the public internet, and no input or parser output was captured.
6. Record only timestamps, technical request IDs, status classes, actions, and
   outcomes in the incident note. Do not reproduce tester sentences.

Official reference: https://render.com/docs/rollbacks

## Remaining live evidence

The inert-service audit verified the connected public repository, exact live
commit, Singapore Starter instance, disabled default subdomain, maintenance
state, empty CORS, clean startup logs, metrics surface, failure notifications,
and an internal `HTTP 200` health response with exactly `{"status":"ok"}`. It
also found that initial service creation did not apply the Blueprint's declared
maintenance state; maintenance was enabled immediately and verified in the
dashboard. Future operations must check live state rather than trusting
configuration intent alone.

The following evidence remains incomplete or blocked:

- custom-domain TLS and HTTP-to-HTTPS behavior, which require approved DNS
- a controlled rollback rehearsal to the prior `e8ca6a6` artifact, which
  requires separate approval
- exact-release load and abuse checks
- post-activation repetition of the relevant assistive-technology checks
- security/privacy deployment review
- broader Deaf/SgSL community review and a consent-led pilot plan

Maintenance mode and empty CORS must remain until those items and every human
review gate are complete.
