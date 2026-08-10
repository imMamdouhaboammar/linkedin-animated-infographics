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

10. UI mockup stories may use a mascot only when it does not cover story-critical controls or imply a product assistant that does not actually exist.
11. Verify identity, provenance, purpose, frame-zero readability, loop reset, motion budget, and accessibility before returning the component.

## HOLD conditions

Return a HOLD when no verified exact SVG is available, Lobe provenance cannot be confirmed for a Lobe-backed identity, the SVG cannot support the requested articulation without identity-changing redraw, required brand details are ambiguous, or the requested mascot behavior would fabricate product behavior or compete with the approved reading order.

## Related components

- routing authority: `helper/GUIDE.md`
- identity policy: `skills/info-stories/references/asset-source-policy.md`
- verified identity worker: `agents/asset-curator.md`
- mascot worker: `agents/mascot-animator.md`
- animator skill: `skills/svg-mascot-animator/SKILL.md`
- creative directions: `skills/svg-mascot-animator/references/creative-directions.md`
- detailed doctrine: `references/mascots.md`
- request validator: `scripts/mascot_contract.py`
- motion baker: `scripts/bake_mascot.py`

## Research gates

Mascot identity provenance follows the local verified identity contract. When the mascot is embedded in a complete Info-story, also respect active `design-dials`, `structural-originality`, `evidence-traceability`, and `bounded-verification` gates from the parent route.
