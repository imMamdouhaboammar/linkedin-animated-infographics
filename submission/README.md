# OpenAI Plugin Submission Handoff

This directory prepares LinkedIn Animated Infographics for the OpenAI Plugins Directory used by ChatGPT and Codex.

The repository does not submit or publish a new plugin version automatically. Final submission or update publication is a manual OpenAI Platform action performed by a verified publisher with the required organization permissions.

## Prepared package

- OpenAI manifest: `../.codex-plugin/plugin.json`
- OpenAI skills bundle: `../openai-skills/`
- listing metadata: `openai-plugin.json`
- reviewer cases: `test-cases.json`
- privacy policy: `../PRIVACY.md`
- terms: `../TERMS.md`
- support: `../SUPPORT.md`

Version 3.2.1 is a skills-only OpenAI package.

The public skill is self-contained and does not depend on the Claude worker runtime. Claude continues to use the existing `skills/`, `agents/`, and native orchestration path.

## Quality target

The OpenAI distribution targets the same quality discipline as the Claude experience while allowing different visual output.

The OpenAI workflow enforces evidence checks, multiple creative directions, explicit macro-layout planning, a blocking still critique before motion, visual failure taxonomy checks, motion critique, and final verification.

## Reviewer tests

The repository tracks exactly five positive and three negative reviewer cases in `test-cases.json` so changes are reviewable and deterministic.

Before submission, run the repository validation gate and exercise the cases on the final packaged OpenAI skill tree. Record environment-specific fixture details when required without adding credentials or private customer data to the repository.

## Manual OpenAI Platform update steps

1. Use an OpenAI organization where the publisher has Apps Management write access
2. Complete or confirm the required individual or business developer verification
3. Open the OpenAI Platform plugin submission or update flow
4. Submit the skills-only package using `.codex-plugin/plugin.json`, `openai-skills/`, and required assets
5. Add the five positive and three negative reviewer cases from `test-cases.json`
6. Select the intended country or region availability in the Platform form when requested
7. Submit for OpenAI review when review is required
8. After approval, use the publisher controls to publish the new version when ready
9. Verify the directory shows the intended release after propagation

A GitHub commit alone does not update the package already published in the directory.

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

The OpenAI validator checks directory metadata, isolated skill packaging, visual-quality contract markers, submission structure, version parity, and Claude regression contracts. It cannot verify external publisher identity, organization permissions, country selection, OpenAI review status, or final publication state.
