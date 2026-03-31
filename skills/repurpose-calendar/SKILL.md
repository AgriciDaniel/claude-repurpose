---
name: repurpose-calendar
description: >
  Generates a 7-day publishing calendar with staggered posts, optimal timing
  per platform, file references, engagement reminders, and theme-day grouping.
  Prevents audience fatigue by limiting to 2-3 posts per day.
user-invokable: false
metadata:
  author: AgriciDaniel
  version: "1.0.0"
  category: content
---

# Publishing Calendar Generator

Produce a 7-day staggered publishing calendar starting from the current date.
Maps all repurposed content to specific days, times, and platforms.

## Inputs

Received from the parent orchestrator:

| Input | Description |
|-------|-------------|
| `generated_outputs` | List of all content files produced by other sub-skills |
| `platforms_requested` | Which platforms were included (all if unspecified) |
| `primary_topic` | Category or niche of the source content |
| `target_audience` | Who benefits from this content |
| `current_date` | Today's date (start of the 7-day window) |

## References

Load these before generating the calendar:

- `references/platform-specs.md` -- posting limits and format rules
- `references/engagement-benchmarks.md` -- optimal timing data and engagement windows

## Output: calendar.md

**File:** `calendar.md`

### Calendar Table Format

The calendar is a markdown table with these columns:

```markdown
| Day | Date | Time | Platform | Content Type | File Reference | Image Needed | Notes |
|-----|------|------|----------|-------------|----------------|--------------|-------|
```

**Column definitions:**

| Column | Description |
|--------|-------------|
| Day | Day name (Monday, Tuesday, etc.) |
| Date | Actual date (YYYY-MM-DD) calculated from `current_date` |
| Time | Recommended posting time in local time |
| Platform | Target platform name |
| Content Type | What is being posted (tweet, thread, carousel, poll, etc.) |
| File Reference | Relative path to the output file (e.g., `twitter/thread.md`) |
| Image Needed | Yes/No -- whether this post requires an image or graphic |
| Notes | Engagement reminders, dependencies, or special instructions |

## Optimal Posting Times

Use these windows as defaults. Adjust if the user specifies a timezone or audience location.

| Platform | Best Days | Best Times (Local) | Peak Window |
|----------|-----------|---------------------|-------------|
| Twitter/X | Mon-Fri | 9-11 AM or 1-3 PM | Tue-Thu 10 AM |
| LinkedIn | Tue-Thu | 8-10 AM | Wed 9 AM |
| Instagram | Mon, Wed, Fri | 11 AM - 1 PM | Wed 12 PM |
| Facebook | Tue-Fri | 9 AM - 12 PM | Thu 10 AM |
| YouTube Community | Tue, Thu | 10 AM - 12 PM | Tue 11 AM |
| Skool | Mon, Wed, Fri | 9 AM - 11 AM | Mon 10 AM |
| Reddit | Mon-Fri | 8-10 AM EST | Tue 9 AM EST |
| Newsletter | Tue or Thu | 8-10 AM | Tue 9 AM |

## Scheduling Rules

### Rule 1: Stagger Across Days

Never post to all platforms on the same day. Spread content across the full 7-day
window to maintain consistent presence without flooding.

### Rule 2: Maximum 2-3 Posts Per Day

No more than 3 posts on any single day. Audience fatigue is real. If a day has
3 posts, they must be on 3 different platforms.

### Rule 3: Lead with Long-Form, Follow with Snippets

Publish comprehensive content first (LinkedIn article, newsletter, Reddit post),
then extract and post shorter pieces (tweets, quote cards, polls) in subsequent
days. This creates a natural content cascade.

### Rule 4: Space Repeated Platforms

If a platform appears twice in the week (e.g., Twitter standalone tweet + Twitter
thread), space them at least 2 days apart.

## Theme Days

Organize the 7-day calendar by content theme. Adapt based on which platforms were
actually generated.

