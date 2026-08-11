import copy
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def mechanism(slug, *, reference_id="REF-001", content_shapes=None, output_modes=None):
    return {
        "slug": slug,
        "name": slug.replace("-", " ").title(),
        "origin": "extracted",
        "story_jobs": ["explain-system"],
        "content_shapes": content_shapes or ["process"],
        "compatibility": {
            "output_modes": output_modes or ["gif", "static"],
            "languages": ["*"],
            "densities": ["medium"],
            "evidence_modes": ["documented"],
            "styles": ["sequence-board"],
            "archetypes": ["step-by-step-playbook"],
            "motions": ["sequential-highlight"],
        },
        "hook": "Show the system before naming its parts.",
        "beats": ["whole", "parts", "payoff"],
        "palette_roles": ["neutral-base", "single-accent"],
        "layout": {
            "topology": f"{slug}-topology",
            "zones": ["hook", "system", "payoff"],
            "proportions": "1:3:1",
            "negative_space": "Separate the hook from the system.",
        },
        "hierarchy": {
            "primary": "system",
            "secondary": "hook",
            "reading_order": ["hook", "system", "payoff"],
        },
        "typography": {
            "classes": ["sans", "mono"],
            "roles": ["display", "body", "label"],
            "language_policy": "Use a script-capable local stack.",
        },
        "motion": {
            "job": "reveal-order",
            "target": "system parts",
            "sequence": ["whole", "parts"],
            "timing_family": "stepped",
            "static_regions": ["hook", "payoff"],
        },
        "loop": {"strategy": "hold-reset", "hold": "long", "reset": "direct"},
        "constraints": ["Keep the first frame complete."],
        "anti_patterns": ["Equal emphasis on every zone."],
        "implementation_hints": ["Use semantic grid areas."],
        "reference_ids": [reference_id],
        "influence_axes": {reference_id: ["structure", "motion"]},
        "originality": {
            "adopt": ["unequal zone hierarchy"],
            "reject": ["source copy", "logos", "signature illustration"],
        },
    }


class InfoStoryRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from scripts import info_stories

        cls.mod = info_stories

    def catalog(self, mechanisms):
        return {
            "mechanisms": mechanisms,
            "references": [{"id": "REF-001"}, {"id": "REF-002"}, {"id": "REF-003"}],
            "styles": [{"slug": "sequence-board"}],
            "archetypes": [{"slug": "step-by-step-playbook"}],
            "motions": [{"slug": "sequential-highlight"}],
        }

    def test_mechanism_schema_accepts_complete_rows(self):
        self.assertEqual([], self.mod.validate_mechanisms(self.catalog([mechanism("system-map")])) )

    def test_mechanism_schema_rejects_missing_fields_duplicate_slugs_and_fingerprints(self):
        first = mechanism("system-map")
        duplicate_slug = mechanism("system-map")
        duplicate_slug["layout"]["topology"] = "other"
        duplicate_fingerprint = copy.deepcopy(first)
        duplicate_fingerprint["slug"] = "same-visual-different-name"
        duplicate_fingerprint["name"] = "Same Visual Different Name"
        duplicate_fingerprint["layout"]["negative_space"] = "Equivalent spacing, reworded."
        incomplete = {"slug": "incomplete"}

        errors = self.mod.validate_mechanisms(
            self.catalog([first, duplicate_slug, duplicate_fingerprint, incomplete])
        )

        self.assertTrue(any("duplicate slug system-map" in error for error in errors), errors)
        self.assertTrue(any("duplicate fingerprint" in error for error in errors), errors)
        self.assertTrue(any("incomplete" in error and "missing" in error for error in errors), errors)

    def test_mechanism_schema_rejects_broken_reference_ids(self):
        broken = mechanism("broken-reference", reference_id="REF-999")
        malformed = mechanism("malformed-reference")
        malformed["reference_ids"] = [7]
        malformed["influence_axes"] = {7: ["structure"]}
        errors = self.mod.validate_mechanisms(self.catalog([broken, malformed]))
        self.assertTrue(any("REF-999" in error and "unknown" in error for error in errors), errors)
        self.assertTrue(any("7" in error and "unknown" in error for error in errors), errors)
        self.assertTrue(self.mod.validate_mechanisms({"mechanisms": [malformed]}))

    def test_mechanism_schema_rejects_incomplete_nested_logic(self):
        incomplete = mechanism("incomplete-logic")
        incomplete["layout"].pop("negative_space")
        incomplete["motion"].pop("static_regions")
        incomplete["originality"].pop("reject")
        incomplete["compatibility"].pop("styles")

        errors = self.mod.validate_mechanisms(self.catalog([incomplete]))

        for field in (
            "compatibility.styles",
            "layout.negative_space",
            "motion.static_regions",
            "originality.reject",
        ):
            self.assertTrue(any(field in error for error in errors), (field, errors))

    def test_mechanism_schema_rejects_unknown_compatible_catalog_axes(self):
        broken = mechanism("broken-compatibility")
        broken["compatibility"]["styles"] = ["missing-style"]

        errors = self.mod.validate_mechanisms(self.catalog([broken]))

        self.assertTrue(any("missing-style" in error and "unknown" in error for error in errors), errors)

    def test_catalog_loader_merges_mechanisms_and_enforces_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog_path = root / "catalog.json"
            extensions = root / "extensions"
            extensions.mkdir()
            catalog_path.write_text(json.dumps({"mechanisms": [mechanism("base")]}))
            (extensions / "one.json").write_text(
                json.dumps({"mechanisms": [mechanism("extension")]})
            )
            merged = self.mod.load_catalog(catalog_path, extensions)
            self.assertEqual(["base", "extension"], [row["slug"] for row in merged["mechanisms"]])

            (extensions / "overflow.json").write_text(
                json.dumps({"mechanisms": [mechanism(f"extra-{index}") for index in range(150)]})
            )
            with self.assertRaisesRegex(ValueError, "150"):
                self.mod.load_catalog(catalog_path, extensions)

    def test_hard_constraints_filter_before_scoring(self):
        matching = mechanism("matching")
        wrong_mode = mechanism("wrong-mode", output_modes=["static"])
        wrong_language = mechanism("wrong-language")
        wrong_language["compatibility"]["languages"] = ["ar"]
        wrong_density = mechanism("wrong-density")
        wrong_density["compatibility"]["densities"] = ["high"]
        wrong_evidence = mechanism("wrong-evidence")
        wrong_evidence["compatibility"]["evidence_modes"] = ["conceptual"]
        wrong_shape = mechanism("wrong-shape", content_shapes=["comparison"])
        query = {
            "story_jobs": ["explain-system"],
            "content_shapes": ["process"],
            "output_mode": "gif",
            "language": "en",
            "density": "medium",
            "evidence_mode": "documented",
            "top_k": 10,
        }

        ranked = self.mod.rank_mechanisms(
            self.catalog([wrong_shape, wrong_evidence, wrong_density, wrong_language, wrong_mode, matching]),
            query,
        )

        self.assertEqual(["matching"], [row["slug"] for row in ranked])
        self.assertGreater(ranked[0]["score"], 0)
        self.assertEqual(
            ["story_jobs", "content_shapes"],
            [reason["axis"] for reason in ranked[0]["score_reasons"]],
        )

    def test_singular_content_shape_is_a_hard_constraint(self):
        query = {
            "story_jobs": ["explain-system"],
            "content_shape": "process",
            "output_mode": "gif",
            "language": "en",
            "density": "medium",
            "evidence_mode": "documented",
            "top_k": 10,
        }
        catalog = self.catalog([
            mechanism("comparison", content_shapes=["comparison"]),
            mechanism("process", content_shapes=["process"]),
        ])

        ranked = self.mod.rank_mechanisms(catalog, query)

        self.assertEqual(["process"], [row["slug"] for row in ranked])

    def test_ranking_requires_every_hard_constraint(self):
        query = {
            "story_jobs": ["explain-system"],
            "content_shape": "process",
            "output_mode": "gif",
            "language": "en",
            "density": "medium",
            "top_k": 1,
        }

        with self.assertRaisesRegex(ValueError, "evidence_mode"):
            self.mod.rank_mechanisms(self.catalog([mechanism("process")]), query)

    def test_ranking_is_deterministic_for_shuffled_input_and_uses_slug_ties(self):
        mechanisms = [mechanism("zeta"), mechanism("alpha"), mechanism("middle")]
        query = {
            "story_jobs": ["explain-system"],
            "content_shapes": ["process"],
            "output_mode": "gif",
            "language": "en",
            "density": "medium",
            "evidence_mode": "documented",
            "top_k": 3,
        }
        expected = ["alpha", "middle", "zeta"]
        for seed in range(8):
            shuffled = copy.deepcopy(mechanisms)
            random.Random(seed).shuffle(shuffled)
            ranked = self.mod.rank_mechanisms(self.catalog(shuffled), query)
            self.assertEqual(expected, [row["slug"] for row in ranked])

    def test_ranking_applies_top_k_and_scores_explicit_references(self):
        preferred = mechanism("preferred", reference_id="REF-002")
        other = mechanism("other")
        query = {
            "story_jobs": ["explain-system"],
            "content_shapes": ["process"],
            "output_mode": "gif",
            "language": "en",
            "density": "medium",
            "evidence_mode": "documented",
            "reference_ids": ["REF-002"],
            "top_k": 1,
        }

        ranked = self.mod.rank_mechanisms(self.catalog([other, preferred]), query)

        self.assertEqual(["preferred"], [row["slug"] for row in ranked])
        reference_reason = next(row for row in ranked[0]["score_reasons"] if row["axis"] == "reference_ids")
        self.assertEqual(3, reference_reason["points"])

    def test_context_capsules_are_stage_specific_and_select_bounded_references(self):
        structural = mechanism("structural", reference_id="REF-001")
        motion = mechanism("motion", reference_id="REF-002")
        motion["influence_axes"] = {"REF-002": ["motion"]}
        typography = mechanism("typography", reference_id="REF-003")
        typography["influence_axes"] = {"REF-003": ["typography"]}
        catalog = self.catalog([structural, motion, typography])
        ranked = [
            {"slug": row["slug"], "score": 10, "score_reasons": []}
            for row in (structural, motion, typography)
        ]

        concept = self.mod.build_context_capsule(catalog, ranked, "concept", 8000)
        layout = self.mod.build_context_capsule(catalog, ranked, "layout", 8000)
        motion_capsule = self.mod.build_context_capsule(catalog, ranked, "motion", 8000)

        self.assertIn("hook", concept["mechanisms"][0])
        self.assertNotIn("layout", concept["mechanisms"][0])
        self.assertIn("layout", layout["mechanisms"][0])
        self.assertNotIn("motion", layout["mechanisms"][0])
        self.assertIn("motion", motion_capsule["mechanisms"][0])
        self.assertEqual(
            [("REF-001", "primary", "structure"), ("REF-002", "secondary", "motion"), ("REF-003", "secondary", "typography")],
            [(row["id"], row["role"], row["influence_axis"]) for row in concept["references"]],
        )

    def test_context_capsule_enforces_utf8_byte_budget(self):
        rows = [mechanism(f"arabic-{index}") for index in range(4)]
        for row in rows:
            row["hook"] = "خريطة مرئية تشرح النظام قبل التفاصيل"
        catalog = self.catalog(rows)
        ranked = [
            {"slug": row["slug"], "score": 10, "score_reasons": [{"axis": "story_jobs", "matches": ["explain-system"], "weight": 8, "points": 8}]}
            for row in rows
        ]

        capsule = self.mod.build_context_capsule(catalog, ranked, "concept", 1300)
        encoded = json.dumps(
            capsule, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")

        self.assertLessEqual(len(encoded), 1300)
        self.assertGreater(capsule["omitted_mechanisms"], 0)

    def test_default_catalog_and_cli_are_valid_and_deterministic(self):
        catalog = self.mod.load_catalog()
        self.assertGreaterEqual(len(catalog["mechanisms"]), 30)
        self.assertLessEqual(len(catalog["mechanisms"]), 50)
        self.assertEqual([], self.mod.validate_mechanisms(catalog))
        query = {
            "stage": "review",
            "story_jobs": ["explain-system"],
            "content_shapes": ["process"],
            "output_mode": "gif",
            "language": "en",
            "density": "medium",
            "evidence_mode": "documented",
            "top_k": 3,
            "byte_budget": 4000,
        }
        with tempfile.TemporaryDirectory() as tmp:
            query_path = Path(tmp) / "query.json"
            query_path.write_text(json.dumps(query))
            command = [sys.executable, str(ROOT / "tools" / "story_retrieve.py"), "--query", str(query_path)]
            first = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
            second = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout)
        self.assertEqual("review", payload["stage"])
        self.assertLessEqual(len(first.stdout.rstrip("\n").encode("utf-8")), 4000)


if __name__ == "__main__":
    unittest.main()
