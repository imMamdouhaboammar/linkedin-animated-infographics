# Findings: LinkedIn Animated Infographics Architecture & Workflow Engine

## 1. MasterOne Front-Door Specification
- **Primary Schema:** `schemas/masterone-profile.schema.json`
- **Location of Persistent Profile:** `.linkedin-infographics/profile.json`
- **Blocking Parameters for `create-post`:**
  1. `content.default_language` (e.g. "en", "ar", "bilingual")
  2. `content.audience` (e.g. "B2B SaaS Founders", "AI Engineers")
  3. `linkedin.output_mode` ("animated", "static")
  4. `copyright.footer_text` (if `copyright.footer_required` is true)

## 2. Agent Router & Model Tier Delegation (GPT-5.6 Sol / Pro Integration)
The orchestrator leverages an **Intelligent Agent Router** that dynamically routes tasks to the optimal model tier:

| Model Tier / Class | Workers Assigned | Capability Justification |
| :--- | :--- | :--- |
| **High-Reasoning Tier**<br>(`pro` / `GPT-5.6 Sol` / `Opus` / `Gemini 3.1 Pro`) | • `creative-director`<br>• `post-critic`<br>• `story-verifier`<br>• `layout-composer`<br>• `motion-director` | Multi-step abstract reasoning, spatial geometry planning, adversarial critique, physics math, and non-negotiable verification gates. |
| **High-Speed Execution Tier**<br>(`flash` / `GPT-5.6 Mini` / `Gemini 3.5 Flash`) | • `copy-compressor`<br>• `caption-writer`<br>• `palette-curator`<br>• `type-curator`<br>• `evidence-checker`<br>• `render-qa`<br>• `masterone` | Fast token throughput, deterministic schema matching, microcopy formatting, regex/DOM checks, and linear metric extraction. |
| **Specialized Tool Tier**<br>(`inherit` with write tools) | • `artboard-builder`<br>• `motion-engineer`<br>• `mascot-animator`<br>• `community-publisher` | Precision file writing, SVG/CSS injection, and test execution. |

## 3. 30-Second Liveness Watchdog Protocol
To guarantee deterministic execution and prevent hung subagents during long-running production:
1. **Heartbeat Initialization**: The orchestrator schedules a 30-second watchdog timer:
   ```json
   {
     "DurationSeconds": 30,
     "TimerCondition": "any",
     "Prompt": "Watchdog Heartbeat: Inspect active subagents, check artifact mtimes, and detect stalls."
   }
   ```
2. **Health Check Routine (Every 30s)**:
   - Poll subagent states via `manage_subagents(Action="list")`.
   - Inspect output artifacts in `build/` (e.g. `build/evidence.json`, `build/post.html`).
   - If a worker has been running with no progress for > 2 ticks (60s), send a status inquiry or trigger a graceful retry.
3. **Bounded Repair Enforcement**:
   - Limit repair loops to a strict maximum of **2 iterations** per quality gate before escalating to MasterOne with a precise HOLD report.

## 4. The Canonical 17-Worker Pipeline (`new-post`)
1. `design-study` -> Reference DNA extraction (`build/reference-dna.json`)
2. `evidence-checker` -> Fact & claim verification (`build/evidence.json`)
3. `asset-curator` -> Lobe-first identity sourcing (`build/asset-plan.json`)
4. `creative-director` -> Concept structure, visual anchor, aha moment (`build/creative-concepts.json`) [GPT-5.6 Sol / Pro]
5. `story-architect` -> Narrative progression & story blueprint (`build/story-brief.json`)
6. `palette-curator` -> Token assignment & contrast floors (`build/palette-check.json`)
7. `type-curator` -> Intentional typography & render-safe fonts (`build/type-spec.json`)
8. `copy-compressor` -> Hooked microcopy & slot budget (`build/artboard-copy.json`) [Flash]
9. `layout-composer` -> 1080x1350 spatial geometry & rail setup (`build/layout-spec.json`) [GPT-5.6 Sol / Pro]
10. `caption-writer` -> Post caption & first comment (`build/caption.md`, `build/first-comment.md`) [Flash]
11. `artboard-builder` -> Static HTML poster generation (`build/post.html`, `build/still.png`)
12. `motion-director` -> Motion recipe & clock choreography (`build/motion-direction.json`) [GPT-5.6 Sol / Pro]
13. `mascot-animator` (optional) -> Rigged SVG character motion (`build/mascot-motion.json`)
14. `motion-engineer` -> CSS keyframes & seekable choreography (`build/post.html`)
15. `render-qa` -> Headless capture & diff analysis (`build/render-report.json`, `build/post.gif`) [Flash]
16. `post-critic` -> Quality gates critique & review findings (`build/post-critique.json`) [GPT-5.6 Sol / Pro]
17. `story-verifier` -> Final shipping certification (`build/verification-report.json`) [GPT-5.6 Sol / Pro]
