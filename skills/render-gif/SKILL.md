---
name: render-gif
description: Render an existing artboard HTML file to a looping GIF and report the three numbers that matter.
disable-model-invocation: true
argument-hint: "[path/to/artboard.html] [--duration 6.0] [--fps 12.5]"
---

# /linkedin-animated-infographics:render-gif

Arguments: **$ARGUMENTS**

1. If no path was given, look for `build/*.html` and ask which one.
2. Lint before spending the render:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/lint_artboard.sh <path>
```

3. Pick duration and fps from the timing table in `linkedin-animated-infographics:motion` if they were not
   given. Do not invent numbers; each verified row divides cleanly and closes.

4. Render:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/render.sh <path> <out.gif> --duration <d> --fps <f>
```

5. Report exactly three things and nothing else: the `motion:` percentage with its verdict, the
   seam result, and the file size. If the seam does not close, name the likely cause from the
   debugging table rather than guessing.

6. Present the GIF with `present_files`. No postamble.
