---
name: new-post
description: Run the complete evidence-to-delivery workflow for a static or animated LinkedIn infographic, including verified identity sourcing, creative concepting, typography direction, story architecture, production, critique, and independent verification.
disable-model-invocation: true
argument-hint: "[topic or URL] [optional: --arabic] [optional: --mascot]"
---

# /linkedin-animated-infographics:new-post

Topic: **$ARGUMENTS**

## Purpose

Run the canonical parent workflow for a complete LinkedIn infographic. The workflow owns routing, user approvals, HOLD resolution, targeted repair loops, and final delivery. Workers return bounded artifacts here and never coordinate peer workers directly.

Read `helper/GUIDE.md` before execution. Treat `helper/router.json`, `helper/capabilities.json`, `helper/quality-gates.json`, `helper/artifacts.json`, `research/capability-notes/gates.json`, and `architecture/plugin-graph.json` as machine-readable contracts.

## Use when

Use this workflow when the user wants a complete new infographic or a substantial redesign that should proceed from source/evidence through verified assets, concept, type, copy, artboard, optional motion, QA, and delivery.

Use focused skills instead when the request is only a render, only QA, only mascot animation, only a design study, or only publishing an already verified demo.

## Inputs

- topic, source material, URL, files, or user-provided facts
- intended audience and one primary takeaway when they cannot be inferred safely
- desired CTA when applicable
- language and static/animated output preference
- optional visual references
- optional brand/UI assets
- optional exact official identity assets or named AI/tool identities that may resolve through Lobe
- explicit typography requirements when present

## Outputs

The parent workflow may produce:

- `build/design-study.json`
- `build/evidence.json`
- `build/asset-plan.json`
- `build/creative-concepts.json`
- `build/story-brief.json`
- `build/palette-check.json`
- `build/type-spec.json`
- `build/artboard-copy.json`
- `build/layout-spec.json`
- `build/caption.md`
- `build/first-comment.md`
- `build/post.html`
- `build/still.png`
- `build/motion-direction.json` for animated output
- `build/mascot/motion-contract.json` when a mascot is active
- `build/render-report.json`
- `build/critic-report.json`
- `build/verification-report.json`
- final static/GIF artifact plus resolved story and validation summary

## Procedure

### 0. Route and conditional gates

Resolve the request through the helper. Apply local quality gates and research gates before production.

If Arabic/RTL is active, load the `arabic` skill before copy or layout work.

If a named or official mascot is requested, record `build/mascot-request.json`. The identity is not allowed to bypass the verified identity path. Exact user/task SVG assets keep priority; supported AI/tool identities may resolve from Lobe; unresolved named identities HOLD.

### 1. Reference diagnosis

Consume `reference_diagnosis` from the helper before evidence inventory:

- `SKIP`: no reference was supplied; do not invoke `design-study`.
- `HOLD`: explicit reference intent has no usable `reference_evidence`; stop before `evidence-checker` with `HOLD: reference evidence unavailable`.
- `READY`: invoke `design-study` as the first worker and save `build/design-study.json`. Activate `reference-dna` and study reusable structure, hierarchy, rhythm, density, type roles, and motion grammar without cloning distinctive work.

Downstream workers receive only the selected mechanism IDs and the focused stage context from `build/design-study.json`, never the full reference library or raw reference media.

### 2. Evidence inventory

Delegate to `evidence-checker`. Save `build/evidence.json` with protected claims, metrics, product states, named identities, logos, proof, and unsupported slots. Unsupported proof is blocked before creative/copy/layout production.

### 3. Verified identity asset plan

Delegate to `asset-curator`. Save `build/asset-plan.json`.

Apply `verified-identity-assets` and `skills/info-stories/references/asset-source-policy.md`. Exact user-supplied official assets win. For supported named AI/tool identities, the worker reads `https://lobehub.com/icons/skill.md` and follows the current Lobe instructions. Final production assets must be local or embedded. If a named identity cannot be verified, stop with `HOLD: verified identity asset required` instead of generating a lookalike.

### 4. Creative concept directions

Delegate to `creative-director` with the evidence record, asset plan, optional design study, audience, language, output mode, and approved constraints. Save `build/creative-concepts.json`.

Require at least three meaningfully different directions. Every direction contains a visual hook, copy hook, aha mechanic, story relationship, dominant visual anchor, structure/archetype, containment strategy, negative-space strategy, motion job, evidence dependencies, risk notes, and why it earns attention.

Apply `hooked-design-copy`, `creative-payoff`, and `clean-creative-structure`. When the story permits, include an editorial low-containment option. When a real relationship exists, include a diagrammatic or relationship-led option. Repeated cards are valid only when repeated units are the story.

The parent workflow selects or approves one direction before story architecture.

### 5. Story contract

Delegate to `story-architect` with the selected concept, evidence, optional design study, one takeaway, CTA, language, and output mode. Save `build/story-brief.json` with Story House, Visual Style, Story Archetype, Motion Patterns, design dials, clean-structure requirements, and execution bridge.

### 6. Palette contract

Delegate to `palette-curator`. Save `build/palette-check.json`.

The plugin default is `creative-attractive-restrained`: use an engaging, memorable, harmonious palette without exaggerated saturation, unnecessary neon, or competing accents unless the approved brief explicitly calls for them. Text/state contrast floors remain blocking.

### 7. Typography contract

Delegate to `type-curator`. Save `build/type-spec.json`.

Apply `intentional-typography` and `skills/info-stories/references/typography-direction.md`. User-specified typography wins when render-safe, followed by supplied/bundled local assets, then a curated deterministic system direction. Remote @import or another render-time font request is blocking.

### 8. Artboard copy

