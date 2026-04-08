#!/usr/bin/env python3
"""
Markdown Mirror Generator — Scaling Lab'
Generates clean /index.md mirrors for every HTML page so AI tools
(ChatGPT, Claude, Perplexity) can read each page without fighting HTML chrome.
Usage: python3 generate_mirrors.py
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import markdownify

# ── Config ─────────────────────────────────────────────────────────────
SITE_DIR = Path(__file__).parent
BASE_URL  = "https://lescalinglab.com"

# HTML files to skip (noindex / utility pages)
SKIP_FILES = {"404.html"}

# Tags to strip entirely (including content)
STRIP_TAGS = ["script", "style", "noscript", "iframe", "svg",
              "link", "meta", "head"]

# Tags to strip but keep children
UNWRAP_TAGS = ["nav", "footer", "header"]

# CSS class substrings that mark chrome elements to remove
STRIP_CLASSES = ["nav", "footer", "cta-split", "ghl", "btn-primary",
                 "pill", "calendly", "divider", "fade-up"]

# ── Helpers ─────────────────────────────────────────────────────────────

def should_strip_element(tag):
    """Return True if this element is navigation / chrome that should be removed."""
    if not hasattr(tag, 'get') or tag.attrs is None:
        return False
    classes = tag.get("class", [])
    if isinstance(classes, str):
        classes = [classes]
    for cls in classes:
        for bad in STRIP_CLASSES:
            if bad in cls.lower():
                return True
    # Also strip by id
    el_id = tag.get("id", "")
    for bad in ["nav", "footer", "header", "calendly"]:
        if bad in el_id.lower():
            return True
    return False


def clean_markdown(md: str) -> str:
    """Post-process raw markdown output."""
    # Collapse 3+ blank lines to 2
    md = re.sub(r'\n{3,}', '\n\n', md)
    # Strip standalone step numbers like "01\n" "02\n"
    md = re.sub(r'^\d{2}\s*$', '', md, flags=re.MULTILINE)
    # Remove bullet separator characters
    md = re.sub(r'^[→•▸▶·]\s*$', '', md, flags=re.MULTILINE)
    # Remove empty image references like ![]()
    md = re.sub(r'!\[\]\([^)]*\)', '', md)
    # Remove lines that are just whitespace
    md = re.sub(r'^\s+$', '', md, flags=re.MULTILINE)
    # Final collapse
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()


def html_to_mirror(html_path: Path) -> str | None:
    """Parse an HTML file and return clean markdown with frontmatter."""
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Check noindex
    robots_meta = soup.find("meta", attrs={"name": "robots"})
    if robots_meta:
        content = robots_meta.get("content", "")
        if "noindex" in content.lower():
            print(f"  ⏭  Skipping (noindex): {html_path.name}")
            return None

    # Extract frontmatter fields
    title = ""
    title_tag = soup.find("title")
    if title_tag:
        title = title_tag.get_text(strip=True)

    description = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag:
        description = desc_tag.get("content", "")

    # Build canonical URL
    rel_path = html_path.relative_to(SITE_DIR)
    if rel_path.name == "index.html":
        canonical = BASE_URL + "/"
    else:
        # e.g. resultats.html → /resultats
        canonical = BASE_URL + "/" + rel_path.stem

    # ── Strip chrome from body ──────────────────────────────────────────
    body = soup.find("body")
    if not body:
        body = soup

    # Remove nav / footer / header elements
    for tag_name in UNWRAP_TAGS:
        for el in body.find_all(tag_name):
            el.decompose()

    # Remove by class heuristic
    for el in body.find_all(True):
        if should_strip_element(el):
            el.decompose()

    # Remove script / style / meta / noscript etc.
    for tag_name in STRIP_TAGS:
        for el in body.find_all(tag_name):
            el.decompose()

    # Remove empty div / span wrappers
    changed = True
    while changed:
        changed = False
        for el in body.find_all(["div", "span", "section", "aside"]):
            if not el.get_text(strip=True) and not el.find(True):
                el.decompose()
                changed = True

    # ── Convert to markdown ────────────────────────────────────────────
    body_html = str(body)
    md_raw = markdownify.markdownify(
        body_html,
        heading_style=markdownify.ATX,
        bullets="-",
        strip=["img"],
    )

    md_clean = clean_markdown(md_raw)

    # ── Build frontmatter ──────────────────────────────────────────────
    frontmatter = f"""---
title: {title}
description: {description}
url: {canonical}
source: {html_path.name}
---

"""
    return frontmatter + md_clean


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    print(f"🔍 Scanning: {SITE_DIR}\n")

    html_files = sorted(SITE_DIR.glob("*.html"))
    html_files += sorted(SITE_DIR.rglob("*/index.html"))

    # Deduplicate
    seen = set()
    unique_files = []
    for f in html_files:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)

    generated = []
    for html_path in unique_files:
        if html_path.name in SKIP_FILES:
            print(f"  ⏭  Skipping: {html_path.name}")
            continue

        print(f"  ✦  Processing: {html_path.relative_to(SITE_DIR)}")

        result = html_to_mirror(html_path)
        if result is None:
            continue

        # Output path: same dir, index.md (or stem.md for non-index pages)
        if html_path.name == "index.html":
            out_path = html_path.parent / "index.md"
        else:
            out_path = html_path.parent / (html_path.stem + ".md")

        out_path.write_text(result, encoding="utf-8")
        print(f"      → {out_path.relative_to(SITE_DIR)}")
        generated.append(out_path)

    print(f"\n✅ Generated {len(generated)} markdown mirror(s):")
    for p in generated:
        rel = p.relative_to(SITE_DIR)
        if rel.name == "index.md":
            url = BASE_URL + "/" + str(rel.parent).replace(".", "") + "index.md"
        else:
            url = BASE_URL + "/" + rel.stem + ".md"
        print(f"   {url}")


if __name__ == "__main__":
    main()
