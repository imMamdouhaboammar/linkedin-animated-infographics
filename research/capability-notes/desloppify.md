# desloppify capability note

Source: https://github.com/peteromallet/desloppify
Inspected commit: `3a7735d531a96b6a226bfbdc9fd662b14195f857`
License: MIT

## Adopt

- Systematic multi-pass loop combining mechanical scan and structural review
- Persistent state tracking across execution rounds to maintain quality momentum
- Dead component and redundant visual element removal
- Strict refusal of gaming metrics; actual code and visual improvements required
- Bounded iterative remediation loops with clear resolution criteria

## Adapt for Info-stories

- Adapt mechanical scan to detect dead DOM containers, unreferenced CSS classes, and redundant SVG glyphs
- Use the repair queue pattern for `post-critic` and `render-qa` iterations
- Bind scorecard criteria to the six-axis pre-emit critique (Philosophy, Hierarchy, Execution, Specificity, Restraint, Variety)

## Reject

- Language-specific AST parsers for non-web targets outside our Python/HTML/CSS/SVG stack
- Multi-repo git tracking state files (`.desloppify/`) inside committed artifacts

## Local targets

- `skills/info-stories/references/ui-taste-engineering.md`
- `skills/info-stories/references/anti-slop-gates.md`
- `agents/post-critic.md`
- `agents/render-qa.md`
