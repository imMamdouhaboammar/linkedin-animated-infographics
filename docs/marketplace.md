# Claude Marketplace

The plugin and marketplace live in the same repository.

- marketplace: `mamdouh-creative-tools`
- plugin: `linkedin-animated-infographics`
- plugin release: `3.1.0`
- marketplace source: `./`
- strict mode: `true`

## Install

In Claude Code:

```text
/plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics
/plugin install linkedin-animated-infographics@mamdouh-creative-tools
```

The marketplace catalog is `.claude-plugin/marketplace.json`; the plugin manifest is `.claude-plugin/plugin.json`.

## Validate locally

```bash
python3 scripts/validate_marketplace.py
claude plugin validate .
```

The local validator checks the same-repository source, strict mode, plugin identity, version agreement, required component directories, demo/schema components, and manifest fields.

## CI install smoke

The GitHub validation workflow creates a clean temporary Claude home, registers the checked-out repository as a local marketplace, verifies that `mamdouh-creative-tools` appears in the marketplace list, and installs:

```text
linkedin-animated-infographics@mamdouh-creative-tools
```

That smoke test proves the marketplace entry is not only schema-valid but installable from the repository layout used by CI.

## Versioning

The plugin manifest version and marketplace plugin-entry version must match.

Version `3.1.0` adds the owned/community demo gallery and opt-in publisher flow on top of the v3 routing-kernel architecture. It includes `share-demo`, `community-publisher`, the strict three-file demo schema, deterministic gallery catalog, export/privacy preflight, and manual-review PR policy.

The top-level marketplace catalog has its own catalog version. It does not need to match the plugin version.

Any future public plugin release should update both the plugin manifest and its marketplace entry and rerun the official Claude validator plus marketplace add/install smoke.

## Release gate

Before merging a marketplace release:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/demo_gallery.py check
python3 scripts/validate_marketplace.py
claude plugin validate .
```

Do not treat a version bump as complete until CI installs that exact checked-out plugin from the same-repository marketplace.
