# Visual Intelligence Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the existing LinkedIn infographic plugin into a deterministic, reference-aware visual intelligence engine using the supplied GIF corpus without copying or packaging unverified source media.

**Architecture:** Deepen the canonical `design-study` handoff and the existing Info-stories registry. One Pillow/stdlib ingestion module creates stable local reference state; one merged `mechanisms` axis supplies reusable creative knowledge; fixed-rule retrieval produces compact consumer-specific context. Existing story, layout, motion, render, critic, and verifier artifacts remain authoritative.

**Tech Stack:** Python 3.11+, unittest, Pillow, Playwright, ffmpeg, JSON, Markdown, HTML/CSS/SVG.

## Global Constraints

- Preserve every unrelated tracked and untracked user change; never stage `.claude/agents/**` or unrelated scratch assets.
- Bun remains mandatory for any JavaScript/TypeScript command; this repository's implementation path is Python.
- Add no embedding model, vector database, network service, or new dependency.
- Source GIFs and sampled frames stay in ignored `.plugin-state/reference-studies/`; Git stores metadata and guidance only.
- Preserve existing `REF-001` through `REF-034`; add the missing unique asset as `REF-035`; retain duplicate IDs as aliases.
- Do not create a second workflow, a new coordinating agent, or a competing design-spec artifact.
- Use failing behavior tests before production changes and fresh focused checks after every mutation.
- Keep the current worker order and canonical artifact responsibilities.
- Every completion claim names changed files, command outcomes, and unverified boundaries.

---

### Task 1: Complete the measured render contract already in progress

**Files:**
- Modify: `scripts/check_render.py`
- Modify: `scripts/build_gif.py`
- Modify: `scripts/render.sh`
- Create: `scripts/render_report.py`
- Complete existing WIP: `helper/visual-contract.json`, `scripts/visual_contract.py`, `scripts/render_probe.py`, `scripts/artboard_audit.py`
- Modify: `agents/render-qa.md`, `skills/artboard/SKILL.md`, `skills/qa-post/SKILL.md`, `skills/render/references/qa-gates.md`, `skills/motion/references/animation-recipes.md`
- Test: `tests/test_visual_contract.py`, `tests/test_artboard_audit.py`, `tests/test_cli_contracts.py`, new `tests/test_render_report.py`

**Interfaces:**
- Consumes: `VisualContract`, shared probes, current render commands.
- Produces: `--mobile/--no-mobile`, JSON audit fragments, merged `build/render-report.json`, non-zero blocking verdicts.

- [ ] Confirm RED with `/opt/homebrew/bin/python3 -m unittest -v tests.test_cli_contracts`; expected five failures naming the two missing mobile flags.
- [ ] Add a mutually exclusive mobile flag group with `mobile=True` default and guard preview creation with `args.mobile`.
- [ ] Replace duplicated still-audit probes with `scripts/render_probe.py` and contract thresholds.
- [ ] Add `--json` output to still and GIF checks; every row includes measurement, threshold, unit, severity, status, and evidence.
- [ ] Implement `render_report.py merge` over artboard, still, and GIF fragments; fail on missing/NA blocking evidence and record input/output SHA-256 digests.
- [ ] Wire lint, artboard audit, still capture, frame capture, GIF build, and merge into `scripts/render.sh`.
- [ ] Run the focused render/CLI tests and real pass/fail fixtures.
- [ ] Commit only Task 1 files as `feat: enforce measured render contract`.

### Task 2: Ingest references with stable identity and cached real assets

**Files:**
- Create: `scripts/reference_intelligence.py`
- Modify: `.gitignore`
- Create: `research/reference-studies/visual-library.json`
- Create: `tests/fixtures/references/valid.gif`, `tests/fixtures/references/invalid.gif`
- Create: `tests/test_reference_intelligence.py`

**Interfaces:**
- Produces: `ingest_library(library: Path, state_dir: Path, curated: dict) -> dict`, `load_reference_library(...)`, CLI commands `ingest`, `check`.
- State: `.plugin-state/reference-studies/{manifest.json,assets/,frames/}`.

