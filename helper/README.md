# Ecosystem Helper

`helper/` is the routing authority for this repository. It sits beside `skills/` and `agents/` and tells an LLM which workflow should run, which capabilities and workers are required, which assets can block progress, and which artifacts form the handoff contract.

The helper does not replace domain skills or agents. It keeps them coordinated.

## Files

- `GUIDE.md`: LLM-facing decision protocol
- `router.json`: intent, workflow, skill, agent, and conditional routing
- `capabilities.json`: capability ownership
- `artifacts.json`: artifact producers, consumers, and blocking semantics

Validate the complete helper with:

```bash
python3 scripts/ecosystem_router.py check
```

Route a structured request with:

```bash
python3 tools/route_request.py --request "Create an animated LinkedIn infographic" --output gif
```

The helper is machine-readable. Human documentation may explain it but must not contradict it.
