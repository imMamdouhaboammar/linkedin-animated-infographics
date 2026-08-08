# Artifact workspace

When writable sandbox or workspace access is observed, persist intermediate work as logical artifacts. The host may materialize them at different physical paths, but every logical artifact keeps the same responsibility.

Recommended task-local structure:

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

## Canonical logical artifacts

- `evidence/evidence.json`: claim inventory, sources, unsupported slots, freshness notes
- `concepts/directions.md`: candidate directions with visual hooks and story structures
- `selected-direction/decision.md`: chosen direction and explicit selection rationale
- `copy/copy-slots.md`: final slot-level copy, evidence references, and removed duplication
- `layout/layout-plan.json`: artboard zones, bounds, occupancy, footer reservation, containment depth
- `build/index.html`: editable deterministic artboard when HTML production is supported
- `still-review/report.json`: still gate findings, top defects, repair count, verdict
- `motion/motion-plan.json`: motion jobs, timing, meaning, reduced-motion behavior when relevant
- `render-qa/report.json`: actual-render QA evidence and verdict
- `verifier/report.json`: independent evidence/process/final-output verification
- `final/delivery.json`: inventory of artifacts actually delivered and capabilities actually used

## Artifact rules

- Each logical artifact has one owner at a time
- Later stages consume the artifact that earlier stages actually emitted
- Never fabricate a logical artifact by naming a path that was not created
- If the host cannot write files, keep the same logical artifact schema in the response but label it `not-materialized`
- Preserve evidence references through copy, build, and verification
- QA must inspect the same build/render generation that is delivered
- Repair attempts update the existing report with attempt number rather than erasing failure history

## Concurrency

Parallel side jobs may write separate artifacts. They must not concurrently modify `build/index.html`, `layout/layout-plan.json`, or any other shared production artifact unless the host provides isolated branches/workspaces and a deliberate merge step.
