# Verification loop

The worker that built or edited an Info-story does not grade its own work. Verification reads artifacts and acceptance criteria directly.

## Verdicts

- `PASS`: every required criterion has direct evidence
- `FAIL:fixable`: one or more criteria failed and the failure has a targeted local fix
- `FAIL:escalate`: acceptance criteria conflict, source facts are missing, the artifact is structurally wrong, or two targeted fix attempts already failed

## Evidence row

Every acceptance criterion records:

- `id`: stable ID such as `IS-01`
- `status`: `PASS`, `FAIL`, or `NA`
- `artifact`: file or source inspected
- `observation`: what the verifier actually observed
- `evidence`: screenshot, command output, metric, file range, or other direct evidence

Do not cite the worker's summary as evidence.

## Default acceptance set

- `IS-01` Story fit: required narrative beats appear in reading order
- `IS-02` Truth: factual claims and named products match sources
- `IS-03` Contrast: declared text pairs and rendered critical text are readable
- `IS-04` Mobile: the takeaway survives the 350px preview
- `IS-05` First frame: frame 0 is a complete still
- `IS-06` Motion: direction and active-state order match the story
- `IS-07` Loop: seam and timing meet existing render gates
- `IS-08` File: dimensions, duration, and size meet delivery constraints
- `IS-09` Anti-slop: no unresolved load-bearing copy pattern or palette-only style claim

Static output marks motion-only criteria `NA` with an observation explaining why.

## Bounded repair

On `FAIL:fixable`, send only failed criterion IDs, evidence, and target fix back to the relevant worker. Re-run verification after the fix. Maximum two targeted fix attempts. A third failure becomes `FAIL:escalate` and returns the unresolved criteria to the user or lead agent.

Run `validate_verification_report()` before accepting a verifier report.
