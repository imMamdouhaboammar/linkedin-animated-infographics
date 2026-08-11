# Typography intelligence

Typography records roles, not screenshot guesses. Each role declares `role`, `stack_id`, supported `scripts`, allowed `weights`, and `font_policy`.

- Roles: `display`, `body`, `label`, and optional `mono`.
- `stack_id` identifies an installed/system stack (for example `arabic-sans-ui` or `latin-grotesk-ui`); list the ordered family fallbacks.
- Scripts are explicit (`latin`, `arabic`, or `mixed`) and weights are numeric.
- `font_policy` is either `exact_declared` (only when the source provides the name) or `role_fallback`; screenshot inspection never proves an exact font.

Record line-height and contrast as implementation constraints. If a script is unsupported by the selected stack, return HOLD rather than silently substituting a mismatched role.
