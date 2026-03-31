---
name: repurpose-seo
description: >
  Generates cross-platform SEO metadata including optimized titles, descriptions,
  hashtag sets, keywords, alt text, and platform-specific search signals. Ensures
  keyword consistency across all repurposed outputs.
user-invokable: false
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Cross-Platform SEO Metadata Generator

Produce a unified SEO metadata file covering every platform in the repurposing
pipeline. Ensures keyword consistency while respecting each platform's unique
search and discovery mechanics.

## Inputs

Received from the parent agent (`repurpose-seo`):

| Input | Description |
|-------|-------------|
| `atoms` | Full list of content atoms with types and impact ratings |
| `main_argument` | One-sentence thesis of the source content |
| `target_audience` | Who benefits from this content |
| `primary_topic` | Category or niche |
| `voice_profile` | Detected or overridden brand voice |
| `platforms_requested` | Which platforms are being generated (all if unspecified) |

## References

Load these before generating output:

- `references/platform-specs.md` -- character limits, hashtag counts, formatting rules
- `references/engagement-benchmarks.md` -- click-through and engagement baselines

## Output: seo-metadata.md

**File:** `seo-metadata.md`

Single file with clearly labeled sections per platform.

### Core Keywords (Cross-Platform)

Before generating platform-specific metadata, establish the keyword foundation:

```markdown
## Core Keywords

**Primary Keywords (3-5):**
- [keyword 1] -- highest relevance to main argument
- [keyword 2]
- [keyword 3]

**Secondary Keywords (5-10):**
- [long-tail keyword 1]
- [long-tail keyword 2]
- ...

**Keyword Selection Rules:**
- Primary: directly describe the content topic (1-2 words)
- Secondary: long-tail phrases the target audience would search
- Avoid generic terms ("marketing", "business") unless paired with specifics
- Include at least one audience-identifying keyword ("for founders", "SaaS")
```

All platform sections below must use these core keywords, adapted to each
platform's conventions.

---

### Twitter/X

| Field | Spec |
|-------|------|
| **Optimized Title** | Under 70 chars; include primary keyword; works as tweet text |
| **Description** | 1-2 sentences; under 200 chars; for Twitter Card meta |
| **Twitter Card Type** | `summary_large_image` (default) or `summary` if no hero image |
| **Hashtags** | 0-2 max. Only if highly relevant. Twitter penalizes hashtag stuffing. |
| **Keywords in Tweet** | Weave primary keyword naturally into tweet copy; never force |
| **Alt Text** | For any attached image: descriptive, keyword-inclusive, under 420 chars |

### LinkedIn

| Field | Spec |
|-------|------|
| **Optimized Headline** | Under 150 chars; professional tone; include primary keyword |
| **Description** | 1-2 sentences for link preview or article summary |
| **Hashtags** | 3-5. Mix of broad (50k+ followers) and niche (<10k followers). Place at post bottom. |
| **Article SEO** | If longform: suggest SEO title (under 70 chars) + meta description (under 155 chars) for LinkedIn article |
| **Keywords** | Include primary keyword in first 2 lines of post (LinkedIn search indexes early text) |
| **Alt Text** | For carousel cover or images: professional, descriptive |

### Instagram

| Field | Spec |
|-------|------|
| **Caption Headline** | First line of caption (before "more" fold); under 125 chars; hook + keyword |
| **Description** | Not applicable (Instagram has no meta description) |
| **Hashtags** | 3-5 niche hashtags. Avoid generic (#marketing, #inspo). Target hashtags with 10k-500k posts for discoverability. |
| **Hashtag Research Notes** | For each hashtag: approximate post count and why it fits |
| **Keywords** | Work primary keyword into caption naturally; Instagram search indexes caption text |
| **Alt Text** | For each carousel slide and reel thumbnail: descriptive, specific, keyword-inclusive |

**Instagram hashtag rules:**
- Place in caption body or first comment (either works; caption preferred for indexing)
- 3-5 total (algorithm penalizes 20+ hashtag lists)
- Mix: 1 broad (100k+ posts), 2-3 niche (10k-500k), 1 micro (<10k)
- Rotate sets across posts to avoid shadow-ban triggers

### Facebook

| Field | Spec |
|-------|------|
| **Optimized Title** | Under 80 chars; conversational tone; primary keyword |
| **Description** | For link preview: under 155 chars |
| **Hashtags** | 0-3. Facebook hashtags have low impact; use only if highly topical. |
| **Keywords** | Include in first sentence; Facebook search indexes post text |
| **Alt Text** | For any images: descriptive, keyword-included |

### YouTube Community

| Field | Spec |
|-------|------|
| **Post Text** | First 2 lines (before fold) should contain primary keyword |
| **Hashtags** | 1-3 relevant hashtags at post bottom |
| **Keywords** | Work into poll questions and post body naturally |

### Reddit

| Field | Spec |
|-------|------|
| **Title Keywords** | Include primary keyword in post title naturally |
| **Post Flair** | Suggest flair text based on subreddit conventions (e.g., "Discussion", "Resource", "Question") |
| **No Hashtags** | Reddit does not use hashtags. Never include them. |
| **Keywords** | Work into post body for Reddit search; use natural language |

### Newsletter / Email

| Field | Spec |
|-------|------|
| **Subject Line Keywords** | Primary keyword in at least 1 of 3 subject variants |
| **Preview Text** | 40-90 chars; complements subject; includes secondary keyword |
| **Alt Text** | For any email images: descriptive (many clients block images) |
| **No Hashtags** | Email does not use hashtags. |

### Skool

| Field | Spec |
|-------|------|
| **Post Title** | Include primary keyword; frame as discussion or challenge |
| **Hashtags** | 0-2 if the Skool community uses tags |
| **Keywords** | Work into post body and discussion prompt |

---

## Cross-Platform Consistency Check

After generating all sections, verify:

1. **Primary keyword appears** in every platform's title/headline
2. **No platform uses more hashtags** than its recommended limit
3. **Alt text is unique** per image, not copy-pasted across platforms
4. **Tone matches platform** (professional for LinkedIn, casual for Twitter, peer-to-peer for Reddit)
5. **No keyword stuffing** -- each keyword appears naturally, max 2 times per platform section

## Keyword Adaptation Rules

| Platform | Keyword Style |
|----------|---------------|
| Twitter | Short, punchy, often as a noun phrase |
| LinkedIn | Professional, may include industry jargon |
| Instagram | Casual, may abbreviate or use slang |
| Facebook | Conversational, question-friendly |
| Reddit | Natural language, no optimization feel |
| Newsletter | Benefit-oriented, action words |
| YouTube | Search-query style, how-to phrasing |

## Error Handling

| Condition | Action |
|-----------|--------|
| Topic too broad for specific keywords | Ask parent agent for niche-down; use audience-specific long-tail |
| Platform not in `platforms_requested` | Skip that section; note in output |
| No images generated | Skip alt text sections; note "Add alt text when images are created" |
| `brief_mode` is true | Generate core keywords + top 3 requested platforms only |
| Hashtag research unclear | Default to topic + audience + format pattern |
