# ViaSign Parser Public Architecture

- **Status:** Public pre-alpha boundary
- **Last updated:** 2026-07-12
- **Repository:** `viasign-parser`

## Purpose

This repository is the clean public architecture for ViaSign's grammar-first
parser prototype. It exists so browser integration, contract review, safety
testing, and future public contribution can happen without exposing or depending
on private ViaSign source, data, review systems, or motion research.

The current service performs draft grammar planning only. It is not a finished
SgSL translator, an interpreter, a linguistic authority, or a motion/avatar
system. It must not be used for certified, emergency, legal, or medical
communication.

## System context

```text
viathorne-web browser
    -> HTTPS public API origin
    -> CORS, deadline, rate-limit, and body guards
    -> strict FastAPI request model
    -> clean-room public parser
    -> safety-invariant validation
    -> review-required public response
```

The website and API remain separate repositories and deployments. The browser
may call only the public API. No website user, public request, container, or
deployment identity may reach private ViaSign, Temple Console, review storage,
community data, lesson sources, or motion systems.

## Runtime boundary

Only three routes are public:

```text
GET  /healthz
GET  /v1/meta
POST /v1/parse
```

Runtime OpenAPI, Swagger UI, ReDoc, translation, motion, avatar, upload,
feedback, corpus, review-administration, and private-source routes are disabled.

Every accepted parse response uses schema `viasign.parser.response.v1` and
contract `1.0.0`. It must contain:

```text
status = review_required
review_required = true
motion_ready = false
```

If an invariant is absent or changes, the unsafe parser payload is not returned.
The API fails closed with a small public error that preserves the review and
motion-unavailable values.

## Component map

| Component | Responsibility | Must not contain |
| --- | --- | --- |
| `contracts/v1/` | Machine-readable request and response schemas | Private types, examples, or review data |
| `api_models.py` | Strict public request, health, metadata, and error models | Linguistic rules or motion fields |
| `contracts.py` | Typed response contract and versioned provenance | Transport, storage, or private identifiers |
| `parser.py` | Minimal clean-room public safety behavior and visible uncertainty | Private parser logic, lexicon, or benchmarks |
| `safety.py` | Final response-invariant enforcement | Recovery that makes unsafe output look valid |
| `middleware.py` | Body ceiling, request deadline, and transient rate limiting | Persistent identities, sentence logs, or analytics |
| `settings.py` | Validated local and deployment configuration | Secrets or wildcard production origins |
| `api.py` | Route composition, CORS, response headers, and server entry point | Private service calls or additional public routes |

The dependency direction stays one way:

```text
HTTP transport -> public models/contracts -> clean-room parser -> safety check
```

The parser does not import the website, deployment provider, private source,
motion engine, review system, or data store.

## Parse request flow

1. CORS permits only explicitly configured website origins.
2. The three-second application deadline begins before parsing and body
   validation, remaining below the website's five-second deadline.
3. The per-network limiter derives a randomly keyed in-memory digest. Missing or
   invalid trusted proxy identity fails closed on Render.
4. The body guard stops buffering above 4,096 bytes and returns a no-store
   `413` response.
5. The typed request model rejects extra fields, blank input, control characters,
   and text longer than 1,000 characters. Validation errors return a generic
   fail-closed body without submitted values.
6. The public parser returns visible uncertainty or an explicit unsupported
   result. Name-sign generation is blocked without analysis fallback.
7. The safety layer verifies the frozen schema and review/motion invariants.
8. The response receives `Cache-Control: no-store` and
   `X-Content-Type-Options: nosniff`. It includes input mode metadata but never
   the submitted sentence.

Timeout responses discard buffered output. The timeout is a response boundary,
not a hard process-kill guarantee; all parser code must therefore remain
side-effect-free and must never persist input.

## Data lifecycle

The service is stateless and has no database, persistent volume, queue, account,
session, feedback store, analytics SDK, tracing SDK, or model service.

Sentence text exists only in the request and short-lived process memory needed
to validate and answer it. It is not returned in success or error responses,
placed in the URL, intentionally logged, stored, used for training, benchmarked,
published, or treated as feedback.

Rate limiting stores only keyed digests, token counts, and monotonic timestamps.
Entries expire after inactivity and disappear on process restart. Provider
network metadata remains a separate documented hosting limitation.

## Deployment architecture

The candidate deployment is one stateless, non-root Docker web service in
Render's Singapore region:

- pinned Python Alpine base digest
- exact locked runtime dependencies
- UID/GID `10001:10001`
- port `10000`
- `/healthz` application and container health checks
- one instance only; in-memory limiters do not support horizontal scaling
- automatic deploys off
- maintenance mode on until explicit activation approval
- empty production CORS until explicit activation approval
- `api.viathorne.com` as the planned custom domain
- default `onrender.com` subdomain disabled after custom-domain activation
- no database, disk, private network dependency, or secret application value

Source publication, Blueprint sync, service creation, and public activation are
four separate decisions. Passing one does not authorize the next.

## Clean-room and provenance boundary

No private implementation candidate is approved for direct copying. The public
parser, transport, tests, schemas, fixtures, and documentation are independently
authored from the public contract and boundary requirements.

The exact prepublication artifact is selected by a deterministic path-and-hash
manifest. `.git`, virtual environments, caches, build output, and `*.local.md`
coordination notes are excluded. A future public repository must be created only
from manifest-listed paths and must never copy the local Git object store.

## Documentation roles

- `AGENTS.md` gives public contributor and agent safety instructions.
- `ARCHITECTURE.md` records the durable component, data, and trust boundaries.
- `ROADMAP.md` records completed gates and future sequencing.
- `docs/PUBLIC_SOURCE_MANIFEST.md` records migration eligibility and exclusions.
- `docs/RELEASE_CHECKLIST.md` separates technical evidence from owner approval.
- Deployment documents record provider-specific controls without authorizing
  hosting.

These three root coordination documents are part of the public safety contract
and should remain tracked. Private or machine-specific working notes must use a
separate `*.local.md` file, which is ignored and excluded from release evidence.

## Evolution rules

Any architectural change must:

1. preserve `review_required=true` and `motion_ready=false`
2. keep uncertainty visible and unsupported output free of analysis
3. remain independent of private code, examples, data, identities, and history
4. add no motion or avatar output to the parser boundary
5. update contracts, focused tests, public documentation, and release manifest
6. repeat provenance, secret, local-path, dependency, and container checks
7. obtain separate human review for linguistic, accessibility, privacy, license,
   trademark, publication, and deployment decisions where applicable

Passing automated checks demonstrates structural consistency. It does not prove
linguistic correctness or community approval.
