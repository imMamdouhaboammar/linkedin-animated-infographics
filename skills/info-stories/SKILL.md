---
name: info-stories
description: Use when turning source material, a topic, a screenshot, or an approved caption into a structured LinkedIn infographic story and choosing its palette, visual grammar, narrative shape, or motion direction.
---

# Info-stories

Info-stories resolves four independent choices before HTML is built: **Story House**, **Visual Style**, **Story Archetype**, and **Motion Pattern**. It is a composition layer over the existing artboard, motion, render, mascot, Arabic, and QA skills.

## Use the registry

`catalog.json` is the machine-readable source of truth. Validate it before a build:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/info_stories.py check
```

Inspect options with `list` and `show`. Use `scaffold` to emit a deterministic story brief after choices are resolved.

## Resolution order

1. Story Archetype from the content's narrative job. Read `references/story-archetypes.md`.
2. Visual Style from information topology and density. Read `references/visual-styles.md`.
3. Story House from tone, brand constraints, and contrast. Read `references/palette-houses.md`.
4. Motion Patterns from what motion must communicate. Read `references/motion-patterns.md`.
5. Check the combination against `references/composition-matrix.md` and the registry.

Explicit user choices win unless they violate a hard contrast, compatibility, or render constraint. Unknown choices fail with valid alternatives instead of silently substituting a default.

## Reference study

When the direction comes from screenshots, GIFs, previous designs, or a public reference, `design-study` owns design-DNA diagnosis using `references/study-protocol.md`. The diagnosis maps reusable principles into local choices and never grants permission to copy source wording or distinctive assets.

## Capability ownership

The parent workflow coordinates focused workers and passes artifacts between them. Workers do not assume hidden peer delegation.

- `evidence-checker` owns claim provenance and blocked proof slots.
- `story-architect` owns the four-axis story contract.
- `palette-curator` owns Story House tokens and contrast verdicts.
- `copy-compressor` owns slot-sized visible copy and anti-slop compression.
- `layout-composer` owns information topology, design-taste gates, and structural fingerprints.
- `caption-writer` owns caption archetype and caption-specific copy rules.
- `artboard-builder` owns static execution of the approved layout.
- `motion-director` owns motion intent and pattern selection.
- `motion-engineer` owns seekable animation implementation.
- `render-qa` owns deterministic render evidence.
- `post-critic` owns adversarial copy, visual, motion, and fingerprint review.
- `story-verifier` owns evidence-backed final acceptance and the bounded repair loop.

The executable graph is tracked in `architecture/plugin-graph.json` and checked by `scripts/plugin_graph.py`.

## Hard constraints

- Keep one 1080x1350 artboard and the existing attribution footer contract.
- Text pairs declared by a Story House must meet 4.5:1 contrast.
- Use at most two motion patterns; every motion needs a reading, hierarchy, sequence, or state reason.
- Frame 0 remains a complete still.
- Never invent metrics, testimonials, proof, product facts, or source claims.
- A palette swap is not a new visual style. Structural choices must change when the story needs a different visual grammar.

## Independent verification

Before delivery, `story-verifier` uses `references/verification-loop.md`, reads artifacts directly, records evidence against stable criteria, and permits at most two targeted fix attempts before escalation.
