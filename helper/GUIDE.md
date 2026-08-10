# LLM Routing Guide

Read this file before choosing a production skill or worker.

## Authority

The machine-readable routing authority is split across:

- `helper/router.json` for intent and conditional routing
- `helper/capabilities.json` for capability ownership, research-gate linkage, and plugin-local defaults
- `helper/quality-gates.json` for blocking local creative/product gates
- `helper/artifacts.json` for handoff artifacts
- `helper/modules.json` for active skills, agents, and public tools
- `research/capability-notes/sources.json` for inspected upstream provenance
- `research/capability-notes/gates.json` for adopted runtime research gates
- `architecture/plugin-graph.json` for executable worker order and required skill preloads
- `scripts/info_stories.py::load_catalog()` for the merged Info-stories registry
- `skills/info-stories/references/asset-source-policy.md` for Lobe-first identity source behavior
- `skills/info-stories/references/typography-direction.md` for intentional render-safe typography behavior
- `schemas/demo.schema.json` and `scripts/demo_gallery.py` for the public demo gallery contract

If prose conflicts with one of those contracts, stop and repair the drift instead of guessing.

## Decision protocol

1. Classify the user intent.
   - create or redesign a post: `create-post`
   - inspect a finished post: `qa`
   - render an approved HTML artboard: `render`
   - study a visual reference: `design-study`
   - animate a named or verified SVG mascot as a focused task: `mascot-animation`
   - compose an Info-story without running the whole post pipeline: `info-story`
   - publish a verified finished demo after explicit consent: `share-demo`
2. Load the route from `router.json`.
3. Resolve capability owners and plugin-local defaults from `capabilities.json`.
4. Apply the route's research gates from `research/capability-notes/gates.json`.
5. Apply conditional asset/language/UI/reference gates before generation.
6. Confirm required evidence and named identity requirements.
7. Invoke the selected workflow or focused skill.
8. Workers return artifacts to the parent workflow. They do not coordinate peers through hidden handoffs.
9. Stop on a blocking `HOLD`; do not improvise around it.

## Canonical shipping order

`new-post` runs:

`design-study -> evidence-checker -> asset-curator -> creative-director -> story-architect -> palette-curator -> type-curator -> copy-compressor -> layout-composer -> caption-writer -> artboard-builder -> motion-director -> optional mascot-animator -> motion-engineer -> render-qa -> post-critic -> story-verifier`

`asset-curator` produces `build/asset-plan.json`. `type-curator` produces `build/type-spec.json`. Downstream workers preserve both artifacts rather than resolving assets or fonts again.

## Plugin-local visual defaults

These are repository product defaults, not research-source claims.

- Palette character is `creative-attractive-restrained`. Prefer color combinations that are distinctive, harmonious, and visually engaging without exaggerated saturation, unnecessary neon, or multiple competing accents unless the approved brief explicitly calls for them.
- Infographic composition is `center-first`. Center the primary visual anchor and major story zones by default so the fixed 1080x1350 page reads as one intentional composition.
- Identity sourcing is `Lobe-first` after exact user-supplied official assets. Supported named AI/tool identities use Lobe and remain identity-locked. Missing verified identities HOLD instead of being approximated.
- Typography is `intentional typography`. User-specified or supplied local fonts take precedence. Final capture uses only system, embedded, or local-file loading and never a remote font dependency.
- Creative structure is relationship-led. Every concept records one dominant anchor, structural archetype, containment strategy, negative-space strategy, and motion job. Repeated cards are used when repetition is the story, not as a default wrapper.
- Use an alignment exception only when it improves comprehension or fidelity. Accepted categories include tables, UI mockups, code/terminal surfaces, timelines, Arabic/RTL reading flow, and documented reference-DNA decisions.
- Record the alignment exception in the layout artifact. Do not introduce off-center composition only for decorative asymmetry.

## Research gates

Research is active production guidance, not background reading. The current adopted gate IDs are:

- `prose-specificity`: reject named filler and low-information copy patterns per slot
- `voice-preservation`: protect facts, mechanisms, names, numbers, and deliberate voice while editing
- `design-dials`: require explicit design variance, visual density, and motion intensity decisions
- `structural-originality`: reject palette-only reskins and require meaningful structural variation
- `reference-dna`: when a reference exists, diagnose reusable structure without cloning distinctive work
- `contrast-discipline`: enforce the established semantic-token and contrast floors
- `evidence-traceability`: tie factual claims, product states, metrics, logos, and acceptance rows to evidence
- `bounded-verification`: keep verification independent and allow at most two targeted repair attempts

