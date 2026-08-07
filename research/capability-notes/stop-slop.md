# stop-slop capability note

Source: https://github.com/hardikpandya/stop-slop
Inspected commit: `8da1f030185bdfe8471220585162991eaeb970e9`
License: MIT

## Adopt

- Detect named prose patterns instead of guessing whether text was AI-written
- Remove throat-clearing, rhetorical setup, binary contrast, negative listing, dramatic fragmentation, and generic declarations
- Prefer concrete actors, verbs, facts, and direct reader language
- Vary sentence rhythm and avoid repetitive paragraph endings
- Run a compact pre-delivery writing gate

## Adapt for Info-stories

- Apply the checks to headline, subline, card copy, labels, CTA, and caption independently
- Preserve intentional fragments when they are labels or diagram nodes
- Treat active voice as a preference for explanatory prose, not a rule for every UI label
- Turn subjective scoring into named pass/fail findings that point to the exact text slot

## Reject

- A universal ban on all adverbs. Some are meaningful and removing them mechanically changes meaning
- A universal ban on every Wh-word sentence. Questions can be legitimate story devices when the brief calls for them
- Rewriting strong user voice only to satisfy stylistic uniformity

## Local targets

- `skills/info-stories/references/anti-slop-gates.md`
- `agents/copy-compressor.md`
- `agents/post-critic.md`
- `tests/test_info_stories.py`
