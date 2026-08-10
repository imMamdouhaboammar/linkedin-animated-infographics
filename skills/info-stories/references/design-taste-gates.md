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

## Motion taste

Every motion must answer one of four questions: what should I read next, what changed, where did this item travel, or which state is active? If none applies, leave it static. Existing motion-budget and seam rules remain authoritative.

## Rules deliberately not imported

Responsive-site navigation, forms, dark-mode parity, React/Tailwind conventions, Core Web Vitals, and mandatory scroll animation are outside this fixed-artboard skill.