Local blocking gates add `verified-identity-assets`, `intentional-typography`, and `clean-creative-structure` on top of the research layer.

The research gate registry records source provenance, stage, severity, owners, local behavior, and implementation references. Upstream repositories are research inputs only; their working copies are not runtime dependencies and are not packaged with the plugin.

Validate this layer with:

```bash
python3 scripts/research_gates.py check
```

## Conditional gates

### Arabic or RTL

Add the `arabic` skill before copy and layout work. Preserve bidi isolation, RTL ordering, Arabic typography, and the existing render constraints. RTL reading flow is an explicit alignment exception when center-first would reduce comprehension.

### Named identity, logo, or mascot

Run the verified identity path. Exact user-supplied or task-attached official assets have first priority. When a named AI/tool identity is supported by Lobe, `asset-curator` reads `https://lobehub.com/icons/skill.md`, resolves the current Lobe asset, records exact provenance, and makes a local or embedded render copy.

If neither an exact user asset nor a verified Lobe match exists, return `HOLD: verified identity asset required`.

Never redraw, approximate, substitute, or generate a named official lookalike. A Lobe-backed mascot is still passed to `mascot-animator` as an exact verified local SVG.

### Typography

Run `type-curator` after palette selection and before copy fitting. Honor explicit user families when render-safe; otherwise use supplied/bundled assets or a curated deterministic system direction. Remote `@import`, Google Fonts capture dependencies, and other render-time font requests fail `intentional-typography`.

### UI mockup story

Enable the `ui-mockup-fidelity` capability. Product states, features, metrics, integrations, logos, and proof that appear real must be evidence-backed. Clearly label concept UI or fictional data when it could be mistaken for documented product behavior. The route applies `structural-originality`, `contrast-discipline`, and `evidence-traceability` where applicable. UI control alignment may override center-first when product fidelity or reading order requires it.

### Visual references

Use `design-study` to extract reusable design DNA. Do not copy a reference pixel-for-pixel or treat its palette as the only source of variation. When a reference is present, activate `reference-dna` before layout production. A studied alignment pattern may override center-first only when it materially serves the content and is recorded as a reference-DNA decision.

### Static versus animated output

Static work stops after still QA and final verification. Animated work adds motion direction, optional mascot animation, motion implementation, and render QA.

### Community publishing

Community publishing is an optional public export boundary after delivery. `new-post` may offer it only after final verification `PASS`. A yes routes to the focused `share-demo` parent workflow; a no or no answer performs no GitHub write.

The public package is exactly `demo.gif`, `index.html`, and `demo.json`. `scripts/demo_submit.py` performs packaging/preflight and `scripts/demo_gallery.py` validates the repository gallery. Source prompts are private by default, rights confirmation is explicit, and GitHub publication stops at a pull request requiring maintainer manual review and merge.

## Parent workflow rule

`new-post` is the canonical parent workflow for complete post creation. It owns user approvals, HOLD resolution, repair loops, and final delivery. `share-demo` is a separate focused parent workflow that owns the optional export consent and contribution handoff after delivery. Every worker returns a bounded artifact to its parent workflow.

## HOLD semantics

A HOLD means a required input or blocking quality gate is missing. Common cases include:

- named identity has neither an exact user asset nor a verified Lobe asset
- final identity asset is still remote instead of local/embedded
- explicit required typography cannot be made render-safe
- typography relies on a remote font request
- unsupported factual proof
- unreadable contrast
- incompatible Info-stories composition
- selected concept fails clean creative structure
- unresolved blocking research-gate finding
- required render evidence unavailable
- community export requested without final verification PASS
- community export requested without explicit rights confirmation
- final GIF or HTML missing for a community package
- GitHub identity/authentication, fork, push, or PR capability unavailable
- public export preflight finds secrets, local paths, signed URLs, or unsafe remote executable resources

Do not convert a HOLD into invented content. State the missing requirement and wait for the parent workflow or user to resolve it.

## Final verification

A complete post is not ready because generation finished. The shipping path ends with render evidence, adversarial review, and independent verification. Final verification includes identity provenance, typography render safety, clean creative structure, and all existing evidence/visual/motion gates. The final verifier may request at most two targeted repair attempts before escalation. Community sharing may be offered only after that final verdict is `PASS`.
