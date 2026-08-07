import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    from scripts.demo_gallery import build_catalog, check_repository, validate_demo_dir
except ModuleNotFoundError:
    build_catalog = check_repository = validate_demo_dir = None


class DemoGalleryContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "demos" / "owned").mkdir(parents=True)
        (self.root / "demos" / "community").mkdir(parents=True)
        (self.root / "demos" / "catalog.json").write_text('{"schema_version":1,"demos":[]}\n')

    def tearDown(self):
        self.tmp.cleanup()

    def make_demo(self, relative="demos/community/alice/demo-one", **overrides):
        path = self.root / relative
        path.mkdir(parents=True, exist_ok=True)
        (path / "demo.gif").write_bytes(b"GIF89a")
        (path / "index.html").write_text("<!doctype html><title>Demo</title>")
        data = {
            "schema_version": 1,
            "id": "alice-demo-one",
            "title": "Demo One",
            "author": "alice",
            "author_url": "https://github.com/alice",
            "description": "A demo",
            "created_with": "linkedin-animated-infographics@3.1.0",
            "language": "en",
            "story_type": "comparison",
            "tags": ["comparison"],
            "gif": "demo.gif",
            "html": "index.html",
            "created_at": "2026-08-08",
            "license": "MIT",
            "rights_confirmed": True,
        }
        data.update(overrides)
        (path / "demo.json").write_text(json.dumps(data))
        return path

    def require_module(self):
        self.assertIsNotNone(validate_demo_dir, "scripts.demo_gallery must exist")

    def test_demo_directory_is_exactly_three_public_files(self):
        self.require_module()
        demo = self.make_demo()
        (demo / "notes.txt").write_text("private")
        errors = validate_demo_dir(demo, self.root)
        self.assertTrue(any("exactly demo.gif, index.html, demo.json" in error for error in errors), errors)

    def test_community_author_namespace_must_match(self):
        self.require_module()
        demo = self.make_demo(author="bob")
        errors = validate_demo_dir(demo, self.root)
        self.assertTrue(any("author namespace" in error for error in errors), errors)

    def test_paths_cannot_escape_demo_directory(self):
        self.require_module()
        demo = self.make_demo(gif="../secret.gif")
        errors = validate_demo_dir(demo, self.root)
        self.assertTrue(any("safe local demo path" in error for error in errors), errors)

    def test_rights_confirmation_is_required(self):
        self.require_module()
        demo = self.make_demo(rights_confirmed=False)
        errors = validate_demo_dir(demo, self.root)
        self.assertTrue(any("rights_confirmed must be true" in error for error in errors), errors)

    def test_unknown_metadata_keys_are_rejected(self):
        self.require_module()
        demo = self.make_demo(secret_note="do not ship")
        errors = validate_demo_dir(demo, self.root)
        self.assertTrue(any("unknown demo.json field" in error for error in errors), errors)

    def test_catalog_order_is_deterministic(self):
        self.require_module()
        self.make_demo("demos/community/zeta/z-demo", id="zeta-z-demo", author="zeta", author_url="https://github.com/zeta")
        self.make_demo("demos/community/alice/a-demo", id="alice-a-demo", author="alice", author_url="https://github.com/alice")
        catalog = build_catalog(self.root)
        ids = [item["id"] for item in catalog["demos"]]
        self.assertEqual(sorted(ids), ids)

    def test_check_rejects_catalog_drift(self):
        self.require_module()
        self.make_demo()
        errors = check_repository(self.root)
        self.assertTrue(any("catalog drift" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