- [ ] Write behavior tests for stable IDs, SHA aliases, corrupt input, cache reuse, unusual dimensions/durations, transparent GIFs, and missing metadata.
- [ ] Verify each new test fails for the intended missing behavior.
- [ ] Implement Pillow/stdlib decoding and SHA-256 identity; always copy canonical assets into ignored state and sample first/middle/final/pre-seam frames.
- [ ] Preserve the curated legacy ID map, add `REF-035`, and retain duplicate IDs as deprecated aliases.
- [ ] Record dimensions, bytes, frame count, duration, FPS, loop, palette shares, frame completeness, changed-pixel mean, seam ratio, and local asset/frame paths.
- [ ] Fail clearly on corrupt/empty inputs; never swallow decode errors or emit an empty-success manifest.
- [ ] Run focused tests, ingest all 37 real GIFs, run `check`, and record 31 canonical assets plus six aliases.
- [ ] Commit Task 2 files as `feat: add stable GIF reference ingestion`.

### Task 3: Add curated mechanisms and deterministic retrieval

**Files:**
- Modify: `scripts/info_stories.py`
- Create: `skills/info-stories/extensions/idea-mechanisms.json`
- Create: `tools/story_retrieve.py`
- Modify: `helper/modules.json`
- Modify: `skills/info-stories/SKILL.md`
- Create: `tests/test_info_story_retrieval.py`

**Interfaces:**
- Produces: `validate_mechanisms(catalog)`, `rank_mechanisms(catalog, query)`, `build_context_capsule(...)`.
- CLI: `python3 tools/story_retrieve.py --query <json-path>` writes one deterministic JSON result.

- [ ] Write failing tests for mechanism schema, duplicate slugs/fingerprints, broken reference IDs, hard filters, score explanations, shuffled-input determinism, slug tie-breaks, top-k, and UTF-8 byte budgets.
- [ ] Extend `load_catalog()` to merge `mechanisms` from extension files and validate a cap of 150.
- [ ] Curate a substantial non-duplicate library split between `extracted` and `new`; each row includes story jobs, content shapes, compatibility, layout/hierarchy/type/motion/loop logic, constraints, anti-patterns, implementation hints, and reference IDs where applicable.
- [ ] Implement fixed weighted overlap after hard filtering; do not use embeddings or LLM ranking.
- [ ] Select one primary reference and at most one motion and one typography reference, each with an explicit influence axis.
- [ ] Build stage-specific capsules and enforce the byte budget after JSON serialization.
- [ ] Register the public tool with truthful tests and reachable guidance, then run the catalog, retrieval, doctor, and module tests.
- [ ] Commit Task 3 files as `feat: add visual mechanism retrieval`.

### Task 4: Deepen the existing study and quality contracts

**Files:**
- Modify: `scripts/info_stories.py`
- Modify: `skills/info-stories/references/study-protocol.md`
- Create: `skills/info-stories/references/typography-intelligence.md`
- Create: `skills/info-stories/references/quality-scoring.md`
- Modify: `agents/design-study.md`, `agents/story-architect.md`, `agents/layout-composer.md`, `agents/motion-director.md`, `agents/post-critic.md`, `agents/story-verifier.md`
- Modify: `helper/artifacts.json`
- Test: `tests/test_reference_intelligence.py`, new `tests/test_visual_quality_contract.py`

**Interfaces:**
- Extends: `validate_study_report(report)` without breaking legacy required fields.
- Produces: `validate_visual_quality_report(report)` with six rubric axes and blocking verdict.

- [ ] Write failing tests for ranked study evidence, confidence, provenance/rights, focused contexts, type roles/font policy, motion jobs/static regions, originality decisions, and evidence-backed quality rows.
- [ ] Extend study validation and agent contracts; explicit reference requests HOLD on missing/invalid evidence, while no-reference flows return an explicit SKIP.
- [ ] Add typography roles with stack ID, scripts, weights, and exact/fallback policy; never infer exact screenshot fonts.
- [ ] Require every motion to name one communication job, target, sequence, duration/easing family, hold/reset, and static regions.
- [ ] Validate the six existing taste axes at 1–5; any applicable score below 3 blocks and every score carries evidence plus an actionable finding.
- [ ] Keep final choices in story/layout/motion artifacts and only reference the selected study IDs/capsules.
- [ ] Run focused study, agent, artifact, graph, and quality tests.
- [ ] Commit Task 4 files as `feat: make visual decisions traceable`.

