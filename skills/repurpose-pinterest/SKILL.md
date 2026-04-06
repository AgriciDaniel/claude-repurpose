---
name: repurpose-pinterest
description: >
  Generates Pinterest content from content atoms: standard pin concepts (3-5 pins)
  with keyword-rich descriptions, idea pin scripts (5-10 slides), and board suggestions.
  Optimizes for saves, clicks, and SEO — Pinterest is a visual search engine, not social
  media. Sub-skill of the Content Repurposing Engine. Use when user says "pinterest",
  "pinterest pin", "idea pin", "pinterest board", or "repurpose for pinterest".
user-invokable: true
argument-hint: "[url-or-atoms]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Pinterest Content Generator

Generate standard pins, idea pin script, and board suggestions from content atoms.

## Inputs

Received from the parent agent (`repurpose-visual`):

| Input | Description |
|-------|-------------|
| `atoms` | Full list of content atoms with types and impact ratings |
| `main_argument` | One-sentence thesis of the source content |
| `target_audience` | Who benefits from this content |
| `primary_topic` | Category or niche |
| `voice_profile` | Detected or overridden brand voice |
| `images_flag` | If true AND /banana available, generate images directly |
| `brief_mode` | If true, produce 1 pin description only |

## References

Load before generating:
- `references/platform-specs.md` -- pin dimensions, algorithm weights, posting times
- `references/hook-formulas.md` -- keyword-first titles, curiosity gap descriptions
- `references/image-sourcing.md` -- 3-tier image pipeline, prompt templates, platform dimensions

## Platform Rules

| Spec | Value |
|------|-------|
| Pin title | 100 characters max |
| Pin description | 500 characters max (keyword-first, SEO-rich) |
| Standard pin image | 1000x1500 (2:3 tall format) |
| Square pin image | 1080x1080 (1:1) |
| Idea pin slides | 2-20 slides, 1080x1920 (9:16) |
| Algorithm | Freshness + keyword relevance + saves + clicks |
| SEO value | HIGH -- Google indexes pins in image search and web results |
| Hashtags | 2-5 relevant tags |
| Best time | Sat/Sun 8-11PM, weekdays 2-4PM |

## Core Principle

Pinterest is a visual SEARCH ENGINE, not social media. Keyword placement matters more than engagement bait. Every pin description should read like a mini SEO snippet. Users are planners and dreamers -- they search with intent to save, try, and buy.

## Output 1: Standard Pins (3-5)

Write to `pinterest/pins.md`.

Generate 3-5 pin concepts. Each pin must include:

### Pin Structure

1. **Title** (100 characters max)
   - Keyword-first: lead with the search term users would type
   - Use "How to", "Best", "Ideas for", "X Ways to" formats
   - Specific and descriptive -- avoid vague or clever wordplay
   - Include the primary topic keyword in the first 40 characters

2. **Description** (500 characters max)
   - First sentence: restate the value proposition with the primary keyword
   - Middle: 2-3 sentences expanding on what the user will learn or gain
   - End with a CTA: "Click to read the full guide" or "Save this for later"
   - Naturally weave in 3-5 related keywords (no keyword stuffing)
   - Write as a mini SEO snippet -- imagine it appearing in Google search results

3. **Image direction**
   - Dimensions: 1000x1500 (2:3 tall portrait)
   - Text overlay: title or key phrase in bold, readable font (5-10 words)
   - Visual style: clean, aspirational, high-contrast
   - Color: bright or warm tones perform best on Pinterest
   - Include /banana prompt if `--images` flag is set

4. **Suggested board**
   - Which board this pin belongs to (from Output 3 or existing boards)
   - Why this board is the right fit

### Pin SEO Rules

| Do | Don't |
|----|-------|
| Lead titles with primary keyword | Use clickbait or vague titles |
| Write descriptions like SEO snippets | Stuff keywords unnaturally |
| Include "how to", "best", "ideas" in titles | Use hashtags as the only discovery mechanism |
| Add 2-5 relevant hashtags at the end | Use more than 5 hashtags |
| Front-load the most important keyword | Bury the topic in the middle of the description |
| Write for searchers with intent | Write for casual scrollers |

