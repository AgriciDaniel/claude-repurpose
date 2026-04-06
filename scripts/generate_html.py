#!/usr/bin/env python3
"""
Generate a single HTML viewer and consolidated markdown from repurposed content.

Usage:
    python generate_html.py <repurposed-dir>
    python generate_html.py ./repurposed/2026-03-31_203526

Generates:
  - index.html: Dark-themed viewer with tabs per platform, Copy buttons
  - all-content.md: Single consolidated markdown with all platform outputs

All user content is sanitized via escape_html() before insertion.

Dependencies: None (stdlib only)
"""

import json
import os
import re
import sys
from pathlib import Path


def escape_html(text: str) -> str:
    """Escape HTML special characters to prevent XSS."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def md_to_html(md: str) -> str:
    """Convert markdown to basic HTML without external dependencies."""
    lines = md.split("\n")
    html_lines = []
    in_code = False
    in_list = False
    in_table = False
    th_done = False

    for line in lines:
        s = line.strip()

        if s.startswith("```"):
            if in_code:
                html_lines.append("</code></pre>")
                in_code = False
            else:
                lang = s[3:].strip()
                cls = f' class="language-{escape_html(lang)}"' if lang else ""
                html_lines.append(f"<pre><code{cls}>")
                in_code = True
            continue
        if in_code:
            html_lines.append(escape_html(line))
            continue

        if "|" in s and s.startswith("|"):
            cells = [c.strip() for c in s.split("|")[1:-1]]
            if all(re.match(r"^[-:]+$", c) for c in cells):
                th_done = True
                continue
            if not in_table:
                html_lines.append('<table class="ct">')
                in_table = True
            tag = "th" if not th_done else "td"
            row = "".join(f"<{tag}>{escape_html(c)}</{tag}>" for c in cells)
            html_lines.append(f"<tr>{row}</tr>")
            continue
        elif in_table:
            html_lines.append("</table>")
            in_table = False
            th_done = False

        if in_list and not s.startswith("- ") and not s.startswith("* "):
            html_lines.append("</ul>")
            in_list = False

        if s.startswith("#### "):
            html_lines.append(f"<h4>{escape_html(s[5:])}</h4>")
        elif s.startswith("### "):
            html_lines.append(f"<h3>{escape_html(s[4:])}</h3>")
        elif s.startswith("## "):
            html_lines.append(f"<h2>{escape_html(s[3:])}</h2>")
        elif s.startswith("# "):
            html_lines.append(f"<h1>{escape_html(s[2:])}</h1>")
        elif s in ("---", "***", "___"):
            html_lines.append("<hr>")
        elif s.startswith("- ") or s.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            c = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s[2:])
            html_lines.append(f"<li>{c}</li>")
        elif not s:
            html_lines.append("")
        else:
            t = escape_html(s)
            t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
            t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
            t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
            t = re.sub(
                r"\[(.+?)\]\((.+?)\)",
                r'<a href="\2" target="_blank" rel="noopener">\1</a>',
                t,
            )
            html_lines.append(f"<p>{t}</p>")

    if in_list:
        html_lines.append("</ul>")
    if in_table:
        html_lines.append("</table>")
    if in_code:
        html_lines.append("</code></pre>")
    return "\n".join(html_lines)


PLATFORMS = {
    "twitter": {"icon": "&#120143;", "name": "Twitter / X", "color": "#1da1f2"},
    "linkedin": {"icon": "in", "name": "LinkedIn", "color": "#0a66c2"},
    "instagram": {"icon": "IG", "name": "Instagram", "color": "#e1306c"},
    "facebook": {"icon": "f", "name": "Facebook", "color": "#1877f2"},
    "youtube-community": {"icon": "YT", "name": "YouTube", "color": "#ff0000"},
    "skool": {"icon": "S", "name": "Skool", "color": "#5865f2"},
    "newsletter": {"icon": "@", "name": "Newsletter", "color": "#10b981"},
    "tiktok": {"icon": "TT", "name": "TikTok", "color": "#00f2ea"},
    "reddit": {"icon": "R", "name": "Reddit", "color": "#ff4500"},
    "quora": {"icon": "Qa", "name": "Quora", "color": "#b92b27"},
    "quotes": {"icon": "Q", "name": "Quotes", "color": "#a855f7"},
}
META_FILES = ["atoms.md", "seo-metadata.md", "calendar.md", "summary.md"]


def collect(d: Path) -> dict:
    content = {"meta": [], "platforms": {}}
    for m in META_FILES:
        p = d / m
        if p.exists():
            content["meta"].append({"name": m.replace(".md", "").replace("-", " ").title(), "file": m, "text": p.read_text()})
    for pd in sorted(d.iterdir()):
        if pd.is_dir() and pd.name != "images":
            files = []
            for f in sorted(pd.glob("*.md")):
                files.append({"name": f.stem.replace("-", " ").title(), "file": f"{pd.name}/{f.name}", "text": f.read_text()})
            if files:
                content["platforms"][pd.name] = files
    return content


def build_consolidated_md(content: dict, source_title: str) -> str:
    """Build a single consolidated markdown file."""
    parts = [f"# {source_title} - Repurposed Content\n"]
    parts.append(f"*Generated by [claude-repurpose](https://github.com/AgriciDaniel/claude-repurpose)*\n")
    parts.append("---\n")

    for item in content["meta"]:
        parts.append(f"\n## {item['name']}\n")
        parts.append(item["text"])
        parts.append("\n---\n")

    for platform, files in content["platforms"].items():
        cfg = PLATFORMS.get(platform, {"name": platform.title()})
        parts.append(f"\n# {cfg['name']}\n")
        for item in files:
            parts.append(f"\n## {item['name']}\n")
            parts.append(item["text"])
            parts.append("\n---\n")

    return "\n".join(parts)


def build_html(d: Path) -> str:
    content = collect(d)

    total = len(content["meta"])
    for fs in content["platforms"].values():
        total += len(fs)

    source_title = "Repurposed Content"
    for item in content["meta"]:
        if "atoms" in item["file"].lower():
            for line in item["text"].split("\n"):
                if line.startswith("**Source**:"):
                    source_title = line.replace("**Source**:", "").strip()
                    break

    # Build tabs + panels
    tabs = '<button class="tab active" data-tab="meta">Overview</button>\n'
    panels = '<div class="tp active" id="p-meta">\n'
    for item in content["meta"]:
        esc = escape_html(item["text"]).replace("\n", "\\n").replace("'", "\\'")
        panels += f'<div class="card"><div class="ch"><h3>{escape_html(item["name"])}</h3>'
        panels += f"<button class=\"cb\" onclick=\"cc(this,'{esc}')\">Copy</button>"
        panels += f'</div><div class="cb2">{md_to_html(item["text"])}</div></div>\n'
    panels += "</div>\n"

    for plat, files in content["platforms"].items():
        cfg = PLATFORMS.get(plat, {"icon": "?", "name": plat.title(), "color": "#6b7280"})
        tabs += f'<button class="tab" data-tab="{plat}" style="--tc:{cfg["color"]}">'
        tabs += f'{cfg["icon"]} {cfg["name"]} <span class="cnt">{len(files)}</span></button>\n'

        panels += f'<div class="tp" id="p-{plat}">\n'
        for item in files:
            esc = escape_html(item["text"]).replace("\n", "\\n").replace("'", "\\'")
            panels += f'<div class="card"><div class="ch"><h3>{escape_html(item["name"])}</h3>'
            panels += f"<button class=\"cb\" onclick=\"cc(this,'{esc}')\">Copy</button>"
            panels += f'</div><div class="cb2">{md_to_html(item["text"])}</div></div>\n'
        panels += "</div>\n"

    # Check images
    img_dir = d / "images"
    if img_dir.exists():
        imgs = list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.webp"))
        if imgs:
            tabs += f'<button class="tab" data-tab="images" style="--tc:#a855f7">Images <span class="cnt">{len(imgs)}</span></button>\n'
            panels += '<div class="tp" id="p-images"><div class="ig">\n'
            for img in sorted(imgs):
                rel = img.relative_to(d)
                panels += f'<div class="ic"><img src="{rel}" alt="{escape_html(img.stem)}" loading="lazy"><p>{escape_html(img.stem)}</p></div>\n'
            panels += "</div></div>\n"

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Repurposed: {escape_html(source_title)}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;background:#0f1117;color:#e1e4e8;line-height:1.6}}.ctn{{max-width:1200px;margin:0 auto;padding:20px}}
header{{text-align:center;padding:40px 20px 30px;border-bottom:1px solid #21262d;margin-bottom:30px}}header h1{{font-size:1.8rem;color:#f0f6fc;margin-bottom:8px}}header p{{color:#8b949e;font-size:.95rem}}
.sts{{display:flex;gap:20px;justify-content:center;margin-top:15px;flex-wrap:wrap}}.st{{background:#161b22;border:1px solid #21262d;border-radius:8px;padding:8px 16px;font-size:.85rem}}.st strong{{color:#58a6ff}}
.tabs{{display:flex;gap:6px;overflow-x:auto;padding-bottom:10px;margin-bottom:20px;border-bottom:1px solid #21262d;flex-wrap:wrap}}
.tab{{background:#161b22;border:1px solid #21262d;border-radius:8px 8px 0 0;padding:8px 16px;color:#8b949e;cursor:pointer;font-size:.85rem;white-space:nowrap;transition:all .2s;display:flex;align-items:center;gap:6px}}
.tab:hover{{background:#1c2128;color:#e1e4e8}}.tab.active{{background:#1c2128;color:#f0f6fc;border-bottom-color:#1c2128;border-top:2px solid var(--tc,#58a6ff)}}
.cnt{{background:#21262d;border-radius:10px;padding:1px 7px;font-size:.75rem}}.tp{{display:none}}.tp.active{{display:block}}
.card{{background:#161b22;border:1px solid #21262d;border-radius:10px;margin-bottom:16px;overflow:hidden}}
.ch{{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;background:#1c2128;border-bottom:1px solid #21262d}}.ch h3{{font-size:1rem;color:#f0f6fc}}
.cb{{background:#238636;color:#fff;border:none;border-radius:6px;padding:6px 14px;cursor:pointer;font-size:.8rem;transition:all .2s}}.cb:hover{{background:#2ea043}}.cb.ok{{background:#1f6feb}}
.cb2{{padding:18px;font-size:.9rem}}.cb2 h1{{font-size:1.3rem;color:#f0f6fc;margin:16px 0 8px}}.cb2 h2{{font-size:1.15rem;color:#f0f6fc;margin:14px 0 8px}}.cb2 h3{{font-size:1rem;color:#c9d1d9;margin:12px 0 6px}}.cb2 h4{{font-size:.9rem;color:#c9d1d9;margin:10px 0 4px}}
.cb2 p{{margin:8px 0;color:#c9d1d9}}.cb2 ul{{margin:8px 0 8px 20px}}.cb2 li{{margin:4px 0;color:#c9d1d9}}.cb2 strong{{color:#f0f6fc}}.cb2 em{{color:#8b949e}}
.cb2 code{{background:#0d1117;padding:2px 6px;border-radius:4px;font-size:.85em;color:#79c0ff}}.cb2 pre{{background:#0d1117;border-radius:6px;padding:14px;overflow-x:auto;margin:10px 0}}.cb2 pre code{{background:none;padding:0}}
.cb2 hr{{border:none;border-top:1px solid #21262d;margin:16px 0}}.cb2 a{{color:#58a6ff;text-decoration:none}}.cb2 a:hover{{text-decoration:underline}}
.ct{{width:100%;border-collapse:collapse;margin:10px 0}}.ct th,.ct td{{padding:8px 12px;border:1px solid #21262d;text-align:left;font-size:.85rem}}.ct th{{background:#1c2128;color:#f0f6fc}}
.ig{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}}.ic{{background:#161b22;border:1px solid #21262d;border-radius:10px;overflow:hidden}}.ic img{{width:100%;height:auto;display:block}}.ic p{{padding:10px;text-align:center;font-size:.85rem;color:#8b949e}}
footer{{text-align:center;padding:30px;color:#484f58;font-size:.8rem;margin-top:30px;border-top:1px solid #21262d}}
@media(max-width:768px){{.tabs{{gap:4px}}.tab{{padding:6px 10px;font-size:.8rem}}.ch{{flex-direction:column;gap:8px;align-items:flex-start}}}}
</style></head><body>
<div class="ctn">
<header><h1>{escape_html(source_title)}</h1><p>Generated by claude-repurpose</p>
<div class="sts"><div class="st"><strong>{len(content["platforms"])}</strong> platforms</div><div class="st"><strong>{total}</strong> content pieces</div></div></header>
<div class="tabs">{tabs}</div>
<div>{panels}</div>
<footer>Generated by <a href="https://github.com/AgriciDaniel/claude-repurpose" style="color:#58a6ff">claude-repurpose</a></footer>
</div>
<script>
document.querySelectorAll('.tab').forEach(t=>{{t.addEventListener('click',()=>{{document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.querySelectorAll('.tp').forEach(x=>x.classList.remove('active'));t.classList.add('active');document.getElementById('p-'+t.dataset.tab).classList.add('active')}});}});
function cc(b,t){{t=t.replace(/\\\\n/g,'\\n');navigator.clipboard.writeText(t).then(()=>{{var o=b.textContent;b.textContent='Copied!';b.classList.add('ok');setTimeout(()=>{{b.textContent=o;b.classList.remove('ok')}},2000)}})}}
</script></body></html>"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_html.py <repurposed-dir>", file=sys.stderr)
        sys.exit(1)

    d = Path(sys.argv[1])
    if not d.is_dir():
        print(json.dumps({"error": f"Not found: {d}"}))
        sys.exit(1)

    content = collect(d)

    # Get source title
    source_title = "Repurposed Content"
    for item in content["meta"]:
        if "atoms" in item["file"].lower():
            for line in item["text"].split("\n"):
                if line.startswith("**Source**:"):
                    source_title = line.replace("**Source**:", "").strip()
                    break

    # Generate HTML
    html = build_html(d)
    html_path = d / "index.html"
    html_path.write_text(html)

    # Generate consolidated markdown
    md = build_consolidated_md(content, source_title)
    md_path = d / "all-content.md"
    md_path.write_text(md)

    fc = sum(1 for _ in d.rglob("*.md"))
    print(json.dumps({"html": str(html_path), "markdown": str(md_path), "files_processed": fc, "error": None}))
    print(f"Generated: {html_path}", file=sys.stderr)
    print(f"Generated: {md_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
