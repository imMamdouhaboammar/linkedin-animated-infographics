import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "post_tool_artboard_lint.py"
HOOKS = ROOT / "hooks" / "hooks.json"


def load_module():
    if not SCRIPT.exists():
        return None
    spec = importlib.util.spec_from_file_location("post_tool_artboard_lint", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CrossHostHookTests(unittest.TestCase):
    def test_hook_delegates_to_cross_host_adapter(self):
        hooks = json.loads(HOOKS.read_text())
        command = hooks["hooks"]["PostToolUse"][0]["hooks"][0]["command"]
        self.assertIn("post_tool_artboard_lint.py", command)
        self.assertIn("PLUGIN_ROOT", command)
        self.assertIn("CLAUDE_PLUGIN_ROOT", command)
        self.assertEqual("Write|Edit", hooks["hooks"]["PostToolUse"][0]["matcher"])

    def test_adapter_extracts_claude_write_file_path(self):
        module = load_module()
        self.assertIsNotNone(module, "missing scripts/post_tool_artboard_lint.py")
        payload = {"tool_input": {"file_path": "build/post.html"}}
        self.assertEqual(["build/post.html"], module.extract_html_targets(payload))

    def test_adapter_extracts_codex_apply_patch_paths(self):
        module = load_module()
        self.assertIsNotNone(module, "missing scripts/post_tool_artboard_lint.py")
        payload = {
            "tool_name": "apply_patch",
            "tool_input": {
                "command": "*** Begin Patch\n*** Update File: build/post.html\n@@\n-old\n+new\n*** End Patch"
            },
        }
        self.assertEqual(["build/post.html"], module.extract_html_targets(payload))

    def test_adapter_ignores_non_html_patch_paths(self):
        module = load_module()
        self.assertIsNotNone(module, "missing scripts/post_tool_artboard_lint.py")
        payload = {
            "tool_input": {
                "command": "*** Begin Patch\n*** Update File: README.md\n*** Add File: build/post.html\n*** End Patch"
            }
        }
        self.assertEqual(["build/post.html"], module.extract_html_targets(payload))


if __name__ == "__main__":
    unittest.main()
