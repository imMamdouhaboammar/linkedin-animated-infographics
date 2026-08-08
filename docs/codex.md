# Codex and ChatGPT

Version 3.2.1 gives Codex and ChatGPT an OpenAI-specific skills distribution while preserving the existing Claude execution path.

The target is quality and process parity, not identical visual output. Claude and OpenAI may choose different creative directions, layouts, palettes, and motion treatments, but both must follow disciplined evidence, concept, layout, still QA, motion, and verification stages.

## Native OpenAI package

The OpenAI plugin entry point is:

```text
.codex-plugin/plugin.json
```

It declares a skills-only plugin and points to:

```text
./openai-skills/
```

The published OpenAI workflow is self-contained under:

```text
openai-skills/linkedin-infographic-studio/
```

It does not depend on Claude worker registration, `.claude-plugin/`, `agents/`, repository helper routing, or Claude-specific environment variables at runtime.

The repository marketplace remains:

```text
.agents/plugins/marketplace.json
```

## Why OpenAI has a separate distribution

Claude can execute the repository's native worker graph and agent roles directly. A skills-only ChatGPT/Codex installation cannot assume those workers are registered.

Version 3.2.1 therefore compiles the same creative discipline into explicit sequential role passes for OpenAI:

1. evidence inventory
2. creative directions
3. story architecture
4. palette contract
5. copy compression
6. macro layout
7. still construction
8. still critique and repair
9. motion direction
10. motion implementation
11. render QA
12. adversarial visual critique
13. final verification

The still gate is blocking. Motion cannot begin while a severe composition defect remains.

## Visual quality gates

The OpenAI skill explicitly checks problems that can pass ordinary technical QA while still producing weak design:

- top-heavy composition
- unexplained bottom dead space
- detached footer
- weak visual anchor
- weak macro rhythm
- excessive nested-card density
- generic dashboard/card grammar
- feed-scale legibility
- motion added to a weak still
- decorative motion with no explanatory job

The layout contract includes measurable guidance for vertical occupancy, a 120px unexplained dead-zone threshold, a maximum of two bordered containment levels, and a two-attempt targeted repair limit.

## Claude regression boundary

Claude keeps the existing canonical runtime:

- `skills/`
- `agents/`
- `helper/`
- `architecture/plugin-graph.json`
- `.claude-plugin/`

The 3.2.1 work does not replace Claude agents with OpenAI role passes. Only release version metadata is synchronized where repository parity requires it.

## Add the repository marketplace

With a Codex CLI release that supports plugins:

```bash
codex plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics --ref main
codex plugin marketplace list
```

Use supported Plugins Directory surfaces for installation and testing.

## Repository-scoped Codex subagents

`.codex/config.toml` and `.codex/agents/*.toml` remain repository-development helpers. They are not a dependency of the installed public plugin.

The project-scoped maintenance roles are:

- `explorer` for read-only execution-path inspection
- `reviewer` for read-only correctness, security, regression, and test review
- `docs_researcher` for read-only primary-documentation verification

They are separate from the skills distributed through the public plugin.

## Compatibility registry

`compatibility/codex.json` records the host split explicitly:

- Claude skills root: `skills`
- OpenAI skills root: `openai-skills`

The canonical Claude product core remains tracked for repository development while the OpenAI distribution is checked for self-containment.

Validate with:

```bash
python3 scripts/validate_codex_plugin.py
```

The validator checks version parity, OpenAI package isolation, directory metadata, visual-quality markers, submission metadata, and the continued presence of Claude execution contracts.

## Updating the published plugin

A commit to GitHub does not automatically replace the package already published in the OpenAI Plugins Directory.

For a new release:

1. update the repository and version metadata
2. run the repository validation gates
3. package the `openai-skills/` distribution with the OpenAI manifest and required assets
4. submit or publish the new version through the supported OpenAI Platform update flow
5. verify the published version after directory propagation

## Public Plugins Directory

Version 3.2.1 is prepared as a skills-only OpenAI update. The tracked handoff lives under `submission/` and includes listing metadata plus exactly five positive and three negative reviewer cases.

See [`../submission/README.md`](../submission/README.md) for the tracked handoff.

## Validation

Run the OpenAI compatibility gate:

```bash
python3 scripts/validate_codex_plugin.py
```

For a complete repository release gate, also run the shared validators documented in [`development.md`](development.md).
