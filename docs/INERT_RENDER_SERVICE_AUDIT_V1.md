# Inert Render Service Audit V1

- **Status:** Owner-approved internal health update; activation blocked
- **Recorded:** 2026-07-13
- **Publication approval:** Repository owner approved all five checkpoint items
  on 2026-07-13
- **Published audit merge:** `842a9ad820e4ac919fb88371a3ab9199ebc74a79`
- **Internal-health publication approval:** Repository owner approved all five
  internal-health publication items on 2026-07-13
- **Provider:** Render
- **Service:** `viasign-parser-api`
- **Live public-source commit:** `e8ca6a688c6905fba1f2f02646b665623f0c689e`

This audit records the first approved inert Render service. It does not approve
DNS changes, production CORS, a website connection, maintenance-mode removal,
public traffic, or submissions. No submitted sentence was used to perform this
audit.

## Verified inert state

The Render dashboard showed the exact public merge commit above as live in one
Singapore Starter instance with 0.5 CPU and 512 MB memory. The service uses the
public repository's Dockerfile, tracks `main`, and has automatic deploys, pull
request previews, autoscaling, and edge caching disabled. Blueprint automatic
sync is paused.

The live environment matched the reviewed inert boundary:

- `VIASIGN_HOST=0.0.0.0`
- `VIASIGN_PORT=10000`
- `VIASIGN_CORS_ORIGINS` is empty
- `VIASIGN_ACCESS_LOG=false`
- `VIASIGN_TRUST_RENDER_PROXY=true`
- the health-check path is `/healthz`
- no persistent disk, database, private source mount, or private credential was
  added

`api.viathorne.com` is registered in Render but has no approved DNS route. The
dashboard showed DNS and certificate setup waiting. The default
`onrender.com` hostname returned a provider-generated `404` with blocked
subdomain routing rather than reaching the application.

Maintenance mode is enabled. Render did not apply the Blueprint's declared
`maintenanceMode.enabled: true` value during initial service creation, so the
owner enabled it immediately in the dashboard and verified the corresponding
service event. Future syncs must therefore verify live maintenance state; the
checked-in Blueprint declaration is not sufficient evidence by itself.

## Internal health verification

On 2026-07-13, the owner approved the next gate in the recorded sequence. The
service was queried only from Render's internal shell at
`http://127.0.0.1:10000/healthz`; no public hostname, parser sentence, or visitor
request was used.

The minimal container does not include `curl`, so the first attempted command
made no request. A Python standard-library request then returned:

```text
HTTP 200
{"status":"ok"}
```

The same shell confirmed that `VIASIGN_CORS_ORIGINS` remained the empty string.
The dashboard still showed maintenance mode enabled, the default Render
subdomain disabled, automatic deploys off, and custom-domain verification
waiting for DNS. The application log remained startup-only: it showed no access
request, submitted text, parser output, error, exception, traceback, failure, or
panic after the internal check.

## Logs, metrics, and notifications

The application logs showed a clean startup with no error, exception,
traceback, failure, or panic. No Uvicorn access-request line, submitted text,
name-sign example, parser output, or reviewer identity appeared. No external
log stream, analytics, tracing, replay, or error-reporting integration was
configured.

The provider metrics page was available and showed the configured instance
limits, instance count, network metrics, and one technical request. It showed
no response-time activity. This is only evidence that the monitoring surfaces
exist; it is not load, latency, or reliability evidence.

Workspace notifications use email with **Only failure notifications**. Render
documents that this setting covers service build or deploy failures and a
running service becoming unhealthy. Recovery notifications require the broader
**All notifications** setting, so recovery-alert coverage is not claimed.

Official reference: https://render.com/docs/notifications

## Evidence still blocked or unavailable

- This is the first successful deploy, so no earlier successful artifact exists
  and a rollback control was not available. No extra deploy will be created
  merely to manufacture rollback evidence.
- Custom-domain TLS and HTTP-to-HTTPS behavior cannot be verified without a
  separately approved DNS change.
- Exact-release load, abuse, accessibility, privacy, and Deaf/SgSL review remain
  incomplete.

## Gate verdict

The approved inert service-creation and internal health gates are complete. The
full live-operations gate is only partially complete. Maintenance mode and
empty CORS must remain, and the website must stay disconnected.

Every parser response must still preserve `review_required=true` and
`motion_ready=false`. This audit does not establish linguistic correctness,
SgSL translation, motion readiness, accessibility approval, community
approval, or production safety.
