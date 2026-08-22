# Design-taste gates

Taste is checked against the story job, not against a generic website aesthetic. These gates are adapted for fixed 1080x1350 LinkedIn artboards.

## Plugin-local visual defaults

These defaults are local product choices, not claims imported from the research sources.

- Palette character: `creative-attractive-restrained`. Prefer memorable, harmonious color combinations with a clear accent and enough personality to feel designed. Avoid exaggerated saturation, unnecessary neon, or multiple competing accents unless the brief explicitly requires them.
- Composition alignment: `center-first`. Center the primary infographic content, visual anchor, and major story zones by default so the page reads as one deliberate composition rather than a loose document layout.
- Identity sourcing: `Lobe-first` for supported named AI/tool identities after exact user-supplied official assets. Read `asset-source-policy.md`; unresolved named identities HOLD instead of being approximated.
- Typography: `intentional typography`. Read `typography-direction.md`; user-specified or supplied fonts take precedence and the final capture must not depend on remote font loading.
- An alignment exception is allowed when the content structure requires it, including tables, UI mockups, code or terminal surfaces, timelines, Arabic/RTL reading flow, or a documented reference-DNA decision.
- An exception must improve comprehension or fidelity, not merely introduce asymmetry for decoration.

## Pre-emit critique

Score 1-5 before production on seven axes: **Purpose, Hierarchy, Execution, Specificity, Restraint, Variety, Cleanliness**. Any score below 3 sends the composition back for one targeted revision.

`Cleanliness` means the story uses the minimum containment and decoration needed to make its dominant relationship obvious. It does not mean visually empty or generic.

## Perception preflight

Run this after the macro layout is defined and before still construction. The purpose is to test whether the composition works perceptually before component styling or motion can hide structural defects.

- **Primary-anchor rule:** exactly one primary focal anchor must carry the first visual beat. Three or more equal-emphasis anchors fail because the eye has no clear entry point.
- **one-second hierarchy test:** at a one-second glance, identify the hook, primary anchor, and takeaway without reading every supporting line.
- **Thumbnail test:** inspect at approximately **100x100** pixels. The dominant silhouette and hierarchy must survive.
- **squint / blur value-mass test:** blur or mentally squint at the page and confirm the main value masses still form the intended reading path.
- **grayscale hierarchy test:** remove color as a cue. Hierarchy must still be carried by scale, placement, spacing, and value contrast.
- **negative-space audit:** distinguish active negative space that frames or separates meaning from accidental dead space produced by weak distribution.
- **edge, crop, and tangency test:** eliminate accidental tangency, ambiguous edge kisses, weak overlaps, and crops that look unintentional.
- **brand-off specificity test:** temporarily ignore logos and brand marks. The composition should still feel specific to this story rather than like a generic dashboard or template.
- **effect-subtraction test:** mentally remove glow, shadows, 3D, texture, decorative particles, and non-explanatory motion. If the concept disappears with the effects, the structure is too weak.

A failed perception check routes only the failing dimension back for revision. Do not restart evidence, asset sourcing, typography, or another already-approved dimension without evidence that it is responsible.

## Reference transfer protocol

When a reference exists, do not copy it and do not blend several references into one vague mood. Deconstruct each relevant mechanism with this exact sequence:

`Evidence -> Observation -> Transferable Rule -> Anti-Rule`

- **Evidence:** describe what is visibly present without interpretation.
- **Observation:** identify the structural, typographic, color, pacing, texture, or motion pattern.
- **Transferable Rule:** turn the observation into a general design decision that can serve the new story.
- **Anti-Rule:** record what must not be copied, over-applied, or mistaken for a universal rule.

When multiple references exist, assign non-overlapping jobs such as composition, typography hierarchy, color harmony, texture/finish, illustration treatment, pacing, or motion. A reference may hold more than one job only when the jobs are explicitly named and do not erase the other references. Never copy distinctive subject matter, identity, proprietary artwork, or a unique layout signature.

