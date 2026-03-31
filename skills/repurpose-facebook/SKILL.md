---
name: repurpose-facebook
description: >
  Generates Facebook content from content atoms: community-focused text posts, polls
  with up to 10 options, and story scripts. Optimizes for saves, DM shares, and
  question-ending formats that drive comments. Sub-skill of the Content Repurposing
  Engine.
user-invokable: false
---

# Facebook Content Generator

Generate text post, poll, and story script from content atoms.

## Inputs

You receive from the orchestrator:
- **Content atoms** (typed and impact-rated)
- **Main argument**, target audience, primary topic
- **Brand voice profile** (5-dimension scores or override flag)
- **Flags**: `--brief` (1 post only), `--images` (generate image prompts)

## References

Load before generating:
- `references/platform-specs.md` -- post limits, image specs, algorithm weights
- `references/hook-formulas.md` -- question hooks, curiosity gap, warning-style
- `references/voice-adaptation.md` -- Facebook tone rules (warm, community-focused, question-ending)

## Platform Rules

| Spec | Value |
|------|-------|
| Post length | No strict limit; optimal 40-80 chars for highest engagement |
| Images | 1080x1350 (4:5) best for feed |
| Video | Up to 240 min; all video auto-classified as Reels |
| Story | 1080x1920 (9:16), 15-second segments |
| Algorithm | Saves + DM shares most powerful signals |
| Feed composition | 50% from non-followed accounts (discovery opportunity) |
| Content mix | 80% value / 20% promotional (strict) |
| Poll options | Up to 10 |
| Best time | Tuesday 9AM-12PM |

## Output 1: Text Post

Write to `facebook/post.md`.

### Post Strategy

Facebook rewards community-building signals. Every post should feel like the start of a conversation, not a broadcast.

### Post Structure

1. **Hook** (first 1-2 lines)
   - Short, attention-grabbing opener
   - 40-80 characters is the sweet spot for pure engagement
   - For value-driven content, longer posts work if the hook earns the read
   - Use question hooks or curiosity gaps from hook-formulas.md

2. **Value body** (for longer posts)
   - Short paragraphs, 1-2 sentences each
   - Conversational tone with warmth and inclusivity
   - Draw from 2-3 atoms: insights, stats, or how-to steps
   - Use emoji sparingly as visual markers (2-4 per post)

3. **Closing question**
   - Every post MUST end with a question
   - Question-ending posts get 2x comments on Facebook
   - Ask for personal experience, opinions, or stories
   - Be specific: "What was YOUR biggest win this week?" not "Thoughts?"

### Content Mix Rule
Ensure the post follows the 80/20 rule:
- 80% pure value (education, entertainment, inspiration, community)
- 20% promotional (only if explicitly needed)
- When in doubt, lean 100% value. Facebook penalizes promotional content.

### Save + Share Optimization
Saves and DM shares are the most powerful algorithm signals. Create content worth saving:
- Frameworks and checklists
- Surprising data points
- Relatable observations
- Actionable tips that apply immediately

## Output 2: Poll

Write to `facebook/poll.md`.

Facebook polls support up to 10 options, making them more flexible than other platforms.

| Spec | Constraint |
|------|-----------|
| Options | 2-10 (use 4-6 for best balance) |
| Image/GIF | Strongly recommended (polls with images outperform text-only) |
| Tone | Conversational, community question |

### Poll Structure

1. **Context** (1-2 sentences)
   - Frame the poll question with a brief setup
   - Connect it to a relatable experience or the content's main theme

2. **Question**
   - Conversational and specific
   - Derived from the content's key decision point, debate, or preference
   - Frame as a community question: "For our community..." or "I'm curious..."

3. **Options** (4-6 recommended)
   - Each represents a genuine position or choice
   - Include one playful or unexpected option to boost engagement
   - Order from most expected to most surprising

4. **Image/GIF suggestion**
   - Recommend adding a relevant image or GIF to boost visibility
   - Describe the visual concept for /banana or manual creation

## Output 3: Story Script

Write to `facebook/story.md`.

Stories are ephemeral (24h) and should feel casual, in-the-moment, and interactive.

### Story Structure (3-5 Frames)

| Frame | Duration | Content | Interactive Element |
|-------|----------|---------|-------------------|
| **Frame 1** | 5-10s | Hook question or bold statement | Poll sticker or Question sticker |
| **Frame 2** | 5-10s | Key insight from content (1 atom) | None (let them read) |
| **Frame 3** | 5-10s | Supporting point or stat | Emoji slider or Quiz sticker |
| **Frame 4** | 5-10s | Actionable takeaway | None |
| **Frame 5** | 5-10s | CTA: "See full post" or engagement prompt | Link sticker (if applicable) |

### Story Rules
- Dimensions: 1080x1920 (9:16) for all frames
- 3-5 frames optimal (respect attention spans)
- Ephemeral feel: casual, raw, less polished than feed posts
- Use interactive stickers (polls, questions, emoji sliders) on at least 2 frames
- Text should be large, centered, and readable at a glance
- Each frame conveys one idea in under 10 seconds

### Story Visual Direction
For each frame, specify:
- Background (solid color, gradient, photo, or video still)
- Text overlay (large, bold, 5-10 words max)
- Sticker type and placement
- Transition suggestion (if any)

## Image Prompts

If `--images` flag is set, suggest:
- **Post image**: 4:5 (1080x1350) concept for the text post
- **Poll image**: visual concept to accompany the poll
- **Story frames**: 9:16 (1080x1920) background concepts
- Include /banana prompt descriptions

## Output Format

```markdown
# Facebook Post: [Topic]

[Full post text]

---
**Posting notes:** [best time, content mix compliance, engagement strategy]
```

## Brief Mode

If `--brief` is active, produce only:
- 1 text post (highest-impact atoms, question-ending)
- Skip poll and story
