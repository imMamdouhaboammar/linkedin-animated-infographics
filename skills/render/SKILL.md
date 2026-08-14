---
name: render
description: Capture deterministic infographic frames, assemble GIF output, measure motion/seam/file size, and run the render acceptance gates before shipment.
---

# Render and ship

## Purpose

Convert an approved static/animated artboard into deterministic render evidence and final GIF output. Rendering is an acceptance stage, not a place to redesign the story.

Read `helper/GUIDE.md` first. Render evidence feeds `post-critic` and `story-verifier` through `build/render-report.json`.

## Use when

Use when capturing frames, building a GIF, diagnosing blank/jittery/oversized output, measuring seam or changed pixels, running render QA, or preparing a final LinkedIn image GIF.

## Inputs

- approved `build/post.html`
- duration/fps from verified motion timing when animated
- output file-size budget
- expected frame-zero state and safe-zone constraints

## Outputs

Return GIF/static render output plus `build/render-report.json` containing frame-zero, mobile legibility, motion percentage, seam result, duration/fps, file size, and any blocking render finding.

## Procedure

1. Use the one-command path when possible:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/render.sh build/post.html build/post.gif --duration 6.0 --fps 12.5
```

2. The underlying deterministic stages are:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/capture_frames.py build/post.html --out build/frames --duration 6.0 --fps 12.5 --selector "#artboard"
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_gif.py build/frames --out build/post.gif --fps 12.5 --max-mb 5 --colors 128
```

3. Read `references/qa-gates.md`, `references/production-pipeline.md`, and `references/pixel-perfect-browser-inspection.md`.
4. Inspect three core measurements: mean changed-pixel `motion:`, loop seam relative to normal frame deltas, and file size.
5. Treat frame 0 as a complete poster frame. It must remain readable before autoplay.
6. Inspect the 350px feed downscale honestly. Render success without feed-scale legibility is not acceptance.
7. Keep the outer 48px safe zone free of motion and account for known SVG `<defs>` false positives when diagnosing geometry.
8. If encoding exceeds the budget, prefer the existing controlled color/fps/scale fallback rather than arbitrary re-authoring.
9. For publishing guidance, read `references/publishing-playbook.md`: LinkedIn GIF output is uploaded as an image; links normally belong in the first comment when the post strategy calls for them.

## HOLD conditions

Return a HOLD when capture fails, frame 0 is incomplete, the seam does not close, changed-pixel motion indicates unintended full-canvas animation, feed-scale output is unreadable, safe-zone rules fail, or output cannot fit the accepted file budget without unacceptable degradation.

## Related components

- routing authority: `helper/GUIDE.md`
- focused render workflow: `skills/render-gif/SKILL.md`
- motion skill: `skills/motion/SKILL.md`
- QA gates: `references/qa-gates.md` and `references/pixel-perfect-browser-inspection.md`
- production setup: `references/production-pipeline.md`
- render worker: `agents/render-qa.md`
- independent verifier: `agents/story-verifier.md`

## Research gates

`bounded-verification` governs how render failures enter the repair/re-check loop. `contrast-discipline` remains relevant to rendered evidence, and `evidence-traceability` applies when the final artifact contains factual proof that must be checked visually.
