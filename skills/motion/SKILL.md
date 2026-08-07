---
name: motion
description: Design and implement deterministic seekable infographic motion that communicates reading order, state, reveal, hierarchy, or route direction while preserving a complete first frame and clean loop.
---

# Motion

## Purpose

Add meaning-driven motion to an already approved still. Motion should clarify sequence, hierarchy, route, state change, reveal, or the selected creative payoff. It is not a substitute for weak structure.

Read `helper/GUIDE.md` first. Rendered infographic animation is seeked frame-by-frame, not screen-recorded in real time.

## Use when

Use when choosing or implementing Motion Patterns, writing keyframes, animating routes or state changes, integrating mascot motion, debugging a loop, or diagnosing an oversized/jittery GIF caused by animation behavior.

## Inputs

- approved `build/still.png` and `build/post.html`
- selected creative concept and aha mechanic when present
- `build/story-brief.json`
- `build/layout-spec.json`
- `build/motion-direction.json` when produced by the motion director
- optional mascot motion contract
- target duration/fps from verified timing options

## Outputs

Return or support the animated `build/post.html`, resolved Motion Patterns, timing rationale, loop/motion-budget notes, and any HOLD that prevents deterministic capture.

## Procedure

1. Read `references/animation-recipes.md` and active helper gates.
2. Use one loop clock. Define `--loop` once and derive sub-animation durations with integer divisions. Do not mix arbitrary unrelated durations.
3. Frame 0 must be a complete readable still and the animation state at 0% and 100% must close.
4. Use at most two meaning-driven motion patterns for the infographic. A Mascot Pointer replaces another pointer primitive rather than adding a third competing route.
5. Available primitives include Sequential Highlight, Path Particles, Path Draw-On, Orbit, Staggered Reveal, Bar Growth, Typewriter, Glow Pulse, Ambient Micro-Loops, and Mascot Pointer.
6. Tie motion to the selected concept's useful payoff. A reveal, state transition, route, or comparison can support `creative-payoff`; decorative movement that does not change understanding should stay static.
7. Keep changed pixels under control. Large blur, backdrop-filter, large shadow spread, and full-canvas decorative motion are poor choices for GIF encoding.
8. Respect the reverse-delay rule for sequential animation. Verify order by capturing quarter-cycle frames instead of trusting intuition.
9. Keep the outer 48px safe zone static and preserve reduced-motion behavior where the delivery context supports it.
10. Render with verified timing rows:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/render.sh build/post.html build/post.gif --duration 6.0 --fps 12.5
```

11. Read seam and changed-pixel evidence before approving the motion.

## HOLD conditions

Return a HOLD when the still is not approved, frame 0 is incomplete, the loop cannot close deterministically, motion contradicts the approved reading order, the requested effect exceeds the motion budget, or a mascot path lacks a validated exact-SVG component.

## Related components

- routing authority: `helper/GUIDE.md`
- local quality gates: `helper/quality-gates.json`
- motion recipes: `references/animation-recipes.md`
- motion planner: `agents/motion-director.md`
- implementation worker: `agents/motion-engineer.md`
- mascot skill: `skills/mascots/SKILL.md`
- render skill: `skills/render/SKILL.md`

## Research gates

Apply `design-dials` when resolving motion intensity and `bounded-verification` when the animated result reaches render/acceptance. `structural-originality` remains relevant when motion behavior is part of the story fingerprint.
