# linkedin-animated-infographics

A Claude Code plugin for designing, rendering, and animating deterministic 1080x1350 GIF infographics, Info-stories, UI mockup stories, and SVG mascots for LinkedIn (Arabic & RTL supported).

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
| `mascots` | Mascot roles, seek-safe rig, motion budgeting, archetype compatibility |
| `render` | Frame capture, GIF assembly with size budgeting, QA gates, publishing |
| `arabic` | RTL mirroring, Arabic type scale, bidi isolation, caption rhythm |
| `svg-mascot-animator` | SVG inspection, rigging, physics, and deterministic animation |

## Info-stories

Info-stories separates a visual direction into four choices:

1. **Story House**: semantic colour palette and contrast roles
2. **Visual Style**: structural grammar such as Signal Sheet, Command Canvas, or Proof Mosaic
3. **Story Archetype**: narrative job such as Framework in One Page or One Prompt, Full Workflow
4. **Motion Pattern**: zero to two meaning-driven motions

Each Visual Style also carries three 1-10 design dials: design variance, motion intensity, and visual density. Reference images or GIFs can be diagnosed first by `design-study`; the diagnosis maps design DNA into ranked local choices rather than copying the source.

Inspect and validate the registry and executable graph:

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

`new-post` is the parent orchestrator. Worker agents return explicit artifacts to it instead of coordinating hidden peer calls. The executable route and capability ownership are tracked in `architecture/plugin-graph.json`.

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
| `motion-engineer` | Implements seekable motion and closes the loop |
| `render-qa` | Produces deterministic render evidence |
| `post-critic` | Red-teams copy, visual structure, and motion before shipment |
| `story-verifier` | Independently verifies acceptance criteria against artifact evidence |

## Hooks

A `PostToolUse` lint runs on HTML files containing an `#artboard`. It catches non-seekable `requestAnimationFrame` motion, network fonts, and missing or wrongly sized artboards before a full render.

## Development & Validation

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tools
python3 scripts/info_stories.py check
python3 scripts/plugin_graph.py check
python3 scripts/validate_marketplace.py
claude plugin validate .
```

## Credits

Built by **Mamdouh Aboammar**, Managing Partner at Momint, founder of PrePilot.cloud and OpenOps Studio.

The mascot layer takes its physics and rig from [vibe-svgs](https://github.com/imMamdouhaboammar/vibe-svgs).

MIT licensed.
