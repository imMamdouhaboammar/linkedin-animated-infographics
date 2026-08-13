# Development and Validation

The repository uses contract-first development. Public behavior is represented in machine-readable helper, graph, gate, module, demo, and host-packaging files and protected by regression tests.

The Python tools require Python 3.11 or newer. CI uses Python 3.12 and installs Pillow, Playwright, and Chromium before running the render and reference fixtures. The real user-supplied GIF corpus is local-only; CI validates the same ingestion contract with tracked synthetic fixtures.

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
python3 scripts/demo_gallery.py check
python3 scripts/validate_marketplace.py
python3 scripts/validate_codex_plugin.py
python3 -m json.tool hooks/hooks.json >/dev/null
python3 -m json.tool schemas/demo.schema.json >/dev/null
bash -n scripts/lint_artboard.sh
bash -n scripts/setup.sh
git diff --check HEAD^ HEAD
```

For Claude packaging:

```bash
claude plugin validate .
```

CI also performs the same-repository Claude Marketplace add/list/install smoke. OpenAI packaging is validated structurally and for host-isolation contracts by `scripts/validate_codex_plugin.py`; any Codex CLI marketplace smoke must use documented non-interactive behavior rather than a fabricated install command.

## Visual intelligence contracts

Run `python3 scripts/reference_intelligence.py ingest --library /path/to/gifs`, `python3 scripts/reference_intelligence.py check`, and `python3 tools/story_retrieve.py --query query.json`. Ingest writes ignored `.plugin-state/reference-studies/{manifest.json,assets/,frames/}`; duplicate SHA inputs become aliases and cache reuse is SHA-based. Retrieval stages are `concept|story|palette-type|layout|motion|review` and output is UTF-8 byte-budgeted. Study status is READY/HOLD/SKIP; quality axes are Purpose, Hierarchy, Execution, Specificity, Restraint, Variety, with applicable scores below 3 blocking.

## Validator responsibilities

### `scripts/info_stories.py check`

Validates the merged Info-stories registry, semantic Story House tokens, compatibility, and deterministic composition behavior.

### `scripts/ecosystem_router.py check`

Validates helper routes, capabilities, artifacts, local quality gates, research-gate linkage, skill/agent references, and graph capability coverage for the repository runtime.

### `scripts/research_gates.py check`

Validates research provenance, source SHAs/licenses, runtime gate contracts, owners, implementation references, and helper linkage.

### `scripts/plugin_graph.py check`

Validates Claude/repository agent inventory, required skill preloads, shipping order, conditional mascot edge, helper/graph capability ownership, and create-post sequence consistency.

### `scripts/ecosystem_doctor.py check`

Strict repository reality gate. It validates active module inventory, paths, tests, reachability, tool references, capability ownership, artifact participants, local/research gate owners, critical shipping workers, and cross-registry drift.

### `scripts/demo_gallery.py check`

Validates every owned/community demo package, author namespace, metadata contract, public-export scanning, safe local paths, duplicate IDs, exact three-file package shape, and deterministic `demos/catalog.json` drift.

### `scripts/demo_submit.py check`

Validates one staged public contribution before GitHub publication. Preparation requires final verification PASS, rights confirmation, a clean export scan, and the approved GIF/HTML pair.

### `scripts/validate_marketplace.py`

Validates the Claude Marketplace/plugin manifests, same-repository source, strict mode, version agreement, and required Claude component structure.

### `scripts/validate_codex_plugin.py`

Validates `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, the isolated `openai-skills/` distribution, directory compliance, square icon/logo references, absence of unsupported screenshots, OpenAI/Claude identity and version parity, `compatibility/codex.json`, current repository Codex subagent configuration, public policy files, and the tracked OpenAI submission package.

It also rejects OpenAI runtime references to Claude-only paths and requires the blocking visual quality markers for vertical occupancy, dead space, containment depth, still-before-motion behavior, visual failure taxonomy, and bounded repair.

## Community demo changes

Every accepted demo directory contains exactly `demo.gif`, `index.html`, and `demo.json`. The root catalog is generated, not hand-edited.

Before opening a community PR:

```bash
python3 scripts/demo_submit.py check demos/community/<github-user>/<slug>
python3 scripts/demo_gallery.py build
python3 scripts/demo_gallery.py check
```

Review the diff after catalog generation. A community contribution should change only its three-file demo package and `demos/catalog.json`.

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

## Adding a Claude/repository skill, agent, or public tool

A new canonical repository module is incomplete until it is declared in `helper/modules.json` with a real path, role, tests, and reachability links. Update routes, graph, preloads, artifacts, and gates as appropriate. `scripts/ecosystem_doctor.py check` must remain clean.

## Adding an OpenAI public skill

OpenAI public skills live under `openai-skills/` and must be self-contained for the behavior they claim to provide. Do not point them at Claude-only agents, helper routing, the repository worker graph, or Claude environment variables.

Update `scripts/validate_codex_plugin.py` and `tests/test_codex_plugin.py` when the OpenAI package contract changes.

## Release work

The current release is `3.4.0`.

A public release requires the same plugin version across the Claude plugin manifest, Claude marketplace plugin entry, OpenAI plugin manifest, Codex compatibility registry, and OpenAI submission metadata.

Claude and OpenAI do not need identical execution packaging. Claude keeps `skills/` + `agents/`; OpenAI uses `openai-skills/`. The parity target is quality discipline, not identical visual output.

Before merge or publication, require unit/validator success, official Claude validation when available, the available marketplace smoke, no blocking external check, and no unresolved review thread. Updating the GitHub repository does not itself republish the OpenAI directory package.