### Day 1 (Start Date): Long-Form Launch

| Priority | Platform | Content Type | Notes |
|----------|----------|-------------|-------|
| 1 | LinkedIn | Text post + carousel | Lead with the authoritative version |
| 2 | Newsletter | Email excerpt (Day 0 of drip) | Send to existing subscribers |

**Engagement reminder:** "Reply to every LinkedIn comment within 60 minutes."

### Day 2: Threads and Discussions

| Priority | Platform | Content Type | Notes |
|----------|----------|-------------|-------|
| 1 | Twitter/X | Thread (8-12 tweets) | Expand on Day 1's core insight |
| 2 | Reddit | Discussion post | Peer-to-peer version of the same insight |

**Engagement reminder:** "Engage with every thread reply for 2 hours after posting."

### Day 3: Visual Content

| Priority | Platform | Content Type | Notes |
|----------|----------|-------------|-------|
| 1 | Instagram | Carousel (7-10 slides) + caption | Visual breakdown of the topic |
| 2 | Twitter/X | Standalone tweet + quote card image | Highest-impact single insight |

**Engagement reminder:** "Reply to Instagram comments within first hour for algorithm boost."

### Day 4: Engagement and Polls

| Priority | Platform | Content Type | Notes |
|----------|----------|-------------|-------|
| 1 | LinkedIn | Poll | Ask audience to weigh in on a key question |
| 2 | Twitter/X | Poll | Same question, adapted for Twitter's format |
| 3 | Facebook | Question post or poll | Conversational version |

**Engagement reminder:** "Vote in your own polls (sets the tone). Comment on early responses."

### Day 5: Community Building

| Priority | Platform | Content Type | Notes |
|----------|----------|-------------|-------|
| 1 | Skool | Challenge or action post | Give the community something to do |
| 2 | YouTube Community | Text post or poll | Engage existing subscribers |

**Engagement reminder:** "Pin a follow-up comment with additional context."

### Day 6: Drip and Reinforcement

| Priority | Platform | Content Type | Notes |
|----------|----------|-------------|-------|
| 1 | Newsletter | Email 2 (Day 2 of drip) | Deeper dive for subscribers |
| 2 | Facebook | Text post | Casual version of a key takeaway |

**Engagement reminder:** "Monitor email replies; respond to any subscriber questions."

### Day 7: Lightweight and Residual

| Priority | Platform | Content Type | Notes |
|----------|----------|-------------|-------|
| 1 | Instagram | Story or reel script | Lightweight, behind-the-scenes feel |
| 2 | Skool | Discussion post | Open-ended community question |

**Engagement reminder:** "Respond to any leftover comments from the week across all platforms."

## Drip Sequence Integration

Map the 3-email drip to calendar days: Email 1 on Day 1 (with long-form launch),
Email 2 on Day 3 or 6, Email 3 on Day 5 or 7. Shift to next weekday if start date
falls on a weekend.

## Platform Filtering

If not all platforms were generated, remove missing rows, redistribute content
(max 2-3/day still applies), compress to 3-4 days for 1-2 platforms.

## Calendar Footer

Include after the table: total pieces count, platforms covered, image assets
needed (reference `images/prompts.md`), email drip status, and these engagement
rules: respond to comments within 60 minutes, engage with 3-5 niche posts before
and after yours, never post and ghost, track top performers for future repurposing.

## Error Handling

| Condition | Action |
|-----------|--------|
| No outputs generated yet | Cannot build calendar; report error to orchestrator |
| Only 1 platform | Generate 3-day schedule; 1 post per day |
| Start date is weekend | Shift Day 1 to next Monday; compress weekend into light days |
| `brief_mode` was used | Condense to 3-day calendar; top 3 platforms only |
| Missing image assets | Mark "Image Needed: Yes" and reference `images/prompts.md` |
| Email drip not generated | Remove drip rows; note in footer |
