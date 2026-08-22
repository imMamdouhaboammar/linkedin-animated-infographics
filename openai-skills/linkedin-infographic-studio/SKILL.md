---
name: linkedin-infographic-studio
description: Create or redesign a static or animated LinkedIn infographic with evidence checks, verified identity sourcing, narrative taste, concept exploration, intentional typography, macro-layout planning, still-first visual critique, disciplined motion, and final verification. Use for full infographic creation in ChatGPT or Codex.
---

# LinkedIn Infographic Studio

## Purpose

Create feed-ready LinkedIn infographics with the same process discipline expected from a multi-role creative team while remaining self-contained inside an OpenAI skill package.

Quality parity with other hosts does not mean identical visual output. Choose the visual direction that best serves the specific story, then enforce the quality gates in this skill.

Before production, read these local references completely:

- `references/openai-runtime.md`
- `references/role-passes.md`
- `references/asset-source-policy.md`
- `references/narrative-taste.md`
- `references/typography-direction.md`
- `references/visual-archetypes.md`
- `references/copy-quality-contract.md`
- `references/visual-quality-contract.md`
- `references/motion-quality-contract.md`
- `references/visual-intelligence-capsule.json`

Read the generated visual-intelligence capsule before creative selection. It is the packaged reference context: apply its hard filters, fixed weights, and slug tie-break to choose mechanisms, then use only the selected mechanism guidance. With no visual reference, treat reference diagnosis as `SKIP`. If reference intent is explicit but supplied evidence cannot be inspected, return `HOLD: reference evidence unavailable` before evidence work. Persistent reference ingestion and source reference media are unavailable in this distribution; do not claim otherwise. The capsule provides abstract local guidance only.

When a repository checkout is actually available, `demos/` may be inspected as a bounded taste corpus under `references/narrative-taste.md`. The installed package does not pretend those demo media are present locally.

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
2. inspectable original-owner source with localized integrity record
3. pinned `https://github.com/imMamdouhaboammar/vibe-svgs` file under `svgs/logos/` for a platform/tool logo only
4. verified Lobe asset for supported named AI/tool identities after reading `https://lobehub.com/icons/skill.md`
5. `HOLD: verified identity asset required`

Vibe SVGs mascot/scene records marked `communityArtwork: true` are community/fan-made and must not be called official. They cannot satisfy an original/official mascot request. Use them only when the user explicitly accepts community artwork and the exact commit/path/blob/SHA-256 provenance is pinned.

Do not redraw, trace, reconstruct, prompt-generate, silently substitute, distort, or unapproved-recolor an identity. Final HTML must use a local or embedded copy instead of a remote identity URL.

## Typography standard

Apply `references/typography-direction.md` before copy fitting.

Use explicit user typography when render-safe, then supplied/local font assets, then a curated deterministic system direction. Allowed loading strategies are system, embedded, or local-file. Remote @import and render-time network font requests fail.

## Creative and narrative standard

The output must feel designed for this specific idea rather than assembled from a generic component library.

Before choosing a layout:

1. identify the useful relationship, tension, comparison, sequence, transformation, decision, proof, or reveal
2. read `references/narrative-taste.md` and choose a story shape before layout grammar
3. when references exist, deconstruct selected mechanisms through `Evidence -> Observation -> Transferable Rule -> Anti-Rule`
4. when multiple references exist, assign explicit jobs such as hook, progression, composition, type hierarchy, color, texture, proof, pacing, motion, or payoff instead of blending them indiscriminately
5. generate at least three meaningfully different creative directions
6. define one dominant visual anchor, containment strategy, and negative-space strategy for every direction
7. include an editorial low-containment direction when the story permits it
8. include a diagrammatic or relationship-led direction when a real relationship exists
9. choose an archetype from `references/visual-archetypes.md` or define a justified custom structure
10. select one direction based on comprehension, memorability, evidence fit, identity fit, narrative payoff, reference originality, and feed behavior
11. build a narrative contract with Reader question and Beat-to-visual mapping for every retained beat
12. define the macro layout only after the narrative contract is coherent

Repeated cards are valid when repeated units are the story. They are not the default wrapper for unrelated text. A list converted into cards is not a narrative.

Avoid automatic reliance on:

- nested cards
- decorative pills and badges
- fake dashboards
- repeated rounded rectangles for unrelated information
- tiny uppercase labels as a substitute for hierarchy
- excessive explanatory copy
- decorative 3D, glow, floating objects, or motion with no story job
- reference mimicry that copies a distinctive composition instead of transferring a general mechanism
- fan-made mascots presented as official identities

## Required workflow

Follow the role passes in `references/role-passes.md` in order.

### Phase 1: Evidence

Create an evidence inventory. Mark unsupported factual slots as blocked. Preserve exact user-supplied facts, names, numbers, terminology, and brand constraints.

### Phase 2: Verified identity assets

Create the asset plan before creative direction. Apply the full precedence and integrity rules in `references/asset-source-policy.md`. Record exact source provenance and local/embedded render disposition for every named identity. Identity-locked geometry, colors, wordmarks, and aspect ratio cannot drift downstream.

### Phase 3: Creative directions

Create at least three directions with different structural ideas, not three color variations. Each direction needs a visual hook, copy hook, useful payoff, story relationship, dominant anchor, structural archetype, containment strategy, negative-space strategy, approved identity roles, and motion job when animated.

When references exist, each direction also records selected reference jobs, transferable rules, and anti-rules. Never reuse distinctive subject matter, protected identity, proprietary artwork, or a unique layout signature from the reference.

Do not present three directions that all reduce to a headline plus repeated cards.

Choose the strongest direction and state why it fits the story.

