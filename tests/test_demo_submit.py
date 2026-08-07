import json
import tempfile
import unittest
from pathlib import Path

try:
    from scripts.demo_submit import prepare_submission, scan_public_text
except ModuleNotFoundError:
    prepare_submission = scan_public_text = None


class DemoSubmitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.build = self.root / "build"
        self.stage = self.root / "stage"
        self.build.mkdir()
        (self.build / "post.html").write_text("<!doctype html><title>Safe demo</title>")
        (self.build / "post.gif").write_bytes(b"GIF89a")
        self.write_verification("PASS")

    def tearDown(self):
        self.tmp.cleanup()

    def write_verification(self, verdict):
        (self.build / "verification-report.json").write_text(json.dumps({"verdict": verdict}))

    def metadata(self, **overrides):
        data = {
            "slug": "demo-one",
            "id": "alice-demo-one",
            "title": "Demo One",
            "author": "alice",
            "author_url": "https://github.com/alice",
            "description": "A safe public demo",
            "created_with": "linkedin-animated-infographics@3.1.0",
            "language": "en",
            "story_type": "comparison",
            "tags": ["comparison"],
            "created_at": "2026-08-08",
            "license": "MIT",
            "rights_confirmed": True,
        }
        data.update(overrides)
        return data

    def require_module(self):
        self.assertIsNotNone(prepare_submission, "scripts.demo_submit must exist")

    def test_prepare_requires_verification_pass(self):
        self.require_module()
        self.write_verification("FAIL:fixable")
        with self.assertRaisesRegex(ValueError, "verification PASS"):
            prepare_submission(self.build, self.stage, self.metadata())

    def test_prepare_requires_rights_confirmation(self):
        self.require_module()
        with self.assertRaisesRegex(ValueError, "rights confirmation"):
            prepare_submission(self.build, self.stage, self.metadata(rights_confirmed=False))

    def test_prepare_requires_author_url_to_match_author(self):
        self.require_module()
        with self.assertRaisesRegex(ValueError, "author_url must match author"):
            prepare_submission(self.build, self.stage, self.metadata(author_url="https://github.com/bob"))

    def test_source_prompt_is_omitted_without_explicit_consent(self):
        self.require_module()
        out = prepare_submission(
            self.build,
            self.stage,
            self.metadata(source_prompt="private prompt", publish_source_prompt=False),
        )
        manifest = json.loads((out / "demo.json").read_text())
        self.assertNotIn("source_prompt", manifest)

    def test_source_prompt_is_included_only_with_explicit_consent(self):
        self.require_module()
        out = prepare_submission(
            self.build,
            self.stage,
            self.metadata(source_prompt="public prompt", publish_source_prompt=True),
        )
        manifest = json.loads((out / "demo.json").read_text())
        self.assertEqual("public prompt", manifest["source_prompt"])

    def test_prepare_copies_only_public_three_file_package(self):
        self.require_module()
        (self.build / "evidence.json").write_text('{"private":true}')
        out = prepare_submission(self.build, self.stage, self.metadata())
        self.assertEqual({"demo.gif", "index.html", "demo.json"}, {p.name for p in out.iterdir()})

    def test_prepare_rejects_existing_destination(self):
        self.require_module()
        destination = self.stage / "community" / "alice" / "demo-one"
        destination.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "already exists"):
            prepare_submission(self.build, self.stage, self.metadata())

    def test_secret_markers_are_rejected(self):
        self.require_module()
        (self.build / "post.html").write_text("<script>const token='ghp_abcdefghijklmnopqrstuvwxyz123456'</script>")
        with self.assertRaisesRegex(ValueError, "public export scan"):
            prepare_submission(self.build, self.stage, self.metadata())

    def test_local_absolute_paths_are_rejected(self):
        self.require_module()
        (self.build / "post.html").write_text('<img src="file:///Users/alice/private.png">')
        with self.assertRaisesRegex(ValueError, "public export scan"):
            prepare_submission(self.build, self.stage, self.metadata())

    def test_signed_urls_are_rejected(self):
        self.require_module()
        (self.build / "post.html").write_text('<img src="https://example.com/a.png?X-Amz-Signature=secret">')
        with self.assertRaisesRegex(ValueError, "public export scan"):
            prepare_submission(self.build, self.stage, self.metadata())

    def test_remote_script_requires_maintainer_review(self):
        self.require_module()
        (self.build / "post.html").write_text('<script src="https://cdn.example.com/lib.js"></script>')
        with self.assertRaisesRegex(ValueError, "remote executable resource"):
            prepare_submission(self.build, self.stage, self.metadata())

    def test_protocol_relative_remote_script_requires_maintainer_review(self):
        self.require_module()
        (self.build / "post.html").write_text('<script src="//cdn.example.com/lib.js"></script>')
        with self.assertRaisesRegex(ValueError, "remote executable resource"):
            prepare_submission(self.build, self.stage, self.metadata())

    def test_scan_public_text_returns_named_findings(self):
        self.require_module()
        findings = scan_public_text("demo", "Authorization: Bearer abcdefghijklmnopqrstuvwxyz")
        self.assertTrue(any("bearer credential" in item for item in findings), findings)


if __name__ == "__main__":
    unittest.main()
