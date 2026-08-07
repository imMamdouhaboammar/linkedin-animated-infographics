# Community Demo Publisher Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a first-class owned/community demo gallery and an opt-in publishing workflow that packages verified GIF + HTML output with strict metadata, then prepares a contributor fork/branch/PR for manual maintainer review.

**Architecture:** `demos/` becomes the repository gallery source of truth. `scripts/demo_gallery.py` validates/discovers packages and deterministically owns `demos/catalog.json`; `scripts/demo_submit.py` prepares a safe three-file contribution from final verified build artifacts. A focused `share-demo` skill and `community-publisher` agent sit behind a new helper route and are offered only after `story-verifier` returns PASS. GitHub publication stops at a PR and never merges or writes directly to upstream `main`.

**Tech Stack:** Python 3.12 standard library, JSON Schema document with an in-repo strict validator, Claude Code plugin skills/agents, existing helper/router/module/artifact registries, GitHub CLI or equivalent host-native GitHub integration for fork/branch/PR execution, GitHub Actions, unittest.

## Global Constraints

- Every demo directory contains exactly `demo.gif`, `index.html`, and `demo.json`.
- Community path: `demos/community/<github-user>/<slug>/`; owned path: `demos/owned/<slug>/`.
- `demos/catalog.json` is generated deterministically and never hand-edited.
- Publishing is opt-in and may be offered only after final verification PASS.
- `rights_confirmed` must be true before packaging or publication.
- `source_prompt` is absent by default and is included only with explicit user consent.
- Never publish secrets, credentials, private URLs, local absolute paths, build reports, source documents, or unrelated user files.
- Never infer content rights from context.
- Never write directly to upstream `main`, enable auto-merge, merge a community PR, or force-push unrelated history.
- Every community PR requires manual review and merge by the maintainer.
- Any unavailable GitHub identity/auth/fork/push capability returns HOLD rather than false success.
- The first implementation release is `3.1.0`, derived from current `3.0.0`.

---

## File Map

**Create**
- `schemas/demo.schema.json` — public metadata contract.
- `scripts/demo_gallery.py` — discovery, package validation, catalog build/list/check.
- `scripts/demo_submit.py` — verified-build packaging and contribution preflight.
- `skills/share-demo/SKILL.md` — focused opt-in parent publishing workflow.
- `agents/community-publisher.md` — narrow GitHub fork/branch/PR worker.
- `demos/README.md` — gallery + contribution guide.
- `demos/catalog.json` — generated gallery index.
- `demos/owned/.gitkeep` — tracked owned namespace until a complete three-file owned package is available.
- `demos/community/.gitkeep` — tracked community namespace before first accepted contribution.
- `tests/test_demo_gallery.py` — schema/package/catalog/security behavior.
- `tests/test_demo_submit.py` — packaging/consent/verification/privacy behavior.
- `tests/test_demo_publisher_contract.py` — route/skill/agent/manual-review contract.
- `docs/community-demos.md` — contribution and publisher safety documentation.

