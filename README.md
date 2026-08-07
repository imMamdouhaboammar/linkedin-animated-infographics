# linkedin-animated-infographics

A Claude Code plugin for designing, rendering, and animating deterministic 1080x1350 GIF infographics and SVG mascots for LinkedIn (Arabic & RTL supported).

## Install

```bash
/plugin install imMamdouhaboammar/linkedin-animated-infographics
```

Then, once per machine:

```bash
bash scripts/setup.sh
```

That installs Playwright and a Chrome binary and checks for `ffmpeg`. Everything else runs on plain Python 3.

## Features & Skills

| Skill | Covers |
|---|---|
| `post` | The main router. Pipeline, non-negotiables, working method |
| `caption` | 7 caption archetypes, the truncation cut, hook & CTA libraries, ban list |
| `info-stories` | Story Houses, Visual Styles, Story Archetypes, Motion Patterns, study, and verification |
| `artboard` | 13 execution archetypes, type scale, offline fonts, and still construction |
| `motion` | 10 seekable primitives, one-loop-clock rule, reverse-delay trap |
| `mascots` | 3 mascot roles, seek-safe rig, motion budgeting, archetype compatibility |
| `render` | Frame capture, GIF assembly with size budgeting, QA gates, publishing |
| `arabic` | RTL mirroring, Arabic type scale, bidi isolation, caption rhythm |
| `svg-mascot-animator` | Physics-driven SVG mascot & logo animation (Anime.js v4 & baked CSS keyframes) |

## Info-stories

Info-stories separates a visual direction into four choices so a new post can change structure without throwing away the existing render pipeline:

1. **Story House** - semantic colour palette and contrast roles
2. **Visual Style** - structural grammar such as Signal Sheet, Command Canvas, or Proof Mosaic
3. **Story Archetype** - narrative job such as Framework in One Page or One Prompt, Full Workflow
4. **Motion Pattern** - zero to two meaning-driven motions

Each Visual Style also carries three 1-10 design dials: design variance, motion intensity, and visual density. Reference images or GIFs can be diagnosed first by `design-study`; the diagnosis maps design DNA into ranked local choices rather than copying the source.

Inspect and validate the registry:

```bash
python3 scripts/info_stories.py check
python3 scripts/info_stories.py list house
python3 scripts/info_stories.py list style
python3 scripts/info_stories.py compose --style signal-sheet --archetype framework-in-one-page --motion sequential-highlight
```

Generate a deterministic story brief with `scripts/info_stories.py scaffold`. External capability research lives under `research/capability-notes/`; the cloned upstream working copies are ignored and are not shipped with the plugin.

### Info-stories tools

```bash
# Browse all ten named Story Houses as a visual HTML chooser
python3 tools/palette_preview.py --out assets/info-stories-palettes.html

# Write a resolved story brief to a file
python3 tools/story_scaffold.py --topic "..." --takeaway "..." --cta "..." \
  --house ember-paper --style signal-sheet --archetype framework-in-one-page \
  --motion sequential-highlight --out build/story-brief.json

# Check whether a style, archetype, and motion set can compose
python3 tools/composition_check.py --style signal-sheet \
  --archetype framework-in-one-page --motion sequential-highlight

# Detect named copy-pattern failures without guessing authorship
python3 tools/copy_slop_check.py "copy to inspect"
```

Tracked chooser: `assets/info-stories-palettes.html`. Acceptance examples: `examples/info-stories/`.

## Workflows (user-invoked)

```bash
/linkedin-animated-infographics:new-post    [topic or URL] [--arabic] [--mascot]
/linkedin-animated-infographics:render-gif  [path.html] [--duration 6.0] [--fps 12.5]
/linkedin-animated-infographics:qa-post     [path.html] [caption.md]
```

## Agents

| Agent | Does |
|---|---|
| `caption-writer` | Writes the caption, enforces the ban list, verifies every number |
| `artboard-builder` | Builds the still until it passes `check_render.py` |
| `motion-engineer` | Implements the resolved zero-to-two motion patterns and makes the loop close |
| `render-qa` | Renders and judges, read-only, keeping render noise off main thread |
| `story-architect` | Resolves the four-axis Info-stories brief before production |
| `design-study` | Extracts design DNA from references without pixel cloning |
| `palette-curator` | Selects and verifies Story House tokens and contrast |
| `layout-composer` | Converts story beats into a structural fingerprint and layout spec |
| `motion-director` | Selects motion patterns and their communication job |
| `copy-compressor` | Compresses artboard copy while preserving facts and voice |
| `evidence-checker` | Blocks unsupported claims and fabricated proof |
| `story-verifier` | Independently verifies acceptance criteria against artifact evidence |
| `post-critic` | Red-teams the finished post before it ships |

## Hooks

A `PostToolUse` lint runs on any HTML file containing an `#artboard`. It catches the three failures that otherwise cost a full render: `requestAnimationFrame` motion that cannot be seeked, a webfont loading over the network, and a missing or wrongly-sized artboard element.

## Development & Validation

```bash
claude plugin validate .
```

## Credits

Built by **Mamdouh Aboammar**, Managing Partner at Momint, founder of PrePilot.cloud and OpenOps Studio.

The mascot layer takes its physics and rig from [vibe-svgs](https://github.com/imMamdouhaboammar/vibe-svgs).

MIT licensed.
