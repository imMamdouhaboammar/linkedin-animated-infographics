# Codex Native Plugin Compatibility Design

Date: 2026-08-08
Status: approved for implementation
Target release: 3.2.0

## Goal

Make `linkedin-animated-infographics` a first-class OpenAI plugin for Codex and ChatGPT without weakening or duplicating the existing Claude plugin ecosystem.

The same product must install and behave consistently across:

- Claude Code through `.claude-plugin/`
- Codex and ChatGPT through `.codex-plugin/`
- repo-scoped Codex/ChatGPT marketplace distribution through `.agents/plugins/marketplace.json`
- the OpenAI universal public Plugins Directory after external submission and review

The canonical product logic remains shared: `skills/`, `agents/`, `helper/`, `research/`, `architecture/`, scripts, tests, and the community demo publisher are not forked per host.

## Upstream contracts

This design follows the current OpenAI plugin contract documented at:

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/submission

Required OpenAI packaging facts used by this design:

- every OpenAI plugin has `.codex-plugin/plugin.json`
- bundled skills can be referenced with `"skills": "./skills/"`
- repo marketplaces live at `.agents/plugins/marketplace.json`
- marketplace entries use explicit source, installation policy, authentication policy, and category
- `codex plugin marketplace add owner/repo --ref main` is the supported CLI path for adding a repo marketplace source
- public plugins are submitted once and, after approval/publication, appear in the universal Plugins Directory shared by ChatGPT and Codex
- skills-only public submissions are supported
- public submission requires five positive and three negative reviewer test cases
- public listing requires website, support, privacy, and terms URLs plus a verified publisher identity

## Product architecture

### One core, two host packages

Claude and Codex packaging are adapters over one canonical product core.

```text
.claude-plugin/                 Claude package metadata
.codex-plugin/                  OpenAI/Codex package metadata
.agents/plugins/                Codex/ChatGPT repo marketplace
skills/                         canonical workflows for every host
agents/                         canonical worker contracts
helper/                         canonical router, capabilities, gates, artifacts, modules
research/                       canonical research-derived gates
architecture/                   canonical execution graph
scripts/                        canonical validators and runtime helpers
compatibility/                  host parity declaration
submission/                     public OpenAI review materials
```

No copied Codex-only version of each skill is allowed. Host-specific guidance may adapt invocation mechanics, but it must reference the same canonical skills and machine-readable authorities.

## OpenAI plugin manifest

Add `.codex-plugin/plugin.json` as the OpenAI package entry point.

The manifest must:

- use plugin name `linkedin-animated-infographics`
- use version `3.2.0`
- point `skills` to `./skills/`
- include publisher metadata matching the repository owner
- include repository and homepage URLs
- include install-surface metadata under `interface`
- use realistic starter prompts for create, Info-story, QA, and share-demo workflows
- use only real repository assets
- use public legal/support URLs that resolve to repository-hosted documents
- avoid declaring MCP servers or apps because this release is intentionally skills-only

The plugin is a skills-only OpenAI plugin in 3.2.0. MCP can be added in a future release only when a real external service dependency justifies it.

## Codex marketplace

Add `.agents/plugins/marketplace.json` as the repo-scoped marketplace source.

The marketplace must expose exactly the root plugin using a local source path that resolves to `./`, with:

- installation: `AVAILABLE`
- authentication: `ON_INSTALL`
- category: `Productivity`
- marketplace display name suitable for the Plugins Directory picker

The README and Codex docs must document:

```bash
codex plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics --ref main
codex plugin marketplace list
```

Installation itself is completed from a supported Plugins Directory surface. Documentation must not invent unsupported `codex plugin install` syntax unless current upstream documentation explicitly supports it.

## Codex runtime compatibility

### Repository guidance

The current `.codex/AGENTS.md` remains the Codex development guide and is expanded to cover:

- the canonical helper authority
- `share-demo` and community publishing
- OpenAI plugin packaging and marketplace validation
- the dual-host parity gate
- safe use of subagents

### Codex config

`.codex/config.toml` is repository-development configuration, not part of the installed plugin contract.

It must not reference missing custom agent files. Any declared `[agents.*] config_file` must resolve to a real `.codex/agents/*.toml` file in the repository and have a narrow maintenance role.

The installed plugin must remain useful without requiring the consumer to copy this repository-development config into their global Codex configuration.

### Worker execution

Canonical product worker definitions stay in `agents/*.md` and `architecture/plugin-graph.json`.

Codex may use subagents when available, but product correctness must not depend on hidden peer-to-peer delegation. Parent workflows remain responsible for orchestration and bounded artifacts. Sequential execution is a valid fallback.

## Compatibility registry

Add `compatibility/codex.json` as a machine-readable parity contract.

It records:

