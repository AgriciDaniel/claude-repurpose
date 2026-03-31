---
name: repurpose
description: >
  Content Repurposing Engine. Transforms any content (YouTube videos, blog posts,
  podcasts, local files, pasted text) into platform-optimized outputs for
  Twitter/X, LinkedIn, Instagram, Facebook, YouTube Community, Skool, Reddit,
  and email newsletters. Atomizes content into reusable pieces, adapts brand
  voice per platform, generates polls, image prompts (via /banana), publishing
  calendars, and SEO metadata. Triggers on: "repurpose", "content repurpose",
  "turn into social media", "cross-platform", "content atomization", "repurpose
  blog", "repurpose video", "turn this into posts".
user-invokable: true
argument-hint: "[url-or-file] [--platforms X,Y] [--voice casual|professional|witty] [--brief] [--images]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Content Repurposing Engine

Transform any content into platform-optimized outputs across 8+ channels.

## Quick Reference

| Command | Description |
|---------|-------------|
| `/repurpose <url-or-file>` | Full repurpose pipeline (all platforms) |
| `/repurpose <input> --platforms twitter,linkedin` | Repurpose to specific platforms only |
| `/repurpose <input> --voice casual` | Override brand voice (casual/professional/witty) |
| `/repurpose <input> --brief` | Quick mode: 1 post per platform, no calendar |
| `/repurpose <input> --images` | Generate image prompts (or /banana images if available) |
| `/repurpose analyze <input>` | Atomize content only, no platform outputs |
| `/repurpose calendar <input>` | Generate 7-day publishing calendar only |

## Step 1: Input Detection

Detect the input type and extract raw content accordingly.

**Detection patterns (check in order):**

| Pattern | Type | Extraction Method |
|---------|------|-------------------|
| `youtube\.com/watch\|youtu\.be/\|youtube\.com/shorts` | YouTube video | Run `scripts/extract_transcript.py <url>` |
| `https?://` (any other URL) | Blog/article | Run `scripts/extract_article.py <url>` |
| Path ending in `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac` | Audio file | Run `scripts/transcribe_audio.py <path>` |
| Path ending in `.md`, `.txt`, `.pdf` | Local file | Read file directly with the Read tool |
| No URL or file path detected | Pasted text | Use the inline text as-is |

**Extraction rules:**
- For YouTube: extract transcript, video title, channel name, description, and duration
- For blog URLs: extract title, author, publication date, body text, and any embedded media descriptions
- For audio: transcribe to text, note duration and any speaker labels
- For local files: read full contents; for PDF use the Read tool with page ranges if large
- For pasted text: use verbatim; ask the user for a title/topic if not obvious

If extraction fails, report the error clearly and ask the user to paste the content directly.

## Step 2: Content Atomization

Break the extracted content into 5-15 reusable "atoms." Each atom is a self-contained content unit.

**Atom types:**

| Type | Description | Example |
|------|-------------|---------|
| `stat` | A specific number, percentage, or data point | "73% of marketers repurpose content" |
| `quote` | A quotable sentence or phrase | "Distribution is the new creation." |
| `insight` | A non-obvious takeaway or lesson | "Repurposing beats fresh creation 3:1 on ROI" |
| `question` | A thought-provoking question from the content | "What if you never had to write from scratch again?" |
| `contrarian` | A bold or counterintuitive claim | "Posting less actually grows your audience faster" |
| `howto` | An actionable step or mini-tutorial | "Step 1: Record a 10-min video. Step 2: Extract 8 clips." |
| `analogy` | A comparison that makes the concept click | "Repurposing is composting: old material feeds new growth" |
| `casestudy` | A real example, result, or before/after | "Gary Vee turns one keynote into 35M+ views across platforms" |
| `prediction` | A forward-looking claim or trend | "By 2027, 90% of content will be AI-assisted remixes" |
| `tldr` | The single-sentence summary of the entire piece | Always extract exactly one |

**Atomization rules:**
1. Extract between 5 and 15 atoms (aim for 8-12 for most content)
2. Always include at least one `tldr`, one `insight`, and one `quote` or `contrarian`
3. Label each atom with its type
4. Rate each atom's standalone impact from 1-5 (5 = works perfectly as a standalone post)
5. Identify the main argument, target audience, and primary topic
6. Preserve the original author's voice in quoted atoms
7. For longer content (>2000 words), aim for 12-15 atoms; for shorter, 5-8

