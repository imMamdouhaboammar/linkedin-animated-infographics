---
name: linkedin-infographic-autopilot
description: Run LinkedIn infographic work in autopilot mode by negotiating available host capabilities, using real side jobs and sandbox artifacts when available, and falling back honestly when they are not. Use for end-to-end creation, redesign, animation, or rigorous production workflows in ChatGPT or Codex.
---

# LinkedIn Infographic Autopilot

## Purpose

Operate as the parent production workflow for LinkedIn infographic work. Use the strongest capabilities actually exposed by the current host without inventing agents, tools, renders, background work, or publishing actions.

Quality parity means the same discipline as a strong multi-role creative workflow while allowing a different visual direction for every host and every brief.

Read these local references before execution:

- `references/capability-negotiation.md`
- `references/execution-paths.md`
- `references/side-jobs.md`
- `references/artifact-workspace.md`
- `references/tool-usage-policy.md`
- `references/autopilot-failure-policy.md`
- `references/workspace-agents-bridge.md`

## Autopilot rule

Start every substantial task by observing the capabilities the host actually exposes. Unknown capabilities are unavailable until observed.

Select exactly one runtime path:

- `full-autopilot`
- `tool-rich-sequential`
- `safe-skill-only`

Prefer the strongest safe path. Never pretend that a stronger path ran.

## Required production sequence

1. Build the evidence inventory
2. Observe runtime capabilities and select the execution path
3. Fan out independent side jobs when real delegation is observed
4. Generate at least three structurally different creative directions
5. Select the direction and define the primary takeaway
6. Compress copy into visual slots
7. Define macro layout before component styling
8. Build the still when sandbox writes are observed
9. Run still critique
10. Repair blocking still defects, maximum two targeted repair attempts
11. Proceed to motion only after the still passes
12. Implement motion only when the requested output and host capabilities support it
13. Run render QA using actual rendered evidence when image inspection is observed
14. Run an independent final verification pass
15. Deliver artifacts plus a truthful capability/execution summary

## Side jobs

When real child-agent or equivalent side-job execution is observed, parallelize independent work instead of making the parent do everything serially.

The first fan-out may include:

- evidence research
- creative direction exploration
- visual archetype exploration
- copy compression critique

The parent waits for required side jobs, validates their bounded artifacts, selects what survives, and owns the final decision.

When real delegation is not observed, run those contracts sequentially. Do not describe sequential role passes as agents.

## Sandbox and artifact behavior

When sandbox or workspace writes are observed, persist intermediate work using the logical artifact contract in `references/artifact-workspace.md`.

Use artifacts to reduce transient-context loss and to make QA inspect the same inputs that the build used.

When write access is unavailable, do not claim that HTML, images, GIFs, screenshots, or files were created. Produce the strongest truthful planning or critique output and return `HOLD` when the requested final artifact cannot be executed.

## Tool behavior

Use tools, apps, search, code execution, image inspection, and publishing connectors only when they materially improve a named job.

Record important tool results in the artifact or verification stage that consumed them.

A tool being described in documentation is not proof that it exists in the current session. Capability must be observed.

## Visual gates

The still is a blocking gate before motion.

Reject severe versions of:

- top-heavy composition
- unexplained bottom dead space
- detached footer
- weak visual anchor
- weak macro rhythm
- excessive nested-card density
- generic UI grammar replacing art direction
- feed-scale legibility failure
- motion on a weak still
- decorative motion dominating explanatory motion

If a blocking still defect remains after two targeted repairs, return `FAIL:fixable` or `HOLD` instead of shipping weak output.

## Focused capability routing

When the host exposes the related public skill and the request is focused, prefer the narrower contract:

- `linkedin-infographic-studio` for full production without explicit autopilot orchestration
- `linkedin-infographic-review` for finished-output QA
- `exact-svg-mascot` for protected named mascot identity
- `share-community-demo` for explicit post-verification community publishing consent

If focused skill routing is not exposed, apply the same safety rule locally rather than claiming the skill was invoked.

## Final report

Return:

- selected execution path
- observed capabilities used
- side jobs actually executed
- artifacts actually created
- still verdict
- motion/render verdict when applicable
- final verdict: `PASS`, `FAIL:fixable`, or `HOLD`

Never claim a tool, agent, sandbox artifact, render, connected app, or publication action that did not actually occur.
