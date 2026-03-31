#!/usr/bin/env python3
"""
Transcribe audio files to text using available system tools.

Usage:
    python transcribe_audio.py "/path/to/audio.mp3"
    python transcribe_audio.py recording.wav --model large-v3-turbo

Checks for transcription tools in order: whisper CLI, voxtype, faster-whisper.
Outputs JSON to stdout with: text, duration_seconds, language, segments,
tool_used, error.

Dependencies:
    - Python 3.10+ stdlib only (no pip dependencies)
    - One of: openai-whisper, whisper.cpp, faster-whisper (system-installed)
    - Optional: ffprobe (for duration detection)

SSRF Protection:
    - Accepts only local file paths, never URLs
    - Path validated to be a real file on disk
"""

import json
import os
import re
import subprocess
import sys
import tempfile


# Supported audio file extensions
_SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm", ".wma", ".aac"}


def _validate_file(filepath: str) -> str | None:
    """
    Validate that the file exists and has a supported audio extension.

    Args:
        filepath: Path to the audio file.

    Returns:
        None if valid, error message string if invalid.
    """
    if not os.path.isfile(filepath):
        return f"File not found: {filepath}"

    ext = os.path.splitext(filepath)[1].lower()
    if ext not in _SUPPORTED_EXTENSIONS:
        return (
            f"Unsupported file extension: {ext}. "
            f"Supported: {', '.join(sorted(_SUPPORTED_EXTENSIONS))}"
        )

    return None


