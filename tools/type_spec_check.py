#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ALLOWED_LOADING_STRATEGIES = {"system", "embedded", "local-file"}
REMOTE_MARKERS = ("@import", "http://", "https://", "remote")
STRING_FIELDS = (
    "direction_name",
    "headline_family",
    "body_family",
    "loading_strategy",
    "pairing_reason",
    "story_fit",
    "render_safety",
    "status",
)


def _nonempty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(payload: dict) -> list[str]:
    errors = []
    if not isinstance(payload, dict):
        return ["type spec must be a JSON object"]

    for field in STRING_FIELDS:
        if not _nonempty_string(payload.get(field)):
            errors.append(f"{field} must be a non-empty string")

    strategy = payload.get("loading_strategy")
    if not isinstance(strategy, str) or strategy not in ALLOWED_LOADING_STRATEGIES:
        errors.append("loading_strategy must be system, embedded, or local-file")

    fallbacks = payload.get("fallbacks")
    if not isinstance(fallbacks, list) or not fallbacks or not all(_nonempty_string(item) for item in fallbacks):
        errors.append("fallbacks must be a non-empty array of font family strings")

    render_safety = payload.get("render_safety")
    safety_text = " ".join(
        value.lower()
        for value in (strategy, render_safety)
        if isinstance(value, str)
    )
    for marker in REMOTE_MARKERS:
        if marker in safety_text:
            errors.append(f"remote font loading is not render-safe: found {marker}")
            break

    headline = payload.get("headline_family")
    body = payload.get("body_family")
    if isinstance(headline, str) and isinstance(body, str):
        if headline.strip() and headline.strip().lower() == body.strip().lower():
            if not _nonempty_string(payload.get("single_family_reason")):
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
