import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "openai-skills" / "linkedin-infographic-autopilot" / "scripts" / "autopilot_runtime.py"


def load_runtime():
    spec = importlib.util.spec_from_file_location("openai_autopilot_runtime", RUNTIME)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OpenAIAutopilotRuntimeHelperTests(unittest.TestCase):
    def test_selects_full_autopilot_only_with_observed_delegation_and_execution(self):
        mod = load_runtime()
        capabilities = mod.normalize_capabilities({
            "subagents": True,
            "sandbox_write": True,
            "shell_or_code_execution": True,
            "image_inspection": True,
        })
        self.assertEqual("full-autopilot", mod.select_execution_path(capabilities))

        without_delegation = dict(capabilities, subagents=False)
        self.assertEqual("tool-rich-sequential", mod.select_execution_path(without_delegation))

    def test_unknown_capabilities_fail_closed(self):
        mod = load_runtime()
        capabilities = mod.normalize_capabilities({"subagents": "unknown", "sandbox_write": None})
        self.assertFalse(capabilities["subagents"])
        self.assertFalse(capabilities["sandbox_write"])
        self.assertEqual("safe-skill-only", mod.select_execution_path(capabilities))

    def test_tool_rich_path_accepts_useful_observed_tools_without_subagents(self):
        mod = load_runtime()
        capabilities = mod.normalize_capabilities({"web_research": True, "image_inspection": True})
        self.assertEqual("tool-rich-sequential", mod.select_execution_path(capabilities))

    def test_dispatch_plan_finishes_evidence_before_parallel_creative_discovery(self):
        mod = load_runtime()
        full = mod.build_dispatch_plan(mod.normalize_capabilities({"subagents": True, "sandbox_write": True}))
        self.assertEqual(["evidence-research"], full["evidence_jobs"])
        self.assertTrue(full["must_finish_evidence_before_discovery"])
        self.assertEqual("parallel", full["discovery_mode"])
        self.assertEqual(
            [
                "creative-direction-exploration",
                "visual-archetype-exploration",
                "copy-compression-critique",
            ],
            full["discovery_jobs"],
        )
        self.assertEqual(
            ["still-critique", "render-qa", "final-verification"],
            full["dependency_bound_jobs"],
        )

        sequential = mod.build_dispatch_plan(mod.normalize_capabilities({"subagents": False, "sandbox_write": True}))
        self.assertEqual("sequential", sequential["discovery_mode"])
        self.assertEqual(["evidence-research"], sequential["evidence_jobs"])
        self.assertTrue(sequential["must_finish_evidence_before_discovery"])

    def test_workspace_scaffold_creates_directories_but_not_fake_delivery_artifacts(self):
        mod = load_runtime()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "work"
            created = mod.create_workspace(root)
            for directory in mod.WORKSPACE_DIRECTORIES:
                self.assertTrue((root / directory).is_dir(), directory)
            self.assertEqual(sorted(mod.WORKSPACE_DIRECTORIES), sorted(created))
            for relative in mod.LOGICAL_ARTIFACTS:
                self.assertFalse((root / relative).exists(), f"fabricated artifact: {relative}")


if __name__ == "__main__":
    unittest.main()
