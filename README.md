# Claude Repurpose

![Claude Repurpose](Claude-repurpose-cover.jpg)

**Content Repurposing Engine for Claude Code** -- Turn 1 piece of content into 10+ platform-optimized posts in seconds.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://code.claude.com)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)

---

## What It Does

Takes **any content** (YouTube video, blog post, podcast, local file) and generates **platform-native** outputs for:

| Platform | Outputs |
|----------|---------|
| **Twitter/X** | Thread (8-12 tweets) + standalone tweets + poll |
| **Threads** | Thread (5-10 posts) + standalone posts + image post |
| **LinkedIn** | Post + PDF carousel script (10-12 slides) + poll |
| **Instagram** | Carousel (7-10 slides) + caption + reel script |
| **TikTok** | Video script (15-60s) + carousel/photo mode + stitch/duet concept |
| **Pinterest** | 3-5 pin descriptions + idea pin script + board suggestions |
| **Snapchat** | Story script (3-5 frames) + Spotlight script + AR concept |
| **Facebook** | Post + poll + story script |
| **YouTube Community** | Text post + image concept + poll |
| **Skool** | Discussion + challenge prompt + poll |
| **Discord** | Announcement + discussion thread + rich embed |
| **Newsletter** | Excerpt + 3 subject lines + 3-email drip sequence |
| **Reddit** | Discussion post + subreddit suggestions |
| **Quora** | Answer (300-1000 words) + Space post + question suggestions |
| **Medium** | Article (1500-3000 words) + tags + publication suggestions |
| **WhatsApp** | Channel update + poll + content teaser |
| **Telegram** | Channel post + deep dive + poll |
| **Quote Graphics** | 5 quotable moments + AI image prompts |
| **SEO Metadata** | Titles, descriptions, hashtags, keywords per platform |
| **Calendar** | 7-day publishing schedule with optimal times |

## Why Not Just Cross-Post?

Cross-posting the same text everywhere **kills engagement**. Each platform has different:
- Character limits (Twitter: 280 vs LinkedIn: 3,000)
- Algorithm preferences (Twitter rewards replies 27x, LinkedIn rewards saves 5x)
- Audience expectations (LinkedIn: professional, Reddit: peer-to-peer, TikTok: entertaining)
- Content formats (LinkedIn PDF carousels: 6.60% engagement, Instagram mixed-media: 2.33%)

This skill **adapts your message** for each platform, not just reformats it.

## Install

```bash
# One-liner
curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-repurpose/main/install.sh | bash

# Or clone and install
git clone https://github.com/AgriciDaniel/claude-repurpose.git
cd claude-repurpose && bash install.sh
```

