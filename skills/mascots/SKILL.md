---
name: mascots
description: Use an exact verified mascot SVG as a story element, choose a communication role and creative motion direction, preserve identity, and keep character motion inside the infographic budget.
---

# Mascots for infographics

## Purpose

Use a mascot as a communication element rather than decoration. The mascot should guide reading, reveal a state, confirm a payoff, or provide a small contextual reaction while preserving the exact verified identity source.

Read `helper/GUIDE.md` and `skills/info-stories/references/asset-source-policy.md` first. `mascot-identity` and `verified-identity-assets` are blocking for named or official mascots.

## Use when

Use when the user names an official mascot, supplies a mascot SVG, asks for mascot motion, wants a character to guide reading order, or needs a mascot component inside an Info-story.

## Inputs

- `build/mascot-request.json`
- `build/asset-plan.json` when the complete/focused parent workflow resolved the identity
- exact verified SVG from user/task input or approved Lobe resolution
- approved still/layout zone
- selected creative concept and mascot communication job
- motion direction and output track

## Outputs

Return validated mascot role, chosen creative direction, source provenance, inspection/identity notes, motion budget, rig constraints, and a mascot motion contract for downstream motion/render verification.

## Procedure

1. Apply the verified identity precedence from `asset-source-policy.md`: exact user/task official asset first, then a verified Lobe asset for a supported named AI/tool identity, otherwise HOLD.
2. The complete workflow consumes the exact local SVG recorded by `build/asset-plan.json`. Never redraw, approximate, substitute, generate a lookalike, or silently use a different mascot.
3. In a direct focused mascot task with no asset plan, ask the user to upload the exact SVG. If it is missing, return `HOLD: exact SVG required`.
   A third-party icon aggregator does not satisfy this gate for mascots. `tools/brand_icon.py` resolves brand marks for artboard logos, where the job is to identify a product in a story. Mascot identity is a stricter job: the asset must be the one the user or the task supplied, because an aggregator's copy has different provenance and may be outdated, unofficial, or a community redraw. You may point the user at `docs/brand-icons.md` as a place to obtain the official file, but the HOLD stands until they supply or confirm it.
4. Validate the request:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/mascot_contract.py check build/mascot-request.json
```

5. Pick one communication role. Pointer carries reading order, Payoff confirms the final state, and Idle provides quiet presence. A mascot pointer replaces another pointer primitive rather than adding a competing route.
6. Read `skills/svg-mascot-animator/references/creative-directions.md`. Adapt a direction such as Guide the Eye, Curious Peek, Inspect and React, Carry and Place, Reveal Assistant, Status Confirmation, Route Follow, Card-to-Card Handoff, Calm Idle Breathing, or Contextual Micro-Reaction.
7. The direction must state what the motion communicates, which existing SVG parts may move, which support elements may be added outside the identity, how the loop resets, and what competing primitive it replaces.
8. Preserve frame 0, the outer 48px safe zone, one artboard clock, and deterministic seekable timing for rendered infographic output.
9. Generate timing/physics from the existing tools rather than hand-nudging arbitrary keyframes:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py budget --mascot 64 --travel 1 --idles 4
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py hop --loop 6000 --id mf --stops 5 --apex 40 --dwell .11
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py idle --loop 6000 --id amb --n 2 --amp 3 --blink
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py payoff --loop 6000 --id win --at .89 --rise 18 --zeta .30
```

10. Route to `svg-mascot-animator` or `agents/mascot-animator.md`.

## HOLD conditions

Return a HOLD when a named/official mascot is requested without an exact SVG source or asset-plan resolution, the mascot lacks a clear reading job, the direction redraws the identity, character motion exceeds the motion budget, frame 0 is altered, or the motion direction conflicts with the story motion.

## Related components

- asset policy: `skills/info-stories/references/asset-source-policy.md`
- brand icons: `tools/brand_icon.py`, `docs/brand-icons.md`
- animator skill: `skills/svg-mascot-animator/SKILL.md`
- contract checker: `scripts/mascot_contract.py`
- math engine: `scripts/bake_mascot.py`
- worker: `agents/mascot-animator.md`

## Research gates

Apply `mascot-identity` to preserve exact mascot geometry and identity. Apply `motion-on-weak-still` and `decorative-motion` to keep character motion meaningful and inside the motion budget.
