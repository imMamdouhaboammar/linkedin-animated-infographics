---
name: artboard
description: Choose and execute the static 1080x1350 infographic composition, including hierarchy, Story House tokens, center-first alignment, UI surfaces, contrast, and feed-scale legibility before motion.
---

# Artboard

## Purpose

Build or evaluate the approved static infographic composition before animation. The still is the visual approval gate and the base artifact consumed by motion and render workers.

Read `helper/GUIDE.md` before choosing structure. When Info-stories is active, the resolved Story House, Visual Style, Story Archetype, creative concept, and layout spec are authoritative inputs.

## Use when

Use for selecting a static visual archetype, executing cards/panels/routes/UI mockups, applying typography and spacing, building `build/post.html`, or checking whether a still is ready for motion.

## Inputs

- selected creative concept when present
- `build/story-brief.json`
- `build/palette-check.json`
- `build/artboard-copy.json`
- `build/layout-spec.json`
- optional caption, UI evidence, exact mascot-zone requirement, and brand assets

## Outputs

Return or support generation of `build/post.html`, `build/still.png`, structural/fidelity notes, visual default compliance, and any blocking render/layout finding to the parent workflow.

## Procedure

1. Read `references/visual-archetypes.md` and `references/design-systems.md`.
2. Choose or execute structure from the content shape. Existing archetypes include Directory Map, Pipeline Stages, Orbit Cycle, Flow Map + Verdict, Logo Grid, Trading Card Grid, Node Tree, Terminal Card, Cheat Sheet Poster, Spec Sheet, Annotated Blueprint, Character Flowchart, and Specimen Grid.
3. When Info-stories is active, use the resolved Story House token block. Do not silently replace it with legacy House 0. Legacy work without a story brief may still use the existing House 0 fallback.
4. Apply the plugin-local palette default `creative-attractive-restrained`. Keep the palette memorable and harmonious, with a clear accent and enough personality to feel designed. Avoid exaggerated saturation, unnecessary neon, and competing accents unless the approved brief explicitly requires them.
5. Apply `center-first` composition to the primary visual anchor and major zones. Use a documented alignment exception only for content that benefits from it, including tables, UI mockups, code/terminal surfaces, timelines, Arabic/RTL reading flow, or reference-DNA fidelity.
6. Build macro zones first, then hierarchy, cards/connectors/UI, then attribution. One zone gets one reading job.
7. For UI stories, read `skills/info-stories/references/ui-mockup-rules.md`. Preserve evidence-qualified product states and feed-width legibility. Concept UI must remain identifiable when it could be mistaken for real product evidence.
8. Keep exactly one `#artboard` at `1080x1350`, system-safe or embedded fonts, mandatory attribution, and load-bearing text at or above the existing feed-scale floor.
9. Enforce text contrast of at least 4.5:1 and the existing state-pair floor. Use the resolved semantic tokens rather than arbitrary one-off colors.
10. When the composition names an official product, use the vendor's own mark rather than a redrawn one. Resolve it from the pinned upstream set and inline the result:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/brand_icon.py list --query claude
python3 ${CLAUDE_PLUGIN_ROOT}/tools/brand_icon.py fetch claude --variant color
```

The set covers AI and LLM brands only. When a named platform is not in it, that is a HOLD on the artwork, not a licence to approximate: keep the literal product name or ask for the exact SVG. If only some members of a zone have a real mark, use literal names for the whole zone rather than shipping a half-branded row, and record which rule applied. Full contract in `docs/brand-icons.md`.

11. Run the static checks:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_render.py build/post.html --out build/still.png
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_render.py build/post.html --mobile
```

12. Inspect the rendered still at feed width. Confirm visual anchor, alignment decision, structural fingerprint, footer clearance, UI readability, and restrained palette character.

## HOLD conditions

Return a HOLD when contrast fails, the selected Story House/style combination is incompatible, the layout needs unsupported factual/product UI, a required asset is missing, center-first is overridden without a defensible reason, or the still is unreadable at feed width.

## Related components

- routing authority: `helper/GUIDE.md`
- local quality gates: `helper/quality-gates.json`
- design defaults: `skills/info-stories/references/design-taste-gates.md`
- UI fidelity: `skills/info-stories/references/ui-mockup-rules.md`
- structural check: `tools/fingerprint_check.py`
- contrast check: `tools/contrast_check.py`
- official brand marks: `tools/brand_icon.py`, `docs/brand-icons.md`
- worker: `agents/artboard-builder.md`

## Research gates

Apply `structural-originality` and `contrast-discipline` on every Info-stories artboard. Apply `reference-dna` when a visual reference drives the layout. Evidence-bearing UI also inherits `evidence-traceability`.