### Phase 4: Narrative and story architecture

Apply `references/narrative-taste.md` before layout.

Define:

- one primary takeaway
- selected story shape
- hook
- ordered beats and reading order
- Reader question per beat
- evidence dependency per beat
- Beat-to-visual mapping per beat
- opening state
- tension/question
- turn/reveal/comparison logic
- final payoff/takeaway
- persistent context
- dominant visual anchor
- containment and negative-space requirements
- density target
- selected demo/reference jobs, transferable rules, anti-rules, and originality changes
- necessary motion jobs only

`Hook -> Tension -> Evidence -> Turn -> Payoff` is a useful default reasoning sequence when it fits, not a mandatory five-screen template.

A viewer should understand what the visual is about within two seconds, but the opening should still create a reason to continue.

### Phase 5: Palette

Resolve a restrained semantic palette with one clear accent and enough personality to feel deliberately designed. Preserve required brand colors without breaking contrast. Do not recolor an identity-locked logo/mascot unless its exact approved source provides that variant.

### Phase 6: Typography

Create a type spec with headline/body roles, optional mono role, loading strategy, fallbacks, role weights, minimum feed sizes, pairing reason, story fit, and render safety.

Do not proceed with a remote font dependency.

### Phase 7: Copy compression

Apply `references/copy-quality-contract.md`.

Write copy by visual slot and narrative beat. Remove repeated explanation before layout. Keep evidence-bearing language precise. Avoid generic thought-leadership filler and vague marketing language.

The visual must carry part of the argument. Do not make headline, subline, body, and takeaway all explain the same idea in different words. Fit copy to approved minimum type sizes rather than shrinking type to rescue dense copy.

### Phase 8: Macro layout and perception preflight

Create an explicit 1080x1350 layout specification before component styling.

Define major zones, proportional heights or bounding boxes, safe margins, alignment, visual anchor, verified identity placements, exact type roles, structural fingerprint, containment strategy, negative-space strategy, expected vertical occupancy, footer reservation, and containment depth.

Map narrative beats to spatial states without turning each beat into a card by default. State why the selected archetype fits the story relationship.

Then run every blocking perception check in `references/visual-quality-contract.md`: one primary focal anchor, one-second hierarchy, approximately 100x100 thumbnail, squint/blur value-mass, grayscale hierarchy, negative-space audit, edge/crop/tangency, brand-off specificity, and effect-subtraction.

A failing check must record evidence, consequence, and the smallest responsible dimension. Repair only that dimension before still construction. Do not reopen unrelated approved stages.

### Phase 9: Still construction

Build the static composition first. The still must communicate the useful idea without animation.

Build macro zones before cards, labels, icons, or micro-decoration. Preserve approved identity assets and type roles exactly.

When HTML is requested, keep the artboard deterministic and fixed at target dimensions. Use semantic HTML/CSS/SVG where appropriate. Preserve editable structure rather than flattening meaningful content prematurely.

### Phase 10: Still critique

Inspect the entire artboard at full size and feed scale.

Explicitly score the complete failure taxonomy from `references/visual-quality-contract.md`, including identity-source, identity-integrity, typography, clean-structure, narrative, and perception failures. Classify non-hard-gate craft defects as critical, major, or minor, calculate cumulative pressure, and include the smallest responsible dimension for each failed item.

Name the top three defects and repair only responsible dimensions. Re-check after repair. Do not proceed to motion while a blocking still defect remains.

Maximum two targeted repair attempts.

### Phase 11: Motion

For animated output, define the motion story before implementing it.

Each motion must explain reading order, change, travel, active state, or the narrative turn/payoff. Follow `references/motion-quality-contract.md`.

Do not compensate for weak static composition with more animation. Motion must not alter identity source, identity geometry/colors, or typography.

### Phase 12: Render and final critique

Inspect frame zero, strongest mid-state, final state, and loop seam when relevant.

Re-run the visual failure taxonomy, perception tests, identity-integrity checks, narrative readability, severity pressure, and motion checks. Verify footer clearance, clipping, feed-scale text, asset loads, font loads, pacing, and whether the primary visual relationship remains obvious.

### Phase 13: Final verification

Return one verdict:

- `PASS`
- `FAIL:fixable`
- `HOLD`

A PASS requires evidence integrity, verified identity provenance/integrity, render-safe typography, coherent narrative progression, a passing perception preflight, a passing still, visual-slop pressure below the blocking threshold, clean creative structure, passing visual critique, and passing motion/render checks when animated.

## Mandatory visual gates

Do not ship when any severe version of these is present:

- unverified or approximated named identity
- official mascot replaced by community/fan-made artwork
- mutable/unpinned identity provenance
- identity geometry/color/wordmark/aspect-ratio drift
- remote identity asset dependency
- remote font dependency
- silent font substitution
- generic headline plus unrelated cards
- narrative beats that do not change understanding
- top-heavy composition
- unexplained bottom dead space
- detached footer
- weak visual anchor
- weak macro rhythm
- excessive nested-card density
- generic UI grammar replacing real art direction
- feed-scale legibility failure
- failed blocking perception preflight
- motion on a weak still
- decorative motion dominating explanatory motion

## Delivery

Deliver the final visual artifact plus a concise summary of:

- selected creative direction
- primary takeaway and narrative shape
- visual archetype
- identity source/integrity summary when named identities are present
- typography direction
- narrative-gate verdict
- perception-preflight verdict
- still critique verdict and cumulative visual-slop pressure
- motion critique verdict when applicable
- final verification verdict

When the task also asks for a LinkedIn caption, keep it specific to the visual's actual insight and provide the first comment separately when a repository link or source belongs there.
