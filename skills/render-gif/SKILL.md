---
name: render-gif
description: Render an existing infographic artboard HTML to a deterministic looping GIF, then report motion, seam, and file-size evidence without changing the approved design.
disable-model-invocation: true
argument-hint: "[path/to/artboard.html] [--duration 6.0] [--fps 12.5]"
---

# /linkedin-animated-infographics:render-gif

Arguments: **$ARGUMENTS**

## Purpose

Provide a **focused workflow** for rendering an already approved artboard. This workflow does not redesign copy, layout, palette, or motion direction; it turns the existing artifact into deterministic GIF evidence.

Read `helper/GUIDE.md` first.

## Use when

Use when the user already has artboard HTML and wants the GIF output, wants a render rerun after a targeted fix, or needs the three core render measurements without running the entire new-post workflow.

## Inputs

- path to approved artboard HTML
- optional duration/fps override
- desired output path and file-size budget

## Outputs

Return the rendered GIF plus motion percentage/verdict, seam result, file size, and any HOLD that prevents a trustworthy render.

## Procedure

1. If no path is supplied, locate candidate `build/*.html` artifacts and ask/select rather than guessing.
2. Lint before rendering:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/lint_artboard.sh <path>
```

3. If duration/fps are not supplied, use a verified timing row from the `motion` skill. Do not invent arbitrary timings that cannot close cleanly.
4. Render:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/render.sh <path> <out.gif> --duration <d> --fps <f>
```

5. Inspect `motion:`, seam, and file size. If the seam fails, use the motion debugging reference to identify the likely cause instead of guessing.
6. Return the GIF and concise render evidence. Do not add a design postamble that implies unperformed QA.

## HOLD conditions

Return a HOLD when lint fails, browser capture is unavailable, frame 0 is invalid, the loop seam fails, output exceeds the accepted budget after controlled fallback, or the render evidence cannot be produced reliably.

## Related components

- routing authority: `helper/GUIDE.md`
- domain render skill: `skills/render/SKILL.md`
- motion skill: `skills/motion/SKILL.md`
- render worker: `agents/render-qa.md`
- full QA workflow: `skills/qa-post/SKILL.md`

## Research gates

`bounded-verification` applies to render failure/re-check behavior. The workflow reports evidence and does not silently mutate the artifact to force a PASS.
