import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import brand_icon  # noqa: E402

MANIFEST = ROOT / "assets" / "brand-icons" / "manifest.json"


class ManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = brand_icon.load_manifest(MANIFEST)

    def test_manifest_pins_a_version_and_records_licence_scope(self):
        self.assertEqual("@lobehub/icons-static-svg", self.manifest["package"])
        self.assertRegex(self.manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual("MIT", self.manifest["license"])
        self.assertIn("trademark", self.manifest["license_scope"].lower())

    def test_url_template_pins_the_version_rather_than_latest(self):
        url = self.manifest["url_template"].format(version=self.manifest["version"], name="claude-color")
        self.assertTrue(url.startswith("https://"))
        self.assertNotIn("@latest", url)
        self.assertIn(self.manifest["version"], url)

    def test_icon_list_is_sorted_and_unique(self):
        icons = self.manifest["icons"]
        self.assertEqual(sorted(icons), icons)
        self.assertEqual(len(icons), len(set(icons)))
        self.assertEqual(self.manifest["icon_count"], len(icons))


class ResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = brand_icon.load_manifest(MANIFEST)

    def test_colour_variant_resolves_when_the_vendor_ships_one(self):
        self.assertEqual("claude-color", brand_icon.resolve_name(self.manifest, "claude", "color"))

    def test_colour_request_falls_back_to_the_vendors_only_mark(self):
        # OpenAI ships a single monochrome mark. Falling back is still that
        # vendor's own artwork, which is the whole point of the exact-SVG rule.
        self.assertEqual("openai", brand_icon.resolve_name(self.manifest, "openai", "color"))

    def test_unknown_slug_reports_nearest_real_choices(self):
        with self.assertRaises(LookupError) as caught:
            brand_icon.resolve_name(self.manifest, "claud", "color")
        self.assertIn("claude", str(caught.exception))

    def test_platform_outside_the_set_fails_as_a_documented_gap(self):
        for slug in ("tiktok", "linkedin", "reddit"):
            with self.assertRaises(LookupError) as caught:
                brand_icon.resolve_name(self.manifest, slug, "color")
            message = str(caught.exception)
            self.assertIn("not in", message)
            self.assertIn("Supply the exact SVG yourself", message)

    def test_brand_variant_finds_a_vendor_that_ships_only_the_plain_brand_file(self):
        self.assertEqual("replicate-brand", brand_icon.resolve_name(self.manifest, "replicate", "brand"))

    def test_brand_variant_prefers_the_colour_brand_file_when_both_exist(self):
        self.assertEqual("google-brand-color", brand_icon.resolve_name(self.manifest, "google", "brand"))

    def test_unknown_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            brand_icon.resolve_name(self.manifest, "claude", "holographic")


class SanitiserTests(unittest.TestCase):
    """A fetched mark is remote input and has to be inert before it is cached."""

    def _reject(self, markup, needle):
        with self.assertRaises(ValueError) as caught:
            brand_icon.sanitise(markup.encode("utf-8"), "probe.svg")
        self.assertIn(needle, str(caught.exception).lower())

    def test_accepts_a_plain_inert_mark(self):
        markup = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="#4285F4"/></svg>'
        self.assertIn("<svg", brand_icon.sanitise(markup.encode("utf-8"), "probe.svg"))

    def test_rejects_embedded_script(self):
        self._reject('<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>', "script")

    def test_rejects_event_handler_attributes(self):
        self._reject('<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"><path d="M0 0"/></svg>', "event handler")

    def test_rejects_remote_references(self):
        self._reject('<svg xmlns="http://www.w3.org/2000/svg"><image href="https://example.com/x.png"/></svg>', "remote")

    def test_rejects_entity_declarations(self):
        markup = '<!DOCTYPE svg [<!ENTITY x SYSTEM "file:///etc/passwd">]><svg xmlns="http://www.w3.org/2000/svg"/>'
        self._reject(markup, "entity")

    def test_rejects_foreign_object(self):
        self._reject('<svg xmlns="http://www.w3.org/2000/svg"><foreignObject><b>x</b></foreignObject></svg>', "foreignobject")

    def test_rejects_a_non_svg_root(self):
        self._reject('<html><body>no</body></html>', "expected svg")

    def test_rejects_a_style_element_outright(self):
        # The mark gets inlined into the artboard, so a stylesheet inside it is a
        # stylesheet in the host document. @import would reach the network too.
        self._reject('<svg xmlns="http://www.w3.org/2000/svg"><style>@import url(https://x.invalid/a.css);</style></svg>', "style")
        self._reject('<svg xmlns="http://www.w3.org/2000/svg"><style>.a{fill:red}</style></svg>', "style")

    def test_rejects_external_url_references_in_any_attribute(self):
        for attribute, value in (("fill", "url(https://x.invalid/a)"),
                                 ("filter", "url(//x.invalid/a)"),
                                 ("mask", "url(http://x.invalid/a)"),
                                 ("clip-path", "url(https://x.invalid/a)")):
            self._reject(
                f'<svg xmlns="http://www.w3.org/2000/svg"><path {attribute}="{value}" d="M0 0"/></svg>',
                "url()",
            )

    def test_allows_a_same_document_fragment_reference(self):
        # Gemini's real mark paints itself with url(#gradient), so this must stay legal.
        markup = ('<svg xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g"/></defs>'
                  '<path fill="url(#g)" d="M0 0"/></svg>')
        self.assertIn("<svg", brand_icon.sanitise(markup.encode("utf-8"), "probe.svg"))

    def test_rejects_an_oversized_payload(self):
        self._reject('<svg xmlns="http://www.w3.org/2000/svg">' + "<path d='M0 0'/>" * 40000 + "</svg>", "ceiling")


class CacheIntegrityTests(unittest.TestCase):
    def test_every_cached_mark_matches_its_recorded_hash(self):
        self.assertEqual([], brand_icon.check(MANIFEST))

    def test_provenance_records_a_pinned_source_for_every_cached_file(self):
        provenance = ROOT / "assets" / "brand-icons" / "provenance.json"
        if not provenance.exists():
            self.skipTest("no marks cached yet")
        doc = json.loads(provenance.read_text())
        manifest = brand_icon.load_manifest(MANIFEST)
        cached = sorted(p.name for p in (ROOT / "assets" / "brand-icons").glob("*.svg"))
        recorded = sorted(Path(a["file"]).name for a in doc["assets"])
        self.assertEqual(cached, recorded, "every cached svg needs a provenance record")
        for asset in doc["assets"]:
            self.assertEqual(manifest["version"], asset["package_version"])
            self.assertIn(manifest["version"], asset["source_url"])
            for field in ("sha256", "license", "license_scope", "trademark", "fetched_on"):
                self.assertTrue(asset.get(field), f"{asset['file']} missing {field}")

    def test_check_flags_a_tampered_cache(self):
        import hashlib
        provenance = ROOT / "assets" / "brand-icons" / "provenance.json"
        if not provenance.exists():
            self.skipTest("no marks cached yet")
        target = ROOT / json.loads(provenance.read_text())["assets"][0]["file"]
        original = target.read_text()
        try:
            target.write_text(original.replace("</svg>", '<path d="M0 0"/></svg>'))
            self.assertTrue(any("sha256" in error for error in brand_icon.check(MANIFEST)))
        finally:
            target.write_text(original)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(),
                         hashlib.sha256(target.read_text().encode()).hexdigest())


