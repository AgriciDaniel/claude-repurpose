# Image Prompt Templates for Content Repurposing

Integration templates for /banana skill image generation during content repurposing.

## /banana Detection

Check for availability in this order:
1. `gemini_generate_image` MCP tool present in current session
2. `~/.claude/skills/banana/SKILL.md` exists on disk

If neither is available, fall back to saving prompts for manual generation (see Fallback section).

## 5-Component Formula (from /banana skill)

Every image prompt follows this structure:
```
Subject -> Action -> Location/Context -> Composition -> Style
```

## Platform Aspect Ratios

| Platform | Ratio | Pixels | Use Case |
|----------|-------|--------|----------|
| Twitter/X | 16:9 | 1600x900 | Post image, thread header |
| LinkedIn post | 1:1 | 1080x1080 | Single image post |
| LinkedIn post (tall) | 4:5 | 1080x1350 | Higher feed presence |
| LinkedIn carousel cover | 4:5 | 1080x1350 | First slide of PDF carousel |
| Instagram carousel | 4:5 | 1080x1350 | All carousel slides |
| Instagram story/reel | 9:16 | 1080x1920 | Vertical full-screen |
| Facebook | 4:5 | 1080x1350 | Feed post |
| YouTube Community | 1:1 | 1080x1080 | Community tab post |

## Quote Card Template

For pulling key quotes from source content into shareable images.

```
Subject: A minimalist quote card displaying "[QUOTE_TEXT]"
Action: Clean typography with the quote prominently centered
Context: [COLOR_SCHEME] gradient background, subtle geometric accents
Composition: Centered layout with generous whitespace, attribution text below
Style: Modern social media design, sharp and professional, high contrast text
```

**Variables to replace:**
- `[QUOTE_TEXT]` - The exact quote (keep under 120 characters for readability)
- `[COLOR_SCHEME]` - Brand colors or platform-appropriate palette

**Tips:**
- One quote per card; never stack multiple quotes
- Attribution format: "-- [Author Name]" or "-- [Author], [Title/Company]"
- Leave 10% margin on all sides for platform safe zones

## Carousel Cover Slide Template

First slide of a carousel that hooks the viewer to swipe.

```
Subject: Bold typographic cover slide reading "[TITLE]"
Action: Eye-catching title treatment with strong visual hierarchy
Context: [BRAND_COLOR] background with subtle pattern or texture
Composition: Title fills 60% of frame, subtitle or byline at bottom
Style: Professional presentation slide, clean and modern, high readability
```

**Variables to replace:**
- `[TITLE]` - Carousel title (keep under 60 characters)
- `[BRAND_COLOR]` - Primary brand color or topic-appropriate color

**Tips:**
- Title should create curiosity or promise value
- Subtitle can include slide count: "7 strategies inside" or author name
- Avoid busy backgrounds; text readability is priority

## Social Hero Image Template

Conceptual image for post headers, blog thumbnails, or feature images.

```
Subject: Conceptual illustration representing [TOPIC]
Action: Visual metaphor for [KEY_CONCEPT]
Context: Clean professional setting with subtle depth
Composition: Balanced composition with clear focal point, text-safe areas
Style: Modern editorial illustration, flat design with depth, brand-consistent colors
```

**Variables to replace:**
- `[TOPIC]` - The broad topic (e.g., "content marketing strategy")
- `[KEY_CONCEPT]` - The specific angle (e.g., "compounding returns of repurposed content")

**Tips:**
- Leave the left or right third relatively empty for text overlay
- Avoid literal representations; metaphors perform better
- Keep detail level low enough to read at mobile thumbnail size

## Stat/Data Highlight Template

For turning statistics from source content into shareable images.

```
Subject: Data visualization card showing "[STAT]" as the hero number
Action: Large bold statistic with supporting context text below
Context: [COLOR_SCHEME] background with minimal data-inspired accents
Composition: Stat number at 40% of frame height, centered, label beneath
Style: Infographic style, clean sans-serif typography, modern and authoritative
```

## /banana Command Patterns

### Single Image Generation
```
Read references/gemini-models.md, then use gemini_generate_image
with model gemini-3.1-flash-image-preview
```

### Batch Generation
```
/banana batch "quote card for [topic]" 5
```

### Set Aspect Ratio
```
Use set_aspect_ratio tool before generating
```

## Fallback: When /banana is NOT Available

When the image generation tools are not detected:

1. Create a file named `banana-prompts.md` in the output directory
2. For each image, include:
   - Target platform and aspect ratio
   - Complete 5-component prompt text
   - Intended use (quote card, cover slide, hero image, etc.)
   - Filename suggestion
3. User can run `/banana generate "[prompt]"` manually later

Format for saved prompts:
```markdown
### [Image Name] - [Platform] ([Aspect Ratio])
**Use:** [quote card / cover slide / hero image]
**Prompt:** [Full 5-component prompt]
**Filename:** [suggested-filename.png]
```

## Cost Awareness

| Model | Cost per Image | Notes |
|-------|---------------|-------|
| Gemini 3.1 Flash | ~$0.04-0.08 | At 2K resolution |

**Typical repurposing batch:**
- 5 quote cards + 2 carousel covers + 3 hero images = ~10 images
- Estimated cost: $0.40-0.80 total

**Rule:** Always show the cost estimate to the user before starting batch generation. Never auto-generate more than 3 images without confirmation.
