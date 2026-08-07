import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "claude-plugin-validation.yml"


class DualHostCIContractTests(unittest.TestCase):
    def test_workflow_is_host_neutral_and_runs_codex_validator(self):
        text = WORKFLOW.read_text()
        self.assertIn("name: Plugin Validation", text)
        self.assertIn("python3 scripts/validate_codex_plugin.py", text)
        self.assertIn("Validate Codex and OpenAI plugin contract", text)

    def test_workflow_parses_all_openai_contract_json(self):
        text = WORKFLOW.read_text()
        for relative in (
            ".codex-plugin/plugin.json",
            ".agents/plugins/marketplace.json",
            "compatibility/codex.json",
            "submission/openai-plugin.json",
            "submission/test-cases.json",
        ):
            self.assertIn(f"python3 -m json.tool {relative}", text, relative)

    def test_existing_claude_validation_and_smoke_remain_required(self):
        text = WORKFLOW.read_text()
        self.assertIn("claude plugin validate .", text)
        self.assertIn("claude plugin marketplace add ./ --scope user", text)
        self.assertIn("claude plugin install linkedin-animated-infographics@mamdouh-creative-tools", text)

    def test_ci_does_not_invent_codex_install_command(self):
        text = WORKFLOW.read_text()
        self.assertNotIn("codex plugin install", text)


if __name__ == "__main__":
    unittest.main()
