# Visual quality contract

This contract is blocking for still construction and final delivery.

## Canvas and macro layout

- Canvas is 1080x1350 unless the user explicitly requests another format.
- Define macro zones before styling individual components.
- The primary composition should use roughly 82-92% of the usable vertical canvas. Intentional sparse concepts may go lower only when the negative space has a clear compositional job.
- Reject an unexplained vertical gap greater than 120px between the end of the primary composition and the footer or final takeaway zone.
- Reserve a footer zone explicitly. The composition must terminate intentionally near it rather than ending early and leaving a detached footer.
- Keep safe outer margins consistent. Do not use the footer as a patch for poor vertical distribution.

## Identity assets

- Every named official AI/tool identity must match the approved asset plan.
- Exact user-supplied official assets have priority; supported named AI/tool identities use verified Lobe sources.
- Generated, traced, approximated, or silently substituted official identities fail.
- Final HTML must use a local or embedded copy, not a remote logo/avatar request.
- Placement, scale, and animation transforms may change; identity-defining marks, silhouette, proportions, and approved color/mono variants stay faithful.

## Visual hierarchy and clean structure

- One visual anchor must dominate within two seconds at feed scale.
- One zone gets one reading job.
- The page must have a visible macro rhythm: hook, visual relationship or evidence, useful reveal, takeaway.
- Preserve the selected relationship, structural archetype, containment strategy, and negative-space strategy.
- A dense story earns density through editing, grouping, scale, and whitespace, not by shrinking text or adding more containers.
- At 25% preview size, the viewer should still perceive one obvious hook, one obvious visual relationship, and one obvious takeaway.
- Reject a generic headline plus unrelated cards when repetition is not the story.

## Perception preflight

Run this after macro layout and before still construction. It is blocking because visual polish must not hide a weak composition.

- exactly one primary focal anchor; three or more equal-emphasis anchors fail
- **one-second hierarchy test**: hook, primary anchor, and takeaway should register without reading every supporting line
- **100x100** thumbnail test: the dominant silhouette and hierarchy must survive at roughly 100x100 pixels
- **squint** or blur value-mass test: the intended reading path should survive loss of detail
- **grayscale** hierarchy test: scale, placement, spacing, and value must still establish hierarchy without hue
- **negative-space audit**: distinguish active negative space from accidental dead space
- edge, crop, and **tangency** test: remove accidental edge kisses, weak overlaps, and crops that look unintended
- **brand-off specificity** test: without logos or brand marks, the structure should still feel specific to this story rather than generic UI
- **effect-subtraction** test: removing glow, shadows, 3D, texture, particles, and decorative motion must not remove the concept itself

A failed preflight records visible evidence and the **smallest responsible dimension**. Route only that dimension for repair and preserve unrelated approved evidence, assets, typography, and copy.

## Reference transfer

When visual references are available, use this exact reasoning chain:

`Evidence -> Observation -> Transferable Rule -> Anti-Rule`

Evidence describes what is visibly present. Observation names the pattern. Transferable Rule converts it into a general design decision for the new story. Anti-Rule records what must not be copied or over-applied.

With multiple references, assign explicit non-overlapping jobs such as composition, type hierarchy, color harmony, texture/finish, illustration treatment, pacing, or motion. Do not blend references indiscriminately. Never copy distinctive subject matter, identity, proprietary artwork, or a unique layout signature.

## Containment and generic UI grammar

- Maximum bordered containment depth is two levels.
- Do not put a bordered card inside a bordered card inside another bordered panel.
- Repeated cards are acceptable for real comparison, cataloguing, specimens, categories, or repeated states. They must not become the automatic structure for unrelated content.
- Pills, badges, mini status chips, tiny uppercase labels, and dashboard-like controls require a semantic job. Decorative use fails.
- Do not create fake analytics, fake product UI, fake proof bars, invented metrics, or fake official identities to make a composition feel richer.
- Avoid generic dashboard grammar when the story is conceptual, editorial, comparative, or diagrammatic.

## Typography and copy density

- Implement the approved type spec exactly unless a targeted repair explicitly revises the type pass.
- Allowed font loading strategies are system, embedded, or local-file.
- Remote @import, font CDN requests, and other render-time network font dependencies fail.
- Preserve clear type hierarchy at feed width.
- Compress repeated explanations before reducing type size.
- Do not turn secondary copy into a wall of small labels.
- Headline, visual anchor, supporting explanation, and takeaway must remain distinguishable without reading every word.
- Silent font substitution is a blocking failure when it changes the approved type direction or breaks layout.

## Static payoff gate

The still must communicate the useful idea with animation disabled.

Motion cannot begin while any of these remain unresolved:
- unverified identity asset
- remote identity or font dependency
- silent typography substitution
- weak or competing visual anchors
- top-heavy composition
- bottom dead zone
- detached footer
- nested-card density
- generic UI grammar
- generic headline-plus-cards structure
- weak macro rhythm
- feed-scale legibility failure
- failed perception preflight

## Failure taxonomy

The critic must explicitly return PASS or FAIL for each item:

- `unverified-identity-asset`
- `remote-asset-dependency`
- `remote-font-dependency`
- `silent-font-substitution`
- `generic-card-first-structure`
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

Hard gates above remain blocking independently. Additional craft findings must be classified:

- `critical`: blocks immediately
- `major`: pressure 3
- `minor`: pressure 1

Block when there is any critical finding, **two or more major** findings, **four or more minor** findings, or **cumulative pressure** of 6 or more. The aggregate score never cancels a hard-gate failure.

Every finding includes status, severity, pressure, visible evidence, consequence, smallest responsible dimension, and exact repair action.

## Targeted revision routing

Use the smallest responsible dimension:

- concept/message -> creative direction
- hierarchy/composition/negative space -> layout
- typography -> type
- Arabic/RTL when active -> Arabic direction
- brand/identity -> asset/brand
- copy density -> copy compression
- motion -> motion direction or implementation
- render/runtime -> render QA

Retry from the last approved artifact for that dimension. Do not rerun unrelated upstream stages and do not chain repairs onto a known-bad visual state when doing so would compound drift.

## Still critique loop

After the first still:

1. inspect the whole 1080x1350 composition, not isolated components
2. compare named identities with the asset plan and type roles with the type spec
3. re-run the perception preflight against the actual render
4. name the top three visual defects with severity and responsible dimension
5. repair only those responsible dimensions
6. inspect again

Maximum two targeted repair attempts. A third unresolved blocking failure returns HOLD or FAIL instead of shipping.

## Acceptance statement

A still is ready for motion only when identity provenance is intact, typography is render-safe and faithful, the composition feels intentional at full size and feed size, the useful relationship is visually obvious, the footer belongs to the page, the perception preflight passes, cumulative visual-slop pressure is below the blocking threshold, and no generic component pattern is doing the creative work that the concept should be doing.
