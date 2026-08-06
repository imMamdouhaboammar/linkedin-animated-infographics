# linkedin-motion

Ship a LinkedIn post as a structured caption plus a 1080x1350 looping GIF infographic.

## Install

```bash
/plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics
/plugin install linkedin-motion@linkedin-animated-infographics
bash ${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh
```

## Start here

```
/linkedin-motion:new-post Turn our paid-media playbook into a post
```

Or just describe what you want. The `post` skill is model-invoked and routes to the rest.

## How the render works

Animations are **seeked**, not recorded. `capture_frames.py` pauses
`document.getAnimations()`, sets `currentTime` per frame, and calls `svg.setCurrentTime()` for
SMIL. That gives pixel-identical frames and a mathematically exact loop close. Real-time screen
recording produces the wobble that reads as amateur.

Which is also why `requestAnimationFrame` and Anime.js runtime motion do not work here. The
lint hook catches it before you spend a render.

## Scripts

| Script | Does |
|---|---|
| `setup.sh` | installs Playwright and a Chrome binary, checks ffmpeg |
| `check_render.py` | still render, 350px mobile downscale, contrast and safe-zone audit |
| `lint_artboard.sh` | grep-level checks that catch render-wasting mistakes in a second |
| `capture_frames.py` | seeks animations and screenshots N deterministic frames |
| `build_gif.py` | two-pass palette GIF assembly with automatic size budgeting |
| `render.sh` | capture then build, one command |
| `bake_mascot.py` | seek-safe mascot motion: hop routes, idles, payoff springs, budget |
| `sync_physics.sh` | refresh the vendored `physics.py` from `svg-mascot-animator` |

## Assets

`house0-tokens.css` and `house0-swatches.html` for the default palette, plus five artboard
templates including `template-mascot-flow.html`, the reference build for the mascot layer.

MIT licensed.