**Atomization output format:**
```
## Content Atoms

**Main Argument:** [one sentence]
**Target Audience:** [who benefits from this content]
**Primary Topic:** [category/niche]

| # | Type | Atom | Impact |
|---|------|------|--------|
| 1 | tldr | ... | 5 |
| 2 | insight | ... | 4 |
| ... | ... | ... | ... |
```

## Step 3: Voice Detection and Adaptation

**Default behavior:** Detect the brand voice from the source content. Analyze formality, humor level, directness, emotion, and jargon to infer the author's natural voice.

**Override flags:**
- `--voice casual` — friendlier, more emoji, conversational, contractions
- `--voice professional` — formal, data-driven, authoritative, measured
- `--voice witty` — personality-forward, clever wordplay, punchy, unexpected angles

**Core rule:** The brand voice stays consistent across all platforms. Only the TONE adapts per platform. Load `references/voice-adaptation.md` for the full platform-tone matrix.

## Step 4: Orchestration — Spawn 5 Parallel Agents

After atomization, spawn 5 subagents in parallel. Each agent receives:
- The full list of content atoms (with types and impact ratings)
- The main argument, target audience, and primary topic
- The detected or overridden brand voice
- The `--brief` flag status (if true, produce 1 post per platform instead of full sets)
- The `--images` flag status

### Agent 1: `repurpose-social`
**Platforms:** Twitter/X, LinkedIn, Facebook
**Receives:** All atoms, voice profile, platform specs
**Produces:**
- Twitter: 1 standalone tweet + 1 thread (8-12 tweets) + 1 poll + image prompt
- LinkedIn: 1 text post + 1 carousel outline (8-10 slides) + 1 poll
- Facebook: 1 text post + 1 question post + 1 poll
**Sub-skills invoked:** `repurpose-twitter`, `repurpose-linkedin`, `repurpose-facebook`

### Agent 2: `repurpose-visual`
**Platforms:** Instagram, Quote cards, Image prompts
**Receives:** All atoms (especially quotes, stats, insights), voice profile
**Produces:**
- Instagram: 1 carousel (7-10 slides with copy) + 1 reel script (30-60s) + caption + hashtags
- Quote cards: 3-5 text overlays for image generation
- Image prompts: hero image + carousel cover + 3 quote card prompts
**Sub-skills invoked:** `repurpose-instagram`, `repurpose-quotes`

### Agent 3: `repurpose-longform`
**Platforms:** Newsletter, Email sequence, Reddit
**Receives:** All atoms, full original content reference, voice profile
**Produces:**
- Newsletter: subject line + preview text + 200-500 word body
- Email sequence: 3-email drip (day 0, day 2, day 4) with subject lines and CTAs
- Reddit: title + post body adapted to subreddit norms
**Sub-skills invoked:** `repurpose-newsletter`, `repurpose-reddit`

### Agent 4: `repurpose-community`
**Platforms:** YouTube Community, Skool
**Receives:** All atoms (especially questions, polls, insights), voice profile
**Produces:**
- YouTube Community: 1 text post + 1 poll (5 options) + 1 image post concept
- Skool: 1 discussion post + 1 challenge/action post + 1 poll
**Sub-skills invoked:** `repurpose-youtube`, `repurpose-skool`

### Agent 5: `repurpose-seo`
**Platforms:** Cross-platform SEO metadata
**Receives:** All atoms, main argument, target audience, topic
**Produces:**
- Primary keywords (3-5) and secondary keywords (5-10)
- Hashtag sets per platform
- SEO title and meta description (for blog/newsletter)
- Alt text suggestions for all generated images
- Schema markup suggestions (Article, VideoObject, FAQPage)
**Sub-skills invoked:** `repurpose-seo`

### Platform filtering
If `--platforms` is specified, only spawn the agents that cover the requested platforms:
- `twitter`, `linkedin`, `facebook` → Agent 1
- `instagram`, `quotes`, `images` → Agent 2
- `newsletter`, `email`, `reddit` → Agent 3
- `youtube`, `skool` → Agent 4
- `seo` → Agent 5

If a single platform is requested, spawn only the relevant agent.

## Step 5: Collect Outputs and Generate Summary

After all agents complete:

