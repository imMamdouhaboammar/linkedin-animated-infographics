# Study protocol

Use this when the user supplies one or more reference images, GIFs, a prior artifact, or a public page and wants the design principles carried into a new Info-story.

## Principle

Extract design DNA, not pixels. The output is a diagnosis and a set of compatible local choices. Do not copy source wording, logos, photography, illustrations, or signature composition details that would turn the new artifact into a replica.

## Source handling

Choose one primary reference as the structural backbone. Additional references may inform one named axis such as colour, density, or motion, but do not average five unrelated references into one style.

Record provenance as one of: user-owned work, public reference, licensed asset, or unknown. If the source looks like a paid template listing or distinctive signature work and the user asks for a close reproduction, stop at diagnosis and propose a different local composition.

## Analysis passes

1. **Surface**: paper/background temperament, surface hierarchy, accent footprint, line strength, texture, and token roles
2. **Type roles**: display, body, labels, mono/code role, weight hierarchy, line-height character. From a screenshot, describe roles rather than claiming an exact typeface
3. **Structure**: title zone, visual anchor, zone topology, card grammar, connector grammar, footer/attribution placement, repeated modules, asymmetry
4. **Rhythm**: density, whitespace distribution, large-to-small scale jumps, content count, repeated gaps, reading cadence
5. **Motion**: only when visible in GIF/video or described by the user. Record reveal order, active-state logic, connector motion, pointer behavior, and whether frame 0 remains complete
6. **Copy boundaries**: note source phrases or branded language that must not be copied

## Required report

Return a JSON-compatible object with: `source`, `source_kind`, `provenance`, `surface`, `type_roles`, `structure`, `rhythm`, `motion`, `visual_anchor`, `recommendations`, and `copy_boundaries`.

`recommendations` must contain ranked candidates for `house`, `style`, `archetype`, and `motion`. The report does not build anything. Validate it with `validate_study_report()` before handoff.

## Study to build handoff

The studied DNA can override catalog defaults only after the user accepts the diagnosis. Even then, keep hard constraints: contrast, safe margin, first-frame completeness, motion budget, honest claims, and attribution.