## Clean creative structure

Every concept records:

- the relationship being visualized
- one dominant visual anchor
- structural archetype
- containment strategy
- negative-space strategy
- motion job when animated

When the story permits it, include at least one editorial low-containment direction. When a real relationship exists, include at least one diagrammatic or relationship-led direction.

Repeated cards are valid when repeated units, specimens, states, or categories are the story. They are not the default wrapper for unrelated text.

Reject:

- generic headline plus unrelated cards
- repeated rounded containers used because they are easy to code
- palette-only reskins
- decorative 3D, glow, floating objects, or motion without a communication job
- density created by shrinking text instead of editing copy/structure
- arbitrary asymmetry that weakens reading order

## Structural fingerprint

Record six fields for every composed story:

1. `zone_topology` - grid, layered stack, flow, sequence, mosaic, catalogue, etc.
2. `card_grammar` - equal cards, mixed-span panels, terminal plus notes, open rows, nested lanes, etc.
3. `divider` - rule, negative space, colour band, connector, or none
4. `visual_anchor` - headline, terminal, diagram, screenshot, number, mascot, or another single anchor
5. `density` - sparse, medium, dense
6. `motion_grammar` - static, sequential highlight, route, reveal, terminal type, etc.

When a previous brief is supplied, change at least two structural axes. Changing only Story House colours fails. Use `validate_fingerprint()` in `scripts/info_stories.py`.

## Composition gates

- One visual anchor must dominate in two seconds at feed scale
- Every zone has one reading job
- Start center-first, then use a documented alignment exception only when the content benefits
- Preserve the selected clean-structure relationship and negative-space strategy
- Card count follows content count; do not create empty decorative cells
- Repetition is allowed when it improves comparison, but the full page must not become one repeated card template
- Shape choices follow a rule; mixed radii need an explicit role distinction
- Section hues, supporting colours, and accent roles stay token-driven
- No arbitrary colour values or type families appear halfway through a build
- Keep palette character creative-attractive-restrained and avoid exaggerated saturation unless specifically briefed
- Preserve the approved type spec; solve density through editing before type reduction
- A dense story earns density through hierarchy, not smaller text
- Real screenshots stay real screenshots; a diagrammatic terminal must be labelled and styled as an illustration rather than presented as captured UI
- Do not fabricate proof bars, metrics, logos, testimonials, or identity assets because the selected style has a slot for them

## Visual-slop pressure

Named hard gates remain blocking on their own. For additional craft defects, record severity and cumulative pressure instead of treating every note as equivalent.

- `critical`: blocks immediately
- `major`: pressure 3
- `minor`: pressure 1

Block when there is any critical finding, **two or more major** findings, **four or more minor** findings, or **cumulative pressure** of 6 or more. The aggregate score never cancels a hard-gate failure.

Every finding must include visible evidence, its consequence at feed scale, and the **smallest responsible dimension** that can repair it.

## Targeted revision routing

Route the repair to the smallest responsible dimension and preserve approved upstream work:

- concept/message -> creative direction
- hierarchy/composition/negative space -> layout composition
- typography -> type curation
- Arabic/RTL -> Arabic direction when active
- brand/identity -> asset or brand owner
- copy density -> copy compression
- motion -> motion direction/implementation
- render/runtime -> render QA

Retry from the last approved artifact for that dimension. Do not chain a revision onto a known-bad visual state when it would compound drift, and do not restart the complete pipeline merely because one local dimension failed.

## Motion taste

Every motion must answer one of four questions: what should I read next, what changed, where did this item travel, or which state is active? If none applies, leave it static. Existing motion-budget and seam rules remain authoritative.

## Rules deliberately not imported

Responsive-site navigation, forms, dark-mode parity, React/Tailwind conventions, Core Web Vitals, and mandatory scroll animation are outside this fixed-artboard skill.
