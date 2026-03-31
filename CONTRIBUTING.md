# Contributing to Claude Repurpose

Thank you for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Follow the development rules in CLAUDE.md
4. Submit a pull request

## Development Rules

- SKILL.md files: under 500 lines
- Reference files: under 200 lines
- Scripts: CLI interface, JSON output, SSRF protection
- Kebab-case naming for directories
- Agents invoked via Agent tool, never Bash

## Adding a New Platform

1. Create `skills/repurpose-<platform>/SKILL.md` with platform specs
2. Add platform to the appropriate agent in `agents/`
3. Update `skills/repurpose/references/platform-specs.md`
4. Update `skills/repurpose/references/engagement-benchmarks.md`
5. Update the main orchestrator routing table

## Reporting Issues

Open an issue on GitHub with:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Claude Code version
