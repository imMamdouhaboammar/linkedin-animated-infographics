# Ecosystem v3 Creative Runtime Addendum Plan

## Task A: Local creative quality gates

Files:
- Create `helper/quality-gates.json`
- Modify `scripts/ecosystem_router.py`
- Create `tests/test_creative_runtime.py`

Requirements:
- route result exposes `quality_gates`
- complete post and Info-story routes include `hooked-design-copy`, `creative-payoff`, `restrained-palette`, and `center-first-composition`
- local quality gates remain distinct from research provenance
- gate owners are real shipping agents

## Task B: Creative director

Files:
- Create `agents/creative-director.md`
- Modify `architecture/plugin-graph.json`
- Modify `helper/router.json`
- Modify `helper/capabilities.json`
- Modify `helper/artifacts.json`
- Modify `skills/new-post/SKILL.md`
- Modify `tests/test_plugin_graph.py`
- Extend `tests/test_creative_runtime.py`

Requirements:
- creative director runs after evidence and before story architecture
- creates `build/creative-concepts.json`
- produces at least three evidence-safe concept directions
- each direction contains visual hook, copy hook, aha mechanic, story shape, recommendations, evidence dependencies, and risk notes
- no peer orchestration

## Task C: Hook-driven design copy

Files:
- Create `skills/info-stories/references/hook-driven-design-copy.md`
- Modify `agents/creative-director.md`
- Modify `agents/copy-compressor.md`
- Modify `agents/caption-writer.md`
- Modify `agents/post-critic.md`
- Modify `skills/caption/SKILL.md`
- Modify `skills/info-stories/SKILL.md`

Requirements:
- hero copy must earn attention without fabricating stakes
- neutral factual labels remain literal where clarity wins
- generic portable hero statements fail
- one strong hook is preferred over cleverness in every slot

## Task D: Strict module reality doctor

Files:
- Create `helper/modules.json`
- Create `scripts/ecosystem_doctor.py`
- Create `tests/test_ecosystem_doctor.py`
- Modify CI workflow

Requirements:
- every public `skills/*/SKILL.md`, `agents/*.md`, and `tools/*.py` has a manifest entry
- every manifest path exists
- active skills/agents are reachable
- active tools are referenced by executable guidance or validator contracts
- each module names at least one test contract that exists
- capabilities, artifacts, local gates, research gates, router, and plugin graph cross-validate
- doctor fails on orphan or fake modules

## Task E: Resume Skills and Agents v3 refactor

After Tasks A-D are GREEN, resume the main v3 plan:
- refactor all skills to the v3 section contract
- refactor all agents to the v3 worker contract
- add helper/research/local-gate references
- update repository guidance, README, focused docs, Marketplace 3.0.0, and CI
- run external reviews and merge only from a verified green PR head