**Modify**
- `helper/router.json` — add focused `share-demo` route.
- `helper/artifacts.json` — declare staged demo metadata/package outputs.
- `helper/modules.json` — register new skill, agent, and tools as real reachable modules.
- `architecture/plugin-graph.json` — register publisher worker skill preload without adding it to the critical `new-post` sequence.
- `skills/new-post/SKILL.md` — add post-delivery optional share offer after PASS only.
- `helper/GUIDE.md` — document share-demo routing and opt-in/HOLD semantics.
- `README.md` — compact Demos section and community contribution CTA.
- `docs/ecosystem.md`, `docs/routing.md`, `docs/agents.md`, `docs/skills.md`, `docs/development.md` — focused public contract updates.
- `.github/workflows/claude-plugin-validation.yml` — run `demo_gallery.py check` and validate demo schema JSON.
- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` — bump plugin entry to `3.1.0`.
- `scripts/validate_marketplace.py`, `tests/test_marketplace.py` — update exact release assertions to `3.1.0`.

---

### Task 1: Demo schema and gallery validator

**Files:**
- Create: `schemas/demo.schema.json`
- Create: `scripts/demo_gallery.py`
- Create: `demos/catalog.json`
- Create: `demos/owned/.gitkeep`
- Create: `demos/community/.gitkeep`
- Test: `tests/test_demo_gallery.py`

**Interfaces:**
- Produces: `load_demo(path: Path) -> dict`, `validate_demo_dir(path: Path, root: Path) -> list[str]`, `discover_demos(root: Path) -> list[dict]`, `build_catalog(root: Path) -> dict`, CLI commands `check|build|list`.
- Catalog entry fields: `id`, `title`, `author`, `author_url`, `description`, `created_with`, `language`, `story_type`, `tags`, `gif`, `html`, `created_at`, `license`, `kind`, `path`.

- [ ] **Step 1: Write failing schema/package tests**

```python
class DemoGalleryTests(unittest.TestCase):
    def test_demo_directory_is_exactly_three_public_files(self):
        demo = self.make_demo(extra_files={"notes.txt": "private"})
        self.assertIn("exactly demo.gif, index.html, demo.json", "\n".join(validate_demo_dir(demo, self.root)))

    def test_community_author_namespace_must_match(self):
        demo = self.make_demo(path="demos/community/alice/demo-one", author="bob")
        self.assertIn("author namespace", "\n".join(validate_demo_dir(demo, self.root)))

    def test_paths_cannot_escape_demo_directory(self):
        demo = self.make_demo(gif="../secret.gif")
        self.assertIn("safe local demo path", "\n".join(validate_demo_dir(demo, self.root)))

    def test_rights_confirmation_is_required(self):
        demo = self.make_demo(rights_confirmed=False)
        self.assertIn("rights_confirmed must be true", "\n".join(validate_demo_dir(demo, self.root)))
```

- [ ] **Step 2: Run RED**

Run: `python3 -m unittest tests.test_demo_gallery -v`
Expected: FAIL because `scripts.demo_gallery` and the schema do not exist.

- [ ] **Step 3: Add strict metadata schema**

`schemas/demo.schema.json` must set `additionalProperties: false`, require all approved required fields, permit only the three optional fields, constrain `id` to `^[a-z0-9]+(?:-[a-z0-9]+)*$`, require non-empty tags, require `gif` exactly `demo.gif`, `html` exactly `index.html`, and require `rights_confirmed` to the constant `true`.

- [ ] **Step 4: Implement minimal gallery validator**

```python
PUBLIC_FILES = {"demo.gif", "index.html", "demo.json"}
DEMO_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def safe_child(base: Path, relative: str) -> Path | None:
    candidate = (base / relative).resolve()
    try:
        candidate.relative_to(base.resolve())
    except ValueError:
        return None
    return candidate
```

Validation must reject absolute/escaping paths, unknown metadata keys, incorrect author namespace, duplicate IDs, missing/extra files, empty GIF/HTML, `rights_confirmed != True`, malformed dates, and suspicious local absolute-path strings in metadata.

- [ ] **Step 5: Add deterministic catalog tests**

```python
def test_catalog_order_is_deterministic(self):
    catalog = build_catalog(self.root)
    ids = [item["id"] for item in catalog["demos"]]
    self.assertEqual(sorted(ids), ids)

def test_check_rejects_catalog_drift(self):
    (self.root / "demos/catalog.json").write_text('{"schema_version":1,"demos":[]}')
    self.assertNotEqual([], check_repository(self.root))
```

- [ ] **Step 6: Implement `build|check|list`**

`build` writes JSON with `sort_keys=True`, `indent=2`, trailing newline, and sorted entries. `check` compares the tracked catalog to `build_catalog()` without mutating files. `list` prints the deterministic catalog JSON to stdout.

- [ ] **Step 7: Run GREEN**

Run: `python3 -m unittest tests.test_demo_gallery -v && python3 scripts/demo_gallery.py check`
Expected: PASS with empty catalog and tracked namespaces.

- [ ] **Step 8: Commit**

Commit message: `feat: add strict demo gallery contract`

---

### Task 2: Verified contribution packaging and privacy preflight

**Files:**
- Create: `scripts/demo_submit.py`
- Test: `tests/test_demo_submit.py`
- Modify: `helper/artifacts.json`

**Interfaces:**
- Consumes: `build/post.html`, final GIF path, `build/verification-report.json`.
- Produces: `prepare_submission(build_dir: Path, stage_root: Path, metadata: dict) -> Path`, `check_submission(demo_dir: Path, repo_root: Path) -> list[str]`, CLI `prepare|check`.
- Staged package path: `<stage_root>/community/<author>/<slug>/` containing exactly three files.

- [ ] **Step 1: Write failing verification and consent tests**

```python
def test_prepare_requires_verification_pass(self):
    self.write_verification("FAIL:fixable")
    with self.assertRaisesRegex(ValueError, "verification PASS"):
        prepare_submission(self.build, self.stage, self.metadata())

