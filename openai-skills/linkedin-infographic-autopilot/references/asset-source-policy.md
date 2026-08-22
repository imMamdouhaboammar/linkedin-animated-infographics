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

Use only files under `svgs/logos/`. Pin commit, path, Git blob SHA, and localized SHA-256. Preserve supplied geometry, identity colors, wordmarks, and aspect ratio. Allow placement only. Do not add internal decoration or claim Vibe SVGs owns/endorses the third-party mark.

Use `identity_status: supplied-third-party-mark` and `alteration_policy: placement-only`.

### Mascots and scenes

Vibe SVGs `asset-manifest.json` marks mascot and scene artwork with `communityArtwork: true`; those assets are community/fan-made and **must not be called official**.

They may be used only when the brief permits community artwork, exact commit/path/blob/SHA-256 are pinned, `community_artwork: true`, `identity_status: community-artwork`, and `user_confirmed: true`.

If the user asks for the original/official mascot, require an exact user-supplied or original-owner asset. Otherwise HOLD.

## Lobe resolution

Read `https://lobehub.com/icons/skill.md` before choosing a Lobe slug/import. Prefer versioned `@lobehub/icons-static-svg` for logos and use avatar assets only when their identity status fits the brief. Final render assets must be local or embedded.

## Integrity lock

Approved identity assets are identity-locked. Record SHA-256 for localized bytes. Protect identity geometry, colors, wordmark spelling/letterforms, mascot-defining geometry, and aspect ratio. Placement transforms are allowed; identity mutation is not.

## Asset-plan fields

Every named identity includes `name`, `kind`, `source_type`, `source_ref`, `render_disposition`, `identity_locked: true`, and `status: PASS` plus source-specific provenance.

For Vibe SVGs include `source_repo`, `source_commit`, `source_path`, `source_blob_sha`, `integrity_sha256`, and `identity_status`. Logos also require `alteration_policy: placement-only`; community artwork requires `community_artwork: true` and `user_confirmed: true`.

## Blocking checks

HOLD or FAIL when a named identity lacks verified provenance, an official mascot is replaced by community artwork, a Vibe SVGs source is mutable/unpinned, a wordmark is reconstructed, aspect ratio is distorted, identity paths/colors differ from the approved source without an approved variant, a generated/traced lookalike is used, or final render depends on a remote identity request.
