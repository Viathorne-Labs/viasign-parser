# Inert Render Service Audit V1

- **Status:** Provider refresh and exact 0.2.1 candidate evidence approved for
  publication; inert service update and activation blocked
- **Recorded:** 2026-07-13; refreshed 2026-07-17
- **Publication approval:** Repository owner approved all five checkpoint items
  on 2026-07-13
- **Published audit merge:** `842a9ad820e4ac919fb88371a3ab9199ebc74a79`
- **Internal-health publication approval:** Repository owner approved all five
  internal-health publication items on 2026-07-13
- **2026-07-17 evidence publication approval:** Repository owner approved all
  five deployment-evidence publication items; this does not authorize a Render
  update or public activation
- **Provider:** Render
- **Service:** `viasign-parser-api`
- **Live public-source commit:** `e8ca6a688c6905fba1f2f02646b665623f0c689e`
- **Reviewed deployment source:** `d88bc2664628135a04ee4961866fea2380e1343d`

This audit records the first approved inert Render service. It does not approve
DNS changes, production CORS, a website connection, maintenance-mode removal,
public traffic, or submissions. No submitted sentence was used to perform this
audit.

## 2026-07-17 read-only provider refresh

The authenticated Render dashboard still showed the service as Blueprint
managed from public repository `Viathorne-Labs/viasign-parser`, branch `main`,
in Singapore on one Starter instance with autoscaling off and no persistent
disk. Automatic deploys and pull-request previews remained off. Maintenance
mode remained enabled.

The live service still runs commit
`e8ca6a688c6905fba1f2f02646b665623f0c689e` and reports parser `0.2.0` from its
internal metadata route. The newer published parser `0.2.1` source at
`d88bc2664628135a04ee4961866fea2380e1343d` has not been deployed. Updating the
inert service requires a separate explicit approval.

The internal shell reconfirmed:

- `VIASIGN_PORT=10000`;
- `VIASIGN_CORS_ORIGINS` is the empty string;
- `VIASIGN_ACCESS_LOG=false`;
- `VIASIGN_TRUST_RENDER_PROXY=true`; and
- `/healthz` returns exactly `{"status":"ok"}`.

The default Render subdomain returned provider `404`, consistent with disabled
subdomain routing. `api.viathorne.com` remained **Waiting for DNS** and its
certificate remained **Waiting for Verification**; an external lookup did not
resolve the name. No DNS, TLS, CORS, website, maintenance, or traffic setting
was changed.

The most recent application log was the clean startup caused by Render platform
maintenance on 2026-07-16. It contained process startup and shutdown lines but
no request body, parser output, access-request line, error, exception, or
traceback. Metrics reported no network-request or response-time data in the
most recent 12-hour view. Workspace email notifications remained set to
**Only failure notifications**; recovery-alert coverage is still not claimed.

The dashboard exposes a regeneratable deploy hook to authorized workspace
users. Because its value was visible during this review, the hook must be
regenerated before any later deployment update. The hook value is not recorded
in this repository.

Any later update must use Render's **Deploy a specific commit** operation for
`d88bc2664628135a04ee4961866fea2380e1343d`; **Deploy latest commit** is not
approved for this candidate. The live event must show that exact commit before
internal health or metadata evidence is accepted.

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

- Render now shows an earlier successful deployment and a rollback control, but
  the two recorded live deployments use the same `e8ca6a6` source. A controlled
  rollback rehearsal remains unapproved and would not yet prove rollback from
  parser `0.2.1` to `0.2.0`.
- Custom-domain TLS and HTTP-to-HTTPS behavior cannot be verified without a
  separately approved DNS change.
- Exact `0.2.1` local image and bounded abuse checks passed, but live load and
  abuse evidence remains incomplete.
- Security and privacy deployment review, the remaining end-to-end unavailable
  states, broader Deaf/SgSL community review, and a consent-led pilot plan remain
  incomplete.

## Gate verdict

The approved inert service-creation and internal health gates are complete. The
read-only provider refresh and local exact-artifact review are complete. The
inert service update and full live-operations gate remain separately blocked.
Maintenance mode and empty CORS must remain, and the website must stay
disconnected.

Every parser response must still preserve `review_required=true` and
`motion_ready=false`. This audit does not establish linguistic correctness,
SgSL translation, motion readiness, accessibility approval, community
approval, or production safety.