**Optional**: Install [/banana](https://github.com/AgriciDaniel/claude-banana) for AI-generated quote cards and carousel cover images.

## Usage

```bash
# Repurpose a blog post to all platforms
/repurpose https://example.com/blog/my-article

# Repurpose a YouTube video
/repurpose https://youtube.com/watch?v=abc123

# Only specific platforms
/repurpose https://example.com/post --platforms twitter,linkedin,instagram

# Quick mode (top 3 platforms only)
/repurpose https://example.com/post --brief

# With AI-generated images (/banana required)
/repurpose https://example.com/post --images

# Override brand voice
/repurpose https://example.com/post --voice witty

# Just analyze content (no outputs)
/repurpose analyze https://example.com/post

# Generate publishing calendar from outputs
/repurpose calendar
```

## How It Works

```
Input (any content)
      |
      v
  Content Extraction        YouTube -> transcript
  (auto-detect type)        Blog URL -> article text
                            Audio -> Whisper transcription
                            Local file -> direct read
      |
      v
  Content Atomization       Extract 5-15 reusable atoms:
  (key insights, quotes,    stats, quotes, insights,
   statistics, arguments)   questions, contrarian takes
      |
      v
  6 Parallel Agents         Social (Twitter+Threads+LinkedIn+Facebook)
  (simultaneous)            Visual (Instagram+TikTok+Pinterest+Snapchat+Quotes)
                            Longform (Newsletter+Email+Reddit+Quora)
                            Community (YouTube+Skool+Discord)
                            Broadcast (WhatsApp+Telegram+Medium)
                            SEO (metadata across all)
      |
      v
  Output Directory          ./repurposed/<timestamp>/
  (30+ files organized      twitter/, linkedin/, instagram/,
   by platform)             facebook/, skool/, quotes/, etc.
```

## Output Structure

```
./repurposed/2026-03-31-1430/
├── summary.md                 # Overview of all generated content
├── atoms.md                   # Extracted content atoms
├── twitter/
│   ├── thread.md              # 8-12 tweet thread
│   ├── standalone-tweet.md     # Standalone tweets
│   └── poll.md
├── linkedin/
│   ├── post.md
│   ├── carousel.md            # Slide-by-slide script
│   └── poll.md
├── instagram/
│   ├── carousel.md            # 7-10 slide script
│   ├── caption.md
│   └── reel-script.md
├── threads/
│   ├── thread.md              # 5-10 post thread
│   ├── standalone-posts.md    # 3-5 standalone posts
│   └── image-post.md          # Image post concept
├── tiktok/
│   ├── video-script.md        # 15-60s video script
│   ├── carousel.md            # Photo mode (2-10 slides)
│   └── stitch-duet.md         # Stitch/duet concept
├── pinterest/
│   ├── pins.md                # 3-5 pin descriptions
│   ├── idea-pin.md            # Idea pin script (5-10 slides)
│   └── boards.md              # Board suggestions
├── snapchat/
│   ├── story-script.md        # 3-5 frames (10s each)
│   ├── spotlight-script.md    # Up to 60s Spotlight
│   └── ar-concept.md          # AR lens concept
├── facebook/
│   ├── post.md
│   ├── poll.md
│   └── story.md
├── youtube-community/
│   ├── post.md
│   ├── image-concept.md
│   └── poll.md
├── skool/
│   ├── discussion.md
│   ├── challenge.md
│   └── poll.md
├── discord/
│   ├── announcement.md        # Server announcement
│   ├── thread-prompt.md       # Discussion thread starter
│   └── embed.md               # Rich embed message
├── newsletter/
│   ├── newsletter.md          # Newsletter excerpt
│   ├── subject-lines.md
│   └── email-sequence.md
├── reddit/
│   ├── post.md
│   └── subreddits.md
├── quora/
│   ├── answer.md              # 300-1000 word answer
│   ├── space-post.md          # Quora Space post
│   └── questions.md           # Question suggestions
├── medium/
│   ├── article.md             # 1500-3000 word article
│   ├── tags-publications.md   # Tags + publication suggestions
│   └── crosspost-note.md      # Canonical URL handling
├── whatsapp/
│   ├── update.md              # Channel update (100-300 chars)
│   ├── poll.md                # Channel poll
│   └── teaser.md              # Content teaser with link
├── telegram/
│   ├── post.md                # Channel post (500-1000 chars)
│   ├── deep-dive.md           # Formatted deep dive
│   └── poll.md                # Poll with optional quiz mode
├── quotes/
│   ├── quotes.md
│   └── banana-prompts.md
├── seo-metadata.md
├── calendar.md
└── images/                    # AI-generated (with --images)
```

## Platform Intelligence (2026 Data)

Built-in knowledge of each platform's current algorithm and best practices:

| Platform | Key Insight | Source |
|----------|------------|--------|
| Twitter/X | Replies weighted 27x a like; threads get +63% impressions | X Algorithm Analysis 2026 |
| LinkedIn | PDF carousels: 6.60% engagement (highest format); saves = 5x a like | LinkedIn Algorithm Feb 2026 |
| Instagram | Mixed media carousels: 2.33% vs 1.80% image-only; "swipe left" = +10% | Instagram Benchmarks 2026 |
| Facebook | 50% of feed from non-followed accounts; saves + DM shares most powerful | Facebook Algorithm 2026 |
| YouTube | Polls = highest community engagement; 2-4 posts/week optimal | YouTube Community Guide 2026 |
| Skool | 20-30% monthly active = healthy; content rotation required | Skool Best Practices 2026 |

## Image Generation (/banana)

With [Claude Banana](https://github.com/AgriciDaniel/claude-banana) installed, the `--images` flag generates:

- **Quote cards** (5): Minimalist designs with content's best quotes
- **Carousel covers**: Bold title slides for Instagram and LinkedIn
- **Hero images**: Topic-relevant visuals for social posts

Without /banana, prompts are saved to `banana-prompts.md` for manual use.

## Requirements

- Claude Code CLI
- Python 3.10+
- **Optional**: yt-dlp (YouTube transcript extraction)
- **Optional**: Whisper (audio transcription)
- **Optional**: /banana (AI image generation)

## Architecture

- **20 sub-skills** covering every platform
- **6 parallel subagents** for maximum speed
- **8 reference files** with platform specs, hook formulas, voice rules, and benchmarks
- **3 Python scripts** for content extraction (article, transcript, audio)

## Ecosystem

Part of the AgriciDaniel Claude Code skill family:

| Skill | Purpose |
|-------|---------|
| [claude-seo](https://github.com/AgriciDaniel/claude-seo) | SEO analysis (19 skills, 12 agents) |
| [claude-youtube](https://github.com/AgriciDaniel/claude-youtube) | YouTube creator tools |
| [claude-ads](https://github.com/AgriciDaniel/claude-ads) | Ad campaign auditing (186+ checks) |
| [claude-banana](https://github.com/AgriciDaniel/claude-banana) | AI image generation |
| **claude-repurpose** | Content repurposing (this skill) |

## License

MIT

---

## Author

Built by [Agrici Daniel](https://agricidaniel.com/about) - AI Workflow Architect.

- [Blog](https://agricidaniel.com/blog) - Deep dives on AI marketing automation
- [AI Marketing Hub](https://www.skool.com/ai-marketing-hub) - Free community, 2,800+ members
- [YouTube](https://www.youtube.com/@AgriciDaniel) - Tutorials and demos
- [All open-source tools](https://github.com/AgriciDaniel)
