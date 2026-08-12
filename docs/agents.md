# Agents

The active worker inventory is declared in `helper/modules.json` and the executable order is declared in `architecture/plugin-graph.json`. Every agent returns a bounded artifact or verdict to the parent workflow. Agents do not coordinate peer agents directly.

## Visual study contract

`design-study` reports ranked evidence, confidence, provenance/rights, focused contexts, and explicit READY/HOLD/SKIP status.

## Complete workflow agents

### `design-study`

Diagnoses visual references into reusable design DNA before concept generation. It owns `reference-dna` when references are present and returns `build/design-study.json`.

### `evidence-checker`

Defines the factual boundary before creative work begins. It classifies claims, product states, metrics, named identities, logos, proof, and UI evidence, then returns `build/evidence.json`. It owns `evidence-traceability` at intake.

### `asset-curator`

Resolves named AI/tool logos and mascot identities before concept generation. Exact user-supplied official assets have priority; supported named AI/tool identities then resolve through Lobe after reading the current Lobe icon skill instructions. It records exact provenance, requires a local or embedded render copy, blocks generated official lookalikes, and returns `build/asset-plan.json`.

### `creative-director`

Generates at least three evidence-safe creative directions after identity assets are verified. Each direction contains a visual hook, copy hook, aha mechanic, story relationship, dominant visual anchor, structural archetype, containment strategy, negative-space strategy, motion job, evidence dependencies, risks, and why it earns attention. It returns `build/creative-concepts.json`.

This agent applies `hooked-design-copy`, `creative-payoff`, and `clean-creative-structure`. It must not use spectacle or generic card grids as a substitute for explanation.

### `story-architect`

Turns the selected creative direction into a deterministic Info-stories brief. It resolves Story Archetype, Visual Style, Story House, Motion Patterns, design dials, and the selected clean-structure requirements, then returns `build/story-brief.json`.

### `palette-curator`

Resolves the Story House and semantic token roles. It enforces `creative-attractive-restrained` palette behavior and the `contrast-discipline` research gate. It returns `build/palette-check.json`.

### `type-curator`

Chooses typography before copy fitting. Explicit user typography wins when render-safe, followed by supplied or bundled local assets, then a curated deterministic system direction. It records headline/body roles, fallbacks, minimum feed sizes, pairing rationale, and an allowed `system`, `embedded`, or `local-file` loading strategy in `build/type-spec.json`. Remote render-time font loading is a blocking failure.

### `copy-compressor`

Compresses source material into infographic-sized design copy while protecting facts, names, numbers, mechanisms, voice, the approved copy hook, and the minimum feed-size constraints from the type spec. It applies `prose-specificity`, `voice-preservation`, and evidence constraints, then returns `build/artboard-copy.json`.

### `layout-composer`

Turns the selected concept, story brief, asset plan, type spec, copy, palette, and optional reference study into a static hierarchy and topology specification. It applies `center-first-composition`, `clean-creative-structure`, `verified-identity-assets`, `intentional-typography`, `design-dials`, `structural-originality`, and `reference-dna` when active. It returns `build/layout-spec.json`.

### `caption-writer`

Writes the LinkedIn caption and first comment. It applies `hooked-design-copy` to the opening, keeps one caption archetype, preserves evidence, and returns `build/caption.md` plus `build/first-comment.md`.

### `artboard-builder`

Builds the approved 1080x1350 HTML still and rendered PNG. It preserves the selected creative payoff and clean structure, uses only identity-locked assets from the asset plan, implements the approved type spec without remote font loading, preserves Story House tokens, center-first layout or documented exception, UI fidelity, and contrast. It returns `build/post.html` and `build/still.png`.

### `motion-director`

Chooses zero to two meaning-driven Motion Patterns after the still is approved. Motion must communicate hierarchy, sequence, reveal, state, route, or the selected creative payoff. It returns `build/motion-direction.json`.

### `mascot-animator`

Conditional worker for a named or official mascot. It consumes the exact verified local SVG from `build/asset-plan.json` when the complete workflow resolved the identity. That SVG may be an exact user/task asset or a verified Lobe asset for a supported named AI/tool identity. Direct focused mascot work keeps the exact user-SVG requirement. The worker inspects real geometry, preserves identity, selects a communication-led direction, and returns `build/mascot/motion-contract.json`. Missing verified identity is a HOLD.

### `motion-engineer`

Implements the approved seekable motion direction on the approved still. It preserves the resolved story brief, frame-zero completeness, one loop clock, motion budget, exact identity assets, and approved typography when present.

### `render-qa`

Produces deterministic static/GIF evidence without editing the artboard. It checks frame 0, feed-scale legibility, contrast, changed-pixel motion, seam, safe zone, duration, and file size. It returns `build/render-report.json`.

### `post-critic`

Performs adversarial review before independent verification. It explicitly checks anti-slop, design taste, `hooked-design-copy`, `creative-payoff`, `clean-creative-structure`, `verified-identity-assets`, `intentional-typography`, `restrained-palette`, `center-first-composition`, UI fidelity, mascot identity, motion meaning, and evidence safety. It returns `build/critic-report.json`.

### `story-verifier`

Read-only independent acceptance worker. It inspects artifact evidence directly, including identity provenance and typography loading, records one evidence row per criterion, enforces `evidence-traceability` and `bounded-verification`, and returns `build/verification-report.json` with `PASS`, `FAIL:fixable`, or `FAIL:escalate`.

## Focused publication agent

### `community-publisher`

Runs only after the `share-demo` parent workflow has explicit consent, final verification PASS, rights confirmation, and a validated three-file export. It handles the contributor fork, fresh `community/<user>/<slug>` branch, scoped commit, push, and pull request against upstream `main`. It never merges, enables auto-merge, pushes to upstream `main`, or claims success without a real PR URL. Every contribution remains pending maintainer manual review and merge.

## Coordination contract

The canonical complete sequence is:

`design-study -> evidence-checker -> asset-curator -> creative-director -> story-architect -> palette-curator -> type-curator -> copy-compressor -> layout-composer -> caption-writer -> artboard-builder -> motion-director -> optional mascot-animator -> motion-engineer -> render-qa -> post-critic -> story-verifier`

The sequence is declared in `architecture/plugin-graph.json` and mirrored by the `create-post` route. The `community-publisher` is intentionally outside that critical sequence and is reachable only through the optional `share-demo` route. Parent workflows own sequencing, user approvals, HOLD resolution, and bounded repair/export rules.

Validate all worker contracts with:

```bash
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 -m unittest tests.test_agent_contracts -v
```
