#!/usr/bin/env python3
import json
from pathlib import Path


_DIRECTIONS = [
    {"slug":"guide-the-eye","purpose":"Use the mascot as the single reading pointer across ordered content.","communication_job":"reading sequence","allowed_parts":["whole body","eyes","one arm if addressable"],"loop_behavior":"return through an invisible or quiet reset","motion_budget":"one travelling mascot; replace any abstract pointer"},
    {"slug":"curious-peek","purpose":"Let the mascot briefly inspect a card edge or panel before attention moves there.","communication_job":"focus cue","allowed_parts":["whole body","eyes","head if addressable"],"loop_behavior":"peek, settle, reset during a quiet beat","motion_budget":"small local motion around one panel"},
    {"slug":"inspect-and-react","purpose":"Inspect one result, then give a restrained reaction tied to that state.","communication_job":"state confirmation","allowed_parts":["eyes","head","whole body scale"],"loop_behavior":"inspect, react once, return to neutral","motion_budget":"one reaction beat"},
    {"slug":"carry-and-place","purpose":"Carry a small support object from input to destination to explain movement of information.","communication_job":"transfer","allowed_parts":["whole body","arms if addressable","support object"],"loop_behavior":"pickup, travel, place, quiet reset","motion_budget":"one support object plus mascot"},
    {"slug":"reveal-assistant","purpose":"Use the mascot to uncover or point to one hidden annotation without hiding required frame-zero content.","communication_job":"hierarchy","allowed_parts":["whole body","one arm if addressable","support curtain/card"],"loop_behavior":"gesture, reveal emphasis, return","motion_budget":"local reveal only"},
    {"slug":"status-confirmation","purpose":"Give a compact nod, bounce, or check reaction when a process reaches a valid state.","communication_job":"status change","allowed_parts":["whole body","head if addressable"],"loop_behavior":"single confirmation beat with long rest","motion_budget":"one small reaction"},
    {"slug":"route-follow","purpose":"Follow an existing connector path so the character explains direction rather than decorating it.","communication_job":"route direction","allowed_parts":["whole body","contact shadow"],"loop_behavior":"travel route, reset off emphasis beat","motion_budget":"one route traveller"},
    {"slug":"card-to-card-handoff","purpose":"Move attention from one card to the next using a brief handoff gesture or body shift.","communication_job":"reading handoff","allowed_parts":["whole body","arms if addressable","eyes"],"loop_behavior":"handoff across two or three stops, then reset","motion_budget":"one active handoff at a time"},
    {"slug":"calm-idle-breathing","purpose":"Keep a mascot alive in a footer or quiet panel without competing with the story.","communication_job":"ambient presence","allowed_parts":["whole body scale","eyes"],"loop_behavior":"slow low-amplitude idle","motion_budget":"3px target, 4px hard cap"},
    {"slug":"contextual-micro-reaction","purpose":"React to a nearby highlighted state with one context-specific micro motion.","communication_job":"local confirmation","allowed_parts":["eyes","head if addressable","whole body"],"loop_behavior":"short reaction followed by long neutral hold","motion_budget":"secondary motion only"}
]

VERIFIED_SOURCES = {"user-supplied", "task-attached", "lobe"}


def creative_directions():
    return [dict(item) for item in _DIRECTIONS]


def validate_mascot_request(request: dict) -> list[str]:
    errors = []
    requested_name = str(request.get("requested_name") or "").strip()
    source = request.get("source")
    svg_path = request.get("svg_path")
    if request.get("allow_substitute"):
        errors.append("Mascot substitution is not allowed for a requested official or named mascot.")
    if requested_name and source not in VERIFIED_SOURCES:
        errors.append("An exact verified SVG is required for a requested official or named mascot.")
    if requested_name and not svg_path:
        errors.append("The exact mascot SVG path is required before animation can begin.")
    if source == "lobe" and not str(request.get("source_ref") or "").strip():
        errors.append("A Lobe mascot request must include its exact source_ref provenance.")
    if svg_path:
        path = Path(svg_path)
        if path.suffix.lower() != ".svg":
            errors.append("Mascot source must be an SVG file.")
        elif source in VERIFIED_SOURCES and not path.exists():
            errors.append("The verified mascot SVG path does not exist.")
    return errors


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description="Validate verified-SVG mascot requests or list creative directions")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check")
    check.add_argument("request", type=Path)
    sub.add_parser("directions")
    args = parser.parse_args(argv)
    if args.command == "directions":
        print(json.dumps(creative_directions(), indent=2))
        return 0
    request = json.loads(args.request.read_text())
    errors = validate_mascot_request(request)
    print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
