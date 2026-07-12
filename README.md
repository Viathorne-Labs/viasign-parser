# ViaSign Parser

ViaSign Parser is a clean public boundary for an early, review-required surface
analyzer intended to support future SgSL-aware planning research.

It is not a finished SgSL translator, an interpreter, a linguistic authority,
or a motion/avatar system. It must not be used for certified, emergency, legal,
or medical communication.

## Current state

No private parser implementation or benchmark data has been migrated.

The provenance gate found mixed private/review lineage in the previous parser
and lexicon, so direct copying remains blocked. This parser is an independent,
smaller implementation built from public contracts and synthetic fixtures.

The versioned request and response contracts now exist with independently
authored structural fixtures. They validate contract behavior only and are not
linguistic benchmarks.

The first clean-room public parser intentionally exposes its limitations:

```text
review_required = true
motion_ready = false
parser_available = true
surface_analysis_available = true
grammar_rules_available = false
```

`POST /v1/parse` returns an `uncertain` response with closed natural-English
surface categories and no proposed signing for ordinary input. It can label
sentence kind, question kind, a generic question category, and a negation cue.
These observations are not SgSL grammar. Name-sign generation requests return
`unsupported` with no analysis. Responses never echo the submitted sentence,
tokens, names, or fragments. No SgSL grammar rules have been added yet.

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest
viasign-api
```

The local server binds to `127.0.0.1:8000`.

Runtime settings are read from `VIASIGN_HOST`, `VIASIGN_PORT`, and the comma-
separated `VIASIGN_CORS_ORIGINS`. The defaults are local-only and allow the
Astro development origins at `localhost:4321` and `127.0.0.1:4321`. Copy
`.env.example` as a reference, but note that the application does not load env
files itself. Production origins must be explicit; wildcard and path-bearing
origins are rejected.

`VIASIGN_ACCESS_LOG` defaults to `false` so Uvicorn does not duplicate client
and request metadata in application logs. The public parse body is limited to
4 KiB before JSON validation; the text field remains limited to 1,000
characters. Parse requests also have a three-second application deadline and
return a fail-closed `503` without releasing buffered output if that deadline is
exceeded.

`POST /v1/parse` also has a transient per-network token bucket: 60 requests per
minute with a burst of 20. It stores only keyed in-memory digests and returns a
plain-language, no-store `429` with `Retry-After`. Render proxy identity is
trusted only when `VIASIGN_TRUST_RENDER_PROXY=true`; local defaults keep it
false. See the [anonymous pilot rate-limit policy](docs/RATE_LIMIT_POLICY.md).

### Local container check

```bash
docker build -t viasign-parser:local .
docker run --rm -p 8000:10000 \
  -e VIASIGN_CORS_ORIGINS=http://127.0.0.1:4321 \
  viasign-parser:local
```

The Render Blueprint remains inert by default: automatic deploys are disabled,
maintenance mode is enabled, and CORS is empty. See the
[Render hosting decision](docs/RENDER_HOSTING_DECISION.md) before changing
those values.

## Repository boundaries

- [Architecture](ARCHITECTURE.md)
- [Repository guidance](AGENTS.md)
- [Public source manifest](docs/PUBLIC_SOURCE_MANIFEST.md)
- [API boundary](docs/API_BOUNDARY.md)
- [Parser response contract V1](docs/PARSER_RESPONSE_CONTRACT_V1.md)
- [Migration provenance gate V1](docs/MIGRATION_PROVENANCE_GATE_V1.md)
- [Viathorne web integration boundary](docs/WEB_INTEGRATION_BOUNDARY.md)
- [Production deployment gate](docs/PRODUCTION_DEPLOYMENT_GATE.md)
- [Render hosting decision](docs/RENDER_HOSTING_DECISION.md)
- [Origin and Content Security Policy](docs/ORIGIN_AND_CSP_POLICY.md)
- [Edge and operations policy](docs/EDGE_AND_OPERATIONS_POLICY.md)
- [Release candidate audit V1](docs/RELEASE_CANDIDATE_AUDIT_V1.md)
- [Release candidate audit V2](docs/RELEASE_CANDIDATE_AUDIT_V2.md)
- [Repository owner review packet V1](docs/OWNER_REVIEW_PACKET_V1.md)
- [Repository owner review packet V2](docs/OWNER_REVIEW_PACKET_V2.md)
- [Third-party dependency review](docs/THIRD_PARTY_DEPENDENCY_REVIEW.md)
- [Container security review](docs/CONTAINER_SECURITY_REVIEW.md)
- [Anonymous pilot rate-limit policy](docs/RATE_LIMIT_POLICY.md)
- [Private-to-public update process](docs/PUBLIC_UPDATE_PROCESS.md)
- [Data and consent](docs/DATA_AND_CONSENT.md)
- [Release checklist](docs/RELEASE_CHECKLIST.md)
- [Roadmap](ROADMAP.md)

## License

Code and original documentation in a published release of this repository are
provided under the Apache License 2.0. That software license does not grant
rights in Singapore Sign Language itself, private lesson material, community
knowledge, personal data, recordings, or ViaSign and Viathorne trademarks.
