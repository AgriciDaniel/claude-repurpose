---
name: repurpose-instagram
description: >
  Generates Instagram content from content atoms: carousel slide scripts (7-10 slides),
  captions optimized for the 125-character fold, and reel scripts with hook-first
  structure. Optimizes for watch time, saves, and shares. Sub-skill of the Content
  Repurposing Engine.
user-invokable: false
---

# Instagram Content Generator

Generate carousel script, caption, and reel script from content atoms.

## Inputs

You receive from the orchestrator:
- **Content atoms** (typed and impact-rated)
- **Main argument**, target audience, primary topic
- **Brand voice profile** (5-dimension scores or override flag)
- **Flags**: `--brief` (caption only), `--images` (generate image prompts)

## References

Load before generating:
- `references/platform-specs.md` -- carousel specs, reel dimensions, algorithm weights
- `references/hook-formulas.md` -- first-slide hooks, caption openers, reel hooks
- `references/voice-adaptation.md` -- Instagram tone rules (relaxed, emoji-rich, visual-first)

## Platform Rules

| Spec | Value |
|------|-------|
| Caption limit | 2,200 characters (125 visible before "more") |
| Carousel slides | 7-10 optimal, up to 20 max |
| Carousel dimensions | 1080x1350 (4:5) |
| Mixed media carousel | 2.33% engagement vs 1.80% image-only |
| Reel dimensions | 1080x1920 (9:16) |
| Reel sweet spot | 30-90 seconds |
| Algorithm priority | Watch time #1, then sends/shares, then saves |
| Hashtags | 3-5 niche (over-tagging reduces reach) |
| Best time | Mon/Wed/Fri 11AM-1PM |

## Output 1: Carousel Script (7-10 Slides)

Write to `instagram/carousel.md`.

### Slide-by-Slide Structure

| Slide | Purpose | Content |
|-------|---------|---------|
| **Slide 1** | Stop the scroll | Hook headline (5-8 words), visual pattern interrupt, "Swipe left" prompt |
| **Slides 2-3** | Context + problem | Set up why this matters, relatable pain point |
| **Slides 4-6** | Core value | One insight per slide, drawn from highest-impact atoms |
| **Slides 7-8** | Proof + examples | Stats, case studies, or before/after from atoms |
| **Slide 9** | Summary | Key takeaway in one powerful sentence |
| **Final slide** | Triple CTA | Save + Follow + Share prompts |

### Carousel Rules
- Dimensions: 1080x1350 (4:5 portrait) for all slides
- One idea per slide -- never stack multiple concepts
- Mix text-heavy slides with visual/graphic slides for rhythm
- Consider mixed media (image + video slides): 2.33% vs 1.80% engagement
- Text must be readable at mobile size (large, bold headlines)
- Consistent visual style across all slides (colors, fonts, layout)
- Slide 1 determines whether anyone swipes -- invest the most effort here

### Visual Direction
For each slide, specify:
- Headline text (5-10 words, bold)
- Supporting text (1-2 short lines, if any)
- Background treatment (color, gradient, image suggestion)
- Layout (centered, left-aligned, split)
- Any icon, illustration, or photo direction

### "Swipe Left" Prompt
Include a directional cue on slide 1. Only 5% of creators use this, but it boosts engagement by ~10%. Options:
- Arrow graphic pointing right
- Text: "Swipe for the full breakdown"
- Visual element that extends past the right edge (implies continuation)

## Output 2: Caption

Write to `instagram/caption.md`.

### Caption Structure

1. **First 125 characters** (visible before "more" fold)
   - This is the hook. Front-load the most compelling statement.
   - Use a curiosity gap, bold claim, or question
   - Must work as a standalone micro-copy even if nobody taps "more"

2. **Body** (up to 2,200 chars total)
   - Expand on the carousel's theme with personal context or story
   - Use line breaks and emoji bullets for scannability
   - Weave in 1-2 atoms that complement (not duplicate) the carousel content
   - Conversational tone with contractions and natural language

3. **Engagement question**
   - End with a specific question that invites comments
   - Questions that ask for personal experience outperform yes/no questions

4. **Hashtags** (3-5)
   - Place at the very end after a line break
   - Mix 1-2 broad niche tags with 2-3 specific tags
   - Never use 30 hashtags (reduces reach in 2026)

### Caption Voice
- Relaxed and creative, not corporate
- Emoji used as visual markers and personality (3-8 per caption)
- Storytelling tone: conversational, flowing, first-person

## Output 3: Reel Script

Write to `instagram/reel-script.md`.

### Reel Structure (30-90 seconds)

| Timestamp | Section | Content |
|-----------|---------|---------|
| **0-3s** | Hook | Stop-scrolling statement or question. This determines everything. |
| **3-10s** | Context | Quick setup: "Here's what most people get wrong about [topic]..." |
| **10-40s** | Value | Core insight from 2-3 atoms. Break into 3-5 second segments with jump cuts. |
| **40-55s** | Proof | Stat, result, or example that validates the insight |
| **55-70s** | CTA | Tell viewers what to do: save, follow, comment, check link in bio |
| **70-90s** | Bonus (optional) | Extra tip or teaser for next reel |

### Reel Rules
- Dimensions: 1080x1920 (9:16 vertical)
- Sweet spot: 30-90 seconds (shorter = better for discoverability)
- Jump cuts every 3-5 seconds to maintain attention
- Hook in first 3 seconds is non-negotiable (determines watch-through rate)
- Watch time is the #1 algorithm signal -- every second must earn the next

### Text Overlay Suggestions
For each section of the reel, suggest:
- On-screen text (key phrase or keyword, 3-6 words)
- Text position (top, center, bottom -- avoid bottom 20% for UI overlap)
- Animation style (pop-in, typewriter, static)

### Audio Direction
- Suggest whether to use: voiceover, trending audio, or original audio
- If voiceover: the script IS the voiceover (write it conversationally)
- Note: trending audio boosts discoverability but must match content mood

## Image Prompts

If `--images` flag is set, suggest:
- **Carousel slides**: 4:5 (1080x1350) visual concepts for each slide
- **Reel cover**: 9:16 (1080x1920) thumbnail concept
- Include /banana prompt descriptions for key slides

## Output Format

Each file should include the content plus production notes:

```markdown
# Instagram Carousel: [Topic]

## Slide 1 -- Hook
**Headline:** [text]
**Visual:** [direction]

## Slide 2 -- [Label]
...

---
**Posting notes:** [best time, hashtag guidance, engagement strategy]
```

## Brief Mode

If `--brief` is active, produce only:
- 1 caption (standalone, not tied to a carousel)
- Skip carousel and reel script
