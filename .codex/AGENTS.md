# Codex Repository Guide

This supplements the root `AGENTS.md`. The repository-specific operating authority is `helper/GUIDE.md`.

Codex and Claude are first-class hosts for the same product core. Do not fork the canonical product workflows or create a Codex-only copy of `skills/` or `agents/`.

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
- `skills/` is the canonical Claude/repository product skill root
- `openai-skills/` is the self-contained public OpenAI skills distribution
- `scripts/validate_codex_plugin.py` is the OpenAI packaging/parity gate
- `.codex/config.toml` and `.codex/agents/*.toml` are repository-development configuration only; installed plugin behavior must not depend on them

Public OpenAI submission materials live under `submission/`. They prepare the package for review but do not mean a new version has been submitted or published.

## Canonical product execution

`new-post` remains the canonical repository production parent workflow. Subtasks return bounded artifacts to it; no worker coordinates peer workers through hidden delegation.

The complete path includes `evidence-checker` before `creative-director`. Evidence must be finalized before creative concepting. The creative worker then supplies evidence-safe concepts, copy/visual hooks, and a useful aha mechanic before downstream story/layout/motion decisions.

After final verification and delivery, `new-post` may offer community sharing. `share-demo` runs only after explicit user consent, validates the public package, and delegates GitHub contribution mechanics to `community-publisher`. Community publication stops at an open PR for maintainer manual review and merge.

Plugin-local defaults:

- `hooked-design-copy`
- `creative-payoff`
- `creative-attractive-restrained`
- `center-first`
- exact SVG required for a named/official mascot

Research-derived gates remain active through `research/capability-notes/gates.json`.

## Codex subagents

Current Codex releases can delegate when a user, `AGENTS.md`, or a Skill requests subagents.

Two categories are allowed under project-scoped `.codex/agents/`:

1. narrow repository-maintenance helpers
2. canonical product-worker adapters that consume, rather than replace, the product core

Maintenance helpers are:

- `explorer`: read-only execution-path evidence
- `reviewer`: read-only correctness/security/test review
- `docs_researcher`: read-only primary-documentation verification

Canonical product-worker adapters are allowed only when they obey all of these rules:

- they must read `helper/GUIDE.md` and `architecture/plugin-graph.json` before product work
- they must read the mapped `agents/*.md` contract completely before executing the assigned role
- the mapped canonical worker contract owns inputs, required skill preloads, gates, HOLD conditions, output artifacts, and handoff semantics
- the adapter executes only a bounded task from the parent and returns to the parent
- the adapter must not create a parallel product orchestration model
- the adapter cannot weaken evidence, visual, identity, verification, or publishing gates
- write-capable adapters may write only canonical or explicitly assigned task-workspace artifacts

Current product adapters map to the canonical repository workers:

- `creative_director` -> `agents/creative-director.md`
- `evidence_researcher` -> `agents/evidence-checker.md`
- `copy_director` -> `agents/copy-compressor.md`
- `layout_composer` -> `agents/layout-composer.md`
- `still_critic` -> `agents/post-critic.md`
- `motion_director` -> `agents/motion-director.md`
- `render_qa` -> `agents/render-qa.md`
- `final_verifier` -> `agents/story-verifier.md`
- `tool_runner` -> bounded execution for a canonical worker contract supplied by the parent

Codex may parallelize independent tasks only after their dependencies are satisfied. Evidence is a prerequisite for creative concepting. Sequential execution remains a valid fallback when delegation is unavailable or unnecessary.

## Public OpenAI runtime boundary

The installed skills-only package does not depend on these project-scoped Codex adapters.

`openai-skills/linkedin-infographic-autopilot/` negotiates the capabilities actually exposed in the current host. If real delegation is observed it may use real side jobs. If not, it runs the same bounded contracts sequentially. It never claims project-scoped Codex agents exist in an installed ChatGPT/Codex plugin session unless they are actually exposed there.

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
