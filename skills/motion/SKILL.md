---
name: motion
description: >-
  Write the animation for a 1080x1350 artboard so it loops seamlessly and captures
  deterministically. Use when adding motion to an infographic, writing keyframes, staggering a
  sequence, animating a path, diagnosing a visible loop point, or fixing a GIF that came back
  oversized, blank, or jittery. Covers ten seekable motion primitives, the one-loop-clock rule,
  the reverse-delay trap, motion budgeting by changed pixels, and a symptom-to-cause debugging
  table.
---

# Motion

Animations are **seeked**, not recorded. `capture_frames.py` pauses
`document.getAnimations()`, sets `currentTime` per frame, and calls `svg.setCurrentTime()` for
SMIL. That gives pixel-identical frames and a mathematically exact loop close. Real-time screen
recording produces the wobble that reads as amateur.

## Three rules that decide whether it works

**One loop clock.** Define `--loop` once and derive everything from it. A sub-animation that
genuinely needs to be faster gets an integer division: `calc(var(--loop) / 4)`. Never `1.3s`
next to `4.8s`. Legal divisors: 1, 2, 3, 4, 5, 6, 8, 10, 12.

**Frame 0 equals frame N.** The value at `0%` and `100%` must be identical.
`build_gif.py` prints the seam delta; anything larger than the biggest normal frame-to-frame
change means something does not close.

**Motion budget is changed pixels, not area.** A dense dark grid animating 85% of its canvas
can encode cheaper than four boxes and four dots on a light textured ground. Judge on
`build_gif.py`'s `motion:` line. Under 2% is healthy. Never animate `filter: blur()`, large
`box-shadow` spread, or `backdrop-filter`: they rewrite every pixel underneath and defeat
rectangle diffing.

## The primitives

Sequential Highlight, Path Particles, Path Draw-On, Orbit, Staggered Reveal, Bar Growth,
Typewriter, Glow Pulse, Ambient Micro-Loops, and Mascot Pointer.

**Use exactly two per artboard.** That is what the reference set does and it is the right
number. A mascot does not add a third: Mascot Pointer replaces Path Particles, and the
highlight it drives is still Sequential Highlight.

`references/animation-recipes.md` has the code for each, the composition table pairing
primitives to archetypes, the timing table of loop/fps combinations verified to close, and the
symptom-to-cause debugging table. Read it before writing any animation CSS.

## The trap that costs the most renders

A negative `animation-delay` pushes an animation **forward** in its cycle. To have element `i`
of `N` active at `t = (i-1) x loop / N`, the delays run in **reverse**:
`0, -loop x 3/4, -loop x 2/4, -loop x 1/4` for four elements. Writing the intuitive
`0, -1/4, -2/4, -3/4` produces the order 1 → 4 → 3 → 2, which looks almost right in a thumbnail
and is obviously wrong once anyone watches it.

Verify by capturing four frames at `t = 0, loop/4, loop/2, 3xloop/4` and checking the order.

## Render

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/render.sh build/post.html build/post.gif --duration 6.0 --fps 12.5
```

Pick duration and fps from the timing table rather than inventing numbers. Each verified row
divides cleanly and closes.
