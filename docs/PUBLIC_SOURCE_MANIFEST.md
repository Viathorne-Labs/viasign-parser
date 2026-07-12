# Public Source Manifest

Status: no private source migrated

This manifest is an allowlist, not an instruction to copy. Every candidate
still requires authorship, provenance, privacy, license, and human review.

## Eligible private implementation candidates

| Candidate | Intended public form | Current status |
| --- | --- | --- |
| Parser package marker | `src/viasign_parser/__init__.py` | Recreated cleanly; no copy needed |
| Parser V2 implementation | `src/viasign_parser/parser.py` | Direct copy blocked; clean-room implementation required |
| Parser V2 typed output | `src/viasign_parser/types.py` | Direct copy blocked; superseded by public V1 contract |
| Lexicon normalization | `src/viasign_parser/lexicon.py` | Direct copy blocked; rebuild only from cleared public sources |
| Parser runtime demo logic | `src/viasign_parser/cli.py` | Direct copy blocked; rewrite after public parser exists |

No other private implementation path is approved.

The decisions and redacted content fingerprints are recorded in
`docs/MIGRATION_PROVENANCE_GATE_V1.md` and
`provenance/v1/migration-candidates.json`.

## Files that must be newly authored

- packaging and dependency metadata
- container, Render Blueprint, and deployment-boundary metadata
- FastAPI transport code
- API request and response models
- tests and fixtures
- README, contribution, conduct, security, consent, and release documentation
- tracked public `AGENTS.md`, `ARCHITECTURE.md`, and `ROADMAP.md` coordination
  documents
- third-party notices

The clean-room request/response contract, generated JSON Schemas, and synthetic
contract fixtures were newly authored in this repository. They contain no
migrated parser implementation or private benchmark data.

The minimal `src/viasign_parser/parser.py` implementation was also authored in
this repository from the public contract and synthetic fixtures. It implements
visible uncertainty and an explicit policy block for name-sign generation. It
contains no SgSL grammar or private lexicon logic.

`src/viasign_parser/surface.py` was independently authored for contract `1.1.0`.
It reports only closed natural-English sentence, question, question-category,
and negation-cue values. It does not return tokens, names, fragments, SgSL
order, glosses, identity fields, motion, or avatar data. No private constants,
vocabulary, examples, benchmark expectations, or type structures were copied.

`Dockerfile`, `.dockerignore`, `render.yaml`, `requirements.lock`, and the
Render hosting decision were newly authored for this public repository. They
copy only the public runtime package and do not contain private source paths,
credentials, datasets, or service connections.

`docs/THIRD_PARTY_DEPENDENCY_REVIEW.md` was newly authored from public package
metadata and public security advisories. It contains no private source or
linguistic material.

`docs/CONTAINER_SECURITY_REVIEW.md` was newly authored from local build and
public vulnerability-scanner results. It contains no private source,
credentials, user submissions, or linguistic material.

`docs/RATE_LIMIT_POLICY.md` and the public rate-limit middleware were newly
authored from the public API boundary and provider documentation. They contain
no private source, stored network identities, user submissions, or linguistic
material.

`docs/ORIGIN_AND_CSP_POLICY.md` was newly authored from the public API and
website contracts. It records only public hostnames, configuration boundaries,
and rollback requirements; it contains no private source or linguistic
material.

`docs/EDGE_AND_OPERATIONS_POLICY.md` and the parse-timeout middleware were newly
authored from the public API contract and public provider documentation. They
contain no private source, user submission, reviewer identity, or linguistic
material.

`scripts/release_manifest.py`, `scripts/audit_release_candidate.py`, and
`docs/RELEASE_CANDIDATE_AUDIT_V1.md` were newly authored for this public
boundary. They enumerate and hash only public candidate files and scan for
release-boundary leaks; they contain no private source or user submission.

`AGENTS.md`, `ARCHITECTURE.md`, and `ROADMAP.md` are public safety and sequencing
documents. Private or machine-specific notes must use ignored `*.local.md`
files and are excluded from the release candidate.

`docs/OWNER_REVIEW_PACKET_V1.md` was newly authored from this public candidate's
license, claims, privacy, and release boundaries. It contains no private source,
signature, personal contact information, or owner identity document.

The public response contract and validation handler were refined before first
publication so neither success nor error responses echo submitted sentence
text. Only non-sensitive input mode metadata and closed surface categories
remain in the response.

## Excluded from the first public release

- all private Git history
- all existing benchmark banks and community-review batches
- lesson notes, converted sources, source audits, PDFs, screenshots, and tables
- teacher notes, reviewer identities, private feedback, and community media
- legacy parser, sign-plan, prompt, pulse, response bridge, and showcase code
- motion engines, motion contracts, avatar code, assets, mappings, and editors
- Temple Console and symbolic internal documentation
- generated previews, virtual environments, caches, and local machine artifacts
- existing internal/public-safe documentation copied verbatim without a separate
  provenance review

## Promotion rule

An item may move from `Not migrated` only when its review record contains:

- exact source identity and hash
- authorship and license-right confirmation
- private-source and personal-data scan results
- example/fixture provenance
- dependency review
- human approval
