# Security Policy

## Scope

Security reports for LinkedIn Animated Infographics should focus on repository code and packaging that can expose data, execute unintended commands, bypass publication consent, escape repository or workspace boundaries, or weaken validation and contribution gates

Relevant areas include:

- public demo export and secret scanning
- GitHub community publishing and fork/PR boundaries
- hook command execution
- path traversal and repository-bound file handling
- plugin and marketplace manifests
- scripts that read or write workspace files
- unsafe remote executable resources in public demos

## Reporting a vulnerability

Do not post live credentials, private exploit details, customer data, or other sensitive material in a public issue

If the repository's GitHub Security page offers a private vulnerability reporting option, use that channel. If no private reporting option is available, open a minimal public issue that asks the maintainer for a private contact path without including exploit details or sensitive data

Repository: https://github.com/imMamdouhaboammar/linkedin-animated-infographics

## What to include

A useful report includes the affected version or commit, the vulnerable path or workflow, reproduction steps that do not expose real secrets, the expected security boundary, the observed behavior, and the likely impact

Use synthetic credentials and redacted data in reproductions whenever possible

## Maintainer handling

Reports should be reproduced against the current supported release before a fix is claimed. Security fixes should include regression coverage when the behavior can be tested deterministically

Do not weaken tests, disable validation, expose credentials, or bypass manual community-review requirements to make a security check pass

## Supported release

The current release line is 3.x. Security fixes are applied to the current maintained release rather than to every historical revision
