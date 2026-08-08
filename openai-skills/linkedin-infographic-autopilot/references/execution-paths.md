# Execution paths

Autopilot chooses one path after capability negotiation. Preference order is:

`full-autopilot > tool-rich-sequential > safe-skill-only`

The strongest path is used only when its required capabilities are observed.

## full-autopilot

Use when real `subagents` are observed and the host exposes enough execution capabilities for the requested deliverable.

Behavior:

- fan out independent side jobs in parallel where dependency-free
- use sandbox artifacts when `sandbox_write` is observed
- use code execution for deterministic build/render/check jobs when observed
- use image inspection for still and rendered-frame QA when observed
- wait for required child results before advancing
- keep the parent responsible for synthesis, approvals, and final verification

Do not let multiple writers modify the same artifact concurrently. Parallelism is for independent evidence, concepts, analysis, and bounded review jobs unless the host provides isolated workspaces.

## tool-rich-sequential

Use when useful tools or sandbox execution are observed but real child-agent delegation is unavailable, unknown, or unsuitable.

Behavior:

- execute the same role contracts sequentially
- persist artifacts between passes when `sandbox_write` is observed
- use tools for named jobs such as research, rendering, validation, and inspection
- maintain a distinct final-verifier pass even though it runs in the parent context

Do not describe sequential role passes as real agents.

## safe-skill-only

Use when the host lacks the execution capabilities required to truthfully build the requested artifact.

Behavior:

- perform evidence, concept, copy, layout, and critique reasoning only as far as the supplied evidence permits
- do not claim files, HTML, GIFs, screenshots, renders, agent runs, app writes, or commands were executed
- return `HOLD` when the requested final deliverable requires unavailable execution
- provide a bounded handoff artifact the user or another capable host can execute

## Degradation rules

If a selected path loses a capability during execution, degrade one level and record why.

A failed subagent launch degrades to `tool-rich-sequential` when useful tools remain.

A failed sandbox or execution environment degrades to `safe-skill-only` when the requested deliverable can no longer be produced truthfully.

Do not claim that a stronger path completed after degradation.