Delegate to `copy-compressor` with evidence, selected concept, type spec, story brief, and target slots. Save `build/artboard-copy.json`. The hero and attention-bearing story openers must use evidence-safe hooks; literal labels remain literal where clarity wins. Copy must fit the type-spec minimum feed sizes without silent font substitution.

### 9. Static layout specification

Delegate to `layout-composer`. Save `build/layout-spec.json` with zone order, proportions, visual anchor, component counts, structural fingerprint, clean-structure requirements, verified asset placements, exact type roles, alignment mode, and any exception reason.

Use `center-first` for the primary visual anchor and major story zones. A non-centered alignment requires a recorded comprehension/fidelity reason such as tables, UI mockups, code/terminal surfaces, timelines, Arabic/RTL flow, or reference-DNA fidelity.

### 10. Caption

Delegate to `caption-writer`. Save `build/caption.md` and `build/first-comment.md`. The opening hook must be specific and evidence-safe. Show the caption and selected story direction for approval before still construction when interactive approval is available.

### 11. Still construction

Delegate to `artboard-builder` with the approved story, asset plan, type spec, palette, copy, layout, and caption artifacts. It returns `build/post.html` and `build/still.png` after source, typography, and static checks. Show the still as the visual approval gate when interaction is available.

### 12. Motion direction

For animated output, delegate to `motion-director` with the approved still, selected concept, story brief, layout spec, and mascot role when applicable. Save `build/motion-direction.json`. Static output records this stage as skipped.

### 13. Mascot component when active

After still construction and before motion implementation, delegate the verified identity SVG to `mascot-animator`. The source may be exact user/task input or a verified Lobe asset already copied locally by `asset-curator`. Save identity and rig evidence plus `build/mascot/motion-contract.json`. The verified SVG remains the identity source.

### 14. Motion implementation

For animated output, delegate to `motion-engineer` with the approved still, story brief, motion direction, and mascot contract when present. It returns the animated `build/post.html`. Static output skips this stage.

### 15. Render mechanics and QA

Delegate to `render-qa`. Save `build/render-report.json`. A render HOLD returns control to this parent workflow for a targeted fix and re-run.

### 16. Adversarial review

Delegate to `post-critic` with the artifact, caption, evidence, asset plan, type spec, selected concept, layout, mascot identity notes when present, and render report. Save `build/critic-report.json`.

The critic explicitly evaluates `hooked-design-copy`, `creative-payoff`, `clean-creative-structure`, `verified-identity-assets`, `intentional-typography`, `restrained-palette`, and `center-first-composition` in addition to applicable research gates.

### 17. Independent acceptance

Delegate to `story-verifier`. Save `build/verification-report.json`. The verifier reads artifacts directly, including identity provenance and typography. `FAIL:fixable` may trigger a targeted fix and re-check. Maximum two targeted repair attempts; a third unresolved failure escalates.

### 18. Deliver

Deliver the final artifact, caption, first comment, resolved Info-stories choices, selected creative concept, identity source summary, type direction, render numbers when applicable, active gate summary, and final verification verdict.

### 19. Share with the community (optional)

Offer community sharing only when the final verification verdict is `PASS` and delivery is complete.

Ask one concise opt-in question: `Share this demo with the community?`

If the user explicitly accepts, transfer control to the focused parent workflow `share-demo`. That workflow owns publication metadata, rights confirmation, public-export preflight, source-prompt consent, packaging, and delegation to `community-publisher` for fork/branch/commit/push/PR mechanics.

If the user declines or gives no answer, stop with no GitHub write. Do not repeat the offer or infer consent from the fact that the user created the demo.

If `share-demo` later returns a HOLD, preserve the already delivered artifact and report only the publication blocker. A publication HOLD does not invalidate the completed post.

## HOLD conditions

Stop and return a precise HOLD when any blocking production requirement is unresolved, including:

- missing verified identity asset for a named AI/tool/logo/mascot
- Lobe coverage cannot be verified for a required supported identity
- final identity asset is remote-only instead of local/embedded
- typography depends on a remote font request or cannot meet feed-scale legibility
- unsupported factual proof, metric, product state, logo, or claim
- hook or aha concept depends on invented evidence
- selected concept fails `clean-creative-structure`
- failing contrast or Story House compatibility
- unresolved blocking local quality gate
- unresolved blocking research gate
- render evidence unavailable when required
- third unresolved verification failure after two targeted repair attempts

The optional community-sharing stage does not create a production HOLD when the user declines or gives no answer. If the user opts in, publication-specific HOLD conditions are owned by `share-demo`.

Do not fill missing inputs with plausible content.

## Related components

- helper: `helper/GUIDE.md`
- router: `helper/router.json`
- local gates: `helper/quality-gates.json`
- artifacts: `helper/artifacts.json`
- executable graph: `architecture/plugin-graph.json`
- identity source policy: `skills/info-stories/references/asset-source-policy.md`
- typography policy: `skills/info-stories/references/typography-direction.md`
- creative copy reference: `skills/info-stories/references/hook-driven-design-copy.md`
- design defaults: `skills/info-stories/references/design-taste-gates.md`
- focused QA: `qa-post`
- focused render: `render-gif`
- optional community publisher: `share-demo`

## Research gates

Complete post creation may activate `prose-specificity`, `voice-preservation`, `design-dials`, `structural-originality`, `reference-dna`, `contrast-discipline`, `evidence-traceability`, and `bounded-verification` according to `research/capability-notes/gates.json`.

The final safety gates include identity provenance, typography render safety, `evidence-traceability`, and `bounded-verification`. They remain active even when the chosen creative direction is intentionally simple. The optional `share-demo` workflow inherits the final PASS as a publication prerequisite.
