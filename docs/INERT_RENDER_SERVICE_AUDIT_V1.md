# Inert Render Service Audit V1

- **Status:** Exact 0.2.1 inert service update complete; post-deployment evidence
  publication approved; activation blocked
- **Recorded:** 2026-07-13; refreshed 2026-07-17
- **Publication approval:** Repository owner approved all five checkpoint items
  on 2026-07-13
- **Published audit merge:** `842a9ad820e4ac919fb88371a3ab9199ebc74a79`
- **Internal-health publication approval:** Repository owner approved all five
  internal-health publication items on 2026-07-13
- **2026-07-17 evidence publication approval:** Repository owner approved all
  five deployment-evidence publication items; this does not authorize a Render
  update or public activation
- **Published deployment-evidence merge:**
  `d6c59f7c0c9b1e00aad2b73e42cebfb38ff2d172` (PR #5)
- **2026-07-17 provider-mutation approval:** Repository owner approved exactly
  deploy-hook regeneration and **Deploy a specific commit** for `d88bc266`; the
  authorization is consumed and permits no additional provider change
- **2026-07-17 post-deployment evidence publication:** Repository owner approved
  the evidence-only publication gate; no provider or activation change is
  authorized
- **Provider:** Render
- **Service:** `viasign-parser-api`
- **Live public-source commit:** `d88bc2664628135a04ee4961866fea2380e1343d`
- **Previous live commit:** `e8ca6a688c6905fba1f2f02646b665623f0c689e`
- **Reviewed deployment source:** `d88bc2664628135a04ee4961866fea2380e1343d`

This audit records the first approved inert Render service. It does not approve
DNS changes, production CORS, a website connection, maintenance-mode removal,
public traffic, or submissions. No submitted sentence was used to perform this
audit.

## Historical pre-deployment provider refresh (2026-07-17)

At this pre-deployment snapshot, the authenticated Render dashboard showed the
service as Blueprint
managed from public repository `Viathorne-Labs/viasign-parser`, branch `main`,
in Singapore on one Starter instance with autoscaling off and no persistent
disk. Automatic deploys and pull-request previews remained off. Maintenance
mode remained enabled.

The live service then ran commit
`e8ca6a688c6905fba1f2f02646b665623f0c689e` and reported parser `0.2.0` from its
internal metadata route. The newer published parser `0.2.1` source at
`d88bc2664628135a04ee4961866fea2380e1343d` had not been deployed. Updating the
inert service required the separate approval recorded below.

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

The dashboard exposed a regeneratable deploy hook to authorized workspace
users. Because its value was visible during this review, the approved runbook
required regeneration before the deployment update. The hook value was not
recorded in this repository.

The approved runbook required Render's **Deploy a specific commit** operation
for `d88bc2664628135a04ee4961866fea2380e1343d`; **Deploy latest commit** was not
approved. The later live event had to show that exact commit before internal
health or metadata evidence could be accepted.

## 2026-07-17 approved inert service update

After the owner approved exactly two provider mutations, the deploy hook was
regenerated through Render's confirmation flow. Neither the prior nor rotated
hook value was copied, recorded, or invoked. That one-time authorization was
then consumed by Render's **Deploy a specific commit** flow for full commit
`d88bc2664628135a04ee4961866fea2380e1343d`. **Deploy latest commit** was never
selected.

Render deployment `dep-d9d4kfn41pts73djkc20` checked out the exact commit,
completed its Docker build, started cleanly, and reached **Live**. Before any
health evidence was accepted, the deployment event itself was verified against
the full commit. The internal shell then returned:

```text
VIASIGN_PORT=10000
VIASIGN_CORS_ORIGINS=
VIASIGN_ACCESS_LOG=false
VIASIGN_TRUST_RENDER_PROXY=true
/healthz {"status":"ok"}
/v1/meta parser_version=0.2.1 maturity=pre-alpha
/v1/meta grammar_rules_available=false
/v1/meta review_required=true motion_ready=false
```

No parser sentence or name-sign example was submitted. Application and deploy
logs contained the expected build, startup, old-instance shutdown, and port
detection lines, with no access-request line, request body, parser output,
error, exception, or traceback.

After deployment, the dashboard still showed maintenance mode enabled,
automatic deploys and pull-request previews off, the Render subdomain disabled,
and `api.viathorne.com` waiting for DNS and certificate verification. The
disabled Render hostname returned provider `404`, the custom hostname had no A
record, and the production website still reported that the tester was not
configured. No DNS, TLS, CORS, website, maintenance, traffic, scaling, disk, or
notification setting changed.

The previous `e8ca6a6` deployment is available as a rollback candidate. A
rollback rehearsal was not authorized and was not performed. The repository
owner separately approved publication of this post-deployment evidence. That
decision does not authorize public activation or any provider change.

## Historical initial inert state (2026-07-13)

The Render dashboard showed exact public commit
`e8ca6a688c6905fba1f2f02646b665623f0c689e` as live in one Singapore Starter
instance with 0.5 CPU and 512 MB memory. The service used the public
repository's Dockerfile, tracked `main`, and had automatic deploys, pull request
previews, autoscaling, and edge caching disabled. Blueprint automatic sync was
paused.

The initial live environment matched the reviewed inert boundary:

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

Maintenance mode was enabled. Render did not apply the Blueprint's declared
`maintenanceMode.enabled: true` value during initial service creation, so the
owner enabled it immediately in the dashboard and verified the corresponding
service event. Future syncs must therefore verify live maintenance state; the
checked-in Blueprint declaration is not sufficient evidence by itself.

## Historical initial internal health verification (2026-07-13)

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

## 2026-07-17 `d88bc266` post-deployment logs, metrics, and notifications

The application logs showed a clean startup with no error, exception,
traceback, failure, or panic. No Uvicorn access-request line, submitted text,
name-sign example, parser output, or reviewer identity appeared. No external
log stream, analytics, tracing, replay, or error-reporting integration was
configured.

The provider metrics page was available and showed the configured instance
limits, instance count, and network metrics. The immediate post-deploy snapshot
showed three aggregated requests in the 12-hour view; it did not establish
visitor traffic or input processing. This is only evidence that the monitoring
surfaces exist; it is not load, latency, or reliability evidence.

Workspace notifications use email with **Only failure notifications**. Render
documents that this setting covers service build or deploy failures and a
running service becoming unhealthy. Recovery notifications require the broader
**All notifications** setting, so recovery-alert coverage is not claimed.

Official reference: https://render.com/docs/notifications

## Evidence still blocked or unavailable

- Render now shows the prior `e8ca6a6` parser `0.2.0` deployment as a rollback
  candidate for the live `d88bc266` parser `0.2.1` artifact. A controlled
  rollback rehearsal remains unapproved.
- Custom-domain TLS and HTTP-to-HTTPS behavior cannot be verified without a
  separately approved DNS change.
- Exact `0.2.1` local image and bounded abuse checks passed, but live load and
  abuse evidence remains incomplete.
- Security and privacy deployment review, the remaining end-to-end unavailable
  states, broader Deaf/SgSL community review, and a consent-led pilot plan remain
  incomplete.

## Gate verdict

The approved inert service-creation, internal health, exact-artifact review,
hook rotation, specific-commit deployment, and evidence-publication gates are
complete. The full live-operations gate and public activation remain separately
blocked. Maintenance mode and empty CORS must remain, and the website must stay
disconnected.

Every parser response must still preserve `review_required=true` and
`motion_ready=false`. This audit does not establish linguistic correctness,
SgSL translation, motion readiness, accessibility approval, community
approval, or production safety.
