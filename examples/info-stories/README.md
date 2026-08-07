# Info-stories acceptance examples

These examples prove that the same registry can resolve two categorically different compositions without changing the render pipeline.

## Ember Signal

- Story House: Ember Paper
- Visual Style: Signal Sheet
- Story Archetype: Framework in One Page
- Motion Patterns: Sequential Highlight + Chip / Badge Pulse
- Design dials: variance 5, motion 4, density 8
- Execution bridge: `cheat-sheet-poster`

Regenerate:

```bash
python3 tools/story_scaffold.py \
  --topic "Agent skills reference" \
  --takeaway "Each layer has one job" \
  --cta "Save this reference" \
  --house ember-paper \
  --style signal-sheet \
  --archetype framework-in-one-page \
  --motion sequential-highlight \
  --motion chip-badge-pulse \
  --out examples/info-stories/ember-signal-brief.json
```

## Midnight Command

- Story House: Midnight Operator
- Visual Style: Command Canvas
- Story Archetype: One Prompt, Full Workflow
- Motion Patterns: Type-On Terminal + Soft Zoom Focus
- Design dials: variance 6, motion 7, density 5
- Execution bridge: `terminal-card`

Regenerate:

```bash
python3 tools/story_scaffold.py \
  --topic "One prompt runs outbound" \
  --takeaway "The terminal coordinates the workflow" \
  --cta "See the workflow" \
  --house midnight-operator \
  --style command-canvas \
  --archetype one-prompt-full-workflow \
  --motion type-on-terminal \
  --motion soft-zoom-focus \
  --out examples/info-stories/midnight-command-brief.json
```

## Palette chooser

Open `assets/info-stories-palettes.html`, or regenerate it with:

```bash
python3 tools/palette_preview.py --out assets/info-stories-palettes.html
```

The tests compare these tracked artifacts to fresh generation so catalog drift cannot silently stale the examples.