def test_prepare_requires_rights_confirmation(self):
    data = self.metadata(rights_confirmed=False)
    with self.assertRaisesRegex(ValueError, "rights confirmation"):
        prepare_submission(self.build, self.stage, data)

def test_source_prompt_is_omitted_without_explicit_consent(self):
    data = self.metadata(source_prompt="private prompt", publish_source_prompt=False)
    out = prepare_submission(self.build, self.stage, data)
    manifest = json.loads((out / "demo.json").read_text())
    self.assertNotIn("source_prompt", manifest)
```

- [ ] **Step 2: Run RED**

Run: `python3 -m unittest tests.test_demo_submit -v`
Expected: FAIL because `scripts.demo_submit` does not exist.

- [ ] **Step 3: Implement verification loader and safe copy**

```python
def require_verification_pass(build_dir: Path) -> None:
    report = json.loads((build_dir / "verification-report.json").read_text())
    verdict = str(report.get("verdict", "")).strip().upper()
    if verdict != "PASS":
        raise ValueError("community publishing requires final verification PASS")
```

Copy only selected final HTML to `index.html` and selected GIF to `demo.gif`. Never recursively copy `build/`.

- [ ] **Step 4: Add privacy/secret tests**

Test rejection for HTML or metadata containing common credential markers (`ghp_`, `github_pat_`, `sk-`, `Authorization: Bearer`), `file:///`, `/Users/`, `/home/<name>/`, signed query strings such as `X-Amz-Signature=`, and unsupported `source_prompt` publication.

- [ ] **Step 5: Implement fail-closed export scan**

Create `scan_public_text(label: str, text: str) -> list[str]` using named patterns and return actionable findings. `prepare_submission` must abort on any finding before writing the staged package.

- [ ] **Step 6: Declare staging artifacts**

Add to `helper/artifacts.json`:

```json
"build/community-demo.json": {
  "producer": "parent:share-demo",
  "consumers": ["community-publisher"],
  "blocking": true
},
"build/community-demo-package": {
  "producer": "parent:share-demo",
  "consumers": ["community-publisher"],
  "blocking": true
}
```

- [ ] **Step 7: Run GREEN**

Run: `python3 -m unittest tests.test_demo_submit -v`
Expected: PASS.

- [ ] **Step 8: Commit**

Commit message: `feat: add verified demo submission preflight`

---

### Task 3: Share-demo route, skill, and publisher agent

**Files:**
- Create: `skills/share-demo/SKILL.md`
- Create: `agents/community-publisher.md`
- Modify: `helper/router.json`
- Modify: `architecture/plugin-graph.json`
- Modify: `helper/modules.json`
- Modify: `helper/GUIDE.md`
- Test: `tests/test_demo_publisher_contract.py`
- Test: existing `tests/test_skill_contracts.py`, `tests/test_agent_contracts.py`, `tests/test_plugin_graph.py`, `tests/test_ecosystem_doctor.py`

**Interfaces:**
- Route: `share-demo` -> workflow `share-demo`, skill `share-demo`, agent `community-publisher`.
- Agent input: validated contribution directory + author + slug + upstream repository.
- Agent output: PR URL or a precise HOLD with prepared local package/manual commands.

- [ ] **Step 1: Write failing routing and safety tests**

```python
def test_share_demo_is_a_focused_route(self):
    route = self.router["routes"]["share-demo"]
    self.assertEqual("share-demo", route["workflow"])
    self.assertEqual(["share-demo"], route["skills"])
    self.assertEqual(["community-publisher"], route["agents"])

def test_publisher_contract_forbids_merge_and_upstream_main_push(self):
    text = (ROOT / "agents/community-publisher.md").read_text()
    self.assertIn("Never merge", text)
    self.assertIn("Never push directly to upstream `main`", text)
    self.assertIn("manual review", text.lower())
```

- [ ] **Step 2: Run RED**

Run: `python3 -m unittest tests.test_demo_publisher_contract -v`
Expected: FAIL for missing route, skill, and agent.

- [ ] **Step 3: Add `share-demo` route**

