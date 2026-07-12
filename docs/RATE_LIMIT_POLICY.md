# Anonymous Pilot Rate-limit Policy

- **Status:** Application policy implemented and locally verified; deployment
  remains blocked
- **Recorded:** 2026-07-12
- **Route:** `POST /v1/parse` only
- **Sustained allowance:** 60 requests per minute per network identity
- **Burst allowance:** 20 requests
- **Storage:** Process memory only; no persistence or logging

This control reduces accidental bursts and simple single-network abuse. It is
not authentication, a linguistic safety check, or complete distributed-attack
protection.

## Client identity boundary

In the reviewed Render configuration, the application reads the first address
in `X-Forwarded-For`. Render documents that applications should use this header
for the true client address because inbound traffic passes through Cloudflare
and Render's load balancers.

The application trusts that header only when
`VIASIGN_TRUST_RENDER_PROXY=true`. This setting is enabled in `render.yaml` and
must not be enabled on an unreviewed hosting path. In Render proxy mode, a
missing or invalid address returns a fail-closed `503`; the parse body is not
processed.

Official references:

- https://render.com/articles/how-render-handles-ddos-attacks
- https://www.uvicorn.org/settings/#http

## Privacy behavior

The limiter:

- creates a random HMAC key at each process start
- immediately converts the network address to a keyed SHA-256 digest
- stores only the digest, token count, and monotonic timestamps
- never stores the submitted sentence in the limiter
- never writes limiter state to disk, logs, analytics, or a datastore
- expires inactive entries after ten minutes
- caps the in-memory table at 10,000 entries and evicts the least recently used
  entry at capacity
- resets all counters when the process restarts

The hosting platform can still process network metadata as documented in
`docs/RENDER_HOSTING_DECISION.md`. The in-application HMAC does not remove the
provider's separate logging boundary.

## Accessible `429` behavior

When the bucket is empty, the service returns:

- HTTP `429 Too Many Requests`
- a numeric `Retry-After` header
- `Cache-Control: no-store`
- `X-Content-Type-Options: nosniff`
- CORS headers for an approved website origin
- code `rate_limit_exceeded`
- plain text explaining that the allowance is network-shared, how long to
  wait, and that the submitted text was not processed
- `review_required=true`
- `motion_ready=false`

The response does not echo the submitted sentence, network address, digest,
or operational details. Health and metadata routes are not rate-limited.

## Deaf-first shared-network tradeoff

People on the same household, school, library, workplace, mobile carrier,
VPN, or community-centre network can share one public address. The 60-per-
minute sustained allowance and burst of 20 are deliberately lenient for a
small pilot so several people can test short phrases without an immediate
block.

If legitimate testers encounter `429`, do not silently lower access or ask for
identity documents. Review the limit with Deaf/SgSL testers and increase or
redesign it before expanding the pilot. The website must keep the user's text
in the input field so waiting does not erase their work.

## Scaling and abuse limitations

The limiter is correct only for the planned one-process, one-instance Starter
pilot. Counts are not shared across processes or instances. Horizontal scaling
is blocked until a separate privacy review approves a shared limiter and its
retention behavior.

Rotating addresses or a distributed attacker can bypass a per-network bucket.
Render's Cloudflare-backed DDoS filtering remains a separate layer, but it does
not replace this application policy. Sustained application abuse is a stop
condition for the pilot.

## Local verification evidence

Focused API and container checks verified that:

- the first 20 immediate parse requests are accepted
- the next same-network request returns the safe `429` contract
- another client address behind the same proxy remains independent
- missing or malformed proxy identity fails closed with `503`
- body-size rejection still returns the safe `413` contract
- approved CORS headers remain readable on `429`
- the limiter table contains only 32-byte keyed digests
- health and metadata remain available without a client-network header

The local `viathorne-web` tester was also exercised against an exhausted
bucket. Its live status announced the wait, the sentence remained in the
textarea, the button was disabled with visible wait text, and the same control
was restored after `Retry-After`. No browser console error was recorded. The
complete 26-page Astro validation also passed.

These are implementation and accessibility-smoke checks, not Deaf/SgSL human
review or permission for public traffic.

## Change rule

Changing the allowance, identity source, hashing, retention, response text,
instance count, or storage design requires:

1. focused tests
2. privacy review
3. shared-network accessibility review
4. deployment-document updates
5. explicit approval before public traffic
