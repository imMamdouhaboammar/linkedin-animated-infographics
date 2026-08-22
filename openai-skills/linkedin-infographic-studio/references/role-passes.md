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

Resolve every named identity before concepting. Apply this precedence:
- exact user-supplied official asset
- inspectable original-owner source with local integrity record
- pinned `https://github.com/imMamdouhaboammar/vibe-svgs` file under `svgs/logos/` for a platform/tool logo only
- Lobe for a supported identity after reading `https://lobehub.com/icons/skill.md`
- HOLD when no verified source exists

For Vibe SVGs logo mirrors, record exact commit, path, Git blob SHA, local SHA-256, `identity_status: supplied-third-party-mark`, and `alteration_policy: placement-only`.

Vibe SVGs mascot/scene records with `communityArtwork: true` are community/fan-made. They must not be called official. They require explicit user confirmation and cannot satisfy an original/official mascot request.

Record exact provenance and require local/embedded render disposition. Never generate, trace, reconstruct, or approximate an official lookalike. Identity geometry, identity colors, wordmarks, and aspect ratio remain locked downstream.

## 3. Creative director

Input: evidence inventory, approved asset plan, audience, desired output mode, optional reference diagnosis.

Read `narrative-taste.md` before final direction selection.

When references are active, deconstruct every selected mechanism using:

`Evidence -> Observation -> Transferable Rule -> Anti-Rule`

For multiple references, assign explicit non-overlapping jobs such as hook, progression, composition, type hierarchy, color, texture, pacing, motion, proof, or payoff. Do not blend all references into one mood and do not copy distinctive subject matter, identity, proprietary artwork, or unique layout signatures.

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
- approved identity-asset roles
- reference jobs, transferable rules, and anti-rules when references exist
- risk notes

Apply clean creative structure. Include an editorial low-containment option when the story permits it. Include a diagrammatic or relationship-led option when a real relationship exists. Repeated cards are valid only when repetition is the story.

Reject three directions that are only palette changes of the same layout.

## 4. Story architect

Input: selected direction, evidence, approved asset plan, and optional reference/demo diagnosis.

Read `narrative-taste.md` completely.

Choose the story shape from the relationship in the evidence, not from a favorite layout. Use `Hook -> Tension -> Evidence -> Turn -> Payoff` when it fits, but compress/reorder when another progression is clearer.

For every retained beat record:
- Reader question
- beat job
- evidence dependency
- Beat-to-visual mapping
- transition job
- payoff dependency

Remove beats that exist only to create another animation state. A card grid is not a story shape by itself.

When repository demos are actually available, inspect only one to three relevant examples and extract abstract mechanisms. Installed OpenAI packages do not pretend `demos/` media is locally present.

Output:
- one primary takeaway
- selected narrative shape
- hook
- ordered beats and reading order
- opening state
- tension or question
- evidence progression
- turn/reveal/comparison logic
- closing payoff/takeaway
- persistent context across states
- dominant visual anchor
- containment and negative-space requirements
- density target
- required motion jobs only
- approved logo/mascot communication jobs without identity mutation
- reference/demo jobs, transferable rules, anti-rules, and originality changes
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

Use a distinctive but restrained palette. Do not use multiple decorative accents to create interest. Approved identity assets keep their locked identity colors unless their exact source provides another approved variant.

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

Copy must follow the narrative beats. Do not make every zone restate the primary takeaway.

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

Map the approved narrative beats to spatial states without turning each beat into a card by default. Preserve the selected clean structure and persistent story context.

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

Identity-locked assets may be placed/scaled but not redrawn, recolored without an approved source variant, distorted, or reconstructed.

## 10. Still critic

Input: rendered or directly inspected still plus asset/type specs.

Output the top three visual defects, their severity, pressure, smallest responsible dimension, and exact repair actions. Apply every blocking rule in `visual-quality-contract.md`, including identity provenance, typography, clean structure, balance, rhythm, visual anchor, content distribution, generic visual patterns, and the full perception preflight against the actual render.

Also compare named logos/mascots with the approved identity plan. Unapproved geometry, wordmark, color, aspect-ratio, or identity-status drift is blocking.

Hard gates block independently. Additional craft findings use critical/major/minor severity and cumulative pressure. Do not return PASS when the aggregate blocking thresholds in the visual-quality contract are reached.

## 11. Motion director

Input: passing still and story architecture.

Output a motion plan that states what each motion explains. Every animation must answer at least one question:
- what should I read next?
- what changed?
- where did this item travel?
- which state is active?

Motion should advance the approved narrative beat sequence. Reserve the strongest change for the strongest conceptual turn/payoff. Mascot motion may transform approved existing groups but cannot redraw identity geometry.

## 12. Motion implementer

Input: passing still and motion plan.

Output deterministic motion that preserves the approved layout, identity assets, and typography. Do not redesign the composition while animating it. Do not mutate identity-locked SVG paths or colors as an animation shortcut.

## 13. Render QA

Input: animated or static artifact.

Output:
- frame-zero completeness
- clipping/overflow verdict
- footer clearance
- feed-scale legibility
- identity-asset load and integrity verdict
- font-load verdict
- narrative readability across sampled states
- animation seam verdict
- motion pacing verdict
- reduced-motion or static fallback notes when relevant

## 14. Adversarial visual critic

Input: final render plus evidence, asset plan, and type spec.

Re-run the visual failure taxonomy, perception preflight, severity pressure, clean structure, identity provenance/integrity, narrative progression, and typography checks. Assume the first version contains defects and actively look for them. Route every failure to the smallest responsible dimension instead of reopening unrelated approved stages.

## 15. Final verifier

Input: evidence inventory, asset plan, type spec, final artifact, still critic report, render QA, and final visual critique.

Output `PASS`, `FAIL:fixable`, or `HOLD` with a specific reason. Do not return PASS when any blocking visual, evidence, identity, typography, narrative, render-safety gate, perception-preflight failure, or aggregate visual-slop threshold remains unresolved.
