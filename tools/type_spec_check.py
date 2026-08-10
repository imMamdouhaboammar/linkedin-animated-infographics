#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ALLOWED_LOADING_STRATEGIES = {"system", "embedded", "local-file"}
REMOTE_MARKERS = ("@import", "http://", "https://", "remote")


def validate(payload: dict) -> list[str]:
    errors = []
    if not isinstance(payload, dict):
        return ["type spec must be a JSON object"]

    required = (
        "direction_name",
        "headline_family",
        "body_family",
        "loading_strategy",
        "fallbacks",
        "pairing_reason",
        "story_fit",
        "render_safety",
        "status",
    )
    for field in required:
        value = payload.get(field)
        if value in (None, "") or (field == "fallbacks" and not value):
            errors.append(f"{field} is required")

    strategy = payload.get("loading_strategy")
    if strategy not in ALLOWED_LOADING_STRATEGIES:
        errors.append("loading_strategy must be system, embedded, or local-file")

    fallbacks = payload.get("fallbacks")
    if fallbacks is not None and (not isinstance(fallbacks, list) or not all(isinstance(item, str) and item for item in fallbacks)):
        errors.append("fallbacks must be a non-empty array of font family strings")

    safety_text = f"{strategy or ''} {payload.get('render_safety', '')}".lower()
    for marker in REMOTE_MARKERS:
        if marker in safety_text:
            errors.append(f"remote font loading is not render-safe: found {marker}")
            break

    headline = str(payload.get("headline_family", "")).strip().lower()
    body = str(payload.get("body_family", "")).strip().lower()
    if headline and headline == body and not str(payload.get("single_family_reason", "")).strip():
        errors.append("single_family_reason is required when headline and body use the same family")

    if payload.get("status") != "PASS":
        errors.append("status must be PASS before layout production")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate an intentional typography spec")
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2))
        return 1
    errors = validate(payload)
    print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
