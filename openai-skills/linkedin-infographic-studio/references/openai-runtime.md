# OpenAI runtime contract

This distribution is designed for ChatGPT and Codex installations that receive skills without the repository's Claude worker runtime.

## Execution model

Run one parent workflow as explicit sequential passes. Do not assume that named Claude workers, repository-scoped subagents, helper routing files, or hidden peer-to-peer handoffs are available.

A role name in this distribution describes a reasoning pass, not a process that must exist as a separately registered agent.

Each pass must consume the artifacts from earlier passes and emit a bounded artifact before the next pass begins.

## Required sequence

1. Evidence inventory
2. Asset curator and verified identity plan
3. Creative directions
4. Story architecture
5. Palette contract
6. Type curator and typography contract
7. Copy compression
8. Macro layout
9. Still construction
10. Still critique and targeted repair
11. Motion direction when animated output is requested
12. Motion implementation
13. Render QA
14. Adversarial visual critique
15. Final verification

Do not collapse evidence, asset sourcing, concept, type, copy, layout, motion, and QA into a single generation pass.

## Identity source boundary

Read `asset-source-policy.md` before concepting when a named official AI/tool identity is required. Exact user-supplied official assets take precedence. Supported named AI/tool identities use Lobe after reading `https://lobehub.com/icons/skill.md`. Missing verified identities HOLD instead of being approximated.

Remote URLs may help resolve an identity, but final HTML uses a local or embedded copy.

## Typography boundary

Read `typography-direction.md` before copy fitting. Explicit user typography takes precedence when render-safe. Otherwise use supplied/local assets or a curated deterministic system direction. Remote @import and render-time network font requests fail.

## Host isolation

This OpenAI distribution must be usable without reading repository paths outside this skill folder. It must not require Claude-only agents, Claude plugin environment variables, repository helper routing, or the repository worker graph.

The Lobe source policy is an external public source instruction, not a dependency on the parent repository. If the active host cannot retrieve or verify a required identity source, return HOLD instead of guessing.

The existing Claude implementation remains authoritative for Claude. Do not rewrite Claude behavior from this skill.

## Approval and repair behavior

When interactive review is possible, show the selected creative direction before still construction and show the still before motion.

When interactive review is not possible, run the same gates internally and continue only after the still passes.

A blocking visual, evidence, identity, typography, or render-safety failure triggers a targeted repair. Allow no more than two targeted repair attempts. A third unresolved blocking failure returns a precise HOLD or FAIL instead of shipping weak output.

## Output principle

Quality parity does not mean identical visual output. The OpenAI runtime may choose a different layout, art direction, palette, archetype, or motion treatment from Claude. It must preserve the same discipline: evidence first, verified identity plan before concept, concept before styling, intentional type before copy fitting, macro layout before detail, still before motion, and independent critique before delivery.
