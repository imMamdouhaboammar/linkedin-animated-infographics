---
name: mascots
description: >-
  Use when an infographic contains a mascot or character, especially when the user names an
  official mascot, supplies an SVG, wants a mascot to guide reading order, or needs character
  motion that stays inside the infographic motion budget.
---

# Mascots for Infographics

A mascot is a communication element, not filler. It must have one clear job in the story and it must preserve the identity of the user's asset.

## Hard gate: exact official mascot

When the user names a specific official mascot or says to use a mascot exactly:

1. Require the exact SVG from the user unless it is already attached to the current task.
2. Treat that SVG as the identity source.
3. Never redraw, approximate, substitute, generate a lookalike, or silently use a different mascot.
4. Preserve recognizable silhouette, colours, marks, face details, and proportions.
5. If the SVG structure cannot support the requested articulation, explain the rig limitation and propose safe motion that still uses the original asset.

The parent workflow owns this intake gate because the focused mascot worker should receive a validated asset, not ask the user for one itself.

Validate the request before planning motion:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/mascot_contract.py check build/mascot-request.json
```

## Roles

| Role | Count | Motion budget | Job |
|---|---:|---:|---|
| Pointer | exactly 1 | route travel | carries reading order |
| Payoff | 0 or 1 | one short reaction | confirms the final state |
| Idle | 0 to 6 | 3px target, 4px cap | quiet presence in a panel/footer |

A mascot pointer replaces an abstract pointer. Do not create two simultaneous reading orders.

## Creative direction

Read `skills/svg-mascot-animator/references/creative-directions.md`. Good starting directions include Guide the Eye, Curious Peek, Inspect and React, Carry and Place, Reveal Assistant, Status Confirmation, Route Follow, Card-to-Card Handoff, Calm Idle Breathing, and Contextual Micro-Reaction.

A direction is valid only when it states:

- what the motion communicates
- which existing mascot parts may move
- which support elements may be added outside the mascot
- how the loop resets
- what competing primitive it replaces

## Seek-safe infographic motion

Use one artboard clock. Frame 0 stays complete. Motion in the outer 48px margin is prohibited. Use baked CSS/SMIL/seekable motion for deterministic frame capture. Do not use runtime `requestAnimationFrame` animation in a rendered LinkedIn GIF.

Generate physics/timing rather than nudging arbitrary keyframes:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py budget --mascot 64 --travel 1 --idles 4
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py hop --loop 6000 --id mf --stops 5 --apex 40 --dwell .11
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py idle --loop 6000 --id amb --n 2 --amp 3 --blink
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py payoff --loop 6000 --id win --at .89 --rise 18 --zeta .30
```

Never hand-edit baked timing output. Change the parameters and regenerate.

## Structural fit

Mascots work best in route, process, annotated, and state-change stories. Dense catalogs and reference sheets usually need no moving character. UI Mockup Stories may use a mascot as a guide, assistant, or state reaction only if it does not cover core controls or imitate a product assistant that does not actually exist.

## Verification

Before shipment confirm:

- the exact supplied SVG remains recognizably unchanged
- the role is singular and clear
- the selected creative direction has a story purpose
- frame 0 is complete
- the motion budget is respected
- the mascot does not compete with UI, copy, or route highlights
- reduced-motion and accessibility requirements from the SVG animator contract are satisfied

Full infographic mascot doctrine and failure modes remain in `references/mascots.md`.
