# Typography direction

Typography is a story and hierarchy decision. Choose it before copy is fitted into layout and preserve it through static and motion production.

## Selection precedence

1. **User-specified typography.** Honor explicit family, weight, and role requirements when render-safe.
2. **Supplied or bundled font assets.** Prefer exact local assets that can be embedded or loaded from a stable local file.
3. **Curated deterministic system stack.** Choose a strong system-safe direction when no exact font asset is available.

A requested font that cannot be loaded deterministically must not be fetched during frame capture. Resolve it to an embedded/local asset first or use an approved fallback with the reason recorded.

## Render safety

Allowed loading strategies:

- `system`
- `embedded`
- `local-file`

Remote @import is not allowed. Do not rely on Google Fonts, a CSS CDN, or another network font request during static capture or GIF frame capture.

When embedding a font, wait for `document.fonts.ready` before capture. When using a local file, keep the final artifact portable or package the asset beside it.

## Curated directions

Choose one small direction that fits the story instead of browsing a large decorative font menu.

### Editorial authority

Use a high-contrast editorial display role with a restrained neutral body role. Best for thought leadership, arguments, essays, and evidence-led editorial layouts.

### Technical editorial

Use an expressive mono or engineered display role with a quieter mono or grotesk body role. Best for agent workflows, code-adjacent concepts, architecture, systems, and product mechanics.

### Modern product

Use a compact grotesk display role with a highly readable neutral grotesk body. Best for product explanations, launches, feature logic, and interface-led stories.

### Data or systems

Use a mono display role with either a restrained sans or mono body depending on density. Best for pipelines, matrices, taxonomies, diagrams, and data-heavy explanatory work.

### Arabic or bilingual

Use the existing Arabic/RTL typography contract. Font direction must preserve Arabic shaping, bidi behavior, and the requested reading flow.

## Type artifact

`type-curator` writes `build/type-spec.json` with:

- `direction_name`
- `headline_family`
- `body_family`
- optional `mono_family`
- `loading_strategy`
- `fallbacks`
- `headline_weight`
- `body_weight`
- `minimum_feed_sizes`
- `pairing_reason`
- `story_fit`
- `render_safety`
- `status: PASS`

When headline and body use the same family, add `single_family_reason` and explain why a one-family system improves the story or reference fidelity.

## Selection checks

A type direction passes only when:

- the headline has enough character to create hierarchy without becoming decorative noise
- the body remains readable at feed scale
- the pairing fits the story and selected visual archetype
- the weights produce visible hierarchy at 1080x1350 and LinkedIn feed scale
- no remote font dependency remains
- copy density is solved through editing and layout before font-size reduction

## Useful examples

When locally available or embedded, pairings such as JetBrains Mono for technical display and Geist Mono for quieter technical body can work for a technical editorial direction. The named families are examples, not mandatory defaults.

System-safe editorial fallbacks may use Iowan Old Style or Palatino for display and the platform UI sans stack for body. Technical system fallbacks may use SF Mono, ui-monospace, Cascadia Mono, Menlo, Consolas, and Liberation Mono.

## HOLD conditions

Return HOLD when:

- an explicit required font is unavailable and no approved fallback is allowed
- the chosen font cannot be made render-safe
- the selected pair fails feed-scale legibility
- the type direction conflicts with Arabic/RTL requirements
- the artifact would depend on remote @import or another render-time network font request
