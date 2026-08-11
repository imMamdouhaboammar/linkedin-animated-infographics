import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_codex_plugin.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_codex_plugin_release", VALIDATOR)
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
        "agents",
        "assets",
        "helper",
        "architecture",
        "research",
        "compatibility",
        "submission",
    ):
        source = ROOT / relative
        if source.exists():
            shutil.copytree(source, root / relative)
    for relative in ("PRIVACY.md", "TERMS.md", "SUPPORT.md"):
        shutil.copy2(ROOT / relative, root / relative)


class CodexReleaseParityTests(unittest.TestCase):
    def test_compatibility_declares_visual_intelligence_boundary(self):
        registry = json.loads((ROOT / "compatibility" / "codex.json").read_text())
        self.assertEqual(
            "skills/info-stories/extensions/idea-mechanisms.json",
            registry["canonical"]["visual_mechanisms"],
        )
        self.assertEqual(
            "research/reference-studies/visual-library.json",
            registry["canonical"]["reference_library"],
        )
        openai = registry["distributions"]["openai"]
        self.assertEqual("generated-compact-capsule", openai["reference_context"])
        self.assertFalse(openai["persistent_reference_ingestion"])
        self.assertEqual(2, len(openai["visual_intelligence_capsules"]))
        self.assertTrue({
            "canonical-reference-capsule-digest",
            "deterministic-reference-selection",
            "no-source-reference-media-export",
        }.issubset(registry["parity_invariants"]))

    def test_validator_rejects_claude_plugin_version_drift(self):
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / ".claude-plugin" / "plugin.json"
            data = json.loads(path.read_text())
            data["version"] = "3.1.9"
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("claude" in error.lower() and "version" in error.lower() for error in errors), errors)

    def test_validator_rejects_claude_marketplace_version_drift(self):
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / ".claude-plugin" / "marketplace.json"
            data = json.loads(path.read_text())
            data["plugins"][0]["version"] = "3.1.9"
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("claude marketplace" in error.lower() and "version" in error.lower() for error in errors), errors)

    def test_validator_accepts_current_release_parity(self):
        module = load_validator()
        self.assertEqual([], module.validate_codex_plugin(ROOT))


if __name__ == "__main__":
    unittest.main()
