# OpenAI Autopilot Runtime Design

## Goal

Upgrade the OpenAI distribution so ChatGPT and Codex use available host capabilities aggressively and safely: real Codex subagents when available, parallel side jobs, sandbox artifacts, connected tools/apps, and deterministic fallback behavior when those capabilities are unavailable.

The target is quality-process parity with the Claude experience, not identical visual output.

## Non-negotiable constraints

- Preserve Claude behavior as a regression baseline
- Keep the public OpenAI package self-contained
- Never claim a tool call, delegation, render, app action, or publish action that did not actually happen
- Still QA must pass before motion
- Exact named mascot identity still requires the exact SVG
- Community publishing still requires explicit consent and stops at a pull request
- Evidence integrity remains blocking
- Maximum two targeted repair attempts for a blocking visual failure
- Version for this change is 3.2.2

## Runtime architecture

The OpenAI distribution gains a parent skill named `linkedin-infographic-autopilot`.

At task start it performs capability negotiation and selects one execution path:

1. `full-autopilot`
   - real subagent/side-job delegation is available
   - sandbox or workspace artifact writes are available
   - relevant tools/apps may be invoked
   - independent jobs are parallelized when safe

2. `tool-rich-sequential`
   - useful tools and sandbox are available
   - real child-agent delegation is not available or not reliable
   - the same role contracts run sequentially with persistent artifacts

3. `safe-skill-only`
   - no write sandbox and no real delegation
   - the skill runs bounded reasoning passes only
   - it does not claim builds, renders, tool use, or background work
   - it returns a precise HOLD when the requested artifact cannot be truthfully produced

Capability negotiation is conservative. Unknown capability means unavailable until observed.

## Capability model

The runtime evaluates these capability classes independently:

- `subagents`: child-agent or side-job execution
- `sandbox_write`: ability to create/update working artifacts
- `shell_or_code_execution`: ability to run scripts, renderers, validators, or build commands
- `image_inspection`: ability to inspect stills and rendered frames
- `web_research`: fresh public research
- `connected_apps`: GitHub, Drive, Notion, or other host-provided apps/tools
- `workspace_agents`: published ChatGPT workspace-agent invocation when available
- `publishing_tools`: authenticated GitHub contribution tools used only after consent

The skill must not infer availability from documentation alone. It uses what the current host actually exposes.

## Side-job policy

When real subagents are available, the parent orchestrator may fan out independent jobs. Recommended initial fan-out for a new infographic:

- evidence researcher
- creative direction explorer
- visual archetype/layout explorer
- copy compression critic

After a direction is selected, later jobs are dependency-bound and normally run in sequence:

- artboard build
- still critique
- targeted repair
- motion direction
- motion implementation
- render QA
- independent final verifier

The parent must wait for all jobs required by the selected path before advancing. Side jobs return bounded artifacts rather than open-ended prose.

## Sandbox artifact contract

When sandbox writes are available, use a task-local workspace structure:

```text
work/
  brief/
  evidence/
  concepts/
  selected-direction/
  copy/
  layout/
  build/
  still-review/
  motion/
  render-qa/
  verifier/
  final/
```

Canonical artifacts:

- `evidence/evidence.json`
- `concepts/directions.md`
- `selected-direction/decision.md`
- `copy/copy-slots.md`
- `layout/layout-plan.json`
- `build/index.html`
- `still-review/report.json`
- `motion/motion-plan.json`
- `render-qa/report.json`
- `verifier/report.json`
- `final/delivery.json`

A host may use different physical paths, but the logical artifact names and responsibilities remain the same.

## Real Codex agents

Repository-development Codex receives real project-scoped roles under `.codex/agents/`:

- `creative_director`
- `evidence_researcher`
- `copy_director`
- `layout_composer`
- `still_critic`
- `motion_director`
- `render_qa`
- `final_verifier`
- `tool_runner`

Each role is narrow. Reviewer/verifier agents are read-only. Builders use workspace-write only when their job requires it. The root orchestrator owns final decisions and publishing consent.

Codex multi-agent behavior is opportunistic, not mandatory for the installed public skill. The public skill has a sequential fallback.

## Tool-use policy

The orchestrator uses tools when they materially improve correctness or artifact quality.

Examples:

- web/search tools for fresh claims or references
- image inspection for rendered still/final frame critique
- sandbox/shell for HTML generation, validation, screenshots, GIF rendering, and deterministic checks
- GitHub for contribution publishing only after explicit consent
- connected file/document tools when the user explicitly supplies or references those sources

Tool calls are never decorative. A tool is invoked for a named job and its result is recorded in the relevant artifact or verification report.

## Workspace Agents bridge

Workspace Agents are treated as an optional external execution capability, not a guaranteed plugin feature.

When the host exposes callable workspace agents, the runtime may delegate bounded jobs to compatible published agents. If they are not exposed, it uses Codex subagents or local role passes instead.

The repository documents recommended workspace-agent roles and input/output contracts but does not claim that installing the skills-only plugin registers workspace agents automatically.

## Visual quality gates

The existing OpenAI visual-quality contract remains authoritative and gains explicit enforcement inside the autopilot path.

Blocking failures include:

- top-heavy composition
- unexplained bottom dead space greater than the defined threshold
- detached footer
- weak visual anchor
- weak macro rhythm
- excessive nested-card density
- generic UI grammar replacing art direction
- feed-scale legibility failure
- motion on a weak still
- decorative motion dominating explanatory motion

No motion work starts while a blocking still failure remains.

## Error and fallback behavior

- Missing evidence: `HOLD`
- Missing exact SVG for a named mascot: `HOLD`
- Missing write sandbox for a requested build: return the strongest truthful planning/critique artifact and state that the build was not executed
- Missing image inspection: do not claim visual QA; run structural checks only and mark visual inspection unavailable
- Missing subagents: use sequential role passes
- Tool failure: retry only when safe and bounded; otherwise degrade to a documented path
- Third unresolved blocking visual failure: `FAIL:fixable` or `HOLD`, never silent shipping

## Validation

Tests must prove:

- the public package contains the autopilot skill and its required references
- all three execution paths are documented and mutually exclusive
- capability negotiation defaults unknown capabilities to unavailable
- side-job contracts require real delegation claims only when observed
- sandbox artifact names are stable
- workspace-agent support is optional and never presented as automatic registration
- all new Codex agent roles exist and have narrow permissions
- Claude manifests, canonical skills root, agents root, and native worker graph remain unchanged apart from version alignment
- OpenAI and Claude package versions remain in parity at 3.2.2

## Release behavior

GitHub changes do not update the already published OpenAI Directory package automatically. After validation and merge, 3.2.2 must be manually submitted/published through the OpenAI plugin update flow.
