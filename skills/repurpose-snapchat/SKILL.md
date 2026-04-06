---
name: repurpose-snapchat
description: >
  Generates Snapchat content from content atoms: story scripts (3-5 frames at 10s each),
  Spotlight scripts (up to 60s vertical video), and AR lens concepts. Optimizes for
  completion rate, shares, and screenshot saves. Sub-skill of the Content Repurposing
  Engine. Use when user says "snapchat", "snap story", "snapchat spotlight", "snap",
  or "repurpose for snapchat".
user-invokable: true
argument-hint: "[url-or-atoms]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Snapchat Content Generator

Generate story script, Spotlight script, and AR lens concept from content atoms.

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
| `brief_mode` | If true, produce 1 story script only |

## References

Load before generating:
- `references/platform-specs.md` -- story specs, Spotlight dimensions, algorithm weights
- `references/hook-formulas.md` -- visual hooks, fast-cut openers, curiosity loops
- `references/voice-adaptation.md` -- Snapchat tone rules (ultra-casual, ephemeral, raw)

## Platform Rules

| Spec | Value |
|------|-------|
| Story segments | 10 seconds each, up to 60s total |
| Spotlight | Up to 60 seconds (single video, like TikTok) |
| Dimensions | 1080x1920 (9:16) for all content |
| Algorithm | Completion rate + shares + screenshot saves |
| Text overlay | Avoid bottom 25% (Snapchat UI elements) |
| Geofilters | Location-based overlays (optional interactive layer) |
| Best time | Mon-Fri 10PM-1AM (younger audience, late-night) |

## Output 1: Story Script (3-5 Frames)

Write to `snapchat/story-script.md`.

### Frame-by-Frame Structure

| Frame | Duration | Content | Interactive Element |
|-------|----------|---------|-------------------|
| **Frame 1** | 10s | Hook -- bold text or shocking visual to stop tapping through | Poll sticker or Question sticker |
| **Frame 2** | 10s | Key insight from content (1 atom, simplified) | None (let them read/watch) |
| **Frame 3** | 10s | Supporting point, stat, or relatable moment | Emoji slider or Quiz sticker |
| **Frame 4** | 10s | Actionable takeaway or "here's what to do" | None |
| **Frame 5** | 10s | CTA: swipe-up link, "screenshot this", or reply prompt | Link attachment (if applicable) |

### Story Rules
- Dimensions: 1080x1920 (9:16) for all frames
- 3-5 frames optimal (Snap attention spans are short)
- Ephemeral feel: raw, unpolished, in-the-moment aesthetic
- Use interactive stickers (polls, questions, emoji sliders) on at least 2 frames
- Text should be large, centered, and readable in under 3 seconds
- Avoid bottom 25% of screen for all text and stickers (Snapchat UI overlap)
- Each frame conveys one idea maximum

### Visual Direction

For each frame, specify:
- Background (selfie-style shot, solid color, quick video clip, or photo)
- Text overlay (large, bold, 3-8 words max, positioned in top 75%)
- Sticker type and placement (if applicable)
- Voiceover or caption (1-2 sentences, conversational)
- Transition (snap cut, no fancy transitions -- raw feels authentic)

### Tone Rules

| Do | Don't |
|----|-------|
| Write like you're texting a friend | Write like a brand or influencer |
| Use slang and informal language | Use corporate speak or jargon |
| Keep it raw and unpolished | Over-produce or over-edit |
| Make it feel spontaneous | Make it feel scripted or rehearsed |
| Use "you" and "lol" and "ngl" | Use formal language or complete sentences |
| Encourage screenshots and replies | Ask for likes or follows (not Snap culture) |

## Output 2: Spotlight Script (Up to 60s)

Write to `snapchat/spotlight-script.md`.

### Spotlight Structure

