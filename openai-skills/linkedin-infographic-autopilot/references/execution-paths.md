# Execution paths

Autopilot chooses one path after capability negotiation. Preference order is:

`full-autopilot > tool-rich-sequential > safe-skill-only`

The strongest path is used only when its required capabilities are observed.

All paths apply the same evidence, identity, narrative-taste, and visual-quality contracts. Capability differences change execution, not standards.

Before creative/layout work, read `narrative-taste.md`. Before using any named logo or mascot, read `asset-source-policy.md`; exact user/original-owner provenance wins, pinned Vibe SVGs logos may be used as intact third-party marks when available, and Vibe SVGs `communityArtwork` mascots must never be promoted to official identities.

## full-autopilot

Use when real `subagents` are observed and the host exposes enough execution capabilities for the requested deliverable.

Behavior:

- fan out independent side jobs in parallel where dependency-free
- use sandbox artifacts when `sandbox_write` is observed
- use code execution for deterministic build/render/check jobs when observed
- use image inspection for still and rendered-frame QA when observed
- inspect a bounded set of repository demos only when repository/demo access is actually observed
- wait for required child results before advancing
- keep the parent responsible for synthesis, approvals, identity integrity, narrative selection, and final verification

Do not let multiple writers modify the same artifact concurrently. Parallelism is for independent evidence, concepts, analysis, and bounded review jobs unless the host provides isolated workspaces.

## tool-rich-sequential

Use when useful tools or sandbox execution are observed but real child-agent delegation is unavailable, unknown, or unsuitable.

Behavior:

- execute the same role contracts sequentially
- persist artifacts between passes when `sandbox_write` is observed
- use tools for named jobs such as research, demo-taste selection, identity resolution, rendering, validation, and inspection
- maintain a distinct final-verifier pass even though it runs in the parent context

Do not describe sequential role passes as real agents.

## safe-skill-only

Use when the host lacks the execution capabilities required to truthfully build the requested artifact.

Behavior:

- perform evidence, identity planning, narrative, concept, copy, layout, and critique reasoning only as far as the supplied evidence permits
- use the packaged abstract narrative guidance instead of pretending repository `demos/` media was inspected
- do not claim files, HTML, GIFs, screenshots, renders, agent runs, app writes, asset downloads, or commands were executed
- return `HOLD` when the requested final deliverable or required official identity source needs unavailable execution/evidence
- provide a bounded handoff artifact the user or another capable host can execute

## Narrative requirement on every path

Before macro layout, produce a compact story contract from `narrative-taste.md` containing the primary takeaway, story shape, hook, ordered beats, Reader question per beat, evidence dependency, Beat-to-visual mapping, turn/payoff, persistent context, reference/demo jobs, transferable rules, anti-rules, and necessary motion jobs.

A list converted to cards does not satisfy this requirement.

## Degradation rules

If a selected path loses a capability during execution, degrade one level and record why.

A failed subagent launch degrades to `tool-rich-sequential` when useful tools remain.

A failed sandbox or execution environment degrades to `safe-skill-only` when the requested deliverable can no longer be produced truthfully.

A lost repository/demo capability means use packaged abstract narrative guidance and do not claim demo inspection.

A lost asset-resolution capability means keep exact supplied identity assets or HOLD when an official identity cannot be verified.

Do not claim that a stronger path completed after degradation.
