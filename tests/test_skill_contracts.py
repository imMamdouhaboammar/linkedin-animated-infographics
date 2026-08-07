import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills"
REQUIRED_SECTIONS = (
    "Purpose",
    "Use when",
    "Inputs",
    "Outputs",
    "Procedure",
    "HOLD conditions",
    "Related components",
    "Research gates",
)


class SkillContractTests(unittest.TestCase):
    def test_every_public_skill_has_v3_contract_sections(self):
        skills = sorted(SKILL_ROOT.glob("*/SKILL.md"))
        self.assertGreaterEqual(len(skills), 10)
        failures = []
        for path in skills:
            text = path.read_text()
            for section in REQUIRED_SECTIONS:
                if not re.search(rf"^## {re.escape(section)}\s*$", text, re.MULTILINE):
                    failures.append(f"{path.parent.name}: missing {section}")
        self.assertEqual([], failures)

    def test_every_skill_frontmatter_has_name_and_description(self):
        failures = []
        for path in sorted(SKILL_ROOT.glob("*/SKILL.md")):
            text = path.read_text()
            if not text.startswith("---\n"):
                failures.append(f"{path.parent.name}: missing frontmatter")
                continue
            frontmatter = text.split("---", 2)[1]
            for key in ("name:", "description:"):
                if key not in frontmatter:
                    failures.append(f"{path.parent.name}: missing {key[:-1]}")
        self.assertEqual([], failures)

    def test_every_skill_points_to_helper_authority(self):
        failures = []
        for path in sorted(SKILL_ROOT.glob("*/SKILL.md")):
            text = path.read_text()
            if "helper/GUIDE.md" not in text:
                failures.append(path.parent.name)
        self.assertEqual([], failures, f"skills missing helper authority: {failures}")

    def test_workflow_skills_name_parent_or_focused_execution(self):
        expectations = {
            "post": "routing entrypoint",
            "new-post": "parent workflow",
            "qa-post": "parent workflow",
            "render-gif": "focused workflow",
        }
        for skill, needle in expectations.items():
            text = (SKILL_ROOT / skill / "SKILL.md").read_text().lower()
            self.assertIn(needle, text, skill)

    def test_named_mascot_rules_remain_exact_svg_only(self):
        for skill in ("mascots", "svg-mascot-animator"):
            text = (SKILL_ROOT / skill / "SKILL.md").read_text().lower()
            self.assertIn("exact svg", text, skill)
            self.assertIn("hold", text, skill)

    def test_research_derived_skills_name_gate_ids(self):
        expectations = {
            "caption": ("prose-specificity", "voice-preservation"),
            "artboard": ("structural-originality", "contrast-discipline"),
            "info-stories": ("design-dials", "structural-originality"),
            "new-post": ("evidence-traceability", "bounded-verification"),
            "qa-post": ("bounded-verification",),
            "render": ("bounded-verification",),
        }
        for skill, gates in expectations.items():
            text = (SKILL_ROOT / skill / "SKILL.md").read_text()
            for gate in gates:
                self.assertIn(f"`{gate}`", text, f"{skill}: missing {gate}")

    def test_visual_creation_skills_name_plugin_local_defaults(self):
        for skill in ("artboard", "info-stories", "new-post"):
            text = (SKILL_ROOT / skill / "SKILL.md").read_text().lower()
            self.assertIn("creative-attractive-restrained", text, skill)
            self.assertIn("center-first", text, skill)


if __name__ == "__main__":
    unittest.main()
