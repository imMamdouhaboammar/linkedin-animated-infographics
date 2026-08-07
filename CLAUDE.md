# Claude Code Guide

This repository is a same-repository Claude Marketplace plugin. Treat its helper registries, agents, skills, research gates, and validators as one executable contract.

## First read

Read `helper/GUIDE.md` before selecting a skill or subagent.

The authoritative machine-readable files are:

- `helper/router.json`
- `helper/capabilities.json`
- `helper/quality-gates.json`
- `helper/artifacts.json`
- `helper/modules.json`
- `research/capability-notes/gates.json`
- `architecture/plugin-graph.json`
- merged Info-stories registry from `scripts/info_stories.py::load_catalog()`

Run:

```bash
python3 scripts/ecosystem_doctor.py check
```

after changing skills, agents, tools, routes, capabilities, artifacts, gates, or module inventory.

## Claude orchestration rule

Subagents do not orchestrate peer subagents. The main/parent workflow owns sequencing and HOLD resolution.

For complete post creation, use `new-post` and follow the graph:

`design-study -> evidence-checker -> creative-director -> story-architect -> palette-curator -> copy-compressor -> layout-composer -> caption-writer -> artboard-builder -> motion-director -> optional mascot-animator -> motion-engineer -> render-qa -> post-critic -> story-verifier`

Required skill knowledge is preloaded through each agent's `skills:` frontmatter.

## Creative behavior

- `creative-director` runs before story architecture and produces multiple evidence-safe concept directions
- hero/design copy must satisfy `hooked-design-copy`, not merely report the topic
- complete concepts should create a useful `creative-payoff` or documented reason to remain intentionally simple
- palette default is `creative-attractive-restrained`
- composition default is `center-first` with evidence/comprehension-driven exceptions only
- named/official mascot requests require the **exact SVG**; ask for it when missing and do not substitute a lookalike

## Research behavior

`research/capability-notes/gates.json` is active production guidance, not optional background reading. Apply the route's gate IDs and keep provenance in `research/capability-notes/sources.json`. Never package ignored upstream clones.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tools skills/svg-mascot-animator/scripts
python3 scripts/info_stories.py check
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/validate_marketplace.py
claude plugin validate .
```

The CI also registers this repository as marketplace `mamdouh-creative-tools` and installs `linkedin-animated-infographics@mamdouh-creative-tools` from a clean checkout.