# Identity asset source policy

This contract applies whenever an infographic names or visually depicts an official AI model, AI application, provider, tool identity, logo, or mascot.

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

`svgs/logos/README.md` identifies the supplied platform/tool marks and explicitly says third-party marks remain the property of their respective owners. When using a Vibe SVGs logo:

- use only a file under `svgs/logos/`
- pin a 40-character commit SHA, never `main`, `latest`, or another mutable ref in the provenance record
- record the repository path and Git blob SHA
- compute and record the localized file SHA-256
- preserve the supplied geometry and identity colors
- allow only placement operations such as size, position, surrounding whitespace, and container alignment
- do not distort aspect ratio
- do not recolor unless the exact source itself provides an approved mono/color variant
- do not add strokes, shadows, gradients, masks, or decorative effects inside the mark
- do not merge the logo into another symbol or mascot
- do not claim that Vibe SVGs owns or officially endorses the mark

The asset-plan `identity_status` for this class is `supplied-third-party-mark` and its `alteration_policy` is `placement-only`.

### Mascots and scenes

Vibe SVGs `asset-manifest.json` marks its mascot and scene artwork with `communityArtwork: true`; the catalog describes those examples as fan-made/community artwork. That means a Vibe SVGs community mascot **must not be called official** and must never satisfy an official-mascot requirement by itself.

A community mascot may be used only when all of these are true:

- the brief permits community/fan-made artwork rather than requiring the official mascot
- the exact Vibe SVGs commit, path, blob SHA, and local SHA-256 are pinned
- `community_artwork: true`
- `identity_status: community-artwork`
- `user_confirmed: true`
- the final copy and metadata do not imply official endorsement or ownership

If the user asks for the original or official mascot, resolve an exact user-supplied or original-owner asset. If that cannot be verified, HOLD. Do not downgrade silently to community artwork.

## Lobe resolution

Before resolving a Lobe asset, read:

`https://lobehub.com/icons/skill.md`

Follow the current instructions for `@lobehub/icons` rather than assuming stale component or slug names.

For deterministic infographic production, prefer:

- logos: `@lobehub/icons-static-svg`
- supported avatars or mascot-like identity assets: `@lobehub/icons-static-avatar`

A CDN or package registry may be used during resolution. The final artboard must reference a local or embedded copy so frame capture does not depend on network availability.

Record the exact Lobe slug, package, and resolved package version or immutable source reference. Do not write `latest` into final provenance when a concrete version can be resolved.

## Integrity lock

Every approved identity asset becomes identity-locked before creative direction.

For local files, record a SHA-256 after resolution. Downstream workers may not replace or mutate the file without reopening asset resolution and generating a new integrity record.

For SVG identity assets, identity lock protects at minimum:

- outer silhouette and viewBox relationship
- path geometry that defines the mark/character
- identity colors and approved variants
- facial or character-defining geometry for mascots
- wordmark spelling and letterforms
- aspect ratio

Placement transforms are not identity mutation. Editing the paths, changing identity colors, redrawing facial features, adding brand-internal decoration, or swapping one variant for another without approval is identity mutation.

## Asset artifact

`asset-curator` writes `build/asset-plan.json`.

The top level contains `assets`, an array of records. Every record includes:

- `name`
- `kind`
- `source_type`: `user-official`, `original-owner`, `lobe`, `vibe-svgs-logo`, or `vibe-svgs-community`
- `source_ref`
- `render_disposition`: `local` or `embedded`
- `local_path` when local
- `identity_locked: true`
- `status: PASS`

Additional required provenance depends on source type.

For `original-owner`:

- `source_owner`
- `integrity_sha256`

For `lobe`:

- `lobe_slug`
- versioned `package`

For either Vibe SVGs source:

- `source_repo: imMamdouhaboammar/vibe-svgs`
- `source_commit`
- `source_path`
- `source_blob_sha`
- `integrity_sha256`
- `identity_status`

Vibe SVGs logos also require `alteration_policy: placement-only`.

Vibe SVGs community artwork also requires `community_artwork: true` and `user_confirmed: true`.

The artifact may contain an empty `assets` array when the brief contains no named identity assets.

## Downstream contract

`creative-director`, `layout-composer`, `artboard-builder`, `mascot-animator`, `post-critic`, and `story-verifier` consume the approved asset plan.

They may change size, placement, animation transform, and an explicitly approved source variant. They may not switch identity source, mutate identity geometry, invent replacement artwork, or reinterpret a community mascot as official.

The final HTML must not depend on a remote logo or avatar URL.

## Blocking checks

Return HOLD or FAIL when any of these occur:

- a named identity has no verified source
- an official mascot is replaced with fan-made/community artwork
- a Vibe SVGs source uses `main`, `latest`, or another mutable ref instead of a pinned commit
- source path, Git blob, or localized SHA-256 is missing for a Vibe SVGs asset
- a required identity differs materially from the approved source
- a wordmark is misspelled or reconstructed
- aspect ratio is distorted
- identity geometry or colors are edited without an approved source variant
- a generated or traced lookalike is used
- the final render depends on a remote asset request
- provenance cannot identify the exact bytes used

A HOLD protects the identity boundary. It is not permission to make a lookalike.
