# Marketplace Packaging

Version 3.2.0 ships two host adapters over one canonical product core.

- Claude marketplace: `.claude-plugin/marketplace.json`
- Claude plugin manifest: `.claude-plugin/plugin.json`
- OpenAI repo marketplace: `.agents/plugins/marketplace.json`
- OpenAI plugin manifest: `.codex-plugin/plugin.json`
- canonical Skills for both hosts: `skills/`

The plugin name is `linkedin-animated-infographics`. The marketplace source name is `mamdouh-creative-tools`.

## Claude Code

Install from Claude Code:

```text
/plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics
/plugin install linkedin-animated-infographics@mamdouh-creative-tools
```

Validate locally:

```bash
python3 scripts/validate_marketplace.py
claude plugin validate .
```

CI also registers the checked-out repository as a clean Claude marketplace source and installs `linkedin-animated-infographics@mamdouh-creative-tools`.

## Codex and ChatGPT

Add the repository marketplace with a current Codex CLI:

```bash
codex plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics --ref main
codex plugin marketplace list
```

The OpenAI marketplace entry points at the repository root using a local `./` source. The root `.codex-plugin/plugin.json` points at the canonical `./skills/` tree.

Use a supported Plugins Directory surface to install and test the plugin. Do not substitute undocumented `codex plugin install` syntax for the current marketplace/Plugins Directory flow.

Validate the OpenAI package and cross-host parity with:

```bash
python3 scripts/validate_codex_plugin.py
```

See [`codex.md`](codex.md) for the full Codex/ChatGPT contract.

## Public OpenAI directory

The 3.2.0 OpenAI package is prepared as a skills-only public submission. Tracked reviewer materials live in `submission/`.

The repository status is `prepared-not-submitted`. OpenAI Platform permissions, verified publisher identity, availability selection, submission, review, and final publication remain external steps.

## Versioning

The 3.2.0 release must agree across:

- `.claude-plugin/plugin.json`
- the plugin entry inside `.claude-plugin/marketplace.json`
- `.codex-plugin/plugin.json`
- `compatibility/codex.json`
- `submission/openai-plugin.json`

The top-level Claude marketplace catalog has its own catalog version and does not need to equal the plugin version.

## Release gate

Before merging a packaging release:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/demo_gallery.py check
python3 scripts/validate_marketplace.py
python3 scripts/validate_codex_plugin.py
claude plugin validate .
```

Do not treat a release as complete until the exact PR head passes the shared validators, both packaging validators, the official Claude validator, the available install smoke checks, and review closure.
