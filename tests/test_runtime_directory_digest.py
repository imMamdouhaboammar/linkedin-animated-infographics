import tempfile
import unittest
from pathlib import Path

from scripts.runtime_directory_digest import directory_descriptor


class RuntimeDirectoryDigestTests(unittest.TestCase):
    def test_rejects_symlinked_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "package"
            target = root / "outside"
            package.mkdir()
            target.mkdir()
            (target / "secret.txt").write_text("outside")
            link = package / "linked-dir"
            try:
                link.symlink_to(target, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"symlinks unavailable: {exc}")

            with self.assertRaisesRegex(ValueError, "symlink"):
                directory_descriptor(package)


if __name__ == "__main__":
    unittest.main()
