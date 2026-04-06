---
name: repurpose-quora
description: >
  Generates Quora content from content atoms: a detailed answer to a relevant question,
  a Quora Space post for thought leadership, and question suggestions for authority
  building. Optimizes for expertise signals, SEO value, and upvote-worthy depth.
  Sub-skill of the Content Repurposing Engine. Use when user says "quora",
  "quora answer", "quora space", "quora post", or "repurpose for quora".
user-invokable: true
argument-hint: "[url-or-atoms]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Quora Content Generator

Produce a detailed answer, a Quora Space post, and question suggestions
from the content atoms provided by the orchestrator.

## Inputs

Received from the parent agent (`repurpose-longform`):

| Input | Description |
|-------|-------------|
| `atoms` | Full list of content atoms with types and impact ratings |
| `main_argument` | One-sentence thesis of the source content |
| `target_audience` | Who benefits from this content |
| `primary_topic` | Category or niche |
| `voice_profile` | Detected or overridden brand voice |
| `brief_mode` | If true, produce answer only (skip Space post and questions) |

## References

Load before generating:
- `references/platform-specs.md` -- Quora character limits, posting times, algorithm weights
- `references/voice-adaptation.md` -- Quora tone rules (expert, evidence-based)
- `references/hook-formulas.md` -- opening hooks for answers and Space posts

## Core Principle: Authority Through Depth

Quora rewards expertise, not marketing. The platform's algorithm and community
both prioritize thorough, evidence-based answers over shallow or promotional content.

**What this means for output:**
- The answer must be **complete and standalone** -- a reader should learn everything
  they need without clicking any link
- Lead with direct answers, not preamble. Quora readers are impatient with "great question!" openings.
- Credentials and specificity build trust. "After analyzing 200 campaigns..." beats "In my experience..."
- Google indexes Quora answers heavily -- treat every answer as a **mini SEO landing page**
- One external link maximum per answer, placed naturally in context or at the bottom
- Never use phrases like "check out my article" or "I wrote about this on my blog"
- Instead: "I covered the full methodology with data here: [link]" (if the link adds genuine value)

## Output 1: Answer

**File:** `quora/answer.md`

### Question

Derive the best question to answer from the content atoms. The question should be:
- Something a real Quora user would actually search for or ask
- Specific enough to have a clear answer, broad enough to attract traffic
- Aligned with the strongest atoms (especially `insight`, `stat`, `howto`)

**Question formulas (pick the best fit):**

| Formula | When to Use |
|---------|-------------|
| "What is the best way to [achieve outcome]?" | When content has clear methodology or steps |
| "Why does [common approach] fail at [topic]?" | When content has contrarian or diagnostic insights |
| "How do [professionals] approach [topic] differently?" | When content reveals expert-level distinctions |
| "What are the most common mistakes in [topic]?" | When content identifies pitfalls or anti-patterns |
| "Is [common belief] actually true for [topic]?" | When content challenges conventional wisdom |

### Answer Structure

**Length:** 300-1000 words. Quora's algorithm favors depth -- longer detailed answers
get 2-3x more upvotes than short ones.

**Format:** Quora-native formatting (bold, italic, headers, lists, blockquotes).

**Structure:**

1. **Direct Answer** (2-3 sentences)
   Open by directly answering the question. No throat-clearing, no "Great question!",
   no biography. The first two sentences should deliver the core answer so clearly
   that a reader could stop here and still benefit.

2. **Evidence and Depth** (3-5 paragraphs)
   Expand with the strongest atoms. Use specific numbers, examples, and comparisons.
   Each paragraph should add a distinct layer of value:
   - Paragraph 1: The primary insight with supporting data
   - Paragraph 2: A real-world example or case study
   - Paragraph 3: The nuance -- when this applies, when it doesn't
   - Paragraphs 4-5 (optional): Additional evidence or secondary insights

3. **Practical Steps** (bulleted, 3-5 items)
   Translate insights into actionable takeaways. Use Quora formatting:
   ```
   **Step 1: [Action]** -- [Brief explanation]
   **Step 2: [Action]** -- [Brief explanation]
   ```

