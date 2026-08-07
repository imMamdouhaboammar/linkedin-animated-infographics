# taste-skill capability note

Source: https://github.com/Leonxlnx/taste-skill
Inspected commit: `e988add20dab0fa97d7a76781c48961c8184288e`
License: MIT

## Adopt

- Read the brief and reference signals before choosing a visual direction
- Track design variance, motion intensity, and visual density as explicit design decisions
- Prevent structural repetition, not only palette repetition
- Lock shape, accent, and typography decisions once chosen
- Require motion to communicate hierarchy, sequence, feedback, or state
- Audit visible copy and reject fabricated precision
- Use a mechanical pre-flight rather than taste-by-feeling alone

## Adapt for Info-stories

- Map the three dials onto a 1080x1350 infographic rather than a responsive website
- Structural variance means different story-zone arrangements, card grammars, connectors, hero ratios, and density patterns
- Motion intensity remains bounded by the existing changed-pixel budget and seekable animation contract
- One Story House owns the token set for a single artifact

## Reject

- React, Next.js, Tailwind, dark-mode, navigation, form-state, and Core Web Vitals rules that do not apply to rendered LinkedIn artboards
- Mandatory GSAP or scroll-driven motion. This project captures deterministic CSS/SMIL animations
- Simulated random choice. Selection must be explainable and deterministic from content shape
- A global ban on warm-paper palettes. Warm editorial houses are a deliberate part of this product

## Local targets

- `skills/info-stories/references/design-taste-gates.md`
- `agents/story-architect.md`
- `agents/layout-composer.md`
- `agents/motion-director.md`
- `tests/test_info_stories.py`
