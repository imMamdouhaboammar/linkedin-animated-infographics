# Composition Matrix

The merged base registry plus `extensions/*.json` is authoritative. This page is the human scan layer.

| Visual Style | Allowed Story Archetypes | Preferred artboard |
|---|---|---|
| Signal Sheet | Framework in One Page; Step-by-Step Playbook; What Each Piece Actually Does; Decision Cards | cheat-sheet-poster |
| Funnel Board | From Raw Input to Final Output; Ecosystem Snapshot; One Prompt, Full Workflow | flow-map-verdict |
| Stack Ledger | Inside the Stack; Ecosystem Snapshot; Framework in One Page | pipeline-stages |
| Command Canvas | One Prompt, Full Workflow; The Working Screen; Build It Once, Reuse It Often | terminal-card |
| Sequence Board | Step-by-Step Playbook; The 30-Day Breakdown; From Raw Input to Final Output | annotated-blueprint |
| Comparison Grid | What Each Piece Actually Does; Decision Cards; Before / After Workflow | trading-card-grid |
| Proof Mosaic | The Working Screen; Build It Once, Reuse It Often; Before / After Workflow | specimen-grid |
| Tool Catalog | Inside the Stack; Ecosystem Snapshot; Framework in One Page | logo-grid |
| Story Strip | One Prompt, Full Workflow; From Raw Input to Final Output; Before / After Workflow | pipeline-stages |
| Field Guide | Framework in One Page; Decision Cards; What Each Piece Actually Does | cheat-sheet-poster |
| UI Storyboard | Screen to Outcome; State Change Story; Before / After Workflow | annotated-blueprint |
| Interface Cutaway | Inside the Interface; State Change Story; The Working Screen | annotated-blueprint |

## UI mockup rules

For UI Storyboard and Interface Cutaway, read `ui-mockup-rules.md`. Product fidelity and evidence rules remain active even when the interface is illustrative.

## Motion compatibility

A motion is compatible when at least one of its structural signals intersects the selected Visual Style. Use no more than two. A primary-only motion must not compete with another primary-only motion.

`Cursor Focus` is secondary and points to one UI region or control. `State Transition` is primary and shows one meaningful interface state change.

Run `python3 scripts/info_stories.py compose --style <slug> --archetype <slug> --motion <slug>` before handoff.
