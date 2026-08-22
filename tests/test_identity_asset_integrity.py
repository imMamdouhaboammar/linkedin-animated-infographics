import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_TOOL = ROOT / "tools" / "asset_policy_check.py"
CANONICAL_POLICY = ROOT / "skills" / "info-stories" / "references" / "asset-source-policy.md"
OPENAI_POLICY = ROOT / "openai-skills" / "linkedin-infographic-studio" / "references" / "asset-source-policy.md"
MASCOT_SKILL = ROOT / "skills" / "mascots" / "SKILL.md"
VIBE_REPO = "imMamdouhaboammar/vibe-svgs"
VIBE_URL = "https://github.com/imMamdouhaboammar/vibe-svgs"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def base_asset(**overrides):
    payload = {
        "name": "OpenAI Codex",
        "kind": "brand-logo",
        "source_type": "vibe-svgs-logo",
        "source_ref": "https://github.com/imMamdouhaboammar/vibe-svgs/blob/13153ef2679562ecc9297f4fd520881d816b85e6/svgs/logos/codex-color.svg",
        "source_repo": VIBE_REPO,
        "source_commit": "13153ef2679562ecc9297f4fd520881d816b85e6",
        "source_path": "svgs/logos/codex-color.svg",
        "source_blob_sha": "a" * 40,
        "integrity_sha256": "b" * 64,
        "identity_status": "supplied-third-party-mark",
        "render_disposition": "local",
        "local_path": "build/assets/codex-color.svg",
        "identity_locked": True,
        "alteration_policy": "placement-only",
        "status": "PASS",
    }
    payload.update(overrides)
    return payload


class IdentityAssetIntegrityTests(unittest.TestCase):
    def test_policy_names_vibe_svgs_and_original_source_precedence(self):
        for path in (CANONICAL_POLICY, OPENAI_POLICY):
            text = path.read_text(encoding="utf-8")
            self.assertIn(VIBE_URL, text)
            self.assertIn("original-owner", text.lower())
            self.assertIn("pinned", text.lower())
            self.assertIn("integrity", text.lower())
            self.assertIn("identity-locked", text.lower())
            self.assertIn("communityArtwork", text)
            self.assertIn("must not be called official", text)

    def test_validator_accepts_pinned_vibe_svg_logo_mirror(self):
        module = load_module(ASSET_TOOL, "asset_policy_check_vibe_logo")
        self.assertEqual([], module.validate({"assets": [base_asset()]}))

    def test_validator_rejects_unpinned_or_mutable_vibe_logo_source(self):
        module = load_module(ASSET_TOOL, "asset_policy_check_vibe_unpinned")
        payload = base_asset(
            source_ref="https://raw.githubusercontent.com/imMamdouhaboammar/vibe-svgs/main/svgs/logos/codex-color.svg",
            source_commit="main",
            source_blob_sha="",
            integrity_sha256="",
        )
        errors = module.validate({"assets": [payload]})
        self.assertTrue(any("source_commit" in error for error in errors), errors)
        self.assertTrue(any("source_blob_sha" in error for error in errors), errors)
        self.assertTrue(any("integrity_sha256" in error for error in errors), errors)
        self.assertTrue(any("immutable" in error.lower() or "commit" in error.lower() for error in errors), errors)

    def test_vibe_community_mascot_cannot_claim_official_identity(self):
        module = load_module(ASSET_TOOL, "asset_policy_check_vibe_mascot")
        payload = base_asset(
            name="Claude",
            kind="mascot",
            source_type="vibe-svgs-community",
            source_path="svgs/mascots/claude-mascot.svg",
            source_ref="https://github.com/imMamdouhaboammar/vibe-svgs/blob/13153ef2679562ecc9297f4fd520881d816b85e6/svgs/mascots/claude-mascot.svg",
            identity_status="official-mascot",
            community_artwork=True,
            user_confirmed=True,
        )
        errors = module.validate({"assets": [payload]})
        self.assertTrue(any("community" in error.lower() and "official" in error.lower() for error in errors), errors)

    def test_vibe_community_mascot_requires_explicit_user_confirmation(self):
        module = load_module(ASSET_TOOL, "asset_policy_check_vibe_community")
        valid = base_asset(
            name="Claude community mascot",
            kind="mascot",
            source_type="vibe-svgs-community",
            source_path="svgs/mascots/claude-mascot.svg",
            source_ref="https://github.com/imMamdouhaboammar/vibe-svgs/blob/13153ef2679562ecc9297f4fd520881d816b85e6/svgs/mascots/claude-mascot.svg",
            identity_status="community-artwork",
            community_artwork=True,
            user_confirmed=True,
        )
        self.assertEqual([], module.validate({"assets": [valid]}))
        invalid = dict(valid, user_confirmed=False)
        errors = module.validate({"assets": [invalid]})
        self.assertTrue(any("user_confirmed" in error for error in errors), errors)

    def test_mascot_contract_forbids_using_vibe_community_art_as_official(self):
        text = MASCOT_SKILL.read_text(encoding="utf-8")
        self.assertIn(VIBE_URL, text)
        self.assertIn("communityArtwork", text)
        self.assertIn("HOLD", text)
        self.assertIn("official", text.lower())
        self.assertIn("identity geometry", text.lower())
        self.assertIn("identity colors", text.lower())


if __name__ == "__main__":
    unittest.main()
