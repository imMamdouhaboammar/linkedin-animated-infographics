# linkedin-animated-infographics

A Claude Code plugin for designing, validating, rendering, and animating evidence-safe LinkedIn infographics with structured Info-stories, creative concept development, UI mockup stories, exact-SVG mascots, Arabic/RTL support, deterministic GIF rendering, and strict repository validation.

Current plugin release: **3.0.0**

## Install from Claude Marketplace

```text
/plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics
/plugin install linkedin-animated-infographics@mamdouh-creative-tools
```

The marketplace and plugin live in this same repository. Validate a local checkout with:

```bash
claude plugin validate .
```

## What v3 adds

The repository is now one connected production ecosystem instead of a loose collection of prompts and workers.

- `helper/` is the LLM routing and guidance authority
- `creative-director` develops multiple evidence-safe concepts before story architecture
- attention-bearing design copy uses `hooked-design-copy`
- complete concepts require a useful `creative-payoff`, not decorative spectacle
- palette default is `creative-attractive-restrained`
- composition default is `center-first`, with documented comprehension/fidelity exceptions
- `research/` ships as active runtime capability gates with provenance and real owners
- named or official mascots require the exact user-supplied/task-attached SVG
- UI Mockup Stories are first-class Info-stories with evidence and feed-width fidelity rules
- `scripts/ecosystem_doctor.py` rejects dead, undeclared, unreachable, untested, or disconnected public modules

## Quick architecture

Read [`helper/GUIDE.md`](helper/GUIDE.md) before choosing a workflow or worker.

The complete production path is:

```text
design-study
  -> evidence-checker
  -> creative-director
  -> story-architect
  -> palette-curator
  -> copy-compressor
  -> layout-composer
  -> caption-writer
  -> artboard-builder
  -> motion-director
  -> optional mascot-animator
  -> motion-engineer
  -> render-qa
  -> post-critic
  -> story-verifier
```

`new-post` is the parent workflow. Agents return bounded artifacts to it; they do not secretly orchestrate peer agents.

## Creative runtime

Before layout starts, `creative-director` produces at least three genuinely different directions in `build/creative-concepts.json`. Every direction includes a visual hook, copy hook, aha mechanic, story shape, recommended visual style/archetype/motion, evidence dependencies, risks, and a reason it earns attention.

A useful wow/aha moment can be a reveal, relationship, comparison, transformation, state change, or interaction that makes the idea easier to understand or remember. It is not a license for random 3D, glow, extreme saturation, arbitrary asymmetry, or excessive motion.

Design copy follows one strong-hook principle: hero/opening copy should earn attention through specificity, supported tension, concrete outcome, recognizable problem, useful surprise, or strong framing. Literal labels, commands, table headers, and UI controls stay literal when clarity is the job.

## Visual defaults

- Palette character: `creative-attractive-restrained`
- Composition: `center-first`
- Text contrast: 4.5:1 floor for meaningful text
- State-defining contrast: 3:1 floor
- One clear visual anchor at feed scale

Alignment can move away from center-first when the content genuinely benefits, including tables, UI mockups, code/terminal surfaces, timelines, Arabic/RTL flow, or documented reference-DNA decisions.

## Info-stories

Info-stories resolves four independent choices:

1. Story House
2. Visual Style
3. Story Archetype
4. Motion Pattern

The source of truth is the merged registry returned by `scripts/info_stories.py::load_catalog()`, combining the stable base with first-party extensions.

UI Mockup Stories include UI Storyboard, Interface Cutaway, Screen to Outcome, Inside the Interface, State Change Story, Cursor Focus, and State Transition. Real-looking product behavior must be evidence-backed; conceptual UI must be identifiable when readers could mistake it for product proof.

## Exact-SVG mascots

If the user names a specific or official mascot, the plugin requires the **exact SVG** supplied by the user or attached to the task. It does not redraw, approximate, substitute, or generate a lookalike automatically.

The mascot path inspects the real SVG, identifies addressable geometry, selects a communication-led creative direction, preserves identity, integrates motion, and verifies the result against the untouched source.

```bash
python3 scripts/mascot_contract.py directions
python3 scripts/mascot_contract.py check build/mascot-request.json
```

## Research gates

Tracked research is active production guidance. The current runtime gates are:

`prose-specificity`, `voice-preservation`, `design-dials`, `structural-originality`, `reference-dna`, `contrast-discipline`, `evidence-traceability`, and `bounded-verification`.

Each gate has source provenance, a local independently-worded behavior, stage, severity, real shipping owners, implementation references, and tests. Ignored upstream working copies are never packaged with the plugin.

## Workflows

```text
/linkedin-animated-infographics:new-post    [topic or URL] [--arabic] [--mascot]
/linkedin-animated-infographics:render-gif  [path.html] [--duration 6.0] [--fps 12.5]
/linkedin-animated-infographics:qa-post     [path.html] [caption.md]
```

For programmatic routing:

```bash
python3 tools/route_request.py --request "Create an animated LinkedIn infographic"
```

## Strict validation

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tools skills/svg-mascot-animator/scripts
python3 scripts/info_stories.py check
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/validate_marketplace.py
claude plugin validate .
```

The CI also registers the checked-out repository as marketplace `mamdouh-creative-tools` and installs `linkedin-animated-infographics@mamdouh-creative-tools` in a clean Claude home.

Useful public tools include:

```text
tools/story_scaffold.py
tools/composition_check.py
tools/palette_preview.py
tools/copy_slop_check.py
tools/contrast_check.py
tools/fingerprint_check.py
tools/route_request.py
```

## Documentation

- [Ecosystem architecture](docs/ecosystem.md)
- [Routing protocol](docs/routing.md)
- [Agents](docs/agents.md)
- [Skills](docs/skills.md)
- [Research gates and provenance](docs/research.md)
- [Claude Marketplace](docs/marketplace.md)
- [Development and validation](docs/development.md)

## Development entrypoints

Coding agents should also read [`AGENTS.md`](AGENTS.md) or [`CLAUDE.md`](CLAUDE.md). Both point back to the same helper, research, module, and validation authority.

## License

MIT
