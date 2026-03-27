#!/usr/bin/env python3
"""
new-post.py — Convert a filled post template into a published blog post.

Usage:
    python new-post.py _drafts/my-post-slug.html

What it does:
  1. Reads your draft HTML file from _drafts/
  2. Copies it to posts/<slug>.html (the public location)
  3. Appends an entry to posts.js so the post appears on the site

After running, commit and push to GitHub — the site updates automatically.

Draft file format: see _post-template.html
"""

import os
import re
import sys
import json
import shutil
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(ROOT, "posts")
POSTS_JS  = os.path.join(ROOT, "posts.js")


def extract_meta(html):
    """Extract metadata from <!-- META ... --> comment block."""
    m = re.search(r"<!--\s*META\s*\n(.*?)-->", html, re.DOTALL)
    if not m:
        raise ValueError("No <!-- META --> block found in the draft file.")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip().lower()] = val.strip()
    return meta


def extract_title(html):
    m = re.search(r"<h1[^>]*class=\"post-title\"[^>]*>(.*?)</h1>", html, re.DOTALL)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    m = re.search(r"<title>(.*?)</title>", html)
    if m:
        return m.group(1).strip()
    return "Untitled"


def extract_excerpt(html):
    """Get first <p> from .post-content as excerpt."""
    m = re.search(r'class="post-content"[^>]*>.*?<p>(.*?)</p>', html, re.DOTALL)
    if m:
        text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if len(text) > 260:
            text = text[:260].rsplit(" ", 1)[0] + "…"
        return text
    return ""


def append_to_posts_js(entry):
    with open(POSTS_JS, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for duplicates
    if '"' + entry["id"] + '"' in content:
        print(f"posts.js already contains id \"{entry['id']}\", skipping.")
        return

    tags_json = json.dumps(entry["tags"])
    block = (
        '\n\n  {\n'
        '    id: "' + entry["id"] + '",\n'
        '    title: ' + json.dumps(entry["title"]) + ',\n'
        '    dateISO: "' + entry["dateISO"] + '",\n'
        '    dateDisplay: "' + entry["dateDisplay"] + '",\n'
        '    platform: "Own",\n'
        '    excerpt: ' + json.dumps(entry["excerpt"]) + ',\n'
        '    url: "posts/' + entry["id"] + '.html",\n'
        '    external: false,\n'
        '    tags: ' + tags_json + ',\n'
        '    featured: false\n'
        '  }'
    )

    updated = re.sub(r'\n\];\s*$', block + "\n];\n", content)
    with open(POSTS_JS, "w", encoding="utf-8") as f:
        f.write(updated)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    draft_path = sys.argv[1]
    if not os.path.isabs(draft_path):
        draft_path = os.path.join(ROOT, draft_path)

    if not os.path.exists(draft_path):
        print(f"Error: file not found: {draft_path}")
        sys.exit(1)

    with open(draft_path, "r", encoding="utf-8") as f:
        html = f.read()

    try:
        meta = extract_meta(html)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    slug = meta.get("slug") or os.path.splitext(os.path.basename(draft_path))[0]
    slug = re.sub(r"[^a-z0-9-]", "", slug.lower().replace(" ", "-"))

    date_iso = meta.get("date", datetime.today().strftime("%Y-%m-%d"))
    try:
        dt = datetime.strptime(date_iso, "%Y-%m-%d")
        date_display = dt.strftime("%B %d, %Y")
    except ValueError:
        date_display = date_iso

    title   = meta.get("title") or extract_title(html)
    excerpt = meta.get("excerpt") or extract_excerpt(html)
    tags    = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]

    # Copy to posts/
    os.makedirs(POSTS_DIR, exist_ok=True)
    dest = os.path.join(POSTS_DIR, slug + ".html")
    shutil.copy2(draft_path, dest)
    print(f"Copied → posts/{slug}.html")

    # Add to posts.js
    append_to_posts_js({
        "id":          slug,
        "title":       title,
        "dateISO":     date_iso,
        "dateDisplay": date_display,
        "excerpt":     excerpt,
        "tags":        tags,
    })
    print(f"Added to posts.js: \"{title}\"")
    print()
    print("Next steps:")
    print(f"  1. Review posts/{slug}.html")
    print("  2. Open posts.js and set featured:true if you want it on the homepage")
    print("  3. git add posts.js posts/" + slug + ".html && git commit -m 'post: " + title + "'")
    print("  4. git push  →  site updates on GitHub Pages automatically")


if __name__ == "__main__":
    main()
