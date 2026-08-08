import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTOPILOT = ROOT / "openai-skills" / "linkedin-infographic-autopilot"
AGENT_DIR = ROOT / ".codex" / "agents"
CONFIG = ROOT / ".codex" / "config.toml"

EXPECTED_AGENTS = {
    "creative_director": "read-only",
    "evidence_researcher": "read-only",
    "copy_director": "read-only",
    "layout_composer": "workspace-write",
    "still_critic": "read-only",
    "motion_director": "workspace-write",
    "render_qa": "read-only",
    "final_verifier": "read-only",
    "tool_runner": "workspace-write",
}


class WorkspaceAgentBridgeTests(unittest.TestCase):
    def test_workspace_agents_bridge_is_optional_and_honest(self):
        text = (AUTOPILOT / "references" / "workspace-agents-bridge.md").read_text()
        for marker in (
            "optional",
            "not automatically registered",
            "observed",
            "Codex subagents",
            "sequential",
        ):
            self.assertIn(marker, text)

    def test_real_project_scoped_codex_roles_exist_with_narrow_sandboxes(self):
        for name, expected_sandbox in EXPECTED_AGENTS.items():
            path = AGENT_DIR / f"{name}.toml"
            self.assertTrue(path.is_file(), name)
            data = tomllib.loads(path.read_text())
            self.assertEqual(name, data["name"])
            self.assertEqual(expected_sandbox, data["sandbox_mode"])
            self.assertTrue(data["description"])
            self.assertTrue(data["developer_instructions"])

    def test_codex_config_registers_real_roles_and_preserves_concurrency(self):
        data = tomllib.loads(CONFIG.read_text())
        agents = data["agents"]
        self.assertTrue(agents["enabled"])
        self.assertEqual(6, agents["max_concurrent_threads_per_session"])
        for name in EXPECTED_AGENTS:
            self.assertIn(name, agents)
            self.assertEqual(f"agents/{name}.toml", agents[name]["config_file"])
            self.assertTrue(agents[name]["description"])


if __name__ == "__main__":
    unittest.main()
