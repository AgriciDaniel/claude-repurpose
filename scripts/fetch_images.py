#!/usr/bin/env python3
"""
fetch_images.py - Stock photo search helper + website image extractor.

Generates optimized search queries for stock platforms, filters article images
by relevance, verifies image URLs, and returns structured JSON for Claude to use
during the content repurposing pipeline.

Usage:
    python3 fetch_images.py --topic "WordPress AI automation" [--count 5]
    python3 fetch_images.py --topic "AI tools" --article-images '{"images": [...]}'

Output: JSON to stdout with stock_queries, website_images, platform_dimensions.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SKIP_PATTERNS = re.compile(
    r"logo|icon|avatar|favicon|sprite|banner-ad|advertisement|"
    r"tracking|pixel|spacer|badge|button|widget",
    re.IGNORECASE,
)

SIZE_PATTERN = re.compile(r"(\d{2,4})x(\d{2,4})")
THUMB_PATTERN = re.compile(r"thumbnail|thumb|_s\.|_xs\.|_sm\.", re.IGNORECASE)
SVG_PATTERN = re.compile(r"\.svg(\?|$)", re.IGNORECASE)

PLATFORM_DIMENSIONS = {
    "twitter": {"width": 1600, "height": 900, "label": "1600x900"},
    "linkedin": {"width": 1080, "height": 1350, "label": "1080x1350"},
    "instagram": {"width": 1080, "height": 1350, "label": "1080x1350"},
    "facebook": {"width": 1080, "height": 1350, "label": "1080x1350"},
    "youtube": {"width": 1080, "height": 1080, "label": "1080x1080"},
    "newsletter": {"width": 1200, "height": 630, "label": "1200x630"},
}

MIN_IMAGE_WIDTH = 400


# ---------------------------------------------------------------------------
# Search query generation
# ---------------------------------------------------------------------------

def generate_stock_queries(topic: str, count: int = 5) -> dict[str, str]:
    """Generate platform-specific search queries for stock photo sites.

    Args:
        topic: The content topic to search for.
        count: Desired number of images (used to hint query breadth).

    Returns:
        Dict mapping platform name to a full search query string.
    """
    # Clean up topic for search: strip excess whitespace
    clean_topic = " ".join(topic.split())

    queries = {
        "pixabay": f"site:pixabay.com {clean_topic} wide banner high quality",
        "unsplash": f"site:unsplash.com {clean_topic} professional",
        "pexels": f"site:pexels.com {clean_topic} high resolution",
    }

    # For larger counts, add broader variant queries
    if count > 5:
        queries["pixabay_alt"] = f"site:pixabay.com {clean_topic} technology modern"
        queries["unsplash_alt"] = f"site:unsplash.com {clean_topic} editorial"

    return queries


# ---------------------------------------------------------------------------
# Article image filtering
# ---------------------------------------------------------------------------

def _is_skippable(url: str, alt: str) -> bool:
    """Check if an image should be skipped based on URL or alt text."""
    combined = f"{url} {alt}"
    if SKIP_PATTERNS.search(combined):
        return True
    if SVG_PATTERN.search(url):
        return True
    return False


def _looks_small(url: str) -> bool:
    """Heuristic: check if the URL contains size hints suggesting < 400px."""
    if THUMB_PATTERN.search(url):
        return True

    match = SIZE_PATTERN.search(url)
    if match:
        w, h = int(match.group(1)), int(match.group(2))
        if max(w, h) < MIN_IMAGE_WIDTH:
            return True

    return False


def _relevance_score(alt: str, topic: str) -> float:
    """Score 0.0-1.0 based on keyword overlap between alt text and topic."""
    if not alt or not topic:
        return 0.1  # Minimal score for images with no alt text

    topic_words = set(topic.lower().split())
    alt_words = set(alt.lower().split())

    # Remove very common stopwords
    stopwords = {"the", "a", "an", "in", "on", "at", "to", "for", "of", "and", "or", "is", "with"}
    topic_words -= stopwords
    alt_words -= stopwords

    if not topic_words:
        return 0.1

    overlap = topic_words & alt_words
    score = len(overlap) / len(topic_words)

    # Bonus for longer, more descriptive alt text (likely a real image)
    if len(alt) > 40:
        score = min(1.0, score + 0.1)

    return round(max(0.05, score), 2)


def filter_article_images(
    images_json: str | list[dict[str, Any]], topic: str, count: int = 5
) -> list[dict[str, Any]]:
    """Filter and rank images extracted from an article by relevance.

    Args:
        images_json: JSON string or list of dicts with 'src' and 'alt' keys.
        topic: The content topic for relevance scoring.
        count: Maximum number of images to return.

    Returns:
        List of dicts with url, alt, relevance_score — sorted by score desc.
    """
    if isinstance(images_json, str):
        try:
            images = json.loads(images_json)
        except json.JSONDecodeError:
            return []
    else:
        images = images_json

    # Handle both {"images": [...]} wrapper and raw list
    if isinstance(images, dict) and "images" in images:
        images = images["images"]

    if not isinstance(images, list):
        return []

    results = []
    seen_urls = set()

    for img in images:
        if not isinstance(img, dict):
            continue

        url = img.get("src", img.get("url", "")).strip()
        alt = img.get("alt", "").strip()

        if not url:
            continue

        # Deduplicate
        if url in seen_urls:
            continue
        seen_urls.add(url)

        # Skip unwanted images
        if _is_skippable(url, alt):
            continue

        # Skip small images
        if _looks_small(url):
            continue

        score = _relevance_score(alt, topic)
        results.append({
            "url": url,
            "alt": alt,
            "relevance_score": score,
        })

    # Sort by relevance descending
    results.sort(key=lambda x: x["relevance_score"], reverse=True)

    return results[:count]


# ---------------------------------------------------------------------------
# URL verification
# ---------------------------------------------------------------------------

def verify_url(url: str, timeout: int = 10) -> dict[str, Any]:
    """Send a HEAD request to verify an image URL is accessible.

    Args:
        url: The image URL to check.
        timeout: Request timeout in seconds.

    Returns:
        Dict with url, status, content_type, size.
    """
    result = {
        "url": url,
        "status": None,
        "content_type": None,
        "size": None,
    }

    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "Mozilla/5.0 (compatible; ContentRepurposer/1.0)")

        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result["status"] = resp.status
            result["content_type"] = resp.headers.get("Content-Type")
            content_length = resp.headers.get("Content-Length")
            if content_length:
                result["size"] = int(content_length)
    except urllib.error.HTTPError as e:
        result["status"] = e.code
    except (urllib.error.URLError, OSError, ValueError):
        result["status"] = 0  # Network error / invalid URL

    return result


# ---------------------------------------------------------------------------
# Platform URL builder
# ---------------------------------------------------------------------------

def build_platform_urls(base_url: str, platform: str | None = None) -> dict[str, str]:
    """Build platform-optimized URLs for Unsplash images.

    For Unsplash URLs, appends resize/crop parameters per platform.
    For non-Unsplash URLs, returns the original URL for each platform.

    Args:
        base_url: The source image URL.
        platform: Specific platform name, or None for all platforms.

    Returns:
        Dict mapping platform names to optimized URLs.
    """
    resize_params = {
        "twitter": "?w=1600&h=900&fit=crop&q=80",
        "linkedin": "?w=1080&h=1350&fit=crop&q=80",
        "instagram": "?w=1080&h=1350&fit=crop&q=80",
        "facebook": "?w=1080&h=1350&fit=crop&q=80",
        "youtube": "?w=1080&h=1080&fit=crop&q=80",
        "newsletter": "?w=1200&h=630&fit=crop&q=80",
    }

    is_unsplash = "images.unsplash.com" in base_url

    # Strip existing query params from Unsplash URLs to avoid duplication
    if is_unsplash and "?" in base_url:
        clean_url = base_url.split("?")[0]
    else:
        clean_url = base_url

    platforms = {platform: resize_params[platform]} if platform else resize_params
    result = {}

    for plat, params in platforms.items():
        if is_unsplash:
            result[plat] = f"{clean_url}{params}"
        else:
            result[plat] = base_url

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stock photo search helper and website image extractor.",
        epilog="Outputs structured JSON to stdout for Claude to consume.",
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="Content topic for generating search queries and scoring relevance.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of images to target (default: 5).",
    )
    parser.add_argument(
        "--article-images",
        dest="article_images",
        default=None,
        help='JSON string of images from extract_article.py (e.g. \'{"images": [...]}\')',
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Run HEAD requests to verify filtered image URLs.",
    )

    args = parser.parse_args()

    output: dict[str, Any] = {
        "stock_queries": {},
        "website_images": [],
        "platform_dimensions": {},
        "error": None,
    }

    try:
        # 1. Generate stock search queries
        output["stock_queries"] = generate_stock_queries(args.topic, args.count)

        # 2. Filter article images if provided
        if args.article_images:
            filtered = filter_article_images(args.article_images, args.topic, args.count)

            # Optionally verify URLs
            if args.verify and filtered:
                for img in filtered:
                    verification = verify_url(img["url"])
                    img["verified"] = verification["status"] == 200
                    img["content_type"] = verification["content_type"]
                    img["size"] = verification["size"]

            output["website_images"] = filtered

        # 3. Platform dimensions
        output["platform_dimensions"] = {
            name: dims["label"] for name, dims in PLATFORM_DIMENSIONS.items()
        }

    except Exception as e:
        output["error"] = str(e)

    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
