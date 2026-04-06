---
name: repurpose-tiktok
description: >
  Generates TikTok content from content atoms: video scripts (15-60s) with hook-first
  structure and text overlay timestamps, carousel/photo mode scripts (2-10 slides),
  and stitch/duet concepts for trend-riding. Optimizes for completion rate and hook
  engagement. Sub-skill of the Content Repurposing Engine. Use when user says "tiktok",
  "tiktok script", "tiktok video", "tiktok carousel", "tiktok stitch",
  "tiktok duet", "tiktok photo mode", or "repurpose for tiktok".
user-invokable: true
argument-hint: "[url-or-atoms]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# TikTok Content Generator

Generate video script, carousel/photo mode, and stitch/duet concept from content atoms.

## Inputs

You receive from the orchestrator:
- **Content atoms** (typed and impact-rated)
- **Main argument**, target audience, primary topic
- **Brand voice profile** (5-dimension scores or override flag)
- **Flags**: `--brief` (video script only), `--images` (generate cover/thumbnail prompts)

## References

Load before generating:
- `references/platform-specs.md` -- video specs, carousel format, algorithm weights
- `references/hook-formulas.md` -- opening hooks, pattern interrupts
- `references/voice-adaptation.md` -- TikTok tone rules (fast, casual, raw/authentic)

## Platform Rules

| Spec | Value |
|------|-------|
| Video length | 15-60s sweet spot (up to 3 min, 10 min for some accounts) |
| Video dimensions | 1080x1920 (9:16) |
| Carousel/Photo mode | 2-10 slides, 1080x1350 (4:5) |
| Algorithm priority | Completion rate #1, then shares, comments, likes |
| Hook window | 0.5-1.5 seconds (determines whether viewer stays or scrolls) |
| Hashtags | 3-5 (mix 1-2 trending + 2-3 niche) |
| Text overlay safe zone | Avoid bottom 20% (TikTok UI overlap) |
| Post types | Video, photo carousel, stitch, duet, LIVE |
| Best time | Tue/Thu/Sat 7-9 PM |

## Output 1: Video Script (15-60s)

Write to `tiktok/video-script.md`.

### Timestamp Structure

| Timestamp | Section | Content |
|-----------|---------|---------|
| **0-1.5s** | Hook | Pattern interrupt, bold claim, or unexpected question. This single moment determines everything. |
| **1.5-5s** | Context | Quick setup: who you are OR why this matters. Keep it raw, not polished. |
| **5-25s** | Value | Core insight from 2-3 highest-impact atoms. Jump cuts every 2-3 seconds. Each sentence must earn the next. |
| **25-45s** | Proof | Stat, result, example, or before/after. Show, don't just tell. |
| **45-55s** | CTA | Follow, comment, stitch, or "link in bio." Only ONE ask. |
| **55-60s** | Loop hook (recommended) | Final line connects back to the opening -- encourages rewatch (boosts completion rate significantly). |

### Video Script Rules
- Every second must justify the next. If a viewer can skip 3 seconds and miss nothing, cut those 3 seconds.
- Jump cuts every 2-3 seconds minimum. No static talking-head shots longer than 3s.
- Write the script as spoken words, not written prose. Fragments. Pauses. Emphasis marks.
- Completion rate is king. A 30s video with 90% completion massively outperforms a 60s video with 40%.
- The hook must work with sound OFF (text overlay carries it) and sound ON (voice carries it).

### Text Overlay Plan

For each timestamp section, specify:

| Timestamp | On-Screen Text | Position | Animation |
|-----------|---------------|----------|-----------|
| 0-1.5s | [Hook phrase, 3-6 words] | Top-center | Pop-in or zoom |
| 1.5-5s | [Context keyword] | Center | Typewriter |
| 5-25s | [Key phrases per jump cut] | Top or center | Cut-sync |
| 25-45s | [Stat or result number] | Center-bold | Scale-up |
| 45-55s | [CTA text] | Center | Pulse |

**Critical**: Avoid bottom 20% of frame for all text overlays -- TikTok's UI (caption, buttons, progress bar) covers this area.

