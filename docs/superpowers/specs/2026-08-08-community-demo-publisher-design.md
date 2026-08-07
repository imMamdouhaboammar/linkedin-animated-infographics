# Community Demo Publisher Design

Date: 2026-08-08
Status: approved architecture, implementation pending

## Goal

Add a first-class demo gallery and contribution workflow to the plugin. The repository should showcase examples created by the maintainer and by the community, and the LLM should offer users an optional path to publish a finished result after successful QA and verification.

The publishing path must never write to `main` or merge a contribution automatically. Community submissions end as a pull request that requires manual review and merge.

## Product behavior

After a complete infographic has passed render QA, adversarial review, and final verification, the parent workflow may offer one optional follow-up:

> Share this demo with the community?

The offer is opt-in. Declining it ends the workflow with no GitHub write. Accepting it activates the `share-demo` workflow and `community-publisher` agent.

The publisher packages exactly three public files for each submission:

- `demo.gif`
- `index.html`
- `demo.json`

No source prompt, private evidence, attachments, secrets, tokens, internal build reports, or user files are published unless explicitly allowed by the contribution contract.

## Repository layout

```text
demos/
├── README.md
├── catalog.json
├── owned/
│   └── <slug>/
│       ├── demo.gif
│       ├── index.html
│       └── demo.json
└── community/
    └── <github-user>/
        └── <slug>/
            ├── demo.gif
            ├── index.html
            └── demo.json

schemas/
└── demo.schema.json

skills/
└── share-demo/
    └── SKILL.md

agents/
└── community-publisher.md

scripts/
├── demo_gallery.py
└── demo_submit.py
```

`demos/catalog.json` is generated deterministically from `demo.json` files and must not be hand-edited.

## Demo contract

Every `demo.json` must validate against `schemas/demo.schema.json`.

Required fields:

- `schema_version`
- `id`
- `title`
- `author`
- `author_url`
- `description`
- `created_with`
- `language`
- `story_type`
- `tags`
- `gif`
- `html`
- `created_at`
- `license`
- `rights_confirmed`

Optional fields:

- `source_prompt`
- `repo_url`
- `notes`

Rules:

- `source_prompt` is absent by default and requires explicit user consent
- `rights_confirmed` must be true before packaging
- `gif` must resolve to `demo.gif` inside the same demo directory
- `html` must resolve to `index.html` inside the same demo directory
- paths must be repository-relative and may not escape the demo directory
- IDs and slugs must be stable, lowercase, filesystem-safe, and unique
- community demos are namespaced by GitHub username
- owned demos live only under `demos/owned/`

## Gallery engine

`scripts/demo_gallery.py` owns deterministic discovery, validation, and catalog generation.

Commands:

```bash
python3 scripts/demo_gallery.py check
python3 scripts/demo_gallery.py build
python3 scripts/demo_gallery.py list
```

`check` validates every demo package, schema, path boundary, unique ID, author namespace, GIF/HTML presence, catalog drift, and prohibited files.

`build` regenerates `demos/catalog.json` in deterministic order without mutating individual submissions.

`list` prints a machine-readable summary usable by LLMs, docs, and future gallery UIs.

The strict ecosystem doctor must treat the gallery scripts, skill, agent, schema, and public demo directories as real declared modules and reject disconnected or untested pieces.

## Publisher engine

`scripts/demo_submit.py` is the deterministic packaging and preflight layer. It does not merge anything.

Commands:

```bash
python3 scripts/demo_submit.py prepare --build-dir build --author <github-user> --slug <slug>
python3 scripts/demo_submit.py check <demo-dir>
```

`prepare` copies only the approved final HTML and GIF into a staging contribution directory and creates `demo.json` from explicit metadata. It must fail if the final verification verdict is not PASS, the GIF/HTML are missing, rights confirmation is absent, or the destination would overwrite an existing demo.

`check` validates the staged package before any GitHub operation.

## LLM routing

The helper gains a new focused intent: `share-demo`.

The canonical complete-post route remains unchanged through final verification. Publishing is a post-delivery optional branch, not part of the shipping critical path.

Flow:

```text
story-verifier PASS
  -> deliver final work
  -> ask user whether to share
      -> no: stop
      -> yes: collect publication metadata + rights confirmation
          -> demo_submit.py prepare
          -> demo_submit.py check
          -> demo_gallery.py check against staged contribution
          -> community-publisher
          -> fork/branch/commit/push/PR
          -> stop and return PR URL
```

The offer must not appear before final verification PASS.

## `share-demo` skill

The skill is a focused parent workflow responsible for:

