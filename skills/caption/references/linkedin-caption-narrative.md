# LinkedIn Caption Narrative

Use this reference when the caption is about a repo, Plugin, Skill, workflow, AI tool, technical resource, curated collection, belief correction, recent-signal research story, GIF, or animated infographic

The broader `caption-patterns.md` remains the canonical archetype library

This reference adds a narrower production pattern for technical storytelling and first-comment utility payloads

## Narrative grammar

The dominant pattern is

**Tension → Named Thing → Mechanism → Specifics → Why It Matters → Visual Bridge → Action**

Not every caption needs every stage

Each block must advance the idea instead of repeating the opening

## Hook rules

Open on one concrete tension

Useful tension types

- a specific tool failure
- a repeated task that became annoying
- an incomplete assumption
- a stale research process
- a metric that hides the real outcome
- a coordination problem created by too many tools or Skills
- a technical constraint that blocks a practical result

Strong shapes

- `Most OCR tools choke on messy documents`
- `Most AI tools talk too much`
- `Your page can rank first and still never become the answer`
- `I built so many AI Skills that using them became its own workflow`

Reject a hook when another product name could replace the real one without changing the meaning

Generate several hook candidates silently before selecting line 1

## Name the artifact early

Prefer the real noun

- repo name
- Plugin name
- Skill name
- model name
- command
- workflow
- source category

Generic `tool`, `solution`, or `platform` language should not replace the real name when the real name is available

## Mechanism before praise

Explain what happens using plain verbs

Prefer

`A hook grabs Claude's reply after it finishes`

Over

`It improves communication with AI`

Prefer

`Searches recent activity across Reddit, X, YouTube, Hacker News, GitHub and prediction markets`

Over

`It gives you better research`

## Specificity as credibility

Use checkable details when supplied or verified

- commands
- repo names
- model names
- inputs and outputs
- license
- hardware
- pricing
- benchmarks
- stars
- steps
- categories
- concrete use cases

Never invent precision to strengthen a post

## Archetype selection

### Repo Explainer

Use for one repo, tool, Skill, model, or Plugin

Flow

```text
specific friction
one-line solution
named artifact
mechanism
↳ consequence
mechanism
↳ consequence
why it matters
link location
one practical question
```

### Stack Catalogue

Use for a large collection

Organize by job rather than dumping a list

Each category gets

- category name
- what the category controls
- named items
- one consequence line

A raw list is not a catalogue story

### Operating Story

Use when the interesting part is the handoff between specialists, Plugins, agents, or stages

Flow

```text
repeated workflow problem
what changed
specialist 1
↳ job
specialist 2
↳ job
specialist 3
↳ job
handoff explanation
visual bridge
first-comment links
question
```

### Belief Correction

Use when a familiar metric or assumption is incomplete

Turn the correction into a practical diagnostic the reader can run

### Recent-Signal Story

Use when freshness is the problem

Name the source roles, then make synthesis and comparison the story rather than source count

### Visual Companion

Use when the GIF or infographic already carries much of the explanation

Keep the caption shorter and explain why the visual matters instead of narrating each frame

## Scan rhythm

- most paragraphs should be one or two short lines
- allow uneven paragraph length
- one main idea per block
- section labels only when they improve scanning
- `↳` means mechanism, clarification, consequence, or sub-step
- do not use `↳` decoratively
- sparse structural emoji only when it fits the writer

## First comment

Use the first comment for material that would slow the caption

- repo links
- Plugin links
- setup commands
- install steps
- sources
- long catalogue entries

Do not repeat the caption

Preserve exact URLs and item order when the visual establishes an order

## Visual division of labor

Caption owns

- why the reader should care
- interpretation
- non-obvious mechanism
- practical consequence
- CTA

Visual owns

- sequence
- topology
- handoff
- comparison
- hierarchy
- category grouping
- spatial relationships

Use one visual bridge at most

A visual can illustrate a process without proving it

Do not imply case-study evidence when the asset is only an example

## Reference-derived lessons

### claudish-to-english

Technical repo explanation works when the background process is explained in plain verbs

### Claude repo catalogue

Large collections need an organizing model and category-level payoff lines

### olmOCR

Operational facts such as supported inputs, benchmark, cost, hardware, and license can carry more weight than adjectives

### i-have-adhd

When a product changes output behavior, show the behavior directly instead of over-explaining architecture

### /last30days

For multi-source research, synthesis is the story, not source count

### GEO/AEO example

A broad educational idea becomes useful when it becomes a diagnostic check the reader can run immediately

## Anti-slop rules

Reject

- generic motivational closes
- fake urgency
- empty superlatives
- repeated `not X, but Y`
- mechanical paragraph symmetry
- generic `Thoughts?` CTA
- repeated recap
- dramatic punctuation without information
- generic AI-product hooks
- unsupported claims

House style outranks this reference

If the user bans terminal periods, remove terminal periods from visible copy except where dots are required inside URLs, version numbers, decimals, commands, filenames, domains, or other technical literals

If the user bans em dashes, use none

## Quality check

Before shipping, verify

1. mobile hook is concrete
2. real nouns appear early
3. mechanism is understandable
4. every precise claim is supported
5. each section advances the narrative
6. visual and caption have distinct jobs
7. first comment carries utility instead of repetition
8. the draft sounds sayable
9. all active house-style rules pass
10. every URL and product name is exact
