---
name: repurpose-reddit
description: >
  Generates Reddit discussion posts adapted to subreddit culture and norms.
  Produces peer-to-peer, non-promotional content with genuine discussion
  prompts and subreddit-specific recommendations.
user-invokable: false
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Reddit Discussion Post Generator

Produce a subreddit-ready discussion post and 2-3 targeted subreddit suggestions
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
| `brief_mode` | If true, produce post only (skip subreddit analysis) |

## Core Principle: The 10% Self-Promotion Rule

Reddit communities enforce a rough 90/10 rule: 90% of your posts should be
genuine contributions, 10% can reference your own work.

**What this means for output:**
- Position the author as a **contributor**, never a marketer
- The post must deliver standalone value -- a reader who never clicks a link
  should still learn something
- Any link to the original content goes at the **bottom**, framed naturally
- Never use phrases like "check out my blog" or "I wrote an article about this"
- Instead: "I put together a longer breakdown here if anyone wants the details: [link]"

## Output 1: Discussion Post

**File:** `reddit/post.md`

### Title

- **Max 300 characters** (Reddit's limit)
- Frame as a **question** or **observation** -- never as an announcement
- Good: "After analyzing 50 newsletters, here's what actually drives opens"
- Good: "Has anyone else noticed [specific trend] in [topic]?"
- Bad: "My guide to newsletter marketing"
- Bad: "Check out my latest blog post on [topic]"

**Title formulas (pick the best fit):**

| Formula | When to Use |
|---------|-------------|
| "After [doing X], here's what I found" | When content has original data or experience |
| "Has anyone else noticed [observation]?" | When content identifies a trend |
| "[Topic] question: [specific question]" | When content answers a non-obvious question |
| "I [did X] and the results surprised me" | When content has a contrarian or unexpected finding |
| "[Number] things I learned about [topic]" | When content has clear, numbered takeaways |

### Post Body

**Length:** 200-500 words. Reddit penalizes both too-short and wall-of-text posts.

**Format:** Reddit markdown.

**Structure:**

1. **Context/Observation** (2-3 sentences)
   Open with a relatable situation or observation. Establish credibility through
   specificity, not credentials. "I've been doing X for Y months" not "As a
   certified expert in X."

2. **Key Insight** (1-2 paragraphs)
   The meatiest atom from the content. Present it as a discovery or realization,
   not a teaching moment. Use evidence: numbers, examples, comparisons.

3. **Supporting Points** (bulleted, 3-5 items)
   Pull from the strongest atoms. Each bullet should be one clear thought.
   Use Reddit markdown formatting:
   ```
   - **Bold the key phrase** then explain briefly
   - **Another point** with supporting detail
   ```

4. **Open Question** (1-2 sentences)
   End with a genuine question that invites debate. NOT "What do you think?"
   (too generic). Instead, ask something specific that people can disagree on.

5. **Optional Link** (1 sentence, at the very bottom)
   Only if the original content adds substantial value beyond the post.
   Frame: "Full breakdown with [specific extra detail] here: [link]"
   Separate from the discussion prompt with a line break.

### Tone Rules

| Do | Do NOT |
|----|--------|
| Use "I" and "we" | Use "you should" or "you need to" |
| Share evidence and specifics | Make unsubstantiated claims |
| Acknowledge uncertainty ("in my experience") | Speak in absolutes |
| Use casual language and contractions | Use marketing jargon |
| Ask genuine questions | Ask rhetorical questions |
| Credit sources | Claim everything as original |
| Use `**bold**` for emphasis | Use ALL CAPS or excessive punctuation |
| Include line breaks between paragraphs | Write wall-of-text blocks |

### Reddit Formatting Reference

```markdown
**bold text**
*italic text*
- bullet point
1. numbered list
> blockquote
`inline code`
[link text](url)

Two line breaks = new paragraph
```

## Output 2: Subreddit Suggestions

**File:** `reddit/subreddits.md`

Analyze the content topic and suggest 2-3 relevant subreddits.

**For each subreddit, provide:**

| Field | Description |
|-------|-------------|
| Subreddit | r/SubredditName |
| Relevance | Why this content fits (1 sentence) |
| Size | Approximate subscriber count tier (small <50k, medium 50-500k, large 500k+) |
| Culture | Brief description of posting norms and community expectations |
| Flair | Suggest applicable post flair if the subreddit uses them |
| Rules to Watch | 1-2 specific rules that could affect this post |
| Adaptation Notes | Any changes needed to the post body for this specific subreddit |

**Subreddit selection criteria:**
1. **Topic match** -- the subreddit actively discusses this subject
2. **Size sweet spot** -- medium subreddits (50k-500k) often have the best engagement
3. **Self-promotion tolerance** -- some subreddits ban all external links; note this
4. **Post type fit** -- discussion-oriented subreddits over link-dump subreddits

**Common subreddit categories by content type:**

| Content Topic | Likely Subreddits |
|---------------|-------------------|
| Marketing | r/marketing, r/digital_marketing, r/content_marketing |
| Entrepreneurship | r/Entrepreneur, r/smallbusiness, r/startups |
| Tech/SaaS | r/SaaS, r/webdev, r/programming |
| Productivity | r/productivity, r/getdisciplined |
| Writing/Content | r/copywriting, r/ContentCreation, r/blogging |
| Social Media | r/socialmedia, r/Instagram, r/Twitter |
| SEO | r/SEO, r/bigseo |
| AI/Automation | r/artificial, r/ChatGPT, r/MachineLearning |

## Error Handling

| Condition | Action |
|-----------|--------|
| Fewer than 3 atoms | Write a shorter post (150-200 words); focus on one insight |
| No `contrarian` or `insight` atoms | Use `stat` + `howto` atoms; frame as a "TIL" style post |
| `brief_mode` is true | Generate post only; skip subreddit suggestions |
| Topic is too niche for major subreddits | Suggest smaller, specialized subreddits; note low traffic |
| Content is purely promotional | Reframe entirely around the insight; strip all product mentions |
