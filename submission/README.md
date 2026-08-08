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

Version 3.3.0 is a skills-only OpenAI package.

The public package is self-contained and does not depend on the Claude worker runtime or repository-development `.codex/` configuration. Claude continues to use the existing `skills/`, `agents/`, and native orchestration path.

## Autopilot runtime

The primary full-production OpenAI route is `linkedin-infographic-autopilot`.

It observes current host capabilities before execution and selects exactly one path:

- `full-autopilot` when real delegation plus useful execution capabilities are observed
- `tool-rich-sequential` when useful tools or sandbox execution are observed without real delegation
- `safe-skill-only` when artifact execution cannot be completed truthfully

Unknown capabilities fail closed as unavailable.

When supported, the package can use real side jobs, writable sandbox artifacts, code execution, image inspection, public research, connected apps, and optional Workspace Agents. It never claims any of those actions unless they were actually exposed and executed in the current host.

When code execution is available, `openai-skills/linkedin-infographic-autopilot/scripts/autopilot_runtime.py` provides deterministic path selection, side-job dispatch planning, and sandbox workspace scaffolding.

Workspace Agents are an optional external capability and are not automatically registered by installing the skills-only package.

## Quality target

The OpenAI distribution targets the same quality discipline as the Claude experience while allowing different visual output.

The OpenAI workflow enforces evidence checks, multiple creative directions, explicit macro-layout planning, a blocking still critique before motion, visual failure taxonomy checks, motion critique, and independent final verification.

The still gate blocks top-heavy composition, unexplained bottom dead space, detached footers, weak visual anchors, generic UI-card stacking, weak macro rhythm, feed-scale legibility failures, and motion added to a weak still.

## Reviewer tests

The repository tracks exactly five positive and three negative reviewer cases in `test-cases.json` so changes are reviewable and deterministic.

The `create-post` case exercises `linkedin-infographic-autopilot` and requires a truthful execution summary naming the selected path, observed capabilities actually used, side jobs actually executed, materialized artifacts, and final QA verdict.

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
python3 -m compileall -q scripts tools skills/svg-mascot-animator/scripts openai-skills/linkedin-infographic-autopilot/scripts
python3 scripts/info_stories.py check
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/demo_gallery.py check
python3 scripts/validate_marketplace.py
python3 scripts/validate_codex_plugin.py
```

The OpenAI validator checks directory metadata, isolated skill packaging, autopilot capability contracts, real repository-development Codex agent registration, visual-quality markers, submission structure, version parity, and Claude regression contracts. It cannot verify external publisher identity, organization permissions, country selection, OpenAI review status, or final publication state.
