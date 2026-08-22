# Identity asset source policy

Apply this contract to every named official AI model, AI application, provider, tool logo, or mascot used in the infographic.

Identity assets are evidence. A familiar-looking mark is not enough. Resolve the source, pin it, preserve it, and prove what it is before creative production starts.

## Mandatory precedence

Use this order for every named identity:

1. **Exact user-supplied official asset.** A task-attached official file wins and remains identity-locked.
2. **Original-owner source.** Prefer an asset published by the identity owner when an inspectable original-owner source is available. Record owner, immutable source reference when possible, and SHA-256 integrity before localizing it.
3. **Pinned Vibe SVGs logo mirror.** For platform/tool logos only, `https://github.com/imMamdouhaboammar/vibe-svgs` may supply an intact mirrored mark from `svgs/logos/`. Pin the exact commit, source path, Git blob SHA, and local SHA-256. Treat it as a supplied third-party mark, not proof that the repository owns the trademark.
4. **Lobe.** When Lobe covers the named AI/tool identity and a stronger source above is not available, resolve the visual through the current Lobe instructions and pin the package/version.
5. **HOLD.** If identity provenance remains ambiguous, return `HOLD: verified identity asset required`.

Do not redraw, approximate, prompt-generate, trace, invent a mascot, silently substitute a different brand mark, or use a logo merely because it looks familiar.

## Vibe SVGs boundary

Vibe SVGs is useful as a curated source and discovery index, but its asset classes are not interchangeable.

Repository:

`https://github.com/imMamdouhaboammar/vibe-svgs`

### Logos

`svgs/logos/README.md` identifies the supplied platform/tool marks and says third-party marks remain the property of their respective owners. When using a Vibe SVGs logo:

- use only a file under `svgs/logos/`
- pin a 40-character commit SHA, never `main`, `latest`, or another mutable ref in the provenance record
- record the repository path and Git blob SHA
- compute and record the localized file SHA-256
- preserve supplied geometry and identity colors
- allow only placement operations such as size, position, surrounding whitespace, and container alignment
- do not distort aspect ratio
- do not recolor unless the exact source itself provides an approved mono/color variant
- do not add strokes, shadows, gradients, masks, or decorative effects inside the mark
- do not merge the logo into another symbol or mascot
- do not claim that Vibe SVGs owns or officially endorses the mark

The asset-plan `identity_status` for this class is `supplied-third-party-mark` and its `alteration_policy` is `placement-only`.

### Mascots and scenes

Vibe SVGs `asset-manifest.json` marks mascot and scene artwork with `communityArtwork: true`; the catalog describes those examples as fan-made/community artwork. A Vibe SVGs community mascot **must not be called official** and must never satisfy an official-mascot requirement by itself.

A community mascot may be used only when all of these are true:

- the brief permits community/fan-made artwork rather than requiring the official mascot
- exact Vibe SVGs commit, path, blob SHA, and local SHA-256 are pinned
- `community_artwork: true`
- `identity_status: community-artwork`
- `user_confirmed: true`
- final copy and metadata do not imply official endorsement or ownership

If the user asks for the original or official mascot, resolve an exact user-supplied or original-owner asset. If that cannot be verified, HOLD. Do not downgrade silently to community artwork.

## Lobe resolution

Read `https://lobehub.com/icons/skill.md` before choosing a Lobe slug or import and follow the current `@lobehub/icons` instructions.

Prefer:

- `@lobehub/icons-static-svg` for supported logos
- `@lobehub/icons-static-avatar` for supported avatar or mascot identity assets only when the identity status is appropriate for the brief

Record exact slug and versioned package or immutable source reference. A remote URL may help resolve the source, but final HTML must use a local or embedded copy so render capture is deterministic.

## Integrity lock

Every approved identity asset becomes identity-locked before creative direction. Record a SHA-256 for localized files. Downstream workers may not replace or mutate those bytes without reopening asset resolution.

For SVG identity assets, identity lock protects at minimum:

- outer silhouette and viewBox relationship
- identity-defining path geometry
- identity colors and approved variants
- mascot face/character geometry
- wordmark spelling and letterforms
- aspect ratio

Placement transforms are allowed. Path editing, identity recoloring, wordmark reconstruction, mascot redrawing, or unapproved variant swaps are identity mutation and block delivery.

## Asset plan

Before creative direction, produce one record per named identity with:

- `name`
- `kind`
- `source_type`: `user-official`, `original-owner`, `lobe`, `vibe-svgs-logo`, or `vibe-svgs-community`
- `source_ref`
- `render_disposition`: `local` or `embedded`
- local path when applicable
- `identity_locked: true`
- `status: PASS`

For `original-owner`, also record `source_owner` and `integrity_sha256`.

For Lobe, also record `lobe_slug` and the versioned package.

For Vibe SVGs, also record `source_repo`, `source_commit`, `source_path`, `source_blob_sha`, `integrity_sha256`, and `identity_status`. Vibe SVGs logos require `alteration_policy: placement-only`. Vibe SVGs community artwork requires `community_artwork: true` and `user_confirmed: true`.

An empty asset list is valid when the story contains no named identity assets.

## Final checks

Fail or HOLD when:

- a required named identity has no verified source
- an official mascot is replaced by community/fan-made artwork
- Vibe SVGs provenance is mutable or unpinned
- the final visual uses a generated, traced, or approximate identity
- a wordmark is reconstructed or misspelled
- aspect ratio is distorted
- identity geometry or colors differ from the approved source without an approved variant
- final HTML still depends on a remote logo/avatar request
- provenance cannot identify the exact bytes used

A HOLD protects the identity boundary. It is not permission to create a lookalike.