class OutPathTests(unittest.TestCase):
    def test_out_outside_the_repository_is_refused(self):
        # check() resolves recorded paths against ROOT, so a target it can never
        # reach would let check pass while the fetched file goes uninspected.
        with self.assertRaises(ValueError) as caught:
            brand_icon.fetch("claude", out="/tmp/escaped-brand-icon.svg")
        self.assertIn("inside the repository", str(caught.exception))


class CliTests(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "tools" / "brand_icon.py"), *args],
                              cwd=ROOT, text=True, capture_output=True)

    def test_list_filters_by_query(self):
        result = self._run("list", "--query", "gemini")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("gemini-color", result.stdout)

    def test_list_reports_the_scope_gap_for_a_non_ai_platform(self):
        result = self._run("list", "--query", "tiktok")
        self.assertEqual(1, result.returncode)
        self.assertIn("AI and LLM brands", result.stderr)

    def test_check_passes_on_the_committed_cache(self):
        result = self._run("check")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("OK", result.stdout)


class ContractTests(unittest.TestCase):
    def test_tool_is_registered_in_the_module_manifest(self):
        modules = json.loads((ROOT / "helper" / "modules.json").read_text())["modules"]["tools"]
        self.assertIn("brand_icon", modules)
        contract = modules["brand_icon"]
        self.assertEqual("tools/brand_icon.py", contract["path"])
        self.assertTrue(contract["tests"])
        self.assertTrue(contract["reachable_from"])

    def test_asset_upstream_is_recorded_outside_the_research_sources(self):
        # research/capability-notes/sources.json records repositories that inform a
        # runtime gate and validates real commit SHAs. This icon set informs no gate;
        # it is an asset source, so its provenance lives with the assets.
        manifest = brand_icon.load_manifest(MANIFEST)
        self.assertIn("lobehub/lobe-icons", manifest["upstream"])
        self.assertEqual("MIT", manifest["license"])
        research = json.loads((ROOT / "research" / "capability-notes" / "sources.json").read_text())
        self.assertNotIn("lobe-icons", [s["name"] for s in research["sources"]])

    def test_documentation_states_the_trademark_boundary(self):
        text = (ROOT / "docs" / "brand-icons.md").read_text().lower()
        self.assertIn("trademark", text)
        self.assertIn("nominative", text)
        self.assertIn("does not carry", text)


if __name__ == "__main__":
    unittest.main()
