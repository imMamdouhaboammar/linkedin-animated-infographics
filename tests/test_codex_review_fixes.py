import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_codex_plugin.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_codex_plugin_review", VALIDATOR)
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


class CodexReviewFixTests(unittest.TestCase):
    def test_support_security_reference_resolves(self):
        support = (ROOT / "SUPPORT.md").read_text()
        self.assertIn("SECURITY.md", support)
        security = ROOT / "SECURITY.md"
        self.assertTrue(security.is_file(), "SUPPORT.md references missing SECURITY.md")
        self.assertGreater(len(security.read_text().strip()), 200)

    def test_validator_accepts_semantically_equivalent_skills_path(self):
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / ".codex-plugin" / "plugin.json"
            data = json.loads(path.read_text())
            data["skills"] = "./openai-skills"
            path.write_text(json.dumps(data))
            self.assertEqual([], module.validate_codex_plugin(root))

    def test_validator_accepts_semantically_equivalent_marketplace_root_with_metadata(self):
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / ".agents" / "plugins" / "marketplace.json"
            data = json.loads(path.read_text())
            data["plugins"][0]["source"] = {
                "source": "local",
                "path": ".",
                "label": "repository root"
            }
            path.write_text(json.dumps(data))
            self.assertEqual([], module.validate_codex_plugin(root))


if __name__ == "__main__":
    unittest.main()
