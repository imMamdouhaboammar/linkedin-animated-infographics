# Repository Agent Guide

This repository is an executable multi-host plugin ecosystem for evidence-safe LinkedIn infographics. Claude Code, Codex, and ChatGPT use package adapters around the same canonical product core. Do not treat `skills/`, `agents/`, `research/`, `helper/`, or `tools/` as independent islands.

## Start here

Read `helper/GUIDE.md` before changing or running production behavior.

Machine-readable authority:

- `helper/router.json`: request to workflow/skills/agents/capabilities
- `helper/capabilities.json`: capability owners and plugin-local defaults
- `helper/quality-gates.json`: local creative/product gates
- `helper/artifacts.json`: worker handoff artifacts
- `helper/modules.json`: active public module manifest
- `research/capability-notes/gates.json`: adopted research-derived runtime gates
- `architecture/plugin-graph.json`: executable worker order and skill preloads
- `scripts/info_stories.py::load_catalog()`: merged Info-stories registry
- `skills/info-stories/references/asset-source-policy.md`: Lobe-first verified identity policy
- `skills/info-stories/references/typography-direction.md`: intentional typography policy
- `compatibility/codex.json`: OpenAI package/parity declaration

Run the strict runtime and host-package validators after structural changes:

```bash
python3 scripts/ecosystem_doctor.py check
python3 scripts/validate_marketplace.py
python3 scripts/validate_codex_plugin.py
```

## Complete production path

`new-post` is the parent workflow. Workers return artifacts to it; workers do not orchestrate peers directly.

The complete path is:

`design-study -> evidence-checker -> asset-curator -> creative-director -> story-architect -> palette-curator -> type-curator -> copy-compressor -> layout-composer -> caption-writer -> artboard-builder -> motion-director -> optional mascot-animator -> motion-engineer -> render-qa -> post-critic -> story-verifier`

`asset-curator` owns verified identity sourcing. `creative-director` owns concept structure. `type-curator` owns intentional typography before copy fitting. Downstream workers preserve `build/asset-plan.json` and `build/type-spec.json` rather than selecting replacements.

Attention-bearing design copy follows `hooked-design-copy`, and a complete concept should produce a useful `creative-payoff` with `clean-creative-structure` rather than decorative spectacle.

After verified delivery, `share-demo` may run only with explicit user consent. Community publishing ends at an open contributor PR and requires maintainer manual review and merge.

## Product defaults

- Palette default: `creative-attractive-restrained`
- Composition default: `center-first`
- Identity default: Lobe-first after an exact user-supplied official asset. Supported named AI/tool identities resolve through Lobe; missing verified identity assets HOLD instead of being approximated
- Typography default: intentional typography. User-specified or supplied render-safe fonts win; otherwise use a curated deterministic system direction. Remote font loading during capture is forbidden
- Creative structure: one dominant visual anchor, explicit relationship, deliberate containment, and deliberate negative space. Repeated cards are used when repetition is the story
- Alignment exceptions are valid for tables, UI mockups, code/terminal surfaces, timelines, Arabic/RTL flow, or documented reference DNA when they improve comprehension/fidelity
- UI mockups that look real must be evidence-backed; conceptual UI must be identifiable when readers could mistake it for product proof

## Host packaging

- Claude Code: `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`
- Codex/ChatGPT: `.codex-plugin/plugin.json` + `.agents/plugins/marketplace.json`
- canonical bundled workflows: `skills/`
- Codex repo-development helpers: `.codex/config.toml` + `.codex/agents/*.toml`

Do not create copied Codex-specific product Skills. The installed OpenAI plugin must not depend on the maintainer's `.codex/config.toml` or private MCP configuration.

## Research gates

Research under `research/` is active production guidance. Adopted runtime gates live in `research/capability-notes/gates.json` and are validated by:

```bash
python3 scripts/research_gates.py check
```

Do not package ignored `research/upstreams/` clones. Keep source URL, inspected SHA, license, Adopt/Adapt/Reject decisions, local implementation references, shipping owners, and tests.

## Change method

1. Add or update a failing regression/contract test
2. Implement the minimum coherent change
3. Run focused tests
4. Run the full suite and validators
5. Update docs/manifest/version when public behavior changes
6. Merge only after exact-head host validation, available marketplace smoke checks, repository checks, and review findings are clean

Minimum deterministic gate:

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
```

## Safety

Never commit credentials, private MCP data, or user secrets. Do not fabricate claims, metrics, logos, UI states, testimonials, product behavior, or identity assets to satisfy a visual slot. Report browser/render environment blockers separately from non-browser validation. Do not claim OpenAI public-directory publication until the external submission, review, and publication steps have actually completed.
