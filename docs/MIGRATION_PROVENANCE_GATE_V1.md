# Migration Provenance Gate V1

Status: candidate audit complete; no private code approved for direct copying

This review fingerprints the previously identified private candidates without
embedding their source, author identity, email addresses, private paths, lesson
content, or Git history in the public repository.

The machine-readable record is:

```text
provenance/v1/migration-candidates.json
```

## Decision summary

| Candidate | Direct-copy decision | Public direction |
| --- | --- | --- |
| Empty package marker | No copy needed | Already recreated cleanly |
| Parser V2 implementation | Blocked | Implement a smaller public parser from the public contract and cleared fixtures |
| Parser V2 types | Blocked as unnecessary | Use the independently authored public V1 contract |
| Curated lexicon | Blocked | Build a minimal lexicon only from independently authored or compatibly licensed public evidence |
| Runtime demo | Blocked | Write a contract-native CLI after a public parser exists |

## Evidence

- Each private candidate has a SHA-256 content fingerprint, Git blob identity,
  line and byte count, dependency summary, and redacted authorship count.
- Current candidate files contain no matched absolute local path or obvious
  credential-name pattern from the audit scan.
- All current lines trace to one Git author identity, but that is evidence of
  repository lineage, not a legal rights determination.
- The parser mixes general mechanics with sentence-specific reviewed branches
  and source-gloss rules.
- The lexicon history explicitly records a raw imported vocabulary bank before
  later curation. The current file therefore cannot be assumed clean merely
  because the raw block was later removed.
- The private type surface includes broader linguistic placeholders than the
  frozen public contract requires.
- The runtime demo embeds examples and depends on the private parser.

## Rights status

The record keeps rights confirmation as `pending_owner_attestation` for every
non-empty private candidate. Human confirmation must not be inferred from Git
authorship metadata.

Rights confirmation would not, by itself, reverse the direct-copy blocks. The
source-separation and review risks above still require clean-room public work.

## Stage 2 boundary

Stage 2 is now a minimal public parser implementation, not a file migration.
It may use only:

- the committed public request/response contracts
- independently authored public fixtures with recorded provenance
- generally known programming techniques
- explicitly cleared, attributable public linguistic sources added through a
  separate review
- Deaf/SgSL review decisions recorded without exposing private identities or
  material

It must not consult or translate private source code line-by-line while being
implemented.