### Task 5: Integrate routing, safety, and OpenAI parity

**Files:**
- Modify: `helper/router.json`, `helper/capabilities.json`, `helper/quality-gates.json`, `research/capability-notes/gates.json`, `architecture/plugin-graph.json`, `helper/GUIDE.md`
- Modify: `skills/new-post/SKILL.md`
- Modify: `openai-skills/linkedin-infographic-autopilot/SKILL.md`, `openai-skills/linkedin-infographic-studio/SKILL.md`
- Create: focused OpenAI visual-intelligence reference/capsule under the existing skills
- Modify: `scripts/validate_codex_plugin.py`, `compatibility/codex.json`
- Test: router, graph, doctor, capability, packaging, and OpenAI parity tests.

**Interfaces:**
- Reference diagnosis becomes conditional but remains at the first worker seam.
- OpenAI packages consume a compact generated capsule plus canonical digest; unavailable persistent ingestion is reported as a capability boundary.

- [ ] Write failing routing/parity tests for explicit-reference HOLD, no-reference SKIP, raw-asset export exclusion, capsule digest drift, and equivalent fixture selections.
- [ ] Remove redundant unconditional reference work while preserving route order and capability ownership.
- [ ] Block source GIFs, contact sheets, absolute paths, and unresolved-rights media from public demo packaging.
- [ ] Generate and validate the compact OpenAI capsule from the canonical registry; do not hand-copy the entire library.
- [ ] Run router, graph, ecosystem doctor, package, and cross-host parity checks.
- [ ] Commit Task 5 files as `feat: integrate reference intelligence across hosts`.

### Task 6: Validate the real corpus and representative generation paths

**Files:**
- Create: `examples/info-stories/reference-retrieval-briefs.json`
- Create: `research/reference-studies/2026-08-11-gif-library-validation.md`
- Update implementation only where real validation exposes a systemic defect.

**Interfaces:**
- Uses the real ignored state produced by Task 2 and the canonical retrieval/runtime paths from Tasks 3–5.

- [ ] Ingest and check all 37 GIFs; prove 31 canonical and six aliases with no corrupt files.
- [ ] Run seven briefs: maturity ladder, model selection, radial ecosystem, layered stack, editorial comparison, human/AI handoff, and local-tool setup.
- [ ] Assert retrieval diversity, deterministic reruns, actual local asset/frame accessibility, and measured context budgets.
- [ ] Produce at least three representative story/layout/motion artifacts through the real scaffold/retrieval path.
- [ ] Render representative outputs when the repository path supports it; inspect still, mobile, middle, final, and seam frames for hierarchy, clipping, font resolution, generic-AI patterns, motion purpose, and originality.
- [ ] Apply only systemic corrections, rerun the exposing check, and record measured evidence and limitations.
- [ ] Commit Task 6 files and any verified corrections as `test: validate real visual reference flow`.

### Task 7: Documentation, version, full gates, and independent review

**Files:**
- Modify: `README.md`, `docs/development.md`, `docs/routing.md`, `docs/skills.md`, `docs/agents.md`
- Modify version surfaces to `3.3.0` only after public behavior and package parity are green.
- Modify CI to install render dependencies and execute pass/fail render fixtures.

**Interfaces:**
- Documents only commands, files, fields, limits, and outcomes verified against the final implementation.

- [ ] Document ingestion, stable IDs/aliases, local state, analysis boundary, curation, retrieval, focused context, typography/motion/taste contracts, adding references, cache refresh, debugging, rights limitations, and real validation.
- [ ] Run docs-guard against every CLI flag, symbol, schema, and path.
- [ ] Run test-guard and clean-code-guard against the complete task diff; fix concrete findings.
- [ ] Run the full unittest suite, compileall, Info-stories, router, research gates, plugin graph, ecosystem doctor, demo gallery, marketplace, Codex/OpenAI validator, JSON/shell syntax, real reference checks, and render fixtures.
- [ ] Dispatch an independent whole-branch architecture/code/visual review; fix load-bearing findings and re-run affected gates.
- [ ] Bump all validated plugin/version surfaces to `3.3.0`, re-run package parity, and commit as `release: prepare visual intelligence 3.3.0`.
- [ ] Leave push, PR, and publication untouched; report every commit, changed file, check outcome, and unverified boundary.