1. **Compile all outputs** into the output directory structure (see below)
2. **Generate images** — ALWAYS attempt image generation when /banana is available (do NOT wait for `--images` flag). If /banana is unavailable, save prompts to `quotes/banana-prompts.md` for manual use later
3. **Generate a summary table** showing what was produced per platform
4. **Generate a 7-day publishing calendar** (unless `--brief` was used)
5. **Generate HTML viewer** — Run `python3 scripts/generate_html.py <output-dir>` to create `index.html` (dark-themed viewer with Copy buttons per content piece) and `all-content.md` (single consolidated file with all platform outputs)
6. **Report to user** — Show summary and link to `index.html` for easy browsing and copying

### Output Directory Structure

```
./repurposed/<YYYY-MM-DD_HHMMSS>/
  summary.md              # Overview of all outputs + publishing calendar
  atoms.md                # Content atomization results
  twitter/
    standalone-tweet.md
    thread.md
    poll.md
  linkedin/
    post.md
    carousel.md
    poll.md
  instagram/
    carousel.md
    reel-script.md
    caption.md
  facebook/
    post.md
    question.md
    poll.md
  youtube-community/
    text-post.md
    poll.md
    image-post.md
  skool/
    discussion.md
    challenge.md
    poll.md
  reddit/
    post.md
  newsletter/
    newsletter.md
    email-sequence.md
  seo/
    keywords.md
    hashtags.md
    metadata.md
  quotes/
    quotes.md             # 5 quotable moments
    banana-prompts.md     # /banana prompts (always generated)
  images/                 # Generated images (auto when /banana available)
    quote-card-*.png
    carousel-cover.*
    hero.*
  seo-metadata.md         # Cross-platform SEO metadata
  all-content.md          # MANDATORY: Single consolidated markdown (all platforms)
  index.html              # MANDATORY: HTML viewer with Copy buttons per content piece
  calendar.md             # 7-day publishing calendar
  summary.md              # Overview report
```

**MANDATORY OUTPUT**: Every `/repurpose` run MUST produce `all-content.md` (single file with everything) and `index.html` (viewer with Copy buttons). Run `python3 scripts/generate_html.py <output-dir>` as the final step.

## Reference Files

Load these references as needed during the pipeline:

| File | When to Load |
|------|-------------|
| `references/platform-specs.md` | Always — before generating any platform output |
| `references/hook-formulas.md` | When writing hooks, headlines, thread openers, email subjects |
| `references/voice-adaptation.md` | After voice detection, before generating any output |
| `references/repurposing-frameworks.md` | During atomization and calendar generation |
| `references/poll-strategy.md` | When generating polls for any platform |
| `references/image-sourcing.md` | When sourcing images (3-tier: website → stock → AI) |
| `references/mistakes-to-avoid.md` | Quality check pass before finalizing outputs |
| `references/engagement-benchmarks.md` | Calendar generation, engagement predictions |

## Sub-Skills

| Sub-Skill | Platform | Key Output |
|-----------|----------|------------|
| `repurpose-twitter` | Twitter/X | Standalone tweet, thread, poll |
| `repurpose-linkedin` | LinkedIn | Text post, carousel, poll |
| `repurpose-instagram` | Instagram | Carousel, reel script, caption |
| `repurpose-facebook` | Facebook | Post, question, poll |
| `repurpose-youtube` | YouTube Community | Text post, poll, image concept |
| `repurpose-skool` | Skool | Discussion, challenge, poll |
| `repurpose-reddit` | Reddit | Subreddit-adapted post |
| `repurpose-newsletter` | Email | Newsletter, 3-email drip |
| `repurpose-quotes` | Visual | Quote cards, text overlays |
| `repurpose-seo` | Cross-platform | Keywords, hashtags, metadata |
| `repurpose-calendar` | Scheduling | 7-day publishing calendar |

## Image Sourcing Pipeline — 3-Tier System

Images are sourced automatically for every platform. The pipeline follows a 3-tier priority chain.

### Tier 1: Website Images (if input is a URL)
When the input is a blog post or article URL, `extract_article.py` extracts images from the page.
- Use `scripts/fetch_images.py --article-images` to filter: skip logos, icons, avatars, ads, SVGs, < 400px
- Rank by keyword overlap with content atoms
- These are the MOST relevant — they came from the source content itself

### Tier 2: Stock Photos (Pixabay → Unsplash → Pexels)
Search for topic-relevant images via WebSearch:
- `site:pixabay.com [topic keywords] wide professional` (preferred, no attribution required)
- `site:unsplash.com [topic keywords] professional` (resize params supported)
- `site:pexels.com [topic keywords] high quality` (fallback)
- Extract direct CDN URLs from results
- Verify each URL with HEAD request before using
- Target: 3-5 relevant images