```json
"share-demo": {
  "workflow": "share-demo",
  "skills": ["share-demo"],
  "agents": ["community-publisher"],
  "capabilities": ["verification-loop"]
}
```

Do not add `community-publisher` to the `new-post` critical sequence.

- [ ] **Step 4: Write focused skill contract**

`skills/share-demo/SKILL.md` must use the same v3 sections as every public skill and explicitly enforce: opt-in, PASS-only, rights confirmation, metadata collection, source-prompt opt-in, `demo_submit.py prepare/check`, `demo_gallery.py check`, delegation to `community-publisher`, and HOLD on unavailable GitHub write access.

- [ ] **Step 5: Write publisher agent contract**

The agent must use host-native GitHub tooling to: resolve authenticated user; verify upstream exact repository; create/reuse fork; create fresh branch `community/<user>/<slug>`; add the three demo files plus root `demos/catalog.json`; commit; push to contributor fork; open PR to upstream `main`; stop. It must explicitly forbid merge, auto-merge, upstream-main push, force-push, unrelated file changes, and success claims without returned PR URL.

- [ ] **Step 6: Register real modules**

Add `share-demo` under skills, `community-publisher` under agents, and `demo_gallery`/`demo_submit` under tools in `helper/modules.json`, each with real test paths and reachable-from references that contain the module names.

- [ ] **Step 7: Register graph preload**

Add:

```json
"community-publisher": {"required_skills": ["share-demo"]}
```

No new-post sequence edge is added.

- [ ] **Step 8: Run contract GREEN**

Run: `python3 -m unittest tests.test_demo_publisher_contract tests.test_skill_contracts tests.test_agent_contracts tests.test_plugin_graph tests.test_ecosystem_doctor -v`
Expected: PASS.

- [ ] **Step 9: Commit**

Commit message: `feat: wire opt-in community demo publishing`

---

### Task 4: Post-delivery offer and no-write-before-consent invariant

**Files:**
- Modify: `skills/new-post/SKILL.md`
- Modify: `helper/GUIDE.md`
- Test: `tests/test_demo_publisher_contract.py`

**Interfaces:**
- `new-post` final stage offers sharing only after delivery + `story-verifier` PASS.
- The user response `yes` transfers control to focused `share-demo`; every other response ends without GitHub write.

- [ ] **Step 1: Write failing ordering tests**

```python
def test_new_post_offers_sharing_only_after_verification_pass(self):
    text = (ROOT / "skills/new-post/SKILL.md").read_text()
    verify = text.index("Independent acceptance")
    deliver = text.index("Deliver")
    share = text.index("Share with the community")
    self.assertLess(verify, deliver)
    self.assertLess(deliver, share)
    self.assertIn("only when the final verification verdict is `PASS`", text)
```

- [ ] **Step 2: Run RED**

Run: `python3 -m unittest tests.test_demo_publisher_contract -v`
Expected: FAIL because the offer does not exist.

- [ ] **Step 3: Add stage 17 to `new-post`**

Add `### 17. Share with the community (optional)` after Deliver. It must ask one concise opt-in question only on PASS, route acceptance to `share-demo`, and state that declining or no answer causes no GitHub write.

- [ ] **Step 4: Add helper HOLD semantics**

Document `share-demo` as an export boundary and list missing verification PASS, rights confirmation, GitHub identity/auth, GIF, or HTML as HOLD causes.

- [ ] **Step 5: Run GREEN**

Run: `python3 -m unittest tests.test_demo_publisher_contract tests.test_skill_contracts -v`
Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `feat: offer community sharing after verified delivery`

---

### Task 5: Gallery documentation and root README integration

**Files:**
- Create: `demos/README.md`
- Create: `docs/community-demos.md`
- Modify: `README.md`
- Modify: `docs/ecosystem.md`
- Modify: `docs/routing.md`
- Modify: `docs/agents.md`
- Modify: `docs/skills.md`
- Modify: `docs/development.md`
- Test: `tests/test_docs_contract.py`
- Test: `tests/test_demo_publisher_contract.py`

**Interfaces:**
- Root README links to `demos/README.md` and `docs/community-demos.md` without becoming the full contribution manual.
- `demos/README.md` separates `Created by Mamdouh` and `Created by the community` and explains the three-file contract.

- [ ] **Step 1: Add failing docs contract**

