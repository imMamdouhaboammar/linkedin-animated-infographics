---
name: linkedin-animated-infographics-conventions
description: Repository conventions for the Python, Markdown, HTML/CSS/SVG, shell, agent, research-gate, and Claude Marketplace ecosystem.
---

# LinkedIn Animated Infographics Repository Conventions

Use this skill when modifying this repository. Start with `helper/GUIDE.md`; do not create a parallel routing or capability model.

## Machine-readable authority

- `helper/router.json`: routes
- `helper/capabilities.json`: owners and plugin-local defaults
- `helper/quality-gates.json`: local creative/product gates
- `helper/artifacts.json`: handoff artifacts
- `helper/modules.json`: active skills, agents, and public tools
- `research/capability-notes/gates.json`: adopted research-derived runtime gates
- `architecture/plugin-graph.json`: shipping sequence and required skill preloads
- the merged registry returned by `scripts/info_stories.py::load_catalog()`: complete Info-stories authority

Detailed visual-source and type behavior lives in `skills/info-stories/references/asset-source-policy.md` and `skills/info-stories/references/typography-direction.md`.

The merged registry returned by `scripts/info_stories.py::load_catalog()` combines `skills/info-stories/catalog.json` with `skills/info-stories/extensions/*.json`. `catalog.json` alone is not the complete authority.

## Actual stack

- Python 3 for validators, registries, render tooling, and public CLIs
- Markdown for skills, agents, docs, research, and plans
- HTML / CSS / SVG for fixed 1080x1350 artboards and deterministic motion
- shell for setup/lint/render wrappers
- JSON for plugin, routing, capability, gate, artifact, module, and Info-stories contracts
- unittest for regression and architecture tests

There is no TypeScript application layer in the current repository.

## Production architecture

`new-post` is the parent workflow. Workers return artifacts to the parent workflow; they do not coordinate peer agents directly.

Shipping order:

`design-study -> evidence-checker -> asset-curator -> creative-director -> story-architect -> palette-curator -> type-curator -> copy-compressor -> layout-composer -> caption-writer -> artboard-builder -> motion-director -> optional mascot-animator -> motion-engineer -> render-qa -> post-critic -> story-verifier`

`asset-curator` applies Lobe-first verified identity sourcing after exact user assets. `creative-director` applies `hooked-design-copy`, `creative-payoff`, and `clean-creative-structure`. `type-curator` applies intentional typography before copy fitting. Palette remains `creative-attractive-restrained` and composition remains `center-first` unless a documented exception improves comprehension.

A named verified identity must come from the approved asset plan. Supported AI/tool identities may resolve from Lobe; unresolved identities HOLD. Downstream workers do not invent substitutes.

## Research

Research is activated through `research/capability-notes/gates.json`. Keep upstream source URL, inspected SHA, license, local Adopt/Adapt/Reject notes, owners, and implementation references. Ignored `research/upstreams/` working copies never ship.

## Development method

Write a failing test first for behavior changes, implement the minimum coherent fix, then run focused and full validation.

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tools skills/svg-mascot-animator/scripts
python3 scripts/info_stories.py check
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/validate_marketplace.py
```

Use `scripts/ecosystem_doctor.py` as the strict reality gate. A declared module must exist, be reachable, have tests, and remain linked to the live architecture.

Never fabricate factual content, product/UI proof, official identity assets, or typography provenance to satisfy a template. Never commit credentials or private MCP configuration.