### Tier 3: AI-Generated (Gemini via /banana)
- **ALWAYS** for quote cards (text overlay requires custom design)
- **ALWAYS** for carousel covers with title text
- **FALLBACK** when Tiers 1-2 produce < 3 suitable images
- Uses 6-Component Brief: Subject → Action → Context → Composition → Lighting → Style
- Load `references/image-sourcing.md` for templates and platform dimensions

### Execution Order
1. Check if input URL has images → extract and filter (Tier 1)
2. Generate stock photo queries → use WebSearch to find Pixabay/Unsplash/Pexels images (Tier 2)
3. Count total images found. If < 3 usable, generate more via /banana (Tier 3)
4. ALWAYS generate 5 quote cards via /banana (or save prompts if unavailable)
5. Save all images to `./repurposed/<timestamp>/images/`
6. Include image URLs/paths in platform output files

### /banana Detection
Check for `gemini_generate_image` MCP tool OR `~/.claude/skills/banana/SKILL.md` OR `GOOGLE_API_KEY` env var.
- Available: generate images automatically
- Not available: save all prompts to `quotes/banana-prompts.md` for manual generation later

## Error Handling

| Error | Resolution |
|-------|------------|
| YouTube transcript unavailable | Ask user to paste transcript or provide alternate URL |
| Blog URL returns 403/404 | Ask user to paste article text directly |
| Audio transcription fails | Check file format; suggest converting to .wav or .mp3 |
| Extraction script not found | Fall back to WebFetch for URLs; Read for local files |
| Platform not recognized | Show supported platforms list; suggest closest match |
| Content too short (<100 words) | Warn user; reduce atom target to 3-5; skip thread/carousel |
| Content too long (>10,000 words) | Chunk into sections; atomize each; merge top atoms |
| /banana not available | Generate prompts only; note in summary |
| Output directory write fails | Fall back to printing all outputs inline |
| Voice detection ambiguous | Default to professional; note in summary |

## Subcommand: `analyze`

**Usage:** `/repurpose analyze <url-or-file>`

Runs only Steps 1-2 (input detection + atomization). Does NOT generate platform outputs.

**Output:**
- Content atoms table with types and impact ratings
- Main argument, target audience, primary topic
- Recommended platforms based on content type
- Suggested voice profile
- Atom count and quality assessment

Use this to preview what the engine extracts before committing to full repurposing.

## Subcommand: `calendar`

**Usage:** `/repurpose calendar <url-or-file>`

Runs Steps 1-2 (extraction + atomization), then generates a 7-day publishing calendar.

**Calendar rules:**
- Monday: Long-form (newsletter or Reddit post)
- Tuesday: Thread (Twitter) + Carousel (LinkedIn)
- Wednesday: Quote cards + Instagram carousel
- Thursday: Polls across all platforms
- Friday: Newsletter send or email drip start
- Saturday: YouTube Community + Skool posts
- Sunday: Stories + light engagement posts (Facebook question, Skool discussion)

**Calendar output includes:**
- Day-by-day schedule with platform, content type, and which atom(s) to use
- Suggested posting times per platform (from platform-specs.md)
- Dependencies (e.g., "Tuesday carousel requires Monday's images")
- Total pieces count

**Output:** Saved to `./repurposed/<timestamp>/calendar.md` and printed to console.

## Execution Flow Summary

```
User input
    |
    v
[1] Detect input type (URL/file/text)
    |
    v
[2] Extract raw content (script or Read)
    |
    v
[3] Atomize into 5-15 labeled atoms
    |
    v
[4] Detect or apply voice profile
    |
    v
[5] Spawn 5 agents in parallel:
    |-- repurpose-social (Twitter + LinkedIn + Facebook)
    |-- repurpose-visual (Instagram + Quotes + Image prompts)
    |-- repurpose-longform (Newsletter + Email + Reddit)
    |-- repurpose-community (YouTube Community + Skool)
    |-- repurpose-seo (Keywords + Hashtags + Metadata)
    |
    v
[6] Collect all outputs → write to ./repurposed/<timestamp>/
    |
    v
[7] Generate summary table + 7-day calendar
    |
    v
[8] Report results to user
```
