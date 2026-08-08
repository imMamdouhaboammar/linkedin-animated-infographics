# Side jobs

Use side jobs only when real delegation is observed. A side job is a bounded unit with a defined input, bounded artifact output, and no authority to publish or make irreversible decisions.

The parent must wait for every required side job before using its result. If a worker fails, the parent either retries once when safe or executes the same contract sequentially.

## Parallel-safe discovery jobs

### evidence-research

Input: supplied brief, claims, source material, and missing evidence slots

Output bounded artifact: evidence inventory with supported, unsupported, and freshness-sensitive claims

### creative-direction-exploration

Input: evidence inventory, audience, primary message, visual constraints

Output bounded artifact: at least three structurally different creative directions with hook, visual anchor, story shape, and motion idea

### visual-archetype-exploration

Input: evidence inventory and candidate directions

Output bounded artifact: recommended visual archetypes, layout risks, and rejected generic-UI patterns

### copy-compression-critique

Input: candidate copy slots and primary takeaway

Output bounded artifact: duplicate ideas, filler, unsupported claims, and compressed alternatives

## Dependency-bound production jobs

These normally run after a direction is selected:

### still-critique

Input: actual still or build artifact when inspection is available, plus layout plan

Output bounded artifact: blocking visual failures, top three defects, and PASS or FAIL:fixable

### render-qa

Input: actual rendered frames or animation evidence when available

Output bounded artifact: clipping, footer clearance, feed-scale legibility, pacing, loop seam, and motion-purpose verdict

### final-verification

Input: evidence inventory, final artifacts, still report, and render report

Output bounded artifact: independent PASS, FAIL:fixable, or HOLD with direct reasons

## Coordination rules

- Parallelize only jobs without dependency edges
- Never allow two side jobs to write the same artifact concurrently unless the host gives them isolated workspaces
- The parent owns creative selection, user approvals, and publishing consent
- A worker cannot promote its own result directly to final delivery
- Real delegation must be observed. When it is not observed, execute the contract sequentially and do not claim an agent ran
- Side-job prose is not enough when a bounded artifact is required; return the named artifact fields
