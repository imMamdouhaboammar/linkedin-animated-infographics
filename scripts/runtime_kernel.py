#!/usr/bin/env python3
import argparse, hashlib, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path): return json.loads(path.read_text())
def canon(value): return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def sha(value): return hashlib.sha256(canon(value)).hexdigest()

def file_sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""): h.update(chunk)
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
    if not path.exists(): return {"$state": "missing"}
    try: return load(path)
    except json.JSONDecodeError: return {"$state": "invalid"}

def projection(value, view):
    if view.get("mode", "full") != "keys" or not isinstance(value, dict): return value
    picked = {k: value[k] for k in view.get("keys", []) if k in value}
    return value if not picked and view.get("on_empty") == "full" else picked

def artifact_value(path):
    raw = path.read_bytes()
    try: return raw.decode("utf-8")
    except UnicodeDecodeError:
        return {"$binary_sha256": hashlib.sha256(raw).hexdigest(), "$size": len(raw)}

def inputs(stage, workspace, data):
    default = data["views"].get("default", {"mode": "full"})
    stage_views = data["views"].get("stages", {}).get(stage, {})
    result = {}
    for rel, contract in data["artifacts"].items():
        if stage not in contract.get("consumers", []): continue
        path = workspace / rel
        if not path.exists(): value = {"$state": "missing"}
        elif path.suffix == ".json": value = load(path)
        else: value = artifact_value(path)
        result[rel] = projection(value, stage_views.get(rel, default))
    return result

def outputs(stage, data):
    return sorted(rel for rel, c in data["artifacts"].items() if c.get("producer") == stage)

def policy(stage, data):
    configured = data["cache"].get("stages", {}).get(stage, {})
    return bool(configured.get("cacheable", data["cache"].get("default_cacheable", False)))

def effective_cache(stage, req, data):
    if not policy(stage, data): return False, "policy-disabled"
    if req.get("$state") == "missing": return False, "missing-request-record"
    if req.get("$state") == "invalid": return False, "invalid-request-record"
    return True, "exact-request-bound"

def capsule(intent, stage, workspace, data):
    req = request(workspace, data)
    route = data["router"]["routes"].get(intent, {})
    model = data["models"].get("stages", {}).get(stage, data["models"].get("default", {}))
    budget = dict(data["budgets"].get("defaults", {})); budget.update(data["budgets"].get("stages", {}).get(stage, {}))
    gates = {
        "quality": {k:v for k,v in data["quality"].items() if stage in v.get("owners", [])},
        "research": {k:v for k,v in data["research"].items() if stage in v.get("owners", [])},
    }
    cap = {"schema_version":1, "runtime_version":data["runtime"]["runtime_version"], "plugin_version":data["plugin"]["version"],
           "intent":intent, "stage":stage, "request":req, "capabilities":route.get("capabilities", []), "gates":gates,
           "model_policy":model, "budget":budget, "inputs":inputs(stage, workspace, data), "outputs":outputs(stage, data)}
    key = sha({"capsule":cap, "view":data["views"].get("stages", {}).get(stage, {}), "strategy":data["cache"]["strategy"]})
    return cap, key, req

def cache_path(workspace, stage, key, data): return workspace / data["cache"]["storage_root"] / stage / key

def restore(workspace, stage, key, data, enabled):
    manifest_path = cache_path(workspace, stage, key, data) / "manifest.json"
    if not enabled or not manifest_path.exists(): return []
    manifest = load(manifest_path); restored = []
    if manifest.get("cache_key") != key: return []
    for rel, expected in manifest.get("outputs", {}).items():
        source = manifest_path.parent / "files" / rel
        if not source.exists() or file_sha(source) != expected: return []
        target = workspace / rel; target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source, target); restored.append(rel)
    return restored

def prepare(intent, stage, workspace):
    data=regs(); cap,key,req=capsule(intent,stage,workspace,data); enabled,reason=effective_cache(stage,req,data)
    cap["cache_key"]=key; raw=len(canon(cap)); limit=cap["budget"].get("capsule_max_bytes"); cap["budget_status"]="over-soft-budget" if limit and raw>limit else "within-soft-budget"
    target=workspace/data["runtime"]["capsule_root"]/f"{stage}.json"; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(json.dumps(cap,indent=2,ensure_ascii=False)+"\n")
    restored=restore(workspace,stage,key,data,enabled)
    print(json.dumps({"stage":stage,"cacheable":enabled,"cache_reason":reason,"cache_hit":bool(restored),"cache_key":key,"capsule_path":str(target),"restored_outputs":restored,"budget_status":cap["budget_status"]},separators=(",",":")))
    return 0

def store(intent, stage, workspace):
    data=regs(); cap,key,req=capsule(intent,stage,workspace,data); enabled,reason=effective_cache(stage,req,data)
    if not enabled: print(json.dumps({"stage":stage,"stored":False,"reason":reason})); return 0
    entry=cache_path(workspace,stage,key,data); saved={}
    for rel in cap["outputs"]:
        source=workspace/rel
        if not source.exists(): continue
        target=entry/"files"/rel; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(source,target); saved[rel]=file_sha(source)
    if not saved: print(json.dumps({"stage":stage,"stored":False,"reason":"no-output"})); return 2
    entry.mkdir(parents=True,exist_ok=True); (entry/"manifest.json").write_text(json.dumps({"schema_version":1,"cache_key":key,"stage":stage,"request_hash":sha(req),"outputs":saved},indent=2)+"\n")
    print(json.dumps({"stage":stage,"stored":True,"cache_key":key,"outputs":sorted(saved)})); return 0

def check():
    data=regs(); known={c.get("producer") for c in data["artifacts"].values()}; errors=[]
    for name in ("views","cache","models","budgets"):
        errors += [f"unknown {name} stage: {s}" for s in data[name].get("stages",{}) if s not in known]
    errors += [f"fresh acceptance stage cannot be cacheable: {s}" for s in data["runtime"].get("fresh_acceptance_stages",[]) if policy(s,data)]
    if errors:
        print("\n".join("ERROR: "+e for e in errors)); return 1
    print("Runtime kernel: OK"); return 0

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="command",required=True)
    for name in ("prepare","store"):
        c=sub.add_parser(name); c.add_argument("--intent",required=True); c.add_argument("--stage",required=True); c.add_argument("--workspace",default=".")
    sub.add_parser("check"); a=p.parse_args()
    if a.command=="check": return check()
    ws=Path(a.workspace).resolve(); return prepare(a.intent,a.stage,ws) if a.command=="prepare" else store(a.intent,a.stage,ws)

if __name__ == "__main__": raise SystemExit(main())
