# Codex and ChatGPT

Version 3.2.0 treats Codex and ChatGPT as first-class hosts for the same product core used by the Claude package.

There is one canonical skill tree. OpenAI packaging points directly at `skills/`; it does not maintain a copied Codex-specific version of the workflows.

## Native OpenAI package

The OpenAI plugin entry point is:

```text
.codex-plugin/plugin.json
```

It declares a skills-only plugin and points to:

```text
./skills/
```

The repository marketplace is:

```text
.agents/plugins/marketplace.json
```

The marketplace entry points back to the repository root, where the OpenAI manifest and canonical Skills live.

## Add the repository marketplace

With a Codex CLI release that supports plugins:

```bash
codex plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics --ref main
codex plugin marketplace list
```

Adding the marketplace makes the repository source available to supported OpenAI plugin surfaces. Installation and local testing are completed through a supported Plugins Directory surface rather than by inventing a separate repository-specific skill installation path.

## Same runtime contracts

Codex and ChatGPT consume the same product authority as Claude:

- `helper/GUIDE.md`
- `helper/router.json`
- `helper/capabilities.json`
- `helper/quality-gates.json`
- `helper/artifacts.json`
- `helper/modules.json`
- `research/capability-notes/gates.json`
- `architecture/plugin-graph.json`
- `scripts/info_stories.py::load_catalog()`

Cross-host parity is declared in `compatibility/codex.json` and validated by:

```bash
python3 scripts/validate_codex_plugin.py
```

The gate checks OpenAI packaging, the repo marketplace, shared identity/version, canonical paths, Codex repository configuration, submission materials, and public-review test cases.

## Codex subagents

`.codex/config.toml` and `.codex/agents/*.toml` are repository-development helpers. They are not a dependency of the installed plugin.

The project-scoped maintenance roles are:

- `explorer` for read-only execution-path inspection
- `reviewer` for read-only correctness, security, regression, and test review
- `docs_researcher` for read-only primary-documentation verification

Product workers remain canonical in `agents/*.md` and `architecture/plugin-graph.json`. Codex may delegate bounded work to subagents when useful, but the parent workflow still owns orchestration and artifacts. Sequential execution is a valid fallback.

## Community publishing

The Codex/ChatGPT package exposes the same `share-demo` contract as Claude.

A generated result is not published automatically. The share path starts only after final verification `PASS`, delivery, explicit user consent, and rights confirmation. The publisher prepares the three-file public package, validates it, opens a contributor pull request, and stops. Maintainer review and merge remain manual.

## Public Plugins Directory

Version 3.2.0 is **submission-ready** as a skills-only OpenAI plugin. The tracked handoff lives under `submission/` and includes listing metadata plus exactly five positive and three negative reviewer cases.

The repository status is `prepared-not-submitted`. Public availability still requires external steps in the OpenAI Platform, including publisher permissions/verification, submission, OpenAI review, and publication after approval.

See [`../submission/README.md`](../submission/README.md) for the tracked handoff.

## Validation

Run the OpenAI compatibility gate:

```bash
python3 scripts/validate_codex_plugin.py
```

For a complete repository release gate, also run the shared validators documented in [`development.md`](development.md).
