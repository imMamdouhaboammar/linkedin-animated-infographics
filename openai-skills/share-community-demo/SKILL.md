---
name: share-community-demo
description: Prepare and publish a verified LinkedIn infographic demo to the community gallery through a contributor GitHub pull request. Use only after explicit user consent, rights confirmation, and final verification PASS.
---

# Share Community Demo

## Purpose

Prepare a verified demo for the community gallery and, when authenticated GitHub contribution tools are available, open a contributor pull request. Stop at the pull request. Never merge it automatically.

## Consent gate

Do nothing unless all are true:

- the user explicitly agreed to share the demo
- the final infographic verification verdict is `PASS`
- the user confirms they have the rights to publish the included material

Silence, ambiguity, or a previous decline means zero publication writes.

## Public package

The public demo package contains exactly:

- `demo.gif`
- `index.html`
- `demo.json`

The gallery catalog may also be regenerated as part of the contribution when the repository contract requires it.

Do not copy the whole working directory.

## Export safety

Before any GitHub write, inspect public text and metadata for:

- credential-like tokens or private keys
- local absolute filesystem paths
- signed or temporary private URLs
- private customer/source material
- remote executable scripts that have not been intentionally reviewed
- source prompts unless the user separately consents to publish them

A blocking finding returns `HOLD`. Do not push first and clean up later.

## Metadata

Require contributor identity appropriate for the public gallery, including the GitHub username used for the community namespace and rights confirmation.

Keep sample or concept data clearly identified when it could be mistaken for real proof.

## GitHub contribution flow

When authenticated GitHub contribution tooling is available:

1. create or reuse the user's contributor fork as appropriate
2. create a fresh branch for the demo
3. place the three-file package under the contributor namespace expected by the repository
4. regenerate the catalog only when required by the repository contract
5. commit only the scoped public contribution
6. push the contributor branch
7. open a pull request targeting upstream `main`
8. stop and report the PR URL and validation status

Never push directly to upstream `main` for a community submission.
Never merge the PR automatically.

If authenticated GitHub contribution tooling is unavailable, return `HOLD` with the exact missing capability instead of pretending publication happened.

## Output

Return:

- consent and rights status
- public package path/shape
- export-safety verdict
- contributor fork/branch when created
- real pull request URL when created
- status: awaiting maintainer review and merge

A completed local package is not the same as a published community contribution.
