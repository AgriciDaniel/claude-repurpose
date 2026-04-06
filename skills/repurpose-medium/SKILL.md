---
name: repurpose-medium
description: >
  Generates Medium publication content from content atoms: long-form articles (1500-3000
  words) with narrative arc, SEO-optimized titles and subtitles, tag and publication
  targeting, and canonical crosspost handling. Optimizes for Google indexing, read time,
  and publication submission. Sub-skill of the Content Repurposing Engine. Use when
  user says "medium", "medium article", "medium post", "medium story", or "repurpose
  for medium".
user-invokable: true
argument-hint: "[url-or-atoms]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Medium Article Generator

Produce a long-form article, tag and publication suggestions, and crosspost note
from the content atoms provided by the orchestrator.

## Inputs

Received from the parent agent (`repurpose-broadcast`):

| Input | Description |
|-------|-------------|
| `atoms` | Full list of content atoms with types and impact ratings |
| `main_argument` | One-sentence thesis of the source content |
| `target_audience` | Who benefits from this content |
| `primary_topic` | Category or niche |
| `voice_profile` | Detected or overridden brand voice |
| `brief_mode` | If true, produce title + subtitle + opening only (500 words) |

## References

Load before generating:

- `references/platform-specs.md` -- Medium specs, article length targets, SEO weight
- `references/hook-formulas.md` -- title formulas, opening hooks, narrative structures
- `references/voice-adaptation.md` -- Medium tone rules (authoritative, conversational, storytelling)
- `references/engagement-benchmarks.md` -- read time targets, clap benchmarks

## Platform Rules

| Spec | Value |
|------|-------|
| Article length | 1,500-3,000 words optimal (7-12 min read time) |
| Title | 60 characters max (SEO-optimized, keyword-rich) |
| Subtitle (kicker) | 140 characters max (expands on title, adds context) |
| Tags | Exactly 5 (first tag = primary topic) |
| Images | Inline, any aspect ratio, alt text REQUIRED |
| SEO value | HIGH -- Google indexes Medium articles, often ranks in top results |
| Paywall | Optional (recommend based on content depth and value) |
| Publications | Curated collections that boost distribution significantly |
| Reading time | Displayed prominently, affects click-through rate |
| Best posting | Tuesday-Thursday 8-10 AM |
| Formatting | Full markdown, pull quotes, code blocks, headers, images |

## Core Principle

Medium is a **PUBLICATION** platform, not social media. Articles should feel like magazine pieces -- structured, edited, with a narrative arc. Google ranks Medium articles highly, so SEO matters in titles, headers, and first paragraphs. Write for depth, personality, and lasting value. Information dumps get skimmed; narrative gets read.

## Output 1: Article

**File:** `medium/article.md`

**Length:** 1,500-3,000 words (7-12 min read time).

### Article Structure

1. **Title** (60 chars max)
   - Keyword-rich for Google indexing
   - Curiosity-driven or value-driven (never clickbait)
   - Formulas:
     - "How [Specific Action] [Achieved Specific Result]"
     - "The [Adjective] Truth About [Topic] Nobody Talks About"
     - "[Number] Lessons From [Experience] That Changed How I [Outcome]"
     - "Why [Common Belief] Is Wrong (And What to Do Instead)"
   - Test: would you click this in Google search results?

2. **Subtitle / Kicker** (140 chars max)
   - Expands on the title -- adds context the title couldn't fit
   - Should answer "Why should I read this?" in one line
   - Include a secondary keyword if natural
   - Example title: "Why Most Content Strategies Fail"
   - Example subtitle: "And the simple framework that turned my 200-view posts into 20K-view articles"

3. **Opening hook** (2-3 sentences)
   - Set the stakes immediately -- why does this matter RIGHT NOW?
   - Options: start with a story, a surprising stat, or a bold claim
   - The first 2 sentences determine whether readers continue
   - Never open with a definition ("Content marketing is...")

4. **Section 1: Context / Problem** (300-500 words)
   - Why this topic matters now
   - Frame the gap: what most people get wrong or miss
   - Use `insight` and `contrarian` atoms to build tension
   - Include at least one specific example or data point
   - Header: descriptive H2, keyword-rich

5. **Section 2: Core Insight** (400-700 words)
   - The main argument with supporting evidence
   - This is the centerpiece -- spend the most words here
   - Use the highest-impact atoms
   - Include a pull quote (the single most quotable line, formatted as blockquote)
   - Header: H2 that reveals the insight

6. **Section 3: Supporting Evidence** (300-500 words)
   - Stats, case studies, examples drawn from atoms
   - If `stat` or `casestudy` atoms exist, expand them with context
   - Use subheadings (H3) if covering multiple supporting points
   - Specific numbers always beat vague claims

7. **Section 4: Practical Application** (300-500 words)
   - Actionable steps the reader can take today
   - Draw from `howto` and `actionable` atoms
   - Numbered steps or bulleted checklist format
   - Each step should be specific and measurable
   - Header: action-oriented H2 ("How to Apply This Today")

8. **Closing** (100-200 words)
   - Forward-looking statement or call-to-action
   - Do NOT summarize the whole article -- trust the reader
   - End with a thought-provoking line or a question
   - Optional: invite claps, follows, or responses

9. **Pull quotes** (2-3 throughout)
   - Formatted as blockquotes (`> quote text`)
   - Place one every 500-800 words for visual rhythm
   - Choose lines that work as standalone insights
   - These also serve as highlight-worthy text for Medium's highlight feature

