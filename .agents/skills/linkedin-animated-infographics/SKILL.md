---
name: linkedin-animated-infographics
description: Use when building, concepting, styling, animating, rendering, auditing, or reviewing LinkedIn animated or static infographics to ensure MasterOne front-door onboarding, GPT-5.6 Sol / Pro Agent Router worker delegation, 30-second watchdog liveness supervision, and deterministic 17-subagent production sequencing.
---

# LinkedIn Animated Infographics: Master Orchestration Engine

## Overview
This skill coordinates the entire LinkedIn animated and static infographic production ecosystem. Start with `helper/GUIDE.md`; do not create a parallel routing or capability model.

## Machine-readable authority
- `helper/router.json`: routes
- `helper/capabilities.json`: owners and plugin-local defaults
- `helper/quality-gates.json`: local creative/product gates
- `helper/artifacts.json`: handoff artifacts
- `helper/modules.json`: active skills, agents, and public tools
- `research/capability-notes/gates.json`: adopted research-derived runtime gates
- `architecture/plugin-graph.json`: shipping sequence and required skill preloads
- the merged registry returned by `scripts/info_stories.py::load_catalog()`: complete Info-stories authority

The merged registry returned by `scripts/info_stories.py::load_catalog()` combines `skills/info-stories/catalog.json` with `skills/info-stories/extensions/*.json`. `catalog.json` alone is not the complete authority.


## Actual stack
- Python 3 for validators, registries, render tooling, and public CLIs
- Markdown for skills, agents, docs, research, and plans
- HTML / CSS / SVG for fixed 1080x1350 artboards and deterministic motion
- shell for setup/lint/render wrappers
- JSON for plugin, routing, capability, gate, artifact, module, and Info-stories contracts
- unittest for regression and architecture tests

---


## When to Use

```
User Request
     │
     ▼
[Step 0: MasterOne Front-Door] ────► Check/Create `.linkedin-infographics/profile.json`
     │                               Ask ONLY route-relevant blocking gaps
     ▼
[Step 1: Router Classification]
     ├──────────────────────┬──────────────────────┬──────────────────────┐
     ▼                      ▼                      ▼                      ▼
`create-post`              `qa`                  `render`            `focused`
(`new-post` pipeline)    (`qa-post`)           (`render-gif`)   (design-study, mascot, info-story, share-demo)
     │
     ▼
[Step 2: Dynamic Agent Router Delegation (GPT-5.6 Sol / Pro vs Fast Tier)]
[Step 3: 30s Watchdog Heartbeat Active (`schedule DurationSeconds=30`)]
     │
     ▼
`design-study` ──► `evidence-checker` ──► `asset-curator` ──► `creative-director (Sol/Pro)` ──►
`story-architect` ──► `palette-curator` ──► `type-curator` ──► `copy-compressor (Flash)` ──►
`layout-composer (Sol/Pro)` ──► `caption-writer (Flash)` ──► `artboard-builder` ──► `motion-director (Sol/Pro)` ──►
`optional mascot-animator` ──► `motion-engineer` ──► `render-qa` ──► `post-critic (Sol/Pro)` ──► `story-verifier (Sol/Pro)`
     │
     ▼
[Step 4: Render QA & Certification] ────► Headless Puppeteer Capture -> Zero-Seam GIF
```

### Triggering Conditions:
- User wants to create a new LinkedIn animated or static infographic from scratch, a prompt, a topic, an article, or raw data.
- User wants to review, inspect, QA, or redesign an existing infographic artifact (`build/post.html`, `build/still.png`, `build/post.gif`).
- User wants to animate an official vector mascot SVG, analyze reference design DNA, or render a GIF.
- User needs project onboarding to set up or update brand colors, copyright footers, fonts, or audiences.

---

## Intelligent Agent Router: Model Tier Allocation

The orchestrator dynamically routes subagent tasks based on complexity and cognitive load:

| Model Tier | Assigned Subagents | Rationale & Task Characteristics |
| :--- | :--- | :--- |
| **High-Reasoning Tier**<br>(`pro` / `GPT-5.6 Sol` / `Opus`) | • `creative-director`<br>• `layout-composer`<br>• `motion-director`<br>• `post-critic`<br>• `story-verifier` | **Complex Synthesis & Judgment:** Visual concept architecture, macro-rhythm, tension hooks, mathematical physics curves, adversarial multi-axis critique, and independent release certification. |
| **High-Speed Execution Tier**<br>(`flash` / `GPT-5.6 Mini`) | • `copy-compressor`<br>• `caption-writer`<br>• `palette-curator`<br>• `type-curator`<br>• `evidence-checker`<br>• `render-qa`<br>• `masterone` | **Precision & Throughput:** Exact slot token fitting, mobile-truncation proof copy, contrast floor verification, font stack schema validation, and headless diff checking. |
| **Tool Execution Tier**<br>(`inherit` + Write Tools) | • `artboard-builder`<br>• `motion-engineer`<br>• `mascot-animator`<br>• `community-publisher` | **Deterministic Artifact Generation:** Generating 1080x1350 HTML, CSS `@keyframes`, SVG rigging, and GitHub PR staging. |

