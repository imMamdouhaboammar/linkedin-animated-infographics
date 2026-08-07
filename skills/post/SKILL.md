---
name: post
description: >-
  Router for building a LinkedIn post as a caption plus a 1080x1350 static or looping
  infographic. Use when the user wants a LinkedIn post, animated infographic, GIF, system map,
  stack map, workflow diagram, cheat sheet, or wants source material turned into a LinkedIn
  visual. Start here even when the immediate ask is only a hook, visual direction, or motion.
---

# LinkedIn Animated Infographics

The core format is a complete static infographic with a small, deliberate motion footprint when animation adds meaning. Motion acts as a reading, route, hierarchy, or state signal. It does not compensate for weak information architecture.

## Pipeline

```text
topic -> Info-stories brief -> caption -> still -> motion -> render -> independent QA -> publish
```

Load only the skill needed for the current stage.

| Stage | Skill | Job |
|---|---|---|
| Composition | `linkedin-animated-infographics:info-stories` | resolve Story Archetype, Visual Style, Story House, Motion Patterns, and design dials |
| Caption | `linkedin-animated-infographics:caption` | write or edit the caption and enforce copy rules |
| Layout | `linkedin-animated-infographics:artboard` | execute the approved static composition |
| Motion | `linkedin-animated-infographics:motion` | implement seekable animation and loop rules |
| Mascots | `linkedin-animated-infographics:mascots` | add an optional character within the motion budget |
| Render | `linkedin-animated-infographics:render` | capture frames, assemble the GIF, and run render gates |
| Arabic | `linkedin-animated-infographics:arabic` | apply Arabic and bilingual layout behavior |

Three workflow skills run common end-to-end tasks: `linkedin-animated-infographics:new-post`, `linkedin-animated-infographics:render-gif`, and `linkedin-animated-infographics:qa-post`.

## Agents

| Agent | Give it |
|---|---|
| `design-study` | supplied visual references when their design DNA should inform a new direction |
| `story-architect` | topic, takeaway, CTA, explicit choices, and optional study report |
| `copy-compressor` | source material and target story slots when the artboard copy is too dense |
| `evidence-checker` | claims, names, metrics, and proof that must survive into the visual |
| `layout-composer` | approved story brief and compressed content blocks |
| `artboard-builder` | approved static layout spec and story brief |
| `motion-director` | approved still and story brief when output is animated |
| `motion-engineer` | approved still plus resolved Motion Patterns |
| `render-qa` | built artboard for render diagnostics |
| `story-verifier` | final artifact plus acceptance criteria and direct evidence |

## Non-negotiables

1. Exactly one `#artboard` element at `width:1080px; height:1350px`.
2. All animation is seekable CSS, WAAPI, or SMIL, shares one `--loop` or an integer division, and keeps frame 0 complete.
3. Fonts are system-safe or base64-embedded. Never `@import` a network font.
4. When Info-stories is active, colour comes from the resolved **Story House** token block. Do not silently replace it with House 0 or invent one-off colours. Legacy posts without a story brief may keep the existing House 0 default.
5. Declared text pairs meet 4.5:1 contrast and declared state pairs meet 3:1.
6. Nothing moves in the outer 48px margin.
7. A mascot replaces another pointer primitive rather than becoming a third competing motion.
8. No fabricated metrics, proof, testimonials, product facts, or source claims.

## Working method

1. Ask only what cannot be inferred: the one takeaway and CTA.
2. If references are supplied, study them before choosing a direction.
3. Resolve and approve the Info-stories brief before production.
4. Write the caption and compress artboard copy without weakening facts.
5. Build and approve the still before motion.
6. Add zero to two meaning-driven Motion Patterns.
7. Render, run existing QA, then run independent story verification.
8. Deliver the artifact, caption, first comment, resolved four-axis selection, and render numbers when applicable.

## Setup

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh
```

The registry and validation tools run on plain Python 3. Browser rendering additionally needs the Playwright browser and its operating-system libraries.
