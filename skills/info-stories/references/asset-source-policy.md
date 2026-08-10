# Identity asset source policy

This contract applies whenever an infographic names or visually depicts an official AI model, AI application, provider, tool identity, logo, or mascot.

## Leading rule: Lobe-first

Use this precedence for every named identity asset:

1. **User-supplied official asset.** An exact user-supplied or task-attached official file wins and remains identity-locked.
2. **Lobe.** When Lobe covers the named AI/tool identity, resolve the official visual from Lobe.
3. **HOLD.** If no exact user asset exists and Lobe does not cover the required named identity, return `HOLD: verified identity asset required`.

Do not redraw, approximate, prompt-generate, trace, restyle beyond approved color variants, or silently substitute a named official identity.

Generic decorative icons and abstract diagram marks are not identity assets. They may use semantic SVG primitives or another approved local source because no official identity is being claimed.

## Lobe resolution

Before resolving a Lobe asset, read:

`https://lobehub.com/icons/skill.md`

Follow the current instructions for `@lobehub/icons` rather than assuming stale component or slug names.

For deterministic infographic production, prefer:

- logos: `@lobehub/icons-static-svg`
- supported avatars or mascot-like identity assets: `@lobehub/icons-static-avatar`

A CDN or package registry may be used during resolution. The final artboard must reference a local or embedded copy so frame capture does not depend on network availability.

Record the exact Lobe slug, package, and resolved package version or immutable source reference. Do not write `latest` into the final provenance record when a concrete version can be resolved.

## Asset artifact

`asset-curator` writes `build/asset-plan.json`.

The top level contains `assets`, an array of records with:

- `name`
- `kind`
- `source_type`: `user-official` or `lobe`
- `source_ref`
- `lobe_slug` when `source_type` is `lobe`
- `package` when `source_type` is `lobe`
- `render_disposition`: `local` or `embedded`
- `local_path` when `render_disposition` is `local`
- `identity_locked: true`
- `status: PASS`

The artifact may contain an empty `assets` array when the brief contains no named identity assets.

## Downstream contract

`creative-director`, `layout-composer`, `artboard-builder`, `mascot-animator`, `post-critic`, and `story-verifier` consume the approved asset plan.

They may change size, placement, animation transform, and an explicitly supported mono/color variant. They may not switch the identity source or invent a replacement.

The final HTML must not depend on a remote logo or avatar URL.

## HOLD conditions

Return HOLD when:

- a named identity is required but neither an exact user asset nor a matching Lobe asset is available
- Lobe coverage is uncertain and cannot be verified
- the requested asset source cannot be copied or embedded before rendering
- a downstream layout requires altering the identity beyond an approved variant
- provenance cannot identify the exact source used

A HOLD protects the identity boundary. It is not permission to create a lookalike.
