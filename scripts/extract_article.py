#!/usr/bin/env python3
"""
Extract article content and metadata from a blog or news URL.

Usage:
    python extract_article.py "https://example.com/blog/post-title"
    python extract_article.py "https://example.com/article" --raw

Outputs JSON to stdout with: title, author, date, text, word_count,
images, url, error.

Dependencies:
    - requests (from requirements.txt)
    - beautifulsoup4 (from requirements.txt)
    - lxml (from requirements.txt, optional fast parser)

SSRF Protection:
    - URL scheme must be http or https
    - Resolved IP checked against private/reserved ranges
    - Blocks: 10.x, 172.16-31.x, 192.168.x, 127.x, 169.254.x, fd00::/8, ::1
    - Blocks cloud metadata endpoints (169.254.169.254)
"""

import argparse
import ipaddress
import json
import re
import socket
import sys
from typing import Optional
from urllib.parse import urljoin, urlparse

try:
    import requests
except ImportError:
    print(
        "Error: requests library required. Install with: pip install requests",
        file=sys.stderr,
    )
    sys.exit(1)

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    print(
        "Error: beautifulsoup4 required. Install with: pip install beautifulsoup4",
        file=sys.stderr,
    )
    sys.exit(1)

try:
    import lxml  # noqa: F401
    _HTML_PARSER = "lxml"
except ImportError:
    _HTML_PARSER = "html.parser"


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 ClaudeRepurpose/1.0"
)

DEFAULT_HEADERS = {
    "User-Agent": DEFAULT_USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

# Tags to strip from content extraction
_STRIP_TAGS = {
    "nav", "header", "footer", "sidebar", "aside",
    "script", "style", "noscript", "iframe", "form",
    "svg", "button", "input", "select", "textarea",
}

# CSS class/id patterns that indicate content areas
_CONTENT_PATTERNS = re.compile(
    r"(content|post|article|entry|blog|story|text|body)",
    re.IGNORECASE,
)

# CSS class/id patterns that indicate non-content areas
_NOISE_PATTERNS = re.compile(
    r"(comment|sidebar|widget|footer|header|nav|menu|"
    r"breadcrumb|pagination|share|social|related|"
    r"advertisement|ad-|advert|promo|popup|modal|"
    r"cookie|consent|newsletter|signup|subscribe)",
    re.IGNORECASE,
)


def _validate_url(url: str) -> str | None:
    """
    Validate that a URL is safe to fetch.

    Checks scheme and prevents SSRF by resolving the hostname
    and blocking private/reserved IP ranges.

    Args:
        url: The URL to validate.

    Returns:
        None if valid, error message string if blocked.
    """
    parsed = urlparse(url)

    # Scheme check
    if parsed.scheme not in ("http", "https"):
        return f"Invalid URL scheme: {parsed.scheme}. Only http/https allowed."

    if not parsed.hostname:
        return "URL has no hostname."

    # Block obvious metadata endpoints
    if parsed.hostname == "169.254.169.254":
        return "Blocked: cloud metadata endpoint."

    # DNS resolution + private IP check
    try:
        addr_infos = socket.getaddrinfo(
            parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80),
            proto=socket.IPPROTO_TCP,
        )
    except socket.gaierror:
        return f"DNS resolution failed for: {parsed.hostname}"

    for family, _type, _proto, _canonname, sockaddr in addr_infos:
        ip_str = sockaddr[0]
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            continue

        if ip.is_private:
            return f"Blocked: URL resolves to private IP ({ip_str})."
        if ip.is_loopback:
            return f"Blocked: URL resolves to loopback ({ip_str})."
        if ip.is_reserved:
            return f"Blocked: URL resolves to reserved IP ({ip_str})."
        if ip.is_link_local:
            return f"Blocked: URL resolves to link-local IP ({ip_str})."
        # Explicit metadata IP check (IPv4-mapped IPv6)
        if ip_str in ("169.254.169.254", "::ffff:169.254.169.254"):
            return "Blocked: cloud metadata endpoint."

    return None


