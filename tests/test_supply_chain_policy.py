import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATION_WORKFLOW = ROOT / ".github" / "workflows" / "claude-plugin-validation.yml"
SECURITY_WORKFLOW = ROOT / ".github" / "workflows" / "security.yml"
DEPENDABOT = ROOT / ".github" / "dependabot.yml"
RUNTIME_REQUIREMENTS = ROOT / "requirements-runtime.txt"
SECURITY_REQUIREMENTS = ROOT / "requirements-security.txt"
SETUP = ROOT / "scripts" / "setup.sh"


class SupplyChainPolicyTests(unittest.TestCase):
    def test_runtime_dependencies_are_exactly_pinned(self):
        dependencies = [
            line.strip()
            for line in RUNTIME_REQUIREMENTS.read_text().splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertEqual(["Pillow==12.3.0", "playwright==1.61.0"], dependencies)
        self.assertTrue(all("==" in dependency for dependency in dependencies))

    def test_security_tooling_is_exactly_pinned(self):
        dependencies = [
            line.strip()
            for line in SECURITY_REQUIREMENTS.read_text().splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertEqual(["pip-audit==2.10.1"], dependencies)

    def test_setup_and_ci_install_from_the_same_runtime_lock(self):
        setup = SETUP.read_text()
        workflow = VALIDATION_WORKFLOW.read_text()
        self.assertIn("requirements-runtime.txt", setup)
        self.assertIn('-r "$RUNTIME_REQUIREMENTS"', setup)
        self.assertIn("-r requirements-runtime.txt", workflow)
        self.assertIn("python3 -m pip check", workflow)
        self.assertIn("runs-on: ubuntu-24.04", workflow)
        self.assertIn("sudo apt-get install -y ffmpeg", workflow)
        self.assertNotIn("pip install Pillow playwright", workflow)
        self.assertNotIn("@latest", workflow)

    def test_security_workflow_audits_dependencies_and_pins_actions(self):
        workflow = SECURITY_WORKFLOW.read_text()
        self.assertIn("-r requirements-security.txt", workflow)
        self.assertIn("python3 -m pip_audit -r requirements-runtime.txt", workflow)
        self.assertIn("queries: security-extended", workflow)
        self.assertEqual(2, workflow.count("runs-on: ubuntu-24.04"))
        action_refs = re.findall(r"uses:\s+[^@\s]+@([^\s]+)", workflow)
        self.assertGreaterEqual(len(action_refs), 5)
        for ref in action_refs:
            self.assertRegex(ref, r"^[0-9a-f]{40}$", ref)

    def test_dependabot_maintains_runtime_and_action_dependencies(self):
        text = DEPENDABOT.read_text()
        self.assertIn('package-ecosystem: "pip"', text)
        self.assertIn('package-ecosystem: "github-actions"', text)
        self.assertIn('target-branch: "main"', text)


if __name__ == "__main__":
    unittest.main()
