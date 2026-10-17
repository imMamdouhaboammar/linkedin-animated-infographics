# Anti-Slop and Direct Execution Standards

These standards govern all copywriting, content creation, visual layout composition, and automated quality gates across this workspace

## 1 Direct Writing Protocol and Four-Part Declaration Formula

Always construct headlines, product copy, ad creatives, and explanatory annotations using this four-part sequence:

```
1 Explicit Definition: State exactly what the product or deliverable is
2 Target Role: Identify the exact practitioner or audience it serves
3 Operational Context: Define the exact moment or scenario of use
4 Practical Outcome: Detail the specific decision or action it executes
```

## 2 Hard Ban on Negative Setup and Positive Reveal Structures

Never write sentences with binary contrast framing pairing negative setups with positive reveals

### Banned Patterns

Arabic:
- `ده مش ... ده ...`
- `هذا ليس ... بل ...`
- `مش مجرد ... لكنه ...`
- `ليس فقط ... بل ...`
- `لا نتحدث عن ... نحن نتحدث عن ...`
- `مش X ده Y`
- `الفرق مش ... الفرق كذا`

English:
- `Not a ... but a ...`
- `This is not ... this is ...`
- `Not just ... it is ...`
- `We are not talking about X, we are talking about Y`
- `Here is the thing`
- `Let us be clear`
- `What most people get wrong`
- `The deeper truth`

## 3 Prohibited Vocabulary and Functional Replacements

Avoid using the following words; replace them with concrete operational terms:

Arabic:
- Prohibited: `نظام`, `أنظمة`, `سيستم` -> Approved: `دليل عمل`, `مرجع`, `منهجية`, `إطار عمل`, `مسار`, `بنية`
- Prohibited: `طبقة`, `طبقات` -> Approved: `مستويات`, `عناصر`, `أجزاء`, `نطاقات`
- Prohibited: `ماكينة` -> Approved: `وسيلة`, `أداة`, `طريقة`, `حزمة`
- Prohibited: `ترس`, `تروس` -> Approved: `عنصر`, `جزء`, `ركيزة`, `محرك`
- Prohibited: `احتلال`, `احتل` -> Approved: `تصدر`, `استحواذ`, `وصول`, `تفوق`
- Prohibited: `الفرق` -> Approved: `التباين`, `المقارنة`, `الميزة المحددة`, `الأثر الفعلي`, `المعيار الحقيقي`

English:
- Prohibited: `system`, `systems` -> Approved: `framework`, `workflow`, `protocol`, `playbook`, `guidelines`, `infrastructure`
- Prohibited: `layer`, `layers` -> Approved: `tier`, `level`, `zone`, `element`, `surface`
- Prohibited: `machine`, `machines` -> Approved: `engine`, `pipeline`, `toolkit`, `suite`, `generator`
- Prohibited: `gear`, `gears`, `cog`, `cogs` -> Approved: `driver`, `lever`, `component`, `building block`
- Prohibited: `occupy`, `dominate` -> Approved: `capture`, `expand reach`, `lead the category`, `convert demand`
- Prohibited: `difference`, `the difference` -> Approved: `operational variance`, `distinct edge`, `performance gap`, `core advantage`, `measurable delta`

## 4 Punctuation and Formatting Invariants

- No period mark `.` at the end of sentences, bullet items, or titles
- No quotation marks `"` unless strictly unavoidable
- No em dash `—` or en dash `–`

## 5 Visual Anti-Slop Discipline

- **No Bento Box Clutter**: Remove random decorative icons; let structure convey meaning
- **No Background Grids**: Remove wireframe lines, dot matrices, or particle meshes
- **No Pulsing Biscuit Pills**: Remove animated pulsing dots on status badges
- **No Keyword Gradient Fills**: Use font weight or primary palette tokens instead
- **No Card Over-Nesting**: Limit visual containment to a single defined boundary
- **No Neon Purple on Dark Themes**: Maintain restrained contrast palettes with approved contrast ratios

## 6 Mandatory TypeScript & JavaScript Code Anti-Slop Discipline

Enforce the `install-anti-slop` Oxlint rules on all TypeScript/JavaScript projects:
- `anti-slop/no-chained-type-assertions`: Reject chained type assertions (`as unknown as T`)
- `anti-slop/no-conditional-empty-object-spread`: Reject `{ ...(cond ? a : {}) }`
- `anti-slop/no-known-value-widening`: Reject widening known types to generic primitives
- `anti-slop/no-module-mocking`: Reject runtime monkey-patching and module mocking in tests
- `anti-slop/no-unsafe-dictionary-type`: Enforce strict key/value record typing
- `anti-slop/require-safety-comment-for-type-assertion`: Mandate safety rationale for every explicit type cast

## 7 Universal Doctrine: Direct Payload and Zero Affordance Narration Invariant

Transition directly from domain headers to technical payloads (tables, code blocks, schemas, media) with zero transitional conversational fluff:
- **Zero Affordance Coaching**: Never explain standard interaction mechanics (e.g. how to play videos, expand accordions, copy blocks, or scroll); label items strictly by technical identity, never user action coaching
- **Zero Conversational Preambles**: Ban meta-transitional phrases before payloads (e.g. "The following table outlines...", "In this section we will explore...", "Below is a code snippet...")
- **Zero Bilingual Title-Stacking**: Never duplicate identical concepts side-by-side in English and Arabic in headings (`Title · الترجمة`)
- **Zero Mechanical Hand-Holding**: Never treat engineers as computer novices (e.g. "open your terminal", "save the file before running")
- **Zero Superlative Inflation**: Never label mundane artifacts as "Live Interactive Showcases" or small scripts as "Enterprise Scalable Pipelines"

## 8 The Zero-Obviousness & Anti-Truism Doctrine

High engineering discipline values silence over noise:
- **Zero Syntax Narration**: Ban line-by-line syntax commentary in comments (`// increment counter`, `// check if null`, `// return result`); comments must document non-obvious invariants and architectural rationales only
- **Zero Tautological Docstrings**: Ban docstrings merely restating function/variable names without adding error contracts, concurrency guarantees, units, or null semantics
- **Zero Patronizing UI Microcopy**: Ban redundant instructional labels beneath obvious UI inputs and buttons (`"Please enter your email"`, `"Click here to submit"`)
- **Zero Speculative Platform Dossiers**: Never invent unprompted third-party platform submission guides, fake reviewer packets, or dead distribution URLs (`docs/OPENAI_SUBMISSION.md`, `platform.openai.com/plugins`)

## 9 The Canonical Grounding & Authority Invariant

Never improvise scaffolding or dependencies:
- Rely strictly on official CLI installers, generators, and starter boilerplates (`uv init`, `cargo new`, `bun create`) rather than hand-crafting directory layouts or configs from LLM memory
- Query package registries and pin verified latest stable releases strictly; never guess outdated version strings

## 10 The Audience Boundary & Zero Meta-Leakage Invariant

Complete physical isolation between internal engineering context and external user-facing surfaces:
- Never render internal developer instructions, agent reminders, mock data banners, or architecture apologies into user-visible DOM/JSX
- Keep internal engineering commentary strictly in code comments or design docs

## 11 The Visual Restraint & Single-Purpose Density Invariant

Every visual element must justify its existence through a distinct, non-redundant primary user objective:
- Prohibit cosmetic clutter masquerading as functionality: overcrowded headers/navbars, multi-row icon spam, repetitive buttons, nested card shells, ornamental badges
- Prioritize purposeful white space, visual hierarchy, and quiet functional utility
