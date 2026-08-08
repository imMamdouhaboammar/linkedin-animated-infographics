import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX_AGENT_DIR = ROOT / ".codex" / "agents"

CANONICAL_ADAPTERS = {
    "creative_director": "agents/creative-director.md",
    "evidence_researcher": "agents/evidence-checker.md",
    "copy_director": "agents/copy-compressor.md",
    "layout_composer": "agents/layout-composer.md",
    "still_critic": "agents/post-critic.md",
    "motion_director": "agents/motion-director.md",
    "render_qa": "agents/render-qa.md",
    "final_verifier": "agents/story-verifier.md",
}


class CodexProductAgentAdapterTests(unittest.TestCase):
    def test_product_subagents_are_explicit_adapters_to_canonical_workers(self):
        for name, canonical in CANONICAL_ADAPTERS.items():
            canonical_path = ROOT / canonical
            self.assertTrue(canonical_path.is_file(), canonical)
            data = tomllib.loads((CODEX_AGENT_DIR / f"{name}.toml").read_text())
            instructions = data["developer_instructions"]
            self.assertIn("helper/GUIDE.md", instructions, name)
            self.assertIn("architecture/plugin-graph.json", instructions, name)
            self.assertIn(canonical, instructions, name)
            self.assertIn("canonical", instructions.lower(), name)
            self.assertIn("adapter", instructions.lower(), name)

    def test_tool_runner_requires_parent_supplied_canonical_worker_contract(self):
        data = tomllib.loads((CODEX_AGENT_DIR / "tool_runner.toml").read_text())
        instructions = data["developer_instructions"]
        self.assertIn("helper/GUIDE.md", instructions)
        self.assertIn("architecture/plugin-graph.json", instructions)
        self.assertIn("canonical worker contract", instructions.lower())
        self.assertIn("supplied by the parent", instructions.lower())

    def test_codex_repository_guide_allows_only_maintenance_roles_or_canonical_adapters(self):
        text = (ROOT / ".codex" / "AGENTS.md").read_text()
        self.assertIn("canonical product-worker adapters", text)
        self.assertIn("must read the mapped `agents/*.md` contract", text)
        self.assertIn("must not create a parallel product orchestration model", text)


if __name__ == "__main__":
    unittest.main()