def _fetch_page(url: str, timeout: int = 15, max_redirects: int = 5) -> tuple[str | None, str | None, str]:
    """
    Fetch a web page with proper headers and redirect handling.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.
        max_redirects: Maximum redirect hops.

    Returns:
        Tuple of (html_content, error_message, final_url).
    """
    try:
        session = requests.Session()
        session.max_redirects = max_redirects

        response = session.get(
            url,
            headers=DEFAULT_HEADERS,
            timeout=timeout,
            allow_redirects=True,
        )
        response.raise_for_status()

        # Check content type
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type and "application/xhtml" not in content_type:
            return None, f"Non-HTML content type: {content_type}", response.url

        return response.text, None, response.url

    except requests.exceptions.Timeout:
        return None, f"Request timed out after {timeout} seconds.", url
    except requests.exceptions.TooManyRedirects:
        return None, f"Too many redirects (max {max_redirects}).", url
    except requests.exceptions.SSLError as e:
        return None, f"SSL error: {e}", url
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        if status == 403:
            return None, "Access denied (403). The site may block automated requests.", url
        if status == 404:
            return None, "Page not found (404).", url
        if status == 451:
            return None, "Unavailable for legal reasons (451).", url
        return None, f"HTTP error {status}: {e}", url
    except requests.exceptions.ConnectionError as e:
        return None, f"Connection error: {e}", url
    except requests.exceptions.RequestException as e:
        return None, f"Request failed: {e}", url


def _extract_title(soup: BeautifulSoup) -> str | None:
    """
    Extract the article title using multiple strategies.

    Priority: h1 > og:title > <title> tag.
    """
    # Strategy 1: First h1 inside article/main
    for container in soup.find_all(["article", "main", "[role='main']"]):
        h1 = container.find("h1")
        if h1:
            return h1.get_text(strip=True)

    # Strategy 2: Any h1 on the page
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)

    # Strategy 3: Open Graph title
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        return og_title["content"].strip()

    # Strategy 4: <title> tag (often includes site name, less ideal)
    title_tag = soup.find("title")
    if title_tag:
        return title_tag.get_text(strip=True)

    return None


def _extract_author(soup: BeautifulSoup) -> str | None:
    """
    Extract the author name using multiple strategies.

    Priority: meta author > rel=author > schema.org > byline class patterns.
    """
    # Strategy 1: <meta name="author">
    meta_author = soup.find("meta", attrs={"name": "author"})
    if meta_author and meta_author.get("content"):
        return meta_author["content"].strip()

    # Strategy 2: <a rel="author"> or <span rel="author">
    rel_author = soup.find(attrs={"rel": "author"})
    if rel_author:
        return rel_author.get_text(strip=True)

    # Strategy 3: Schema.org JSON-LD author
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            # Handle both single object and @graph arrays
            items = [data] if isinstance(data, dict) else data if isinstance(data, list) else []
            if isinstance(data, dict) and "@graph" in data:
                items = data["@graph"]
            for item in items:
                if not isinstance(item, dict):
                    continue
                author = item.get("author")
                if isinstance(author, dict):
                    name = author.get("name")
                    if name:
                        return name.strip()
                elif isinstance(author, str):
                    return author.strip()
                elif isinstance(author, list) and author:
                    first = author[0]
                    if isinstance(first, dict) and first.get("name"):
                        return first["name"].strip()
                    elif isinstance(first, str):
                        return first.strip()
        except (json.JSONDecodeError, TypeError, AttributeError):
            continue

    # Strategy 4: Byline class/id patterns
    byline_patterns = re.compile(
        r"(byline|author|writer|contributor|by-line|post-author)",
        re.IGNORECASE,
    )
    for el in soup.find_all(class_=byline_patterns):
        text = el.get_text(strip=True)
        if text and len(text) < 100:
            # Strip common prefixes
            text = re.sub(r"^(by|written by|author:)\s*", "", text, flags=re.IGNORECASE).strip()
            if text:
                return text

    return None


