#!/usr/bin/env python3
import argparse
import copy
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "masterone-profile.json"
PROFILE_REL = Path(".linkedin-infographics/profile.json")
START = "<!-- MASTERONE:START -->"
END = "<!-- MASTERONE:END -->"
SUPPORTED_INTENTS = (
    "create-post",
    "qa",
    "render",
    "design-study",
    "mascot-animation",
    "info-story",
    "share-demo",
)
SKIP_DIRS = {".git", ".linkedin-infographics", "build", "node_modules", ".venv", "venv", "__pycache__"}


def load_template():
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))


def profile_path(workspace):
    return Path(workspace).resolve() / PROFILE_REL


def read_profile(workspace):
    path = profile_path(workspace)
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def compatible(value, expected):
    if expected is None:
        return value is None or isinstance(value, (str, int, float, bool))
    if isinstance(expected, bool):
        return isinstance(value, bool)
    if isinstance(expected, list):
        return isinstance(value, list) and all(isinstance(item, str) for item in value)
    if isinstance(expected, dict):
        return isinstance(value, dict)
    if isinstance(expected, str):
        return isinstance(value, str)
    if isinstance(expected, (int, float)):
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return True


def validate_shape(payload, template=None, prefix=""):
    template = load_template() if template is None else template
    if not isinstance(payload, dict):
        return ["profile must be an object"]
    errors = []
    unknown = sorted(set(payload) - set(template))
    missing = sorted(set(template) - set(payload))
    errors.extend(f"unknown field: {prefix}{name}" for name in unknown)
    errors.extend(f"missing field: {prefix}{name}" for name in missing)
    for key in sorted(set(payload) & set(template)):
        value, expected = payload[key], template[key]
        dotted = f"{prefix}{key}"
        if isinstance(expected, dict):
            if not isinstance(value, dict):
                errors.append(f"invalid type: {dotted}")
            else:
                errors.extend(validate_shape(value, expected, dotted + "."))
        elif not compatible(value, expected):
            errors.append(f"invalid type: {dotted}")
    if not prefix and payload.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not prefix:
        if payload.get("mascots", {}).get("enabled") not in {"yes", "no", "ask"}:
            errors.append("mascots.enabled must be yes, no, or ask")
        if payload.get("linkedin", {}).get("output_mode") not in {None, "static", "animated"}:
            errors.append("linkedin.output_mode must be static, animated, or null")
        if payload.get("motion", {}).get("default_intensity") not in {"low", "medium", "high"}:
            errors.append("motion.default_intensity must be low, medium, or high")
        if payload.get("visual", {}).get("reference_policy") not in {None, "inspiration", "strict-direction", "ask"}:
            errors.append("visual.reference_policy is invalid")
    return errors


def get_path(payload, dotted):
    current = payload
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted)
        current = current[part]
    return current


def set_path(payload, dotted, value):
    parts = dotted.split(".")
    current = payload
    for part in parts[:-1]:
        if not isinstance(current, dict) or part not in current or not isinstance(current[part], dict):
            raise KeyError(dotted)
        current = current[part]
    leaf = parts[-1]
    if leaf not in current:
        raise KeyError(dotted)
    current[leaf] = value


def deep_merge(base, patch, template, prefix=""):
    if not isinstance(patch, dict):
        raise ValueError(f"{prefix or 'profile'} patch must be an object")
    result = copy.deepcopy(base)
    for key, value in patch.items():
        if key not in template:
            raise KeyError(f"unknown field: {prefix}{key}")
        expected = template[key]
        if isinstance(expected, dict):
            if not isinstance(value, dict):
                raise ValueError(f"invalid type: {prefix}{key}")
            result[key] = deep_merge(result[key], value, expected, f"{prefix}{key}.")
        else:
            if not compatible(value, expected):
                raise ValueError(f"invalid type: {prefix}{key}")
            result[key] = value
    return result


def missing_blockers(profile, intent):
    if intent != "create-post":
        return []
    fields = ["content.default_language", "content.audience", "linkedin.output_mode"]
    if profile.get("copyright", {}).get("footer_required"):
        fields.append("copyright.footer_text")
    missing = []
    for dotted in fields:
        try:
            value = get_path(profile, dotted)
        except KeyError:
            value = None
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(dotted)
    return missing


def status_payload(workspace, intent):
    profile = read_profile(workspace)
    path = profile_path(workspace)
    if profile is None:
        return {
            "profile_state": "HOLD" if intent == "create-post" else "READY",
            "profile_exists": False,
            "intent": intent,
            "missing_blocking_fields": ["content.default_language", "content.audience", "linkedin.output_mode"] if intent == "create-post" else [],
            "profile_path": str(path),
        }
    errors = validate_shape(profile)
    missing = missing_blockers(profile, intent) if not errors else []
    return {
        "profile_state": "READY" if not errors and not missing else "HOLD",
        "profile_exists": True,
        "intent": intent,
        "missing_blocking_fields": missing,
        "validation_errors": errors,
        "profile_path": str(path),
    }


