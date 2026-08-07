# Codex Repository Guide

This supplements the root `AGENTS.md`. The repository-specific operating authority is `helper/GUIDE.md`.

Codex and Claude are first-class hosts for the same product core. Do not fork the workflows or create a Codex-only copy of `skills/`.

## Required authority

Before changing routing, skills, agents, tools, research, packaging, or distribution, read:

- `helper/GUIDE.md`
- `helper/router.json`
- `helper/capabilities.json`
- `helper/quality-gates.json`
- `helper/artifacts.json`
- `helper/modules.json`
- `research/capability-notes/gates.json`
- `architecture/plugin-graph.json`
- `compatibility/codex.json`

Use the merged Info-stories registry from `scripts/info_stories.py::load_catalog()` rather than treating `catalog.json` alone as the source of truth.

## OpenAI plugin surfaces

- `.codex-plugin/plugin.json` is the native OpenAI plugin manifest
- `.agents/plugins/marketplace.json` is the repository marketplace for Codex and ChatGPT
- `skills/` is the canonical bundled skill root for both OpenAI and Claude packaging
- `scripts/validate_codex_plugin.py` is the OpenAI packaging/parity gate
- `.codex/config.toml` and `.codex/agents/*.toml` are repository-development configuration only; installed plugin behavior must not depend on them

Public OpenAI submission materials live under `submission/`. They prepare the package for review but do not mean the plugin has been submitted or published.

## Execution model

`new-post` is the production parent workflow. Subtasks return bounded artifacts to it; no worker coordinates peer workers through hidden delegation.

The complete path includes `creative-director` after evidence gathering and before story architecture. The creative worker supplies evidence-safe concepts, copy/visual hooks, and a useful aha mechanic before downstream story/layout/motion decisions.

After final verification and delivery, `new-post` may offer community sharing. `share-demo` runs only after explicit user consent, validates the public package, and delegates GitHub contribution mechanics to `community-publisher`. Community publication stops at an open PR for maintainer manual review and merge.

Plugin-local defaults:

- `hooked-design-copy`
- `creative-payoff`
- `creative-attractive-restrained`
- `center-first`
- exact SVG required for a named/official mascot

Research-derived gates remain active through `research/capability-notes/gates.json`.

## Codex subagents

Current Codex releases can delegate when a user, `AGENTS.md`, or a Skill requests subagents. Use project-scoped `.codex/agents/` only for repository maintenance tasks such as exploration, review, and documentation verification.

The canonical product workers remain `agents/*.md` plus `architecture/plugin-graph.json`. Codex subagents may help execute bounded work, but they must return to the parent workflow and must not create a parallel product orchestration model. Sequential execution remains a valid fallback when delegation is unavailable or unnecessary.

Project maintenance agents are intentionally narrow:

- `explorer`: read-only execution-path evidence
- `reviewer`: read-only correctness/security/test review
- `docs_researcher`: read-only primary-documentation verification

## Strict validation

Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/demo_gallery.py check
python3 scripts/validate_marketplace.py
python3 scripts/validate_codex_plugin.py
```

`scripts/ecosystem_doctor.py` is the strict runtime reality gate. `scripts/validate_codex_plugin.py` checks native OpenAI packaging, marketplace structure, Codex project config, and cross-host parity.

## Repo skills

- Generic/coding-agent conventions: `.agents/skills/linkedin-animated-infographics/SKILL.md`
- Claude-facing companion: `.claude/skills/linkedin-animated-infographics/SKILL.md`

Keep user credentials and private MCP configuration outside the repository. Do not fabricate claims, UI behavior, proof, or mascot assets to satisfy a build. Do not publish a community demo without explicit user consent and export validation.
