# Origin and Content Security Policy

- **Status:** Production values frozen; activation blocked
- **Recorded:** 2026-07-12
- **Canonical website origin:** `https://www.viathorne.com`
- **Intended API origin:** `https://api.viathorne.com`

This record fixes the browser origin boundary before any Render deployment or
website API enablement. It does not approve a Blueprint sync, custom domain,
preview, public traffic, repository publication, commit, or push.

## Exact production values

When a separately approved production deployment is activated, the API CORS
allowlist must be exactly:

```text
https://www.viathorne.com
```

The website Content Security Policy must permit the API only through:

```text
connect-src 'self' https://api.viathorne.com
```

The website may then set `PUBLIC_VIASIGN_API_URL` to exactly:

```text
https://api.viathorne.com
```

Until that separate deployment decision, `render.yaml` must keep
`VIASIGN_CORS_ORIGINS` empty, maintenance mode enabled, and automatic deploys
off. The production website environment must also omit
`PUBLIC_VIASIGN_API_URL`, leaving the tester disabled.

## Explicit exclusions

The production API must not allow:

- the apex origin `https://viathorne.com`
- any `netlify.app` deploy-preview, branch-deploy, or site origin
- the Render service's `onrender.com` origin as a browser caller
- wildcard, reflected, regex, suffix, or credentialed origins
- origins containing a path, query, fragment, user information, or secret
- non-local HTTP origins

An origin is not approved merely because it belongs to Viathorne, Netlify, or
Render. A future preview must name each exact HTTPS website origin in a new
review record. It must never be enabled with a wildcard or domain suffix.

Local development remains limited to the existing loopback origins:

```text
http://localhost:4321
http://127.0.0.1:4321
```

These local values are development defaults only and must not be copied into a
production Render environment.

## Boundary and limitations

CORS controls which browser origins can read API responses. It is not
authentication and does not stop direct, scripted, or non-browser requests.
The Content Security Policy limits where the website can initiate connections;
it does not protect the independently reachable API hostname.

Every accepted parser response must still fail closed unless
`review_required=true` and `motion_ready=false` are present with the frozen
schema and contract versions. Origin approval does not make draft grammar
planning linguistically correct, motion-ready, or suitable for emergency,
legal, medical, certified, or final SgSL communication.

## Rollback

The website rollback is to remove `PUBLIC_VIASIGN_API_URL` and redeploy the
static site. The API rollback is to restore an empty `VIASIGN_CORS_ORIGINS`,
enable Render maintenance mode, and roll back or suspend the service under the
separate deployment runbook. Removing the website value must disable the tester
without removing the static ViaSign explanation and limitations.