def parse_value(raw):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def managed_section():
    return f"""{START}
## MasterOne project profile

Before LinkedIn infographic production:

1. Read `.linkedin-infographics/profile.json` when present
2. Use `masterone` for first-run onboarding and profile readiness
3. Ask only for materially missing inputs
4. Treat discovered assets as candidates until confirmed
5. Preserve the canonical downstream workflows from `helper/router.json`
6. Never invent copyright, attribution, fonts, official logos, mascot identity, or reference intent

MasterOne manages only this bounded section. `new-post` remains the complete-production parent workflow.
{END}"""


def sync_claude(workspace):
    path = Path(workspace).resolve() / "CLAUDE.md"
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    section = managed_section()
    if START in original and END in original:
        before, rest = original.split(START, 1)
        _, after = rest.split(END, 1)
        updated = before.rstrip() + "\n\n" + section + after
    else:
        updated = original.rstrip() + ("\n\n" if original.strip() else "") + section + "\n"
    if updated != original:
        path.write_text(updated, encoding="utf-8")
    return path


def discover(workspace):
    ws = Path(workspace).resolve()
    result = {
        "logo_candidates": [],
        "mascot_candidates": [],
        "font_candidates": [],
        "reference_candidates": [],
        "advisory_only": True,
    }
    image_ext = {".gif", ".png", ".jpg", ".jpeg", ".webp", ".svg"}
    font_ext = {".ttf", ".otf", ".woff", ".woff2"}
    for path in ws.rglob("*"):
        if not path.is_file():
            continue
        rel_obj = path.relative_to(ws)
        if any(part in SKIP_DIRS for part in rel_obj.parts):
            continue
        rel = rel_obj.as_posix()
        lower = path.name.lower()
        suffix = path.suffix.lower()
        if suffix in font_ext:
            result["font_candidates"].append(rel)
        if suffix in image_ext:
            if "logo" in lower or "brand" in lower:
                result["logo_candidates"].append(rel)
            if "mascot" in lower or "character" in lower:
                result["mascot_candidates"].append(rel)
            if suffix == ".gif" or "reference" in lower or "ref-" in lower or lower.startswith("ref_"):
                result["reference_candidates"].append(rel)
    for key, value in result.items():
        if isinstance(value, list):
            result[key] = sorted(set(value))
    return result


def ensure_profile(workspace):
    path = profile_path(workspace)
    if not path.exists():
        atomic_write_json(path, load_template())
    return path


def build_parser():
    parser = argparse.ArgumentParser(description="Manage MasterOne project onboarding preferences")
    sub = parser.add_subparsers(dest="command", required=True)

    def common(name):
        p = sub.add_parser(name)
        p.add_argument("--workspace", default=".")
        return p

    common("init")
    status = common("status")
    status.add_argument("--intent", choices=SUPPORTED_INTENTS, default="create-post")
    check = common("check")
    check.add_argument("--intent", choices=SUPPORTED_INTENTS, default="create-post")
    setter = common("set")
    setter.add_argument("field")
    setter.add_argument("value")
    merge = common("merge")
    merge.add_argument("--input", required=True)
    common("sync-claude")
    common("discover")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    ws = Path(args.workspace).resolve()
    try:
        if args.command == "init":
            path = ensure_profile(ws)
            print(json.dumps({"profile_path": str(path), "created_or_present": True}))
            return 0
        if args.command in {"status", "check"}:
            payload = status_payload(ws, args.intent)
            print(json.dumps(payload, indent=2))
            return 0 if payload["profile_state"] == "READY" else 2
        if args.command == "set":
            path = ensure_profile(ws)
            current = json.loads(path.read_text(encoding="utf-8"))
            candidate = copy.deepcopy(current)
            set_path(candidate, args.field, parse_value(args.value))
            errors = validate_shape(candidate)
            if errors:
                raise ValueError("; ".join(errors))
            atomic_write_json(path, candidate)
            print(json.dumps({"updated": args.field, "profile_path": str(path)}))
            return 0
        if args.command == "merge":
            path = ensure_profile(ws)
            current = json.loads(path.read_text(encoding="utf-8"))
            patch = json.loads(Path(args.input).read_text(encoding="utf-8"))
            candidate = deep_merge(current, patch, load_template())
            errors = validate_shape(candidate)
            if errors:
                raise ValueError("; ".join(errors))
            atomic_write_json(path, candidate)
            print(json.dumps({"merged": True, "profile_path": str(path)}))
            return 0
        if args.command == "sync-claude":
            path = sync_claude(ws)
            print(json.dumps({"claude_path": str(path), "synced": True}))
            return 0
        if args.command == "discover":
            print(json.dumps(discover(ws), indent=2))
            return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
