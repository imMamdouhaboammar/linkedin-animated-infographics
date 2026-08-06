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
| `artboard` | 13 layout archetypes, House 0 palette, type scale, offline fonts |
| `motion` | 10 seekable primitives, one-loop-clock rule, reverse-delay trap |
| `mascots` | 3 mascot roles, seek-safe rig, motion budgeting, archetype compatibility |
| `render` | Frame capture, GIF assembly with size budgeting, QA gates, publishing |
| `arabic` | RTL mirroring, Arabic type scale, bidi isolation, caption rhythm |
| `svg-mascot-animator` | Physics-driven SVG mascot & logo animation (Anime.js v4 & baked CSS keyframes) |

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
| `motion-engineer` | Adds exactly two primitives and makes the loop close |
| `render-qa` | Renders and judges, read-only, keeping render noise off main thread |
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
