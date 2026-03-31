#!/usr/bin/env bash
set -euo pipefail

echo "Uninstalling Claude Repurpose..."

SKILLS=(
    repurpose repurpose-twitter repurpose-linkedin repurpose-instagram
    repurpose-facebook repurpose-youtube repurpose-skool repurpose-newsletter
    repurpose-reddit repurpose-quotes repurpose-seo repurpose-calendar
)

for skill in "${SKILLS[@]}"; do
    rm -rf "${HOME}/.claude/skills/${skill}" 2>/dev/null && \
        echo "  ✓ Removed skill: ${skill}" || true
done

AGENTS=(
    repurpose-social repurpose-visual repurpose-longform
    repurpose-community repurpose-seo
)

for agent in "${AGENTS[@]}"; do
    rm -f "${HOME}/.claude/agents/${agent}.md" 2>/dev/null && \
        echo "  ✓ Removed agent: ${agent}" || true
done

echo ""
echo "✓ Claude Repurpose uninstalled."
