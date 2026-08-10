---
name: artboard
description: Choose and execute the static 1080x1350 infographic composition, including hierarchy, verified identity assets, intentional typography, Story House tokens, center-first alignment, UI surfaces, contrast, and feed-scale legibility before motion.
---

# Artboard

## Purpose

Build or evaluate the approved static infographic composition before animation. The still is the visual approval gate and the base artifact consumed by motion and render workers.

Read `helper/GUIDE.md` before choosing structure. When Info-stories is active, the resolved Story House, Visual Style, Story Archetype, creative concept, verified asset plan, type spec, and layout spec are authoritative inputs.

## Use when

Use for selecting a static visual archetype, executing cards/panels/routes/UI mockups, applying approved identity assets and typography, building `build/post.html`, or checking whether a still is ready for motion.

## Inputs

- selected creative concept when present
- `build/story-brief.json`
- `build/asset-plan.json`
- `build/type-spec.json`
- `build/palette-check.json`
- `build/artboard-copy.json`
- `build/layout-spec.json`
- optional caption, UI evidence, mascot-zone requirement, and brand assets

## Outputs

Return or support generation of `build/post.html`, `build/still.png`, asset/type confirmations, structural/fidelity notes, visual default compliance, and any blocking render/layout finding to the parent workflow.

## Procedure

1. Read `references/visual-archetypes.md`, `references/design-systems.md`, `../info-stories/references/asset-source-policy.md`, and `../info-stories/references/typography-direction.md`.
2. Choose or execute structure from the content shape. Existing archetypes include Directory Map, Pipeline Stages, Orbit Cycle, Flow Map + Verdict, Logo Grid, Trading Card Grid, Node Tree, Terminal Card, Cheat Sheet Poster, Spec Sheet, Annotated Blueprint, Character Flowchart, and Specimen Grid.
3. When Info-stories is active, use the resolved Story House token block. Do not silently replace it with legacy House 0. Legacy work without a story brief may still use the existing House 0 fallback.
4. Apply `clean-creative-structure`. Preserve the chosen dominant anchor, relationship, containment strategy, and negative-space strategy. Do not flatten an editorial or diagrammatic concept into a repeated card set.
5. Apply `verified-identity-assets`. Named AI/tool identities must come from exact user-supplied or approved Lobe records in `build/asset-plan.json`. Use a local/embedded copy in final HTML and preserve identity lock.
6. Apply `intentional-typography`. Use the exact approved type roles and fallbacks from `build/type-spec.json`. Allowed loading strategies are system, embedded, or local-file. Remote @import and render-time font requests fail.
7. Apply the plugin-local palette default `creative-attractive-restrained`. Keep the palette memorable and harmonious, with a clear accent and enough personality to feel designed. Avoid exaggerated saturation, unnecessary neon, and competing accents unless the approved brief explicitly requires them.
8. Apply `center-first` composition to the primary visual anchor and major zones. Use a documented alignment exception only for content that benefits from it, including tables, UI mockups, code/terminal surfaces, timelines, Arabic/RTL reading flow, or reference-DNA fidelity.
9. Build macro zones first, then hierarchy, approved relationship/card/connector/UI grammar, then attribution. One zone gets one reading job.
10. For UI stories, read `skills/info-stories/references/ui-mockup-rules.md`. Preserve evidence-qualified product states and feed-width legibility. Concept UI must remain identifiable when it could be mistaken for real product evidence.
11. Keep exactly one `#artboard` at `1080x1350`, render-safe fonts, mandatory attribution, and load-bearing text at or above the existing feed-scale floor.
12. Enforce text contrast of at least 4.5:1 and the existing state-pair floor. Use the resolved semantic tokens rather than arbitrary one-off colors.
13. When the composition names an official product, use the vendor's own mark rather than a redrawn one. Resolve it from the pinned upstream set and inline the result:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/brand_icon.py list --query claude
python3 ${CLAUDE_PLUGIN_ROOT}/tools/brand_icon.py fetch claude --variant color
```

The set covers AI and LLM brands only. When a named platform is not in it, that is a HOLD on the artwork, not a licence to approximate: keep the literal product name or ask for the exact SVG. If only some members of a zone have a real mark, use literal names for the whole zone rather than shipping a half-branded row, and record which rule applied. Full contract in `docs/brand-icons.md`.

14. Run the static checks:

```bash
python3 tools/asset_policy_check.py build/asset-plan.json
python3 tools/type_spec_check.py build/type-spec.json
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_render.py build/post.html --out build/still.png
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_render.py build/post.html --mobile
```

15. Inspect the rendered still at feed width. Confirm visual anchor, clean structure, identity fidelity, typography, alignment decision, structural fingerprint, footer clearance, UI readability, and restrained palette character.

## HOLD conditions

Return a HOLD when contrast fails, the selected Story House/style combination is incompatible, a named identity is unresolved or remote-only, the type spec requires remote loading or becomes unreadable at feed width, the layout needs unsupported factual/product UI, a required asset is missing, center-first is overridden without a defensible reason, or the still is unreadable at feed width.

## Related components

- routing authority: `helper/GUIDE.md`
- local quality gates: `helper/quality-gates.json`
- design defaults: `skills/info-stories/references/design-taste-gates.md`
- identity assets: `skills/info-stories/references/asset-source-policy.md`
- typography: `skills/info-stories/references/typography-direction.md`
- UI fidelity: `skills/info-stories/references/ui-mockup-rules.md`
- structural check: `tools/fingerprint_check.py`
- identity check: `tools/asset_policy_check.py`
- typography check: `tools/type_spec_check.py`
- contrast check: `tools/contrast_check.py`
- official brand marks: `tools/brand_icon.py`, `docs/brand-icons.md`
- worker: `agents/artboard-builder.md`

## Research gates

Apply `structural-originality` and `contrast-discipline` on every Info-stories artboard. Apply `reference-dna` when a visual reference drives the layout. Evidence-bearing UI and named identity assets inherit `evidence-traceability`.
