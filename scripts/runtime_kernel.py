#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text())


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha(value):
    return hashlib.sha256(canon(value)).hexdigest()


def file_sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def regs():
    return {
        "runtime": load(ROOT / "helper/runtime-contract.json"),
        "views": load(ROOT / "helper/artifact-views.json"),
        "cache": load(ROOT / "helper/cache-policy.json"),
        "models": load(ROOT / "helper/model-policy.json"),
        "budgets": load(ROOT / "helper/token-budgets.json"),
        "artifacts": load(ROOT / "helper/artifacts.json")["artifacts"],
        "router": load(ROOT / "helper/router.json"),
        "quality": load(ROOT / "helper/quality-gates.json")["gates"],
        "research": load(ROOT / "research/capability-notes/gates.json")["gates"],
        "plugin": load(ROOT / ".claude-plugin/plugin.json"),
    }


def request(workspace, data):
    path = workspace / data["runtime"]["capsule_root"] / "request.json"
    if not path.exists():
        return {"$state": "missing"}
    try:
        return load(path)
    except json.JSONDecodeError:
        return {"$state": "invalid"}


def projection(value, view):
    if view.get("mode", "full") != "keys" or not isinstance(value, dict):
        return value
    picked = {key: value[key] for key in view.get("keys", []) if key in value}
    return value if not picked and view.get("on_empty") == "full" else picked


def artifact_value(path):
    if path.suffix == ".json":
        return load(path)
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return {"$binary_sha256": hashlib.sha256(raw).hexdigest(), "$size": len(raw)}


def inputs(stage, workspace, data):
    default = data["views"].get("default", {"mode": "full"})
    views = data["views"].get("stages", {}).get(stage, {})
    result = {}
    for rel, contract in data["artifacts"].items():
        if stage not in contract.get("consumers", []):
            continue
        path = workspace / rel
        value = {"$state": "missing"} if not path.exists() else artifact_value(path)
        result[rel] = projection(value, views.get(rel, default))
    return result


def outputs(stage, data):
    return sorted(rel for rel, contract in data["artifacts"].items() if contract.get("producer") == stage)


def policy(stage, data):
    configured = data["cache"].get("stages", {}).get(stage, {})
    return bool(configured.get("cacheable", data["cache"].get("default_cacheable", False)))


def effective_cache(stage, req, data):
    if not policy(stage, data):
        return False, "policy-disabled"
    state = req.get("$state")
    if state == "missing":
        return False, "missing-request-record"
    if state == "invalid":
        return False, "invalid-request-record"
    return True, "exact-request-bound"


def capsule(intent, stage, workspace, data):
    req = request(workspace, data)
    model = data["models"].get("stages", {}).get(stage, data["models"].get("default", {}))
    budget = dict(data["budgets"].get("defaults", {}))
    budget.update(data["budgets"].get("stages", {}).get(stage, {}))
    cap = {
        "schema_version": 1,
        "runtime_version": data["runtime"]["runtime_version"],
        "plugin_version": data["plugin"]["version"],
        "intent": intent,
        "stage": stage,
        "request": req,
        "capabilities": data["router"]["routes"].get(intent, {}).get("capabilities", []),
        "gates": {
            "quality": {k: v for k, v in data["quality"].items() if stage in v.get("owners", [])},
            "research": {k: v for k, v in data["research"].items() if stage in v.get("owners", [])},
        },
        "model_policy": model,
        "budget": budget,
        "inputs": inputs(stage, workspace, data),
        "outputs": outputs(stage, data),
    }
    key = sha({"capsule": cap, "view": data["views"].get("stages", {}).get(stage, {}), "strategy": data["cache"]["strategy"]})
    return cap, key, req


def cache_path(workspace, stage, key, data):
    return workspace / data["cache"]["storage_root"] / stage / key


def restore(workspace, stage, key, data, enabled):
    manifest_path = cache_path(workspace, stage, key, data) / "manifest.json"
    if not enabled or not manifest_path.exists():
        return []
    manifest = load(manifest_path)
    if manifest.get("cache_key") != key:
        return []
    restored = []
    for rel, expected in manifest.get("outputs", {}).items():
        source = manifest_path.parent / "files" / rel
        if not source.exists() or file_sha(source) != expected:
            return []
        target = workspace / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        restored.append(rel)
    return restored


def prepare(intent, stage, workspace):
    data = regs()
    cap, key, req = capsule(intent, stage, workspace, data)
    enabled, reason = effective_cache(stage, req, data)
    cap["cache_key"] = key
    limit = cap["budget"].get("capsule_max_bytes")
    cap["budget_status"] = "over-soft-budget" if limit and len(canon(cap)) > limit else "within-soft-budget"
    target = workspace / data["runtime"]["capsule_root"] / f"{stage}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(cap, indent=2, ensure_ascii=False) + "\n")
    restored = restore(workspace, stage, key, data, enabled)
    print(json.dumps({"stage": stage, "cacheable": enabled, "cache_reason": reason, "cache_hit": bool(restored), "cache_key": key, "capsule_path": str(target), "restored_outputs": restored, "budget_status": cap["budget_status"]}, separators=(",", ":")))
    return 0


def store(intent, stage, workspace):
    data = regs()
    cap, key, req = capsule(intent, stage, workspace, data)
    enabled, reason = effective_cache(stage, req, data)
    if not enabled:
        print(json.dumps({"stage": stage, "stored": False, "reason": reason}))
        return 0
    entry = cache_path(workspace, stage, key, data)
    saved = {}
    for rel in cap["outputs"]:
        source = workspace / rel
        if not source.exists():
            continue
        target = entry / "files" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        saved[rel] = file_sha(source)
    if not saved:
        print(json.dumps({"stage": stage, "stored": False, "reason": "no-output"}))
        return 2
    entry.mkdir(parents=True, exist_ok=True)
    (entry / "manifest.json").write_text(json.dumps({"schema_version": 1, "cache_key": key, "stage": stage, "request_hash": sha(req), "outputs": saved}, indent=2) + "\n")
    print(json.dumps({"stage": stage, "stored": True, "cache_key": key, "outputs": sorted(saved)}))
    return 0


def check():
    data = regs()
    known = {contract.get("producer") for contract in data["artifacts"].values()}
    errors = []
    for name in ("views", "cache", "models", "budgets"):
        errors.extend(f"unknown {name} stage: {stage}" for stage in data[name].get("stages", {}) if stage not in known)
    errors.extend(f"fresh acceptance stage cannot be cacheable: {stage}" for stage in data["runtime"].get("fresh_acceptance_stages", []) if policy(stage, data))
    if errors:
        print("\n".join("ERROR: " + error for error in errors))
        return 1
    print("Runtime kernel: OK")
    return 0


def main():
    parser = argparse.ArgumentParser()
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
