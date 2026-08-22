# Visual quality contract

This contract is blocking for autopilot still construction and final delivery. It carries the same visual quality floor as the OpenAI studio route so choosing autopilot cannot bypass layout or critique requirements.

## Canvas and macro layout

- Canvas is 1080x1350 unless the user explicitly requests another format.
- Define macro zones before styling individual components.
- The primary composition should use roughly 82-92% of the usable vertical canvas. Intentional sparse concepts may go lower only when the negative space has a clear compositional job.
- Reject an unexplained vertical gap greater than 120px between the end of the primary composition and the footer or final takeaway zone.
- Reserve a footer zone explicitly. The composition must terminate intentionally near it rather than ending early and leaving a detached footer.
- Keep safe outer margins consistent. Do not use the footer as a patch for poor vertical distribution.

## Visual hierarchy

- One visual anchor must dominate within two seconds at feed scale.
- One zone gets one reading job.
- The page must have a visible macro rhythm: hook, visual relationship or evidence, useful reveal, takeaway.
- A dense story earns density through editing, grouping, scale, and whitespace, not by shrinking text or adding more containers.
- At 25% preview size, the viewer should still perceive one obvious hook, one obvious visual relationship, and one obvious takeaway.

## Perception preflight

Run a blocking **perception preflight** after macro layout and before still construction:

- exactly one primary focal anchor; three or more equal-emphasis anchors fail
- **one-second hierarchy test** for hook, primary anchor, and takeaway
- **100x100** thumbnail test for dominant silhouette and hierarchy
- **squint** or blur value-mass test for the intended reading path
- **grayscale** hierarchy test so structure does not depend on hue alone
- **negative-space audit** that distinguishes intentional framing from accidental dead space
- edge, crop, and **tangency** test
- **brand-off specificity** test so the structure remains story-specific without logos
- **effect-subtraction** test so glow, shadows, 3D, texture, or decorative motion are not carrying the concept

For each failure, record visible evidence, consequence, and the **smallest responsible dimension**. Repair only that dimension and preserve unrelated approved work.

## Reference transfer

When inspectable references exist, apply:

`Evidence -> Observation -> Transferable Rule -> Anti-Rule`

With multiple references, assign explicit non-overlapping jobs such as composition, type hierarchy, color harmony, texture, pacing, or motion. Do not blend references indiscriminately and do not copy distinctive subject matter, identity, proprietary artwork, or unique composition signatures.

## Containment and generic UI grammar

- Maximum bordered containment depth is two levels.
- Do not put a bordered card inside a bordered card inside another bordered panel.
- Repeated cards are acceptable for real comparison, cataloguing, or repeated states. They must not become the automatic structure for unrelated content.
- Pills, badges, mini status chips, tiny uppercase labels, and dashboard-like controls require a semantic job. Decorative use fails.
- Do not create fake analytics, fake product UI, fake proof bars, or invented metrics to make a composition feel richer.
- Avoid generic dashboard grammar when the story is conceptual, editorial, comparative, or diagrammatic.

## Typography and copy density

- Preserve clear type hierarchy at feed width.
- Compress repeated explanations before reducing type size.
- Do not turn secondary copy into a wall of small labels.
- Headline, visual anchor, supporting explanation, and takeaway must remain distinguishable without reading every word.

## Static payoff gate

The still must communicate the useful idea with animation disabled.

Motion cannot begin while any of these remain unresolved:

- weak or competing visual anchors
- top-heavy composition
- bottom dead zone
- detached footer
- nested-card density
- generic UI grammar
- weak macro rhythm
- feed-scale legibility failure
- failed perception preflight

## Failure taxonomy

The critic must explicitly return PASS or FAIL for each item:

- `top-heavy-composition`
- `bottom-dead-zone`
- `nested-card-density`
- `generic-ui-grammar`
- `weak-macro-rhythm`
- `weak-visual-anchor`
- `footer-detachment`
- `motion-on-weak-still`
- `decorative-motion`
- `feed-scale-legibility`

Any severe failure blocks delivery.

## Severity and visual-slop pressure

Hard gates remain blocking independently. Additional craft findings use:

- `critical`: blocks immediately
- `major`: pressure 3
- `minor`: pressure 1

Block on any critical finding, **two or more major** findings, **four or more minor** findings, or **cumulative pressure** of 6 or more. The aggregate score never cancels a hard-gate failure.

Every finding records severity, pressure, visible evidence, consequence, smallest responsible dimension, and exact repair action.

## Targeted revision routing

Route to the smallest responsible dimension:

- concept/message -> creative direction
- hierarchy/composition/negative space -> layout
- typography -> type
- Arabic/RTL when active -> Arabic direction
- brand/identity -> asset/brand
- copy density -> copy compression
- motion -> motion direction or implementation
- render/runtime -> render QA

Retry from the last approved artifact for that dimension. Do not rerun unrelated stages and do not compound drift by repairing on top of a known-bad visual state.

## Still critique loop

After the first still:

1. inspect the whole 1080x1350 composition, not isolated components
2. re-run the full perception preflight against the actual render
3. name the top three visual defects with severity and responsible dimension
4. repair only those defects
5. inspect again

Maximum two targeted repair attempts. A third unresolved blocking failure returns HOLD or FAIL instead of shipping.

## Acceptance statement

A still is ready for motion only when the composition feels intentional at full size and feed size, the useful relationship is visually obvious, the footer belongs to the page, the perception preflight passes, cumulative visual-slop pressure remains below the blocking threshold, and no generic component pattern is doing the creative work that the concept should be doing.