def _extract_date(soup: BeautifulSoup) -> str | None:
    """
    Extract the publication date using multiple strategies.

    Priority: article:published_time > <time> > schema datePublished > meta date.
    """
    # Strategy 1: Open Graph published time
    og_date = soup.find("meta", property="article:published_time")
    if og_date and og_date.get("content"):
        return og_date["content"].strip()

    # Strategy 2: <time datetime="..."> element
    time_el = soup.find("time", attrs={"datetime": True})
    if time_el:
        return time_el["datetime"].strip()

    # Strategy 3: Schema.org datePublished
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            items = [data] if isinstance(data, dict) else data if isinstance(data, list) else []
            if isinstance(data, dict) and "@graph" in data:
                items = data["@graph"]
            for item in items:
                if isinstance(item, dict):
                    dp = item.get("datePublished")
                    if dp:
                        return str(dp).strip()
        except (json.JSONDecodeError, TypeError):
            continue

    # Strategy 4: <meta name="date"> or similar
    for name_attr in ("date", "publish_date", "article:published"):
        meta = soup.find("meta", attrs={"name": name_attr})
        if meta and meta.get("content"):
            return meta["content"].strip()

    return None


def _find_content_element(soup: BeautifulSoup) -> Optional[Tag]:
    """
    Find the main content element of the page.

    Uses a priority-based approach to locate the article body.

    Returns:
        BeautifulSoup Tag containing the main content, or None.
    """
    # Strategy 1: <article> tag
    article = soup.find("article")
    if article and len(article.get_text(strip=True)) > 200:
        return article

    # Strategy 2: [role="main"]
    main_role = soup.find(attrs={"role": "main"})
    if main_role and len(main_role.get_text(strip=True)) > 200:
        return main_role

    # Strategy 3: Elements with content-related class/id
    candidates = []
    for el in soup.find_all(["div", "section"]):
        classes = " ".join(el.get("class", []))
        el_id = el.get("id", "")
        combined = f"{classes} {el_id}"

        if _CONTENT_PATTERNS.search(combined) and not _NOISE_PATTERNS.search(combined):
            text_len = len(el.get_text(strip=True))
            if text_len > 200:
                candidates.append((text_len, el))

    if candidates:
        # Return the largest matching element
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    # Strategy 4: <main> tag
    main_tag = soup.find("main")
    if main_tag and len(main_tag.get_text(strip=True)) > 100:
        return main_tag

    # Strategy 5: Fallback - largest text block in body
    body = soup.find("body")
    if body:
        largest = None
        largest_len = 0
        for el in body.find_all(["div", "section"]):
            text_len = len(el.get_text(strip=True))
            if text_len > largest_len:
                largest_len = text_len
                largest = el
        if largest and largest_len > 100:
            return largest

    return None


def _strip_noise(element: Tag) -> None:
    """
    Remove non-content elements from a content container (in-place).

    Strips navigation, footers, sidebars, scripts, ads, etc.
    """
    # Remove unwanted tags entirely
    for tag_name in _STRIP_TAGS:
        for tag in element.find_all(tag_name):
            tag.decompose()

    # Remove elements with noisy class/id patterns
    for el in element.find_all(True):
        classes = " ".join(el.get("class", []))
        el_id = el.get("id", "")
        combined = f"{classes} {el_id}"
        if _NOISE_PATTERNS.search(combined):
            el.decompose()


def _extract_images(element: Tag, base_url: str) -> list[dict]:
    """
    Extract all images from the content element.

    Args:
        element: Content container Tag.
        base_url: Base URL for resolving relative image paths.

    Returns:
        List of dicts with 'src' and 'alt' keys.
    """
    images = []
    seen_srcs = set()

    for img in element.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src") or ""
        src = src.strip()

        if not src or src.startswith("data:"):
            continue

        # Resolve relative URLs
        if base_url:
            src = urljoin(base_url, src)

        # Deduplicate
        if src in seen_srcs:
            continue
        seen_srcs.add(src)

        alt = (img.get("alt") or "").strip()
        images.append({"src": src, "alt": alt})

    return images


