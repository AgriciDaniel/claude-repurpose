---
name: repurpose-youtube
description: >
  Generates YouTube Community tab content from content atoms: text posts, image concepts,
  and polls with up to 5 options. Optimizes for between-upload engagement, subscriber
  retention, and poll-driven interaction. Sub-skill of the Content Repurposing Engine.
user-invokable: false
---

# YouTube Community Post Generator

Generate text post, image concept, and poll from content atoms.

## Inputs

You receive from the orchestrator:
- **Content atoms** (typed and impact-rated)
- **Main argument**, target audience, primary topic
- **Brand voice profile** (5-dimension scores or override flag)
- **Flags**: `--brief` (1 post only), `--images` (generate image prompts)
- **Source URL** (if input was a YouTube video, reference it)

## References

Load before generating:
- `references/platform-specs.md` -- Community tab specs, poll limits, image sizes
- `references/hook-formulas.md` -- question hooks, curiosity gap openers
- `references/voice-adaptation.md` -- YouTube tone rules (casual, fan-oriented, interactive)

## Platform Rules

| Spec | Value |
|------|-------|
| Text limit | 5,000 characters |
| Poll options | Up to 5 |
| Chars per option | 65 (text polls), 36 (image polls) |
| Images | 1080x1080 or 1280x1280, max 16MB, JPG/PNG/GIF/WEBP |
| Frequency | 2-4 posts per week optimal |
| Best format | Polls (2-3x engagement vs text posts) |
| Post types | Text, image, poll, GIF |

## Core Purpose

YouTube Community posts serve a specific role: **keeping subscribers engaged between video uploads**. Every post should:
- Feel like a direct conversation with the audience (not a broadcast)
- Invite participation (vote, comment, share an opinion)
- Build anticipation for upcoming content
- Reinforce the creator's personality and niche authority

## Output 1: Text Post

Write to `youtube-community/post.md`.

### Post Structure

1. **Opening hook** (first 1-2 lines)
   - Casual, conversational tone -- like talking to a friend
   - Use a question, behind-the-scenes insight, or teaser
   - Reference the source content naturally if the input was a YouTube URL

2. **Value body** (2-4 paragraphs)
   - Draw from 2-3 atoms: insights, stats, or questions
   - Keep paragraphs short and scannable
   - Use contractions and casual language throughout
   - Match the channel's personality (detected from voice profile)

3. **Engagement close**
   - End with a direct question or invitation to comment
   - "Drop your answer below" or "Tell me in the comments"
   - Avoid generic CTAs -- be specific to the content

### Source Video Cross-Reference
If the input content was a YouTube video URL:
- Reference the video naturally: "In my latest video, I covered..."
- Do NOT just summarize the video -- add a new angle, ask for feedback, or share a behind-the-scenes take
- Link back only if it adds value (Community posts can include links)

### Post Tone
- Casual and fan-oriented, like a creator talking to their community
- First-person, personal, conversational
- Emoji usage matches the channel personality (moderate by default)
- Never formal, corporate, or scripted-sounding

## Output 2: Image Concept

Write to `youtube-community/image-concept.md`.

Create a concept description for a shareable image post. This is NOT the image itself -- it is a detailed brief for creation via /banana or manual design.

### Image Concept Structure

1. **Post text** (1-3 sentences above the image)
   - Brief context that frames the image
   - Question or prompt that invites comments

2. **Image description**
   - Dimensions: 1080x1080 (1:1) or 1280x1280
   - Subject: what the image depicts (quote card, infographic, meme, behind-the-scenes)
   - Text overlay: exact text to display on the image (if any)
   - Style: matches channel aesthetic
   - Color palette: suggest based on brand or content mood

3. **/banana prompt** (if `--images` flag is set)
   - Full 5-component prompt: Subject, Action, Context, Composition, Style
   - Aspect ratio: 1:1
   - Filename suggestion

### Image Types That Work
- Quote cards with a key insight from the content
- Data/stat highlights (one big number with context)
- Behind-the-scenes or "making of" concept
- Meme-style content that matches the niche
- Infographic snippet (one section, not a full infographic)

## Output 3: Poll

Write to `youtube-community/poll.md`.

Polls are the highest-engagement Community post format (2-3x vs text). Always generate one.

| Spec | Constraint |
|------|-----------|
| Options | Up to 5 |
| Chars per option | 65 maximum |
| Format | Text poll (image polls: 36 chars/option) |

### Poll Structure

1. **Context** (1-2 sentences)
   - Frame the question with brief setup
   - Make it feel like you genuinely want to know the audience's opinion

2. **Question**
   - Derived from the content's key debate, decision point, or prediction
   - Specific and relevant to the audience's experience
   - Conversational tone: "Quick question for you all..."

3. **Options** (3-5 recommended)
   - Each represents a genuine position
   - Include one fun/unexpected option (e.g., "Show me the results" or a humorous take)
   - Order: most common answer first, wildcard last

4. **Follow-up plan**
   - Note: suggest sharing results in a future video or Community post
   - Creates a content loop: poll -> results post -> discussion

## Between-Upload Value

Community posts fill the gap between video uploads. Suggest a posting rhythm:
- **Day after upload**: Poll related to the video's topic
- **Mid-week**: Behind-the-scenes or teaser for next video
- **Weekend**: Casual question or image post
- Target: 2-4 Community posts per week

## Output Format

```markdown
# YouTube Community Post: [Topic]

[Full post text]

---
**Posting notes:** [frequency, cross-reference to source, engagement strategy]
**Source video:** [URL if applicable, "N/A" otherwise]
```

## Brief Mode

If `--brief` is active, produce only:
- 1 poll (highest engagement format)
- Skip text post and image concept
