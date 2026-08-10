# Visual Source, Typography, and Creative Engine Design

## Goal

Make the infographic engine reliably source named AI and tool identities from Lobe when available, choose typography intentionally, and generate cleaner, structurally varied creative directions before layout production.

## Scope

This change affects the canonical `new-post` workflow, focused `info-story` creation, QA, the Claude worker graph, and the isolated OpenAI infographic studio distribution.

It does not add a web application, remote service, telemetry, or a runtime dependency on Lobe during final GIF capture.

## Design decisions

### 1. Identity asset sourcing is a blocking contract

Named brand logos, AI identities, and AI mascots use this precedence:

1. An exact user-supplied official asset wins.
2. If the identity is covered by Lobe, resolve it from Lobe and record the exact source.
3. If a named identity is not available from Lobe and the user did not supply an official asset, return `HOLD: verified identity asset required`.

The engine must not redraw, approximate, invent, or silently substitute a named official identity.

Lobe discovery starts by reading `https://lobehub.com/icons/skill.md` and following the current `@lobehub/icons` instructions. Static production should prefer SVG from `@lobehub/icons-static-svg` for logos and the Lobe static avatar package for supported avatars or mascots. The exact package/version or source reference used must be recorded in the asset artifact.

Remote CDN URLs may be used to resolve an asset, but the final artboard must use a local or embedded copy so deterministic frame capture never depends on network availability.

Generic decorative icons are not identity assets. They may use semantic SVG primitives, text, or another approved local source when the story needs them. The Lobe rule applies to supported named AI/tool identities, not to every decorative glyph.

### 2. A dedicated asset pass owns identity resolution

Add `asset-curator` after `evidence-checker` and before `creative-director`.

It produces `build/asset-plan.json` with one record per named identity:

- `name`
- `kind`
- `source_type`: `user-official` or `lobe`
- `source_ref`
- `lobe_slug` when applicable
- `package` and resolved version when applicable
- `local_path` or embedding plan
- `identity_locked: true`
- `status`: `PASS` or blocking finding

The artifact is blocking when named identities are part of the brief.

Downstream creative, layout, artboard, mascot, critic, and verifier passes consume this artifact instead of sourcing identities independently.

### 3. Typography gets its own decision artifact

Add `type-curator` after `palette-curator` and before `copy-compressor`.

It produces `build/type-spec.json` with:

- `direction_name`
- `headline_family`
- `body_family`
- optional `mono_family`
- `loading_strategy`: `system`, `embedded`, or `local-file`
- `fallbacks`
- role weights and minimum feed-scale sizes
- `pairing_reason`
- `story_fit`
- `render_safety`
- `status`

Precedence:

1. Explicit user typography requirements.
2. Supplied or bundled local font assets.
3. A curated deterministic system stack selected by story shape and tone.

Never use remote `@import` or depend on a webfont request during frame capture.

A single family for headline and body is allowed only when it has a clear editorial or technical reason. The type artifact records that reason.

### 4. Curated type directions

The engine should choose from a small set of strong roles rather than a long font menu.

- Editorial authority: high-contrast editorial display plus neutral grotesk body.
- Technical editorial: expressive mono or engineered display plus neutral mono or grotesk body.
- Modern product: compact grotesk display plus neutral grotesk body.
- Data or systems: mono display plus restrained sans or mono body depending density.
- Arabic or bilingual: use the existing Arabic typography contract and preserve RTL rules.

The selected direction is a semantic decision, not decoration. It must fit the story, density, reference DNA, language, and visual anchor.

### 5. Creative direction receives a clean-structure gate

Keep the existing requirement for at least three genuinely different concepts, but strengthen the generation grammar.

For each concept, the creative director must state:

- the relationship being visualized
- the dominant visual anchor
- the structural archetype
- containment strategy
- negative-space strategy
- motion job
- why the structure is cleaner than a generic card grid

At least one direction must be editorial and low-containment when the story permits it. At least one must be diagrammatic or relationship-led when the content contains a real relationship. Repeated-card layouts are valid only when repetition is the story.

The chosen concept must pass `clean-creative-structure` before story architecture.

Blocking failures include:

- generic headline plus unrelated cards
- palette-only variation
- card-first composition where the story does not require repeated units
- decorative 3D, glow, floating objects, or motion without a story job
- no dominant anchor
- no useful relationship or payoff
- visual density created by shrinking text instead of editing structure

### 6. Machine-readable gates

Add three blocking local gates:

- `verified-identity-assets`
- `intentional-typography`
- `clean-creative-structure`

Add capabilities:

- `visual-asset-sourcing`
- `typography-direction`

Add deterministic validators:

- `tools/asset_policy_check.py`
- `tools/type_spec_check.py`

The validators reject invalid artifacts before downstream production.

### 7. Workflow order

Canonical sequence:

`design-study -> evidence-checker -> asset-curator -> creative-director -> story-architect -> palette-curator -> type-curator -> copy-compressor -> layout-composer -> caption-writer -> artboard-builder -> motion-director -> optional mascot-animator -> motion-engineer -> render-qa -> post-critic -> story-verifier`

The mascot branch consumes the already verified identity asset. It does not create a second identity-sourcing path.

### 8. OpenAI parity

The isolated OpenAI infographic studio must include the same behavioral gates without depending on Claude workers.

Add asset and typography references to the OpenAI skill package and insert explicit asset-curator and type-curator reasoning passes in its required sequence.

OpenAI final verification must fail when a named supported identity was approximated instead of sourced, or when typography depends on a remote font load.

### 9. QA and acceptance

A production PASS requires:

- every named supported AI/tool identity sourced from an exact user asset or Lobe
- no invented official logo or mascot
- final identity assets local or embedded for render determinism
- a complete passing type spec
- no remote font dependency
- creative concepts with real structural variation
- chosen concept passes the clean-structure gate
- downstream layout and artboard preserve the approved asset and type artifacts
- critic and verifier explicitly check all three new gates

## Non-goals

- bundling the full Lobe icon package into this repository
- downloading every supported logo in advance
- adding a browser UI for font picking
- using a large catalog of decorative fonts
- replacing the existing Story House, reference-DNA, contrast, or anti-slop contracts

## Compatibility

Existing explicit user assets and font requirements keep priority. Existing Claude behavior remains intact except for the two new bounded passes and stronger gates. Static and animated production continue to use the same 1080x1350 artboard and deterministic render pipeline.
