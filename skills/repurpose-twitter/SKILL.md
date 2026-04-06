---
name: repurpose-twitter
description: >
  Generates Twitter/X content from content atoms: threaded breakdowns (8-12 tweets),
  standalone tweets (3-5 variations), and engagement polls. Optimizes for reply-driven
  reach, curiosity-gap hooks, and algorithm-friendly formatting. Sub-skill of the
  Content Repurposing Engine. Use when user says "twitter", "tweet", "X post",
  "thread", "tweet thread", or "repurpose for twitter".
user-invokable: true
argument-hint: "[url-or-atoms]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Twitter/X Content Generator

Generate thread, standalone tweets, and poll from content atoms.

## Inputs

You receive from the orchestrator:
- **Content atoms** (typed and impact-rated)
- **Main argument**, target audience, primary topic
- **Brand voice profile** (5-dimension scores or override flag)
- **Flags**: `--brief` (1 tweet only), `--images` (generate image prompts)

## References

Load before generating:
- `references/platform-specs.md` -- character limits, algorithm weights, posting times
- `references/hook-formulas.md` -- curiosity gap, contrarian, data-driven, question hooks
- `references/voice-adaptation.md` -- Twitter tone rules (concise, punchy, no hedging)

## Platform Rules

| Spec | Value |
|------|-------|
| Character limit | 280 (standard), 25,000 (Premium) |
| Sweet spot | 71-100 characters for highest engagement |
| Thread length | 8-12 tweets (+63% impressions vs single) |
| Hashtags | 0-2 max per tweet (more = lower reach) |
| Algorithm | Reply = 27x a like; Conversation = 150x a like |
| External links | Near-zero reach for non-Premium accounts |
| Images | 1600x900 (16:9), up to 4 per tweet |
| Best time | Tuesday 9AM, generally 8-10AM weekdays |

## Output 1: Thread (8-12 Tweets)

Write to `twitter/thread.md`.

### Thread Structure

1. **Hook tweet** (tweet 1)
   - Must work as a standalone tweet even if nobody expands the thread
   - Use a curiosity gap OR bold stat from the highest-impact atom
   - End with `:` or `A thread:` to signal continuation
   - Never open with "Thread:" or "1/"
   - 71-100 characters is the sweet spot

2. **Insight tweets** (tweets 2-9)
   - One key point per tweet, drawn from individual atoms
   - Number each tweet for scannability (`2/` prefix)
   - Use line breaks between ideas within a single tweet
   - Alternate between stat, insight, contrarian, and howto atoms
   - Insert a **visual break** every 3-4 tweets: a one-liner quote, a question, or an image suggestion

3. **Closing tweet** (final tweet)
   - Summarize the main argument in one sentence
   - Include a clear CTA: follow, repost, reply, or bookmark
   - If a link is needed: suggest placing it in a **reply** to the final tweet (not in the tweet body) to avoid reach suppression
   - For non-Premium accounts, alternatively suggest "link in bio"

### Thread Rules
- Each tweet must be under 280 characters
- Thread should flow logically even if individual tweets are read in isolation
- Frame at least 2 tweets as questions or contrarian takes to invite replies (Reply = 27x like)
- Do not repeat the same hook formula twice in one thread

## Output 2: Standalone Tweets (3-5)

Write to `twitter/standalone-tweet.md`.

Generate 3-5 standalone tweets. Each one:
- Captures a single atom and works completely independently
- Uses a different format from the others:
  - **Stat tweet**: leads with a number or data point
  - **Question tweet**: asks a thought-provoking question
  - **Hot take tweet**: bold/contrarian claim that invites debate
  - **Tip tweet**: one actionable piece of advice
  - **Analogy tweet**: comparison that makes the concept click
- Stays within the 71-100 character sweet spot when possible (never exceed 280)
- Includes 0-1 hashtags maximum

### Engagement Optimization
- Frame for replies, not likes. Questions and contrarian takes generate 27x more algorithmic weight than passive likes.
- Tweets that invite disagreement or personal experience outperform agreement-bait.
- Avoid "Agree?" or "Thoughts?" -- ask a specific question instead.

## Output 3: Poll

Write to `twitter/poll.md`.

Derive one poll from the content's key decision point or debatable topic.

| Spec | Constraint |
|------|-----------|
| Options | 2-4 |
| Chars per option | 25 maximum |
| Duration | Suggest 24h or 7 days |

**Poll structure:**
- Question: specific, not generic (derived from the content's central tension or choice)
- Options: represent real positions; include one surprising/contrarian option
- Context tweet: 1-2 sentences above the poll that frame why this question matters

## External Link Warning

Links in tweet bodies receive near-zero reach for non-Premium accounts. Always:
1. Place links in a **reply** to the main tweet (not the tweet body)
2. Or suggest "Link in bio" with a directional cue
3. Note this in the output so the user understands the trade-off

## Image Prompts

If `--images` flag is set, suggest one hero image for the thread opener:
- Dimensions: 1600x900 (16:9)
- Purpose: visual hook for tweet 1 of the thread
- Include a prompt description for /banana (subject, context, style, composition)

## Output Format

Each output file should use this structure:

```markdown
# Twitter Thread: [Topic]

## Hook Tweet
[tweet text]

## Tweet 2/N
[tweet text]

...

## Closing Tweet
[tweet text]

---
**Posting notes:** [best time, link placement advice, image suggestions]
```

## Brief Mode

If `--brief` is active, produce only:
- 1 standalone tweet (highest-impact atom)
- Skip thread and poll
