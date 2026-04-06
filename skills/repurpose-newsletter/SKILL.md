---
name: repurpose-newsletter
description: >
  Generates newsletter excerpts, subject line variants, and 3-email drip
  sequences from atomized content. Produces inbox-optimized copy with
  open-rate-tested subject formulas, preview text, personal tone, and
  single-CTA discipline per email. Sub-skill of the Content Repurposing Engine.
  Use when user says "newsletter", "email sequence", "drip sequence",
  "subject lines", or "repurpose for email".
user-invokable: true
argument-hint: "[url-or-atoms]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Newsletter and Email Sequence Generator

Produce a newsletter excerpt, 3 subject line options, and a 3-email drip sequence
from the content atoms provided by the orchestrator.

## Inputs

Received from the parent agent (`repurpose-longform`):

| Input | Description |
|-------|-------------|
| `atoms` | Full list of content atoms with types and impact ratings |
| `main_argument` | One-sentence thesis of the source content |
| `target_audience` | Who benefits from this content |
| `primary_topic` | Category or niche |
| `voice_profile` | Detected or overridden brand voice |
| `brief_mode` | If true, produce excerpt + 1 subject line only |

## References

Load these before generating any output:

- `references/voice-adaptation.md` -- tone rules for email/newsletter
- `references/hook-formulas.md` -- subject line and opener formulas
- `references/engagement-benchmarks.md` -- open rate and CTR targets

## Output 1: Newsletter Excerpt

**File:** `newsletter/newsletter.md`

**Length:** 150-200 words.

**Structure:**

1. **Opening line** -- Lead with the single most valuable insight from the atoms.
   Do NOT open with "Hi [name]" or "In this week's issue." Start with the insight.
2. **Body** -- 2-3 short paragraphs (2-4 sentences each). **Bold key phrases** for
   scanners. Use contractions and first-person where the voice allows.
3. **Exclusive feel** -- Frame the content as something the reader gets before
   everyone else: "Before I shared this anywhere else..." or "This one's just for
   the list."
4. **Single CTA** -- One clear call-to-action at the end. Link text should describe
   the outcome, not the action ("See the full breakdown" not "Click here").

**Rules:**
- Short paragraphs (max 3 sentences)
- No walls of text
- Bold 2-3 key phrases
- Exactly one CTA
- Personal, not corporate

## Output 2: Subject Lines

**File:** `newsletter/subject-lines.md`

Generate exactly 3 subject line variants, each using a different formula.

### Variant 1: Number-Driven (+57% open rate lift)

**Formula:** `[Number] [insights/lessons/mistakes] from [topic] that [changed/revealed/broke] [outcome]`

**Examples:**
- "5 insights from content repurposing that doubled my reach"
- "3 mistakes in email marketing that cost me 2,000 subscribers"

**Rules:** 40-60 characters. Must contain a specific number. Outcome must be concrete.

### Variant 2: Question Hook

**Formula:** `Are you [making/missing/ignoring] this [topic] [mistake/opportunity/signal]?`

**Examples:**
- "Are you making this LinkedIn mistake?"
- "Are you ignoring this SEO signal?"

**Rules:** 40-60 characters. Must be a yes/no question. Should trigger self-doubt.

### Variant 3: Curiosity Gap

**Formula:** `[Topic]: what most [audience] get wrong`

**Examples:**
- "Content repurposing: what most creators get wrong"
- "Newsletter growth: what most marketers miss"

**Rules:** 40-60 characters. Must imply a knowledge gap. No clickbait -- the email must deliver.

### Preview Text

For each subject line, generate matching preview text:
- 40-90 characters
- Complements the subject -- does NOT repeat it
- Adds a second reason to open
- Example subject: "5 insights that changed my content game"
- Example preview: "Plus the one tool I wish I'd found sooner."

## Output 3: Email Drip Sequence

**File:** `newsletter/email-sequence.md`

Generate a 3-email sequence. Each email has: subject line, preview text, body, and CTA.

### Email 1 -- Day 0: Immediate Value

**Goal:** Deliver the best insight instantly. Build trust.

| Element | Spec |
|---------|------|
| Subject | Use Number-Driven formula |
| Tone | "Here's what I learned" -- personal discovery |
| Body | 200-300 words |
| Content | Lead with the highest-impact atom. One supporting point. |
| CTA | Soft -- "Reply and tell me if this matches your experience" |

**Structure:**
1. Hook (1 sentence -- the key insight)
2. Context (2-3 sentences -- why this matters)
3. The insight expanded (2-3 sentences)
4. CTA (1 sentence -- reply or read more)

### Email 2 -- Day 2: Deeper Dive

**Goal:** Expand context. Tell a story or share a case study.

| Element | Spec |
|---------|------|
| Subject | Use Question Hook formula |
| Tone | "Let me show you what I mean" -- teacher mode |
| Body | 300-500 words |
| Content | Story, case study, or expanded framework from the atoms |
| CTA | Medium -- "Here's the full breakdown" (link to original content) |

**Structure:**
1. Callback to Email 1 (1 sentence -- "Remember when I said...")
2. Story or case study (3-4 paragraphs)
3. Key lesson distilled (1-2 sentences)
4. CTA (1 sentence -- link to original)

### Email 3 -- Day 4: Action CTA

**Goal:** Drive a specific next step. Create gentle urgency.

| Element | Spec |
|---------|------|
| Subject | Use Curiosity Gap formula |
| Tone | "Here's exactly what to do" -- coach mode |
| Body | 200-400 words |
| Content | Actionable steps derived from howto/insight atoms |
| CTA | Strong -- specific action with urgency element |

**Structure:**
1. "If you've been following along..." (1 sentence)
2. 3-5 concrete steps (bulleted, brief)
3. Urgency element ("This week only" / "Before the algorithm shifts" / time-bound)
4. CTA (1 sentence -- specific action)

## Rules for All Emails

- **Short paragraphs**: 1-3 sentences max per paragraph
- **One CTA per email**: Never compete with yourself
- **Personal tone**: Write like one person to one person. Use "I" and "you."
- **200-500 words per email**: Respect inbox time
- **No image-heavy layouts**: Text-first for deliverability
- **P.S. line optional**: Use for a secondary hook or human aside

## Error Handling

| Condition | Action |
|-----------|--------|
| Fewer than 3 atoms | Generate excerpt + 1 email only; skip sequence |
| No `quote` or `insight` atoms | Synthesize from `tldr` and `howto` atoms |
| `brief_mode` is true | Generate excerpt + 1 subject line; skip sequence |
| Voice profile unclear | Default to professional; note in output header |
