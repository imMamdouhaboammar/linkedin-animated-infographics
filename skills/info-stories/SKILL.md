---
name: info-stories
description: Use when turning source material, a topic, a screenshot, or an approved caption into a structured LinkedIn infographic story and choosing its palette, visual grammar, narrative shape, or motion direction.
---

# Info-stories

Info-stories resolves four independent choices before any HTML is built: **Story House**, **Visual Style**, **Story Archetype**, and **Motion Pattern**. It is an orchestration layer over the existing artboard, motion, render, mascot, Arabic, and QA skills.

## Use the registry

`catalog.json` is the machine-readable source of truth. Validate it before a build:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/info_stories.py check
```

Inspect options with `list` and `show`. Use `scaffold` to emit a deterministic story brief after choices are resolved.

## Resolution order

1. **Story Archetype** from the content's narrative job. Read `references/story-archetypes.md`.
2. **Visual Style** from information topology and density. Read `references/visual-styles.md`.
3. **Story House** from tone, brand constraints, and contrast. Read `references/palette-houses.md`.
4. **Motion Patterns** from what motion must communicate. Read `references/motion-patterns.md`.
5. Check the combination against `references/composition-matrix.md` and the registry.

Explicit user choices win unless they violate a hard contrast, compatibility, or render constraint. Unknown choices fail with valid alternatives instead of silently substituting a default.

## Reference study

When the direction comes from screenshots, GIFs, previous designs, or a public reference, use `design-study` and read `references/study-protocol.md` before selecting the four axes. A study diagnoses design DNA; it does not grant permission to copy source wording or distinctive assets.

## Agent handoff

Use `story-architect` for the four-axis brief. It may delegate palette, layout, motion, copy compression, and evidence checks to their focused agents. Once the brief is approved, hand the static composition to `artboard-builder`, then hand approved motion direction to `motion-engineer`. Existing render and QA skills stay authoritative for capture, GIF assembly, mobile checks, seam checks, and file budgets.

## Hard constraints

- Keep one 1080x1350 artboard and the existing attribution footer contract.
- Text pairs declared by a Story House must meet 4.5:1 contrast.
- Use at most two motion patterns; every motion needs a reading, hierarchy, sequence, or state reason.
- Frame 0 remains a complete still.
- Never invent metrics, testimonials, proof, product facts, or source claims.
- A palette swap is not a new visual style. Structural choices must change when the story needs a different visual grammar.

## Independent verification

Before delivery of a built Info-story, use `story-verifier` and `references/verification-loop.md`. The verifier reads artifacts directly, records evidence against stable criteria, and permits at most two targeted fix attempts before escalation.
