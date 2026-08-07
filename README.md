# linkedin-animated-infographics

A Claude Code plugin for designing, rendering, and animating deterministic 1080x1350 GIF infographics, Info-stories, UI mockup stories, and exact-SVG mascots for LinkedIn (Arabic & RTL supported).

## Install from the Claude Marketplace

Add the marketplace hosted by this repository, then install the plugin:

```text
/plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics
/plugin install linkedin-animated-infographics@mamdouh-creative-tools
```

The marketplace catalog is `.claude-plugin/marketplace.json`. It exposes the plugin at the repository root with strict manifest mode.

For local development, Claude Code can validate the same repository with:

```bash
claude plugin validate .
```

Then, once per machine for browser rendering:

```bash
bash scripts/setup.sh
```

That installs Playwright and a Chrome binary and checks for `ffmpeg`. Registry, graph, and marketplace validation run on plain Python 3.

## Features & Skills

| Skill | Covers |
|---|---|
| `post` | The main router. Pipeline, non-negotiables, working method |
| `caption` | Caption archetypes, truncation cut, hook and CTA libraries, ban list |
| `info-stories` | Story Houses, Visual Styles, Story Archetypes, Motion Patterns, study, and verification |
| `artboard` | Execution archetypes, type scale, offline fonts, and still construction |
| `motion` | Seekable primitives, one-loop-clock rule, reverse-delay trap |
| `mascots` | Exact mascot identity, roles, motion budget, and infographic fit |
| `render` | Frame capture, GIF assembly with size budgeting, QA gates, publishing |
| `arabic` | RTL mirroring, Arabic type scale, bidi isolation, caption rhythm |
| `svg-mascot-animator` | Exact-SVG inspection, rigging, physics, creative directions, and deterministic animation |

## Info-stories

Info-stories separates a visual direction into four choices:

1. **Story House**: semantic colour palette and contrast roles
2. **Visual Style**: structural grammar such as Signal Sheet, Command Canvas, UI Storyboard, or Interface Cutaway
3. **Story Archetype**: narrative job such as Framework in One Page, Screen to Outcome, or State Change Story
4. **Motion Pattern**: zero to two meaning-driven motions

Each Visual Style also carries three 1-10 design dials: design variance, motion intensity, and visual density. Reference images or GIFs can be diagnosed first by `design-study`; the diagnosis maps design DNA into ranked local choices rather than copying the source.

The stable base lives in `skills/info-stories/catalog.json`. First-party story families can extend it through `skills/info-stories/extensions/*.json`. `scripts/info_stories.py::load_catalog()` merges the registry deterministically and is the machine-readable source used by agents and tools.

### UI Mockup Stories

UI Mockup Stories make interface states part of the infographic narrative rather than decorative screenshots.

- **UI Storyboard**: two to four screens or interface states in a clear sequence
- **Interface Cutaway**: one dominant interface with annotated internal zones
- **Screen to Outcome**: starting screen, interaction, visible result
- **Inside the Interface**: hero interface, internal zones, why they matter
- **State Change Story**: before state, trigger, after state
- **Cursor Focus**: restrained secondary cue for one control or region
- **State Transition**: one primary interface state change

The UI rules preserve feed-width legibility, distinguish documented product UI from concept UI, label fictional data when it could be mistaken for real evidence, and block unsupported features, metrics, integrations, or customer proof.

### Mascot Animator 2

When the user names a specific official mascot, the plugin requires the exact user-supplied or task-attached SVG before mascot animation starts. It never redraws, approximates, substitutes, or generates a lookalike automatically.

The mascot path is:

`exact SVG -> identity contract -> SVG inspection -> rig plan -> creative direction -> mascot-animator -> motion integration -> render QA -> adversarial review -> independent verification`

Creative starting directions include Guide the Eye, Curious Peek, Inspect and React, Carry and Place, Reveal Assistant, Status Confirmation, Route Follow, Card-to-Card Handoff, Calm Idle Breathing, and Contextual Micro-Reaction. Each direction must state its communication job, movable SVG parts, reset behavior, and motion budget.

