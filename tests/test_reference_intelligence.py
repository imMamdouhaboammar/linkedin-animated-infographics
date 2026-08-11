import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reference_intelligence.py"
FIXTURES = ROOT / "tests" / "fixtures" / "references"


def load_module():
    spec = importlib.util.spec_from_file_location("reference_intelligence", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_gif(path: Path, size=(7, 3), durations=(20, 120, 340), loop=None):
    frames = []
    for index, color in enumerate(((255, 0, 0, 0), (0, 255, 0, 128), (0, 0, 255, 255))):
        frame = Image.new("RGBA", size, color)
        frame.putpixel((index, index % size[1]), (255, 255, 255, 255))
        frames.append(frame)
    options = {"save_all": True, "append_images": frames[1:], "duration": list(durations)}
    if loop is not None:
        options["loop"] = loop
    frames[0].save(path, format="GIF", transparency=0, disposal=2, **options)


def curated(*sources):
    return {
        "schema_version": 1,
        "references": [
            {
                "id": reference_id,
                "source_filename": filename,
                "observations": [],
                "confidence": "unreviewed",
                "provenance_state": "unverified",
                "rights_state": "unverified",
                "boundaries": {"adopt": [], "adapt": [], "reject": []},
            }
            for reference_id, filename in sources
        ],
    }


class ReferenceIntelligenceTests(unittest.TestCase):
    def test_sha_duplicates_preserve_lowest_legacy_id_and_unmapped_alias(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            library = root / "library"
            library.mkdir()
            for filename in ("first.gif", "legacy-copy.gif", "new-copy.gif"):
                shutil.copy2(FIXTURES / "valid.gif", library / filename)

            manifest = module.ingest_library(
                library,
                root / "state",
                curated(("REF-002", "first.gif"), ("REF-001", "legacy-copy.gif")),
            )

            self.assertEqual(["REF-001"], [row["id"] for row in manifest["references"]])
            self.assertEqual(2, len(manifest["aliases"]))
            legacy = next(row for row in manifest["aliases"] if row.get("id") == "REF-002")
            self.assertEqual("REF-001", legacy["alias_of"])
            self.assertTrue(legacy["deprecated"])
            new_alias = next(row for row in manifest["aliases"] if row["source_filename"] == "new-copy.gif")
            self.assertNotIn("id", new_alias)
            self.assertFalse(new_alias["deprecated"])

    def test_corrupt_input_fails_without_empty_success_manifest(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            library = root / "library"
            library.mkdir()
            shutil.copy2(FIXTURES / "invalid.gif", library / "invalid.gif")

            with self.assertRaisesRegex(module.ReferenceIngestionError, "invalid.gif"):
                module.ingest_library(library, root / "state", curated(("REF-001", "invalid.gif")))

            self.assertFalse((root / "state" / "manifest.json").exists())

    def test_corrupt_existing_manifest_fails_instead_of_hiding_cache_damage(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            library = root / "library"
            library.mkdir()
            shutil.copy2(FIXTURES / "valid.gif", library / "valid.gif")
            state = root / "state"
            state.mkdir()
            (state / "manifest.json").write_text("{")

            with self.assertRaisesRegex(module.ReferenceIngestionError, "invalid cached manifest"):
                module.ingest_library(library, state, curated(("REF-001", "valid.gif")))

    def test_unchanged_sha_reuses_cached_asset_and_frames(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            library = root / "library"
            library.mkdir()
            shutil.copy2(FIXTURES / "valid.gif", library / "valid.gif")
            state = root / "state"
            metadata = curated(("REF-001", "valid.gif"))

            first = module.ingest_library(library, state, metadata)
            cached_paths = [state / first["references"][0]["asset_path"]]
            cached_paths.extend(state / path for path in first["references"][0]["frame_paths"].values())
            mtimes = {path: path.stat().st_mtime_ns for path in cached_paths}
            time.sleep(0.01)
            second = module.ingest_library(library, state, metadata)

            self.assertEqual(first, second)
            self.assertEqual(mtimes, {path: path.stat().st_mtime_ns for path in cached_paths})

    def test_unusual_dimensions_durations_transparency_and_missing_loop_are_measured(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            library = root / "library"
            library.mkdir()
            write_gif(library / "unusual.gif")

            manifest = module.ingest_library(
                library, root / "state", curated(("REF-035", "unusual.gif"))
            )
            reference = manifest["references"][0]

            self.assertEqual([7, 3], reference["dimensions"])
            self.assertEqual(3, reference["frame_count"])
            self.assertEqual(480, reference["duration_ms"])
            self.assertAlmostEqual(6.25, reference["fps"])
            self.assertIsNone(reference["loop"])
            self.assertEqual({"first", "middle", "pre_seam", "final"}, set(reference["frame_paths"]))
            self.assertTrue(any(color["hex"].endswith("00") for color in reference["palette_shares"]))
            for field in ("frame_completeness", "changed_pixel_mean", "seam_ratio"):
                self.assertGreaterEqual(reference[field], 0)
                self.assertLessEqual(reference[field], 1)

    def test_unique_source_without_curated_metadata_fails_clearly(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            library = root / "library"
            library.mkdir()
            shutil.copy2(FIXTURES / "valid.gif", library / "unknown.gif")

            with self.assertRaisesRegex(module.ReferenceIngestionError, "missing curated metadata.*unknown.gif"):
                module.ingest_library(library, root / "state", curated())

    def test_empty_library_fails_clearly(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            library = root / "library"
            library.mkdir()
            with self.assertRaisesRegex(module.ReferenceIngestionError, "no GIF files"):
                module.ingest_library(library, root / "state", curated())

    def test_cli_ingest_then_check_validates_cached_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            library = root / "library"
            library.mkdir()
            shutil.copy2(FIXTURES / "valid.gif", library / "valid.gif")
            curated_path = root / "curated.json"
            curated_path.write_text(json.dumps(curated(("REF-001", "valid.gif"))))
            state = root / "state"

            ingest = subprocess.run(
                [sys.executable, str(SCRIPT), "ingest", "--library", str(library), "--state-dir", str(state), "--curated", str(curated_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            check = subprocess.run(
                [sys.executable, str(SCRIPT), "check", "--state-dir", str(state), "--curated", str(curated_path)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(0, ingest.returncode, ingest.stderr)
            self.assertIn("1 canonical, 0 aliases", ingest.stdout)
            self.assertEqual(0, check.returncode, check.stderr)
            self.assertIn("Reference library: OK", check.stdout)

    def test_load_reference_library_rejects_missing_required_metadata(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "curated.json"
            path.write_text(json.dumps({"schema_version": 1, "references": [{"id": "REF-001"}]}))
            with self.assertRaisesRegex(module.ReferenceIngestionError, "source_filename"):
                module.load_reference_library(path)

    def test_check_rejects_missing_deprecated_legacy_alias(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            library = root / "library"
            library.mkdir()
            for filename in ("canonical.gif", "legacy.gif"):
                shutil.copy2(FIXTURES / "valid.gif", library / filename)
            metadata = curated(("REF-001", "canonical.gif"))
            metadata["aliases"] = [
                {"id": "REF-002", "source_filename": "legacy.gif", "alias_of": "REF-001", "deprecated": True}
            ]
            state = root / "state"
            module.ingest_library(library, state, metadata)
            manifest_path = state / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["aliases"] = []
            manifest_path.write_text(json.dumps(manifest))

            self.assertIn("missing curated IDs: REF-002", module.check_library(state, metadata))


if __name__ == "__main__":
    unittest.main()
