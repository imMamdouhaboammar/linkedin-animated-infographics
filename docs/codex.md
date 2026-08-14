# Codex and ChatGPT

Version 3.5.0 gives Codex and ChatGPT a capability-negotiated OpenAI autopilot distribution while preserving the existing Claude execution path.

The target is quality and process parity, not identical visual output. Claude and OpenAI may choose different creative directions, layouts, palettes, and motion treatments, but both must follow disciplined evidence, concept, layout, still QA, motion, and verification stages.

## Native OpenAI package

The OpenAI plugin entry point is:

```text
.codex-plugin/plugin.json
```

It declares a skills-only plugin and points to:

```text
./openai-skills/
```

The primary full-production public workflow is:

```text
openai-skills/linkedin-infographic-autopilot/
```

Focused public skills remain available for full studio production, review, exact-SVG mascot work, and community sharing.

The public OpenAI distribution does not depend on Claude worker registration, `.claude-plugin/`, repository `agents/`, repository helper routing, `.codex/config.toml`, or `.codex/agents/` at runtime.

The repository marketplace remains:

```text
.agents/plugins/marketplace.json
```

## Autopilot execution model

The OpenAI parent observes the capabilities actually exposed by the current host before it chooses an execution path.

Unknown capabilities fail closed as unavailable.

The execution paths are:

```text
full-autopilot
  real side jobs + the execution capabilities required for the deliverable

tool-rich-sequential
  useful sandbox/tools + sequential role contracts

safe-skill-only
  bounded reasoning only, with HOLD when execution is required
```

The preference order is:

```text
full-autopilot > tool-rich-sequential > safe-skill-only
```

The parent never reports the stronger path when it had to degrade.

## Capability classes

The runtime tracks these capabilities independently:

- `subagents`
- `sandbox_write`
- `shell_or_code_execution`
- `image_inspection`
- `web_research`
- `connected_apps`
- `workspace_agents`
- `publishing_tools`

A capability counts as available only after it is observed in the current host. Documentation or repository configuration alone is not enough.

## Real side jobs

Evidence is a dependency, not a peer creative job.

The parent first completes `evidence-research` and finalizes the supported, unsupported, contradicted, freshness-sensitive, and protected-fact boundary.

After that evidence artifact is finalized, real delegation may run these independent creative jobs concurrently:

- creative-direction exploration
- visual-archetype exploration
- copy-compression critique

The parent waits for all required bounded results and remains responsible for synthesis and final decisions.

Production jobs with dependencies remain ordered:

- still construction
- complete still critique
- targeted repair
- motion direction
- motion implementation
- render QA
- final verification

Multiple workers do not write the same shared artifact concurrently unless the host gives them isolated workspaces and an explicit merge step.

## Executable runtime helper

When code execution is available, the public skill can use:

```text
openai-skills/linkedin-infographic-autopilot/scripts/autopilot_runtime.py
```

The helper provides deterministic behavior for:

- capability normalization
- execution-path selection
- evidence-first side-job dispatch planning
- sandbox workspace scaffolding

It does not discover capabilities by itself. The parent passes only capabilities already observed in the current host.

Example operations:

```text
python scripts/autopilot_runtime.py select-path --capabilities-json '<observed-json>'
python scripts/autopilot_runtime.py dispatch-plan --capabilities-json '<observed-json>'
python scripts/autopilot_runtime.py init-workspace <task-workspace>/work
```

If code execution is unavailable, the skill applies the same contracts directly and does not claim the helper ran.

## Sandbox artifact workspace

When write access is observed, the workflow persists logical artifacts for:

- evidence
- candidate concepts
- selected direction
- copy
- macro layout
- editable build
- still review
- motion plan
- render QA
- final verifier
- delivery inventory

This makes later QA consume the same inputs and outputs that production actually used instead of relying on transient conversation context.

Workspace initialization creates directories only. It does not fabricate evidence, builds, renders, QA reports, or final artifacts.

## Visual quality gates

The still gate is blocking before motion.

Autopilot ships its own complete copy of the blocking OpenAI visual quality floor so selecting the parent workflow cannot bypass the studio gate.

The complete gate includes:

