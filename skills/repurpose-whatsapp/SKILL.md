---
name: repurpose-whatsapp
description: >
  Generates WhatsApp Channel content from content atoms: concise channel updates,
  conversational polls, and content teasers. Optimizes for personal tone, mobile-first
  readability, and permission-based engagement. Sub-skill of the Content Repurposing
  Engine. Use when user says "whatsapp", "whatsapp channel", "whatsapp broadcast",
  "whatsapp update", or "repurpose for whatsapp".
user-invokable: true
argument-hint: "[url-or-atoms]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# WhatsApp Channel Content Generator

Generate a channel update, poll, and content teaser from content atoms.

## Inputs

You receive from the orchestrator (`repurpose-broadcast`):

| Input | Description |
|-------|-------------|
| `atoms` | Full list of content atoms with types and impact ratings |
| `main_argument` | One-sentence thesis of the source content |
| `target_audience` | Who benefits from this content |
| `primary_topic` | Category or niche |
| `voice_profile` | Detected or overridden brand voice |
| `brief_mode` | If true, produce channel update only |

## References

Load before generating:

- `references/platform-specs.md` -- character limits, formatting, posting cadence
- `references/hook-formulas.md` -- curiosity gap and personal-tone openers
- `references/voice-adaptation.md` -- WhatsApp tone rules (personal, direct, emoji-driven)

## Platform Rules

| Spec | Value |
|------|-------|
| Channel update limit | 2048 chars |
| Formatting | NO markdown; emoji-driven structure; liberal line breaks |
| Images | 1 per update, any ratio (1080x1080 square recommended) |
| Polls | Single question, up to 12 options |
| Links | Supported, show preview |
| Algorithm | Chronological (no algorithmic feed) |
| Cadence | 2-3x per week max (overposting = permanent unsubscribes) |
| Best time | 8-9 AM and 6-8 PM (commute windows) |

## Core Principle: Permission-Based and Personal

WhatsApp is the most personal platform -- content lands in the same app as family
and friends messages. Every update must deliver enough value that the reader does
not mute the channel. Overposting causes permanent unsubscribes. Quality over
frequency, always.

## Output 1: Channel Update

**File:** `whatsapp/update.md`

**Length:** 100-300 chars.

**Structure:**
1. **Emoji opener** -- Single emoji signaling topic or mood.
2. **Key insight** -- 1-2 sentences with the single most valuable takeaway.
   Must feel like a personal message, not a broadcast. Mobile-first.
3. **Value hook** -- One line on why this matters to the reader.
4. **Link** (if applicable) -- Bare URL or short context + URL.

**Rules:**
- Write as if texting ONE person; use "you" and "I"
- Short sentences, line breaks between every thought
- No formal language, no corporate feel
- Emoji as paragraph markers (1-2 per update max)

## Output 2: Poll

**File:** `whatsapp/poll.md`

| Spec | Constraint |
|------|-----------|
| Options | 2-4 (under 25 chars each) |
| Max options | 12 (platform limit) |
| Question | Conversational, derived from content |

**Poll structure:**
- **Context message**: 1-2 sentences framing why this question matters.
- **Question**: Specific, conversational. Write as if asking a friend.
- **Options**: Real positions, under 25 chars each. Include one lighthearted option.

## Output 3: Content Teaser

**File:** `whatsapp/teaser.md`

**Length:** 200-500 chars.

**Structure:**
1. **Curiosity hook** -- One line creating an information gap.
2. **Bullet points** -- 2-3 emoji-bulleted items of what they will learn.
3. **Link** -- Full URL to original content.
4. **Emoji CTA** -- Single-line casual call-to-action.

## Tone Rules

| Do | Do NOT |
|----|--------|
| Write like texting a friend | Write like a newsletter |
| Use "you" and "I" | Use "we are pleased to announce" |
| Use emoji as paragraph markers | Overload with emoji (max 3-4) |
| Keep sentences under 15 words | Write multi-clause sentences |
| Line breaks between every thought | Write dense paragraphs |
| Deliver value in every message | Post just to stay visible |

## Output Format

```markdown
# WhatsApp Channel Update: [Topic]

[Full update text with emoji formatting and line breaks]

---
**Posting notes:** [best time, cadence reminder, link preview note]
```

## Brief Mode

If `--brief` is active, produce only:
- 1 channel update (highest-impact atom, shortest format)
- Skip poll and teaser

## Error Handling

| Condition | Action |
|-----------|--------|
| Fewer than 3 atoms | Single update only (shortest format) |
| No `stat` atoms | Use `insight` + question framing |
| `brief_mode` is true | Generate update only; skip poll and teaser |
| Content too formal | Aggressively rewrite to casual, personal tone |
| Content is promotional | Reframe as tip or insight; strip product mentions |
| Long content | Extract single best takeaway for update |
