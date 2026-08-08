# OpenAI runtime contract

This distribution is designed for ChatGPT and Codex installations that receive skills without the repository's Claude worker runtime.

## Execution model

Run one parent workflow as explicit sequential passes. Do not assume that named Claude workers, repository-scoped subagents, helper routing files, or hidden peer-to-peer handoffs are available.

A role name in this distribution describes a reasoning pass, not a process that must exist as a separately registered agent.

Each pass must consume the artifacts from earlier passes and emit a bounded artifact before the next pass begins.

## Required sequence

1. Evidence inventory
2. Creative directions
3. Story architecture
4. Palette contract
5. Copy compression
6. Macro layout
7. Still construction
8. Still critique and targeted repair
9. Motion direction when animated output is requested
10. Motion implementation
11. Render QA
12. Adversarial visual critique
13. Final verification

Do not collapse concept, copy, layout, motion, and QA into a single generation pass.

## Host isolation

This OpenAI distribution must be usable without reading repository paths outside this skill folder. It must not require Claude-only agents, Claude plugin environment variables, repository helper routing, or the repository worker graph.

The existing Claude implementation remains authoritative for Claude. Do not rewrite Claude behavior from this skill.

## Approval and repair behavior

When interactive review is possible, show the selected creative direction before still construction and show the still before motion.

When interactive review is not possible, run the same gates internally and continue only after the still passes.

A blocking visual or evidence failure triggers a targeted repair. Allow no more than two targeted repair attempts. A third unresolved blocking failure returns a precise HOLD or FAIL instead of shipping weak output.

## Output principle

Quality parity does not mean identical visual output. The OpenAI runtime may choose a different layout, art direction, palette, archetype, or motion treatment from Claude. It must preserve the same discipline: evidence first, concept before styling, macro layout before detail, still before motion, and independent critique before delivery.
