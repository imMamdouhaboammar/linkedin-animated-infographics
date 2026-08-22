---
name: linkedin-caption-narrative
description: Use when writing or rewriting LinkedIn captions for repos, plugins, AI workflows, GIFs, infographics, technical ideas, curated collections, tool explainers, belief-correction posts, or first-comment link payloads that need a strong mobile hook and mechanism-first narrative
---

# LinkedIn Caption Narrative

## Purpose

Write high-signal LinkedIn captions that read like a useful explanation someone would stop to read, not launch copy pretending to be conversational

Core principle

**Hook with a real tension, name the thing early, explain the mechanism with concrete nouns, let the visual carry part of the story, and move link-heavy utility into the first comment when that improves the read**

This Skill is designed for technical and AI-adjacent posts where the artifact itself matters: repositories, Plugins, Skills, workflows, models, research methods, animated infographics, GIFs, catalogues, and practical belief corrections

## Use when

Use this Skill when the user asks for any of the following

- a hooky or stop-scroll LinkedIn caption
- a caption for a GitHub repo, Plugin, Skill, workflow, AI tool, model, or technical resource
- a caption that accompanies a GIF or animated infographic
- a curated list or catalogue of repos, tools, or workflows
- a belief-correction educational post
- a recent-signal or research-process post
- a caption plus first comment
- a rewrite inspired by high-signal AI, developer, marketing, GTM, or technical LinkedIn posts

Do not use this as a generic thought-leadership template when there is no real mechanism, artifact, evidence, or practical idea to explain

## Inputs

Resolve these from the user material before drafting

1. **Thing**: what exactly is being shown or discussed
2. **Reader**: who would care and why
3. **Tension**: what friction, misconception, repeated task, or missing context creates interest
4. **Mechanism**: what actually happens
5. **Specifics**: names, commands, steps, inputs, outputs, limits, categories, or verified numbers
6. **Proof**: only evidence supplied or verified
7. **Visual job**: what the GIF or infographic already communicates
8. **CTA**: one useful next action
9. **First-comment payload**: links, setup steps, sources, install commands, or long catalogue entries
10. **House style**: punctuation, banned language, dialect, capitalization, formatting, or other explicit user rules

If a factual claim, number, benchmark, price, star count, license, compatibility statement, performance claim, testimonial, or product behavior is not supported, do not invent it

## Outputs

Return the finished caption first

Return a finished first comment when the user requests one or when links, commands, sources, or a long catalogue would make the caption harder to read

Do not expose pattern names, scoring, internal routing, or drafting notes unless the user asks for them

## Core narrative grammar

The dominant transferable pattern is

**Tension → Named Thing → Mechanism → Specifics → Why It Matters → Visual Bridge → Action**

Not every post needs every stage

The important rule is that each block must advance the idea instead of restating the hook

### 1. Tension

Open on something recognizable and concrete

Strong tension types

- a tool behaves badly in a specific way
- a repeated task has become annoying
- a common assumption is incomplete
- a category changes faster than the research process
- a metric looks good but hides the real problem
- too many resources create a coordination problem
- a technical constraint blocks a practical outcome

Good shapes

- `Most OCR tools choke on messy documents`
- `Most AI tools talk too much`
- `Your page can rank first and still never become the answer`
- `I built so many AI Skills that using them became its own workflow`

Weak shapes

- `AI is changing everything`
- `This tool is amazing`
- `The future of work is here`
- `I found a game-changing repo`

Reject a hook if another product name can be swapped in without changing the meaning

### 2. Named Thing

Name the artifact early

Useful forms

- `Meet {repo-name}`
- `The {repo-name} GitHub repo`
- `This Skill`
- `This Plugin`
- `The stack`
- `The visual below`

Named things reduce vagueness and make the post inspectable

### 3. Mechanism

Explain what happens using plain verbs

Prefer

`A hook grabs Claude's reply after it finishes`

Over

`It improves communication with AI`

Prefer

`Searches recent activity across Reddit, X, YouTube, Hacker News, GitHub and prediction markets`

Over

`It gives you better research`

Mechanism is the credibility layer

### 4. Specifics

Use details that can be checked or acted on

