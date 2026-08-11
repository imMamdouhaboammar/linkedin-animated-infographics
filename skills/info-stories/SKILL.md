---
name: info-stories
description: Resolve the infographic story contract across Story House, Visual Style, Story Archetype, Motion Patterns, creative concept, UI story behavior, and evidence-safe design choices before HTML production.
---

# Info-stories

## Purpose

Turn source material into a structured infographic story before HTML is built. Info-stories sits above the existing artboard, caption, motion, mascot, Arabic, render, and QA skills and keeps composition decisions deterministic and inspectable.

Read `helper/GUIDE.md` first. The merged registry returned by `scripts/info_stories.py::load_catalog()` is authoritative.

## Use when

Use when choosing the narrative shape, visual grammar, Story House, motion behavior, UI mockup story, reference-informed direction, or deterministic story brief for a LinkedIn infographic.

## Inputs

- evidence-safe source material
- selected `build/creative-concepts.json` direction when available
- optional `build/design-study.json`
- audience, takeaway, CTA, language, and output mode
- explicit user choices for any registry axis
- optional UI, brand, mascot, or reference constraints

## Outputs

Return or support creation of `build/story-brief.json` with Story House, Visual Style, Story Archetype, Motion Patterns, design dials, execution bridge, structural fingerprint inputs, and rationale for every resolved axis.

## Procedure

1. Validate the merged registry:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/info_stories.py check
```

2. Base options live in `catalog.json`; first-party extension families and curated visual mechanisms live in `extensions/*.json`. They are merged deterministically by filename.
3. When a complete workflow is running, consume the selected concept from `creative-director` before resolving the story. Preserve its visual hook, copy hook, and aha mechanic unless evidence or compatibility gates require a change.
4. Resolve Story Archetype from the narrative job using `references/story-archetypes.md`.
5. Resolve Visual Style from information topology and density using `references/visual-styles.md`.
6. Resolve Story House from tone, brand constraints, and contrast using `references/palette-houses.md`.
7. Resolve Motion Patterns from what motion must communicate using `references/motion-patterns.md`.
8. Check combinations against `references/composition-matrix.md` and the merged registry. Explicit user choices win unless they violate a hard compatibility, contrast, evidence, or render constraint.
9. Apply `creative-attractive-restrained` as the palette character default and `center-first` as the composition default. Alignment exceptions require a real comprehension/fidelity reason.
10. Apply `hooked-design-copy` and `creative-payoff`. Attention-bearing copy needs a real hook, and the story should contain a useful visual payoff or aha mechanism rather than a generic headline-plus-cards treatment.
11. UI Mockup Stories are first-class. Use `UI Storyboard` or `Interface Cutaway` with `references/ui-mockup-rules.md`. Dedicated archetypes include `Screen to Outcome`, `Inside the Interface`, and `State Change Story`; dedicated motion includes `Cursor Focus` and `State Transition`.
12. When visual references exist, `design-study` uses `references/study-protocol.md` to extract reusable design DNA without cloning distinctive work.
13. A named official mascot uses the exact user-supplied/task-attached SVG and the mascot path; missing SVG holds that path.

## Deterministic mechanism retrieval

Use the public retrieval tool when a stage needs focused visual reference context:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/story_retrieve.py --query path/to/query.json
```

The query object accepts `story_jobs`, `content_shape` (or `content_shapes` for multiple shapes), `output_mode`, `language`, `density`, `evidence_mode`, optional `reference_ids`, `top_k`, `byte_budget`, and one stage: `concept`, `story`, `palette-type`, `layout`, `motion`, or `review`. Output mode, language, density, evidence mode, and content shape are hard filters. Ranking then uses fixed weighted overlap with slug tie-breaking; it does not use embeddings or model ranking.

The tool writes one compact JSON capsule within the measured UTF-8 byte budget. Each stage receives only its relevant mechanism fields. Reference selection is bounded to one structural primary plus at most one motion and one typography secondary, each with an explicit influence axis. Treat adopted traits as abstract guidance; rejected traits, source copy, logos, people, screenshots, and signature illustrations remain blocked unless separately verified for the current brief.

## HOLD conditions

Return a HOLD when a requested registry choice is unknown or incompatible, contrast fails, UI evidence is insufficient for a real-product story, a creative payoff depends on unsupported facts, a named official mascot lacks its exact SVG, or a visual reference cannot be used without copying distinctive work.

Unknown choices should fail with valid alternatives rather than silently substituting a default.

## Related components

- routing authority: `helper/GUIDE.md`
- local quality gates: `helper/quality-gates.json`
- creative copy: `references/hook-driven-design-copy.md`
- design defaults: `references/design-taste-gates.md`
- UI mockups: `references/ui-mockup-rules.md`
- reference study: `references/study-protocol.md`
- verification: `references/verification-loop.md`
- executable graph: `architecture/plugin-graph.json`
- deterministic tools: `scripts/info_stories.py`, `tools/story_retrieve.py`, `tools/story_scaffold.py`, `tools/composition_check.py`, `tools/palette_preview.py`, `tools/contrast_check.py`, `tools/fingerprint_check.py`, `tools/copy_slop_check.py`

Capability owners include `creative-director`, `evidence-checker`, `story-architect`, `palette-curator`, `copy-compressor`, `layout-composer`, `caption-writer`, `artboard-builder`, `motion-director`, `mascot-animator`, `motion-engineer`, `render-qa`, `post-critic`, and `story-verifier` through the parent workflow.

## Research gates

Use `design-dials`, `structural-originality`, and `contrast-discipline` for normal story composition. Add `reference-dna` when visual references are supplied, `evidence-traceability` for product/proof claims, `prose-specificity` and `voice-preservation` for visible copy, and `bounded-verification` before delivery.
