# Design-taste gates

Taste is checked against the story job, not against a generic website aesthetic. These gates are adapted for fixed 1080x1350 LinkedIn artboards.

## Pre-emit critique

Score 1-5 before production on six axes: **Purpose, Hierarchy, Execution, Specificity, Restraint, Variety**. Any score below 3 sends the composition back for one targeted revision.

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
- Card count follows content count; do not create empty decorative cells
- Repetition is allowed when it improves comparison, but the full page must not become one repeated card template
- Shape choices follow a rule; mixed radii need an explicit role distinction
- Section hues, supporting colours, and accent roles stay token-driven
- No arbitrary colour values or type families appear halfway through a build
- A dense story earns density through hierarchy, not smaller text
- Real screenshots stay real screenshots; a diagrammatic terminal must be labelled and styled as an illustration rather than presented as captured UI
- Do not fabricate proof bars, metrics, logos, or testimonials because the selected style has a slot for them

## Motion taste

Every motion must answer one of four questions: what should I read next, what changed, where did this item travel, or which state is active? If none applies, leave it static. Existing motion-budget and seam rules remain authoritative.

## Rules deliberately not imported

Responsive-site navigation, forms, dark-mode parity, React/Tailwind conventions, Core Web Vitals, and mandatory scroll animation are outside this fixed-artboard skill.
