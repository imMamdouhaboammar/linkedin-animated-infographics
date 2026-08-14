# LinkedIn Animated Infographics - Antigravity Rules

These rules govern all autonomous subagents, workers, and workflows when creating LinkedIn animated infographics in this repository.

## 1. Dimensional & Canvas Invariants
- Artboards must strictly target the fixed **1080x1350** aspect ratio (4:5 vertical).
- No floating unbounded containers; all visual zones must sit within deliberate layout containers with safe margins (min 60px outer padding).

## 2. Verified Identity & Asset Invariants (Lobe-First)
- User-supplied official vector assets take highest precedence.
- Named AI, SaaS, language, framework, and database marks must resolve via verified Lobe hub (`https://lobehub.com/icons`).
- Missing or unverifiable brand assets must **HOLD**. Never generate, approximate, or hallucinate trademarked logos or official mascots.
- All resolved brand marks must be saved as local embedded or file assets before concept layout.

## 3. Intentional Render-Safe Typography
- Prioritize user-specified or bundled local/system font families.
- Remote font loading (e.g. `@import url('https://fonts.googleapis.com/...')`) during render capture is strictly forbidden to prevent flaky offline captures and network drift.
- Typography specs must be validated via `tools/type_spec_check.py`.

## 4. Visual & Structural Standards
- **Palette**: Default to `creative-attractive-restrained`. Harmonious, high-contrast, professional, non-garish tones.
- **Composition**: Default to `center-first`. Center the primary visual anchor unless a documented alignment exception applies (e.g., Arabic RTL flow, UI mockups, code terminals, structured comparison tables).
- **Macro-Rhythm**: Maintain one dominant visual anchor per post. Avoid decorative slop, gratuitous badges, and over-nested cards.

## 5. Still-First QA & Motion Discipline
- Static artboard must achieve an independent **PASS** from `post-critic` and `render-qa` before motion engineering begins.
- Motion must perform a specific storytelling job (progressive reveal, state change, flow indicator) rather than ambient distraction.
- Animation must be deterministic, seekable, and strictly loop within the frame budget.

## 6. Research Gates & Bounded Repair
- Respect all active research gates in `research/capability-notes/gates.json`.
- A maximum of 2 targeted repair loops is permitted for QA before escalation.
