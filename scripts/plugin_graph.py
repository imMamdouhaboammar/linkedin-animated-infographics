#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}
    _, frontmatter, _ = text.split("---", 2)
    data = {}
    current_list = None
    for raw in frontmatter.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_list:
            data[current_list].append(line[4:].strip())
            continue
        current_list = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if value:
            data[key] = value.strip('"\'')
        else:
            data[key] = []
            current_list = key
    return data


def load_component_graph(root: Path = ROOT) -> dict:
    return json.loads((root / "architecture" / "plugin-graph.json").read_text())


def validate_component_graph(root: Path = ROOT) -> list[str]:
    errors = []
    graph_path = root / "architecture" / "plugin-graph.json"
    if not graph_path.exists():
        return ["missing architecture/plugin-graph.json"]
    graph = load_component_graph(root)
    agent_dir = root / "agents"
    skill_dir = root / "skills"
    actual_agents = {p.stem for p in agent_dir.glob("*.md")}
    graph_agents = set(graph.get("agents", {}))
    if actual_agents != graph_agents:
        missing = sorted(actual_agents - graph_agents)
        extra = sorted(graph_agents - actual_agents)
        if missing:
            errors.append(f"agents missing from graph: {', '.join(missing)}")
        if extra:
            errors.append(f"graph references missing agents: {', '.join(extra)}")

    actual_skills = {p.parent.name for p in skill_dir.glob("*/SKILL.md")}
    for agent, contract in graph.get("agents", {}).items():
        path = agent_dir / f"{agent}.md"
        if not path.exists():
            continue
        frontmatter = parse_frontmatter(path)
        declared = set(frontmatter.get("skills", []))
        for skill in contract.get("required_skills", []):
            if skill not in actual_skills:
                errors.append(f"{agent} requires missing skill {skill}")
            if skill not in declared:
                errors.append(f"{agent} does not preload required skill {skill}")

    workflow = graph.get("workflows", {}).get("new-post", {})
    sequence = workflow.get("sequence", [])
    for agent in sequence:
        if agent not in graph_agents:
            errors.append(f"new-post references unknown agent {agent}")

    conditional_agents = set()
    for name, edge in workflow.get("conditional", {}).items():
        agent = edge.get("agent")
        if not agent or agent not in graph_agents:
            errors.append(f"conditional edge {name} references unknown agent {agent!r}")
            continue
        conditional_agents.add(agent)
        after, before = edge.get("after"), edge.get("before")
        if after not in sequence or before not in sequence:
            errors.append(f"conditional edge {name} has invalid anchors {after!r}/{before!r}")
        elif sequence.index(after) >= sequence.index(before):
            errors.append(f"conditional edge {name} anchors are out of order")
        if not edge.get("asset_gate"):
            errors.append(f"conditional edge {name} is missing asset_gate")

    shipping = set(sequence) | conditional_agents
    for capability, owners in graph.get("capabilities", {}).items():
        unknown = sorted(set(owners) - graph_agents)
        if unknown:
            errors.append(f"{capability} has unknown owners: {', '.join(unknown)}")
        if not shipping.intersection(owners):
            errors.append(f"{capability} has no owner on the shipping path")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate plugin agent/skill/capability graph")
    parser.add_argument("command", nargs="?", default="check", choices=("check",))
    parser.parse_args(argv)
    errors = validate_component_graph(ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Plugin graph: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
