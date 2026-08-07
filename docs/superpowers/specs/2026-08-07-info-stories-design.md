# Info-stories design

Date: 2026-08-07
Repository: `linkedin-animated-infographics`
Status: approved for implementation

## Goal

Add an Info-stories layer that lets a user choose or infer four independent creative dimensions:

1. Story House: colour palette and token roles
2. Visual Style: page composition and component language
3. Story Archetype: narrative shape and information order
4. Motion Pattern: deterministic animation behavior

The feature must extend the current artboard, motion, render, mascot, Arabic, and QA pipeline rather than replace it

## Success criteria

- A user can request an infographic by goal or select named Info-stories options explicitly
- The router can infer a safe combination when options are omitted
- New houses pass contrast rules before render
- New visual styles map onto the existing 1080x1350 artboard contract
- Motion remains seekable, deterministic, loop-safe, and compatible with current render scripts
- Existing skills and workflows keep working without migration
- New agents and tools expose narrow responsibilities and can be tested independently
- The system supports adding new houses, styles, archetypes, and motion patterns without editing every agent
## Architecture options considered

### Option A: parallel Info-stories stack

Create new artboard, motion, render, and QA skills dedicated to Info-stories

Pros: isolated naming and fast experimentation
Cons: duplicates current rendering rules, creates two sources of truth, and raises maintenance cost

### Option B: orchestration layer over current skills

Add Info-stories as a routing and reference layer while extending existing artboard and motion references with named registries

Pros: reuses proven capture and QA behavior, avoids duplicated rules, and keeps old commands valid
Cons: requires careful boundaries so the new router does not become a large catch-all file

### Option C: replace existing artboard taxonomy with Info-stories

Rename the current houses and archetypes and make Info-stories the only public model

Pros: simplest public vocabulary after migration
Cons: breaks existing prompts, docs, agents, and examples for little functional gain

## Decision

Use Option B

Info-stories becomes the composition model and current skills remain the execution model
The design keeps each axis independent so a new palette does not require a new layout or motion implementation
## Public model

### Story Houses

Initial registry:

- Ember Paper
- Clay Ledger
- Sage Ledger
- Lilac Brief
- Mist Board
- Sand Quartz
- Midnight Operator
- Graphite Glow
- Coral Terminal
- Navy Grid

Each house defines semantic tokens rather than arbitrary swatches: background, surface, ink, ink-2, muted, line, accent, accent-deep, and optional supporting hues
Every text pair must meet the existing 4.5:1 rule and every state-defining boundary must meet 3:1 where applicable

### Visual Styles

Initial registry:

- Signal Sheet
- Funnel Board
- Stack Ledger
- Command Canvas
- Sequence Board
- Comparison Grid
- Proof Mosaic
- Tool Catalog
- Story Strip
- Field Guide
### Story Archetypes

Initial registry:

- One Prompt, Full Workflow
- From Raw Input to Final Output
- The 30-Day Breakdown
- Inside the Stack
- What Each Piece Actually Does
- Build It Once, Reuse It Often
- The Working Screen
- Step-by-Step Playbook
- Decision Cards
- Ecosystem Snapshot
- Before / After Workflow
- Framework in One Page

Each archetype defines content zones, required beats, optional beats, density guidance, and compatible visual styles
It does not own colour or animation

### Motion Patterns

Initial registry:

- Sequential Highlight
- Connector Draw
- Node Pulse
- Active Route Swap
- Card Reveal
- Type-On Terminal
- Soft Zoom Focus
- Spotlight Sweep
- Chip / Badge Pulse
- Float Micro-Motion

The current motion skill remains authoritative for timing, seekability, loop closure, and motion budget
## Agents

Add focused agents and keep current execution agents intact

