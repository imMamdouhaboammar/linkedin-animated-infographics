import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "runtime_context.py"


class RuntimeBinaryArtifactTests(unittest.TestCase):
    def test_motion_context_hashes_binary_still_instead_of_decoding_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            build = workspace / "build"
            context = build / "runtime-context"
            context.mkdir(parents=True)
            (context / "request.json").write_text(json.dumps({
                "topic": "Binary-safe runtime",
                "audience": "designers",
                "language": "en",
                "output_mode": "animated",
            }))
            (build / "creative-concepts.json").write_text("{}")
            (build / "story-brief.json").write_text("{}")
            (build / "layout-spec.json").write_text("{}")
            first_bytes = b"\x89PNG\r\n\x1a\n\xff\xfe\x00valid-binary-fixture"
            (build / "still.png").write_bytes(first_bytes)

            first = subprocess.run(
                [sys.executable, str(RUNTIME), "prepare", "--intent", "create-post", "--stage", "motion-director", "--workspace", str(workspace)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, first.returncode, first.stderr)
            first_response = json.loads(first.stdout)
            capsule = json.loads(Path(first_response["capsule_path"]).read_text())
            still = capsule["inputs"]["build/still.png"]
            self.assertEqual(len(first_bytes), still["$size"])
            self.assertEqual(hashlib.sha256(first_bytes).hexdigest(), still["$binary_sha256"])

            (build / "still.png").write_bytes(first_bytes + b"changed")
            second = subprocess.run(
                [sys.executable, str(RUNTIME), "prepare", "--intent", "create-post", "--stage", "motion-director", "--workspace", str(workspace)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertNotEqual(first_response["cache_key"], json.loads(second.stdout)["cache_key"])


if __name__ == "__main__":
    unittest.main()
