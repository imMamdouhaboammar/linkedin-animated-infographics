# Identity asset source policy

Apply this contract to every named official AI model, AI application, provider, tool logo, or mascot used in the infographic.

## Precedence

1. Use an exact user-supplied official asset when present.
2. When Lobe covers the named AI/tool identity, use Lobe.
3. Otherwise return `HOLD: verified identity asset required`.

Do not redraw, approximate, prompt-generate, trace, or silently substitute a named official identity.

Generic decorative icons and diagram primitives are outside this identity rule because they do not claim an official brand identity.

## Lobe-first resolution

Read `https://lobehub.com/icons/skill.md` before choosing a Lobe slug or import and follow the current `@lobehub/icons` instructions.

Prefer:

- `@lobehub/icons-static-svg` for supported logos
- `@lobehub/icons-static-avatar` for supported avatar or mascot identity assets

Record the exact slug and versioned package or immutable source reference used. A remote URL may be used to resolve the source, but the final HTML must use a local or embedded copy so render capture is deterministic.

## Asset plan

Before creative direction, produce a bounded asset plan with one record per named identity:

- `name`
- `kind`
- `source_type`: `user-official` or `lobe`
- `source_ref`
- `lobe_slug` and package when applicable
- `render_disposition`: `local` or `embedded`
- local path when applicable
- `identity_locked: true`
- `status: PASS`

An empty asset list is valid when the story contains no named identity assets.

## Final checks

Fail or HOLD when:

- a required named identity has no verified source
- Lobe coverage is uncertain and cannot be checked
- the final visual uses a generated or approximate official identity
- the final HTML still depends on a remote logo/avatar request
- the visible identity differs materially from the approved source
