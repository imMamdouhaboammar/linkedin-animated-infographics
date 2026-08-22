import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts import package_codex_release

ROOT = Path(__file__).resolve().parents[1]


class PublicPluginInstallabilityTests(unittest.TestCase):
    def build_archive(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        output = Path(tmp.name) / "plugin.zip"
        result = package_codex_release.build_archive(ROOT, output)
        self.assertTrue(output.is_file())
        return output, result

    def test_packaged_archive_uses_openai_documented_skills_root(self):
        output, result = self.build_archive()
        self.assertEqual("skills", result["skills_root"])
        self.assertEqual("openai-skills", result["source_skills_root"])

        with zipfile.ZipFile(output) as archive:
            names = archive.namelist()
            manifest = json.loads(archive.read(".codex-plugin/plugin.json"))

        self.assertEqual("./skills/", manifest["skills"])
        self.assertTrue(any(name.startswith("skills/") for name in names))
        self.assertFalse(any(name.startswith("openai-skills/") for name in names))
        self.assertFalse(any(name.startswith("demos/") for name in names))
        self.assertFalse(any(name.startswith("tests/") for name in names))
        self.assertFalse(any(name.startswith(".github/") for name in names))
        self.assertFalse(any(name.startswith("agents/") for name in names))

        skill_dirs = sorted({name.split("/", 2)[1] for name in names if name.startswith("skills/")})
        self.assertTrue(skill_dirs)
        for slug in skill_dirs:
            self.assertIn(f"skills/{slug}/SKILL.md", names)

    def test_workspace_and_python_baseline_skills_are_packaged(self):
        output, _ = self.build_archive()
        with zipfile.ZipFile(output) as archive:
            names = set(archive.namelist())

        self.assertIn("skills/host-workspace-operator/SKILL.md", names)
        self.assertIn("skills/sandbox-python-executor/SKILL.md", names)

    def test_public_brand_pack_is_complete_and_declared_icon_is_present(self):
        output, _ = self.build_archive()
        with zipfile.ZipFile(output) as archive:
            names = set(archive.namelist())
            manifest = json.loads(archive.read(".codex-plugin/plugin.json"))

        for path in (
            "assets/logo-light.svg",
            "assets/logo-dark.svg",
            "assets/plugin-icon.svg",
        ):
            self.assertIn(path, names)

        interface = manifest["interface"]
        self.assertEqual("./assets/plugin-icon.svg", interface["logo"])
        self.assertEqual("./assets/plugin-icon.svg", interface["composerIcon"])
        self.assertLessEqual(len(interface["displayName"]), 30)
        self.assertLessEqual(len(interface["shortDescription"]), 30)
        self.assertLessEqual(len(interface["defaultPrompt"]), 3)
        for prompt in interface["defaultPrompt"]:
            self.assertLessEqual(len(prompt), 128)

    def test_public_assets_exclude_demo_and_template_media(self):
        output, _ = self.build_archive()
        with zipfile.ZipFile(output) as archive:
            names = archive.namelist()

        forbidden = [
            name
            for name in names
            if name.startswith("assets/")
            and (name.lower().endswith(".html") or name.lower().endswith(".gif"))
        ]
        self.assertEqual([], forbidden)

    def test_only_plugin_json_lives_inside_codex_plugin_directory(self):
        output, _ = self.build_archive()
        with zipfile.ZipFile(output) as archive:
            manifest_members = [name for name in archive.namelist() if name.startswith(".codex-plugin/")]
        self.assertEqual([".codex-plugin/plugin.json"], manifest_members)


if __name__ == "__main__":
    unittest.main()
