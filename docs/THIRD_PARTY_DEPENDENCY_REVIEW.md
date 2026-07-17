# Third-party Dependency Review

- **Status:** Runtime dependency gate passed; container operating-system scan
  remains separate
- **Reviewed:** 2026-07-12
- **Scope:** Exact packages in `requirements.lock`
- **Audit tool:** `pip-audit 2.9.0`
- **License tool:** `pip-licenses 5.5.0`

This review covers Python packages only. It does not approve deployment,
publication, linguistic correctness, or the base image's operating-system
packages.

## Vulnerability result

The first audit found five advisories against `starlette==0.52.1`:

- `PYSEC-2026-161` / `CVE-2026-48710`
- `PYSEC-2026-249` / `CVE-2026-54283`
- `PYSEC-2026-248` / `CVE-2026-54282`
- `GHSA-wqp7-x3pw-xc5r` / `CVE-2026-48818`
- `GHSA-x746-7m8f-x49c` / `CVE-2026-48817`

The repository had imposed `starlette<1.0`; FastAPI 0.139.0 itself declares
`starlette>=0.46.0`. The public lock was therefore advanced to
`starlette==1.3.1`, which includes all five fixes. The complete test suite was
also exercised against 1.3.1 before changing the lock.

The response-header middleware now uses the raw ASGI `scope["path"]` instead
of `request.url.path`, so its no-store decision does not depend on a URL
reconstructed from the client-controlled Host header.

The post-upgrade command is:

```bash
pip-audit -r requirements.lock --progress-spinner off
```

Expected result for this recorded review:

```text
No known vulnerabilities found
```

Advisory references:

- https://github.com/advisories/GHSA-86qp-5c8j-p5mr
- https://github.com/advisories/GHSA-82w8-qh3p-5jfq
- https://github.com/advisories/GHSA-jp82-jpqv-5vv3
- https://github.com/advisories/GHSA-wqp7-x3pw-xc5r
- https://github.com/advisories/GHSA-x746-7m8f-x49c

This result is time-bounded. Repeat it against the exact lock immediately
before building any deployment artifact.

## License result

| Package | Version | SPDX license |
| --- | --- | --- |
| annotated-doc | 0.0.4 | MIT |
| annotated-types | 0.7.0 | MIT |
| anyio | 4.14.1 | MIT |
| click | 8.4.2 | BSD-3-Clause |
| fastapi | 0.139.0 | MIT |
| h11 | 0.16.0 | MIT |
| idna | 3.18 | BSD-3-Clause |
| pydantic | 2.13.4 | MIT |
| pydantic-core | 2.46.4 | MIT |
| starlette | 1.3.1 | BSD-3-Clause |
| typing-extensions | 4.16.0 | PSF-2.0 |
| typing-inspection | 0.4.2 | MIT |
| uvicorn | 0.51.0 | BSD-3-Clause |

These permissive runtime licenses are compatible with this repository's
Apache-2.0 distribution plan. No dependency code is vendored into the source
repository. Installed wheels retain their upstream license files in their
`.dist-info/licenses` directories inside the runtime environment.

The public `NOTICE` describes ViaSign's own copyright, trademark, language,
community-knowledge, and private-source boundaries. It must not imply that an
open-source software license grants rights over SgSL or community knowledge.

## Exact 0.2.1 refresh

On 2026-07-17, `requirements.lock` from exact public source commit
`d88bc2664628135a04ee4961866fea2380e1343d` was reviewed again before any
deployment update. `pip-audit 2.9.0` reported no known vulnerability. The
runtime package versions and licenses matched the table above, and both fresh
Linux arm64 and Linux amd64 images passed `pip check`. Their installed package
metadata retained the expected upstream license material.

This time-bounded refresh authorizes no Render update or public activation.

## Release rule

Before each release or container build:

1. Recreate a clean environment from `requirements.lock`.
2. Run `pip check` and `pip-audit`.
3. Regenerate the runtime license inventory and compare it with this table.
4. Confirm installed packages retain their upstream license files.
5. Stop the release on an unexplained license, missing notice, incompatible
   dependency, or unreviewed vulnerability.
