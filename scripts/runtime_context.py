#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    return json.loads(path.read_text())


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def project(value, view):
    if view.get("mode", "full") != "keys" or not isinstance(value, dict):
        return value
    selected = {key: value[key] for key in view.get("keys", []) if key in value}
    if not selected and view.get("on_empty") == "full":
        return value
    return selected


def read_artifact(path: Path, view):
    if not path.exists():
        return {"$state": "missing"}
    if path.suffix == ".json":
        return project(load_json(path), view)
    return path.read_text()


def contracts(root: Path):
    return {
        "runtime": load_json(root / "helper/runtime-contract.json"),
        "views": load_json(root / "helper/artifact-views.json"),
        "cache": load_json(root / "helper/cache-policy.json"),
        "models": load_json(root / "helper/model-policy.json"),
        "budgets": load_json(root / "helper/token-budgets.json"),
        "artifacts": load_json(root / "helper/artifacts.json")["artifacts"],
        "router": load_json(root / "helper/router.json"),
        "quality": load_json(root / "helper/quality-gates.json")["gates"],
        "research": load_json(root / "research/capability-notes/gates.json")["gates"],
        "plugin": load_json(root / ".claude-plugin/plugin.json"),
    }


def stage_inputs(stage: str, workspace: Path, data):
    defaults = data["views"].get("default", {"mode": "full"})
    views = data["views"].get("stages", {}).get(stage, {})
    result = {}
    for relative, contract in data["artifacts"].items():
        if stage not in contract.get("consumers", []):
            continue
        result[relative] = read_artifact(workspace / relative, views.get(relative, defaults))
    return result


def stage_outputs(stage: str, data):
    return sorted(
        relative for relative, contract in data["artifacts"].items()
        if contract.get("producer") == stage
    )


def stage_gates(stage: str, data):
    return {
        "quality": {key: gate for key, gate in data["quality"].items() if stage in gate.get("owners", [])},
        "research": {key: gate for key, gate in data["research"].items() if stage in gate.get("owners", [])},
    }


def stage_policy(stage: str, registry, default):
    return registry.get("stages", {}).get(stage, default)


def cacheable(stage: str, data) -> bool:
    default = data["cache"].get("default_cacheable", False)
    return bool(stage_policy(stage, data["cache"], {"cacheable": default}).get("cacheable", default))


def build_capsule(intent: str, stage: str, workspace: Path, data):
    route = data["router"]["routes"].get(intent, {})
    model = stage_policy(stage, data["models"], data["models"].get("default", {}))
    budget = dict(data["budgets"].get("defaults", {}))
    budget.update(data["budgets"].get("stages", {}).get(stage, {}))
    capsule = {
        "schema_version": 1,
        "runtime_version": data["runtime"]["runtime_version"],
        "plugin_version": data["plugin"]["version"],
        "intent": intent,
        "stage": stage,
        "capabilities": route.get("capabilities", []),
        "gates": stage_gates(stage, data),
        "model_policy": model,
        "budget": budget,
        "inputs": stage_inputs(stage, workspace, data),
        "outputs": stage_outputs(stage, data),
    }
    key_material = dict(capsule)
    key_material["artifact_view"] = data["views"].get("stages", {}).get(stage, {})
    key_material["cache_strategy"] = data["cache"].get("strategy")
    return capsule, digest(key_material)


def cache_dir(workspace: Path, stage: str, key: str, data):
    root = data["cache"].get("storage_root", ".plugin-state/runtime-cache/")
    return workspace / root / stage / key


def restore(workspace: Path, stage: str, key: str, data):
    if not cacheable(stage, data):
        return []
    entry = cache_dir(workspace, stage, key, data)
    manifest_path = entry / "manifest.json"
    if not manifest_path.exists():
        return []
    manifest = load_json(manifest_path)
    if manifest.get("cache_key") != key:
        return []
    restored = []
    for relative, expected in manifest.get("outputs", {}).items():
        source = entry / "files" / relative
        if not source.exists() or file_digest(source) != expected:
            return []
        target = workspace / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        restored.append(relative)
    return restored


def prepare(intent: str, stage: str, workspace: Path):
    data = contracts(ROOT)
    capsule, key = build_capsule(intent, stage, workspace, data)
    capsule["cache_key"] = key
    raw_size = len(canonical(capsule))
    limit = capsule["budget"].get("capsule_max_bytes")
    capsule["budget_status"] = "over-soft-budget" if limit and raw_size > limit else "within-soft-budget"
    target = workspace / data["runtime"]["capsule_root"] / f"{stage}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(capsule, indent=2, ensure_ascii=False) + "\n")
    session = workspace / data["runtime"]["session_file"]
    session.write_text(json.dumps({"intent": intent, "stage": stage, "capsule_path": str(target), "cache_key": key}) + "\n")
    restored = restore(workspace, stage, key, data)
    result = {
        "stage": stage,
        "cacheable": cacheable(stage, data),
        "cache_hit": bool(restored),
        "cache_key": key,
        "capsule_path": str(target),
        "restored_outputs": restored,
        "budget_status": capsule["budget_status"],
    }
    print(json.dumps(result, separators=(",", ":")))
    return 0


def store(intent: str, stage: str, workspace: Path):
    data = contracts(ROOT)
    capsule, key = build_capsule(intent, stage, workspace, data)
    if not cacheable(stage, data):
        print(json.dumps({"stage": stage, "stored": False, "reason": "not-cacheable"}, separators=(",", ":")))
        return 0
    outputs = {}
    entry = cache_dir(workspace, stage, key, data)
    files = entry / "files"
    for relative in capsule["outputs"]:
        source = workspace / relative
        if not source.exists():
            continue
        target = files / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        outputs[relative] = file_digest(source)
    if not outputs:
        print(json.dumps({"stage": stage, "stored": False, "reason": "no-output"}, separators=(",", ":")))
        return 2
    entry.mkdir(parents=True, exist_ok=True)
    (entry / "manifest.json").write_text(json.dumps({"schema_version": 1, "cache_key": key, "stage": stage, "plugin_version": data["plugin"]["version"], "outputs": outputs}, indent=2) + "\n")
    print(json.dumps({"stage": stage, "stored": True, "cache_key": key, "outputs": sorted(outputs)}, separators=(",", ":")))
    return 0


def check():
    data = contracts(ROOT)
    known = set(data["artifacts"][path].get("producer") for path in data["artifacts"])
    errors = []
    for stage in data["views"].get("stages", {}):
        if stage not in known:
            errors.append(f"unknown artifact-view stage: {stage}")
    for stage in data["cache"].get("stages", {}):
        if stage not in known:
            errors.append(f"unknown cache-policy stage: {stage}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Runtime context: OK")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Compile stage context and manage exact local runtime cache entries.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("prepare", "store"):
        command = sub.add_parser(name)
        command.add_argument("--intent", required=True)
        command.add_argument("--stage", required=True)
        command.add_argument("--workspace", default=".")
    sub.add_parser("check")
    args = parser.parse_args()
    if args.command == "check":
        return check()
    workspace = Path(args.workspace).resolve()
    return prepare(args.intent, args.stage, workspace) if args.command == "prepare" else store(args.intent, args.stage, workspace)


if __name__ == "__main__":
    raise SystemExit(main())
