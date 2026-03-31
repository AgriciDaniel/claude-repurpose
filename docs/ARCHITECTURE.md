# Architecture

## Overview

claude-repurpose follows the Agent Skills open standard with a 3-layer architecture:

1. **Directive Layer** (SKILL.md files) - Rules, routing, platform specs
2. **Orchestration Layer** (agents/) - Parallel subagent execution
3. **Execution Layer** (scripts/) - Python content extraction

## Component Flow

```
User: /repurpose <input>
         │
         ▼
┌─────────────────────────┐
│  repurpose/SKILL.md     │  Directive Layer
│  (Main Orchestrator)    │  Detects input type, atomizes content,
│                         │  spawns agents, collects outputs
└────────┬────────────────┘
         │
         ├── scripts/extract_transcript.py   ← YouTube URLs
         ├── scripts/extract_article.py      ← Blog URLs
         └── scripts/transcribe_audio.py     ← Audio files
         │
         ▼
┌─────────────────────────────────────────────┐
│  5 Parallel Subagents (Orchestration Layer) │
│                                             │
│  repurpose-social    ──→ twitter/SKILL.md   │
│                          linkedin/SKILL.md  │
│                          facebook/SKILL.md  │
│                                             │
│  repurpose-visual    ──→ instagram/SKILL.md │
│                          quotes/SKILL.md    │
│                                             │
│  repurpose-longform  ──→ newsletter/SKILL.md│
│                          reddit/SKILL.md    │
│                                             │
│  repurpose-community ──→ youtube/SKILL.md   │
│                          skool/SKILL.md     │
│                                             │
│  repurpose-seo       ──→ seo/SKILL.md      │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Output Directory       │  ./repurposed/<timestamp>/
│  30+ platform files     │  Organized by platform
│  + calendar + summary   │
└─────────────────────────┘
```

## Skill Delegation

The main orchestrator ROUTES, it does not IMPLEMENT. Each sub-skill contains:

- Platform-specific character limits, image dimensions, algorithm rules
- Output file format and structure
- Voice adaptation rules for that platform
- References to load on-demand

## Reference System

8 reference files loaded ON-DEMAND (never all at startup):

| File | When Loaded |
|------|------------|
| platform-specs.md | Always (core spec data) |
| hook-formulas.md | When generating hooks/openers |
| voice-adaptation.md | When --voice flag set or for tone adaptation |
| repurposing-frameworks.md | During content atomization |
| poll-strategy.md | When generating polls |
| image-sourcing.md | When sourcing images (stock, website, AI) |
| mistakes-to-avoid.md | Quality check pass |
| engagement-benchmarks.md | Calendar generation + quality check |

## Extension System

Optional add-ons that enhance but aren't required:

- **banana/** - AI image generation via Gemini (/banana skill)
  - Detection: checks for `gemini_generate_image` MCP tool
  - Fallback: saves prompts to `banana-prompts.md` for manual use

## Security

- SSRF protection in all URL-fetching scripts (blocks private IPs, loopback, metadata endpoints)
- No credentials stored in repo
- URL validation before any external request
- Output directory is local (no remote write)
