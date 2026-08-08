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

## 2. Creative director

Input: evidence inventory, audience, desired output mode, optional reference diagnosis.

Output: at least three meaningfully different creative directions. Each direction must include:
- visual hook
- copy hook
- useful reveal or relationship
- story shape
- recommended visual archetype
- motion behavior if relevant
- evidence dependencies
- risk notes

Reject three directions that are only palette changes of the same layout.

## 3. Story architect

Input: selected direction and evidence.

Output:
- one primary takeaway
- reading order
- opening state
- reveal or comparison logic
- closing takeaway
- visual anchor
- density target
- intended emotional tone without exaggerated marketing language

## 4. Palette curator

Input: story architecture and brand constraints.

Output:
- background
- primary text
- secondary text
- primary accent
- optional secondary accent with a defined semantic job
- state colors only when needed

Use a distinctive but restrained palette. Do not use multiple decorative accents to create interest.

## 5. Copy compressor

Input: evidence and story architecture.

Output copy by slot, not as a paragraph dump. Prioritize one idea per zone. Remove repeated explanation. Preserve mechanism, evidence, and useful specificity.

## 6. Layout composer

Input: story architecture, copy slots, palette.

Output an explicit macro-layout specification before HTML or styling details:
- canvas: 1080x1350
- safe margins
- headline zone
- primary visual-anchor zone
- supporting evidence/story zone
- takeaway zone
- footer zone
- zone bounding boxes or proportional heights
- alignment choice and reason
- structural fingerprint
- expected vertical occupancy
- maximum containment depth

Do not solve layout by immediately creating cards around every text block.

## 7. Still builder

Input: approved layout specification and copy.

Output a complete still-capable HTML artboard. Build macro zones first, then typography, visual relationship, details, and attribution.

The still must communicate the useful idea with animation disabled.

## 8. Still critic

Input: rendered or directly inspected still.

Output the top three visual defects, their severity, and exact repair actions. Apply every blocking rule in `visual-quality-contract.md`.

Do not pass a still because its text is technically readable. Balance, rhythm, visual anchor, content distribution, and generic visual patterns are first-class acceptance criteria.

## 9. Motion director

Input: passing still and story architecture.

Output a motion plan that states what each motion explains. Every animation must answer at least one question:
- what should I read next?
- what changed?
- where did this item travel?
- which state is active?

## 10. Motion implementer

Input: passing still and motion plan.

Output deterministic motion that preserves the approved layout. Do not redesign the composition while animating it.

## 11. Render QA

Input: animated or static artifact.

Output:
- frame-zero completeness
- clipping/overflow verdict
- footer clearance
- feed-scale legibility
- animation seam verdict
- motion pacing verdict
- reduced-motion or static fallback notes when relevant

## 12. Adversarial visual critic

Input: final render.

Re-run the visual failure taxonomy. Assume the first version contains defects and actively look for them.

## 13. Final verifier

Input: evidence inventory, final artifact, still critic report, render QA, final visual critique.

Output `PASS`, `FAIL:fixable`, or `HOLD` with a specific reason. Do not return PASS when any blocking visual or evidence gate remains unresolved.
