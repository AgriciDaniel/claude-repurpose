#!/usr/bin/env bash
set -euo pipefail

# Claude Repurpose Installer
# Wraps everything in main() to prevent partial execution on network failure

main() {
    SKILL_DIR="${HOME}/.claude/skills/repurpose"
    AGENT_DIR="${HOME}/.claude/agents"
    REPO_URL="https://github.com/AgriciDaniel/claude-repurpose"
    REPO_TAG="${CLAUDE_REPURPOSE_TAG:-v1.0.0}"

    echo "════════════════════════════════════════"
    echo "║  Claude Repurpose - Installer        ║"
    echo "║  Content Repurposing Engine          ║"
    echo "════════════════════════════════════════"
    echo ""

    # Check prerequisites
    command -v python3 >/dev/null 2>&1 || { echo "✗ Python 3 is required but not installed."; exit 1; }
    command -v git >/dev/null 2>&1 || { echo "✗ Git is required but not installed."; exit 1; }

    # Check Python version (3.10+ required)
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PYTHON_OK=$(python3 -c 'import sys; print(1 if sys.version_info >= (3, 10) else 0)')
    if [ "${PYTHON_OK}" = "0" ]; then
        echo "✗ Python 3.10+ is required but ${PYTHON_VERSION} was found."
        exit 1
    fi
    echo "✓ Python ${PYTHON_VERSION} detected"

    # Check optional tools
    if command -v yt-dlp >/dev/null 2>&1; then
        echo "✓ yt-dlp detected (YouTube transcript extraction)"
    else
        echo "⚠ yt-dlp not found. Install for YouTube support: pip install yt-dlp"
    fi

    if command -v whisper >/dev/null 2>&1 || command -v voxtype >/dev/null 2>&1; then
        echo "✓ Audio transcription available"
    else
        echo "⚠ Whisper not found. Audio transcription will require manual transcript input."
    fi

    # Create directories
    mkdir -p "${SKILL_DIR}"
    mkdir -p "${AGENT_DIR}"

    # Clone or update
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf ${TEMP_DIR}" EXIT

    echo "↓ Downloading Claude Repurpose (${REPO_TAG})..."
    git clone --depth 1 --branch "${REPO_TAG}" "${REPO_URL}" "${TEMP_DIR}/claude-repurpose" 2>/dev/null

    # Copy all skills
    echo "→ Installing skill files..."
    if [ -d "${TEMP_DIR}/claude-repurpose/skills" ]; then
        for skill_dir in "${TEMP_DIR}/claude-repurpose/skills"/*/; do
            skill_name=$(basename "${skill_dir}")
            target="${HOME}/.claude/skills/${skill_name}"
            mkdir -p "${target}"
            cp -r "${skill_dir}"* "${target}/"
        done
    fi

    # Copy agents
    echo "→ Installing subagents..."
    cp -r "${TEMP_DIR}/claude-repurpose/agents/"*.md "${AGENT_DIR}/" 2>/dev/null || true

    # Copy scripts
    if [ -d "${TEMP_DIR}/claude-repurpose/scripts" ]; then
        mkdir -p "${SKILL_DIR}/scripts"
        cp -r "${TEMP_DIR}/claude-repurpose/scripts/"* "${SKILL_DIR}/scripts/"
    fi

    # Copy hooks
    if [ -d "${TEMP_DIR}/claude-repurpose/hooks" ]; then
        mkdir -p "${SKILL_DIR}/hooks"
        cp -r "${TEMP_DIR}/claude-repurpose/hooks/"* "${SKILL_DIR}/hooks/"
    fi

    # Copy extensions
    if [ -d "${TEMP_DIR}/claude-repurpose/extensions" ]; then
        for ext_dir in "${TEMP_DIR}/claude-repurpose/extensions"/*/; do
            [ -d "${ext_dir}" ] || continue
            ext_name=$(basename "${ext_dir}")
            mkdir -p "${SKILL_DIR}/extensions/${ext_name}"
            cp -r "${ext_dir}"* "${SKILL_DIR}/extensions/${ext_name}/"
        done
    fi

    # Copy requirements.txt to skill dir
    cp "${TEMP_DIR}/claude-repurpose/requirements.txt" "${SKILL_DIR}/requirements.txt" 2>/dev/null || true

    # Install Python dependencies
    echo "→ Installing Python dependencies..."
    VENV_DIR="${SKILL_DIR}/.venv"
    if python3 -m venv "${VENV_DIR}" 2>/dev/null; then
        "${VENV_DIR}/bin/pip" install --quiet -r "${TEMP_DIR}/claude-repurpose/requirements.txt" 2>/dev/null && \
            echo "  ✓ Installed in venv at ${VENV_DIR}" || \
            echo "  ⚠ Venv pip install failed. Run: ${VENV_DIR}/bin/pip install -r ${SKILL_DIR}/requirements.txt"
    else
        pip install --quiet --user -r "${TEMP_DIR}/claude-repurpose/requirements.txt" 2>/dev/null || \
        echo "  ⚠ Could not auto-install. Run: pip install --user -r ${SKILL_DIR}/requirements.txt"
    fi

    echo ""
    echo "✓ Claude Repurpose installed successfully!"
    echo ""
    echo "Usage:"
    echo "  1. Start Claude Code:  claude"
    echo "  2. Run commands:       /repurpose https://example.com/blog/post"
    echo "  3. YouTube support:    /repurpose https://youtube.com/watch?v=..."
    echo "  4. Quick mode:         /repurpose <url> --brief"
    echo "  5. With images:        /repurpose <url> --images"
    echo ""
    echo "Optional:"
    echo "  - Install yt-dlp for YouTube:  pip install yt-dlp"
    echo "  - Install /banana for images:  See extensions/banana/README.md"
    echo ""
    echo "To uninstall: curl -fsSL ${REPO_URL}/raw/main/uninstall.sh | bash"
}

main "$@"
