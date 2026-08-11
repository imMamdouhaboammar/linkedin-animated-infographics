---
name: new-post
description: Run the complete evidence-to-delivery workflow for a static or animated LinkedIn infographic, including creative concepting, story architecture, production, critique, and independent verification.
disable-model-invocation: true
argument-hint: "[topic or URL] [optional: --arabic] [optional: --mascot]"
---

# /linkedin-animated-infographics:new-post

Topic: **$ARGUMENTS**

## Purpose

Run the canonical parent workflow for a complete LinkedIn infographic. The workflow owns routing, user approvals, HOLD resolution, targeted repair loops, and final delivery. Workers return bounded artifacts here and never coordinate peer workers directly.

Read `helper/GUIDE.md` before execution. Treat `helper/router.json`, `helper/capabilities.json`, `helper/quality-gates.json`, `helper/artifacts.json`, `research/capability-notes/gates.json`, and `architecture/plugin-graph.json` as machine-readable contracts.

## Use when

Use this workflow when the user wants a complete new infographic or a substantial redesign that should proceed from source/evidence through concept, copy, artboard, optional motion, QA, and delivery.

Use focused skills instead when the request is only a render, only QA, only mascot animation, only a design study, or only publishing an already verified demo.

## Inputs

- topic, source material, URL, files, or user-provided facts
- intended audience and one primary takeaway when they cannot be inferred safely
- desired CTA when applicable
- language and static/animated output preference
- optional visual references
- optional brand/UI assets
- exact SVG when a named or official mascot is requested

## Outputs

The parent workflow may produce:

- `build/design-study.json`
- `build/evidence.json`
- `build/creative-concepts.json`
- `build/story-brief.json`
- `build/palette-check.json`
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

### 0. Route and asset gates

Resolve the request through the helper. Apply local quality gates and research gates before production.

If the user names a specific or official mascot, require the exact user-supplied or task-attached SVG. Record `build/mascot-request.json` and validate it with `scripts/mascot_contract.py check`. Never redraw, approximate, substitute, or silently generate a lookalike.

If Arabic/RTL is active, load the `arabic` skill before copy or layout work.

### 1. Reference diagnosis

Consume `reference_diagnosis` from the helper before evidence inventory:

- `SKIP`: no reference was supplied; do not invoke `design-study`.
- `HOLD`: explicit reference intent has no usable `reference_evidence`; stop before `evidence-checker` with `HOLD: reference evidence unavailable`.
- `READY`: invoke `design-study` as the first worker and save `build/design-study.json`. Activate `reference-dna` and study reusable structure, hierarchy, rhythm, density, and motion grammar without cloning distinctive work.

Downstream workers receive only the selected mechanism IDs and the focused stage context from `build/design-study.json`, never the full reference library or raw reference media.

### 2. Evidence inventory

Delegate to `evidence-checker`. Save `build/evidence.json` with protected claims, metrics, product states, logos, proof, and unsupported slots. Unsupported proof is blocked before creative/copy/layout production.

### 3. Creative concept directions

Delegate to `creative-director` with the evidence record, optional design study, audience, language, output mode, and approved constraints. Save `build/creative-concepts.json`.

Require at least three meaningfully different directions. Every direction contains a visual hook, copy hook, aha mechanic, story shape, recommended style/archetype/motion behavior, evidence dependencies, risk notes, and why it earns attention. At least one direction must contain a useful visual payoff or aha moment through a reveal, relationship, comparison, transformation, state change, or interaction. Spectacle without a story job does not count.

Apply `hooked-design-copy` and `creative-payoff`. The parent workflow selects or approves one direction before story architecture.

### 4. Story contract

Delegate to `story-architect` with the selected concept, evidence, optional design study, one takeaway, CTA, language, and output mode. Save `build/story-brief.json` with Story House, Visual Style, Story Archetype, Motion Patterns, design dials, and execution bridge.

### 5. Palette contract

Delegate to `palette-curator`. Save `build/palette-check.json`.

The plugin default is `creative-attractive-restrained`: use an engaging, memorable, harmonious palette without exaggerated saturation, unnecessary neon, or competing accents unless the approved brief explicitly calls for them. Text/state contrast floors remain blocking.

### 6. Artboard copy

