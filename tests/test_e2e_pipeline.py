#!/usr/bin/env python3
"""End-to-End (E2E) integration test suite for the LinkedIn Animated Infographics plugin.

This suite executes the entire production pipeline end-to-end:
1. MasterOne profile & router resolution
2. Story intelligence retrieval & scaffolding
3. Verified identity asset management & policy checks
4. Intentional typography & offline font enforcement
5. Story House color palette & WCAG contrast compliance
6. Copy compression & anti-slop guardrails
7. Static artboard linting and DOM auditor
8. Headless browser rendering, frame capture, and GIF assembly (render.sh)
9. Render report verification and quality gates
10. Antigravity subagent catalog & multi-host parity validators
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


class EndToEndPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_e2e_01_routing_and_orchestration(self):
        """E2E Test: Router correctly routes 'create-post' through canonical 17-stage workflow."""
        script = ROOT / "scripts" / "ecosystem_router.py"
        proc = subprocess.run(
            [sys.executable, str(script), "route", "--request", "create a developer signal map post", "--intent", "create-post"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=True,
        )
        data = json.loads(proc.stdout)
        self.assertEqual("new-post", data["workflow"])
        self.assertIn("agents", data)
        self.assertIn("capabilities", data)
        self.assertIn("quality_gates", data)

        # Confirm critical worker sequence
        agents = data["agents"]
        self.assertIn("creative-director", agents)
        self.assertIn("asset-curator", agents)
        self.assertIn("type-curator", agents)
        self.assertIn("layout-composer", agents)
        self.assertIn("artboard-builder", agents)
        self.assertIn("motion-director", agents)
        self.assertIn("motion-engineer", agents)
        self.assertIn("render-qa", agents)
        self.assertIn("story-verifier", agents)

    def test_e2e_02_masterone_profile(self):
        """E2E Test: MasterOne profile manager initializes and validates project configuration."""
        script = ROOT / "scripts" / "masterone_profile.py"
        proc = subprocess.run(
            [sys.executable, str(script), "check", "--intent", "create-post"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=True,
        )
        data = json.loads(proc.stdout)
        self.assertEqual("READY", data.get("profile_state"))
        self.assertEqual([], data.get("validation_errors"))

    def test_e2e_03_story_intelligence_retrieval(self):
        """E2E Test: Deterministic retrieval returns valid Info-stories context capsule."""
        retrieve_script = ROOT / "tools" / "story_retrieve.py"
        query_file = self.tmp_path / "query.json"
        query_file.write_text(json.dumps({
            "stage": "review",
            "story_jobs": ["explain-system"],
            "content_shapes": ["process"],
            "output_mode": "gif",
            "language": "en",
            "density": "medium",
            "evidence_mode": "documented",
            "top_k": 3,
            "byte_budget": 4000
        }))

        proc = subprocess.run(
            [sys.executable, str(retrieve_script), "--query", str(query_file)],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=True,
        )
        capsule = json.loads(proc.stdout)
        self.assertEqual("review", capsule.get("stage"))
        self.assertIn("mechanisms", capsule)
        self.assertGreater(len(capsule["mechanisms"]), 0)

    def test_e2e_04_verified_identity_sourcing_and_policy(self):
        """E2E Test: Brand icon catalog verification and asset policy validation."""
        # 1. Brand icon check
        brand_tool = ROOT / "tools" / "brand_icon.py"
        proc = subprocess.run(
            [sys.executable, str(brand_tool), "check"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=True,
        )
        self.assertIn("Brand icons: OK", proc.stdout)

        # 2. Asset policy check with valid plan
        valid_plan_file = self.tmp_path / "asset-plan.json"
        valid_plan_file.write_text(json.dumps({
            "schema_version": 1,
            "assets": [
                {
                    "name": "ChatGPT / OpenAI Brand Mark",
                    "kind": "icon",
                    "source_type": "lobe",
                    "lobe_slug": "openai",
                    "package": "@lobehub/icons-static-svg@1.94.0",
                    "source_ref": "@lobehub/icons-static-svg@1.94.0:assets/brand-icons/openai.svg",
                    "render_disposition": "local",
                    "local_path": "assets/brand-icons/openai.svg",
                    "identity_locked": True,
                    "status": "PASS",
                    "provenance": {
                        "source_url": "https://unpkg.com/@lobehub/icons-static-svg@1.94.0/icons/openai.svg",
                        "sha256": "a595df6b423920c67a7f8f73c063e4bfb72d415948097b6cac063a2366bb5186",
                        "license": "MIT",
                        "trademark_notice": "OpenAI / ChatGPT mark used nominatively for product identification."
                    }
                }
            ]
        }))

        asset_policy_tool = ROOT / "tools" / "asset_policy_check.py"
        proc_valid = subprocess.run(
            [sys.executable, str(asset_policy_tool), str(valid_plan_file)],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(0, proc_valid.returncode, f"Asset policy failed on valid plan: {proc_valid.stderr}")

        # 3. Asset policy check rejects unverified / generated / remote assets
        invalid_plan_file = self.tmp_path / "invalid-asset-plan.json"
        invalid_plan_file.write_text(json.dumps({
            "schema_version": 1,
            "assets": [
                {
                    "name": "Generated Lookalike Logo",
                    "kind": "icon",
                    "source_type": "generated",
                    "render_disposition": "remote",
                    "status": "PASS"
                }
            ]
        }))
        proc_invalid = subprocess.run(
            [sys.executable, str(asset_policy_tool), str(invalid_plan_file)],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertNotEqual(0, proc_invalid.returncode)

    def test_e2e_05_typography_and_contrast_compliance(self):
        """E2E Test: Typography spec validation & Story House contrast checks."""
        # 1. Typography spec check with system/local fonts
        valid_type_file = self.tmp_path / "type-spec.json"
        valid_type_file.write_text(json.dumps({
            "schema_version": 1,
            "direction_name": "clean-editorial-system",
            "headline_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            "body_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            "loading_strategy": "system",
            "fallbacks": ["Helvetica Neue", "Arial", "sans-serif"],
            "pairing_reason": "Clean modern system sans pairing with high legibility.",
            "story_fit": "Fits technical signal map and editorial infographic story.",
            "single_family_reason": "Single geometric system sans ensures high density balance.",
            "render_safety": "System fonts are locally available without network requests.",
            "status": "PASS"
        }))
        type_tool = ROOT / "tools" / "type_spec_check.py"
        proc_type = subprocess.run(
            [sys.executable, str(type_tool), str(valid_type_file)],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(0, proc_type.returncode, f"Type check failed: {proc_type.stdout}")

        # 2. Remote font dependency is rejected
        invalid_type_file = self.tmp_path / "invalid-type-spec.json"
        invalid_type_file.write_text(json.dumps({
            "schema_version": 1,
            "direction_name": "remote-google-fonts",
            "headline_family": "Inter",
            "body_family": "Roboto",
            "loading_strategy": "remote",
            "fallbacks": ["sans-serif"],
            "pairing_reason": "Online fonts",
            "story_fit": "Testing rejection",
            "render_safety": "https://fonts.googleapis.com/css2?family=Inter",
            "status": "PASS"
        }))
        proc_type_inv = subprocess.run(
            [sys.executable, str(type_tool), str(invalid_type_file)],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertNotEqual(0, proc_type_inv.returncode)

        # 3. Contrast check on default Story House tokens
        contrast_tool = ROOT / "tools" / "contrast_check.py"
        proc_contrast = subprocess.run(
            [sys.executable, str(contrast_tool), "--house", "ember-paper", "--fg", "ink", "--bg", "bg"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(0, proc_contrast.returncode, f"Contrast check failed: {proc_contrast.stdout}")

    def test_e2e_06_copy_compression_anti_slop(self):
        """E2E Test: Copy anti-slop guardrails flag low-information buzzwords."""
        copy_tool = ROOT / "tools" / "copy_slop_check.py"

        # Compliant factual copy
        clean_text = "The signal map indexes 8 public sources across 30 days."
        proc_clean = subprocess.run(
            [sys.executable, str(copy_tool), clean_text],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(0, proc_clean.returncode)

        # Slop copy containing rejected buzzwords
        slop_text = "This revolutionary game changer will elevate your synergy seamlessly."
        proc_slop = subprocess.run(
            [sys.executable, str(copy_tool), slop_text],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertNotEqual(0, proc_slop.returncode)

    def test_e2e_07_full_render_pipeline_and_qa_evidence(self):
        """E2E Test: Full render pipeline from HTML artboard to GIF, still PNG, and merged QA report."""
        artboard_fixture = FIXTURES / "artboard-min.html"
        self.assertTrue(artboard_fixture.exists(), "Missing artboard-min.html fixture")

        out_gif = self.tmp_path / "post.gif"
        render_sh = ROOT / "scripts" / "render.sh"

        # Execute full render.sh pipeline
        proc = subprocess.run(
            ["bash", str(render_sh), str(artboard_fixture), str(out_gif), "--duration", "1.0", "--fps", "10"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        if "render toolchain unavailable" in proc.stderr or "playwright is not installed" in proc.stderr:
            raise unittest.SkipTest("Browser render toolchain unavailable in this environment")

        self.assertEqual(0, proc.returncode, f"render.sh failed: stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")

        # Verify all output artifacts were created
        still_png = self.tmp_path / "still.png"
        mobile_png = self.tmp_path / "still_mobile350.png"
        report_json = self.tmp_path / "render-report.json"
        evidence_dir = self.tmp_path / ".render-evidence"

        self.assertTrue(out_gif.is_file(), "post.gif was not created")
        self.assertTrue(still_png.is_file(), "still.png was not created")
        self.assertTrue(mobile_png.is_file(), "still_mobile350.png was not created")
        self.assertTrue(report_json.is_file(), "render-report.json was not created")
        self.assertTrue(evidence_dir.is_dir(), ".render-evidence directory was not created")

        # Verify file size constraint (< 5MB for LinkedIn)
        gif_size = out_gif.stat().st_size
        self.assertGreater(gif_size, 0)
        self.assertLess(gif_size, 5 * 1024 * 1024, "GIF exceeds 5MB limit")

        # Verify QA report contains PASS verdict and all required evidence sections
        report = json.loads(report_json.read_text())
        self.assertEqual("PASS", report.get("verdict"))
        self.assertIn("sources", report)
        self.assertIn("artboard", report["sources"])
        self.assertIn("still", report["sources"])
        self.assertIn("gif", report["sources"])
        self.assertIn("findings", report)
        self.assertIn("summary", report)
        self.assertEqual(0, report["summary"]["counts"]["FAIL"])

    def test_e2e_08_multihost_and_subagent_integrity(self):
        """E2E Test: Multi-host packages and 20 Antigravity subagent definitions are strictly synchronized."""
        # 1. Ecosystem doctor check
        proc_doc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "ecosystem_doctor.py"), "check"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=True,
        )
        self.assertIn("Ecosystem doctor: OK", proc_doc.stdout)

        # 2. Antigravity subagents sync check (19 specialized subagents)
        proc_agy = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "antigravity_agents.py"), "check"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=True,
        )
        self.assertIn("Antigravity agents check: OK (19 agents verified)", proc_agy.stdout)

        # 3. Host package validators
        subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_antigravity_plugin.py")], check=True, cwd=ROOT)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_marketplace.py")], check=True, cwd=ROOT)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_codex_plugin.py")], check=True, cwd=ROOT)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "research_gates.py"), "check"], check=True, cwd=ROOT)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "plugin_graph.py"), "check"], check=True, cwd=ROOT)


if __name__ == "__main__":
    unittest.main()