| Timestamp | Section | Content |
|-----------|---------|---------|
| **0-2s** | Hook | Stop-scrolling moment. Visual or text that makes them NOT swipe away. |
| **2-8s** | Setup | Quick context: "ok so basically..." or "nobody talks about this but..." |
| **8-30s** | Value | Core insight from 2-3 atoms. Fast cuts, one point per segment. |
| **30-45s** | Proof/Payoff | The "aha" moment -- stat, result, or surprising reveal |
| **45-55s** | CTA | "screenshot this", "share with someone who needs this", or reply prompt |
| **55-60s** | Loop point (optional) | End with something that makes sense looping back to the start |

### Spotlight Rules
- Dimensions: 1080x1920 (9:16 vertical)
- Maximum: 60 seconds (shorter = better for completion rate)
- Hook in first 2 seconds is non-negotiable (determines swipe-away rate)
- Completion rate is the #1 algorithm signal -- every second must earn the next
- Raw/casual feel over polished production (Snapchat culture values authenticity)
- Jump cuts and fast pacing preferred (3-5 second segments)
- Loop-friendly endings boost replay metrics

### Text Overlay Suggestions

For each section of the Spotlight, suggest:
- On-screen text (key phrase, 3-6 words)
- Text position (top or center -- NEVER bottom 25%)
- Style (handwritten feel, bold sans-serif, or Snapchat native text)

### Audio Direction
- Suggest whether to use: voiceover, trending sound, or no audio (text-only)
- If voiceover: write it conversationally -- sounds like talking to a friend, not presenting
- Trending sounds boost Spotlight discoverability but must match content vibe
- Raw audio (talking to camera) performs best for authenticity

## Output 3: AR Lens Concept

Write to `snapchat/ar-concept.md`.

Design one interactive AR lens concept tied to the content topic.

### AR Concept Structure

1. **Lens name** (catchy, shareable, 3-5 words)

2. **Description** (1 paragraph)
   - What the lens does when activated
   - How it ties to the content topic
   - What the user sees and interacts with
   - Why it would be fun to share (virality angle)

3. **Interaction type**
   - Face filter, world lens, or game lens
   - Trigger: tap, open mouth, raise eyebrows, point camera at object, etc.

4. **Shareability hook**
   - Why someone would screenshot or send this to a friend
   - How it creates user-generated content around the topic

### AR Concept Rules
- Keep it simple -- one core interaction, not a complex game
- Must tie directly to the content's primary topic or main argument
- Prioritize shareability: the best lenses make people want to show others
- Describe the concept clearly enough for a Lens Studio developer to build it

## Image Prompts

If `--images` flag is set, suggest:
- **Story frames**: 9:16 (1080x1920) background concepts for each frame
- **Spotlight thumbnail**: 9:16 (1080x1920) cover frame concept
- Include /banana prompt descriptions (subject, context, style, raw/casual aesthetic)

## Output Format

Each output file should use this structure:

```markdown
# Snapchat Story: [Topic]

## Frame 1 -- Hook
**Visual:** [direction]
**Text overlay:** [text, positioned in top 75%]
**Voiceover:** [caption]
**Sticker:** [type and placement]

## Frame 2 -- [Label]
...

---
**Posting notes:** [best time, interactive sticker strategy, completion tips]
```

## Brief Mode

If `--brief` is active, produce only:
- 1 story script (3 frames, highest-impact atoms)
- Skip Spotlight script and AR lens concept

## Error Handling

| Condition | Action |
|-----------|--------|
| Fewer than 3 atoms | Shorten story to 3 frames; skip Spotlight |
| Content too formal/corporate | Aggressively rewrite in ultra-casual Gen-Z tone; preserve core meaning |
| No video-friendly content | Focus on text-overlay story frames with bold visuals |
| `--images` but no /banana | Save prompts to file; note for manual creation |
| Target audience skews older | Note in posting notes that Snapchat skews 13-34; suggest adapting tone |
| Content is evergreen/long-form | Break into bite-sized moments; Snapchat rewards ephemeral, timely content |
