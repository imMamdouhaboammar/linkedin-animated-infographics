import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPENAI_SKILL = ROOT / "openai-skills" / "linkedin-caption-narrative"
CANONICAL_CAPTION = ROOT / "skills" / "caption" / "SKILL.md"
CANONICAL_REFERENCE = ROOT / "skills" / "caption" / "references" / "linkedin-caption-narrative.md"


class CaptionNarrativeSkillTests(unittest.TestCase):
    def test_openai_skill_package_exists(self):
        required = (
            OPENAI_SKILL / "SKILL.md",
            OPENAI_SKILL / "agents" / "openai.yaml",
            OPENAI_SKILL / "references" / "reference-examples.md",
            OPENAI_SKILL / "references" / "quality-gates.md",
        )
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual([], missing)

    def test_openai_skill_has_discovery_frontmatter(self):
        text = (OPENAI_SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertIn("name: linkedin-caption-narrative", frontmatter)
        self.assertIn("description: Use when", frontmatter)

    def test_openai_default_prompt_is_a_string(self):
        text = (OPENAI_SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertRegex(text, r'(?m)^\s*default_prompt:\s*".+"\s*$')
        self.assertNotRegex(text, r'(?m)^\s*default_prompt:\s*$')

    def test_canonical_caption_routes_matching_work_to_narrative_reference(self):
        caption = CANONICAL_CAPTION.read_text(encoding="utf-8")
        self.assertIn("references/linkedin-caption-narrative.md", caption)
        self.assertIn("Plugin or Skill stacks", caption)
        self.assertIn("first-comment utility split", caption)

    def test_reference_preserves_pattern_and_house_style_contract(self):
        text = CANONICAL_REFERENCE.read_text(encoding="utf-8")
        for marker in (
            "Tension → Named Thing → Mechanism → Specifics → Why It Matters → Visual Bridge → Action",
            "Repo Explainer",
            "Stack Catalogue",
            "Operating Story",
            "Belief Correction",
            "Recent-Signal Story",
            "Visual Companion",
            "House style outranks this reference",
            "If the user bans terminal periods",
        ):
            self.assertIn(marker, text)

    def test_reference_examples_cover_supplied_style_family(self):
        text = (OPENAI_SKILL / "references" / "reference-examples.md").read_text(encoding="utf-8")
        for marker in (
            "claudish-to-english",
            "100+ Claude repos catalogue",
            "olmOCR",
            "i-have-adhd",
            "/last30days",
            "GEO and AEO page example",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
