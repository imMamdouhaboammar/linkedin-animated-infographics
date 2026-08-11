---
name: linkedin-infographic-studio
description: Create or redesign a static or animated LinkedIn infographic with evidence checks, concept exploration, art-direction selection, macro-layout planning, still-first visual critique, disciplined motion, and final verification. Use for full infographic creation in ChatGPT or Codex.
---

# LinkedIn Infographic Studio

## Purpose

Create feed-ready LinkedIn infographics with the same process discipline expected from a multi-role creative team while remaining self-contained inside an OpenAI skill package.

Quality parity with other hosts does not mean identical visual output. Choose the visual direction that best serves the specific story, then enforce the quality gates in this skill.

Before production, read these local references completely:

- `references/openai-runtime.md`
- `references/role-passes.md`
- `references/visual-archetypes.md`
- `references/copy-quality-contract.md`
- `references/visual-quality-contract.md`
- `references/motion-quality-contract.md`
- `references/visual-intelligence-capsule.json`

Read the generated visual-intelligence capsule before creative selection. It is the only packaged reference context: apply its hard filters, fixed weights, and slug tie-break to choose mechanisms, then use only the selected mechanism guidance. With no visual reference, treat reference diagnosis as `SKIP`. If reference intent is explicit but the supplied evidence cannot be inspected, return `HOLD: reference evidence unavailable` before evidence work. Persistent reference ingestion and source reference media are unavailable in this distribution; do not claim otherwise. The capsule provides abstract local guidance only.

## Use when

Use this skill when the user asks to create, redesign, animate, critique, or materially improve a LinkedIn infographic and the task includes more than one production stage.

For a finished visual review, start at the still/final critique stages instead of rebuilding automatically.

## Inputs

Collect or infer only what can be inferred safely:

- topic, source material, files, URLs, or protected facts
- audience
- one primary takeaway
- desired CTA when relevant
- language
- static or animated output
- optional visual references
- optional brand assets
- exact user-provided identity assets when a named official mascot or logo must be preserved

Do not invent missing evidence, product states, metrics, testimonials, logos, integrations, or claims.

## Creative standard

The output must feel designed for this specific idea rather than assembled from a generic component library.

Before choosing a layout:

1. identify the useful relationship, tension, comparison, sequence, transformation, or reveal
2. generate at least three meaningfully different creative directions
3. choose an archetype from `references/visual-archetypes.md` or define a justified custom structure
4. select one direction based on comprehension, memorability, evidence fit, and feed behavior
5. define the macro layout before writing detailed HTML/CSS

Avoid automatic reliance on:

- nested cards
- decorative pills and badges
- fake dashboards
- repeated rounded rectangles for unrelated information
- tiny uppercase labels as a substitute for hierarchy
- excessive explanatory copy
- decorative motion with no story job

## Required workflow

Follow the role passes in `references/role-passes.md` in order.

### Phase 1: Evidence

Create an evidence inventory. Mark unsupported factual slots as blocked. Preserve exact user-supplied facts, names, numbers, terminology, and brand constraints.

### Phase 2: Creative directions

Create at least three directions with different structural ideas, not three color variations. Each direction needs a visual hook, copy hook, useful payoff, story shape, visual archetype, and motion idea when animated.

Do not present three directions that all reduce to a headline plus repeated cards.

Choose the strongest direction and state why it fits the story.

### Phase 3: Story architecture

Define:

- one primary takeaway
- reading order
- visual anchor
- opening state
- useful reveal
- final takeaway
- density target

A viewer should understand what the visual is about within two seconds.

### Phase 4: Copy compression

Apply `references/copy-quality-contract.md`.

Write copy by visual slot. Remove repeated explanation before layout. Keep evidence-bearing language precise. Avoid generic thought-leadership filler and vague marketing language.

The visual must carry part of the argument. Do not make the headline, subline, body, and takeaway all explain the same idea in different words.

### Phase 5: Macro layout

Create an explicit 1080x1350 layout specification before component styling.

Define the major zones, proportional heights or bounding boxes, safe margins, alignment, visual anchor, structural fingerprint, expected vertical occupancy, footer reservation, and containment depth.

State why the selected archetype fits the story relationship.

Apply every blocking rule in `references/visual-quality-contract.md`.

### Phase 6: Still construction

Build the static composition first. The still must communicate the useful idea without animation.

Build macro zones before cards, labels, icons, or micro-decoration.

When HTML is the requested production format, keep the artboard deterministic and fixed at the target dimensions. Use semantic HTML/CSS/SVG where appropriate. Preserve editable structure rather than flattening meaningful content prematurely.

### Phase 7: Still critique

Inspect the entire artboard at full size and feed scale.

Explicitly score the complete failure taxonomy from `references/visual-quality-contract.md`.

Name the top three defects and repair them. Re-check after repair. Do not proceed to motion while a blocking still defect remains.

Maximum two targeted repair attempts.

### Phase 8: Motion

For animated output, define the motion story before implementing it.

Each motion must explain reading order, change, travel, or active state. Follow `references/motion-quality-contract.md`.

Do not compensate for weak static composition with more animation.

### Phase 9: Render and final critique

Inspect frame zero, the strongest mid-state, the final state, and the loop seam when relevant.

Re-run the visual failure taxonomy and motion checks. Verify footer clearance, clipping, feed-scale text, pacing, and whether the primary visual relationship remains obvious.

### Phase 10: Final verification

Return one verdict:

- `PASS`
- `FAIL:fixable`
- `HOLD`

A PASS requires evidence integrity, a passing still, a passing visual critique, and passing motion/render checks when animated.

## Mandatory visual gates

Do not ship when any severe version of these is present:

- top-heavy composition
- unexplained bottom dead space
- detached footer
- weak visual anchor
- weak macro rhythm
- excessive nested-card density
- generic UI grammar replacing real art direction
- feed-scale legibility failure
- motion on a weak still
- decorative motion dominating explanatory motion

## Delivery

Deliver the final visual artifact plus a concise summary of:

- selected creative direction
- primary takeaway
- visual archetype
- still critique verdict
- motion critique verdict when applicable
- final verification verdict

When the task also asks for a LinkedIn caption, keep it specific to the visual's actual insight and provide the first comment separately when a repository link or source belongs there.
