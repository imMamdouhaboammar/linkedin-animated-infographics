# Development and Validation

The repository uses contract-first development. Public behavior is represented in machine-readable helper/graph/gate/module files and protected by regression tests.

## Core development loop

1. Add or update a failing test for the intended behavior
2. Implement the smallest coherent change
3. Run focused tests
4. Run the full deterministic gate
5. Update public docs and version metadata when behavior changes
6. Open or update the PR and inspect external reviews/checks
7. Merge only from the exact verified green head

## Full deterministic gate

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tools skills/svg-mascot-animator/scripts
python3 scripts/info_stories.py check
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/validate_marketplace.py
python3 -m json.tool hooks/hooks.json >/dev/null
bash -n scripts/lint_artboard.sh
bash -n scripts/setup.sh
git diff --check HEAD^ HEAD
```

For Claude packaging:

```bash
claude plugin validate .
```

CI also performs a same-repository marketplace add/list/install smoke test.

## Validator responsibilities

### `scripts/info_stories.py check`

Validates the merged Info-stories registry, semantic Story House tokens, compatibility, and deterministic composition behavior.

### `scripts/ecosystem_router.py check`

Validates helper routes, capabilities, artifacts, local quality gates, research-gate linkage, skill/agent references, and graph capability coverage.

### `scripts/research_gates.py check`

Validates research provenance, source SHAs/licenses, runtime gate contracts, owners, implementation references, and helper linkage.

### `scripts/plugin_graph.py check`

Validates agent inventory, required skill preloads, shipping order, conditional mascot edge, helper/graph capability ownership, and create-post sequence consistency.

### `scripts/ecosystem_doctor.py check`

Strict repository reality gate. It validates active module inventory, paths, tests, reachability, tool references, capability ownership, artifact participants, local/research gate owners, critical shipping workers, and cross-registry drift.

### `scripts/validate_marketplace.py`

Validates the Claude Marketplace/plugin manifests, same-repository source, strict mode, version agreement, and required component structure.

## Browser rendering

Browser-dependent checks require Playwright/Chromium plus host libraries and FFmpeg. Run setup where those dependencies can be installed:

```bash
bash scripts/setup.sh
```

If the current environment lacks a required OS browser library, report the browser-render gate as environment-blocked. Do not claim visual rendering passed because non-browser unit tests passed.

## Research changes

When adopting a new external capability:

1. record repository URL, inspected commit, and license
2. write local Adopt / Adapt / Reject notes
3. add or update a stable runtime gate in `research/capability-notes/gates.json`
4. connect the gate to a capability and real shipping owner
5. point to independently-worded local implementation references
6. add regression tests
7. run research gates and the strict doctor

Ignored upstream clones under `research/upstreams/` never ship.

## Adding a skill, agent, or public tool

A new public module is incomplete until it is declared in `helper/modules.json` with a real path, role, tests, and reachability links. Update routes/graph/preloads/artifacts/gates as appropriate. `scripts/ecosystem_doctor.py check` must remain clean.

## Release work

A plugin release requires matching version values in `.claude-plugin/plugin.json` and the plugin entry in `.claude-plugin/marketplace.json`. The current v3 release is `3.0.0`.

Before merge, require unit/validator success, official Claude validation, marketplace install smoke, no blocking external check, and no unresolved review thread.