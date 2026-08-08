# Autopilot failure policy

Autopilot fails closed on missing evidence, protected identity assets, unavailable execution, unsafe publishing, and unresolved blocking visual defects.

## Blocking outcomes

Return `HOLD` when:

- a required factual claim has no acceptable evidence
- a named official mascot or protected identity is requested without the exact SVG
- the requested final artifact requires execution that the host cannot truthfully perform
- a requested external write lacks the required consent or authorization
- a required verification stage cannot inspect the evidence it is supposed to verify

Return `FAIL:fixable` when the artifact exists but a blocking quality defect is repairable within the same environment.

Return `PASS` only after every required gate for the selected execution path has direct evidence.

## Repair budget

A blocking still or render failure permits at most two targeted repair attempts.

Each attempt must:

1. name the blocking finding
2. change the smallest relevant artifact
3. rerun the affected gate
4. preserve previous failure history

If the same blocking class remains after the second repair, stop. Do not add a third silent repair loop.

## Capability failure

- failed real delegation: degrade to sequential execution when possible
- failed sandbox write: degrade to non-materialized artifacts or `HOLD` if a build is required
- failed image inspection: do not claim visual QA; run structural checks only and mark the limitation
- failed web research: use supplied evidence only and mark freshness-sensitive claims unresolved
- failed connected-app read: do not substitute a different source unless it answers the same authorized question

## No fabricated recovery

Never claim that a tool, agent, render, sandbox write, app read, or external publication succeeded when no successful result was observed.

Never lower a blocking visual, evidence, identity, or consent gate merely to reach delivery.
