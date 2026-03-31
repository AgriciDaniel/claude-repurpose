---
name: repurpose-skool
description: >
  Generates Skool community content from content atoms: discussion posts framed as
  open debates, multi-day challenge prompts with action steps, and community polls.
  Enforces content rotation and teacher/leader tone. Sub-skill of the Content
  Repurposing Engine.
user-invokable: false
---

# Skool Community Post Generator

Generate discussion post, challenge prompt, and poll from content atoms.

## Inputs

You receive from the orchestrator:
- **Content atoms** (typed and impact-rated)
- **Main argument**, target audience, primary topic
- **Brand voice profile** (5-dimension scores or override flag)
- **Flags**: `--brief` (1 post only), `--images` (generate image prompts)

## References

Load before generating:
- `references/platform-specs.md` -- Skool specs, community health benchmarks
- `references/hook-formulas.md` -- question hooks, challenge framing
- `references/voice-adaptation.md` -- Skool tone rules (teacher/leader, empowering, action-oriented)

## Platform Rules

| Spec | Value |
|------|-------|
| Character limit | No strict limit |
| Supports | Text, images, GIFs, short video |
| Healthy benchmark | 20-30% monthly active members |
| Content rotation | REQUIRED: polls, discussions, challenges, questions |
| Admin responsiveness | Critical signal; respond within 2 hours |
| Growth timeline | 60-90 days to build community momentum |
| Gamification | Core to Skool; frame posts as challenges and action items |

## Content Rotation Rule

**NEVER generate the same content type twice in a row.** Skool communities thrive on variety. The three outputs below are designed to be posted on different days as part of a rotation cycle:

| Day | Type | Purpose |
|-----|------|---------|
| Day 1 | Discussion | Open debate, gather perspectives |
| Day 2 | Challenge | Action-oriented, daily check-ins |
| Day 3 | Poll | Quick engagement, community opinion |

Suggest this rotation in the output notes. The orchestrator may also generate question posts via other sub-skills -- those fill additional rotation slots.

## Output 1: Discussion Post

Write to `skool/discussion.md`.

### Discussion Structure

1. **Hook** (first 1-2 lines)
   - Frame the content as an open question or debate
   - Use a contrarian, insight, or question atom as the seed
   - Tone: curious, inviting, not lecturing

2. **Context** (2-3 paragraphs)
   - Share the key insight or finding from the source content
   - Present it as a topic for community exploration, not a settled answer
   - Include enough detail that members can form their own opinion
   - Use 2-3 atoms to build the case

3. **Discussion prompt**
   - Ask a specific, open-ended question that invites detailed responses
   - Frame it so members share their own experience, not just agree/disagree
   - Examples:
     - "What has worked for YOU when it comes to [topic]?"
     - "Do you agree with this approach, or have you found something better?"
     - "I'd love to hear how your experience compares -- drop your take below."

4. **Engagement hooks** (optional)
   - Tag specific community members who might have relevant experience
   - Reference a previous community discussion if relevant
   - Offer to compile the best responses into a resource

### Discussion Tone
- Teacher/leader voice: empowering and encouraging, not authoritative or preachy
- Frame yourself as a fellow learner exploring alongside the community
- Acknowledge that members bring valuable experience
- Use contractions, casual language, and warmth

## Output 2: Challenge Prompt

Write to `skool/challenge.md`.

Derive a 3-7 day challenge from the source content. Challenges drive the highest sustained engagement on Skool.

### Challenge Structure

1. **Challenge title**
   - Action-oriented: "The 5-Day [Topic] Challenge"
   - Specific outcome promise: "...to [measurable result]"

2. **Why this challenge** (2-3 sentences)
   - Connect to the source content's main insight
   - Frame the gap: "Most people know [insight] but never act on it"
   - This challenge bridges knowing and doing

3. **Challenge rules** (3-5 bullet points)
   - Duration: 3-7 days
   - One clear action per day
   - Reporting requirement: "Post your result in the comments each day"
   - Completion reward: badge, shoutout, or community recognition

4. **Daily action steps**

| Day | Action | Check-In Prompt |
|-----|--------|----------------|
| Day 1 | [Specific, small action derived from content] | "Post what you did + one thing you learned" |
| Day 2 | [Build on Day 1] | "Share your progress + any obstacles" |
| Day 3 | [Increase difficulty slightly] | "What surprised you so far?" |
| Day 4+ | [Continue progression] | [Relevant check-in question] |
| Final day | [Culminating action] | "Share your before/after or key takeaway" |

5. **Completion CTA**
   - "When you finish, post your results with #[ChallengeName]"
   - "I'll feature the best responses in a follow-up post"
   - Encourage members to cheer each other on

### Challenge Rules
- Each daily action must be completable in 15-30 minutes
- Actions must be specific and measurable (not "think about X" but "write down 3 examples of X")
- Progress should be visible (members can see each other's check-ins)
- Include at least one "share with the community" touchpoint per day

## Output 3: Poll

Write to `skool/poll.md`.

Community opinion poll derived from the content's key question.

### Poll Structure

1. **Context** (1-2 sentences)
   - Brief framing of the question
   - Connect to the source content or an ongoing community theme

2. **Question**
   - Community-oriented: "Where does our community stand on [topic]?"
   - Specific to the audience's decisions or experiences
   - Avoid yes/no -- prefer multi-option

3. **Options** (3-5)
   - Each represents a genuine position members might hold
   - Include one option that might spark debate
   - Members can elaborate in comments

4. **Follow-up invitation**
   - "Drop your reasoning in the comments -- I want to hear the WHY behind your vote"
   - This transforms a quick poll into a discussion thread

## Admin Responsiveness

Include a note in every output reminding the user:
- Respond to comments within 2 hours (critical Skool engagement signal)
- Ask follow-up questions to commenters to deepen discussion
- Heart/react to every response (minimum engagement)
- Admin silence kills Skool communities faster than anything else

## Skool MCP Integration

If Skool MCP tools are detected in the current session (`mcp__skool__*` tools available), note in the output:
- "Skool MCP tools detected. These posts can be published directly using the Skool MCP integration."
- Reference available tools: `skool_get_feed`, `skool_get_community`
- Note: check community guidelines before posting with `skool_get_community`

## Output Format

```markdown
# Skool Discussion: [Topic]

[Full post text]

---
**Content rotation:** Discussion (next: Challenge or Poll)
**Admin response plan:** Respond to first 5 comments within 2 hours
**Engagement target:** [realistic based on community size]
```

## Brief Mode

If `--brief` is active, produce only:
- 1 discussion post (most versatile format)
- Skip challenge and poll