def _clean_text(element: Tag) -> str:
    """
    Extract and clean visible text from a content element.

    Normalizes whitespace, removes empty lines, decodes HTML entities.
    BeautifulSoup handles entity decoding automatically.

    Args:
        element: Content container Tag.

    Returns:
        Cleaned article text.
    """
    # Get text with newlines between block elements
    text = element.get_text(separator="\n", strip=True)

    # Normalize whitespace within lines
    lines = []
    for line in text.split("\n"):
        cleaned = re.sub(r"[ \t]+", " ", line).strip()
        if cleaned:
            lines.append(cleaned)

    # Join with single newlines, then collapse triple+ newlines to double
    result = "\n".join(lines)
    result = re.sub(r"\n{3,}", "\n\n", result)

    return result.strip()


def extract_article(url: str) -> dict:
    """
    Extract article content and metadata from a web URL.

    Args:
        url: The article URL to extract from.

    Returns:
        Dictionary with:
            - title: Article title
            - author: Author name
            - date: Publication date
            - text: Clean article text
            - word_count: Number of words in the article
            - images: List of {src, alt} dicts
            - url: Final URL (after redirects)
            - error: Error message if extraction failed, else null
    """
    result = {
        "title": None,
        "author": None,
        "date": None,
        "text": None,
        "word_count": 0,
        "images": [],
        "url": url,
        "error": None,
    }

    # 1. Validate URL (SSRF protection)
    url_error = _validate_url(url)
    if url_error:
        result["error"] = url_error
        return result

    # 2. Fetch the page
    html, fetch_error, final_url = _fetch_page(url)
    result["url"] = final_url

    if fetch_error:
        result["error"] = fetch_error
        return result

    if not html:
        result["error"] = "Empty response body."
        return result

    # 3. Parse with BeautifulSoup
    soup = BeautifulSoup(html, _HTML_PARSER)

    # 4. Extract metadata
    result["title"] = _extract_title(soup)
    result["author"] = _extract_author(soup)
    result["date"] = _extract_date(soup)

    # 5. Find and extract main content
    content_el = _find_content_element(soup)

    if content_el is None:
        # Last resort: try the whole body
        content_el = soup.find("body")
        if content_el is None:
            result["error"] = (
                "Could not locate article content. "
                "The page may be JavaScript-rendered (SPA) or have non-standard markup."
            )
            return result

    # 6. Extract images before stripping noise
    result["images"] = _extract_images(content_el, final_url)

    # 7. Strip noise elements
    _strip_noise(content_el)

    # 8. Extract clean text
    text = _clean_text(content_el)

    if not text or len(text) < 50:
        result["error"] = (
            "Extracted content is too short (< 50 characters). "
            "The page may require JavaScript rendering, be behind a paywall, "
            "or use non-standard content markup."
        )
        # Still include whatever we got
        if text:
            result["text"] = text
            result["word_count"] = len(text.split())
        return result

    result["text"] = text
    result["word_count"] = len(text.split())

    return result


def main():
    """CLI entry point. Accepts a URL as a positional argument."""
    parser = argparse.ArgumentParser(
        description="Extract article content and metadata from a URL."
    )
    parser.add_argument("url", help="Article URL to extract")
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Include raw text without paragraph breaks (single-line output)",
    )

    args = parser.parse_args()

    result = extract_article(args.url)

    # Optionally flatten text to single line
    if args.raw and result["text"]:
        result["text"] = re.sub(r"\n+", " ", result["text"]).strip()

    # JSON output to stdout (machine-readable)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Human-readable summary to stderr
    if result["error"]:
        print(f"\nError: {result['error']}", file=sys.stderr)
    else:
        print(f"\nExtracted: {result['title']}", file=sys.stderr)
        if result["author"]:
            print(f"Author: {result['author']}", file=sys.stderr)
        if result["date"]:
            print(f"Date: {result['date']}", file=sys.stderr)
        print(f"Words: {result['word_count']}", file=sys.stderr)
        print(f"Images: {len(result['images'])}", file=sys.stderr)

    # Exit non-zero on fatal error (no text at all)
    if result["error"] and result["text"] is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
