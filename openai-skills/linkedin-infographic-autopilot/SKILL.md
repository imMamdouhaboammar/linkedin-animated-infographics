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
- `references/visual-quality-contract.md`
- `references/visual-intelligence-capsule.json`

Read the generated visual-intelligence capsule before creative selection. It is the only packaged reference context: apply its hard filters, fixed weights, and slug tie-break, then pass only selected mechanism guidance into production. No visual reference is `SKIP`. Explicit reference intent with evidence that cannot be inspected is `HOLD: reference evidence unavailable` before evidence research. Persistent reference ingestion and source reference media are unavailable in this distribution; never claim they were loaded. The capsule is abstract local guidance only.

The complete blocking visual gate in `references/visual-quality-contract.md` is authoritative for Autopilot. The summary below never replaces or weakens it.

## Autopilot rule

Start every substantial task by observing the capabilities the host actually exposes. Unknown capabilities are unavailable until observed.

Select exactly one runtime path:

- `full-autopilot`
- `tool-rich-sequential`
- `safe-skill-only`

Prefer the strongest safe path. Never pretend that a stronger path ran.

## Executable runtime helper

When `shell_or_code_execution` is observed, use `scripts/autopilot_runtime.py` to make orchestration decisions deterministic instead of relying only on free-form model judgment.

Pass only capabilities actually observed in the current host. Example shape:

```json
{
  "subagents": true,
  "sandbox_write": true,
  "shell_or_code_execution": true,
  "image_inspection": true,
  "web_research": true
}
```

The helper can:

- normalize unknown values to unavailable
- select the execution path
- generate a bounded evidence-first side-job dispatch plan
- initialize the logical artifact workspace without fabricating artifact files

Typical commands when execution is available:

```text
python scripts/autopilot_runtime.py select-path --capabilities-json '<observed-json>'
python scripts/autopilot_runtime.py dispatch-plan --capabilities-json '<observed-json>'
python scripts/autopilot_runtime.py init-workspace <task-workspace>/work
```

If code execution is not observed, apply the same contracts directly from the references. Do not claim the helper ran.

## Reference behavior

When inspectable visual references are supplied, derive reusable guidance rather than copying the reference. For every selected mechanism use:

`Evidence -> Observation -> Transferable Rule -> Anti-Rule`

When multiple references exist, assign explicit non-overlapping jobs such as composition, type hierarchy, color, texture, pacing, or motion. Do not blend them into one vague style and do not copy distinctive subject matter, identity, proprietary artwork, or unique composition signatures.

## Required production sequence

1. Observe runtime capabilities and select the execution path
2. Run evidence research/inventory first and finalize `evidence/evidence.json` or its non-materialized equivalent
3. Only after the evidence artifact is finalized, fan out independent creative discovery side jobs when real delegation is observed
4. Generate at least three structurally different creative directions from the finalized evidence boundary, applying the reference-transfer protocol when references exist
5. Select the direction and define the primary takeaway
6. Compress copy into visual slots using only approved evidence
7. Define macro layout before component styling
8. Run the complete blocking perception preflight from `references/visual-quality-contract.md` and repair only the smallest responsible dimension when a check fails
9. Build the still when sandbox writes are observed
10. Run the complete still critique taxonomy, perception tests, severity pressure, and targeted revision routing from `references/visual-quality-contract.md`
11. Repair blocking still defects, maximum two targeted repair attempts
12. Proceed to motion only after the complete still gate passes
13. Implement motion only when the requested output and host capabilities support it
14. Run render QA using actual rendered evidence when image inspection is observed
15. Run an independent final verification pass
16. Deliver artifacts plus a truthful capability/execution summary

## Side jobs

When real child-agent or equivalent side-job execution is observed, use dependency-aware delegation rather than making the parent do everything serially.

Evidence is not part of the first creative fan-out. `evidence-research` must complete first because every downstream creative job consumes its finalized supported/unsupported/freshness-sensitive inventory.

After evidence is finalized, the creative fan-out may run these independent jobs in parallel:

- creative direction exploration
- visual archetype exploration
- copy compression critique

The parent waits for required side jobs, validates their bounded artifacts, selects what survives, and owns the final decision.

When real delegation is not observed, run the same contracts sequentially in the same dependency order. Do not describe sequential role passes as agents.

## Sandbox and artifact behavior

When sandbox or workspace writes are observed, persist intermediate work using the logical artifact contract in `references/artifact-workspace.md`.

Use artifacts to reduce transient-context loss and to make QA inspect the same inputs that the build used.

When write access is unavailable, do not claim that HTML, images, GIFs, screenshots, or files were created. Produce the strongest truthful planning or critique output and return `HOLD` when the requested final artifact cannot be executed.

## Tool behavior

Use tools, apps, search, code execution, image inspection, and publishing connectors only when they materially improve a named job.

Record important tool results in the artifact or verification stage that consumed them.

A tool being described in documentation is not proof that it exists in the current session. Capability must be observed.

## Visual gates

Apply every rule and every PASS/FAIL taxonomy item in `references/visual-quality-contract.md`.

In particular, for the default LinkedIn format the gate includes:

- 1080x1350 canvas unless the user requests another format
- roughly 82-92% usable vertical occupancy unless intentional negative space has a clear compositional job
- rejection of unexplained footer/final-zone gaps greater than 120px
- maximum bordered containment depth of two levels
- one dominant visual anchor at feed scale
- explicit macro rhythm and footer reservation
- a blocking perception preflight including one-second hierarchy, 100x100 thumbnail, squint/blur, grayscale, negative-space, tangency, brand-off specificity, and effect-subtraction checks
- severity-aware visual-slop pressure that never cancels a hard-gate failure
- rejection of generic UI grammar, nested-card density, weak macro rhythm, weak visual anchor, top-heavy composition, and feed-scale legibility failure

The critic must explicitly return PASS or FAIL for the full taxonomy, including `top-heavy-composition`, `bottom-dead-zone`, `nested-card-density`, `generic-ui-grammar`, `weak-macro-rhythm`, `weak-visual-anchor`, `footer-detachment`, `motion-on-weak-still`, `decorative-motion`, and `feed-scale-legibility`.

Motion cannot begin while any blocking still item or perception-preflight item fails.

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
- perception-preflight verdict
- complete still taxonomy verdict
- severity counts and cumulative visual-slop pressure
- targeted repairs actually performed and their responsible dimensions
- motion/render verdict when applicable
- final verdict: `PASS`, `FAIL:fixable`, or `HOLD`

Never claim a tool, agent, sandbox artifact, render, connected app, or publication action that did not actually occur.
