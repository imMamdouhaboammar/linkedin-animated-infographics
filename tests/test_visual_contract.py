"""The visual contract is the single source of truth for measurable thresholds.

These tests lock it in both directions:

* contract -> prose: every ``doc_assertions`` string must still appear in the named
  file, so editing a number in the JSON without updating the docs fails, and editing
  the number in a doc makes its assertion string disappear and fails the same test.
* contract -> code: the thresholds must equal the constants the scripts actually use,
  so an implementation default can never quietly diverge from the published number.
"""

import argparse
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "helper" / "visual-contract.json"
SEVERITIES = {"blocking", "advisory"}
REQUIRED_FIELDS = ("value", "unit", "severity", "gate", "measured_by", "rationale")


def load_contract():
    return json.loads(CONTRACT.read_text())


def _argparse_defaults(script_relpath):
    """Return {dest: default} for a script's parser without executing its main()."""
    path = ROOT / script_relpath
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    captured = {}
    original = argparse.ArgumentParser.parse_args

    def intercept(self, *args, **kwargs):
        for action in self._actions:
            captured[action.dest] = action.default
        raise SystemExit(0)

    argparse.ArgumentParser.parse_args = intercept
    try:
        spec.loader.exec_module(module)
        try:
            module.main()
        except SystemExit:
            pass
    finally:
        argparse.ArgumentParser.parse_args = original
    return captured


class VisualContractStructureTests(unittest.TestCase):
    def test_contract_parses_and_declares_thresholds(self):
        contract = load_contract()
        self.assertEqual(1, contract["schema_version"])
        self.assertTrue(contract["thresholds"], "contract declares no thresholds")

    def test_every_threshold_is_fully_specified(self):
        contract = load_contract()
        gates = contract["gates"]
        failures = []
        for tid, threshold in contract["thresholds"].items():
            for field in REQUIRED_FIELDS:
                if threshold.get(field) in (None, ""):
                    failures.append(f"{tid}: missing {field}")
            if threshold.get("severity") not in SEVERITIES:
                failures.append(f"{tid}: severity must be one of {sorted(SEVERITIES)}")
            if threshold.get("gate") not in gates:
                failures.append(f"{tid}: gate {threshold.get('gate')!r} is not declared")
            if not isinstance(threshold.get("value"), (int, float)):
                failures.append(f"{tid}: value must be numeric")
        self.assertEqual([], failures)

    def test_measuring_scripts_exist(self):
        contract = load_contract()
        missing = [
            f"{tid}: {threshold['measured_by']}"
            for tid, threshold in contract["thresholds"].items()
            if not (ROOT / threshold["measured_by"]).is_file()
        ]
        self.assertEqual([], missing)

    def test_advisory_thresholds_explain_why_they_do_not_block(self):
        """An advisory threshold is a deliberate choice and must justify itself."""
        contract = load_contract()
        thin = [
            tid
            for tid, threshold in contract["thresholds"].items()
            if threshold["severity"] == "advisory" and len(threshold["rationale"]) < 60
        ]
        self.assertEqual([], thin)


class ContractMatchesProseTests(unittest.TestCase):
    def test_documented_numbers_match_the_contract(self):
        contract = load_contract()
        failures = []
        for tid, threshold in contract["thresholds"].items():
            for relpath, needles in threshold.get("doc_assertions", {}).items():
                target = ROOT / relpath
                if not target.is_file():
                    failures.append(f"{tid}: missing doc {relpath}")
                    continue
                text = target.read_text()
                for needle in needles:
                    if needle not in text:
                        failures.append(f"{tid}: {relpath} no longer states {needle!r}")
        self.assertEqual([], failures)

    def test_blocking_thresholds_are_documented_somewhere(self):
        contract = load_contract()
        undocumented = [
            tid
            for tid, threshold in contract["thresholds"].items()
            if threshold["severity"] == "blocking" and not threshold.get("doc_assertions")
            and tid != "contrast.state_min_ratio"
        ]
        self.assertEqual([], undocumented)

    def test_superseded_loop_metrics_stay_out_of_the_docs(self):
        """The absolute seam percentages were replaced by the ratio; keep them gone."""
        contract = load_contract()
        self.assertEqual(2.0, contract["thresholds"]["loop.seam_ratio_max"]["value"])
        offenders = []
        for relpath in ("skills/render/references/qa-gates.md",
                        "skills/motion/references/animation-recipes.md"):
            text = (ROOT / relpath).read_text()
            for stale in ("under 8%", "Above 8%", "Above\n0.5%", "0.5% means"):
                if stale in text:
                    offenders.append(f"{relpath}: {stale!r}")
        self.assertEqual([], offenders)


class ContractMatchesCodeTests(unittest.TestCase):
    def test_check_render_defaults_match_the_contract(self):
        contract = load_contract()["thresholds"]
        defaults = _argparse_defaults("scripts/check_render.py")
        self.assertEqual(contract["artboard.width"]["value"], defaults["width"])
        self.assertEqual(contract["artboard.height"]["value"], defaults["height"])
        self.assertEqual(contract["safe_margin_px"]["value"], defaults["margin"])

    def test_capture_frames_defaults_match_the_contract(self):
        contract = load_contract()["thresholds"]
        defaults = _argparse_defaults("scripts/capture_frames.py")
        self.assertEqual(contract["artboard.width"]["value"], defaults["width"])
        self.assertEqual(contract["artboard.height"]["value"], defaults["height"])

    def test_gif_budget_matches_build_gif_default(self):
        contract = load_contract()["thresholds"]
        defaults = _argparse_defaults("scripts/build_gif.py")
        expected_mb = contract["gif.max_bytes"]["value"] / 1024 / 1024
        self.assertEqual(expected_mb, defaults["max_mb"])

    def test_caller_budget_cannot_weaken_the_contract_limit(self):
        from scripts.build_gif import file_budget_finding
        from scripts.visual_contract import VisualContract

        contract = VisualContract()
        contract_limit = contract.value("gif.max_bytes")
        row = file_budget_finding(
            contract,
            size=contract_limit + 1,
            requested_mb=10,
        )
        self.assertEqual(row["status"], "FAIL")
        self.assertEqual(row["threshold"], contract_limit)

    def test_contrast_floors_match_the_catalog_validator(self):
        """info_stories.validate_catalog enforces these; the contract must agree."""
        contract = load_contract()["thresholds"]
        source = (ROOT / "scripts" / "info_stories.py").read_text()
        self.assertIn(f"< {contract['contrast.text_min_ratio']['value']}", source)
        self.assertIn(f"< {contract['contrast.state_min_ratio']['value']}", source)

    def test_motion_pattern_limit_matches_check_composition(self):
        from scripts.info_stories import check_composition, load_catalog

        limit = int(load_contract()["thresholds"]["motion.max_patterns"]["value"])
        catalog = load_catalog()
        style = catalog["styles"][0]
        too_many = [motion["slug"] for motion in catalog["motions"][: limit + 1]]
        self.assertEqual(limit + 1, len(too_many), "catalog has too few motions to test")
        errors = check_composition(
            catalog, style["slug"], style["archetypes"][0], too_many
        )
        self.assertTrue(
            any("at most two motion patterns" in error.lower() for error in errors),
            f"check_composition did not enforce the {limit}-pattern limit: {errors}",
        )


if __name__ == "__main__":
    unittest.main()