Extend docs tests to require both new docs and root README links. Assert the phrases `Created by Mamdouh`, `Created by the community`, `GIF + HTML + demo.json`, and `manual review` exist in `demos/README.md`.

- [ ] **Step 2: Run RED**

Run: `python3 -m unittest tests.test_docs_contract tests.test_demo_publisher_contract -v`
Expected: FAIL because gallery docs are absent.

- [ ] **Step 3: Write concise gallery docs**

`demos/README.md` explains browsing, attribution, paths, contract, manual contribution, agent-assisted publication, and manual merge policy. `docs/community-demos.md` documents metadata fields, consent/privacy boundary, validation commands, PR policy, and HOLD states.

- [ ] **Step 4: Update public ecosystem docs**

Add only focused references to the new route/skill/agent/tooling. Preserve existing helper/research authority statements.

- [ ] **Step 5: Run GREEN**

Run: `python3 -m unittest tests.test_docs_contract tests.test_demo_publisher_contract -v`
Expected: PASS including local Markdown link resolution.

- [ ] **Step 6: Commit**

Commit message: `docs: add owned and community demo gallery`

---

### Task 6: CI, strict doctor, and release 3.1.0

**Files:**
- Modify: `.github/workflows/claude-plugin-validation.yml`
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `scripts/validate_marketplace.py`
- Modify: `tests/test_marketplace.py`
- Modify: `README.md`
- Test: all tests

**Interfaces:**
- CI commands additionally include `python3 -m json.tool schemas/demo.schema.json` and `python3 scripts/demo_gallery.py check`.
- Release version is exactly `3.1.0` in plugin manifest, marketplace entry, validator expectations, tests, and README badge/text where version is explicit.

- [ ] **Step 1: Write failing marketplace version assertion**

Update the exact test to expect `3.1.0` while manifests are still `3.0.0`.

- [ ] **Step 2: Run RED**

Run: `python3 -m unittest tests.test_marketplace -v`
Expected: FAIL showing current `3.0.0`.

- [ ] **Step 3: Bump manifests and validator to `3.1.0`**

Update both `.claude-plugin` JSON files, exact validator assertion, and root README release text. Do not rename marketplace/plugin IDs.

- [ ] **Step 4: Add CI demo gates**

Insert after strict ecosystem doctor:

```yaml
- name: Validate demo gallery
  run: python3 scripts/demo_gallery.py check
```

Add `python3 -m json.tool schemas/demo.schema.json >/dev/null` to JSON validation.

- [ ] **Step 5: Run local full gate**

Run:

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
python3 -m json.tool schemas/demo.schema.json >/dev/null
```

Expected: all PASS; only the existing four intentional upstream-research skips remain.

- [ ] **Step 6: Commit**

Commit message: `release: ship community demo gallery 3.1.0`

---

### Task 7: PR review, GitHub validation, and merge gate

**Files:**
- No product file changes unless review finds a defect.

**Interfaces:**
- Feature branch -> PR against `main` -> full GitHub Actions -> external review -> manual squash merge only after clean head.

- [ ] **Step 1: Open a PR from `feat/community-demo-publisher-v3` to `main`**

PR body must summarize gallery contract, privacy boundary, opt-in flow, manual-review rule, 3.1.0 version bump, and exact validation results.

- [ ] **Step 2: Verify GitHub Actions on the exact head SHA**

Require successful `Claude Plugin Validation`, including official `claude plugin validate .` and same-repository marketplace install smoke.

- [ ] **Step 3: Review external feedback**

Inspect Qlty, CodeRabbit status, Qodo/review threads, and any security-sensitive finding. Fix real defects with tests before resolving threads. Do not claim a full CodeRabbit review if it is rate-limited.

- [ ] **Step 4: Security review the export boundary**

Re-check secret/path scanning, exact three-file package, rights/source-prompt consent, no direct upstream-main behavior, no auto-merge behavior, and safe catalog generation.

- [ ] **Step 5: Merge with exact head SHA**

Use squash merge with GitHub's expected-head protection. Abort if the head moved or any blocking check/review appeared.

- [ ] **Step 6: Verify `main` contents**

Fetch `.claude-plugin/plugin.json`, `demos/README.md`, `schemas/demo.schema.json`, `skills/share-demo/SKILL.md`, and `agents/community-publisher.md` from default branch and confirm version `3.1.0` plus the manual-review publisher contract.
