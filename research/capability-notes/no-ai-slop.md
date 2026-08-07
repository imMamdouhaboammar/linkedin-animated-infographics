# no-ai-slop capability note

Source: https://github.com/petergyang/no-ai-slop
Inspected commit: `d30eddb9e04562234f2070b5ee63ca4649d9a05e`
License: MIT

## Adopt

- Preserve the writer's real voice and make the minimum effective edit
- Use a portability test: a sentence that could move unchanged to another product is probably filler
- Protect specific facts, mechanisms, numbers, and named examples
- Detect faux-insight setups, importance puffery, interpretive metadiscourse, synonym cycling, robotic rhythm, recap endings, and weasel attribution
- Separate detect from edit behavior
- Require a final self-evaluation after editing

## Adapt for Info-stories

- The copy-compressor first records the factual payload and voice signals, then compresses
- A detect-only mode returns slot, pattern, evidence, and fix direction without rewriting
- Fact slots cannot be compressed into broader claims
- Layout labels may repeat the same noun when repetition improves diagram clarity

## Reject

- Any rule that assumes long-form prose when the slot is a badge, node, command, or table label
- Guessing authorship from prose patterns
- Inventing replacement examples to make copy feel more specific

## Local targets

- `skills/info-stories/references/anti-slop-gates.md`
- `agents/copy-compressor.md`
- `agents/evidence-checker.md`
- `agents/post-critic.md`
