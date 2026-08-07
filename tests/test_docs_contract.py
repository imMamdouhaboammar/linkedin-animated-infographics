import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = {
    "ecosystem": ROOT / "docs" / "ecosystem.md",
    "routing": ROOT / "docs" / "routing.md",
    "agents": ROOT / "docs" / "agents.md",
    "skills": ROOT / "docs" / "skills.md",
    "research": ROOT / "docs" / "research.md",
    "marketplace": ROOT / "docs" / "marketplace.md",
    "development": ROOT / "docs" / "development.md",
    "community_demos": ROOT / "docs" / "community-demos.md",
}
README = ROOT / "README.md"
DEMOS_README = ROOT / "demos" / "README.md"


class DocsContractTests(unittest.TestCase):
    def test_required_v3_docs_exist(self):
        failures = [name for name, path in DOCS.items() if not path.exists()]
        if not DEMOS_README.exists():
            failures.append("demos_readme")
        self.assertEqual([], failures)

    def test_readme_is_a_concise_gateway_to_focused_docs(self):
        text = README.read_text()
        for relative in (
            "docs/ecosystem.md", "docs/routing.md", "docs/agents.md", "docs/skills.md",
            "docs/research.md", "docs/marketplace.md", "docs/development.md",
            "docs/community-demos.md", "demos/README.md",
        ):
            self.assertIn(relative, text)
        self.assertIn("helper/GUIDE.md", text)
        self.assertIn("creative-director", text)
        self.assertIn("ecosystem_doctor.py", text)

    def test_demo_gallery_readme_names_both_sections_and_contract(self):
        self.assertTrue(DEMOS_README.exists())
        text = DEMOS_README.read_text()
        for needle in (
            "Created by Mamdouh",
            "Created by the community",
            "GIF + HTML + demo.json",
            "manual review",
            "scripts/demo_gallery.py check",
        ):
            self.assertIn(needle, text)

    def test_community_demo_doc_names_export_and_pr_safety_contract(self):
        self.assertTrue(DOCS["community_demos"].exists())
        text = DOCS["community_demos"].read_text()
        for needle in (
            "rights_confirmed",
            "source_prompt",
            "verification `PASS`",
            "community-publisher",
            "Never merge",
            "demos/community/<github-user>/<slug>/",
            "python3 scripts/demo_submit.py check",
        ):
            self.assertIn(needle, text)

    def test_agent_doc_covers_every_active_agent(self):
        self.assertTrue(DOCS["agents"].exists())
        text = DOCS["agents"].read_text()
        manifest = json.loads((ROOT / "helper" / "modules.json").read_text())["modules"]["agents"]
        for name in manifest:
            self.assertIn(f"`{name}`", text, name)

    def test_skill_doc_covers_every_active_skill(self):
        self.assertTrue(DOCS["skills"].exists())
        text = DOCS["skills"].read_text()
        manifest = json.loads((ROOT / "helper" / "modules.json").read_text())["modules"]["skills"]
        for name in manifest:
            self.assertIn(f"`{name}`", text, name)

    def test_research_doc_covers_every_active_gate_and_source(self):
        self.assertTrue(DOCS["research"].exists())
        text = DOCS["research"].read_text()
        gates = json.loads((ROOT / "research" / "capability-notes" / "gates.json").read_text())["gates"]
        sources = json.loads((ROOT / "research" / "capability-notes" / "sources.json").read_text())["sources"]
        for gate_id in gates:
            self.assertIn(f"`{gate_id}`", text, gate_id)
        for source in sources:
            self.assertIn(source["name"], text, source["name"])

    def test_marketplace_doc_has_real_install_and_validation_commands(self):
        self.assertTrue(DOCS["marketplace"].exists())
        text = DOCS["marketplace"].read_text()
        for needle in (
            "/plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics",
            "/plugin install linkedin-animated-infographics@mamdouh-creative-tools",
            "claude plugin validate .",
            "python3 scripts/validate_marketplace.py",
        ):
            self.assertIn(needle, text)

    def test_development_doc_names_all_strict_validators(self):
        self.assertTrue(DOCS["development"].exists())
        text = DOCS["development"].read_text()
        for command in (
            "python3 scripts/ecosystem_router.py check",
            "python3 scripts/research_gates.py check",
            "python3 scripts/plugin_graph.py check",
            "python3 scripts/ecosystem_doctor.py check",
            "python3 scripts/demo_gallery.py check",
            "python3 scripts/validate_marketplace.py",
        ):
            self.assertIn(command, text)

    def test_docs_local_markdown_links_resolve(self):
        missing = []
        files = [README, DEMOS_README, *DOCS.values()]
        for path in files:
            if not path.exists():
                continue
            text = path.read_text()
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                clean = target.split("#", 1)[0]
                if not clean:
                    continue
                resolved = (path.parent / clean).resolve()
                if not resolved.exists():
                    missing.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual([], missing)


if __name__ == "__main__":
    unittest.main()