- default 1080x1350 canvas unless the user requests another format
- roughly 82-92% usable vertical occupancy unless negative space has a clear compositional job
- rejection of unexplained gaps greater than 120px near the footer/final zone
- maximum bordered containment depth of two levels
- one dominant visual anchor at feed scale
- explicit macro rhythm and footer reservation
- per-item PASS/FAIL taxonomy for top-heavy composition, bottom dead zone, nested-card density, generic UI grammar, weak macro rhythm, weak visual anchor, footer detachment, motion on a weak still, decorative motion, and feed-scale legibility
- maximum two targeted repair attempts

Motion does not start until the full still taxonomy passes.

## Workspace Agents

Workspace Agents are an optional external execution capability.

Installing this skills-only plugin does not automatically create, register, publish, or invoke Workspace Agents.

If compatible callable Workspace Agents are actually exposed in the current host, the parent may use them for bounded jobs. Otherwise it falls back to Codex subagents when available or to sequential role contracts.

The public workflow never claims that a Workspace Agent ran when no callable agent was observed.

## Claude regression boundary

Claude keeps the existing canonical runtime:

- `skills/`
- `agents/`
- `helper/`
- `architecture/plugin-graph.json`
- `.claude-plugin/`

The 3.5.0 work does not replace Claude agents with OpenAI role passes. Claude remains on `native-worker-graph`. Only release version metadata is synchronized where repository parity requires it.

## Add the repository marketplace

With a Codex CLI release that supports plugins:

```bash
codex plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics --ref main
codex plugin marketplace list
```

Use supported Plugins Directory surfaces for installation and testing.

## Repository-scoped Codex subagents

`.codex/config.toml` and `.codex/agents/*.toml` are repository-development helpers. They are not a dependency of the installed public plugin.

Existing repository-maintenance roles remain:

- `explorer`
- `reviewer`
- `docs_researcher`

Version 3.5.0 also adds real project-scoped Codex adapters for canonical product workers:

- `creative_director` -> `agents/creative-director.md`
- `evidence_researcher` -> `agents/evidence-checker.md`
- `copy_director` -> `agents/copy-compressor.md`
- `layout_composer` -> `agents/layout-composer.md`
- `still_critic` -> `agents/post-critic.md`
- `motion_director` -> `agents/motion-director.md`
- `render_qa` -> `agents/render-qa.md`
- `final_verifier` -> `agents/story-verifier.md`
- `tool_runner` -> a canonical worker contract explicitly supplied by the parent

These are adapters, not an alternative product graph. Each adapter reads `helper/GUIDE.md`, `architecture/plugin-graph.json`, and its mapped canonical worker contract before product work. The canonical worker owns required preloads, gates, HOLD conditions, artifact shapes, and handoff semantics.

Read/review roles use read-only sandboxes. Layout, motion, and bounded execution roles use workspace-write only where their canonical job requires it. The root orchestrator owns final selection and publishing consent.

The repository caps concurrent Codex subagent threads at six.

## Compatibility registry

`compatibility/codex.json` records the host split explicitly:

- Claude skills root: `skills`
- Claude execution: `native-worker-graph`
- OpenAI skills root: `openai-skills`
- OpenAI execution: `capability-negotiated-autopilot`
- OpenAI sandbox artifacts: enabled by contract when the host exposes writes
- OpenAI side jobs: enabled by contract when real delegation is observed
- Workspace Agents: optional

The canonical Claude product core remains tracked for repository development while the OpenAI distribution is checked for self-containment.

## Validation

Run the OpenAI compatibility gate:

```bash
python3 scripts/validate_codex_plugin.py
```

For a complete repository release gate, run the shared validators documented in [`development.md`](development.md).

The validator checks version parity, OpenAI package isolation, capability-negotiated autopilot contracts, real repository-development Codex agent registrations, directory metadata, visual-quality markers, submission metadata, and the continued presence of Claude execution contracts.

## Updating the published plugin

A commit to GitHub does not automatically replace the package already published in the OpenAI Plugins Directory.

For a new release:

1. update the repository and version metadata
2. run the repository validation gates
3. package the `openai-skills/` distribution with the OpenAI manifest and required assets
4. submit or publish the new version through the supported OpenAI Platform update flow
5. verify the published version after directory propagation

## Public Plugins Directory

Version 3.5.0 is prepared as a skills-only OpenAI update. The tracked handoff lives under `submission/` and includes listing metadata plus exactly five positive and three negative reviewer cases.

The primary `create-post` reviewer case targets `linkedin-infographic-autopilot` and exercises capability negotiation, evidence-first delegation, the complete visual gate, and truthful fallback behavior.

See [`../submission/README.md`](../submission/README.md) for the tracked handoff.
