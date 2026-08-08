# OpenAI Visual Parity CI Verification

This file exists to create a pull-request head over the completed 3.2.1 repository state so the repository's PR-triggered validation can run against the exact OpenAI visual parity changes.

The verification target includes:

- isolated `openai-skills/` packaging
- Claude behavior regression boundary
- directory metadata compliance
- visual-quality failure taxonomy
- still-before-motion gate
- bounded repair contract
- version and submission metadata consistency

No runtime behavior is changed by this verification marker.
