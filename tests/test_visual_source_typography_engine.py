import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "architecture" / "plugin-graph.json"
CAPABILITIES = ROOT / "helper" / "capabilities.json"
QUALITY = ROOT / "helper" / "quality-gates.json"
ARTIFACTS = ROOT / "helper" / "artifacts.json"
ASSET_POLICY = ROOT / "skills" / "info-stories" / "references" / "asset-source-policy.md"
TYPE_POLICY = ROOT / "skills" / "info-stories" / "references" / "typography-direction.md"
ASSET_TOOL = ROOT / "tools" / "asset_policy_check.py"
TYPE_TOOL = ROOT / "tools" / "type_spec_check.py"
OPENAI_ROOT = ROOT / "openai-skills" / "linkedin-infographic-studio"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VisualSourceTypographyEngineTests(unittest.TestCase):
    def test_new_workers_have_bounded_positions(self):
        sequence = json.loads(GRAPH.read_text())["workflows"]["new-post"]["sequence"]
        self.assertLess(sequence.index("evidence-checker"), sequence.index("asset-curator"))
        self.assertLess(sequence.index("asset-curator"), sequence.index("creative-director"))
        self.assertLess(sequence.index("palette-curator"), sequence.index("type-curator"))
        self.assertLess(sequence.index("type-curator"), sequence.index("copy-compressor"))

    def test_capabilities_gates_and_artifacts_are_registered(self):
        capabilities = json.loads(CAPABILITIES.read_text())["capabilities"]
        quality = json.loads(QUALITY.read_text())["gates"]
        artifacts = json.loads(ARTIFACTS.read_text())["artifacts"]
        self.assertIn("visual-asset-sourcing", capabilities)
        self.assertIn("typography-direction", capabilities)
        for gate in ("verified-identity-assets", "intentional-typography", "clean-creative-structure"):
            self.assertIn(gate, quality)
        self.assertEqual("asset-curator", artifacts["build/asset-plan.json"]["producer"])
        self.assertEqual("type-curator", artifacts["build/type-spec.json"]["producer"])

    def test_asset_policy_is_lobe_first_and_render_safe(self):
        text = ASSET_POLICY.read_text().lower()
        self.assertIn("https://lobehub.com/icons/skill.md", text)
        self.assertIn("@lobehub/icons-static-svg", text)
        self.assertIn("@lobehub/icons-static-avatar", text)
        self.assertIn("user-supplied", text)
        self.assertIn("lobe", text)
        self.assertIn("hold", text)
        self.assertIn("local", text)
        self.assertIn("embedded", text)

    def test_typography_policy_is_intentional_and_offline_safe(self):
        text = TYPE_POLICY.read_text().lower()
        self.assertIn("build/type-spec.json", text)
        self.assertIn("user-specified", text)
        self.assertIn("system", text)
        self.assertIn("embedded", text)
        self.assertIn("local-file", text)
        self.assertIn("remote @import", text)
        self.assertIn("pairing_reason", text)

    def test_asset_validator_accepts_verified_lobe_asset_and_rejects_generated_identity(self):
        module = load_module(ASSET_TOOL, "asset_policy_check")
        valid = {
            "assets": [{
                "name": "Claude",
                "kind": "brand-logo",
                "source_type": "lobe",
                "source_ref": "@lobehub/icons-static-svg@1.91.0:claude.svg",
                "lobe_slug": "claude",
                "package": "@lobehub/icons-static-svg@1.91.0",
                "render_disposition": "local",
                "local_path": "build/assets/claude.svg",
                "identity_locked": True,
                "status": "PASS",
            }]
        }
        self.assertEqual([], module.validate(valid))
        invalid = {
            "assets": [{
                "name": "Claude",
                "kind": "brand-logo",
                "source_type": "generated",
                "source_ref": "prompt",
                "render_disposition": "remote",
                "identity_locked": False,
                "status": "PASS",
            }]
        }
        errors = module.validate(invalid)
        self.assertTrue(any("source_type" in error for error in errors), errors)
        self.assertTrue(any("render_disposition" in error for error in errors), errors)

    def test_type_validator_accepts_safe_pair_and_rejects_remote_loading(self):
        module = load_module(TYPE_TOOL, "type_spec_check")
        valid = {
            "direction_name": "technical-editorial",
            "headline_family": "JetBrains Mono",
            "body_family": "Geist Mono",
            "loading_strategy": "embedded",
            "fallbacks": ["ui-monospace", "monospace"],
            "pairing_reason": "High-contrast technical headline with quieter dense body copy.",
            "story_fit": "technical editorial",
            "render_safety": "fonts embedded before capture",
            "status": "PASS",
        }
        self.assertEqual([], module.validate(valid))
        invalid = dict(valid, loading_strategy="remote-import", render_safety="remote @import")
        errors = module.validate(invalid)
        self.assertTrue(any("loading_strategy" in error for error in errors), errors)
        self.assertTrue(any("remote" in error.lower() for error in errors), errors)

    def test_openai_distribution_has_matching_asset_and_type_passes(self):
        skill = (OPENAI_ROOT / "SKILL.md").read_text().lower()
        runtime = (OPENAI_ROOT / "references" / "openai-runtime.md").read_text().lower()
        roles = (OPENAI_ROOT / "references" / "role-passes.md").read_text().lower()
        for text in (skill, runtime, roles):
            self.assertIn("asset", text)
            self.assertIn("typ", text)
        self.assertTrue((OPENAI_ROOT / "references" / "asset-source-policy.md").exists())
        self.assertTrue((OPENAI_ROOT / "references" / "typography-direction.md").exists())
        self.assertIn("asset curator", roles)
        self.assertIn("type curator", roles)


if __name__ == "__main__":
    unittest.main()
