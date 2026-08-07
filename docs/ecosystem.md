# Ecosystem Architecture

Version 3 organizes the repository around a central routing helper and explicit worker contracts. Skills, agents, research, tools, artifacts, and Claude Marketplace packaging are validated as one connected product.

## Authority

The LLM entry guide is [`../helper/GUIDE.md`](../helper/GUIDE.md).

Machine-readable contracts:

- `helper/router.json`: intent and conditional routing
- `helper/capabilities.json`: capability owners and plugin-local defaults
- `helper/quality-gates.json`: local product/creative gates
- `helper/artifacts.json`: producer/consumer handoffs
- `helper/modules.json`: active public modules
- `research/capability-notes/gates.json`: adopted research-derived gates
- `architecture/plugin-graph.json`: shipping worker order and skill preloads
- `scripts/info_stories.py::load_catalog()`: merged Info-stories registry

## Complete shipping path

`new-post` owns the complete parent workflow:

1. `design-study`, when references exist
2. `evidence-checker`
3. `creative-director`
4. `story-architect`
5. `palette-curator`
6. `copy-compressor`
7. `layout-composer`
8. `caption-writer`
9. `artboard-builder`
10. `motion-director`
11. optional `mascot-animator`
12. `motion-engineer`
13. `render-qa`
14. `post-critic`
15. `story-verifier`

Workers return bounded artifacts to the parent workflow. A worker never assumes it can secretly coordinate peer workers.

## Creative runtime

`creative-director` receives evidence and optional reference diagnosis before story architecture. It produces at least three evidence-safe directions in `build/creative-concepts.json`. Each direction specifies a visual hook, copy hook, aha mechanic, story shape, recommended visual style/archetype/motion, evidence dependencies, risks, and why the concept earns attention.

The creative runtime does not equate spectacle with quality. A useful wow/aha moment is a reveal, relationship, comparison, transformation, state change, or interaction that improves comprehension or recall.

Plugin-local blocking defaults:

- `hooked-design-copy`
- `creative-payoff`
- `restrained-palette`
- `center-first-composition`

Palette character defaults to `creative-attractive-restrained`. Composition defaults to `center-first` unless tables, UI mockups, code/terminal surfaces, timelines, Arabic/RTL flow, or documented reference DNA make another alignment more legible or faithful.

## Evidence and exact assets

Evidence is resolved before creative production. Product states, metrics, proof, logos, integrations, and real UI behavior may not be invented to satisfy a visual slot.

A named or official mascot requires the exact user-supplied or task-attached SVG. Missing SVG means `HOLD: exact SVG required`. The mascot worker may animate addressable geometry and add removable support cues, but it may not silently redraw or substitute the identity.

## Info-stories

Info-stories resolves four independent axes:

- Story House
- Visual Style
- Story Archetype
- Motion Pattern

The registry is the deterministic result of `load_catalog()`, merging the base catalog and first-party extensions. UI Mockup Stories are a first-party extension and remain subject to evidence and feed-width legibility gates.

## Research and local rules

Research-derived gates have source provenance and local independently-worded behavior. Plugin-local behavior such as exact mascot identity, hook-led design copy, restrained palettes, center-first composition, and creative payoff is kept separate from upstream attribution.

See [`research.md`](research.md) for the provenance chain.

## Strict reality gate

`scripts/ecosystem_doctor.py` validates that every public skill, agent, and tool is declared, real, reachable, tested, and connected to the current registries. It also checks capability ownership, artifacts, gates, critical shipping workers, and helper/graph sequence consistency.

```bash
python3 scripts/ecosystem_doctor.py check
```

A module that exists only in documentation does not pass this gate.