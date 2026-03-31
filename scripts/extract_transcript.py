#!/usr/bin/env python3
"""
Extract transcript and metadata from a YouTube video using yt-dlp.

Usage:
    python extract_transcript.py "https://youtube.com/watch?v=VIDEO_ID"
    python extract_transcript.py "https://youtu.be/VIDEO_ID"
    python extract_transcript.py "https://youtube.com/shorts/VIDEO_ID"

Outputs JSON to stdout with: title, description, channel, transcript,
duration_seconds, view_count, publish_date, word_count, error.

Dependencies:
    - yt-dlp (system-installed CLI, NOT a pip package)
    - Python 3.10+ stdlib only (no pip dependencies)

SSRF Protection:
    - URL must match youtube.com or youtu.be patterns
    - No arbitrary URL fetching
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlparse


# Allowed YouTube URL patterns
_YOUTUBE_PATTERNS = [
    re.compile(r"^https?://(www\.)?youtube\.com/watch\?"),
    re.compile(r"^https?://(www\.)?youtube\.com/shorts/"),
    re.compile(r"^https?://youtu\.be/"),
    re.compile(r"^https?://(www\.)?youtube\.com/live/"),
    re.compile(r"^https?://m\.youtube\.com/watch\?"),
]


def _validate_youtube_url(url: str) -> str | None:
    """
    Validate that a URL is a legitimate YouTube video URL.

    Args:
        url: The URL to validate.

    Returns:
        None if valid, error message string if invalid.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return f"Invalid URL scheme: {parsed.scheme}. Only http/https allowed."

    for pattern in _YOUTUBE_PATTERNS:
        if pattern.match(url):
            return None

    return (
        "URL does not match any known YouTube video pattern. "
        "Accepted: youtube.com/watch, youtube.com/shorts, youtu.be, youtube.com/live"
    )


def _check_ytdlp_installed() -> str | None:
    """
    Check that yt-dlp is available on the system PATH.

    Returns:
        None if installed, error message string if not found.
    """
    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return None
        return "yt-dlp returned non-zero exit code. Is it installed correctly?"
    except FileNotFoundError:
        return (
            "yt-dlp is not installed or not in PATH. "
            "Install with: sudo apt install yt-dlp  OR  pip install yt-dlp"
        )
    except subprocess.TimeoutExpired:
        return "yt-dlp --version timed out."


def _extract_metadata(url: str) -> dict | None:
    """
    Extract video metadata using yt-dlp --dump-json.

    Args:
        url: Validated YouTube URL.

    Returns:
        Parsed JSON dict from yt-dlp, or None on failure.
    """
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "--no-download", url],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None


