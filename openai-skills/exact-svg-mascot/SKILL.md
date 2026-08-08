---
name: exact-svg-mascot
description: Animate a named or official mascot using the exact user-supplied SVG while preserving its identity. Use when the mascot asset must not be redrawn, substituted, approximated, or silently regenerated.
---

# Exact SVG Mascot

## Purpose

Animate the exact SVG supplied by the user without changing the mascot's identity.

This is an asset-integrity workflow. The supplied SVG is the identity source.

## Blocking asset gate

Before animation:

1. confirm an SVG file was supplied or is directly available to the task
2. confirm the file is actually SVG content and can be read
3. preserve an untouched source copy or source representation for comparison
4. inspect `viewBox`, visible groups/elements, transforms, clipping, and IDs/classes that may support animation

If the exact SVG is missing, unreadable, or not actually SVG, return `HOLD` and request the exact asset.

Do not:

- redraw the mascot
- generate a lookalike
- substitute another mascot
- trace a raster image into a replacement
- replace the identity with emoji, iconography, or a generic character

## Motion directions

Develop 2-3 motion directions around geometry that already exists in the SVG. Examples include:

- whole-character entrance or travel
- head/body/limb motion when the SVG structure safely supports it
- eye or expression changes only when the original SVG contains appropriate elements
- prop movement when the prop is part of the supplied SVG
- reading-pointer movement that guides attention through the infographic

Do not invent new facial features, body parts, logos, or branded details.

## Implementation rules

Prefer non-destructive animation:

- CSS transforms on existing SVG groups
- SVG transforms on existing elements
- opacity changes on existing elements
- clip or mask animation only when existing identity remains intact
- wrapper movement around the untouched SVG when internal rigging is unsafe

Avoid rewriting path geometry unless the user explicitly asks for a morph and identity preservation can be verified.

The final animated composition must keep the original mascot recognizable at every important frame.

## Identity check

Before delivery compare the animated mascot with the original source for:

- silhouette
- proportions
- colors
- logo/brand markings
- face and defining features
- accessory placement

Any unintended identity drift is blocking.

## Output

Return:

- asset validation verdict
- selected motion direction
- which original SVG elements are animated
- identity-preservation notes
- final artifact or integration instructions
- final verdict: `PASS`, `FAIL:fixable`, or `HOLD`

Never complete a named-mascot request by substituting an asset when the exact SVG gate fails.
