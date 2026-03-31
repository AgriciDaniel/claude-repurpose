---
name: repurpose-linkedin
description: >
  Generates LinkedIn content from content atoms: text posts with hook-first formatting,
  PDF carousel slide scripts (10-12 slides), and strategic polls. Optimizes for saves,
  meaningful comments, and the critical first 60-90 minute window. Sub-skill of the
  Content Repurposing Engine.
user-invokable: false
---

# LinkedIn Content Generator

Generate text post, carousel slide script, and poll from content atoms.

## Inputs

You receive from the orchestrator:
- **Content atoms** (typed and impact-rated)
- **Main argument**, target audience, primary topic
- **Brand voice profile** (5-dimension scores or override flag)
- **Flags**: `--brief` (1 post only), `--images` (generate image prompts)

## References

Load before generating:
- `references/platform-specs.md` -- character limits, carousel specs, algorithm weights
- `references/hook-formulas.md` -- curiosity gap, contrarian, data-driven, question hooks
- `references/voice-adaptation.md` -- LinkedIn tone rules (professional, opinion-led, no bait)
- `references/poll-strategy.md` -- poll derivation, option constraints, follow-up strategy

## Platform Rules

| Spec | Value |
|------|-------|
| Post character limit | 3,000 characters |
| First visible line | 60-90 characters before "see more" fold |
| PDF carousel | Up to 300 pages, 100MB; 6.60% engagement (highest format) |
| Images | 1080x1080 (1:1) or 1080x1350 (4:5) |
| Algorithm | Saves = 5x a like; only comments >10 words count |
| External links | 40% less reach -- always place in FIRST COMMENT |
| Hashtags | 3-5 optimal |
| Poll engagement | 4.4-8.9% (highest engagement format after carousels) |
| Best time | Tuesday-Thursday 8-10AM |
| Critical window | First 60-90 minutes determine distribution |

## Output 1: Text Post

Write to `linkedin/post.md`.

### Post Structure

1. **Hook** (first 60-90 characters)
   - This is the only text visible before the "see more" fold on mobile
   - Use a curiosity gap, bold claim, or data-driven hook from hook-formulas.md
   - Must compel the click to expand
   - No hashtags, no emoji, no fluff in the hook line

2. **Body** (short single-line paragraphs)
   - One idea per paragraph, 1-2 sentences each
   - Use strategic line breaks and whitespace for scannability
   - Weave in 2-3 atoms: combine insights, stats, and actionable takeaways
   - Include at least one data point or specific result

3. **Key insight with data**
   - Dedicate 1-2 paragraphs to the strongest stat or case study atom
   - Use precise numbers (6.60%, not "around 7%")

4. **Engagement question**
   - End with a specific question that invites thoughtful responses (>10 words)
   - Avoid generic "Agree?" or "Thoughts?" -- ask something that requires personal experience

5. **Hashtags** (3-5)
   - Place at the very end, after the engagement question
   - Mix broad (#ContentMarketing) with niche (#ContentRepurposing)

### Save-Worthy Content
Saves = 5x a like on LinkedIn. Optimize for save-worthy formats:
- Checklists and frameworks
- Data-backed insights
- Step-by-step processes
- Counterintuitive findings

### External Link Handling
Links in the post body reduce reach by 40%. Always:
1. Write "Link in comments" or a specific note in the post body
2. Include the URL separately, marked as "FIRST COMMENT" in the output
3. The user posts the link as their first comment immediately after publishing

## Output 2: PDF Carousel Slide Script

Write to `linkedin/carousel.md`.

Generate a 10-12 slide script. Each slide includes title, bullet points, and visual direction.

### Slide Structure

| Slide | Content | Visual Direction |
|-------|---------|-----------------|
| **Slide 1** | Bold title (5-8 words) + hook subtitle | Pattern interrupt: bold color, high contrast, "Swipe ->" cue |
| **Slides 2-10** | One insight per slide: title + 2-3 bullet points | Clean typography, generous whitespace, 28px+ title text |
| **Slide 11** | Summary/key takeaway | Recap the 3 most important points |
| **Final slide** | CTA + "Save this for later" | Follow prompt, profile tag, save reminder |

### Carousel Rules
- Dimensions: 1080x1350 (4:5 portrait) for maximum feed presence
- Each slide must be readable in under 5 seconds
- Title text: 28px or larger equivalent (bold, high contrast)
- Body text: 2-3 bullet points maximum per slide (not paragraphs)
- One core idea per slide -- never combine two concepts
- Progress indicator optional (e.g., "3/10" in corner)
- Final slide CTA: combine "Save", "Share", and "Follow" prompts

### Visual Direction Notes
For each slide, include:
- Suggested background treatment (solid, gradient, or subtle pattern)
- Text alignment and hierarchy
- Any icon or visual element suggestions
- Color guidance (consistent throughout the deck)

## Output 3: Poll

Write to `linkedin/poll.md`.

Derive one poll from the content's key decision point.

| Spec | Constraint |
|------|-----------|
| Options | 2-4 |
| Chars per option | 30 maximum |
| Duration | Suggest 1 week (7 days) |
| Engagement rate | 4.4-8.9% expected |

**Poll structure:**
- **Context paragraph**: 2-3 sentences framing why this question matters (hook + stakes)
- **Question**: specific, relevant to the target audience's daily decisions
- **Options**: represent real positions the audience holds; include one contrarian option
- **Follow-up note**: suggest sharing results as a future post (closes the content loop)

## Image Prompts

If `--images` flag is set, suggest:
- **Post image**: 1:1 (1080x1080) or 4:5 (1080x1350) for the text post
- **Carousel cover**: 4:5 (1080x1350) for slide 1
- Include /banana prompt descriptions (subject, context, style, composition)

## Output Format

Each output file should use this structure:

```markdown
# LinkedIn Post: [Topic]

[Full post text with line breaks preserved]

---
**First comment:** [URL or additional context to post as first comment]
**Hashtags:** [included in post]
**Best posting time:** Tuesday-Thursday 8-10AM
**Optimization notes:** [save triggers, engagement hooks]
```

## Brief Mode

If `--brief` is active, produce only:
- 1 text post (use highest-impact atoms)
- Skip carousel and poll
