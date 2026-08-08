# Capability negotiation

Autopilot begins by observing what the current host actually exposes. Documentation, repository configuration, or a previously available tool is not evidence that the capability exists in this session.

Unknown capabilities are unavailable until they are observed.

## Capability keys

- `subagents`: real child-agent, side-job, or delegated worker execution is exposed
- `sandbox_write`: the host exposes a writable sandbox, workspace, or equivalent artifact store
- `shell_or_code_execution`: commands, scripts, Python, Node, renderers, validators, or equivalent code execution can actually run
- `image_inspection`: the host can inspect generated or supplied stills/frames rather than reasoning from filenames alone
- `web_research`: a fresh public-search or browsing capability is exposed
- `connected_apps`: authenticated apps/connectors are exposed for the current session
- `workspace_agents`: callable published Workspace Agents are exposed to this session
- `publishing_tools`: authenticated contribution tooling is exposed and permitted for the requested publishing action

## Observation states

For every key record one state:

- `observed-available`
- `observed-unavailable`
- `unknown`

Treat both `observed-unavailable` and `unknown` as unavailable for execution-path selection.

## Capability evidence

Accept evidence such as:

- a callable tool namespace visible in the current host
- successful creation of a child agent/thread
- a writable sandbox or file tool exposed by the host
- a successful non-destructive probe needed for the task

Do not probe with destructive writes, publication, external messages, or irreversible actions.

## Selection inputs

`full-autopilot` requires observed real delegation plus the execution capabilities needed for the requested deliverable.

`tool-rich-sequential` requires useful execution tooling or sandbox access but does not require subagents.

`safe-skill-only` is selected when artifact execution cannot be truthfully completed with the capabilities observed.

## Truthfulness invariant

Never convert an `unknown` capability into `observed-available` because the model believes the product normally supports it. The final report names only capabilities that were observed and actually used.
