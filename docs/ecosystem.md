# Ecosystem Architecture

Version 3 organizes the repository around a central routing helper and explicit worker contracts. Skills, agents, research, tools, artifacts, host packaging, and the demo gallery are validated as one connected product.

Claude Code, Codex, and ChatGPT are package adapters over the same canonical runtime. Host compatibility must not fork product Skills, routes, gates, or worker contracts.

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
- `schemas/demo.schema.json`: public demo metadata contract
- `scripts/demo_gallery.py`: owned/community demo validation and deterministic catalog
- `compatibility/codex.json`: OpenAI host-parity declaration

## Host packaging

Claude Code packaging lives under `.claude-plugin/`.

OpenAI packaging lives under `.codex-plugin/`, while the repository marketplace for Codex/ChatGPT lives at `.agents/plugins/marketplace.json`.

Both packages consume the same `skills/` tree. `.codex/config.toml` and `.codex/agents/*.toml` are repository-development helpers and are not dependencies of the installed OpenAI plugin.

Host packaging is validated separately from runtime topology:

```bash
python3 scripts/validate_marketplace.py
python3 scripts/validate_codex_plugin.py
```

## Complete shipping path

`new-post` owns the complete production parent workflow:

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
16. deliver
17. optional handoff to `share-demo` after PASS

Workers return bounded artifacts to their parent workflow. A worker never assumes it can secretly coordinate peer workers.

## Optional community publishing

Community publishing is deliberately outside the critical production sequence. A delivered artifact is complete before publication is considered.

After `story-verifier` returns `PASS`, `new-post` may offer one opt-in question. An explicit yes transfers control to the focused `share-demo` parent workflow. A decline or no answer causes no GitHub write.

`share-demo` prepares a strict public package containing exactly `demo.gif`, `index.html`, and `demo.json`. `scripts/demo_submit.py` enforces final-verification, rights, privacy, and export checks. `community-publisher` then handles only contributor fork, branch, commit, push, and pull-request mechanics.

The publisher never merges, enables auto-merge, or pushes to upstream `main`. Every community contribution waits for maintainer manual review and merge.

Gallery namespaces:

```text
demos/owned/<slug>/
demos/community/<github-user>/<slug>/
```

The root `demos/catalog.json` is generated deterministically from accepted manifests.

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

Research-derived gates have source provenance and local independently-worded behavior. Plugin-local behavior such as exact mascot identity, hook-led design copy, restrained palettes, center-first composition, creative payoff, and opt-in public demo export is kept separate from upstream attribution.

See [`research.md`](research.md) for the provenance chain, [`community-demos.md`](community-demos.md) for the public-export contract, and [`codex.md`](codex.md) for OpenAI packaging.

## Strict reality gate

`scripts/ecosystem_doctor.py` validates that every public skill, agent, and tool is declared, real, reachable, tested, and connected to the current registries. It also checks capability ownership, artifacts, gates, critical shipping workers, and helper/graph sequence consistency.

```bash
python3 scripts/ecosystem_doctor.py check
python3 scripts/demo_gallery.py check
python3 scripts/validate_marketplace.py
python3 scripts/validate_codex_plugin.py
```

A module, host package, or demo contract that exists only in documentation does not pass these gates.