- exact commands
- repo names
- model names
- supported inputs
- output format
- licenses
- hardware
- pricing
- benchmark scores
- star counts
- steps
- concrete use cases

Specificity must serve the decision, not decorate the copy

### 5. Why it matters

Translate the mechanism into one or two practical consequences

Examples

- `If Ollama is down, Claude still works normally`
- `The useful answer can be extracted without decoding four paragraphs first`
- `You stop reopening the same context every session`

### 6. Visual bridge

When a GIF or infographic is attached, use one short bridge at most

Examples

- `The GIF below is how I think about the handoff`
- `The visual shows where each specialist enters`
- `The animation makes the sequence easier to see`
- `The page inside the GIF is an example, not a client result`

Do not narrate every frame

### 7. Action

Choose one practical next action

- open the repo
- install the Skill
- try one Plugin
- save the setup
- inspect the first comment
- answer one practical question

Avoid vague asks such as `Thoughts?`

## Caption archetypes

Choose one primary archetype and stay in it

### A. Repo Explainer

Use when one repo, tool, Skill, model, or Plugin is the subject

Shape

```text
{specific friction}

{one-line solution}

Meet {name}

{verified free/open-source/local/license line when relevant}

Here's what it does:

{mechanism}
↳ {practical consequence}

{mechanism}
↳ {practical consequence}

Why it matters:

{one concrete consequence}

{link location}

P.S. {easy practical question}
```

### B. Stack Catalogue

Use when the value comes from a collection

Shape

```text
{how the collection became necessary}

{count + collection + what unifies it}

{CATEGORY}, {what the category controls}

✦ {item}
✦ {item}
✦ {item}

{one-line category payoff}

{next category}

{compounding line}

{link location}

P.S. {which one would you use first}
```

Critical rule

The collection needs an organizing model

A raw list is not a catalogue story

### C. Operating Story

Use when the interesting part is how work moves

Shape

```text
{repeated workflow problem}

{what changed in the way the work is handled}

{specialist 1}
↳ {job}

{specialist 2}
↳ {job}

{specialist 3}
↳ {job}

The interesting part is the handoff

{how the work moves between them}

{visual bridge}

{first comment}

{question}
```

Good for Plugin stacks, agent workflows, multi-step research, and production pipelines

### D. Belief Correction

Use when a familiar metric or assumption is incomplete

Shape

```text
{strong belief correction}

{why the normal interpretation is incomplete}

That usually comes down to {N} things

1. {factor}
↳ {specific behavior}

2. {factor}
↳ {specific behavior}

3. {factor}
↳ {specific behavior}

{diagnostic question}

{visual disclaimer when needed}

{reader question}
```

### E. Recent-Signal Story

Use when freshness is the problem

Shape

```text
{what goes stale}

{how quickly the category changes}

{named sources and what each contributes}

The interesting part is {comparison or synthesis}

↳ collect
↳ compare
↳ filter
↳ synthesize

{practical use cases}

{visual bridge}

{question about manual source checking}
```

### F. Visual Companion

Use when the visual already carries much of the narrative

Shape

```text
{one-line tension}

{one-line frame for the visual}

{2 to 5 points the viewer should notice}

{what the animation makes easier to understand}

{link or source location}

{one question}
```

Keep this shorter than the visual's information density would suggest

## Hook procedure

Before drafting the body, generate 8 to 12 hook candidates silently

Use at least three different hook mechanisms

- friction
- belief correction
- concrete curiosity
- catalogue scale
- direct utility
- operating problem

Reject hooks that

- could introduce almost any AI product
- depend on hype adjectives
- need the next line to explain what the first line meant
- create suspense around a trivial fact
- promise an unsupported result
- sound written to impress rather than clarify

Keep line 1 compact enough to survive mobile truncation when the language allows it

Roughly 55 characters is a useful default, not a hard law

## Scan rhythm

- keep most paragraphs to one or two short lines
- allow uneven paragraph lengths
- put one main idea in each block
- use whitespace deliberately
- do not turn every sentence into a standalone paragraph when it damages flow
- use section labels only when they make a dense technical post easier to scan
- use `↳` for mechanism, clarification, consequence, or sub-step
- do not use `↳` as decoration
- keep emoji sparse and structural when the writer uses them

