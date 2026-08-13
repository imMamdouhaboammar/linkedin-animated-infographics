import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "runtime_context.py"


class RuntimeDirectoryArtifactTests(unittest.TestCase):
    def test_community_publisher_hashes_directory_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            build = workspace / "build"
            context = build / "runtime-context"
            package = build / "community-demo-package"
            context.mkdir(parents=True)
            package.mkdir(parents=True)
            (context / "request.json").write_text(json.dumps({"topic": "demo"}))
            (package / "demo.json").write_text("{}")
            (package / "index.html").write_text("<main>demo</main>")

            first = subprocess.run(
                [sys.executable, str(RUNTIME), "prepare", "--intent", "share-demo", "--stage", "community-publisher", "--workspace", str(workspace)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(0, first.returncode, first.stderr)
            first_response = json.loads(first.stdout)
            capsule = json.loads(Path(first_response["capsule_path"]).read_text())
            value = capsule["inputs"]["build/community-demo-package"]
            self.assertEqual(2, value["$files"])
            self.assertEqual(64, len(value["$directory_sha256"]))

            (package / "index.html").write_text("<main>changed</main>")
            second = subprocess.run(
                [sys.executable, str(RUNTIME), "prepare", "--intent", "share-demo", "--stage", "community-publisher", "--workspace", str(workspace)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertNotEqual(first_response["cache_key"], json.loads(second.stdout)["cache_key"])


if __name__ == "__main__":
    unittest.main()
