# Typography direction

Typography is selected before copy fitting and layout execution. It must fit the story, language, density, reference DNA, and visual anchor while remaining deterministic during render capture.

## Precedence

1. Honor explicit user-specified typography when render-safe.
2. Prefer supplied or locally available font assets that can be embedded or loaded from a stable local file.
3. Otherwise choose a curated deterministic system stack.

## Allowed loading strategies

- `system`
- `embedded`
- `local-file`

Remote @import is forbidden. Do not depend on Google Fonts, CSS font CDNs, or another network font request while frames are captured.

## Type directions

Choose one direction with a clear story job:

- **Editorial authority:** expressive editorial display plus neutral body
- **Technical editorial:** engineered or mono display plus quieter mono/grotesk body
- **Modern product:** compact grotesk display plus neutral grotesk body
- **Data or systems:** mono display plus restrained sans/mono body according to density
- **Arabic or bilingual:** a shaping-safe Arabic direction that preserves RTL/bidi requirements

When locally available or embedded, JetBrains Mono plus Geist Mono is a valid technical-editorial pairing. It is an example, not a mandatory default.

## Type spec

Before copy compression, record:

- `direction_name`
- `headline_family`
- `body_family`
- optional `mono_family`
- `loading_strategy`
- `fallbacks`
- role weights
- minimum feed sizes
- `pairing_reason`
- `story_fit`
- `render_safety`
- `status: PASS`

If headline and body use the same family, include `single_family_reason`.

## Acceptance

The type direction passes only when the hierarchy is visible at feed scale, body copy remains readable, the pairing fits the story instead of adding decorative novelty, and no remote font dependency remains.

Solve density by editing copy and structure before reducing load-bearing type size.
