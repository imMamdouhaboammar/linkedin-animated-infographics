# Codex Repository Guide

This supplements the root `AGENTS.md`. The repository-specific operating authority is `helper/GUIDE.md`.

## Required authority

Before changing routing, skills, agents, tools, research, or marketplace packaging, read:

- `helper/GUIDE.md`
- `helper/router.json`
- `helper/capabilities.json`
- `helper/quality-gates.json`
- `helper/artifacts.json`
- `helper/modules.json`
- `research/capability-notes/gates.json`
- `architecture/plugin-graph.json`

Use the merged Info-stories registry from `scripts/info_stories.py::load_catalog()` rather than treating `catalog.json` alone as the source of truth.

## Execution model

`new-post` is the parent workflow. Subtasks return bounded artifacts to it; no worker coordinates peer workers through hidden delegation.

The complete path includes `creative-director` after evidence gathering and before story architecture. The creative worker supplies evidence-safe concepts, copy/visual hooks, and a useful aha mechanic before downstream story/layout/motion decisions.

Plugin-local defaults:

- `hooked-design-copy`
- `creative-payoff`
- `creative-attractive-restrained`
- `center-first`
- exact SVG required for a named/official mascot

Research-derived gates remain active through `research/capability-notes/gates.json`.

## Strict validation

Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/validate_marketplace.py
```

`scripts/ecosystem_doctor.py` is the strict reality gate for module existence, reachability, ownership, artifacts, tests, and cross-registry drift.

## Repo skills

- Generic/coding-agent conventions: `.agents/skills/linkedin-animated-infographics/SKILL.md`
- Claude-facing companion: `.claude/skills/linkedin-animated-infographics/SKILL.md`

Keep user credentials and private MCP configuration outside the repository. Do not fabricate claims, UI behavior, proof, or mascot assets to satisfy a build.