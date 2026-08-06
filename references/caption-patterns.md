# Caption Patterns

Reverse-engineered from 13 high-performing LinkedIn posts in the AI / GTM / marketing
space. Six archetypes, plus the shared mechanics that apply to all of them.

## Contents

- [Shared mechanics](#shared-mechanics)
- [A. Numbered Inventory](#a-numbered-inventory)
- [B. Result Case Study](#b-result-case-study)
- [C. Bundle Manifest](#c-bundle-manifest)
- [D. Setup Walkthrough](#d-setup-walkthrough)
- [E. Operating Story](#e-operating-story)
- [F. Belief Correction](#f-belief-correction)
- [G. Catalogue Tease](#g-catalogue-tease)
- [Hook library](#hook-library)
- [CTA library](#cta-library)
- [Banned patterns](#banned-patterns)

---

## Shared mechanics

### The truncation cut

LinkedIn truncates at roughly 140 characters or 3 short lines on mobile, whichever
comes first, then shows "…see more". Everything before that cut is the entire ad.

Structure it as:

```
Line 1  →  the claim, the number, or the tension          (≤ 55 chars)
(blank)
Line 2  →  the promise of what follows                    (≤ 60 chars)
(blank)
Line 3  →  optional proof or the first item
```

Line 1 patterns that survive the cut in the reference set:

- `Multichannel outreach gets 2-4x more replies than email alone.` — stat as fact
- `My 9 (most-used) Claude Skills to write prompts.` — inventory declaration
- `Claude has 1000+ MCP connectors.` — scale claim
- `We killed our website Figma last month.` — decision, past tense, specific
- `BREAKING: You can now generate high-performing ad creatives on Claude.` — news frame
- `Delete every prompt template you ever saved.` — imperative that costs the reader something
- `Your boss pretends to read your (ugly) Excel.` — named social friction
- `Most people think marketing is simple.` — belief to be corrected
- `What if your favourite mentors lived in Claude?` — question with a concrete image
- `Save this setup before you write a single line:` — instruction + implied urgency

### Whitespace

Almost every line is its own paragraph. Blocks are 1–2 lines. A caption that runs 500
words still reads in 20 seconds because it is 90% air. When a block hits 3 lines,
break it.

### Specificity as proof

Every reference post is dense with named things:

- Numbers: `275+ clients`, `$7M ARR`, `1.8% to 4.3%`, `300+ hours`, `250+ Ecom brands`,
  `24 minutes`, `4h manual workflow → 20-minute structured pipeline`
- Products by name: `lemlist`, `FullEnrich`, `PredictLeads`, `Knock2.ai`, `MillionVerifier`,
  `Netlify`, `gamma.app`, `Wispr`
- Commands and paths: `/prompt-master`, `~/.claude/skills/`, `SKILL.md`

Generic nouns ("a tool", "an AI platform", "significant results") read as filler and
are skipped. Replace every generic noun with the actual name or delete the line.

### Bullet glyphs

The reference set uses a small consistent vocabulary. Pick one per post and stay in it.

| Glyph | Used for |
|---|---|
| `→` | sub-steps inside a numbered item, or a list of actions |
| `▫️` | deliverables in a bundle manifest |
| `1️⃣ 2️⃣ 3️⃣` | top-level numbered steps in a system |
| `-` | plain lists inside a paragraph block |
| `☑` | checklist items in an inventory |
| `↳` | the consequence or payoff of the item above |

### Length

The reference posts run 150–450 words. Inventory and manifest archetypes run long
because each line is short. Belief Correction runs shortest. There is no length
penalty on LinkedIn if the whitespace rhythm holds.

### Emoji

Sparse and structural, never decorative. `♻️` for repost, `👉` for the one link,
`💌 🫡 👋` at most once as a sign-off. Zero emoji inside body sentences.

---

## A. Numbered Inventory

**Use when:** you have N discrete items of equal weight.
**Visual pairing:** Character Flowchart, Trading Card Grid, Directory Map.

### Skeleton

```
My {N} {qualifier} {things} to {outcome}.

{One-line access offer}:

👉 {url} - {what happens when they go there}

{Optional: "Everything below is what you'll get:"}

1. {name} - {one line: what it does, in verb form}

2. {name} - {one line}

...

{The compounding line: why the set beats the parts}

{CTA}
```

### What makes it work

Each entry is **one line, verb-first, no adjectives**. From the reference:

> `2. /grill-me - interrogates until nothing is vague. The prompt fixes itself in the answers.`

Not "a powerful skill that helps you refine your prompts". The item does something to
something. Two clauses maximum.

The number in line 1 should be odd and specific. 9 outperforms 10. `My 9 (most-used)`
beats `My top 10` because the parenthetical implies a larger set behind it.

### The compounding line

Every strong inventory post has one line near the end explaining why the collection is
worth more than any single item:

> `The best part: the Skills stack. Claude runs /grill-me into /48 into /personal-voice
> in one chat - you just answer the questions and watch.`

Without it the post is a list. With it, it is a system.

---

## B. Result Case Study

**Use when:** you have a genuine before/after metric you can name.
**Visual pairing:** Cheat Sheet Poster, Pipeline Stages, Flow Map.

### Skeleton

```
{Category claim as a stat}.

{Credibility line: volume + scale}:

{The specific case: from X to Y}.

{One line of context: segment, deal size}

The exact system we ran:

1️⃣ {Step name as an imperative}

{2-4 lines of mechanism, including a tool name}

{The mistake most people make at this step}

2️⃣ ...

{Restate the metric: X to Y, in {timeframe}}

{Question CTA}

{P.S. credit line}
```

### What makes it work

The metric appears **three times**: as a category claim in line 1, as a specific case
near the top, and as the closing restatement. Reference:

> Line 1: `Multichannel outreach gets 2-4x more replies than email alone.`
> Early: `We took a client from 1.8% to 4.3% positive replies just by layering channels.`
> Close: `1.8% to 4.3%, in 2 months.`

Each numbered step names the **mistake** as well as the method:

> `Most people apply Tier 3 effort to Tier 1 accounts. On a high-ticket list, that can cost you.`

That line is what makes the reader feel diagnosed rather than lectured.

Tool mentions sit in parentheses, off to the side, so they read as a footnote rather
than a plug: `(Use Hypertide.io if you're going to send emails at scale)`.

---

## C. Bundle Manifest

**Use when:** you are gating a free resource behind a comment.
**Visual pairing:** Directory Map, Trading Card Grid, Node Tree.

### Skeleton

```
I {built / turned X + Y into} a {complete system} for {audience}.

{One line on what it produces}

{One line on why that matters}

Here's what you'll get:

▫️ {Deliverable name}
{One line of what it contains}

▫️ {Deliverable name}
{One line}

... (6–8 items)

{The insight paragraph: 3 short lines naming the real problem the bundle solves}

{Partner/tool credit, if any}

{Comment gate}
```

### What makes it work

The `▫️ Name` + description-underneath structure creates a scannable manifest where
each item has a title and a body. Six to eight items is the sweet spot — four feels
thin, ten feels like padding.

The insight paragraph is the part that earns the comment. Reference:

> `Most outbound teams start with a random list.`
> `Then they try to fix weak targeting with better copy.`
> `This playbook fixes the list before the first message is written.`

Three lines. Problem, wrong fix, right fix. No adjectives.

### Comment gate wording

```
Comment "{KEYWORD}" and I'll send it to you for free.
(Must be connected)
```

Or the three-condition version, which raises follower count as well as comments:

```
→ Add me to your network
→ Follow {Brand}
→ Comment "{KEYWORD}"

I'll send it to you in a DM 🫡
```

Keyword rules: one word, all caps, 4–9 letters, semantically tied to the asset.
`PLAYBOOK`, `CREATIVES`, `GTM`, `API`, `CLAUDE`.

---

## D. Setup Walkthrough

**Use when:** the value is a procedure and the reader could do it today.
**Visual pairing:** Annotated Blueprint, Terminal Card, Spec Sheet.

### Skeleton

```
{Imperative hook that implies saving}:

Step 1. {Action}. {Result}.

Step 2. {Action}. {Result}.

... (5–13 steps)

That's it. {Outcome} in {specific time}.

{The credibility line: what you did so they don't have to}

{Access instructions as their own numbered micro-list}

{Belief-shift close: two lines}

{Repost CTA}
```

### What makes it work

Steps are written at the level of **actual clicks**, not concepts:

> `Step 2. Go to Spreadsheet file → Download → PDF. Done.`
> `Step 4. Turn on bypass permissions in settings. No more clicking "allow" 30 times.`

The parenthetical benefit after each step ("No more clicking allow 30 times") is what
separates this from documentation.

The time claim must be oddly specific. `live in 24 minutes` and `in just 2 minutes`
both outperform "in minutes" because the precision implies someone actually timed it.

The belief-shift close is two lines that reframe what the reader thought was required:

> `People still think you need to learn to code for this.`
> `You don't. You need to learn to screenshot.`

---

## E. Operating Story

**Use when:** you made a real decision inside your company and can show the consequence.
**Visual pairing:** Orbit Cycle, Flow Map, Pipeline Stages.

### Skeleton

```
We {decision, past tense, specific} {timeframe}.

{What we actually did, 2 lines with the cost admitted}

{Verdict line: 3-5 words}

{Mechanism paragraph: why the new way is structurally better}

{Concrete speed or cost delta}

{Who inside the company benefits, one line each}

{What we removed entirely}

{Closing principle: 3 short lines about why this compounds}
```

### What makes it work

**No CTA.** Not one. This archetype trades reach for authority. The reference post
ends on a principle and stops.

The cost is admitted early and specifically:

> `Three weeks of painful work, running two versions in parallel, rebuilding
> illustrations that were easy in Framer from scratch as code.`

Then: `Worth every hour.` Four words on their own line.

The delta must be a number a manager would recognise:

> `Changes that used to take two hours now take five minutes.`

The internal-beneficiary lines are what make it feel true, because they name roles that
would never appear in a marketing post:

> `Our SEO consultants edit the codebase directly.`
> `Our CMO pushes new pages without opening Figma.`

---

## F. Belief Correction

**Use when:** you have a point of view and nothing to sell.
**Visual pairing:** Node Tree, Flow Map, or no visual at all.

### Skeleton

```
{The belief, stated plainly as other people hold it}.

{Two-word correction}

{What everyone sees, as a short list}

{The reframe: what layer that actually is}

{Where the failure happens}

Because none of it works alone:

→ {X} means nothing without {Y}
→ {X} means nothing if {Y}
... (4 parallel lines)

{Consequence, 2 short lines}

{The common misdiagnosis, quoted}

{What actually happened}

{Aphoristic close: 2 lines with inverted parallelism}

{Repost + follow CTA}
```

### What makes it work

Line length collapses to 3–8 words for most of the post. That vertical rhythm is the
entire aesthetic. Reference:

> `Miss one piece.`
> `The rest gets weaker.`
> `You won't see it on a dashboard.`
> `You'll see it when the numbers stop adding up.`
> `And by then it's expensive.`

The four parallel `→` lines must share an identical grammatical frame. Breaking the
parallelism kills the rhythm.

The close uses inverted parallelism, which is the one rhetorical device this archetype
permits:

> `One strong piece won't save four weak ones.`
> `But one weak piece can sink four strong ones.`

---

## G. Catalogue Tease

**Use when:** you are giving away a large set and the visual can show it.
**Visual pairing:** Specimen Grid, Logo Grid.

The Numbered Inventory's bigger sibling. Inventory lists all N items. Catalogue Tease
shows five, names the number, and lets the visual carry the rest.

### Skeleton

```
{Tool} {does the surprising new thing} now.

{N} {types}, one install, free:

{Item}. {One sentence of what it does, present tense.}
{Item}. {One sentence.}
{Item}. {One sentence.}
{Item}. {One sentence.}
{Item}. {One sentence.}

That is 5 of {N}.

{What the rest covers, 3 short lines}

{Provenance: who built it, licence, proof of scale}

One line installs the lot:

{the literal command}

{How it works, 2 lines}

{What it replaces, as a list of absences}

{What it actually produces, 2 lines}

{Personal use: I do X this way now}

{Link 1}
{Link 2}

{Repost CTA}
```

### What makes it work

**"That is 5 of 42."** One line, on its own, after the samples. It converts a list into
a sample and makes the number feel understated rather than boastful. This is the move
the archetype exists for.

**Each sample is exactly two sentences, subject-first, present tense:**

> `Count-up. A counter runs 0 to 100,000.`
> `Code diff. Red collapses, green expands.`
> `Light leak. A warm flare crosses the frame.`

No adjectives. No benefits. The thing, then what it does. The rhythm is the appeal.

**Provenance in three flat lines.** Who made it, the licence, the proof of scale. Facts
only, no praise:

> `HeyGen built it and open sourced it.`
> `39,000 stars. Apache 2.0. No paywall.`

Verify every number here before posting. This block is the whole credibility of the post
and a wrong star count is the one thing commenters will find.

**Absence list.** Name what the reader no longer needs, as bare nouns:

> `No timeline. No keyframes. No After Effects.`

This is the closest the archetype comes to a contrast, and it works because it never
says what the thing *is* by denying what it is not. It only lists what is gone.

**First-person adoption.** One line, no elaboration:

> `I edit every YouTube video this way now.`

Without it the post is a press release. With it, it is a recommendation.

### Where it breaks

The samples must be genuinely different from each other. Five variations on one idea
makes the reader assume the other 37 are padding. Pick the five that are furthest apart.

## Hook library

Grouped by mechanism. Fill the brackets with something specific.

**Stat as fact**
- `{Practice} gets {N}x more {outcome} than {alternative}.`
- `{Product} has {big number} {things}.`

**Inventory declaration**
- `My {N} (most-used) {things} to {outcome}.`
- `The {N} {things} to replace {big number} {old things}.`

**Decision, past tense**
- `We {killed / rebuilt / moved} our {thing} {timeframe}.`
- `I turned {A} + {B} into a complete {system}.`

**News frame**
- `BREAKING: You can now {capability} on {platform}.`
- `{Product} is back (it's free until {date}).`

**Costly imperative**
- `Delete every {thing} you ever saved.`
- `Save this setup before you {action}:`

**Named social friction**
- `Your boss pretends to read your (ugly) {artifact}.`
- `Most {role}s start with a random {input}.`

**Belief to correct**
- `Most people think {domain} is simple.`
- `People still think you need {barrier} for this.`

**Concrete counterfactual**
- `What if your favourite {people} lived in {tool}?`

**Blocker reveal**
- `{Tool} completely changed how I run {job}. But there's one problem:`

**Capability announcement**
- `{Tool} {does the surprising thing} now.`
- `{N} {types}, one install, free:`

---

## CTA library

One per post. Placed last, after a blank line.

| Type | Wording | Optimises for |
|---|---|---|
| Comment gate | `Comment "{KEYWORD}" and I'll send it over.` | Comments + DMs + connections |
| Bare command | the literal install line, on its own | Adoption. No gate, no friction |
| Triple gate | `→ Add me to your network / → Follow {X} / → Comment "{KEYWORD}"` | Followers |
| Repost | `♻️ Repost this to {benefit to their network}.` | Reach |
| Question | `Which {thing} are you still {gap}?` | Comments |
| Newsletter funnel | `Step 1. Subscribe free at {url}. Step 2. Open the welcome email.` | List growth |
| Credit P.S. | `P.S: {Name} made this analysis. Check their profile.` | Relationship |
| None | — | Authority (Operating Story only) |

Repost lines land hardest when they name the benefit to a third party:
`♻️ Repost this so they stop paying for websites they could build by lunch.`

---

## Banned patterns

These read as AI-written and must never appear in output, English or Arabic.

**Denial then reveal.** Any structure that frames a thing by theatrically rejecting a
smaller thing first:

- `This is not a X. This is a Y.`
- `Not just a X, but a Y.`
- `ده مش X. ده Y.`
- `مش مجرد X، لكنه Y.`
- `هذا ليس X، بل Y.`
- `ليس فقط X بل Y.`

Write the thing directly instead. `The playbook gives a performance marketer a reference
they can open mid-campaign when the numbers move.`

**Em dashes.** Use a period and a line break.

**Buzzwords.** unleash, unlock, harness, leverage, optimize, revolutionize,
game-changing, cutting-edge, state-of-the-art, next-generation, elevate, innovative,
groundbreaking, seamless, effortless, the power of, empower, transform, disrupt,
maximize, streamline, synergy, paradigm shift, robust, scalable, best-in-class,
world-class, industry-leading, unparalleled, unprecedented.

**Hedged openers.** "In today's fast-paced world", "Let's dive in", "Here's the thing",
"The reality is".

**Rhetorical question stacks.** More than one question mark before the CTA.

### Self-check before output

Read every line. If a line can be reduced to "not X, but Y", delete it and write the
positive statement. If a line contains a banned word, rewrite the line, do not swap
synonyms. If line 1 exceeds 60 characters, cut it.