### SEO Optimization

- **Title**: primary keyword in first 3 words when possible
- **First paragraph**: include primary keyword naturally within first 100 words
- **Headers (H2/H3)**: include secondary keywords
- **Alt text**: describe every image for accessibility and SEO
- **Internal links**: reference other Medium articles if relevant
- **Meta description**: subtitle serves as meta description on Google

### Formatting Rules
- Short paragraphs (2-4 sentences max)
- Generous whitespace between sections
- Bold key phrases for scanners (2-3 per section)
- Use H2 for main sections, H3 for subsections
- Code blocks for any technical content
- Bulleted/numbered lists for actionable content
- Pull quotes for visual breaks and emphasis

## Output 2: Tags + Publication Suggestions

**File:** `medium/tags-publications.md`

### Tags (exactly 5)

| Position | Strategy |
|----------|----------|
| Tag 1 (primary) | Broadest relevant topic (highest search volume) |
| Tag 2 | Specific niche within the topic |
| Tag 3 | Audience-related tag (e.g., "Startup", "Self Improvement") |
| Tag 4 | Format or methodology tag (e.g., "How To", "Case Study") |
| Tag 5 | Trending or timely tag if applicable |

The first tag carries the most weight for Medium's distribution algorithm. Choose the broadest relevant topic with the highest search volume.

### Publication Suggestions (2-3)

For each publication, provide:

| Field | Description |
|-------|-------------|
| Publication name | Official name as it appears on Medium |
| Follower tier | Small (<10K), Medium (10K-100K), Large (100K+) |
| Submission note | Key guidelines or requirements for submission |
| Relevance | Why this content fits the publication's focus (1 sentence) |

**Publication selection criteria:**
1. **Topic alignment** -- the publication actively covers this subject
2. **Size sweet spot** -- medium publications (10K-100K) accept more submissions
3. **Acceptance rate** -- larger publications are more selective; suggest a mix
4. **Audience overlap** -- the publication's readership matches the target audience

**Common publications by content type:**

| Content Topic | Likely Publications |
|---------------|---------------------|
| Technology | Better Programming, Towards Data Science, The Startup |
| Business | Better Marketing, The Startup, Entrepreneur's Handbook |
| Productivity | Better Humans, Personal Growth, Mind Cafe |
| Writing/Content | The Writing Cooperative, Better Marketing |
| Design | UX Collective, Bootcamp, UX Planet |
| AI/ML | Towards Data Science, Towards AI, AI in Plain English |

## Output 3: Crosspost Note

**File:** `medium/crosspost-note.md`

Handle canonical URL attribution to protect SEO.

### If content was originally published elsewhere:
- Include canonical URL import note: "Use Medium's Import tool (medium.com/p/import) to set the canonical URL to [original source]"
- Footer text: "Originally published at [source name + URL]"
- Note: Medium's import tool automatically sets `rel=canonical` to avoid duplicate content penalties

### If this is original content:
- Note: "First published on Medium"
- Suggest the user set up a custom domain or publication for branding
- Optional: suggest crossposting TO their blog later with canonical pointing back to Medium

### Crosspost Format

```markdown
**Canonical source:** [Original URL or "Medium (original)"]
**Import method:** [Medium Import tool / Manual paste]
**Footer attribution:** [Text to include at bottom of article]
**SEO note:** [Canonical URL guidance]
```

## Tone Rules

| Do | Do NOT |
|----|--------|
| Write in first person ("I discovered", "In my experience") | Use third person or passive voice |
| Tell stories and share genuine insights | Write dry, encyclopedia-style content |
| Use conversational language with personality | Use academic jargon or corporate speak |
| Include specific numbers and evidence | Make vague, unsubstantiated claims |
| Build a narrative arc (tension, insight, resolution) | Dump information in list format only |
| Use pull quotes for visual rhythm | Write unbroken walls of text |
| Acknowledge nuance and uncertainty | Speak in absolutes without evidence |
| Write headlines that work in Google search | Write clickbait or misleading titles |

## Output Format

```markdown
# [Article Title]
## [Subtitle / Kicker]

[Full article text with headers, pull quotes, and formatting]

---
**Reading time:** ~[X] min
**Tags:** [tag1], [tag2], [tag3], [tag4], [tag5]
**Suggested publications:** [publication1], [publication2]
**Paywall recommendation:** [Yes/No + reasoning]
**Best posting time:** Tuesday-Thursday 8-10 AM
**SEO notes:** [primary keyword, secondary keywords, title optimization]
```

## Brief Mode

If `--brief` is active, produce only:
- Title + subtitle
- Opening 3 paragraphs (~500 words)
- 5 tags
- Skip full article, publication suggestions, and crosspost note

## Error Handling

| Condition | Action |
|-----------|--------|
| Fewer than 5 atoms | Write shorter article (800-1,200 words); reduce to 3 sections |
| No `stat` or `casestudy` atoms | Use narrative-driven structure; lean on `insight` and `contrarian` atoms |
| `brief_mode` is true | Generate title + subtitle + opening only (500 words) + tags |
| Content too short for full article | Frame as a "thought piece" (800 words); note shorter read time |
| Promotional content detected | Reframe as an insight story; strip product mentions, focus on lessons learned |
| Voice profile unclear | Default to conversational-authoritative; note in output header |
