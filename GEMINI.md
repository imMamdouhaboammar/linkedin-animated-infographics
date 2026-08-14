# Google Antigravity & Gemini CLI Guide

This repository is an executable multi-host plugin ecosystem for evidence-safe LinkedIn infographics. Google Antigravity, Claude Code, Codex, and ChatGPT use package adapters around the same canonical product core.

## Antigravity Plugin & Agent Surfaces

- Manifest: `plugin.json` (Root) and `.agents/plugins/linkedin-animated-infographics/plugin.json`
- Discovered configurations: `.agents/plugins.json` and `.agents/skills.json`
- Lifecycle hooks: `.agents/hooks.json`
- Directory rules: `.agents/rules/linkedin-animated-infographics.md`
- 19 Specialized Subagents catalog: `.agents/agents/catalog.json`
- Parity & compatibility declaration: `compatibility/antigravity.json`
- Antigravity agent definition generator: `scripts/antigravity_agents.py`

## Canonical Architecture

`new-post` is the primary parent workflow. Subagents return bounded artifacts to the parent workflow and do not orchestrate peers directly.

The shipping order is:

`design-study -> evidence-checker -> asset-curator -> creative-director -> story-architect -> palette-curator -> type-curator -> copy-compressor -> layout-composer -> caption-writer -> artboard-builder -> motion-director -> optional mascot-animator -> motion-engineer -> render-qa -> post-critic -> story-verifier`

## Core Invariants

- **Viewport**: Strictly 1080x1350 vertical aspect ratio.
- **Identity (Lobe-First)**: User official assets win; named tools/AI resolve via Lobe. Missing assets HOLD.
- **Typography**: Intentional, render-safe, local/system only; remote `@import` during render capture is forbidden.
- **Palette**: `creative-attractive-restrained` default with verified contrast floors.
- **Layout**: `center-first` default; exceptions must be comprehension/evidence backed (tables, UI, code, RTL).
- **QA**: Static artboard PASS is required before motion engineering begins.

## Validation Commands

```bash
python3 scripts/validate_antigravity_plugin.py
python3 scripts/antigravity_agents.py check
python3 scripts/ecosystem_doctor.py check
python3 -m unittest discover -s tests -v
```