def _extract_subtitles(url: str) -> str | None:
    """
    Extract subtitles from a YouTube video.

    Tries manual (human) subtitles first, then auto-generated.
    Uses JSON3 format for structured parsing.

    Args:
        url: Validated YouTube URL.

    Returns:
        Clean transcript text, or None if no subtitles available.
    """
    with tempfile.TemporaryDirectory(prefix="repurpose_sub_") as tmpdir:
        output_template = os.path.join(tmpdir, "sub")

        # Try to download subtitles (manual + auto, English)
        try:
            result = subprocess.run(
                [
                    "yt-dlp",
                    "--write-sub",
                    "--write-auto-sub",
                    "--sub-lang", "en",
                    "--sub-format", "json3",
                    "--skip-download",
                    "-o", output_template,
                    url,
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None

        # Look for downloaded subtitle files
        # yt-dlp names them: sub.en.json3, sub.en-orig.json3, etc.
        sub_files = []
        for fname in os.listdir(tmpdir):
            if fname.endswith(".json3"):
                sub_files.append(os.path.join(tmpdir, fname))

        if not sub_files:
            # No JSON3 files found; try VTT fallback
            return _extract_subtitles_vtt(url)

        # Prefer manual subs (no "auto" in filename) over auto-generated
        manual = [f for f in sub_files if "auto" not in os.path.basename(f).lower()]
        chosen = manual[0] if manual else sub_files[0]

        return _parse_json3_subtitles(chosen)


def _extract_subtitles_vtt(url: str) -> str | None:
    """
    Fallback: extract subtitles in VTT format if JSON3 is unavailable.

    Args:
        url: Validated YouTube URL.

    Returns:
        Clean transcript text, or None if unavailable.
    """
    with tempfile.TemporaryDirectory(prefix="repurpose_vtt_") as tmpdir:
        output_template = os.path.join(tmpdir, "sub")

        try:
            subprocess.run(
                [
                    "yt-dlp",
                    "--write-sub",
                    "--write-auto-sub",
                    "--sub-lang", "en",
                    "--sub-format", "vtt",
                    "--skip-download",
                    "-o", output_template,
                    url,
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None

        vtt_files = [
            os.path.join(tmpdir, f)
            for f in os.listdir(tmpdir)
            if f.endswith(".vtt")
        ]

        if not vtt_files:
            return None

        manual = [f for f in vtt_files if "auto" not in os.path.basename(f).lower()]
        chosen = manual[0] if manual else vtt_files[0]

        return _parse_vtt_subtitles(chosen)


def _parse_json3_subtitles(filepath: str) -> str | None:
    """
    Parse a JSON3 subtitle file into clean text.

    JSON3 format contains events with segments (segs) that have utf8 text.
    Duplicate/overlapping segments are deduplicated.

    Args:
        filepath: Path to the .json3 subtitle file.

    Returns:
        Cleaned transcript text, or None on parse failure.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    events = data.get("events", [])
    segments = []
    seen_texts = set()

    for event in events:
        segs = event.get("segs", [])
        for seg in segs:
            text = seg.get("utf8", "").strip()
            if text and text != "\n" and text not in seen_texts:
                seen_texts.add(text)
                segments.append(text)

    if not segments:
        return None

    # Join segments and clean up whitespace
    raw = " ".join(segments)
    # Collapse multiple spaces/newlines
    clean = re.sub(r"\s+", " ", raw).strip()
    return clean


def _parse_vtt_subtitles(filepath: str) -> str | None:
    """
    Parse a VTT subtitle file into clean text.

    Strips timestamps, positioning tags, and deduplicates lines.

    Args:
        filepath: Path to the .vtt subtitle file.

    Returns:
        Cleaned transcript text, or None on parse failure.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return None

    lines = content.split("\n")
    text_lines = []
    seen = set()

    for line in lines:
        line = line.strip()
        # Skip headers, timestamps, empty lines, positioning
        if not line:
            continue
        if line.startswith("WEBVTT"):
            continue
        if line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if re.match(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->", line):
            continue
        if re.match(r"^\d+$", line):
            continue
        # Strip HTML-like tags (e.g., <c>, </c>, <b>, etc.)
        clean = re.sub(r"<[^>]+>", "", line).strip()
        if clean and clean not in seen:
            seen.add(clean)
            text_lines.append(clean)

    if not text_lines:
        return None

    raw = " ".join(text_lines)
    clean = re.sub(r"\s+", " ", raw).strip()
    return clean


def extract_transcript(url: str) -> dict:
    """
    Extract transcript and metadata from a YouTube video.

    Args:
        url: YouTube video URL.

    Returns:
        Dictionary with:
            - title: Video title
            - description: Video description
            - channel: Channel name
            - transcript: Full transcript text
            - duration_seconds: Video length in seconds
            - view_count: Number of views
            - publish_date: Upload/publish date (YYYY-MM-DD or YYYYMMDD)
            - word_count: Number of words in transcript
            - error: Error message if extraction failed, else null
    """
    result = {
        "title": None,
        "description": None,
        "channel": None,
        "transcript": None,
        "duration_seconds": 0,
        "view_count": 0,
        "publish_date": None,
        "word_count": 0,
        "error": None,
    }

    # 1. Validate URL
    url_error = _validate_youtube_url(url)
    if url_error:
        result["error"] = url_error
        return result

    # 2. Check yt-dlp is installed
    install_error = _check_ytdlp_installed()
    if install_error:
        result["error"] = install_error
        return result

    # 3. Extract video metadata
    metadata = _extract_metadata(url)
    if metadata is None:
        result["error"] = (
            "Failed to extract video metadata. "
            "The video may be private, unavailable, or region-locked."
        )
        return result

    result["title"] = metadata.get("title")
    result["description"] = metadata.get("description")
    result["channel"] = metadata.get("channel") or metadata.get("uploader")
    result["duration_seconds"] = metadata.get("duration", 0) or 0
    result["view_count"] = metadata.get("view_count", 0) or 0

    # Normalize publish date
    upload_date = metadata.get("upload_date", "")
    if upload_date and len(upload_date) == 8:
        # yt-dlp returns YYYYMMDD, convert to YYYY-MM-DD
        result["publish_date"] = (
            f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
        )
    else:
        result["publish_date"] = upload_date or None

    # 4. Extract subtitles/transcript
    transcript = _extract_subtitles(url)

    if transcript:
        result["transcript"] = transcript
        result["word_count"] = len(transcript.split())
    else:
        # Fallback: use description as partial content
        desc = result["description"] or ""
        if len(desc) > 100:
            result["transcript"] = desc
            result["word_count"] = len(desc.split())
            result["error"] = (
                "No subtitles available (manual or auto-generated). "
                "Falling back to video description as content source. "
                "For best results, provide a manual transcript."
            )
        else:
            result["error"] = (
                "No subtitles available and description is too short for content extraction. "
                "This video may have subtitles disabled. "
                "Consider providing a manual transcript."
            )

    return result


def main():
    """CLI entry point. Accepts a YouTube URL as the first argument."""
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            "Usage: python extract_transcript.py <youtube-url>\n\n"
            "Extract transcript and metadata from a YouTube video.\n"
            "Outputs JSON to stdout.\n\n"
            "Examples:\n"
            '  python extract_transcript.py "https://youtube.com/watch?v=dQw4w9WgXcQ"\n'
            '  python extract_transcript.py "https://youtu.be/dQw4w9WgXcQ"\n'
            '  python extract_transcript.py "https://youtube.com/shorts/ABC123"',
            file=sys.stderr,
        )
        sys.exit(1 if len(sys.argv) < 2 else 0)

    url = sys.argv[1]
    result = extract_transcript(url)

    # JSON output to stdout (machine-readable)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Human-readable summary to stderr
    if result["error"]:
        print(f"\nError: {result['error']}", file=sys.stderr)
    else:
        print(f"\nExtracted: {result['title']}", file=sys.stderr)
        print(f"Channel: {result['channel']}", file=sys.stderr)
        print(f"Duration: {result['duration_seconds']}s", file=sys.stderr)
        print(f"Words: {result['word_count']}", file=sys.stderr)

    # Exit non-zero only on fatal errors (no transcript at all)
    if result["error"] and result["transcript"] is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