4. **Closing Thought** (1-2 sentences)
   End with either a forward-looking statement or a qualifier that shows intellectual
   honesty ("This works for X context; for Y, you'd adjust by...").

5. **Optional Link** (1 sentence, separate from the answer body)
   Only if the original content adds substantial depth beyond the answer.
   Frame: "Full breakdown with [specific extra value] here: [link]"

### Tone Rules

| Do | Do NOT |
|----|--------|
| Use "I" and share experience with specifics | Make vague, unsubstantiated claims |
| Lead with the answer, then explain | Start with "Great question!" or autobiography |
| Cite numbers, studies, or concrete examples | Use marketing buzzwords or jargon |
| Acknowledge nuance and edge cases | Speak in absolutes |
| Use bold for key terms and takeaways | Use ALL CAPS or excessive formatting |
| Write in clear, structured paragraphs | Write wall-of-text blocks |
| Be authoritative but approachable | Be condescending or pedantic |
| Credit sources when referencing data | Present others' work as your own |

### Quora Formatting Reference

```
**bold text**
*italic text*
- bullet point
1. numbered list
> blockquote
[link text](url)

Headers are created with bold text on its own line.
Two line breaks = new paragraph.
```

## Output 2: Space Post

**File:** `quora/space-post.md`

A shorter, more opinion-forward piece for a relevant Quora Space.

### Space Post Structure

**Length:** 150-300 words. Space posts are lighter than answers -- think LinkedIn post
energy but with Quora's intellectual depth.

**Structure:**
1. **Hook** (1-2 sentences) -- Bold observation or insight from the atoms
2. **Body** (2-3 short paragraphs) -- Personal take, supporting evidence, practical angle
3. **Discussion prompt** (1 sentence) -- Invite Space members to share their perspective
4. **Suggested Space** -- Name 1-2 relevant Quora Spaces based on the content topic

### Space Selection Criteria
- Topic relevance: Space actively discusses this subject
- Activity level: Prefer Spaces with regular posting and engagement
- Size: Medium Spaces (10k-100k followers) for best visibility

**Common Space categories by content type:**

| Content Topic | Likely Spaces |
|---------------|---------------|
| Marketing | Marketing Strategies, Digital Marketing, Content Marketing |
| Entrepreneurship | Startups, Business Strategy, Entrepreneurship |
| Tech/SaaS | Technology Trends, Software Engineering, Product Management |
| Productivity | Personal Productivity, Self-Improvement, Time Management |
| Writing/Content | Writing Tips, Content Creation, Blogging |
| SEO | Search Engine Optimization, Digital Marketing |
| AI/Automation | Artificial Intelligence, Machine Learning, AI Tools |

## Output 3: Question Suggestions

**File:** `quora/questions.md`

Analyze the content topic and suggest 3-5 questions the user could find and answer on Quora.

**For each question, provide:**

| Field | Description |
|-------|-------------|
| Question | The exact question text as it would appear on Quora |
| Relevance | Why this content can answer it well (1 sentence) |
| Competition | Low / Medium / High -- based on how many quality answers likely exist |
| SEO Potential | Low / Medium / High -- based on whether the question likely gets Google traffic |
| Adaptation Notes | Any changes needed to the answer for this specific question |

**Question selection criteria:**
1. **Topic match** -- the question naturally aligns with the content atoms
2. **Search intent** -- the question reflects what people actually search for on Google
3. **Answer gap** -- questions where existing answers are shallow or outdated
4. **Evergreen potential** -- questions that will stay relevant for months or years

## Error Handling

| Condition | Action |
|-----------|--------|
| Fewer than 3 atoms | Write a shorter answer (200-400 words); focus on one insight |
| No `insight` or `stat` atoms | Use `howto` + `quote` atoms; frame as practical guide |
| `brief_mode` is true | Generate answer only; skip Space post and question suggestions |
| Topic is too niche for broad Quora reach | Note in questions.md; suggest specific Spaces instead |
| Content is purely promotional | Reframe entirely around the expertise; strip all product mentions |
| No clear question derivable | Use the `tldr` atom to reverse-engineer a "How to..." question |
