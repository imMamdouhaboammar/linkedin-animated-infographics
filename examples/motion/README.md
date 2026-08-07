# Motion Skill Example: ROAS Reality Check

This example applies the `motion` skill to a realistic LinkedIn infographic from prompt to deterministic GIF render.

## Realistic user prompt

> Create a 1080x1350 animated LinkedIn infographic for paid media managers. Explain why a campaign with 4.2 platform ROAS can still lose money after refunds, gross margin, and blended acquisition cost. Use a restrained editorial style, keep the title and footer static, guide the reader through four checks in order, and end with a commercial verdict. The loop must close cleanly and the GIF must stay below 5 MB.

## Motion design decision

Archetype: Flow Map + Verdict

The skill requires exactly two primitives per artboard. This example uses:

1. `Sequential Highlight` on the four profit checks
2. `Path Particles` on the four SVG connectors flowing into the verdict

The master clock is `--loop: 4800ms`, using the verified timing row `4.8 seconds at 12.5 fps`, which produces 60 frames.

The step delays use the required reverse order:

```css
0, -3/4 loop, -2/4 loop, -1/4 loop
```

This produces the reading order 1, 2, 3, 4 at 0.0s, 1.2s, 2.4s, and 3.6s.

## Render

```bash
bash scripts/render.sh \
  examples/motion/roas-reality-check.html \
  build/roas-reality-check.gif \
  --duration 4.8 \
  --fps 12.5
```

## Verified QA result

- Artboard: 1080x1350
- Smallest rendered type: 22px
- Safe margin: clean
- RequestAnimationFrame use: none
- CSS animation duration: 4800ms only
- Frames: 60
- Mean changed pixels per frame: 0.27%
- Largest normal frame transition: 4.44%
- Loop seam transition: 4.33%
- Seam ratio: 0.97, so the loop closes cleanly
- GIF size with 128 colors: 0.23 MB

The HTML is self-contained and uses no remote fonts or network assets.
