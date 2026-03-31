---
name: repurpose-quotes
description: >
  Extracts the 5 most quotable moments from content atoms and generates
  /banana image prompts for each using the 5-Component Formula. Produces
  quote cards ready for social sharing with platform-specific aspect ratios,
  color palettes, and text overlays.
user-invokable: false
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Quote Graphics and Image Prompt Generator

Extract 5 quotable moments from content atoms and produce /banana image generation
prompts (or generate images directly if /banana is available).

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
| `author_name` | Name for attribution on quote cards |

## References

Load these before generating output:

- `references/image-prompts.md` -- prompt engineering patterns for /banana
- `references/platform-specs.md` -- image dimensions per platform

## Output 1: Quotable Moments

**File:** `quotes/quotes.md`

Select exactly 5 quotes from the content atoms. Rank and pick using these criteria
(in priority order):

### Selection Criteria

| # | Criterion | What to Look For | Best Atom Types |
|---|-----------|-------------------|-----------------|
| 1 | **Standalone impact** | Works perfectly without any surrounding context. A stranger seeing just this line would understand and feel something. | `quote`, `contrarian`, `tldr` |
| 2 | **Statistical weight** | Contains a specific number, percentage, or data point that anchors the claim. | `stat`, `casestudy` |
| 3 | **Contrarian angle** | Challenges conventional wisdom or says something most people would disagree with at first glance. | `contrarian`, `prediction` |
| 4 | **Emotional resonance** | Provokes a feeling -- surprise, validation, frustration, curiosity, motivation. | `quote`, `analogy`, `insight` |
| 5 | **Practical insight** | Gives the reader something actionable they can use immediately. | `howto`, `insight` |

**Rules:**
- Pick the 5 BEST quotes across all criteria -- do not force one per criterion
- Prefer atoms rated 4-5 impact
- Polish slightly for readability if needed (fix grammar, trim filler) but
  preserve the author's voice and meaning
- Each quote should be 1-2 sentences max (under 200 characters ideal for cards)
- If the content has fewer than 5 strong quotes, use what exists; never pad

### Quote Output Format

For each quote:

```markdown
### Quote [N]

**Text:** "[Exact or polished quote]"
**Attribution:** [Author/Speaker Name]
**Criterion:** [Which selection criterion it satisfies]
**Source Atom:** [Atom number and type from atomization]
**Card Text (short):** [Condensed to under 120 chars if original is longer]
```

## Output 2: /banana Image Prompts

**File:** `quotes/banana-prompts.md`

For each of the 5 quotes, generate a /banana-compatible image prompt using the
5-Component Formula.

### The 5-Component Formula

Every prompt must specify these 5 components in order:

| Component | Description | Example |
|-----------|-------------|---------|
| **Subject** | What the image shows (abstract or concrete) | "Minimalist desk workspace" |
| **Action** | Movement or state of the subject | "bathed in soft morning light" |
| **Context** | Environment or background setting | "against a clean gradient background" |
| **Composition** | Layout, framing, text placement zone | "left-aligned with 40% right margin for text overlay" |
| **Style** | Visual aesthetic and rendering approach | "editorial photography, muted tones, shallow depth of field" |

### Prompt Template

```
/banana generate

**Subject:** [subject description]
**Action:** [action or state]
**Context:** [background/environment]
**Composition:** [layout and text zone]
**Style:** [aesthetic direction]
**Dimensions:** [WxH based on target platform]
**Text Overlay:** "[exact quote text]"
**Attribution:** [author name, positioned bottom-right]
**Color Palette:** [3-4 hex colors based on content mood]
```

### Target Aspect Ratios

Generate prompts for all three sizes per quote:

| Platform | Aspect Ratio | Dimensions | Use Case |
|----------|-------------|------------|----------|
| Social (general) | 1:1 | 1080x1080 | LinkedIn, Facebook, default |
| Instagram feed | 4:5 | 1080x1350 | Instagram posts |
| Twitter/X | 16:9 | 1600x900 | Twitter cards, blog headers |

**Default:** Generate the 1:1 prompt. Note the other dimensions in the prompt file
for manual adaptation.

### Color Palette by Content Mood

| Mood | Palette Direction | Example Hex |
|------|-------------------|-------------|
| Professional/Authority | Navy, charcoal, white, gold accent | #1B2A4A, #333333, #FFFFFF, #C9A84C |
| Energetic/Motivational | Deep orange, white, dark gray | #E85D26, #FFFFFF, #2D2D2D, #FF8C42 |
| Calm/Thoughtful | Sage green, cream, soft gray | #7C9A82, #F5F0E8, #9E9E9E, #4A6B52 |
| Bold/Contrarian | Red, black, white | #D32F2F, #1A1A1A, #FFFFFF, #FF5252 |
| Tech/Innovation | Electric blue, dark bg, white text | #2196F3, #0D1117, #FFFFFF, #64B5F6 |
| Creative/Playful | Purple, teal, light bg | #7B1FA2, #00897B, #FAFAFA, #CE93D8 |

Analyze the `primary_topic`, `voice_profile`, and strongest atom types to select the
appropriate mood and palette.

## Image Generation Logic

### If `--images` flag AND /banana is available:

1. Generate all 5 quote card images at 1:1 (1080x1080)
2. Save to `images/quote-card-1.png` through `images/quote-card-5.png`
3. Also save the prompts to `quotes/banana-prompts.md` for reference
4. Note in output: "5 quote card images generated via /banana"

### If /banana is NOT available:

1. Save all prompts to `quotes/banana-prompts.md`
2. Include full prompt text for each quote in all 3 aspect ratios
3. Note in output: "Image prompts saved. Run /banana with these prompts to generate visuals."

### If `--images` flag is NOT set:

1. Save prompts only to `quotes/banana-prompts.md`
2. Note: "Use --images flag to auto-generate quote cards"

## Font Style Suggestions

Include a font direction for each quote card:

| Content Tone | Font Style | Examples |
|-------------|------------|---------|
| Professional | Sans-serif bold | Montserrat Bold, Inter Black |
| Personal/Story | Serif elegant | Playfair Display, Lora |
| Casual/Witty | Rounded sans | Nunito, Quicksand |
| Data/Technical | Monospace accent | JetBrains Mono, Fira Code |
| Motivational | All-caps sans | Oswald, Bebas Neue |

## Error Handling

| Condition | Action |
|-----------|--------|
| Fewer than 5 quotable atoms | Use what exists; generate prompts for each; note count |
| No `quote` type atoms | Extract quotable lines from `insight`, `contrarian`, `stat` atoms |
| Author name unknown | Use "Unknown" or ask parent agent; omit attribution line on card |
| /banana returns error | Save prompts; note failure; suggest manual generation |
| `brief_mode` is true | Generate 3 quotes instead of 5; 1:1 prompts only |
| Content mood ambiguous | Default to Professional/Authority palette |
