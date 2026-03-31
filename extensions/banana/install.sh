#!/usr/bin/env bash
set -euo pipefail

# Claude Repurpose - Banana Extension Installer
# Installs the /banana skill for AI image generation (quote cards, carousel covers, hero images)

echo "════════════════════════════════════════"
echo "║  Banana Extension for Repurpose     ║"
echo "║  AI Image Generation via Gemini     ║"
echo "════════════════════════════════════════"
echo ""

BANANA_SKILL="${HOME}/.claude/skills/banana/SKILL.md"

if [ -f "${BANANA_SKILL}" ]; then
    echo "✓ /banana skill already installed at ${BANANA_SKILL}"
    echo ""
    echo "The repurpose skill will automatically detect /banana and use it"
    echo "when you run: /repurpose <url> --images"
    exit 0
fi

echo "The /banana skill is not installed."
echo ""
echo "To install /banana for AI image generation:"
echo ""
echo "  Option 1 (recommended):"
echo "    git clone https://github.com/AgriciDaniel/claude-banana.git"
echo "    cd claude-banana && bash install.sh"
echo ""
echo "  Option 2 (one-liner):"
echo "    curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-banana/main/install.sh | bash"
echo ""
echo "After installing, the repurpose skill will automatically generate"
echo "quote cards, carousel covers, and hero images when you use --images."
echo ""
echo "Without /banana, the skill saves image prompts to banana-prompts.md"
echo "for manual generation later."
