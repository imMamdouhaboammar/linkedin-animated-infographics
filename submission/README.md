# OpenAI Plugin Submission Handoff

This directory prepares LinkedIn Animated Infographics for the universal OpenAI Plugins Directory used by ChatGPT and Codex.

The repository does not submit or publish the plugin automatically. Final submission is a manual OpenAI Platform action performed by a verified publisher with the required organization permissions.

## Prepared package

- OpenAI manifest: `../.codex-plugin/plugin.json`
- canonical skills bundle: `../skills/`
- listing metadata: `openai-plugin.json`
- reviewer cases: `test-cases.json`
- privacy policy: `../PRIVACY.md`
- terms: `../TERMS.md`
- support: `../SUPPORT.md`

Version 3.2.0 is a skills-only plugin. There is no maintainer-owned MCP server to register for this release.

## Reviewer tests

OpenAI currently requires at least five positive and three negative test cases. This repository tracks exactly five positive and three negative cases in `test-cases.json` so changes are reviewable and deterministic.

Before submission, run the repository validation gate and exercise the cases on the final packaged skill tree. Record any environment-specific fixture details needed by the reviewer without adding credentials or private customer data to the repository.

## Manual OpenAI Platform steps

1. Use an OpenAI organization where the publisher has Apps Management write access
2. Complete or confirm the required individual or business developer verification
3. Open the OpenAI Platform plugin submission flow
4. Submit the skills-only plugin package and listing information from `openai-plugin.json`
5. Add the five positive and three negative reviewer cases from `test-cases.json`
6. Select the intended country or region availability in the Platform form
7. Submit for OpenAI review
8. After approval, use the publisher controls to publish when ready

Do not describe the plugin as publicly available until the OpenAI review and publication steps have actually completed.

## Pre-submission validation

Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/demo_gallery.py check
python3 scripts/validate_marketplace.py
python3 scripts/validate_codex_plugin.py
```

The validator checks tracked submission structure and cross-host parity. It cannot verify external publisher identity, organization permissions, country selection, OpenAI review status, or final publication state.
