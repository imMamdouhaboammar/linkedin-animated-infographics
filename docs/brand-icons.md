# Brand icons and identity assets

Named AI/tool marks must come from exact, inspectable sources instead of model memory.

## Source precedence

Use the identity source policy in `skills/info-stories/references/asset-source-policy.md`:

1. exact user-supplied official asset
2. original-owner source when inspectable
3. pinned Vibe SVGs logo mirror for platform/tool logos
4. verified Lobe asset for covered identities
5. HOLD

A familiar-looking redraw is never an acceptable fallback.

## Vibe SVGs

Repository: https://github.com/imMamdouhaboammar/vibe-svgs

Vibe SVGs gives the workflow a broader open repository to inspect for platform/tool logos and community visual assets.

### Platform/tool logos

Only files under `svgs/logos/` may satisfy the `vibe-svgs-logo` source class. The Vibe SVGs logo catalog states that third-party marks remain the property of their respective owners and should be kept intact.

For every imported logo record:

- exact repository `source_commit`, never `main`/`latest`
- `source_path`
- Git `source_blob_sha`
- localized `integrity_sha256`
- `identity_status: supplied-third-party-mark`
- `alteration_policy: placement-only`
- local/embedded render disposition

The mark may be sized and positioned. Do not distort it, rebuild it, add internal decoration, modify identity geometry/colors, or imply endorsement.

### Mascots are different

Vibe SVGs `asset-manifest.json` marks its mascot/scene work with `communityArtwork: true` and describes examples as fan-made/community artwork.

That is useful creative material, but it is not an official-mascot authority.

If the brief explicitly accepts community artwork, a pinned Vibe SVGs mascot may be used with `identity_status: community-artwork`, `community_artwork: true`, and `user_confirmed: true`.

If the user asks for the official/original mascot, the workflow must resolve an exact user-supplied or original-owner asset. Otherwise it returns HOLD. Community artwork is never silently upgraded to official status.

## Lobe source

The repository also maintains a deterministic Lobe-backed logo cache.

| | |
|---|---|
| Package | `@lobehub/icons-static-svg` |
| Version | pinned in `assets/brand-icons/manifest.json` |
| Upstream | https://github.com/lobehub/lobe-icons |
| Gallery | https://lobehub.com/icons |
| Licence | MIT |

The MIT licence covers packaging/code, not ownership of third-party marks. It does not carry trademark ownership, endorsement rights, or permission to present a third-party identity as ours. Every logo remains the trademark of its owner. Use it nominatively to identify a product that genuinely appears in the story. Do not use marks as decoration or imply a partnership/integration that does not exist.

Before resolving through Lobe, read `https://lobehub.com/icons/skill.md` and follow current package/slug instructions rather than guessing from memory.

## Scope and mixed-set rule

The Lobe set covers AI/LLM identities broadly but not every social, advertising, analytics, or general software platform. Vibe SVGs may cover some additional platform/tool logos, but neither source should be treated as universal.

If a zone names several platforms and only some have verified marks, do not create a visually inconsistent half-branded row by accident. Either resolve every required mark or deliberately use literal product names for the whole zone. Record the decision.

## Existing Lobe helper

```bash
python3 tools/brand_icon.py list --query claude
python3 tools/brand_icon.py fetch claude --variant color
python3 tools/brand_icon.py fetch openai
python3 tools/brand_icon.py check
```

Variants are `color`, `mono`, `text`, and `brand`. A color request may fall back to the source package's monochrome mark when that is the only supplied variant; it still may not synthesize a new brand treatment.

Marks land in `assets/brand-icons/` with provenance carrying resolved name, source URL, pinned version, licence/trademark note, SHA-256, and fetch date.

## Remote SVG safety

Any fetched SVG is untrusted remote input before validation. Reject:

- `<script>`, `<style>`, `<foreignObject>`, `<iframe>`, `<audio>`, or `<video>`
- `on*` event handler attributes
- external `href`/`src` references
- `javascript:` or HTML data URLs
- CSS pulling external `url()` resources
- DOCTYPE/entity declarations
- oversized payloads
- anything that does not parse as SVG XML

Final artboards must inline or localize validated SVG assets. Render capture must not depend on remote logo requests.

## Identity integrity

Every approved identity becomes identity-locked before creative direction.

Protected properties include:

- SVG path geometry defining the mark/character
- viewBox/aspect relationship
- identity colors and exact approved variants
- wordmark spelling and letterforms
- mascot face/character-defining geometry

Downstream workers may position/scale approved assets. Any byte-changing identity edit requires reopening asset resolution and recording a new integrity digest.

## Story job

A verified logo can still be bad design if it has no communication job. Use a mark to identify an entity, source, destination, comparison member, or verified tool state. A logo wall with no story purpose fails regardless of asset provenance.

Mascots require an even stronger job: reading pointer, state confirmation, payoff, route follower, or another explicit communication role. Decorative character motion is not enough.