- `story-architect`: selects or validates archetype, style, house, density, and output mode
- `palette-curator`: validates named house tokens and contrast pairs
- `layout-composer`: translates visual style plus archetype into the existing artboard contract
- `motion-director`: selects compatible motion patterns before handing execution to `motion-engineer`
- `copy-compressor`: reduces source material into headline, subline, section, card, proof, and CTA chunks
- `evidence-checker`: checks names, numbers, claims, and source notes

Existing `artboard-builder`, `motion-engineer`, `render-qa`, and `post-critic` stay as execution and QA roles

## Skills and references

Add `skills/info-stories/SKILL.md` as the public router with references:

- `palette-houses.md`
- `visual-styles.md`
- `story-archetypes.md`
- `motion-patterns.md`
- `layout-rules.md`
- `composition-matrix.md`

The skill must point to existing artboard and motion references for shared rules instead of copying them

## Tools

First release should include deterministic utilities only:

- `palette_preview.py`: list or render semantic house tokens
- `contrast_check.py`: calculate WCAG ratios for named token pairs
- `story_scaffold.py`: emit a structured story brief from selected dimensions
- `composition_check.py`: reject incompatible style, archetype, and motion combinations

Render and GIF utilities remain where they are
## Data flow

1. Intake supplies topic, source material, takeaway, CTA, language, and optional Info-stories choices
2. `story-architect` resolves missing dimensions and returns a compact story brief
3. `copy-compressor` shapes content to the selected archetype and density target
4. `palette-curator` resolves house tokens and validates required contrast pairs
5. `layout-composer` maps story zones to a compatible existing or new template
6. `artboard-builder` builds and validates the still using the current artboard contract
7. `motion-director` selects one primary and at most one secondary pattern
8. `motion-engineer` implements motion using the current seekable primitive rules
9. `render-qa` runs the existing render and mobile gates
10. `post-critic` checks the final communication before delivery

Explicit user selections win unless they violate a hard constraint
When a combination is incompatible, the router must name the conflict and suggest the nearest compatible option instead of silently substituting

## Composition rules

- Story House, Visual Style, Story Archetype, and Motion Pattern are independent registries with stable slugs
- Registries use human names for prompts and slugs for tools
- A visual style declares compatible archetypes and preferred existing artboard archetypes
- A story archetype declares required information beats and density range
- A motion pattern declares compatible visual structures and whether it can be primary or secondary
- Static posts use the same story and style registries with motion set to `none`
- Arabic remains a layout variant handled by the existing Arabic skill, not a separate Info-stories style
- Mascots remain optional and must obey the current mascot budget and QA gates
## Error handling

- Unknown house, style, archetype, or motion slug fails with valid choices
- Missing optional choices are inferred from content shape and output mode
- Contrast failures identify the exact foreground/background pair and measured ratio
- Unsupported composition fails before HTML generation
- A requested motion pattern that cannot seek or close is rejected before render
- Tools return non-zero exit codes for invalid input and write diagnostics to stderr
- No tool mutates an existing artboard unless explicitly given an output path

## Testing strategy

Add focused tests before implementation for each utility and registry behavior

1. Registry tests confirm unique slugs, required fields, and no duplicate public names
2. Palette tests verify all declared text pairs against the 4.5:1 floor
3. Composition tests cover accepted and rejected style/archetype/motion combinations
4. Scaffold tests verify deterministic output for the same inputs
5. CLI tests verify useful errors for unknown slugs and missing required arguments
6. Integration smoke test routes one light editorial story and one dark terminal story into valid briefs
7. Existing render and lint tests remain the regression gate

## Scope for first implementation

Build the full registries and routing contract, but only add new HTML templates where current templates cannot represent a visual style cleanly
Do not rewrite the GIF capture pipeline
Do not create a second QA pipeline
Do not migrate existing examples in the first pass
Do not add external runtime dependencies for registry or validation tools

## Documentation impact

Update README with the Info-stories model, available houses/styles/archetypes, and one selection example
Update the main post router so it can invoke Info-stories before the existing caption and artboard stages
Document extension rules so contributors can add one registry item without editing unrelated files