Inspect the available directions or validate a request:

```bash
python3 scripts/mascot_contract.py directions
python3 scripts/mascot_contract.py check build/mascot-request.json
```

## Validation and tools

Inspect and validate the registry, executable graph, and marketplace:

```bash
python3 scripts/info_stories.py check
python3 scripts/plugin_graph.py check
python3 scripts/validate_marketplace.py
python3 scripts/info_stories.py list house
python3 scripts/info_stories.py list style
```

External capability research lives under `research/capability-notes/`; cloned upstream working copies are ignored and are not shipped with the plugin.

### Info-stories tools

```bash
python3 tools/palette_preview.py --out assets/info-stories-palettes.html
python3 tools/story_scaffold.py --topic "..." --takeaway "..." --cta "..." \
  --house ember-paper --style signal-sheet --archetype framework-in-one-page \
  --motion sequential-highlight --out build/story-brief.json
python3 tools/composition_check.py --style signal-sheet \
  --archetype framework-in-one-page --motion sequential-highlight
python3 tools/copy_slop_check.py "copy to inspect"
python3 tools/contrast_check.py --house ember-paper --fg accent_deep --bg bg --minimum 4.5
python3 tools/fingerprint_check.py --current build/fingerprint.json \
  --previous build/previous-fingerprint.json --min-changes 2
```

Tracked palette chooser: `assets/info-stories-palettes.html`. Acceptance examples: `examples/info-stories/`.

## Workflows

```text
/linkedin-animated-infographics:new-post    [topic or URL] [--arabic] [--mascot]
/linkedin-animated-infographics:render-gif  [path.html] [--duration 6.0] [--fps 12.5]
/linkedin-animated-infographics:qa-post     [path.html] [caption.md]
```

`new-post` is the parent orchestrator. Worker agents return explicit artifacts to it instead of coordinating hidden peer calls. The executable route, conditional mascot path, skill preloads, and capability ownership are tracked in `architecture/plugin-graph.json`.

## Agents

| Agent | Does |
|---|---|
| `design-study` | Extracts reusable design DNA from references without pixel cloning |
| `evidence-checker` | Blocks unsupported claims and fabricated proof |
| `story-architect` | Resolves the four-axis Info-stories brief |
| `palette-curator` | Verifies Story House tokens and contrast |
| `copy-compressor` | Compresses artboard copy while preserving facts and voice |
| `layout-composer` | Produces the structural fingerprint and layout specification |
| `caption-writer` | Writes the caption under caption-specific rules |
| `artboard-builder` | Builds and checks the still |
| `motion-director` | Defines the communication job of motion |
| `mascot-animator` | Inspects and animates the exact supplied mascot SVG under an identity contract |
| `motion-engineer` | Integrates seekable motion and closes the loop |
| `render-qa` | Produces deterministic render evidence |
| `post-critic` | Red-teams copy, UI fidelity, mascot identity, visual structure, and motion |
| `story-verifier` | Independently verifies acceptance criteria against artifact evidence |

## Hooks

A `PostToolUse` lint runs on HTML files containing an `#artboard`. It catches non-seekable `requestAnimationFrame` motion, network fonts, and missing or wrongly sized artboards before a full render.

## Development & Validation

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tools skills/svg-mascot-animator/scripts
python3 scripts/info_stories.py check
python3 scripts/plugin_graph.py check
python3 scripts/validate_marketplace.py
claude plugin validate .
```

The GitHub validation workflow also registers the marketplace from a clean checkout and installs `linkedin-animated-infographics@mamdouh-creative-tools` as an end-to-end marketplace smoke test.

## Credits

Built by **Mamdouh Aboammar**, Managing Partner at Momint, founder of PrePilot.cloud and OpenOps Studio.

The mascot layer takes its physics and rig from [vibe-svgs](https://github.com/imMamdouhaboammar/vibe-svgs).

MIT licensed.