## Output 2: Idea Pin Script (5-10 Slides)

Write to `pinterest/idea-pin.md`.

### Slide-by-Slide Structure

| Slide | Purpose | Content |
|-------|---------|---------|
| **Slide 1** | Hook/Cover | Bold title (5-8 words), eye-catching visual, "Keep swiping" cue |
| **Slides 2-3** | Problem/Context | Why this matters, relatable pain point or aspiration |
| **Slides 4-7** | Core value | One insight per slide from highest-impact atoms, actionable steps |
| **Slide 8-9** | Summary/Result | Key takeaway, before/after, or transformation promise |
| **Final slide** | CTA | Follow prompt, save prompt, link to full content |

### Idea Pin Rules
- Dimensions: 1080x1920 (9:16 vertical) for all slides
- One idea per slide -- never stack multiple concepts
- Text overlay on every slide: large, bold, readable at mobile size
- Visual consistency: same color palette, font style, and layout across all slides
- Cover slide determines whether anyone swipes -- invest the most effort here
- Include a "step" or "number" indicator on instructional slides (Step 1, Step 2...)
- Background should be clean and not compete with text overlay

### Visual Direction

For each slide, specify:
- Headline text (5-10 words, bold)
- Supporting text (1-2 short lines, if any)
- Background treatment (solid color, lifestyle photo, flat lay, gradient)
- Text position (centered, top-third, bottom-third)
- Color palette (consistent across all slides)

## Output 3: Board Suggestions

Write to `pinterest/boards.md`.

Suggest 2-3 relevant boards to pin content to.

### Board Structure

For each board:

1. **Board name**
   - Keyword-rich and descriptive (e.g., "Healthy Meal Prep Ideas" not "Food")
   - 3-5 words, search-friendly

2. **Board description** (up to 500 characters)
   - SEO-optimized: include related keywords naturally
   - Describe what a user will find on this board
   - Aspirational tone: frame as a collection of valuable resources

3. **Why it fits**
   - Brief explanation of how this content aligns with the board's theme
   - Which pins from Output 1 belong here

### Board Strategy
- Boards act as keyword categories -- name them for search, not creativity
- A well-named board helps ALL pins on it rank higher in Pinterest search
- Suggest one broad board and one niche board minimum

## Image Prompts

If `--images` flag is set, suggest:
- **Standard pins**: 2:3 (1000x1500) visual concepts for each pin
- **Idea pin cover**: 9:16 (1080x1920) cover slide concept
- Include /banana prompt descriptions (subject, context, style, composition, text overlay)

## Output Format

Each file should include the content plus production notes:

```markdown
# Pinterest Pin: [Topic]

## Pin 1
**Title:** [keyword-first title, 100 chars max]
**Description:** [SEO-rich description, 500 chars max]
**Image:** [visual direction]
**Board:** [suggested board name]
**Hashtags:** [2-5 tags]

## Pin 2
...

---
**Posting notes:** [best time, SEO tips, board strategy]
```

## Brief Mode

If `--brief` is active, produce only:
- 1 pin description + image direction (highest-impact atom, keyword-optimized)
- Skip idea pin and board suggestions

## Error Handling

| Condition | Action |
|-----------|--------|
| Fewer than 3 atoms | Generate fewer pins to match; minimum 1 pin |
| Content not visual | Focus on text-overlay pins with clean backgrounds |
| No clear keywords | Analyze main_argument and primary_topic for search terms |
| `--images` but no /banana | Save prompts to file; suggest Canva templates as alternative |
| Content is time-sensitive | Note in posting notes that Pinterest favors evergreen content |
| Atoms lack actionable angle | Reframe as "how to" or "ideas for" to match Pinterest search intent |
