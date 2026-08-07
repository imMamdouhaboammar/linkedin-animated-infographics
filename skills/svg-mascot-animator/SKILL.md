---
name: svg-mascot-animator
description: Animate an exact SVG mascot, logo, icon, or character with identity-preserving, rig-aware, professional motion for deterministic or runtime delivery tracks.
license: MIT
---

# SVG Mascot Animator

## Purpose

Animate the exact supplied SVG while preserving identity-critical geometry, colors, marks, proportions, and recognizable details. Animation adds behavior around the user's asset; it does not redesign the mascot.

Read `helper/GUIDE.md` first. For named or official mascots, the exact-SVG gate is mandatory.

## Use when

Use when the user supplies an SVG for animation, names an official mascot that must be used exactly, requests believable mascot motion, or needs a mascot component for an Info-story or interactive web context.

## Inputs

- exact user-supplied/task-attached SVG when identity must be preserved
- validated `build/mascot-request.json` when used in the infographic workflow
- approved communication job and creative direction
- output track: deterministic baked/static or runtime interactive
- approved layout/motion constraints when embedded in an infographic

## Outputs

Return animated asset/component, inspection report, chosen creative direction, physics/timing rationale, identity-preservation notes, rig limitations, and the motion contract/evidence needed by downstream motion, render, critique, and verification workers.

## Procedure

1. For a named or official mascot, require the **exact SVG** before animation begins. Keep an untouched copy of the source.
2. If the exact SVG is missing in the main conversational context, ask the user to upload it and stop. Inside a worker, return `HOLD: exact SVG required` to the parent workflow.
3. Validate the request contract:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/mascot_contract.py check build/mascot-request.json
```

4. Inspect the SVG before promising articulation:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/svg-mascot-animator/scripts/inspect_svg.py <path-to-svg>
```

Record viewBox, bounds, IDs, groups, transforms, clips, paths, and addressable parts. Do not silently split identity-critical geometry to fake articulation.
5. Choose the delivery track. Deterministic self-contained SVG/CSS/SMIL is the default for LinkedIn GIFs and frame capture. Runtime Anime.js is valid only when the target environment genuinely supports interaction.
6. Read `references/creative-directions.md`, `references/rigging.md`, `references/physics.md`, `references/animejs.md`, and `references/contract.md` as needed.
7. Define the motion job before keyframes. Specify communication purpose, exact existing SVG parts allowed to move, optional non-identity support elements, loop/reset behavior, and motion budget.
8. Use believable relationships such as projectile paths, damped landing reactions, pendulum timing for genuine swings, contact shadows derived from height, velocity-linked squash/stretch, anticipation, and follow-through only on addressable parts.
9. Avoid constant bouncing, random blinking, large rotations, unmotivated floating, or deformation that changes the mascot's identity.
10. Support elements such as route lines, cursors, cards, badges, or contact shadows must remain visually separate from the identity source and removable without changing the official mascot.
11. Verify the output:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/svg-mascot-animator/scripts/check_asset.py <output.svg>
python3 ${CLAUDE_PLUGIN_ROOT}/skills/svg-mascot-animator/scripts/check_asset.py --runtime <scene.html>
```

12. Compare the result with the untouched source and confirm identity, purpose, loop closure, frame-zero readability when used in an infographic, reduced-motion behavior, accessible labeling, namespaced IDs/keyframes, and zero accidental network dependencies for baked assets.

## HOLD conditions

Return a HOLD when the exact SVG is missing, the requested articulation is impossible without identity-changing redraw, required brand details are ambiguous, the runtime track is requested in an environment that cannot support it, or the requested motion would violate the infographic's approved reading order or evidence boundary.

## Related components

- routing authority: `helper/GUIDE.md`
- infographic mascot skill: `skills/mascots/SKILL.md`
- focused worker: `agents/mascot-animator.md`
- request validator: `scripts/mascot_contract.py`
- creative directions: `references/creative-directions.md`
- rigging: `references/rigging.md`
- physics: `references/physics.md`
- asset contract: `references/contract.md`

## Research gates

Mascot identity/rigging is a local-native capability. When embedded in the complete infographic route, inherit applicable `design-dials`, `structural-originality`, `evidence-traceability`, and `bounded-verification` gates from the parent workflow.