def _check_tool(command: list[str], timeout: int = 10) -> bool:
    """
    Check if a CLI tool is available by running a test command.

    Args:
        command: Command and args to test (e.g., ["whisper", "--help"]).
        timeout: Timeout in seconds.

    Returns:
        True if the command succeeds, False otherwise.
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def _detect_tool() -> str | None:
    """
    Detect which transcription tool is available on the system.

    Checks in priority order: whisper, voxtype, faster-whisper.

    Returns:
        Tool name string ("whisper", "voxtype", "faster-whisper"), or None.
    """
    # 1. OpenAI Whisper or whisper.cpp
    if _check_tool(["whisper", "--help"]):
        return "whisper"

    # 2. voxtype (user's GPU-accelerated tool)
    if _check_tool(["voxtype", "status"]):
        return "voxtype"

    # 3. faster-whisper CLI
    if _check_tool(["faster-whisper", "--help"]):
        return "faster-whisper"

    return None


def _get_duration_ffprobe(filepath: str) -> float | None:
    """
    Get audio duration in seconds using ffprobe.

    Args:
        filepath: Path to the audio file.

    Returns:
        Duration in seconds, or None if ffprobe is unavailable.
    """
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                filepath,
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0 and result.stdout.strip():
            return float(result.stdout.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        pass
    return None


def _estimate_duration_from_size(filepath: str) -> float:
    """
    Rough duration estimate from file size (fallback when ffprobe unavailable).

    Uses average bitrate assumptions:
    - MP3: ~128 kbps
    - WAV: ~1411 kbps (CD quality)
    - M4A/AAC: ~128 kbps
    - OGG: ~112 kbps
    - FLAC: ~900 kbps

    Args:
        filepath: Path to the audio file.

    Returns:
        Estimated duration in seconds.
    """
    size_bytes = os.path.getsize(filepath)
    ext = os.path.splitext(filepath)[1].lower()

    # Bitrates in bits per second
    bitrate_map = {
        ".mp3": 128_000,
        ".wav": 1_411_000,
        ".m4a": 128_000,
        ".aac": 128_000,
        ".ogg": 112_000,
        ".flac": 900_000,
        ".webm": 128_000,
        ".wma": 128_000,
    }

    bitrate = bitrate_map.get(ext, 128_000)
    return (size_bytes * 8) / bitrate


def _transcribe_whisper(filepath: str, model: str) -> dict:
    """
    Transcribe using the OpenAI Whisper CLI (or whisper.cpp).

    Args:
        filepath: Path to the audio file.
        model: Whisper model name (e.g., "large-v3", "large-v3-turbo", "medium").

    Returns:
        Dict with text, language, and segments.
    """
    result = {
        "text": None,
        "language": None,
        "segments": [],
        "error": None,
    }

    with tempfile.TemporaryDirectory(prefix="repurpose_whisper_") as tmpdir:
        try:
            proc = subprocess.run(
                [
                    "whisper",
                    filepath,
                    "--model", model,
                    "--output_format", "json",
                    "--output_dir", tmpdir,
                ],
                capture_output=True,
                text=True,
                timeout=600,  # 10 minutes for long audio
            )
        except subprocess.TimeoutExpired:
            result["error"] = "Whisper transcription timed out (10 minute limit)."
            return result
        except FileNotFoundError:
            result["error"] = "Whisper CLI not found."
            return result

        if proc.returncode != 0:
            stderr = proc.stderr.strip()
            result["error"] = f"Whisper failed (exit {proc.returncode}): {stderr[:500]}"
            return result

        # Find the output JSON file
        json_files = [f for f in os.listdir(tmpdir) if f.endswith(".json")]
        if not json_files:
            # Whisper may have written to stdout instead
            result["text"] = proc.stdout.strip() if proc.stdout.strip() else None
            if not result["text"]:
                result["error"] = "Whisper produced no output."
            return result

        json_path = os.path.join(tmpdir, json_files[0])
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            result["error"] = f"Failed to parse Whisper output: {e}"
            return result

        result["text"] = data.get("text", "").strip()
        result["language"] = data.get("language")

        # Extract segments if available
        for seg in data.get("segments", []):
            result["segments"].append({
                "start": seg.get("start", 0),
                "end": seg.get("end", 0),
                "text": seg.get("text", "").strip(),
            })

    return result


def _transcribe_faster_whisper(filepath: str, model: str) -> dict:
    """
    Transcribe using the faster-whisper CLI.

    Args:
        filepath: Path to the audio file.
        model: Whisper model name.

    Returns:
        Dict with text, language, and segments.
    """
    result = {
        "text": None,
        "language": None,
        "segments": [],
        "error": None,
    }

    try:
        proc = subprocess.run(
            [
                "faster-whisper",
                filepath,
                "--model", model,
                "--output_format", "json",
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )
    except subprocess.TimeoutExpired:
        result["error"] = "faster-whisper transcription timed out (10 minute limit)."
        return result
    except FileNotFoundError:
        result["error"] = "faster-whisper CLI not found."
        return result

    if proc.returncode != 0:
        stderr = proc.stderr.strip()
        result["error"] = f"faster-whisper failed (exit {proc.returncode}): {stderr[:500]}"
        return result

    # Try to parse JSON output from stdout
    try:
        data = json.loads(proc.stdout)
        result["text"] = data.get("text", "").strip()
        result["language"] = data.get("language")
        for seg in data.get("segments", []):
            result["segments"].append({
                "start": seg.get("start", 0),
                "end": seg.get("end", 0),
                "text": seg.get("text", "").strip(),
            })
    except json.JSONDecodeError:
        # Plain text output fallback
        text = proc.stdout.strip()
        if text:
            result["text"] = text
        else:
            result["error"] = "faster-whisper produced no parseable output."

    return result


def transcribe_audio(filepath: str, model: str = "large-v3-turbo") -> dict:
    """
    Transcribe an audio file using the best available system tool.

    Args:
        filepath: Path to the audio file.
        model: Whisper model name (default: large-v3-turbo for GPU systems).

    Returns:
        Dictionary with:
            - text: Full transcription text
            - duration_seconds: Audio duration in seconds
            - language: Detected language code
            - segments: List of {start, end, text} dicts
            - tool_used: Name of the transcription tool used
            - error: Error message if transcription failed, else null
    """
    result = {
        "text": None,
        "duration_seconds": 0,
        "language": "en",
        "segments": [],
        "tool_used": None,
        "error": None,
    }

    # 1. Validate file
    filepath = os.path.abspath(filepath)
    file_error = _validate_file(filepath)
    if file_error:
        result["error"] = file_error
        return result

    # 2. Get duration
    duration = _get_duration_ffprobe(filepath)
    if duration is None:
        duration = _estimate_duration_from_size(filepath)
    result["duration_seconds"] = round(duration, 2)

    # 3. Detect available tool
    tool = _detect_tool()

    if tool is None:
        result["error"] = (
            "No transcription tool found. Install one of:\n"
            "  1. pip install openai-whisper    (OpenAI Whisper, requires CUDA for speed)\n"
            "  2. pip install faster-whisper     (CTranslate2 backend, faster on GPU)\n"
            "  3. Build whisper.cpp from source  (CPU-optimized C++ implementation)\n\n"
            "Alternatively, paste the transcript manually when prompted."
        )
        return result

    result["tool_used"] = tool

    # 4. Transcribe with the detected tool
    if tool == "whisper":
        transcription = _transcribe_whisper(filepath, model)
    elif tool == "voxtype":
        # voxtype is a live-mic tool, not designed for file transcription.
        # Recommend whisper instead, but note it as the detected tool.
        result["error"] = (
            "voxtype detected but it is a live-microphone tool (Super+H), "
            "not suitable for file transcription. "
            "Install openai-whisper for file transcription:\n"
            "  pip install openai-whisper\n\n"
            "Alternatively, paste the transcript manually when prompted."
        )
        result["tool_used"] = "voxtype (unsupported for files)"
        return result
    elif tool == "faster-whisper":
        transcription = _transcribe_faster_whisper(filepath, model)
    else:
        result["error"] = f"Unknown tool: {tool}"
        return result

    # 5. Merge transcription results
    if transcription["error"]:
        result["error"] = transcription["error"]
        # Still include partial results if available
        if transcription["text"]:
            result["text"] = transcription["text"]

    if transcription["text"]:
        result["text"] = transcription["text"]
    if transcription["language"]:
        result["language"] = transcription["language"]
    if transcription["segments"]:
        result["segments"] = transcription["segments"]

    # Calculate word count for logging
    if result["text"] and not result["error"]:
        word_count = len(result["text"].split())
        # Log but don't add to output schema (transcript word_count
        # is computed by the caller from the text field)
        pass

    return result


def main():
    """CLI entry point. Accepts a file path as the first argument."""
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            "Usage: python transcribe_audio.py <audio-file> [--model MODEL]\n\n"
            "Transcribe an audio file using the best available tool.\n"
            "Outputs JSON to stdout.\n\n"
            f"Supported formats: {', '.join(sorted(_SUPPORTED_EXTENSIONS))}\n\n"
            "Options:\n"
            "  --model MODEL    Whisper model name (default: large-v3-turbo)\n"
            "                   Options: tiny, base, small, medium, large-v3,\n"
            "                   large-v3-turbo\n\n"
            "Examples:\n"
            '  python transcribe_audio.py recording.mp3\n'
            '  python transcribe_audio.py podcast.wav --model medium\n'
            '  python transcribe_audio.py "/path/to/audio.m4a" --model large-v3',
            file=sys.stderr,
        )
        sys.exit(1 if len(sys.argv) < 2 else 0)

    # Parse arguments (minimal, no argparse to keep stdlib-only)
    filepath = sys.argv[1]
    model = "large-v3-turbo"

    # Check for --model flag
    if "--model" in sys.argv:
        model_idx = sys.argv.index("--model")
        if model_idx + 1 < len(sys.argv):
            model = sys.argv[model_idx + 1]
        else:
            print("Error: --model requires a value.", file=sys.stderr)
            sys.exit(1)

    result = transcribe_audio(filepath, model=model)

    # JSON output to stdout (machine-readable)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Human-readable summary to stderr
    if result["error"]:
        print(f"\nError: {result['error']}", file=sys.stderr)
    else:
        word_count = len(result["text"].split()) if result["text"] else 0
        print(f"\nTranscribed: {os.path.basename(filepath)}", file=sys.stderr)
        print(f"Tool: {result['tool_used']}", file=sys.stderr)
        print(f"Duration: {result['duration_seconds']}s", file=sys.stderr)
        print(f"Language: {result['language']}", file=sys.stderr)
        print(f"Words: {word_count}", file=sys.stderr)
        print(f"Segments: {len(result['segments'])}", file=sys.stderr)

    # Exit non-zero on fatal error (no text at all)
    if result["error"] and result["text"] is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