- explicit opt-in confirmation
- GitHub username resolution
- title, description, language, story type, and tags
- rights confirmation
- optional source-prompt consent
- selecting the final verified GIF and HTML
- invoking deterministic packaging and validation
- delegating GitHub contribution work to `community-publisher`
- returning the pull request URL and contribution summary

It must return HOLD when GitHub identity, required files, rights confirmation, or writable GitHub authentication are unavailable.

## `community-publisher` agent

The publisher is a narrow GitHub contribution worker. It receives only a validated contribution directory and metadata.

It must:

1. verify the contribution preflight again
2. detect the authenticated GitHub user
3. ensure the target repository is `imMamdouhaboammar/linkedin-animated-infographics`
4. create or reuse the contributor's fork when needed
5. create a fresh contribution branch such as `community/<user>/<slug>`
6. add only the three demo files plus the regenerated `demos/catalog.json` when required by the contribution contract
7. commit with a scoped message
8. push to the contributor fork
9. open a pull request against upstream `main`
10. stop

It must never merge the PR, enable auto-merge, push directly to upstream `main`, rewrite unrelated history, or force-push an existing unrelated branch.

Preferred GitHub execution uses the authenticated GitHub CLI or equivalent native GitHub integration available to the host agent. If fork creation or push access is unavailable, the workflow returns a HOLD with a locally prepared contribution package and exact manual commands instead of pretending publication succeeded.

## Pull request contract

Community PR title:

```text
demo: add <title> by @<github-user>
```

PR body must include:

- demo title
- author attribution
- GIF preview path
- story type and tags
- plugin version used
- rights confirmation
- validation results
- statement that merge requires maintainer review

No automatic merge is permitted even when every check passes.

## Validation and CI

Add dedicated tests and CI gates for:

- JSON schema validation
- required three-file package
- safe paths and no parent traversal
- no duplicate IDs or slugs
- author namespace consistency
- generated catalog determinism and drift
- forbidden publication files
- opt-in requirement
- verified-final-artifact requirement
- rights confirmation requirement
- no auto-merge behavior
- no direct upstream-main publishing path
- module manifest reachability
- docs/README links

The existing full Claude Plugin Validation workflow should run:

```bash
python3 scripts/demo_gallery.py check
```

and the unit tests for `demo_submit.py`, routing, contracts, and publisher behavior.

## Security and privacy gates

The publishing workflow is a data-export boundary and must fail closed.

Before packaging, reject or require explicit removal of:

- API keys, tokens, credentials, cookies, or secrets
- local absolute paths
- private URLs or signed URLs
- hidden evidence files or build reports
- prompts or source documents without explicit consent
- externally hosted assets that the contributor cannot redistribute
- identifiable private data not needed for the demo

`index.html` must be self-contained or use redistribution-safe public dependencies allowed by repository policy. The validator should flag suspicious remote script/resource references for maintainer review.

The agent must never infer rights ownership. `rights_confirmed` is an explicit user assertion.

## Owned demos

Maintainer-created demos use the same schema and validation contract under `demos/owned/<slug>/`.

The existing `assets/demo_artboard_v4.gif` should remain available for README compatibility during migration. A first owned demo may reference or copy that artifact into the new demo package only when the matching HTML is available and the package passes the same validator as community submissions.

No special validation bypass exists for owned demos.

## README and docs

The main README should gain a compact `Demos` section that shows maintainer examples and points to the community gallery.

`demos/README.md` explains:

- Created by Mamdouh
- Created by the community
- how to browse a demo
- how to contribute manually
- how the plugin can offer to publish after creation
- manual review/merge policy

Add focused documentation for the contribution contract and publisher safety model rather than expanding the root README into a long manual.

## Versioning

This feature adds a new public skill, agent, helper route, schema, scripts, and user-visible workflow. It should ship as a minor plugin release rather than a documentation-only patch. The implementation plan should determine the next semantic version from the current repository version at execution time.

## Non-goals

This iteration does not build a hosted web gallery, ranking system, likes, comments, remote database, automatic moderation service, or automatic PR merge.

The repository itself is the gallery source of truth.

## Acceptance criteria

The feature is complete when:

- owned and community demo namespaces exist
- every demo package is exactly GIF + HTML + `demo.json`
- `demo.json` has a strict schema and safe-path validator
- gallery catalog generation is deterministic
- helper routing exposes `share-demo`
- `share-demo` is optional and appears only after final verification PASS
- `community-publisher` can prepare a fork/branch/PR workflow when GitHub auth permits
- lack of GitHub write capability produces a clear HOLD instead of a false success
- publication requires explicit rights confirmation
- source prompt publication is opt-in only
- all new modules are declared, reachable, documented, and tested
- CI blocks malformed or unsafe community PRs
- every contribution requires manual review and merge
