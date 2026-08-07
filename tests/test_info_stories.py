import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "skills" / "info-stories" / "catalog.json"


class InfoStoriesRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from scripts import info_stories
        cls.mod = info_stories
        cls.catalog = info_stories.load_catalog(CATALOG)

    def test_registry_counts_and_unique_slugs(self):
        expected = {"houses": 10, "styles": 12, "archetypes": 15, "motions": 12}
        for axis, count in expected.items():
            items = self.catalog[axis]
            self.assertEqual(count, len(items), axis)
            slugs = [item["slug"] for item in items]
            names = [item["name"] for item in items]
            self.assertEqual(len(slugs), len(set(slugs)), f"duplicate {axis} slug")
            self.assertEqual(len(names), len(set(names)), f"duplicate {axis} name")

    def test_every_house_has_semantic_tokens_and_readable_text_pairs(self):
        required = {"bg", "surface", "ink", "ink_2", "muted", "line", "accent", "accent_deep"}
        for house in self.catalog["houses"]:
            self.assertTrue(required.issubset(house["tokens"]), house["slug"])
            for fg_name, bg_name in house["text_pairs"]:
                ratio = self.mod.contrast_ratio(house["tokens"][fg_name], house["tokens"][bg_name])
                self.assertGreaterEqual(ratio, 4.5, f"{house['slug']} {fg_name}/{bg_name} = {ratio:.2f}")

    def test_catalog_validator_reports_no_errors(self):
        self.assertEqual([], self.mod.validate_catalog(self.catalog))

    def test_unknown_slug_cli_fails_with_valid_choices(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "info_stories.py"), "show", "house", "does-not-exist"], cwd=ROOT, text=True, capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Valid choices", result.stderr)
        self.assertIn("ember-paper", result.stderr)

    def test_accepts_editorial_composition(self):
        self.assertEqual([], self.mod.check_composition(self.catalog, "signal-sheet", "framework-in-one-page", ["sequential-highlight"]))

    def test_accepts_terminal_composition(self):
        self.assertEqual([], self.mod.check_composition(self.catalog, "command-canvas", "one-prompt-full-workflow", ["type-on-terminal", "soft-zoom-focus"]))

    def test_rejects_terminal_motion_on_non_terminal_style(self):
        errors = self.mod.check_composition(self.catalog, "signal-sheet", "framework-in-one-page", ["type-on-terminal"])
        self.assertTrue(any("type-on-terminal" in error for error in errors))

    def test_scaffold_is_deterministic(self):
        kwargs = dict(topic="Agent skills explained", takeaway="Each layer has one job", cta="Save this reference", house="ember-paper", style="signal-sheet", archetype="framework-in-one-page", motions=["sequential-highlight", "chip-badge-pulse"], language="en", output_mode="gif")
        first = self.mod.build_brief(self.catalog, **kwargs)
        second = self.mod.build_brief(self.catalog, **kwargs)
        self.assertEqual(first, second)
        self.assertEqual("cheat-sheet-poster", first["execution"]["artboard_archetype"])
        self.assertEqual(["sequential-highlight", "chip-badge-pulse"], first["selection"]["motions"])

    def test_scaffold_unknown_slug_suggests_nearest_choice(self):
        with self.assertRaisesRegex(ValueError, "Did you mean 'signal-sheet'"):
            self.mod.build_brief(self.catalog, topic="x", takeaway="y", cta="z", house="ember-paper", style="signal-shet", archetype="framework-in-one-page", motions=[], language="en", output_mode="static")

    def test_public_skill_references_and_agents_exist(self):
        required = ["skills/info-stories/SKILL.md","skills/info-stories/references/palette-houses.md","skills/info-stories/references/visual-styles.md","skills/info-stories/references/story-archetypes.md","skills/info-stories/references/motion-patterns.md","skills/info-stories/references/composition-matrix.md","agents/story-architect.md","agents/palette-curator.md","agents/layout-composer.md","agents/motion-director.md","agents/copy-compressor.md","agents/evidence-checker.md"]
        self.assertEqual([], [path for path in required if not (ROOT / path).exists()])

    def test_reference_docs_cover_every_public_catalog_name(self):
        mappings = {"houses": ROOT / "skills/info-stories/references/palette-houses.md", "styles": ROOT / "skills/info-stories/references/visual-styles.md", "archetypes": ROOT / "skills/info-stories/references/story-archetypes.md", "motions": ROOT / "skills/info-stories/references/motion-patterns.md"}
        for axis, path in mappings.items():
            text = path.read_text()
            for item in self.catalog[axis]:
                self.assertIn(item["name"], text, f"{item['name']} missing from {path.name}")

    def test_agents_declare_narrow_handoff_contracts(self):
        requirements = {"story-architect.md":["Inputs","Outputs","Do not build HTML"],"palette-curator.md":["Inputs","Outputs","contrast"],"layout-composer.md":["Inputs","Outputs","artboard-builder"],"motion-director.md":["Inputs","Outputs","motion-engineer"],"copy-compressor.md":["Inputs","Outputs","facts"],"evidence-checker.md":["Inputs","Outputs","Do not invent"]}
        for filename, needles in requirements.items():
            text = (ROOT / "agents" / filename).read_text()
            for needle in needles:
                self.assertIn(needle, text, f"{needle!r} missing from {filename}")

    def test_copy_slop_detector_names_patterns(self):
        findings = self.mod.detect_copy_slop("Here's the thing: it's not just speed, it's a revolution. In conclusion, this changes everything.")
        names = {item["pattern"] for item in findings}
        self.assertIn("throat-clearing", names); self.assertIn("binary-contrast", names); self.assertIn("importance-puffery", names); self.assertIn("recap-ending", names)

    def test_copy_slop_detector_leaves_specific_plain_sentence_alone(self):
        self.assertEqual([], self.mod.detect_copy_slop("Deploy time fell from 40 minutes to 4 minutes."))

    def test_structural_fingerprint_rejects_palette_only_reskin(self):
        previous={"zone_topology":"three-column-board","card_grammar":"equal-rounded-cards","divider":"hairline","visual_anchor":"headline","density":"medium","motion_grammar":"sequential-highlight"}
        errors=self.mod.validate_fingerprint(dict(previous),previous,min_changes=2)
        self.assertTrue(errors); self.assertIn("structural", errors[0].lower())

    def test_structural_fingerprint_accepts_real_shape_change(self):
        previous={"zone_topology":"three-column-board","card_grammar":"equal-rounded-cards","divider":"hairline","visual_anchor":"headline","density":"medium","motion_grammar":"sequential-highlight"}
        current=dict(previous,zone_topology="layered-stack",card_grammar="mixed-span-panels",divider="negative-space")
        self.assertEqual([], self.mod.validate_fingerprint(current,previous,min_changes=2))

    def test_upstream_gates_are_wired_into_agents(self):
        for path in [ROOT/"skills/info-stories/references/anti-slop-gates.md",ROOT/"skills/info-stories/references/design-taste-gates.md"]: self.assertTrue(path.exists(),str(path))
        for path in [ROOT/"agents/copy-compressor.md",ROOT/"agents/layout-composer.md",ROOT/"agents/post-critic.md"]:
            text=path.read_text(); self.assertIn("anti-slop",text.lower()); self.assertIn("design-taste",text.lower())

    def test_every_visual_style_declares_design_dials(self):
        for style in self.catalog["styles"]:
            self.assertEqual({"design_variance","motion_intensity","visual_density"},set(style["dials"]),style["slug"])
            for value in style["dials"].values(): self.assertGreaterEqual(value,1); self.assertLessEqual(value,10)

    def test_story_brief_carries_style_design_dials(self):
        brief=self.mod.build_brief(self.catalog,topic="x",takeaway="y",cta="z",house="ember-paper",style="signal-sheet",archetype="framework-in-one-page",motions=["sequential-highlight"],language="en",output_mode="gif")
        self.assertEqual(8, brief["execution"]["design_dials"]["visual_density"])

    def test_new_post_resolves_info_stories_before_artboard_build(self):
        text=(ROOT/"skills/new-post/SKILL.md").read_text(); self.assertIn("info-stories",text.lower()); self.assertIn("story-architect",text); self.assertLess(text.index("story-architect"),text.index("artboard-builder"))

    def test_execution_agents_consume_resolved_story_brief(self):
        artboard=(ROOT/"agents/artboard-builder.md").read_text().lower(); motion=(ROOT/"agents/motion-engineer.md").read_text().lower(); self.assertIn("story brief",artboard); self.assertIn("story house",artboard); self.assertIn("motion pattern",motion); self.assertIn("story brief",motion)

    def test_plugin_version_and_readme_publish_info_stories(self):
        plugin=json.loads((ROOT/".claude-plugin/plugin.json").read_text()); self.assertEqual("3.0.0",plugin["version"]); self.assertIn("info-stories",plugin["keywords"])
        readme=(ROOT/"README.md").read_text().lower()
        for needle in ["info-stories","story house","scripts/info_stories.py","tools/palette_preview.py","tools/story_scaffold.py","tools/composition_check.py","tools/copy_slop_check.py"]: self.assertIn(needle,readme)

    def test_no_stale_linkedin_motion_namespace_in_core_skills_or_agents(self):
        offenders=[]
        for directory in (ROOT/"skills",ROOT/"agents"):
            for path in directory.rglob("*.md"):
                if "linkedin-motion" in path.read_text(): offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual([],offenders)

    def test_info_stories_public_tools_exist(self):
        required=[ROOT/"tools/palette_preview.py",ROOT/"tools/story_scaffold.py",ROOT/"tools/composition_check.py",ROOT/"tools/copy_slop_check.py"]
        self.assertEqual([], [str(path) for path in required if not path.exists()])

    def test_palette_preview_contains_every_story_house(self):
        result=subprocess.run([sys.executable,str(ROOT/"tools/palette_preview.py"),"--stdout"],cwd=ROOT,text=True,capture_output=True); self.assertEqual(0,result.returncode,result.stderr)
        for house in self.catalog["houses"]: self.assertIn(house["name"],result.stdout); self.assertIn(house["tokens"]["accent"],result.stdout)

    def test_copy_slop_tool_reports_machine_readable_findings(self):
        result=subprocess.run([sys.executable,str(ROOT/"tools/copy_slop_check.py"),"Here's the thing: this changes everything."],cwd=ROOT,text=True,capture_output=True); self.assertEqual(1,result.returncode); self.assertTrue(json.loads(result.stdout)["findings"])
        clean=subprocess.run([sys.executable,str(ROOT/"tools/copy_slop_check.py"),"Deploy time fell from 40 minutes to 4 minutes."],cwd=ROOT,text=True,capture_output=True); self.assertEqual(0,clean.returncode)

    def test_two_acceptance_story_briefs_are_deterministic(self):
        cases=[dict(topic="Agent skills reference",takeaway="Each layer has one job",cta="Save this reference",house="ember-paper",style="signal-sheet",archetype="framework-in-one-page",motions=["sequential-highlight","chip-badge-pulse"],language="en",output_mode="gif"),dict(topic="One prompt runs outbound",takeaway="The terminal coordinates the workflow",cta="See the workflow",house="midnight-operator",style="command-canvas",archetype="one-prompt-full-workflow",motions=["type-on-terminal","soft-zoom-focus"],language="en",output_mode="gif")]
        for case in cases: self.assertEqual(json.dumps(self.mod.build_brief(self.catalog,**case),sort_keys=True),json.dumps(self.mod.build_brief(self.catalog,**case),sort_keys=True))

    def test_tracked_palette_preview_matches_catalog_renderer(self):
        asset=ROOT/"assets/info-stories-palettes.html"; self.assertTrue(asset.exists()); result=subprocess.run([sys.executable,str(ROOT/"tools/palette_preview.py"),"--stdout"],cwd=ROOT,text=True,capture_output=True); self.assertEqual(0,result.returncode,result.stderr); self.assertEqual(result.stdout.rstrip("\n"),asset.read_text().rstrip("\n"))

    def test_tracked_acceptance_briefs_match_generator(self):
        cases=[(ROOT/"examples/info-stories/ember-signal-brief.json",dict(topic="Agent skills reference",takeaway="Each layer has one job",cta="Save this reference",house="ember-paper",style="signal-sheet",archetype="framework-in-one-page",motions=["sequential-highlight","chip-badge-pulse"],language="en",output_mode="gif")),(ROOT/"examples/info-stories/midnight-command-brief.json",dict(topic="One prompt runs outbound",takeaway="The terminal coordinates the workflow",cta="See the workflow",house="midnight-operator",style="command-canvas",archetype="one-prompt-full-workflow",motions=["type-on-terminal","soft-zoom-focus"],language="en",output_mode="gif"))]
        for path,case in cases: self.assertTrue(path.exists(),str(path)); self.assertEqual(self.mod.build_brief(self.catalog,**case),json.loads(path.read_text()))

    def test_state_defining_pairs_meet_three_to_one(self):
        for house in self.catalog["houses"]:
            for fg_name,bg_name in house.get("state_pairs",[]): self.assertGreaterEqual(self.mod.contrast_ratio(house["tokens"][fg_name],house["tokens"][bg_name]),3.0)

    def test_palette_preview_uses_deep_accent_for_text(self):
        result=subprocess.run([sys.executable,str(ROOT/"tools/palette_preview.py"),"--stdout"],cwd=ROOT,text=True,capture_output=True); self.assertEqual(0,result.returncode,result.stderr); self.assertIn("--accent-deep:",result.stdout); self.assertIn("color:var(--accent-deep)",result.stdout)


if __name__ == "__main__":
    unittest.main()