- schema version
- plugin release version
- canonical skills root
- canonical helper/router locations
- canonical worker graph
- supported OpenAI surfaces
- repo marketplace path
- OpenAI manifest path
- public submission type `skills-only`
- parity invariants between Claude and Codex

The parity invariants include:

- same plugin name and release version
- same canonical skills
- same request routes
- same quality and research gates
- same exact-SVG mascot rule
- same evidence/UI fidelity requirements
- same community demo publishing contract
- same manual-review-only contribution rule

## Validation

Add `scripts/validate_codex_plugin.py` and `tests/test_codex_plugin.py`.

The validator is fail-closed and checks at minimum:

1. `.codex-plugin/plugin.json` exists and is valid JSON
2. manifest identity/version matches `.claude-plugin/plugin.json`
3. manifest `skills` resolves to the canonical `skills/` root
4. required install-surface metadata exists
5. all manifest paths are repo-bound and resolve
6. the repo marketplace exists at `.agents/plugins/marketplace.json`
7. marketplace source resolves to the plugin root and contains required policy/category fields
8. `compatibility/codex.json` exists and matches live paths/version
9. `.codex/config.toml` contains no dead custom-agent references
10. declared `.codex/agents/*.toml` files exist and stay repo-bound
11. public submission materials contain exactly five positive and three negative cases
12. public legal/support documents exist
13. version parity remains true across Claude plugin, Claude marketplace, Codex plugin, compatibility registry, and submission metadata

The existing strict ecosystem doctor remains authoritative for runtime modules. The Codex validator must not duplicate its full module graph logic.

## Public submission package

Add tracked, reviewable submission preparation files under `submission/`.

Required files:

- `submission/openai-plugin.json`: listing metadata, submission type, starter prompts, release notes, external prerequisites
- `submission/test-cases.json`: five positive and three negative reviewer cases with expected behavior and result shape
- `submission/README.md`: exact manual steps for uploading the final skills bundle and completing the OpenAI Platform form

The repository prepares the public submission but does not claim the plugin is submitted or published automatically.

External prerequisites are explicitly marked as external:

- Apps Management write access in the publishing OpenAI organization
- verified individual or business developer identity
- final selection of country/region availability
- manual submission through the OpenAI Platform portal
- OpenAI review and publisher-triggered publication after approval

## Legal and support material

Add public repository documents:

- `PRIVACY.md`
- `TERMS.md`
- `SUPPORT.md`

They must describe this repository accurately as a local skills-based plugin. They must not claim that OpenAI or GitHub sends data to a maintainer-owned server when no such server exists.

The community demo publication flow is opt-in and may send the user-approved `demo.gif`, `index.html`, `demo.json`, and generated catalog change to GitHub through the contributor's authenticated tooling. Source prompts remain excluded unless separately consented to under the existing `share-demo` contract.

## README and docs

Update the root README so Claude Code and Codex/ChatGPT are presented as first-class installation targets without turning the README back into a long manual.

Add focused `docs/codex.md` covering:

- OpenAI plugin structure
- repo marketplace setup
- Plugins Directory installation/testing
- Codex development guidance
- validation commands
- public submission status

Update `docs/marketplace.md`, `docs/development.md`, `docs/ecosystem.md`, and repository guidance where needed.

## CI

Extend the existing validation workflow after the shared product validators with:

```bash
python3 scripts/validate_codex_plugin.py
```

CI must validate both host packages on every PR.

A true Codex marketplace smoke test should be added only if the current CI environment can install a Codex CLI version that exposes the documented plugin marketplace commands without interactive requirements. If that command cannot be run reliably in CI, the validator must still deterministically verify marketplace structure and the limitation must be documented rather than faking a passing smoke test.

Claude validation and same-repo Claude Marketplace smoke remain required.

## Release semantics

This is a feature release: `3.1.0 -> 3.2.0`.

Version must be updated consistently across all public host manifests and submission metadata.

## Acceptance criteria

The implementation is ready to merge only when:

- the OpenAI manifest and repo marketplace are present and strict-valid
- Codex config has no dead references
- all canonical Skills remain shared, not copied
- `compatibility/codex.json` passes parity validation
- five positive and three negative public-review cases exist
- privacy, terms, support, and website links in manifest/submission resolve to public repository URLs
- README documents Claude and Codex installation accurately
- all existing tests pass
- all new Codex tests pass
- strict ecosystem validators remain green
- demo gallery/community publisher validators remain green
- Claude official validator remains green
- review findings are resolved before merge

## Non-goals

- no new MCP server in 3.2.0
- no automatic OpenAI public submission
- no duplicated Codex-only skill tree
- no direct write or auto-merge changes to the community publisher
- no requirement that plugin users adopt the repository maintainer's MCP configuration