Delegate to `copy-compressor` with evidence, selected concept, story brief, and target slots. Save `build/artboard-copy.json`. The hero and attention-bearing story openers must use evidence-safe hooks; literal labels remain literal where clarity wins.

### 7. Static layout specification

Delegate to `layout-composer`. Save `build/layout-spec.json` with zone order, proportions, visual anchor, component counts, structural fingerprint, assets, alignment mode, and any exception reason.

Use `center-first` for the primary visual anchor and major story zones. A non-centered alignment requires a recorded comprehension/fidelity reason such as tables, UI mockups, code/terminal surfaces, timelines, Arabic/RTL flow, or reference-DNA fidelity.

### 8. Caption

Delegate to `caption-writer`. Save `build/caption.md` and `build/first-comment.md`. The opening hook must be specific and evidence-safe. Show the caption and selected story direction for approval before still construction when interactive approval is available.

### 9. Still construction

Delegate to `artboard-builder` with the approved story, palette, copy, layout, and caption artifacts. It returns `build/post.html` and `build/still.png` after static checks. Show the still as the visual approval gate when interaction is available.

### 10. Motion direction

For animated output, delegate to `motion-director` with the approved still, selected concept, story brief, layout spec, and mascot role when applicable. Save `build/motion-direction.json`. Static output records this stage as skipped.

### 11. Mascot component when active

After still construction and before motion implementation, delegate the validated exact SVG to `mascot-animator`. Save identity and rig evidence plus `build/mascot/motion-contract.json`. The supplied SVG remains the identity source.

### 12. Motion implementation

For animated output, delegate to `motion-engineer` with the approved still, story brief, motion direction, and mascot contract when present. It returns the animated `build/post.html`. Static output skips this stage.

### 13. Render mechanics and QA

Delegate to `render-qa`. Save `build/render-report.json`. A render HOLD returns control to this parent workflow for a targeted fix and re-run.

### 14. Adversarial review

Delegate to `post-critic` with the artifact, caption, evidence, selected concept, layout, mascot identity notes when present, and render report. Save `build/critic-report.json`.

The critic must explicitly evaluate `hooked-design-copy`, `creative-payoff`, `restrained-palette`, and `center-first-composition` in addition to applicable research gates.

### 15. Independent acceptance

Delegate to `story-verifier`. Save `build/verification-report.json`. The verifier reads artifacts directly. `FAIL:fixable` may trigger a targeted fix and re-check. Maximum two targeted repair attempts; a third unresolved failure escalates.

### 16. Deliver

Deliver the final artifact, caption, first comment, resolved Info-stories choices, selected creative concept, render numbers when applicable, active gate summary, and final verification verdict.

### 17. Share with the community (optional)

Offer community sharing only when the final verification verdict is `PASS` and delivery is complete.

Ask one concise opt-in question: `Share this demo with the community?`

If the user explicitly accepts, transfer control to the focused parent workflow `share-demo`. That workflow owns publication metadata, rights confirmation, public-export preflight, source-prompt consent, packaging, and delegation to `community-publisher` for fork/branch/commit/push/PR mechanics.

If the user declines or gives no answer, stop with no GitHub write. Do not repeat the offer or infer consent from the fact that the user created the demo.

If `share-demo` later returns a HOLD, preserve the already delivered artifact and report only the publication blocker. A publication HOLD does not invalidate the completed post.

## HOLD conditions

Stop and return a precise HOLD when any blocking production requirement is unresolved, including:

- missing exact SVG for a named or official mascot
- unsupported factual proof, metric, product state, logo, or claim
- hook or aha concept that depends on invented evidence
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
- creative copy reference: `skills/info-stories/references/hook-driven-design-copy.md`
- design defaults: `skills/info-stories/references/design-taste-gates.md`
- focused QA: `qa-post`
- focused render: `render-gif`
- optional community publisher: `share-demo`

## Research gates

Complete post creation may activate `prose-specificity`, `voice-preservation`, `design-dials`, `structural-originality`, `reference-dna`, `contrast-discipline`, `evidence-traceability`, and `bounded-verification` according to `research/capability-notes/gates.json`.

The two final safety gates are `evidence-traceability` and `bounded-verification`; they remain active even when the chosen creative direction is intentionally simple. The optional `share-demo` workflow inherits the final PASS as a publication prerequisite.
