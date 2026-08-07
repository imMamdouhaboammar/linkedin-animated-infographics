# COG-second-brain capability note

Source: https://github.com/huytieu/COG-second-brain
Inspected commit: `19471473a34a29a042c0d7738ce573cc2dcee119`
License: MIT

## Adopt

- The worker does not grade its own output
- Acceptance criteria use stable IDs and each verdict cites observed evidence
- A verifier reads the artifact directly rather than trusting the worker summary
- Multi-part work gets an integration verification pass
- Failed verification enters a bounded fix and re-check loop
- Significant work ends with a short retrospective that feeds future rules

## Adapt for Info-stories

- Story verification criteria cover content truth, structural fit, contrast, mobile downscale, first frame, motion order, seam, and file budget
- Read-only `story-verifier` reports PASS, FAIL:fixable, or FAIL:escalate
- Maximum two targeted fix attempts before escalation
- Visual criteria require rendered evidence when an artifact exists
- Evidence rows reference local acceptance IDs such as `IS-01`

## Reject

- Importing the complete COG vault/checkpoint hierarchy into this small plugin
- Requiring a full run directory for tiny registry-only changes
- Letting the verifier mutate the artifact

## Local targets

- `agents/story-verifier.md`
- `skills/info-stories/references/verification-loop.md`
- `agents/render-qa.md`
- acceptance smoke tests