### Audio Direction
- **Option A: Voiceover** -- The script IS the voiceover. Write it conversationally with natural pauses.
- **Option B: Trending sound** -- Note: "Use trending audio for discoverability. Voice as text overlay only."
- **Option C: Original audio** -- Direct-to-camera delivery. Mark emphasis and pace changes.
- Always recommend trending sound research: "Check TikTok's Creative Center for current trending sounds in [niche]."

### Tone Rules

| Do | Do NOT |
|----|--------|
| Use casual, conversational language | Use corporate or formal phrasing |
| Start mid-thought ("So I just found out...") | Start with introductions ("Hi, I'm...") |
| Use trending phrases and patterns | Use dated slang or forced memes |
| Speak in short, punchy fragments | Write in complete, polished sentences |
| Be raw and authentic | Over-produce or over-edit the feel |
| Use "you" and "I" naturally | Lecture or teach from above |
| Show genuine reactions and opinions | Be neutral or hedging |

## Output 2: Carousel / Photo Mode (2-10 Slides)

Write to `tiktok/carousel.md`.

### Slide Structure

| Slide | Purpose | Content |
|-------|---------|---------|
| **Slide 1** | Stop the scroll | Hook headline (5-8 words), bold visual, "Swipe" implied by format |
| **Slides 2-5** | Core value | One idea per slide from highest-impact atoms. Text-forward, minimal graphics. |
| **Slides 6-8** | Proof + examples | Stats, comparisons, or actionable steps |
| **Final slide** | CTA | Follow + save prompt, or teaser for related content |

### Carousel Rules
- Dimensions: 1080x1350 (4:5) for all slides
- TikTok carousels are text-forward -- prioritize readability over visual complexity
- One idea per slide, large readable text
- Consistent visual style across slides
- TikTok carousel captions are shorter than Instagram -- keep to 150-300 chars
- Photo mode is a rising format with lower competition than video (2026)

### Caption for Carousel
- 150-300 characters (shorter than Instagram)
- Hook in first line
- 3-5 hashtags (mix trending + niche)
- End with engagement prompt ("Save this for later" or "Which one surprised you?")

## Output 3: Stitch/Duet Concept

Write to `tiktok/stitch-duet.md`.

### Concept Structure

| Field | Content |
|-------|---------|
| **Trending angle** | Describe the type of trending content to respond to (not a specific video) |
| **Your hook** | Opening line for the stitch/duet (0.5-1.5s) |
| **Response script** | 15-30s script with your angle from the atoms |
| **Why it works** | 1-2 sentences on why stitch/duet boosts reach (algorithm loves participatory content: 20-30% more reach) |

### Stitch vs Duet
- **Stitch**: Use the first 1-5s of another video, then cut to your take. Best for "reacting to" or "adding to" a trending topic.
- **Duet**: Side-by-side with another video. Best for comparisons, demonstrations, or visual responses.

### Concept Rules
- Suggest the TYPE of trending content to stitch/duet with, not a specific creator or video
- The response portion must deliver standalone value from the atoms
- Frame as contributing to a conversation, not stealing content
- Keep the response to 15-30 seconds

## Image Prompts

If `--images` flag is set, suggest:
- **Video thumbnail**: 9:16 (1080x1920) eye-catching cover frame concept
- **Carousel slides**: 4:5 (1080x1350) visual concepts for key slides
- Include /banana prompt descriptions

## Output Format

Each file should include content plus production notes:

```markdown
# TikTok Video Script: [Topic]

## Hook (0-1.5s)
**Say:** "[spoken text]"
**Text overlay:** [on-screen text] | Position: [top/center] | Animation: [type]
**Visual:** [what the viewer sees]

## Context (1.5-5s)
...

---
**Production notes:** [audio direction, posting time, hashtag suggestions, trending sound research]
```

## Brief Mode

If `--brief` is active, produce only:
- 1 video script (15-60s)
- Skip carousel and stitch/duet concept

## Error Handling

| Condition | Action |
|-----------|--------|
| Fewer than 3 atoms | Write a shorter script (15-30s); focus on one insight |
| No `stat` or `casestudy` atoms | Skip the Proof section; extend Value section |
| `brief_mode` is true | Generate video script only; skip carousel and stitch/duet |
| Content is too academic/formal | Increase casual rewording; add "imagine this..." framing |
| Topic doesn't suit video | Prioritize carousel/photo mode over video script |
| Content is purely promotional | Reframe around the insight; strip product mentions |
