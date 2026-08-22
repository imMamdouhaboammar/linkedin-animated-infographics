# Role passes

Each role pass has one job. Complete the pass and record its bounded output before moving on.

## 1. Evidence editor

Input: user prompt, source material, URLs, files, brand assets.

Output:
- protected facts and claims
- numbers, names, product states, logos, and proof that must stay accurate
- unsupported slots that must not be invented
- language and audience constraints

Block creative claims that require unavailable evidence.

## 2. Asset curator

Input: evidence inventory, exact user-supplied assets, and named AI/tool identities required by the brief.

Read `asset-source-policy.md`.

Output a verified identity asset plan. Apply this precedence:
- exact user-supplied official asset
- Lobe for supported named AI/tool identities after reading `https://lobehub.com/icons/skill.md`
- HOLD when no verified source exists

Record exact provenance and require local/embedded render disposition. Never generate an official lookalike.

## 3. Creative director

Input: evidence inventory, approved asset plan, audience, desired output mode, optional reference diagnosis.

When references are active, deconstruct every selected mechanism using:

`Evidence -> Observation -> Transferable Rule -> Anti-Rule`

For multiple references, assign explicit non-overlapping jobs such as composition, type hierarchy, color, texture, pacing, or motion. Do not blend all references into one mood and do not copy distinctive subject matter, identity, proprietary artwork, or unique layout signatures.

Output at least three meaningfully different creative directions. Each direction must include:
- visual hook
- copy hook
- useful reveal or relationship
- story shape
- relationship being visualized
- dominant visual anchor
- recommended visual archetype
- containment strategy
- negative-space strategy
- motion behavior and its story job when animated
- evidence dependencies
- reference jobs, transferable rules, and anti-rules when references exist
- risk notes

Apply clean creative structure. Include an editorial low-containment option when the story permits it. Include a diagrammatic or relationship-led option when a real relationship exists. Repeated cards are valid only when repetition is the story.

Reject three directions that are only palette changes of the same layout.

## 4. Story architect

Input: selected direction and evidence.

Output:
- one primary takeaway
- reading order
- opening state
- reveal or comparison logic
- closing takeaway
- dominant visual anchor
- containment and negative-space requirements
- density target
- intended emotional tone without exaggerated marketing language

Preserve the selected concept's clean structural relationship rather than converting it into generic cards.

## 5. Palette curator

Input: story architecture and brand constraints.

Output:
- background
- primary text
- secondary text
- primary accent
- optional secondary accent with a defined semantic job
- state colors only when needed

Use a distinctive but restrained palette. Do not use multiple decorative accents to create interest.

## 6. Type curator

Input: story architecture, palette, optional reference diagnosis, language, and explicit user font requirements.

Read `typography-direction.md`.

Output:
- direction name
- headline family
- body family
- optional mono family
- loading strategy
- fallbacks
- weights and minimum feed sizes
- pairing reason
- story fit
- render safety

Use user-specified type when render-safe, then supplied/local assets, then a curated deterministic system direction. Remote @import and render-time network font requests fail.

## 7. Copy compressor

Input: evidence, selected direction, story architecture, and approved type spec.

Output copy by slot, not as a paragraph dump. Prioritize one idea per zone. Remove repeated explanation. Preserve mechanism, evidence, useful specificity, and the minimum feed sizes implied by the type spec.

## 8. Layout composer and perception preflight

Input: story architecture, asset plan, type spec, copy slots, and palette.

Output an explicit macro-layout specification before HTML or styling details:
- canvas: 1080x1350
- safe margins
- headline zone
- primary visual-anchor zone
- supporting evidence/story zone
- takeaway zone
- footer zone
- zone bounding boxes or proportional heights
- verified identity asset placements
- exact type roles
- alignment choice and reason
- structural fingerprint
- containment strategy
- negative-space strategy
- expected vertical occupancy
- maximum containment depth

Do not solve layout by immediately creating cards around every text block. Preserve the selected clean structure.

Before still construction, run the blocking perception preflight from `visual-quality-contract.md`:
- one primary focal anchor
- one-second hierarchy test
- approximately 100x100 thumbnail test
- squint/blur value-mass test
- grayscale hierarchy test
- negative-space audit
- edge/crop/tangency test
- brand-off specificity test
- effect-subtraction test

Record PASS/FAIL, evidence, consequence, and smallest responsible dimension for each failure. Repair only the failing dimension and preserve unrelated approved work.

## 9. Still builder

Input: approved layout specification, passing perception preflight, asset plan, type spec, and copy.

Output a complete still-capable HTML artboard. Build macro zones first, then typography, verified assets, visual relationship, details, and attribution.

The still must communicate the useful idea with animation disabled. Final identity assets and fonts must be local, embedded, or system-safe rather than network-dependent.

## 10. Still critic

Input: rendered or directly inspected still plus asset/type specs.

Output the top three visual defects, their severity, pressure, smallest responsible dimension, and exact repair actions. Apply every blocking rule in `visual-quality-contract.md`, including identity provenance, typography, clean structure, balance, rhythm, visual anchor, content distribution, generic visual patterns, and the full perception preflight against the actual render.

Hard gates block independently. Additional craft findings use critical/major/minor severity and cumulative pressure. Do not return PASS when the aggregate blocking thresholds in the visual-quality contract are reached.

## 11. Motion director

Input: passing still and story architecture.

Output a motion plan that states what each motion explains. Every animation must answer at least one question:
- what should I read next?
- what changed?
- where did this item travel?
- which state is active?

## 12. Motion implementer

Input: passing still and motion plan.

Output deterministic motion that preserves the approved layout, identity assets, and typography. Do not redesign the composition while animating it.

## 13. Render QA

Input: animated or static artifact.

Output:
- frame-zero completeness
- clipping/overflow verdict
- footer clearance
- feed-scale legibility
- identity-asset load verdict
- font-load verdict
- animation seam verdict
- motion pacing verdict
- reduced-motion or static fallback notes when relevant

## 14. Adversarial visual critic

Input: final render plus evidence, asset plan, and type spec.

Re-run the visual failure taxonomy, perception preflight, severity pressure, clean structure, identity provenance, and typography checks. Assume the first version contains defects and actively look for them. Route every failure to the smallest responsible dimension instead of reopening unrelated approved stages.

## 15. Final verifier

Input: evidence inventory, asset plan, type spec, final artifact, still critic report, render QA, and final visual critique.

Output `PASS`, `FAIL:fixable`, or `HOLD` with a specific reason. Do not return PASS when any blocking visual, evidence, identity, typography, render-safety gate, perception-preflight failure, or aggregate visual-slop threshold remains unresolved.
