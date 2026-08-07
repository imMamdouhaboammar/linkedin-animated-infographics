# Privacy Policy

Last updated: August 8, 2026

LinkedIn Animated Infographics is an open-source, skills-based plugin for ChatGPT, Codex, and Claude Code. Version 3.2.0 does not operate a maintainer-owned backend service and does not require a maintainer-hosted MCP server.

## Data handled by the plugin

The plugin provides instructions, local scripts, validators, templates, and repository assets. Content you give to ChatGPT, Codex, Claude Code, or another compatible host is handled by that host and by any tools or services you explicitly connect to it. Those services have their own privacy terms.

The repository does not contain analytics code that sends prompts, generated content, or usage telemetry to a server operated by the maintainer.

## Local files

Generation and validation can read and write files in the workspace allowed by your host and its permission settings. Generated working artifacts may include HTML, GIF, PNG, JSON, Markdown, evidence notes, render reports, and verification reports.

The community export flow is designed not to copy the complete working directory. It prepares only the public demo package described below.

## Community demo publishing

Community publishing is optional. A finished result is not submitted merely because it was generated or rendered.

After final verification, the plugin may offer to share the demo. GitHub contribution work begins only after explicit user consent and rights confirmation.

The public demo package contains exactly:

- `demo.gif`
- `index.html`
- `demo.json`

A generated `demos/catalog.json` change may also be included in the pull request. The export path checks for obvious credential markers, signed URLs, local absolute paths, and remote executable resources before publication.

Source prompts are excluded by default. A source prompt may be included only when the user separately and explicitly consents to publish it.

If GitHub publishing is approved, the plugin or coding host may use the user's authenticated GitHub tooling to create or reuse a contributor fork, create a branch, commit the approved demo package, push that branch, and open a pull request to `imMamdouhaboammar/linkedin-animated-infographics`. The publisher must stop at the pull request. Maintainer review and merge are manual.

GitHub processes data involved in those operations under GitHub's own terms and privacy policies.

## External tools

Repository-development configuration may reference optional external tools such as GitHub, documentation services, browser tooling, or MCP servers. These are development conveniences, are not required by the installed skills-only plugin, and may have independent privacy policies.

## Secrets and private material

Do not place credentials, private keys, access tokens, confidential source material, or private URLs in content intended for community publication. The repository includes automated checks intended to catch common leakage patterns, but users remain responsible for reviewing material before making it public.

## Changes and contact

Material changes to this policy are tracked in the public repository history.

For questions or reports, use the repository's GitHub Issues page: https://github.com/imMamdouhaboammar/linkedin-animated-infographics/issues
