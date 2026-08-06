---
name: render
description: >-
  Capture frames, assemble the GIF, run the quality gates, and publish. Use when rendering an
  artboard to a GIF, when a render fails or comes back oversized, blank, or jittery, when
  checking a post against the QA gates before export, or when asking how to upload and post it
  on LinkedIn. Covers the headless-Chrome capture pipeline, two-pass palette GIF assembly with
  size budgeting, every QA gate, and the upload and first-comment mechanics.
---

# Render and ship

## One command

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/render.sh build/post.html build/post.gif --duration 6.0 --fps 12.5
```

That wraps two steps you can also run separately:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/capture_frames.py build/post.html --out build/frames \
        --duration 6.0 --fps 12.5 --selector "#artboard"
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_gif.py build/frames --out build/post.gif \
        --fps 12.5 --max-mb 5 --colors 128
```

`build_gif.py` runs a two-pass ffmpeg palette and then steps down colours, then fps, then
scale until the file fits the budget, printing every attempt so you can see the trade it made.

## Read three numbers from the output

- **`motion:`** the mean share of pixels changing per frame. Under 2% is healthy. Over 5% means
  something full-bleed is animating; find it.
- **`loop:`** the seam delta against the biggest normal frame-to-frame change. If the seam is
  no larger than any other frame boundary, the loop closes.
- **file size.** Keep under 5 MB and under 8 seconds or LinkedIn converts it.

## Gates before export

Run `references/qa-gates.md`. The four that catch the most failures:

- **First-frame integrity.** LinkedIn shows a static poster frame before playback. Frame 0 must
  be a complete, readable infographic on its own.
- **Mobile legibility.** `check_render.py --mobile` produces the 350px downscale. Look at it
  honestly.
- **Loop close.** Frame 0 and the last frame indistinguishable from any other frame boundary.
- **Safe zone.** Nothing animated in the outer 48px. Note the known false positive for animated
  groups inside `<defs>`, which report a zero-size rect at the origin.

## Publishing

Two things people get wrong, both in `references/publishing-playbook.md`:

- Upload the GIF as an **image**, not a document or a video. LinkedIn autoplays image GIFs.
- Put links in the **first comment**, not the caption, and say so in the caption.

## Environment

`references/production-pipeline.md` covers renderer setup, troubleshooting, and the HyperFrames
interop path for when the deliverable is a video rather than a post.

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh
```
