# Side jobs

Use side jobs only when real delegation is observed. A side job is a bounded unit with a defined input, bounded artifact output, and no authority to publish or make irreversible decisions.

The parent must wait for every required side job before using its result. If a worker fails, the parent either retries once when safe or executes the same contract sequentially.

## Phase 1: evidence boundary

### evidence-research

This job always completes before creative discovery begins.

Input: supplied brief, claims, source material, and missing evidence slots

Output bounded artifact: finalized evidence inventory with supported, unsupported, contradicted, and freshness-sensitive claims plus protected fact slots

The parent must wait for this artifact. Creative directions, visual archetypes, and copy critique consume the finalized evidence boundary rather than a preliminary inventory.

## Phase 2: parallel-safe creative discovery

After evidence is finalized, these jobs are independent enough to fan out when real delegation is observed.

### creative-direction-exploration

Input: finalized evidence inventory, audience, primary message, and visual constraints

Output bounded artifact: at least three structurally different creative directions with hook, visual anchor, story shape, useful reveal, and motion idea

### visual-archetype-exploration

Input: finalized evidence inventory, audience, message relationship, and creative constraints

Output bounded artifact: recommended visual archetypes, structural options, layout risks, and rejected generic-UI patterns

### copy-compression-critique

Input: finalized evidence inventory, primary takeaway, protected fact slots, and available candidate copy/source language

Output bounded artifact: duplication risks, filler, unsupported wording, protected facts, and compression guidance

These creative-discovery jobs may be concurrent, but they cannot weaken or reinterpret the finalized evidence boundary.

## Phase 3: dependency-bound production jobs

These run only after the parent selects a direction and the required upstream artifact exists.

### still-critique

Input: actual still or build artifact when inspection is available, layout plan, and complete visual-quality contract

Output bounded artifact: explicit PASS/FAIL taxonomy, blocking visual failures, top three defects, repair count, and PASS or FAIL:fixable/HOLD

### render-qa

Input: actual rendered frames or animation evidence when available plus passing still report

Output bounded artifact: clipping, footer clearance, feed-scale legibility, pacing, loop seam, motion-purpose verdict, and PASS/FAIL:fixable/HOLD

### final-verification

Input: finalized evidence inventory, final artifacts, complete still report, render report when applicable, and execution summary

Output bounded artifact: independent PASS, FAIL:fixable, or HOLD with direct evidence

## Coordination rules

- Evidence is a dependency, not a peer of creative discovery
- Finish `evidence-research` before launching creative-direction, visual-archetype, or copy-compression discovery
- Parallelize only jobs without dependency edges
- Never allow two side jobs to write the same artifact concurrently unless the host gives them isolated workspaces
- The parent owns creative selection, user approvals, and publishing consent
- A worker cannot promote its own result directly to final delivery
- Real delegation must be observed. When it is not observed, execute the contract sequentially and do not claim an agent ran
- Side-job prose is not enough when a bounded artifact is required; return the named artifact fields
