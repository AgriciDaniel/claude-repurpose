---
name: repurpose-discord
description: >
  Generates Discord community content from content atoms: announcement posts for
  channels, discussion thread prompts designed for reply-generation, and rich embed
  messages with structured fields. Enforces casual peer tone, reaction prompts, and
  conversation-first design. Sub-skill of the Content Repurposing Engine. Use when
  user says "discord", "discord post", "discord announcement", "discord thread",
  or "repurpose for discord".
user-invokable: true
argument-hint: "[url-or-atoms]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Discord Community Content Generator

Generate announcement post, discussion thread prompt, and rich embed message from content atoms.

## Inputs

Received from the parent agent (`repurpose-community`):

| Input | Description |
|-------|-------------|
| `atoms` | Full list of content atoms with types and impact ratings |
| `main_argument` | One-sentence thesis of the source content |
| `target_audience` | Who benefits from this content |
| `primary_topic` | Category or niche |
| `voice_profile` | Detected or overridden brand voice |
| `brief_mode` | If true, produce announcement post only |

## References

Load before generating:

- `references/platform-specs.md` -- Discord specs, message limits, embed constraints
- `references/hook-formulas.md` -- question hooks, contrarian openers, reaction prompts
- `references/voice-adaptation.md` -- Discord tone rules (casual, peer, emoji-friendly)

## Platform Rules

| Spec | Value |
|------|-------|
| Message limit | 2,000 characters per message |
| Embed title | 256 characters max |
| Embed description | 4,096 characters max |
| Embed fields | Up to 25 fields |
| Embed color | Hex code (mood-based) |
| Markdown | Full support (bold, italic, code blocks, lists, headers via ##) |
| Threads | Auto-create from any message, unlimited replies |
| Reactions | Lightweight polls and engagement signals |
| Images | Up to 10 per message, any aspect ratio |
| Best posting | Weekdays 3-8 PM EST (after school/work hours) |

## Core Principle

Discord is about **CONVERSATION**, not broadcasting. Every post should invite a specific response. Silent posts get buried by the scroll. Design every output for reply-generation -- ask questions, prompt reactions, spark debate. A post with zero replies is a failed post.

## Output 1: Announcement Post

Write to `discord/announcement.md`.

Formatted message for a #general or #announcements channel. Must stay under 2,000 characters.

### Announcement Structure

1. **Bold headline** (1 line)
   - Lead with the strongest insight or most surprising atom
   - Use `**bold**` markdown for the opening line
   - Keep it punchy: 8-15 words max

2. **Body** (2-3 short paragraphs)
   - Expand on the headline with context from 2-3 atoms
   - Short paragraphs (2-3 sentences each)
   - Use line breaks between paragraphs for readability
   - Contractions and casual language throughout

3. **Bullet point takeaways** (3-5 items)
   - Pull the most actionable or surprising atoms
   - Each bullet is one clear thought
   - Use emoji bullets where natural (not forced)

4. **Reaction prompt** (final line)
   - Drive engagement through reactions: "React with :fire: if you've experienced this"
   - Or a direct question: "Drop your take below -- what's YOUR experience with this?"
   - Never end without a clear engagement hook

### Announcement Rules
- Total length under 2,000 characters (hard Discord limit)
- No walls of text -- Discord users skim aggressively
- At least one reaction prompt OR direct question
- Bold the most important phrase in each paragraph

## Output 2: Discussion Thread Prompt

Write to `discord/thread-prompt.md`.

Message designed to start a thread. Opens conversation, not delivers a lecture.

### Thread Prompt Structure

1. **Opening hook** (1-2 sentences)
   - Use a contrarian take, surprising stat, or provocative question from the atoms
   - Frame as your own observation or question, not a teaching moment
   - "Okay so ngl, I just learned something that kinda broke my brain..."

2. **Context** (2-3 sentences)
   - Provide just enough background for people to form an opinion
   - Don't explain everything -- leave gaps that invite people to fill in

3. **Specific invitation** (1-2 sentences)
   - NOT "What do you think?" (too generic, gets ignored)
   - Instead: "Drop your take below -- have y'all run into this?"
   - Or: "Genuinely curious -- does this match your experience or am I way off?"
   - Frame it so members share personal experience, not just agreement

### Thread Prompt Rules
- Under 1,000 characters (shorter = more replies)
- Must contain at least one direct question
- Designed for ongoing conversation, not one-and-done reactions
- Leave room for disagreement -- don't present a settled conclusion

## Output 3: Embed Message

Write to `discord/embed.md`.

Rich embed format for bot-posted or webhook content.

### Embed Structure

1. **Title** (256 chars max)
   - Bold insight or key finding from the strongest atom
   - Concise and curiosity-driving

2. **Description** (under 4,096 chars)
   - Expanded context around the title insight
   - 2-3 short paragraphs with Discord markdown formatting
   - Include the "so what" -- why this matters to the community

3. **Color** (hex code)
   - Match the content mood:
     - `#FF6B6B` -- urgent, warning, contrarian
     - `#4ECDC4` -- tips, how-to, educational
     - `#FFE66D` -- insight, discovery, new finding
     - `#95E1D3` -- community, discussion, collaborative
     - `#A8E6CF` -- success, case study, positive result

4. **Fields** (3-5 key takeaways)
   - Each field has a `name` (bold label) and `value` (brief explanation)
   - One atom per field
   - Keep field values under 100 characters for clean formatting
   - Use `inline: true` for side-by-side fields where appropriate

5. **Footer**
   - Source attribution: "Source: [original content title or URL]"
   - Timestamp if relevant

### Embed Format Template

```markdown
**Embed Title:** [insight or finding]
**Color:** #[hex]

**Description:**
[2-3 paragraphs of context]

**Fields:**
- **[Takeaway 1 Label]:** [brief value]
- **[Takeaway 2 Label]:** [brief value]
- **[Takeaway 3 Label]:** [brief value]

**Footer:** Source: [attribution]
```

## Tone Rules

| Do | Do NOT |
|----|--------|
| Use "y'all", "ngl", "tbh", contractions | Use formal language or corporate speak |
| Include emoji naturally (not excessively) | Force emoji into every sentence |
| Write like a peer sharing something cool | Write like a brand broadcasting content |
| Ask specific questions that invite replies | Use generic "Thoughts?" or "Agree?" |
| Use Discord markdown (bold, code blocks) | Write plain unformatted text walls |
| Reference community inside jokes if known | Assume knowledge of the community culture |
| Keep paragraphs short (2-3 sentences max) | Write essay-length paragraphs |
| Use reaction prompts for quick engagement | Ignore engagement hooks entirely |

## Output Format

```markdown
# Discord Announcement: [Topic]

[Full message text]

---
**Channel suggestion:** #[recommended channel type]
**Best posting time:** Weekdays 3-8 PM EST
**Engagement strategy:** [reaction prompt, thread follow-up plan]
**Character count:** [count]/2000
```

## Brief Mode

If `--brief` is active, produce only:
- 1 announcement post (most versatile format)
- Skip thread prompt and embed

## Error Handling

| Condition | Action |
|-----------|--------|
| Fewer than 3 atoms | Write shorter announcement (under 1,000 chars); skip thread and embed |
| No `contrarian` or `question` atoms | Use `insight` + `howto` atoms; frame announcement as a tip share |
| `brief_mode` is true | Generate announcement only; skip thread prompt and embed |
| Content too formal for Discord tone | Rewrite with casual language, contractions, and peer framing |
| Promotional content detected | Reframe as community value -- "found this useful, thought y'all might too" |
