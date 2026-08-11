import json
import hashlib
import base64
import tempfile
import unittest
from pathlib import Path

try:
    from scripts.demo_submit import check_submission, prepare_submission, scan_public_text
except ModuleNotFoundError:
    check_submission = prepare_submission = scan_public_text = None


class DemoSubmitTests(unittest.TestCase):
    REFERENCE_GIF = b"GIF89a-reference-private-payload"

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

    def write_reference_library_for_gif(self, payload=b"GIF89a"):
        path = self.root / "research" / "reference-studies"
        path.mkdir(parents=True, exist_ok=True)
        (path / "visual-library.json").write_text(json.dumps({
            "schema_version": 1,
            "references": [{"id": "REF-001", "sha256": hashlib.sha256(payload).hexdigest()}],
            "aliases": [],
        }))

    def write_canonical_library_state(self, state):
        path = self.root / "research" / "reference-studies" / "visual-library.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        if state == "missing":
            path.unlink(missing_ok=True)
        elif state == "malformed":
            path.write_text("{not-json")
        elif state == "empty":
            path.write_text(json.dumps({"schema_version": 1, "references": [], "aliases": []}))
        else:
            self.write_reference_library_for_gif(b"canonical-reference-that-is-not-demo")

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
        token_like = "gh" + "p_" + "abcdefghijklmnopqrstuvwxyz123456"
        (self.build / "post.html").write_text(f"<script>const token='{token_like}'</script>")
        with self.assertRaisesRegex(ValueError, "public export scan"):
            prepare_submission(self.build, self.stage, self.metadata())

    def test_local_absolute_paths_are_rejected(self):
        self.require_module()
        (self.build / "post.html").write_text('<img src="file:///Users/alice/private.png">')
        with self.assertRaisesRegex(ValueError, "public export scan"):
            prepare_submission(self.build, self.stage, self.metadata())

    def test_reference_source_digest_is_rejected_even_with_rights_confirmation(self):
        self.require_module()
        self.write_reference_library_for_gif()
        with self.assertRaisesRegex(ValueError, "reference source media digest"):
            prepare_submission(self.build, self.stage, self.metadata(), repo_root=self.root)

    def test_embedded_reference_gif_data_uri_is_rejected(self):
        self.require_module()
        self.write_reference_library_for_gif(self.REFERENCE_GIF)
        encoded = base64.b64encode(self.REFERENCE_GIF).decode("ascii")
        (self.build / "post.html").write_text(f'<img src="data:image/gif;base64,{encoded}">')
        with self.assertRaisesRegex(ValueError, "embedded reference source media digest"):
            prepare_submission(self.build, self.stage, self.metadata(), repo_root=self.root)

    def test_malformed_embedded_gif_data_uri_is_rejected(self):
        self.require_module()
        self.write_reference_library_for_gif(b"other-reference")
        (self.build / "post.html").write_text('<img src="data:image/gif;base64,%%%not-base64%%%">')
        with self.assertRaisesRegex(ValueError, "malformed embedded media"):
            prepare_submission(self.build, self.stage, self.metadata(), repo_root=self.root)

    def test_contact_sheet_and_reference_study_paths_are_rejected(self):
        self.require_module()
        cases = (
            '<img src="contact-sheet.png">',
            '<img src=".plugin-state/reference-studies/contact_sheet.png">',
            '<img src="frames/REF-001/frame-0001.png">',
            '<img src="assets/REF-001.gif">',
        )
        for index, html in enumerate(cases):
            with self.subTest(html=html):
                (self.build / "post.html").write_text(html)
                with self.assertRaisesRegex(ValueError, "reference study media"):
                    prepare_submission(self.build, self.stage / str(index), self.metadata())

    def test_posix_and_windows_absolute_media_attributes_are_rejected(self):
        self.require_module()
        cases = ('<img src="/var/tmp/private.png">', '<a href="D:\\work\\private.png">x</a>')
        for index, html in enumerate(cases):
            with self.subTest(html=html):
                (self.build / "post.html").write_text(html)
                with self.assertRaisesRegex(ValueError, "absolute media path"):
                    prepare_submission(self.build, self.stage / str(index), self.metadata())

    def test_unquoted_src_srcset_and_css_absolute_media_are_rejected(self):
        self.require_module()
        cases = (
            '<img src=/var/tmp/private.png>',
            '<a href=/var/tmp/private.html>private</a>',
            '<img srcset="/var/tmp/a.png 1x, /var/tmp/b.png 2x">',
            '<img srcset=/var/tmp/a.png>',
            '<style>.hero{background-image:url(/var/tmp/private.png)}</style>',
            '<style>.hero{background-image:url("/var/tmp/private.png")}</style>',
        )
        for index, html in enumerate(cases):
            with self.subTest(html=html):
                (self.build / "post.html").write_text(html)
                with self.assertRaisesRegex(ValueError, "absolute media path"):
                    prepare_submission(self.build, self.stage / f"media-{index}", self.metadata())

    def test_prepare_fails_closed_without_valid_canonical_digest_authority(self):
        self.require_module()
        for state in ("missing", "malformed", "empty"):
            with self.subTest(state=state):
                self.write_canonical_library_state(state)
                with self.assertRaisesRegex(ValueError, "canonical reference digest authority"):
                    prepare_submission(
                        self.build,
                        self.stage / f"prepare-{state}",
                        self.metadata(),
                        repo_root=self.root,
                    )

    def test_check_fails_closed_without_valid_canonical_digest_authority(self):
        self.require_module()
        for state in ("missing", "malformed", "empty"):
            with self.subTest(state=state):
                self.write_canonical_library_state("valid")
                out = prepare_submission(
                    self.build,
                    self.stage / f"check-{state}",
                    self.metadata(),
                    repo_root=self.root,
                )
                self.write_canonical_library_state(state)
                errors = check_submission(out, self.root)
                self.assertTrue(
                    any("canonical reference digest authority" in error for error in errors),
                    errors,
                )

    def test_prepare_fails_closed_on_malformed_optional_local_digest_authority(self):
        self.require_module()
        self.write_canonical_library_state("valid")
        manifest = self.root / ".plugin-state" / "reference-studies" / "manifest.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text("{not-json")
        with self.assertRaisesRegex(ValueError, "local reference digest authority"):
            prepare_submission(
                self.build,
                self.stage,
                self.metadata(),
                repo_root=self.root,
            )

    def test_plain_route_text_is_not_misclassified_as_absolute_media_path(self):
        self.require_module()
        (self.build / "post.html").write_text("Open /pricing to compare plans.")
        out = prepare_submission(self.build, self.stage, self.metadata())
        self.assertTrue((out / "index.html").is_file())

    def test_unverified_media_rights_record_is_rejected(self):
        self.require_module()
        metadata = self.metadata(media=[{"path": "diagram.svg", "rights_state": "unresolved"}])
        with self.assertRaisesRegex(ValueError, "rights_state"):
            prepare_submission(self.build, self.stage, metadata)

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
