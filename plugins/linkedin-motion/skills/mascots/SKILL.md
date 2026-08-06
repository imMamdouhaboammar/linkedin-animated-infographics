---
name: mascots
description: >-
  Put an animated character on an infographic without breaking the reading order. Use when
  adding a mascot, character, or logo animation to a LinkedIn visual, when a mascot should walk
  a route or react to an outcome, when idle characters should breathe or blink in a panel, or
  when a mascot renders static, blank, or out of sync with the highlight. Covers the three
  mascot roles, the seek-safe rig, the bake_mascot.py generator, the loop seam, motion
  budgeting, and which archetypes accept a character at all.
---

# Mascots

A mascot is the loudest moving object anyone can put on a page. Dropped in casually it stops
being decoration and starts competing with the reading pointer.

So the mascot is not added *next to* the pointer. **Where a mascot exists, the mascot becomes
the reading pointer**, and the abstract particle is deleted.

## Three roles, and the counts are not stylistic

| Role | Count | Amplitude | Job |
|---|---|---|---|
| **Pointer** | exactly 1 | travels the route | cards light as it lands |
| **Payoff** | 0 or 1 | one spring, ~20px | reacts at the last stop |
| **Idle** | 0 to 6 | 3px, hard cap 4px | ambient life in a panel or footer |

Two pointers means two reading orders, which means no reading order at all.

## Generate the motion, do not write it

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py budget --mascot 64 --travel 1 --idles 4
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py hop    --loop 6000 --id mf  --stops 5 --apex 40 --dwell .11
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py idle   --loop 6000 --id amb --n 2 --amp 3 --blink
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py payoff --loop 6000 --id win --at .89 --rise 18 --zeta .30
```

Run `budget` first. It costs nothing and it is the difference between finding out the mascot is
too big now or after a five-minute render.

`hop` prints the `keyTimes`/`keyPoints` pair, the landing squash, the phased contact shadow, the
seam fade, **the arrival instants already converted to the reversed negative delays the cards
need**, and the implied gravity. Read the gravity line: below 500 the mascot floats, above 2000
it snaps. Fix it by changing `--apex` or `--dwell`, never by nudging keyframes.

Never hand-edit the baked output. Change the arguments and re-run.

## What breaks it

- **Anime.js runtime motion.** `requestAnimationFrame` is not seekable. The render comes back
  static or blank. Use the baked static track only.
- **A mascot clock that is not the artboard clock.** Everything inherits `var(--loop)` or an
  integer division of it.
- **The seam on frame 0.** Frame 0 is LinkedIn's poster frame and must be a complete
  infographic. Shift every mascot track by `calc(var(--loop) * -0.5)` and the
  `<animateMotion>` by `begin="-3s"` so the fade that hides the loop teleport happens mid-cycle.
- **A missing `rotate="0"`.** `animateMotion` banks to the path tangent by default, so the
  mascot arrives at each stop tilted.

## Not every archetype takes one

Native: Character Flowchart, Pipeline Stages, Annotated Blueprint.
Idles only: Trading Card Grid, Node Tree, Directory Map.
None: Specimen Grid, Cheat Sheet Poster, Terminal Card, Logo Grid, Spec Sheet.

Full doctrine, the rig, the budget table, and the failure modes:
`references/mascots.md`. Reference build: `${CLAUDE_PLUGIN_ROOT}/assets/template-mascot-flow.html`.

## Physics comes from the sibling plugin

The timing equations live in `${CLAUDE_PLUGIN_ROOT}/scripts/physics.py`, vendored from the
`svg-mascot-animator` plugin. Plugins are copied to a cache directory on install, so a
cross-plugin relative path would not resolve. Install that plugin too when you need the full
runtime track, Anime.js, or the README asset contract.