---

## 30-Second Watchdog Liveness Heartbeat

To ensure that autonomous multi-agent pipelines never freeze or loop indefinitely, the orchestrator implements a **30-second Watchdog protocol**:

### 1. Watchdog Scheduling
At the start of execution, schedule a recurring 30-second heartbeat check:
```json
{
  "DurationSeconds": 30,
  "TimerCondition": "any",
  "Prompt": "Watchdog Heartbeat: Check active worker states, inspect build/ artifact mtimes, and detect stalls."
}
```

### 2. Watchdog Heartbeat Responsibilities
Every 30 seconds upon wake-up:
1. **List Active Subagents**: Call `manage_subagents(Action="list")` to inspect live lifecycle states.
2. **Inspect Artifact Generation**: Check the `build/` directory for updated artifact timestamps.
3. **Stall Detection**: If an active worker shows no output progress for **2 consecutive watchdog intervals (60s)**, send an inquiry message via `send_message` or cancel and re-dispatch with a simplified prompt.
4. **Bounded Repair Enforcement**: Enforce a strict maximum of **2 repair iterations** per quality failure before returning a structured `HOLD` to MasterOne.

---

## Core Operational Workflow

### Phase 0: MasterOne Front-Door Protocol (`masterone`)
**Every infographic request must enter through MasterOne first.** MasterOne prepares reusable project context and resolves only missing blockers before routing.

1. **Inspect Existing Profile**: Read `.linkedin-infographics/profile.json` if present.
2. **Initialize if Missing**: If absent, create `.linkedin-infographics/profile.json` using `schemas/masterone-profile.schema.json`.
3. **Resolve ONLY Route-Relevant Blockers**:
   - For `create-post`, required blocking fields are:
     - `content.default_language` (e.g. `"en"`, `"ar"`, `"bilingual"`)
     - `content.audience` (e.g. `"B2B SaaS Founders"`, `"AI Engineers"`)
     - `linkedin.output_mode` (`"animated"` or `"static"`)
     - `copyright.footer_text` (ONLY if `copyright.footer_required` is `true`)
   - **Do NOT block** on optional brand colors, fonts, or mascots unless the request explicitly requires them.
   - Ask for all missing blocking fields in **one single compact turn**. Never ask for fields already provided.
4. **Persist Context**: Save user answers back to `.linkedin-infographics/profile.json`.

---

### Phase 1: Intent Routing & Dispatch
Map the user request to the exact canonical route in `helper/router.json`:

| User Intent | Route Name | Target Parent Workflow | Skills Loaded |
| :--- | :--- | :--- | :--- |
| Create complete new infographic | `create-post` | `new-post` | `info-stories`, `artboard`, `motion`, `caption`, `render` |
| Inspect existing HTML / PNG / GIF | `qa` | `qa-post` | `render`, `artboard`, `qa-post` |
| Render HTML to GIF / Still | `render` | `render-gif` | `render` |
| Analyze visual reference DNA | `design-study` | `design-study` | `artboard`, `info-stories` |
| Animate exact SVG mascot | `mascot-animation` | `svg-mascot-animator` | `mascots`, `svg-mascot-animator`, `motion` |
| Compose standalone story block | `info-story` | `info-stories` | `info-stories`, `artboard` |
| Publish to Community Gallery | `share-demo` | `share-demo` | `share-demo` |

---

### Phase 2: The 17-Subagent Production Sequence (`new-post`)

