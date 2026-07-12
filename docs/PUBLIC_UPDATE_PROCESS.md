# Private-to-Public Update Process

Private ViaSign development and the public parser are separate products with a
reviewed projection boundary.

## Never synchronize repositories directly

Do not merge, mirror, subtree-copy, or replay commits from the private
repository into the public repository. Do not preserve private Git history.

## Periodic public update flow

```text
private research or implementation insight
    -> describe the proposed public behavior without copying source
    -> independently author public fixtures
    -> provenance and rights review
    -> Deaf/SgSL review where the change makes linguistic claims
    -> implement the smallest clean-room public change
    -> contract, privacy, and regression tests
    -> release manifest with path hashes
    -> explicit public release approval
```

## What may cross the boundary

- a behavior proposal written without private code or private examples
- independently authored public fixtures
- explicitly cleared public sources with attribution
- privacy-safe review decisions
- schema and API changes that preserve fail-closed behavior

## What must not cross

- private source files or commit history
- lesson notes, teacher feedback, community submissions, or recordings
- private benchmark cases or reviewer identities
- motion, avatar, enterprise, hosted-service, or internal deployment code
- assumptions that a private result is ready merely because it passes tests

Every public update is a new reviewed implementation decision. The public
repository is not a delayed mirror of the private repository.

