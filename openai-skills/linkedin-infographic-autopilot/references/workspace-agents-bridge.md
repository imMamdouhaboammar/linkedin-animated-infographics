# Workspace Agents bridge

Workspace Agents are an optional execution capability and are not automatically registered by installing this skills-only plugin.

Use a Workspace Agent only when a callable agent is observed in the current host and its contract matches the bounded side job being delegated.

## Priority

When real delegation is available, choose the best observed execution surface for the job:

1. compatible callable Workspace Agent when explicitly exposed and appropriate
2. Codex subagents when available in the current Codex environment
3. sequential role passes when no real delegation surface is observed

The priority is not a claim that every host exposes all three.

## Suggested external agent roles

A workspace may publish agents corresponding to:

- Creative Director
- Evidence Researcher
- Layout Composer
- Still Critic
- Motion Director
- Final Verifier

These are recommendations and interoperability contracts, not resources installed by this plugin.

## Invocation contract

Before delegation provide:

- one bounded task
- explicit input artifacts
- explicit output artifact schema
- prohibited actions
- whether writes are allowed

After delegation verify the returned artifact before advancing.

## Honesty rule

If a Workspace Agent is not observed, do not claim it exists, was invoked, or ran in the background. Use Codex subagents or sequential execution instead.

If a published agent is exposed but cannot access the required source/artifact, do not fabricate a result. Degrade to a capable execution surface or return `HOLD`.
