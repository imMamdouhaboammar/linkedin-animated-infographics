---
name: linkedin-infographic-studio
description: Create or redesign a static or animated LinkedIn infographic with evidence checks, verified identity sourcing, concept exploration, intentional typography, macro-layout planning, still-first visual critique, disciplined motion, and final verification. Use for full infographic creation in ChatGPT or Codex.
---

# LinkedIn Infographic Studio

## Purpose

Create feed-ready LinkedIn infographics with the same process discipline expected from a multi-role creative team while remaining self-contained inside an OpenAI skill package.

Quality parity with other hosts does not mean identical visual output. Choose the visual direction that best serves the specific story, then enforce the quality gates in this skill.

Before production, read these local references completely:

- `references/openai-runtime.md`
- `references/role-passes.md`
- `references/asset-source-policy.md`
- `references/typography-direction.md`
- `references/visual-archetypes.md`
- `references/copy-quality-contract.md`
- `references/visual-quality-contract.md`
- `references/motion-quality-contract.md`

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
- optional brand assets or named AI/tool identities
- explicit typography requirements when supplied

Do not invent missing evidence, product states, metrics, testimonials, logos, integrations, identities, or claims.

## Identity standard

For named official AI/tool identities, apply `references/asset-source-policy.md` before concepting.

Precedence:

1. exact user-supplied official asset
2. verified Lobe asset for supported named AI/tool identities after reading `https://lobehub.com/icons/skill.md`
3. `HOLD: verified identity asset required`

Do not redraw or prompt-generate an official lookalike. Final HTML must use a local or embedded copy instead of a remote identity URL.

## Typography standard

Apply `references/typography-direction.md` before copy fitting.

Use explicit user typography when render-safe, then supplied/local font assets, then a curated deterministic system direction. Allowed loading strategies are system, embedded, or local-file. Remote @import and render-time network font requests fail.

## Creative standard

The output must feel designed for this specific idea rather than assembled from a generic component library.

Before choosing a layout:

1. identify the useful relationship, tension, comparison, sequence, transformation, or reveal
2. generate at least three meaningfully different creative directions
3. define one dominant visual anchor, containment strategy, and negative-space strategy for every direction
4. include an editorial low-containment direction when the story permits it
5. include a diagrammatic or relationship-led direction when a real relationship exists
6. choose an archetype from `references/visual-archetypes.md` or define a justified custom structure
7. select one direction based on comprehension, memorability, evidence fit, identity fit, and feed behavior
8. define the macro layout before writing detailed HTML/CSS

Repeated cards are valid when repeated units are the story. They are not the default wrapper for unrelated text.

Avoid automatic reliance on:

- nested cards
- decorative pills and badges
- fake dashboards
- repeated rounded rectangles for unrelated information
- tiny uppercase labels as a substitute for hierarchy
- excessive explanatory copy
- decorative 3D, glow, floating objects, or motion with no story job

## Required workflow

Follow the role passes in `references/role-passes.md` in order.

### Phase 1: Evidence

Create an evidence inventory. Mark unsupported factual slots as blocked. Preserve exact user-supplied facts, names, numbers, terminology, and brand constraints.

### Phase 2: Verified identity assets

Create the asset plan before creative direction. Apply the exact user asset then Lobe then HOLD precedence. Record exact source provenance and local/embedded render disposition for every named identity.

### Phase 3: Creative directions

Create at least three directions with different structural ideas, not three color variations. Each direction needs a visual hook, copy hook, useful payoff, story relationship, dominant anchor, structural archetype, containment strategy, negative-space strategy, and motion job when animated.

Do not present three directions that all reduce to a headline plus repeated cards.

Choose the strongest direction and state why it fits the story.

### Phase 4: Story architecture

Define:

- one primary takeaway
- reading order
- visual anchor
- opening state
- useful reveal
- final takeaway
- containment and negative-space requirements
- density target

A viewer should understand what the visual is about within two seconds.

### Phase 5: Palette

Resolve a restrained semantic palette with one clear accent and enough personality to feel deliberately designed. Preserve required brand colors without breaking contrast.

### Phase 6: Typography

Create a type spec with headline/body roles, optional mono role, loading strategy, fallbacks, role weights, minimum feed sizes, pairing reason, story fit, and render safety.

Do not proceed with a remote font dependency.

### Phase 7: Copy compression

Apply `references/copy-quality-contract.md`.

Write copy by visual slot. Remove repeated explanation before layout. Keep evidence-bearing language precise. Avoid generic thought-leadership filler and vague marketing language.

The visual must carry part of the argument. Do not make the headline, subline, body, and takeaway all explain the same idea in different words. Fit copy to the approved minimum type sizes rather than shrinking type to rescue dense copy.

### Phase 8: Macro layout

Create an explicit 1080x1350 layout specification before component styling.

Define the major zones, proportional heights or bounding boxes, safe margins, alignment, visual anchor, verified identity placements, exact type roles, structural fingerprint, containment strategy, negative-space strategy, expected vertical occupancy, footer reservation, and containment depth.

State why the selected archetype fits the story relationship.

Apply every blocking rule in `references/visual-quality-contract.md`.

### Phase 9: Still construction

Build the static composition first. The still must communicate the useful idea without animation.

Build macro zones before cards, labels, icons, or micro-decoration. Preserve approved identity assets and type roles exactly.

When HTML is the requested production format, keep the artboard deterministic and fixed at the target dimensions. Use semantic HTML/CSS/SVG where appropriate. Preserve editable structure rather than flattening meaningful content prematurely.

### Phase 10: Still critique

Inspect the entire artboard at full size and feed scale.

Explicitly score the complete failure taxonomy from `references/visual-quality-contract.md`, including identity-source, typography, and clean-structure failures.

Name the top three defects and repair them. Re-check after repair. Do not proceed to motion while a blocking still defect remains.

Maximum two targeted repair attempts.

### Phase 11: Motion

For animated output, define the motion story before implementing it.

Each motion must explain reading order, change, travel, or active state. Follow `references/motion-quality-contract.md`.

Do not compensate for weak static composition with more animation. Motion must not alter identity source or typography.

### Phase 12: Render and final critique

Inspect frame zero, the strongest mid-state, the final state, and the loop seam when relevant.

Re-run the visual failure taxonomy and motion checks. Verify footer clearance, clipping, feed-scale text, asset loads, font loads, pacing, and whether the primary visual relationship remains obvious.

### Phase 13: Final verification

Return one verdict:

- `PASS`
- `FAIL:fixable`
- `HOLD`

A PASS requires evidence integrity, verified identity provenance, render-safe typography, a passing still, clean creative structure, a passing visual critique, and passing motion/render checks when animated.

## Mandatory visual gates

Do not ship when any severe version of these is present:

- unverified or approximated named identity
- remote identity asset dependency
- remote font dependency
- silent font substitution
- generic headline plus unrelated cards
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
- identity source summary when named identities are present
- typography direction
- still critique verdict
- motion critique verdict when applicable
- final verification verdict

When the task also asks for a LinkedIn caption, keep it specific to the visual's actual insight and provide the first comment separately when a repository link or source belongs there.