## First comment

The first comment has a separate job

It carries utility without slowing the main caption

Use it for

- repo or Plugin links
- installation commands
- setup steps
- source references
- long resource catalogues
- exact paths or technical instructions

### Link index pattern

```text
All links from the visual 👇

1. {Name}
{one-line job}
{URL}

2. {Name}
{one-line job}
{URL}

Start with the one closest to a task you already repeat
```

### Install guide pattern

```text
Setup:

Step 1
↳ {command}

Step 2
↳ {command}

Step 3
↳ {command}

Repo:
{URL}
```

### Source note pattern

```text
Sources / references:

↳ {source}
↳ {source}
↳ {source}

The visual simplifies the idea, so use the sources above for the full context
```

First-comment rules

- do not repeat the whole caption
- do not add a second sales pitch
- do not hide a material limitation in the comment
- preserve exact URLs
- keep names in the same order as the visual when order matters
- if two links use the same display name, distinguish the variants when known

## Visual companion contract

Caption and visual should divide the communication job

Caption owns

- reason to care
- tension
- interpretation
- mechanism that is not obvious visually
- practical consequence
- CTA

Visual owns

- sequence
- topology
- handoff
- comparison
- hierarchy
- before and after
- category grouping
- spatial relationships

Ask two questions before finalizing

1. If the GIF disappears, what useful information is missing from the caption
2. If the caption disappears, what useful information is missing from the GIF

Both answers should contain something important

If the caption merely narrates the animation, compress it

A visual can illustrate a process without proving it

Use `shows`, `maps`, `illustrates`, or `explains`

Do not imply case-study evidence unless the supplied evidence supports it

## Voice and anti-slop rules

- plain English over polished corporate prose
- specific nouns over adjectives
- mechanism before praise
- useful roughness over suspiciously perfect symmetry
- preserve normal technical vocabulary
- no fake urgency
- no invented anecdotes
- no invented proof
- no generic motivational conclusion
- no repeated recap
- no empty superlatives
- no em dash
- avoid repeated `not X, but Y` constructions
- avoid generic transition phrases
- avoid engagement bait disguised as a question

House style outranks this Skill

If the user bans terminal periods, remove terminal periods from visible copy while preserving dots required inside URLs, version numbers, decimals, commands, filenames, domains, and other technical literals

If the user supplies a voice sample, derive cadence and vocabulary from that sample instead of copying example phrasing from this Skill

## Procedure

1. Resolve the inputs and evidence boundary
2. Read `references/reference-examples.md` when the user asks to match the supplied style family or when pattern choice is uncertain
3. Pick one archetype
4. Generate and filter hook candidates
5. Draft the narrative around one primary idea
6. Name the real artifact early
7. Explain mechanism before praise
8. Add only supported specifics
9. Divide the communication job between caption and visual
10. Move link-heavy utility into the first comment when useful
11. Apply the user's house style as hard constraints
12. Read `references/quality-gates.md`
13. Revise until every hard gate passes
14. Return only the requested caption and first comment unless critique is requested

## HOLD conditions

Return a HOLD only when the requested output depends on a claim that cannot be supported without inventing or materially changing the user's approved premise

Examples

- unsupported benchmark or result must remain in the hook
- exact product behavior is unknown and cannot be safely generalized
- a visual is described as a client result but the evidence says it is only an example
- a link or product identity cannot be resolved and exactness is required

Otherwise remove unsupported precision and continue

## Related components

Inside the source repository, this Skill complements the canonical `caption` Skill and its broader caption archetype reference

When the host provides the repository tools, run the existing copy-slop checker where appropriate

```bash
python3 tools/copy_slop_check.py --file <caption.txt>
```

This checker is supplemental

The final narrative judgment, evidence boundary, first-comment split, and visual-caption division remain the responsibility of this Skill

## Research gates

Apply these conceptual gates to every visible draft

- **prose-specificity**: prefer checkable names and mechanisms over generic language
- **voice-preservation**: preserve the writer's natural vocabulary and useful cadence
- **evidence-traceability**: every factual precision must come from supplied or verified evidence
- **visual-alignment**: caption and visual must not contradict each other
- **house-style-compliance**: explicit user rules are hard constraints
