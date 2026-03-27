#!/usr/bin/env python3
"""
sync.py — Auto-sync posts from Medium and Kumparan into posts.js

Run manually:
    python sync.py

Or let GitHub Actions run it daily (see .github/workflows/sync.yml).

The script fetches RSS/Atom feeds from Medium and Kumparan,
compares against existing posts.js entries, and appends new ones.
New posts are inserted AFTER the existing entries so your manual
edits (featured flag, custom excerpts, tags) are never overwritten.
"""

import urllib.request
import xml.etree.ElementTree as ET
import json
import re
import os
from datetime import datetime
from email.utils import parsedate

# ── Config ────────────────────────────────────────────────────────────────────

MEDIUM_RSS   = "https://medium.com/feed/@marcelbonifaciotirtawijata"
KUMPARAN_URL = "https://kumparan.com/marcel-bonifacio-tirta-wijata"  # scraped
POSTS_JS     = os.path.join(os.path.dirname(__file__), "posts.js")

# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_rfc2822(date_str):
    """Parse RFC 2822 date (pubDate in RSS) → (ISO string, display string)."""
    try:
        t = parsedate(date_str)
        dt = datetime(*t[:6])
        return dt.strftime("%Y-%m-%d"), dt.strftime("%B %d, %Y")
    except Exception:
        return "", date_str

def clean_html(text, maxlen=280):
    """Strip HTML tags and truncate."""
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > maxlen:
        text = text[:maxlen].rsplit(" ", 1)[0] + "…"
    return text

def slug_from_url(url):
    """Derive a slug from a URL (strip trailing Medium hash)."""
    path = url.rstrip("/").split("/")[-1]
    path = re.sub(r"-[0-9a-f]{8,}$", "", path)   # strip Medium hash
    return path or re.sub(r"[^a-z0-9]+", "-", url.lower())

def load_existing_ids():
    """Read posts.js and return a set of existing post IDs."""
    try:
        with open(POSTS_JS, "r", encoding="utf-8") as f:
            content = f.read()
        return set(re.findall(r'id:\s*"([^"]+)"', content))
    except FileNotFoundError:
        return set()

def append_posts_to_js(new_posts):
    """Inject new post objects before the closing ]; of POSTS array."""
    if not new_posts:
        return 0

    with open(POSTS_JS, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    for p in new_posts:
        tags_json = json.dumps(p.get("tags", []))
        entry = (
            '  {\n'
            '    id: "' + p["id"] + '",\n'
            '    title: ' + json.dumps(p["title"]) + ',\n'
            '    dateISO: "' + p["dateISO"] + '",\n'
            '    dateDisplay: "' + p["dateDisplay"] + '",\n'
            '    platform: "' + p["platform"] + '",\n'
            '    excerpt: ' + json.dumps(p["excerpt"]) + ',\n'
            '    url: "' + p["url"] + '",\n'
            '    external: true,\n'
            '    tags: ' + tags_json + ',\n'
            '    featured: false\n'
            '  }'
        )
        entries.append(entry)

    block = "\n\n" + ",\n".join(entries)
    # Insert before the closing ];
    updated = re.sub(r'\n\];\s*$', block + "\n];\n", content)

    with open(POSTS_JS, "w", encoding="utf-8") as f:
        f.write(updated)

    return len(new_posts)

# ── Sources ───────────────────────────────────────────────────────────────────

def fetch_medium():
    """Fetch posts from Medium RSS feed."""
    print("Fetching Medium RSS …")
    posts = []
    try:
        req = urllib.request.Request(MEDIUM_RSS, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()
        root = ET.fromstring(xml_data)
        channel = root.find("channel")
        if channel is None:
            return posts
        for item in channel.findall("item"):
            title = (item.findtext("title") or "").strip()
            link  = (item.findtext("link") or "").strip()
            pub   = (item.findtext("pubDate") or "").strip()
            desc  = (item.findtext("description") or "").strip()
            if not title or not link:
                continue
            date_iso, date_display = parse_rfc2822(pub)
            posts.append({
                "id":          slug_from_url(link),
                "title":       title,
                "dateISO":     date_iso,
                "dateDisplay": date_display,
                "platform":    "Medium",
                "excerpt":     clean_html(desc),
                "url":         link,
            })
        print(f"  Found {len(posts)} Medium post(s).")
    except Exception as e:
        print(f"  Medium fetch failed: {e}")
    return posts

def fetch_kumparan():
    """
    Attempt to scrape Kumparan profile for article links.
    Kumparan does not publish a standard RSS feed; this parser
    looks for Open Graph / JSON-LD article entries in the HTML.
    It may return nothing if the page blocks scraping — that's OK.
    """
    print("Fetching Kumparan profile …")
    posts = []
    try:
        req = urllib.request.Request(
            KUMPARAN_URL,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        # Look for article URLs in the page source
        links = re.findall(
            r'href="(https://kumparan\.com/marcel-bonifacio-tirta-wijata/[^"]+)"',
            html
        )
        seen = set()
        for url in links:
            # Skip profile/tag pages, keep article links
            if url.count("/") < 5:
                continue
            if url in seen:
                continue
            seen.add(url)
            slug = slug_from_url(url)
            posts.append({
                "id":          slug,
                "title":       slug.replace("-", " ").title(),
                "dateISO":     "",
                "dateDisplay": "",
                "platform":    "Kumparan",
                "excerpt":     "Read the full article on Kumparan.",
                "url":         url,
            })
        print(f"  Found {len(posts)} Kumparan post(s).")
    except Exception as e:
        print(f"  Kumparan fetch failed: {e}")
    return posts

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    existing_ids = load_existing_ids()
    print(f"Existing posts: {len(existing_ids)}")

    candidates = fetch_medium() + fetch_kumparan()
    new_posts = [p for p in candidates if p["id"] not in existing_ids]

    if not new_posts:
        print("No new posts found.")
        return

    added = append_posts_to_js(new_posts)
    print(f"Added {added} new post(s) to posts.js")
    for p in new_posts:
        print(f"  + [{p['platform']}] {p['title']}")
    print()
    print("Review posts.js — set featured:true, fix titles/excerpts/tags as needed.")

if __name__ == "__main__":
    main()
