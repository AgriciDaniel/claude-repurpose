---
name: repurpose-threads
description: >
  Generates Meta Threads content from content atoms: threaded breakdowns (5-10 posts),
  standalone posts (3-5 variations), and image post concepts. Optimizes for engagement,
  shares, and conversational authenticity. Sub-skill of the Content Repurposing Engine.
  Use when user says "threads", "threads post", "threads thread", "meta threads",
  or "repurpose for threads".
user-invokable: true
argument-hint: "[url-or-atoms]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Threads Content Generator

Generate thread, standalone posts, and image post concept from content atoms.

## Inputs

You receive from the orchestrator:
- **Content atoms** (typed and impact-rated)
- **Main argument**, target audience, primary topic
- **Brand voice profile** (5-dimension scores or override flag)
- **Flags**: `--brief` (1 post only), `--images` (generate image prompts)

## References

Load before generating:
- `references/platform-specs.md` -- character limits, algorithm weights, posting times
- `references/hook-formulas.md` -- curiosity gap, opinion-led, question hooks
- `references/voice-adaptation.md` -- Threads tone rules (casual, conversational, authentic)

## Platform Rules

| Spec | Value |
|------|-------|
| Character limit | 500 per post |
| Thread length | Unlimited posts (5-10 optimal) |
| Images | Up to 10 per post, 1080x1350 (4:5) or 1080x1080 (1:1) |
| Video | Up to 5 min, 1080x1920 (9:16) |
| Algorithm | Engagement + shares + follows from post |
| Links | NO suppression (unlike Twitter -- use freely in-body) |
| Hashtags | Not supported as discovery mechanism (use keywords in text instead) |
| Best time | Tuesday/Thursday 10AM-1PM |

## Output 1: Thread (5-10 Posts)

Write to `threads/thread.md`.

### Thread Structure

1. **Hook post** (post 1)
   - Must work as a standalone post even if nobody reads the rest
   - Use an opinion-led hook or bold claim from the highest-impact atom
   - Conversational opener -- feels like the start of a story, not a lecture
   - Under 500 characters; aim for 100-200 for maximum punch
   - Never open with "Thread:" or "1/"

2. **Insight posts** (posts 2-8)
   - One key point per post, drawn from individual atoms
   - No hashtags -- weave keywords naturally into the text
   - Links allowed in-body (no reach penalty, unlike Twitter)
   - Use line breaks for readability within a single post
   - Alternate between insight, story, contrarian, and data atoms
   - Insert a **breather post** every 3-4 posts: a one-liner opinion, rhetorical question, or relatable observation

3. **Closing post** (final post)
   - Summarize the main argument in one conversational sentence
   - Include a clear CTA: follow, repost, or reply
   - End with a question that invites personal experience (community-building)

### Thread Rules
- Each post must be under 500 characters
- Thread should flow like a conversation, not a listicle
- Frame at least 2 posts as opinions or questions to invite replies
- Links can go directly in-body -- no need for "link in bio" workarounds
- Do not use hashtags anywhere in the thread (Threads does not use them for discovery)

## Output 2: Standalone Posts (3-5)

Write to `threads/standalone-posts.md`.

Generate 3-5 standalone posts. Each one:
- Captures a single atom and works completely independently
- Uses a different format from the others:
  - **Opinion post**: first-person take that invites agreement or pushback
  - **Question post**: asks the community for their experience
  - **Story post**: short personal-feeling anecdote or observation
  - **Tip post**: one actionable piece of advice, conversational delivery
  - **Hot take post**: bold claim designed to spark discussion
- Stays under 500 characters (sweet spot: 150-300)
- No hashtags; weave keywords naturally into text
- Links allowed where relevant

### Tone Rules

| Do | Don't |
|----|-------|
| Write like you're texting a smart friend | Write like a brand account |
| Use first-person and contractions | Use corporate jargon or hedging |
| Share opinions confidently | Be vague or non-committal |
| Ask genuine questions | Use "Thoughts?" or "Agree?" |
| Include links freely in-body | Hide links or use "link in bio" |
| Keep it casual and conversational | Over-polish or sound scripted |

## Output 3: Image Post Concept

Write to `threads/image-post.md`.

Design one visual post concept that pairs an image with a caption.

### Image Post Structure

1. **Image direction**
   - Dimensions: 1080x1350 (4:5) or 1080x1080 (1:1)
   - Visual concept description (subject, mood, style)
   - Text overlay suggestion (if applicable): 5-8 words max, bold and readable
   - Include /banana prompt description if `--images` flag is set

2. **Caption** (under 500 characters)
   - Complements the image -- adds context the visual cannot convey
   - Conversational tone, first-person
   - Ends with a question or CTA

3. **Posting note**
   - Why this visual + text combination works for the topic
   - Suggested post timing

## Image Prompts

If `--images` flag is set, suggest:
- **Image post**: 4:5 (1080x1350) or 1:1 (1080x1080) visual concept
- Include /banana prompt description (subject, context, style, composition)

## Output Format

Each output file should use this structure:

```markdown
# Threads Thread: [Topic]

## Post 1 -- Hook
[post text]

## Post 2
[post text]

...

## Closing Post
[post text]

---
**Posting notes:** [best time, link placement, engagement strategy]
```

## Brief Mode

If `--brief` is active, produce only:
- 1 standalone post (highest-impact atom, opinion-led)
- Skip thread and image post concept

## Error Handling

| Condition | Action |
|-----------|--------|
| Fewer than 5 atoms | Shorten thread to match available atoms; minimum 3 posts |
| Content too technical | Simplify language; Threads audience expects casual tone |
| No clear opinion angle | Frame insights as "Here's what most people miss..." |
| `--images` but no /banana | Save prompt to file; note for manual generation |
| Content has no links | Omit link references; focus on text-only engagement |
| Atoms lack conversational tone | Rewrite in first-person casual voice; preserve meaning |
