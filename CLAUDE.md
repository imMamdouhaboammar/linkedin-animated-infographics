# Claude Code Guide

This repository is a same-repository Claude Marketplace plugin. Treat its helper registries, agents, skills, research gates, runtime contracts, and validators as one executable contract.

## First read

Read `helper/GUIDE.md` before selecting a skill or subagent.

The authoritative machine-readable files are:

- `helper/router.json`
- `helper/capabilities.json`
- `helper/quality-gates.json`
- `helper/artifacts.json`
- `helper/modules.json`
- `helper/runtime-contract.json`
- `helper/artifact-views.json`
- `helper/cache-policy.json`
- `helper/model-policy.json`
- `helper/token-budgets.json`
- `research/capability-notes/gates.json`
- `architecture/plugin-graph.json`
- merged Info-stories registry from `scripts.info_stories.py::load_catalog()`

Supporting source contracts:

- `skills/info-stories/references/asset-source-policy.md`: Lobe-first verified identity behavior
- `skills/info-stories/references/typography-direction.md`: intentional typography behavior

Run:

```bash
python3 scripts/ecosystem_doctor.py check
python3 scripts/runtime_context.py check
```

after changing skills, agents, tools, routes, capabilities, artifacts, gates, runtime policies, or module inventory.

## Claude orchestration rule

Subagents do not orchestrate peer subagents. The main/parent workflow owns sequencing and HOLD resolution.

For complete post creation, use `new-post` and follow the graph:

`design-study -> evidence-checker -> asset-curator -> creative-director -> story-architect -> palette-curator -> type-curator -> copy-compressor -> layout-composer -> caption-writer -> artboard-builder -> motion-director -> optional mascot-animator -> motion-engineer -> render-qa -> post-critic -> story-verifier`

Required skill knowledge is preloaded through each agent's `skills:` frontmatter. Runtime capsules add focused state; they do not weaken skill, evidence, quality-gate, or HOLD contracts.

## Token-efficient runtime protocol

For a complete production run, write the normalized request once to `build/runtime-context/request.json`. Include the topic or source identity, audience, language, output mode, CTA, and approved constraints that can change stage output.

Before spawning a stage that `helper/cache-policy.json` marks cacheable, run:

```bash
python3 scripts/runtime_context.py prepare --intent create-post --stage <agent> --workspace .
```

- If the result has `cache_hit=true`, treat it as `CACHE HIT`: use the restored registered output and do not spawn that worker.
- If the request record is missing or invalid, cache reuse is disabled for that stage.
- On a miss, spawn the worker normally. The generated `build/runtime-context/<agent>.json` is the focused runtime capsule for that stage.
- After the worker output passes its blocking stage gates, store the exact result with:

```bash
python3 scripts/runtime_context.py store --intent create-post --stage <agent> --workspace .
```

The cache is exact, content-addressed, request-bound, local-only, and never semantic. `post-critic` and `story-verifier` always run fresh. A cache hit never overrides a HOLD, approval requirement, evidence rule, or final verification.

## Creative behavior

- `asset-curator` applies Lobe-first verified identity sourcing after exact user-supplied official assets. Supported named AI/tool identities use Lobe; unresolved named identities HOLD rather than becoming lookalikes
- `creative-director` runs after verified assets and before story architecture, producing multiple evidence-safe directions with explicit relationship, anchor, containment, negative space, and motion job
- hero/design copy must satisfy `hooked-design-copy`, not merely report the topic
- complete concepts should create a useful `creative-payoff` and pass `clean-creative-structure`
- palette default is `creative-attractive-restrained`
- `type-curator` applies intentional typography before copy fitting. Explicit/supplied render-safe fonts win; remote font loading during capture is forbidden
- composition default is `center-first` with evidence/comprehension-driven exceptions only
- a verified identity may come from an exact user/task SVG or an approved Lobe asset; downstream workers preserve the exact local SVG rather than substituting it

## Research behavior

`research/capability-notes/gates.json` is active production guidance, not optional background reading. Apply the route's gate IDs and keep provenance in `research/capability-notes/sources.json`. Never package ignored upstream clones.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tools skills/svg-mascot-animator/scripts
python3 scripts/info_stories.py check
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/runtime_context.py check
python3 scripts/validate_marketplace.py
python3 scripts/validate_codex_plugin.py
python3 scripts/validate_antigravity_plugin.py
claude plugin validate .
```

The CI also registers this repository as marketplace `mamdouh-creative-tools` and installs `linkedin-animated-infographics@mamdouh-creative-tools` from a clean checkout.

<!-- MASTERONE:START -->
## MasterOne project profile

Before LinkedIn infographic production:

1. Read `.linkedin-infographics/profile.json` when present
2. Use `masterone` for first-run onboarding and profile readiness
3. Ask only for materially missing inputs
4. Treat discovered assets as candidates until confirmed
5. Preserve the canonical downstream workflows from `helper/router.json`
6. Never invent copyright, attribution, fonts, official logos, mascot identity, or reference intent

MasterOne manages only this bounded section. `new-post` remains the complete-production parent workflow.
<!-- MASTERONE:END -->
