---
name: svg-mascot-animator
description: >-
  Animate an exact SVG mascot, logo, icon, or character with professional physics-driven motion.
  Use whenever the user supplies an SVG for animation, names an official mascot that must be used
  exactly, requests believable mascot motion, or wants static/baked or runtime SVG animation.
license: MIT
---

# SVG Mascot Animator

The input SVG is the identity source. Animation adds behavior around that source; it does not redesign the character.

## Identity and asset gate

For a named or official mascot:

- require the exact user-supplied or task-attached SVG before animation begins
- never substitute a generated mascot or a visually similar asset
- keep an untouched copy of the source SVG
- preserve recognizable silhouette, proportions, brand colours, face details, marks, and distinctive geometry

If the exact SVG is missing and this skill is running in the main conversational context, ask the user to upload the exact SVG and do not start mascot production. If this skill is running inside a focused subagent, return `HOLD: exact SVG required` to the parent workflow instead of contacting the user or inventing an asset.

Run the request contract before inspection:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/mascot_contract.py check build/mascot-request.json
```

## Inspect before promising motion

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/svg-mascot-animator/scripts/inspect_svg.py <path-to-svg>
```

Record viewBox, bounds, IDs, groups, transforms, clips, paths, and addressable parts. A single-path mascot cannot articulate limbs or eyes independently. Use body-level transforms, external support elements, or ask the user whether an articulated derivative is acceptable. Never split identity-critical geometry silently.

## Choose the delivery track

**Deterministic static/baked track** is the default for LinkedIn GIFs, README assets, and anything captured frame by frame. Use self-contained SVG/CSS/SMIL with no runtime JavaScript.

**Runtime track** uses Anime.js when the final environment genuinely supports interaction. Use it for interactive web contexts, then bake an equivalent deterministic version if the same motion must appear in a rendered infographic.

Install and inspect the local Anime.js surface when runtime work is required:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/svg-mascot-animator/scripts/setup.sh
node ${CLAUDE_PLUGIN_ROOT}/skills/svg-mascot-animator/scripts/bake.mjs list
```

## Creative direction before keyframes

Read `references/creative-directions.md`. Start from a communication job, then adapt the motion to the supplied rig. The starter set includes Guide the Eye, Curious Peek, Inspect and React, Carry and Place, Reveal Assistant, Status Confirmation, Route Follow, Card-to-Card Handoff, Calm Idle Breathing, and Contextual Micro-Reaction.

Creative work is encouraged, but each new direction must define:

1. communication purpose
2. exact existing SVG parts allowed to move
3. optional non-identity support elements
4. loop/reset behavior
5. motion budget

Do not reuse the same bounce or float treatment for every mascot.

## Rig rules

Normalize pivots once, then separate transform concerns into nested groups: position, vertical motion, rotation, scale. Prefer transforms on existing groups and paths. Read `references/rigging.md` before changing transform structure.

If articulation exists, secondary parts may lag the primary motion by a small amount. If it does not exist, do not fake limb movement by deforming identity-critical geometry.

## Physical motion rules

Read `references/physics.md` and `references/animejs.md` before implementation. Use real motion relationships rather than decorative easing:

- projectile paths for hops and transfers
- damped springs for short landing/payoff reactions
- pendulum timing for genuine swings
- linear sampling for physical paths
- contact shadow derived from subject height
- squash/stretch tied to velocity and contact
- anticipation before committed movement
- follow-through only on addressable secondary parts

Keep contact frames short. Keep ambient motion small. Long constant bouncing, random blinking, large rotations, and unmotivated floating are failures.

## Story-aware support elements

You may add a small contact shadow, pointer dot, cursor, route line, card, badge, or lightweight prop when it helps the story and the user did not forbid it. These elements must remain visually separate from the mascot identity and should be removable without changing the official asset.

## Accessibility and asset contract

Read `references/contract.md`. Both delivery tracks require accessible labeling, ID/keyframe namespacing, reduced-motion behavior, collision-safe IDs, and no accidental external dependencies. Brand colours remain brand colours.

For static assets:

- zero JavaScript
- zero web fonts or network dependencies
- self-contained styles/animation
- deterministic seekable timing

## Verification

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/svg-mascot-animator/scripts/check_asset.py <output.svg>
python3 ${CLAUDE_PLUGIN_ROOT}/skills/svg-mascot-animator/scripts/check_asset.py --runtime <scene.html>
```

Also compare the animated output with the untouched source. Confirm identity preservation, motion purpose, loop closure, frame-zero readability when used in an infographic, and reduced-motion behavior.

## Output

Return the animated asset/component, inspection report, chosen creative direction, physics/timing rationale, identity-preservation notes, and any rig limitation. For Info-stories, return these to the parent workflow so `motion-engineer`, `render-qa`, `post-critic`, and `story-verifier` can consume the same evidence.
