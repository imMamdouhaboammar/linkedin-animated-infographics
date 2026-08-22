---
name: mascots
description: Use an exact verified mascot SVG as a story element, choose a communication role and creative motion direction, preserve identity, and keep character motion inside the infographic budget.
---

# Mascots for infographics

## Purpose

Use a mascot as a communication element rather than decoration. The mascot should guide reading, reveal a state, confirm a payoff, or provide a small contextual reaction while preserving the exact verified identity source.

Read `helper/GUIDE.md` and `skills/info-stories/references/asset-source-policy.md` first. `mascot-identity` and `verified-identity-assets` are blocking for named or official mascots.

## Non-negotiable identity rule

A named mascot is not a prompt. It is an identity asset.

Never redraw, approximate, trace, prompt-generate, reconstruct, or silently substitute an official mascot. Never alter identity geometry or identity colors to make the mascot fit the composition. Solve the composition around the mascot instead.

If the exact official source cannot be verified, return HOLD rather than inventing a lookalike.

## Vibe SVGs boundary

The repository `https://github.com/imMamdouhaboammar/vibe-svgs` may be used as a curated discovery/source surface, but its manifest explicitly marks mascot/scene work with `communityArtwork: true` and describes those assets as fan-made/community artwork.

Therefore:

- Vibe SVGs community mascots must not be called official.
- A Vibe SVGs community mascot cannot satisfy a request for the original or official mascot by itself.
- If the user explicitly accepts a community/fan-made mascot, pin the Vibe SVGs commit, path, blob SHA, local SHA-256, set `identity_status: community-artwork`, set `community_artwork: true`, and require `user_confirmed: true`.
- If the user asks for an official/original mascot, use an exact user-supplied or original-owner asset. If unavailable, HOLD.
- Vibe SVGs platform/tool logos under `svgs/logos/` follow the separate identity asset policy. Do not treat logo availability as proof that a mascot in the same repository is official.

## Use when

Use when the user names an official mascot, supplies a mascot SVG, asks for mascot motion, wants a character to guide reading order, or needs a mascot component inside an Info-story.

## Inputs

- `build/mascot-request.json`
- `build/asset-plan.json` when the complete/focused parent workflow resolved the identity
- exact verified SVG from user/task input or approved original-owner resolution
- explicitly confirmed community SVG only when the brief permits community artwork
- approved still/layout zone
- selected creative concept and mascot communication job
- motion direction and output track

## Outputs

Return validated mascot role, chosen creative direction, source provenance, inspection/identity notes, motion budget, rig constraints, and a mascot motion contract for downstream motion/render verification.

## Procedure

1. Apply the verified identity precedence from `asset-source-policy.md`: exact user/task official asset first, original-owner source second, then only source classes explicitly allowed by the policy. A community mascot is never promoted to official by inference.
2. The complete workflow consumes the exact local SVG recorded by `build/asset-plan.json`. Never redraw, approximate, substitute, generate a lookalike, or silently use a different mascot.
3. In a direct focused mascot task with no asset plan, first resolve whether the request means official/original or explicitly community artwork. For official/original, require an exact verifiable source. If none is available, return `HOLD: exact official mascot SVG required`.
4. Validate the request:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/mascot_contract.py check build/mascot-request.json
```

5. Record an identity fingerprint before motion work. At minimum retain source SHA-256, viewBox, outer aspect ratio, identity-defining paths/groups, and identity colors. Later QA compares against this fingerprint.
6. Pick one communication role. Pointer carries reading order, Payoff confirms the final state, and Idle provides quiet presence. A mascot pointer replaces another pointer primitive rather than adding a competing route.
7. Read `skills/svg-mascot-animator/references/creative-directions.md`. Adapt a direction such as Guide the Eye, Curious Peek, Inspect and React, Carry and Place, Reveal Assistant, Status Confirmation, Route Follow, Card-to-Card Handoff, Calm Idle Breathing, or Contextual Micro-Reaction.
8. The direction must state what the motion communicates, which existing SVG parts may move, which support elements may be added outside the identity, how the loop resets, and what competing primitive it replaces.
9. Preserve identity geometry and identity colors. Motion may transform existing groups for translation, rotation, squash, limb articulation, blink, or expression only when the existing SVG structure supports it. Do not redraw missing limbs, facial features, logos, or wordmarks inside the mascot.
10. Preserve frame 0, the outer 48px safe zone, one artboard clock, and deterministic seekable timing for rendered infographic output.
11. Generate timing/physics from the existing tools rather than hand-nudging arbitrary keyframes:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py budget --mascot 64 --travel 1 --idles 4
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py hop --loop 6000 --id mf --stops 5 --apex 40 --dwell .11
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py idle --loop 6000 --id amb --n 2 --amp 3 --blink
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/bake_mascot.py payoff --loop 6000 --id win --at .89 --rise 18 --zeta .30
```

12. Route to `svg-mascot-animator` or `agents/mascot-animator.md`.
13. Final mascot QA must compare the rendered mascot against the approved identity source. Any unapproved path/color/wordmark change is blocking even if the animation is visually attractive.

## HOLD conditions

Return HOLD when:

- an official/original mascot is requested without an exact verified source
- a Vibe SVGs `communityArtwork` asset is being presented as official
- source provenance is mutable, missing, or cannot identify exact bytes
- identity geometry or identity colors would need to be changed to make the layout work
- the mascot lacks a clear reading job
- character motion exceeds the motion budget
- frame 0 is altered
- motion direction conflicts with story motion
- downstream output no longer matches the approved identity fingerprint

## Related components

- asset policy: `skills/info-stories/references/asset-source-policy.md`
- brand icons: `tools/brand_icon.py`, `docs/brand-icons.md`
- Vibe SVGs: `https://github.com/imMamdouhaboammar/vibe-svgs`
- animator skill: `skills/svg-mascot-animator/SKILL.md`
- contract checker: `scripts/mascot_contract.py`
- math engine: `scripts/bake_mascot.py`
- worker: `agents/mascot-animator.md`

## Research gates

Apply `mascot-identity` to preserve exact mascot geometry, source provenance, and identity status. Apply `motion-on-weak-still` and `decorative-motion` to keep character motion meaningful and inside the motion budget.