| Step | Worker Name | Model Tier | Input Artifacts | Output Artifact | Key Quality / Research Gate |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **01** | `design-study` | `flash` | User visual references | `build/reference-dna.json` | `reference-dna`, `structural-originality` |
| **02** | `evidence-checker` | `flash` | Raw text, URLs, metrics | `build/evidence.json` | `evidence-traceability` (Anti-hallucination) |
| **03** | `asset-curator` | `inherit` | Named logos, tools, AI models | `build/asset-plan.json` | `verified-identity-assets` (Lobe-first; HOLD if missing) |
| **04** | `creative-director` | `pro` / `Sol` | Evidence + Asset Plan | `build/creative-concepts.json` | `hooked-design-copy`, `clean-creative-structure` |
| **05** | `story-architect` | `inherit` | Creative concept + Archetype | `build/story-brief.json` | Story House tokens & slot definition |
| **06** | `palette-curator` | `flash` | Story Brief + Brand preferences | `build/palette-check.json` | `restrained-palette` (WCAG contrast floors) |
| **07** | `type-curator` | `flash` | Story Brief + Language | `build/type-spec.json` | `intentional-typography` (Embedded Base64 / Local / System) |
| **08** | `copy-compressor` | `flash` | Story Brief + Type Spec | `build/artboard-copy.json` | `prose-specificity`, `anti-slop` slot checks |
| **09** | `layout-composer` | `pro` / `Sol` | Copy + Palette + Type Spec | `build/layout-spec.json` | `center-first-composition` (or documented exception) |
| **10** | `caption-writer` | `flash` | Copy + Story Brief + Evidence | `build/caption.md`, `first-comment.md` | Mobile truncation cut (< 55 chars line 1) |
| **11** | `artboard-builder` | `inherit` | Layout Spec + Assets + CSS | `build/post.html`, `build/still.png` | **Frame 0 Complete & Feed-Legible** |
| **12** | `motion-director` | `pro` / `Sol` | Approved Still + Story Brief | `build/motion-direction.json` | Single `--loop` clock, max 2 motion primitives |
| **13** | `mascot-animator` | `inherit` | *(Optional)* Exact mascot SVG | `build/mascot-motion.json` | `mascot-identity` physics & squash/stretch |
| **14** | `motion-engineer` | `inherit` | Approved HTML + Motion Plan | `build/post.html` (updated) | Pure CSS / SMIL keyframes (Seekable & deterministic) |
| **15** | `render-qa` | `flash` | Animated `build/post.html` | `build/render-report.json`, `post.gif` | Changed pixels < 0.5%, Seam ratio `x1.0`-`x1.25` |
| **16** | `post-critic` | `pro` / `Sol` | Still, GIF, Code, Evidence | `build/post-critique.json` | 6-axis quality scoring; Max 2 repair loops |
| **17** | `story-verifier` | `pro` / `Sol` | All artifacts + QA Reports | `build/verification-report.json` | `bounded-verification` PASS certification |

---

## Core Design & Physics Invariants

### 1. Viewport Geometry
- **Dimensions:** Strictly `1080px` width by `1350px` height.
- **Safe Padding:** Outer margin of at least `48px - 64px` around all storytelling elements.
- **Attribution Footer:** Anchored to bottom `0px`, height `84px`, full width `1080px`.

### 2. Identity Assets (Lobe-First Policy)
- Exact user-supplied vector assets take first priority.
- Named AI models, dev tools, cloud providers, and frameworks resolve via **Lobe Hub** (`@lobehub/icons`).
- Missing or unverifiable identity marks must **HOLD**. Never generate, approximate, trace, or hallucinate trademarked logos.

### 3. Intentional Typography
- **Zero Network Dependency:** No `@import url('https://fonts.googleapis.com/...')` during capture.
- Custom fonts must be embedded as **Base64 WOFF2** or use robust System UI font stacks.
- Validate type specs with `python3 tools/type_spec_check.py build/type-spec.json`.

### 4. Deterministic Single-Clock Motion Physics
- Define one master variable: `--loop: 6s` or `--loop: 8s`.
- All keyframes, squashes, rings, and highlights express their timings as percentages of `--loop`.
- Frame 0 (at `0%`) must equal Frame N (at `100%`) for seamless infinite looping (`Seam ratio <= x1.25`).
- **Changed-Pixel Budget:** Target `< 0.5%` changed pixels per frame. Avoid full-canvas `filter: blur()` or massive `backdrop-filter` sweeps that balloon GIF file sizes.

---

## Anti-Rationalization & Red Flags

| Rationalization / Excuse | Reality & Hard Rule |
| :--- | :--- |
| *"I'll skip MasterOne and start designing immediately."* | **Forbidden.** Skipping MasterOne loses persistent preferences and risks recreating conflicting footer, language, or brand settings. |
| *"I don't have the exact logo, so I'll generate a placeholder SVG."* | **Forbidden.** Unresolved identities must return a **HOLD**. Approximating official marks violates brand authenticity. |
| *"I'll import Google Fonts via CSS @import."* | **Forbidden.** Remote font calls cause blank/flaky headless captures. Embed Base64 WOFF2 or use system font stacks. |
| *"I'll use JavaScript `requestAnimationFrame` for animation."* | **Forbidden.** Runtime JS animations cannot be seeked deterministically by `capture_frames.py`. Use pure CSS `@keyframes`. |
| *"I'll let a hung subagent run indefinitely without checking."* | **Forbidden.** The 30-second watchdog must detect stalls within 60s and enforce bounded recovery. |

---

## Verification & Doctor Suite

Execute these deterministic commands to verify any infographic or workflow modification:

```bash
# 1. Antigravity plugin and agent definition validation
python3 scripts/validate_antigravity_plugin.py
python3 scripts/antigravity_agents.py check

# 2. Ecosystem doctor, routing, and research gates
python3 scripts/ecosystem_doctor.py check
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check

# 3. Full test discovery
python3 -m unittest discover -s tests -v
```
