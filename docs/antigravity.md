# Google Antigravity & Gemini CLI Architecture

This document describes the native **Google Antigravity** and **Gemini CLI** host packaging, agent catalog, discovery mechanisms, lifecycle hooks, and cross-host parity in this repository.

---

## 1. Overview & Packaging

The Google Antigravity distribution packages the same canonical product core (`skills/`, `agents/`, `helper/`, `tools/`, `research/`) through native Antigravity discovery conventions without forking business logic.

### Manifests & Configurations
- **Root Manifest**: [`plugin.json`](../plugin.json) declares plugin metadata, version `3.4.0`, capabilities, and chat UI actions.
- **Local Directory Manifest**: [`.agents/plugins/linkedin-animated-infographics/plugin.json`](../.agents/plugins/linkedin-animated-infographics/plugin.json) enables local project discovery.
- **Plugin Registration**: [`.agents/plugins.json`](../.agents/plugins.json) registers project-level plugin entries.
- **Skill Registration**: [`.agents/skills.json`](../.agents/skills.json) maps Antigravity skills directly to canonical `skills/`.
- **Lifecycle Hooks**: [`.agents/hooks.json`](../.agents/hooks.json) runs synchronous validation and runtime context injection.
- **Directory Rules**: [`.agents/rules/linkedin-animated-infographics.md`](../.agents/rules/linkedin-animated-infographics.md) enforces canvas, typography, and QA invariants.
- **Host Compatibility**: [`compatibility/antigravity.json`](../compatibility/antigravity.json) declares cross-host parity invariants and distribution metadata.

---

## 2. Antigravity 19 Specialized Subagents

All 19 canonical agents from `agents/*.md` are parsed and cataloged in [`.agents/agents/catalog.json`](../.agents/agents/catalog.json).

Each agent is defined with:
- `name`: unique identifier
- `role`: human-readable job title
- `description`: front-facing purpose
- `enable_write_tools`: bounded filesystem/command permissions (`True` for builders/engineers, `False` for reviewers/critics)
- `model`: recommended model tier (`pro` for complex critique and concepting, `flash` for lightweight research, `inherit` for standard workers)
- `system_prompt`: full domain instructions

### Agent Catalog Summary

| Agent | Role | Permissions | Model Tier | Output Artifact |
| :--- | :--- | :--- | :--- | :--- |
| `design-study` | Design Study Specialist | Read-only | `flash` | `build/design-study.json` |
| `evidence-checker` | Evidence Checker | Read-only | `flash` | `build/evidence.json` |
| `asset-curator` | Asset Curator | Read-only | `inherit` | `build/asset-plan.json` |
| `creative-director` | Creative Director | Read-only | `pro` | `build/creative-concepts.json` |
| `story-architect` | Story Architect | Read-only | `inherit` | `build/story-brief.json` |
| `palette-curator` | Palette Curator | Read-only | `flash` | `build/palette-check.json` |
| `type-curator` | Type Curator | Read-only | `flash` | `build/type-spec.json` |
| `copy-compressor` | Copy Compressor | Read-only | `flash` | `build/artboard-copy.json` |
| `layout-composer` | Layout Composer | Write | `pro` | `build/layout-spec.json` |
| `caption-writer` | Caption Writer | Read-only | `flash` | `build/caption.md` |
| `artboard-builder` | Artboard Builder | Write | `inherit` | `build/post.html`, `build/still.png` |
| `motion-director` | Motion Director | Write | `pro` | `build/motion-direction.json` |
| `mascot-animator` | Mascot Animator | Write | `inherit` | `build/mascot/motion-contract.json` |
| `motion-engineer` | Motion Engineer | Write | `inherit` | `build/post.html` (animated) |
| `render-qa` | Render QA | Read-only | `flash` | `build/render-report.json` |
| `post-critic` | Post Critic | Read-only | `pro` | `build/critic-report.json` |
| `story-verifier` | Story Verifier | Read-only | `pro` | `build/verification-report.json` |
| `masterone` | MasterOne Onboarding | Read-only | `flash` | `.linkedin-infographics/profile.json` |
| `community-publisher`| Community Publisher | Write | `inherit` | GitHub PR URL |

---

## 3. Lifecycle Hooks (`hooks.json`)

Antigravity executes lifecycle hooks to enforce quality and context injection:

1. **`PostToolUse` (Artboard Linter)**:
   - Matches: `replace_file_content`, `multi_replace_file_content`, `write_to_file`.
   - Command: `python3 scripts/post_tool_artboard_lint.py`.
   - Purpose: Real-time static linting of generated HTML artboards.
2. **`PreInvocation` (Runtime Context Injector)**:
   - Command: `python3 scripts/runtime_subagent_context.py`.
   - Purpose: Injects runtime request and boundary contexts to active subagents.

---

## 4. Agent Manager Script (`scripts/antigravity_agents.py`)

The agent manager CLI provides programmatic management for Antigravity subagents:

```bash
# List all 19 agents and their configuration
python3 scripts/antigravity_agents.py list

# Validate all agent definitions
python3 scripts/antigravity_agents.py check

# Export / refresh .agents/agents/catalog.json
python3 scripts/antigravity_agents.py export

# Retrieve JSON definition for define_subagent
python3 scripts/antigravity_agents.py get --name creative-director
```

---

## 5. Validation and Health Checks

Validate the complete Antigravity plugin contract using:

```bash
python3 scripts/validate_antigravity_plugin.py check
python3 -m unittest tests/test_antigravity_plugin.py -v
```
