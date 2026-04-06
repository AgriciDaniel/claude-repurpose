# Claude Repurpose: Content Repurposing Engine

## Project Overview

Standalone Claude Code skill that transforms any content (YouTube videos, blog posts,
podcasts, local files) into 10+ platform-optimized outputs. Follows the Agent Skills
open standard and the 3-layer architecture (directive, orchestration, execution).
20 sub-skills, 6 parallel subagents, 8 reference files, and 3 Python scripts.

## Architecture

```
claude-repurpose/
  .claude-plugin/plugin.json       # Plugin manifest
  skills/
    repurpose/                     # Main orchestrator
      SKILL.md                     # Entry point, routing table, core rules
      references/                  # 8 on-demand knowledge files
    repurpose-twitter/SKILL.md     # Twitter/X (threads, tweets, polls)
    repurpose-linkedin/SKILL.md    # LinkedIn (posts, PDF carousels, polls)
    repurpose-instagram/SKILL.md   # Instagram (carousels, captions, reels)
    repurpose-tiktok/SKILL.md      # TikTok (video scripts, carousels, stitch/duet)
    repurpose-threads/SKILL.md     # Threads (threads, standalone posts, image posts)
    repurpose-pinterest/SKILL.md   # Pinterest (pins, idea pins, boards)
    repurpose-snapchat/SKILL.md    # Snapchat (stories, Spotlight, AR concepts)
    repurpose-facebook/SKILL.md    # Facebook (posts, polls, stories)
    repurpose-youtube/SKILL.md     # YouTube Community (posts, polls)
    repurpose-skool/SKILL.md       # Skool (discussions, challenges, polls)
    repurpose-newsletter/SKILL.md  # Newsletter + email sequences
    repurpose-discord/SKILL.md     # Discord (announcements, threads, embeds)
    repurpose-reddit/SKILL.md      # Reddit (discussion posts)
    repurpose-quora/SKILL.md       # Quora (answers, Space posts, questions)
    repurpose-medium/SKILL.md      # Medium (articles, tags, publications)
    repurpose-whatsapp/SKILL.md    # WhatsApp (channel updates, polls, teasers)
    repurpose-telegram/SKILL.md    # Telegram (channel posts, deep dives, polls)
    repurpose-quotes/SKILL.md      # Quote graphics + /banana prompts
    repurpose-seo/SKILL.md         # Cross-platform SEO metadata
    repurpose-calendar/SKILL.md    # 7-day publishing calendar
  agents/                          # 5 parallel subagents
    repurpose-social.md            # Twitter + Threads + LinkedIn + Facebook
    repurpose-visual.md            # Instagram + TikTok + Pinterest + Snapchat + Quotes
    repurpose-longform.md          # Newsletter + Email + Reddit + Quora
    repurpose-community.md         # YouTube Community + Skool + Discord
    repurpose-seo.md               # SEO metadata across all
    repurpose-broadcast.md         # WhatsApp + Telegram + Medium
  scripts/
    extract_transcript.py          # YouTube -> transcript (yt-dlp)
    extract_article.py             # URL -> clean text (bs4)
    transcribe_audio.py            # Audio -> text (whisper/voxtype)
  hooks/hooks.json                 # PostToolUse validation
  extensions/banana/               # /banana image gen helper
```

## Commands

| Command | Purpose |
|---------|---------|
| `/repurpose <url-or-file>` | Full repurposing to all platforms |
| `/repurpose <url> --platforms twitter,linkedin` | Specific platforms only |
| `/repurpose <url> --voice casual\|professional\|witty` | Override brand voice |
| `/repurpose <url> --brief` | Quick mode: top 3 platforms |
| `/repurpose <url> --images` | Generate images via /banana |
| `/repurpose analyze <url>` | Content atomization only (no outputs) |
| `/repurpose calendar` | Generate 7-day publishing calendar |

## Development Rules

- Keep SKILL.md files under 500 lines
- Reference files under 200 lines
- Scripts: CLI interface, JSON output, SSRF protection
- Kebab-case naming for all directories
- Agents invoked via Agent tool, never via Bash
- Python deps install into `~/.claude/skills/repurpose/.venv/`

## Security Rules

- No hardcoded credentials or secrets
- URL validation in all scripts (block private IPs, loopback)
- No user credentials in output files
- Use `os.path.dirname(os.path.abspath(__file__))` for paths

## Key Principles

1. **Progressive Disclosure**: Metadata loaded, instructions on activation, references on demand
2. **Content Detection**: Auto-detect YouTube, blog URL, local file, audio, pasted text
3. **Parallel Execution**: 5 subagents run simultaneously for maximum speed
4. **Platform-Native**: Never cross-post verbatim; adapt message, tone, format per platform
5. **/banana Integration**: Image generation is ENFORCED by default when /banana is available — quote cards, carousel covers, hero images generate automatically (no flag needed). Prompts always saved as fallback.
6. **Mandatory Outputs**: Every run MUST produce `all-content.md` (single consolidated file) and `index.html` (dark-themed viewer with Copy buttons). Run `scripts/generate_html.py` as final step.

## Ecosystem

Part of the Claude Code skill family:
- [Claude SEO](https://github.com/AgriciDaniel/claude-seo) -- SEO analysis suite
- [Claude YouTube](https://github.com/AgriciDaniel/claude-youtube) -- YouTube creator tools
- [Claude Ads](https://github.com/AgriciDaniel/claude-ads) -- Ad campaign auditing
- [Claude Banana](https://github.com/AgriciDaniel/claude-banana) -- AI image generation
