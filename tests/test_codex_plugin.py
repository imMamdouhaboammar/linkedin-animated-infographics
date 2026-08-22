import importlib.util
import json
import shutil
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX_PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
CLAUDE_AGENT = ROOT / "agents" / "artboard-builder.md"
COMPATIBILITY = ROOT / "compatibility" / "codex.json"
VALIDATOR = ROOT / "scripts" / "validate_codex_plugin.py"
CODEX_CONFIG = ROOT / ".codex" / "config.toml"
CODEX_AGENT_DIR = ROOT / ".codex" / "agents"
OPENAI_SKILL = ROOT / "openai-skills" / "linkedin-infographic-studio"
OPENAI_AUTOPILOT = ROOT / "openai-skills" / "linkedin-infographic-autopilot"
SELECTION_FIXTURE = ROOT / "tests" / "fixtures" / "openai-selection-parity.json"
EXPECTED_CODEX_AGENTS = {
    "explorer": "read-only",
    "reviewer": "read-only",
    "docs_researcher": "read-only",
}
EXPECTED_VERSION = "3.7.0"


def load_validator():
    if not VALIDATOR.exists():
        return None
    spec = importlib.util.spec_from_file_location("validate_codex_plugin", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_fixture(root: Path):
    for relative in (
        ".claude-plugin",
        ".codex-plugin",
        ".agents",
        ".codex",
        "skills",
        "openai-skills",
        "agents",
        "helper",
        "architecture",
        "research",
        "compatibility",
        "submission",
        "assets",
    ):
        source = ROOT / relative
        if source.exists():
            shutil.copytree(source, root / relative)
    for relative in ("PRIVACY.md", "TERMS.md", "SUPPORT.md"):
        source = ROOT / relative
        if source.exists():
            shutil.copy2(source, root / relative)


class CodexPluginPackagingTests(unittest.TestCase):
    def test_openai_plugin_manifest_uses_isolated_skills(self):
        self.assertTrue(CODEX_PLUGIN.exists(), "missing .codex-plugin/plugin.json")
        data = json.loads(CODEX_PLUGIN.read_text())
        self.assertEqual("linkedin-animated-infographics", data["name"])
        self.assertEqual(EXPECTED_VERSION, data["version"])
        self.assertEqual("./openai-skills/", data["skills"])
        self.assertTrue(OPENAI_SKILL.is_dir())
        self.assertEqual("Mamdouh Aboammar", data["author"]["name"])
        self.assertEqual(
            "https://github.com/imMamdouhaboammar/linkedin-animated-infographics",
            data["repository"],
        )

    def test_openai_plugin_manifest_is_directory_compliant(self):
        interface = json.loads(CODEX_PLUGIN.read_text())["interface"]
        for field in (
            "displayName",
            "shortDescription",
            "longDescription",
            "developerName",
            "category",
            "capabilities",
            "websiteURL",
            "privacyPolicyURL",
            "termsOfServiceURL",
            "defaultPrompt",
            "composerIcon",
            "logo",
        ):
            self.assertTrue(interface.get(field), field)
        self.assertEqual("Productivity", interface["category"])
        self.assertLessEqual(len(interface["defaultPrompt"]), 3)
        self.assertGreaterEqual(len(interface["defaultPrompt"]), 1)
        self.assertNotIn("screenshots", interface)
        self.assertEqual("./assets/plugin-icon.svg", interface["composerIcon"])
        self.assertEqual("./assets/plugin-icon.svg", interface["logo"])

    def test_openai_studio_is_self_contained(self):
        self.assertTrue((OPENAI_SKILL / "SKILL.md").is_file())
        text = "\n".join(path.read_text() for path in OPENAI_SKILL.rglob("*.md"))
        for forbidden in (
            ".claude-plugin/",
            "agents/",
            "${CLAUDE_PLUGIN_ROOT}",
            "helper/",
            "architecture/",
        ):
            self.assertNotIn(forbidden, text)

    def test_openai_visual_contract_has_blocking_layout_gates(self):
        path = OPENAI_SKILL / "references" / "visual-quality-contract.md"
        text = path.read_text()
        for marker in (
            "82-92%",
            "120px",
            "Maximum bordered containment depth is two levels",
            "top-heavy-composition",
            "bottom-dead-zone",
            "nested-card-density",
            "generic-ui-grammar",
            "weak-macro-rhythm",
            "weak-visual-anchor",
            "footer-detachment",
            "motion-on-weak-still",
            "decorative-motion",
            "feed-scale-legibility",
            "Maximum two targeted repair attempts",
            "unverified-identity-asset",
            "remote-font-dependency",
            "generic-card-first-structure",
        ):
            self.assertIn(marker, text)
        skill = (OPENAI_SKILL / "SKILL.md").read_text()
        self.assertIn("Do not proceed to motion while a blocking still defect remains", skill)

    def test_repo_marketplace_exposes_root_plugin(self):
        self.assertTrue(CODEX_MARKETPLACE.exists(), "missing .agents/plugins/marketplace.json")
        data = json.loads(CODEX_MARKETPLACE.read_text())
        self.assertEqual("mamdouh-creative-tools", data["name"])
        self.assertEqual("Mamdouh Creative Tools", data["interface"]["displayName"])
        self.assertEqual(1, len(data["plugins"]))
        entry = data["plugins"][0]
        self.assertEqual("linkedin-animated-infographics", entry["name"])
        self.assertEqual({"source": "local", "path": "./"}, entry["source"])
        self.assertEqual("AVAILABLE", entry["policy"]["installation"])
        self.assertEqual("ON_INSTALL", entry["policy"]["authentication"])
        self.assertEqual("Productivity", entry["category"])

    def test_claude_execution_contract_remains_present(self):
        codex = json.loads(CODEX_PLUGIN.read_text())
        claude = json.loads(CLAUDE_PLUGIN.read_text())
        self.assertEqual(claude["name"], codex["name"])
        self.assertEqual(EXPECTED_VERSION, claude["version"])
        self.assertTrue(CLAUDE_AGENT.is_file())
        text = CLAUDE_AGENT.read_text()
        self.assertIn("model: opus", text)
        self.assertIn("artboard", text)
        self.assertIn("info-stories", text)


class CodexPluginParityTests(unittest.TestCase):
    def require_validator(self):
        module = load_validator()
        self.assertIsNotNone(module, "missing scripts/validate_codex_plugin.py")
        return module

    def test_compatibility_registry_declares_host_specific_distributions(self):
        self.assertTrue(COMPATIBILITY.exists(), "missing compatibility/codex.json")
        data = json.loads(COMPATIBILITY.read_text())
        self.assertEqual(EXPECTED_VERSION, data["plugin_version"])
        self.assertEqual("skills", data["canonical"]["skills_root"])
        self.assertEqual("skills", data["distributions"]["claude"]["skills_root"])
        self.assertEqual("openai-skills", data["distributions"]["openai"]["skills_root"])
        self.assertEqual("skills", data["distributions"]["openai"]["package_skills_root"])
        self.assertEqual("native-worker-graph", data["distributions"]["claude"]["execution"])
        self.assertEqual("capability-negotiated-autopilot", data["distributions"]["openai"]["execution"])
        self.assertEqual("helper/router.json", data["canonical"]["router"])
        self.assertEqual("architecture/plugin-graph.json", data["canonical"]["worker_graph"])
        self.assertEqual("skills-only", data["public_submission"]["type"])
        self.assertEqual("openai-skills", data["public_submission"]["skills_root"])
        self.assertEqual("skills", data["public_submission"]["package_skills_root"])
        self.assertIn("codex", data["surfaces"])
        self.assertIn("chatgpt", data["surfaces"])
        self.assertIn("verified-identity-source-before-concept", data["parity_invariants"])
        self.assertIn("intentional-render-safe-typography", data["parity_invariants"])
        self.assertIn("canonical-public-skills-layout", data["parity_invariants"])
        self.assertIn("host-workspace-operator-packaged", data["parity_invariants"])
        self.assertIn("sandbox-python-executor-packaged", data["parity_invariants"])
        self.assertEqual(
            "skills/info-stories/extensions/idea-mechanisms.json",
            data["canonical"]["visual_mechanisms"],
        )
        self.assertEqual(
            "research/reference-studies/visual-library.json",
            data["canonical"]["reference_library"],
        )
        openai = data["distributions"]["openai"]
        self.assertEqual("generated-compact-capsule", openai["reference_context"])
        self.assertFalse(openai["persistent_reference_ingestion"])
        self.assertEqual(2, len(openai["visual_intelligence_capsules"]))
        for invariant in (
            "canonical-reference-capsule-digest",
            "deterministic-reference-selection",
            "no-source-reference-media-export",
        ):
            self.assertIn(invariant, data["parity_invariants"])

    def test_validator_reports_clean_repository(self):
        module = self.require_validator()
        self.assertEqual([], module.validate_codex_plugin(ROOT))

    def test_validator_rejects_version_drift(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / ".codex-plugin" / "plugin.json"
            data = json.loads(path.read_text())
            data["version"] = "9.9.9"
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("version" in error.lower() and "drift" in error.lower() for error in errors), errors)

    def test_validator_rejects_skills_path_escape(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / ".codex-plugin" / "plugin.json"
            data = json.loads(path.read_text())
            data["skills"] = "../outside-skills"
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("unsafe" in error.lower() and "skills" in error.lower() for error in errors), errors)

    def test_validator_rejects_four_default_prompts(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / ".codex-plugin" / "plugin.json"
            data = json.loads(path.read_text())
            data["interface"]["defaultPrompt"].append("Fourth prompt")
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("one to three" in error.lower() for error in errors), errors)

    def test_validator_rejects_screenshots_field(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / ".codex-plugin" / "plugin.json"
            data = json.loads(path.read_text())
            data["interface"]["screenshots"] = ["./assets/demo.gif"]
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("must not declare screenshots" in error.lower() for error in errors), errors)

    def test_validator_rejects_unavailable_openai_runtime_reference(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / "openai-skills" / "linkedin-infographic-studio" / "SKILL.md"
            path.write_text(path.read_text() + "\nRead agents/artboard-builder.md\n")
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("unavailable runtime reference" in error.lower() for error in errors), errors)

    def test_validator_rejects_missing_visual_gate(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / "openai-skills" / "linkedin-infographic-studio" / "references" / "visual-quality-contract.md"
            path.write_text(path.read_text().replace("bottom-dead-zone", "bottom-gap"))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("missing marker: bottom-dead-zone" in error.lower() for error in errors), errors)

    def test_validator_rejects_marketplace_policy_drift(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / ".agents" / "plugins" / "marketplace.json"
            data = json.loads(path.read_text())
            data["plugins"][0]["policy"]["installation"] = "INSTALLED_BY_DEFAULT"
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("marketplace" in error.lower() and "installation" in error.lower() for error in errors), errors)

    def test_validator_rejects_compatibility_path_drift(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / "compatibility" / "codex.json"
            data = json.loads(path.read_text())
            data["canonical"]["router"] = "helper/not-real.json"
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("compatibility" in error.lower() and "router" in error.lower() for error in errors), errors)

    def test_generated_visual_capsules_are_identical_exact_and_compact(self):
        module = self.require_validator()
        expected = module.serialize_openai_visual_capsule(module.build_openai_visual_capsule(ROOT))
        paths = (
            OPENAI_SKILL / "references" / "visual-intelligence-capsule.json",
            OPENAI_AUTOPILOT / "references" / "visual-intelligence-capsule.json",
        )
        payloads = [path.read_bytes() for path in paths]
        self.assertEqual(payloads[0], payloads[1])
        self.assertEqual(expected, payloads[0])
        self.assertLessEqual(len(payloads[0]), module.OPENAI_VISUAL_CAPSULE_MAX_BYTES)

    def test_validator_rejects_canonical_source_mutation_as_capsule_drift(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / "skills" / "info-stories" / "extensions" / "idea-mechanisms.json"
            data = json.loads(path.read_text())
            data["mechanisms"][0]["hook"] += " Changed."
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("visual intelligence capsule drift" in error.lower() for error in errors), errors)

    def test_validator_rejects_capsule_mutation_even_with_fresh_digest(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / "openai-skills" / "linkedin-infographic-studio" / "references" / "visual-intelligence-capsule.json"
            data = json.loads(path.read_text())
            data["guidance"][0]["hook"] += " Mutated."
            data["canonical_sha256"] = module.canonical_visual_sources_sha256(root)
            path.write_text(json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n")
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("visual intelligence capsule drift" in error.lower() for error in errors), errors)

    def test_openai_selection_matches_canonical_ranking_and_reference_roles(self):
        module = self.require_validator()
        from scripts.info_stories import build_context_capsule, load_catalog, rank_mechanisms

        capsule = module.build_openai_visual_capsule(ROOT)
        catalog = load_catalog()
        fixture = json.loads(SELECTION_FIXTURE.read_text())
        for case in fixture["cases"]:
            with self.subTest(case=case["id"]):
                canonical = rank_mechanisms(catalog, case["query"])
                openai = module.rank_openai_visual_capsule(capsule, case["query"])
                self.assertEqual(case["expected_ranked"], openai)
                self.assertEqual(canonical, openai)
                context = build_context_capsule(catalog, canonical, "review", 100000)
                self.assertEqual(case["expected_references"], context["references"])
                self.assertEqual(
                    context["references"],
                    module.selected_openai_references(capsule, openai),
                )

    def test_capsule_excludes_source_media_and_private_paths(self):
        module = self.require_validator()
        text = module.serialize_openai_visual_capsule(module.build_openai_visual_capsule(ROOT)).decode()
        for forbidden in (
            "source_filename", "asset_path", "frame_paths", "contact-sheet",
            "contact_sheet", ".gif", ".png", "/Users/", "C:\\Users\\",
        ):
            self.assertNotIn(forbidden, text)


class CodexRepositoryAgentTests(unittest.TestCase):
    def require_validator(self):
        module = load_validator()
        self.assertIsNotNone(module, "missing scripts/validate_codex_plugin.py")
        return module

    def test_codex_config_uses_current_subagent_controls(self):
        data = tomllib.loads(CODEX_CONFIG.read_text())
        agents = data.get("agents", {})
        self.assertIs(True, agents.get("enabled"))
        self.assertEqual(6, agents.get("max_concurrent_threads_per_session"))
        self.assertNotIn("max_threads", agents)

    def test_project_scoped_codex_agents_are_real_and_narrow(self):
        self.assertTrue(CODEX_AGENT_DIR.is_dir(), "missing .codex/agents")
        for filename, expected_sandbox in EXPECTED_CODEX_AGENTS.items():
            path = CODEX_AGENT_DIR / f"{filename}.toml"
            self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")
            data = tomllib.loads(path.read_text())
            self.assertEqual(filename, data.get("name"))
            self.assertTrue(data.get("description"))
            self.assertTrue(data.get("developer_instructions"))
            self.assertEqual(expected_sandbox, data.get("sandbox_mode"))

    def test_installed_plugin_does_not_depend_on_repo_codex_config(self):
        manifest = json.loads(CODEX_PLUGIN.read_text())
        text = json.dumps(manifest)
        self.assertNotIn(".codex/config.toml", text)
        self.assertNotIn(".codex/agents", text)

    def test_validator_rejects_explicit_dead_agent_config_reference(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            config_path = root / ".codex" / "config.toml"
            config_path.write_text(
                config_path.read_text()
                + '\n[agents.broken]\ndescription = "broken fixture"\nconfig_file = "agents/not-real.toml"\n'
            )
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("agent config" in error.lower() and "not-real.toml" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
