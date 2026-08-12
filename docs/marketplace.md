# Marketplace Packaging

Version 3.3.0 ships two host adapters with shared quality intent and host-specific execution packaging.

- Claude marketplace: `.claude-plugin/marketplace.json`
- Claude plugin manifest: `.claude-plugin/plugin.json`
- Claude Skills and workers: `skills/` + `agents/`
- OpenAI repo marketplace: `.agents/plugins/marketplace.json`
- OpenAI plugin manifest: `.codex-plugin/plugin.json`
- OpenAI public Skills bundle: `openai-skills/`

The plugin name is `linkedin-animated-infographics`. The marketplace source name is `mamdouh-creative-tools`.

## Claude Code

Install from Claude Code:

```text
/plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics
/plugin install linkedin-animated-infographics@mamdouh-creative-tools
```

Claude keeps the existing native worker architecture. The OpenAI packaging change does not replace Claude agents or change the Claude routing contract.

Validate Claude packaging:

```bash
python3 scripts/validate_marketplace.py
claude plugin validate .
```

## Codex and ChatGPT

Add the repository marketplace with a current Codex CLI:

```bash
codex plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics --ref main
codex plugin marketplace list
```

The root `.codex-plugin/plugin.json` points at `./openai-skills/`.

The OpenAI public workflow is compiled into `openai-skills/linkedin-infographic-studio/` so a skills-only installation does not depend on Claude-only agents, helper routing, or repository worker registration.

Use a supported Plugins Directory surface to install and test the public plugin.

Validate the OpenAI package with:

```bash
python3 scripts/validate_codex_plugin.py
```

See [`codex.md`](codex.md) for the full Codex/ChatGPT contract and visual QA rules.

## Quality parity

Host parity means equivalent discipline and acceptance criteria, not identical visuals.

Claude and OpenAI may make different creative choices. Both should preserve:

- evidence integrity
- concept exploration before layout
- macro-layout planning before component styling
- still QA before motion
- adversarial visual critique
- bounded repair before delivery

## Public OpenAI directory

The 3.3.0 OpenAI package is prepared as a skills-only update. Tracked reviewer materials live in `submission/`.

Repository commits do not automatically replace the package already published in the OpenAI Plugins Directory. A new package/version still needs the supported OpenAI Platform update and publication flow.

## Versioning

The 3.3.0 release must agree across:

- `.claude-plugin/plugin.json`
- the plugin entry inside `.claude-plugin/marketplace.json`
- `.codex-plugin/plugin.json`
- `compatibility/codex.json`
- `submission/openai-plugin.json`

The top-level Claude marketplace catalog has its own catalog version and does not need to equal the plugin version.

## Release gate

Before publishing a packaging release:

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

Do not treat a release as complete until the exact commit passes the applicable shared validators, both host packaging validators, and available install smoke checks.
