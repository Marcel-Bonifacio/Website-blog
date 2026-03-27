#!/usr/bin/env python3
"""
sync.py — Auto-sync posts from Medium (and Kumparan) into posts.js

Features
--------
• Fetches Medium RSS feed and adds any NEW posts to posts.js
• Refreshes the `image` field for ALL existing Medium posts every run,
  so updating your header image on Medium is reflected automatically.
• Preserves hand-edited fields (featured, tags, custom excerpts) on
  existing posts — only `image` is refreshed automatically.
• Kumparan scraping is attempted opportunistically; failures are silent.

Usage
-----
    python sync.py              # add new posts + refresh images
    python sync.py --dry-run    # print what would change, no file writes
"""

import urllib.request
import xml.etree.ElementTree as ET
import json
import re
import os
import sys
from datetime import datetime
from email.utils import parsedate

# ── Config ────────────────────────────────────────────────────────────────────

MEDIUM_RSS   = "https://medium.com/feed/@marcelbonifaciotirtawijata"
KUMPARAN_URL = "https://kumparan.com/marcel-bonifacio-tirta-wijata"
POSTS_JS     = os.path.join(os.path.dirname(__file__), "posts.js")
DRY_RUN      = "--dry-run" in sys.argv

# RSS namespace used by Medium for media attachments
MEDIA_NS = "http://search.yahoo.com/mrss/"
CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"

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
    """Strip HTML tags and truncate to a readable excerpt."""
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > maxlen:
        text = text[:maxlen].rsplit(" ", 1)[0] + "…"
    return text

def canonical_url(url):
    """Strip query strings and fragments from a URL."""
    return url.split("?")[0].split("#")[0].rstrip("/")

def slug_from_url(url):
    """Derive a stable slug from a URL (strips query strings and trailing Medium hash)."""
    url = canonical_url(url)
    path = url.split("/")[-1]
    path = re.sub(r"-[0-9a-f]{8,}$", "", path)  # strip Medium's trailing hash
    return path or re.sub(r"[^a-z0-9]+", "-", url.lower())

def extract_image(item):
    """
    Pull the best available image URL from a Medium RSS <item>.

    Priority order:
      1. <media:content url="…">  — the actual article header image
      2. <media:thumbnail url="…">
      3. First <img src="…"> found in <content:encoded> HTML
      4. First <img src="…"> found in <description> HTML
    """
    # 1. media:content (most reliable — this IS the header image)
    mc = item.find(f"{{{MEDIA_NS}}}content")
    if mc is not None:
        url = mc.get("url", "")
        if url:
            return url

    # 2. media:thumbnail
    mt = item.find(f"{{{MEDIA_NS}}}thumbnail")
    if mt is not None:
        url = mt.get("url", "")
        if url:
            return url

    # 3 & 4. Scrape first image from HTML body fields
    for tag in [f"{{{CONTENT_NS}}}encoded", "description"]:
        html = item.findtext(tag) or ""
        if html:
            m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html)
            if m:
                return m.group(1)

    return ""

# ── posts.js read / write ─────────────────────────────────────────────────────

def load_existing_ids():
    """Return a set of all post IDs currently in posts.js."""
    try:
        with open(POSTS_JS, "r", encoding="utf-8") as f:
            content = f.read()
        return set(re.findall(r'id:\s*"([^"]+)"', content))
    except FileNotFoundError:
        return set()

def append_new_posts(new_posts):
    """Add new post objects before the closing ]; of the POSTS array."""
    if not new_posts:
        return 0

    with open(POSTS_JS, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    for p in new_posts:
        image_line = ('    image: ' + json.dumps(p.get("image", "")) + ',\n') if p.get("image") else ""
        entry = (
            '  {\n'
            '    id: "' + p["id"] + '",\n'
            '    title: ' + json.dumps(p["title"]) + ',\n'
            '    dateISO: "' + p["dateISO"] + '",\n'
            '    dateDisplay: "' + p["dateDisplay"] + '",\n'
            '    platform: "' + p["platform"] + '",\n'
            '    excerpt: ' + json.dumps(p["excerpt"]) + ',\n'
            '    url: "' + p["url"] + '",\n'
            + image_line +
            '    external: true,\n'
            '    tags: ' + json.dumps(p.get("tags", [])) + ',\n'
            '    featured: false\n'
            '  }'
        )
        entries.append(entry)

    block = "\n\n" + ",\n".join(entries) + "\n];\n"
    # Use a lambda to avoid re treating backslashes in block as escape sequences
    updated = re.sub(r'\n\];\s*$', lambda _: block, content)

    if not DRY_RUN:
        with open(POSTS_JS, "w", encoding="utf-8") as f:
            f.write(updated)

    return len(new_posts)

def refresh_images_in_js(image_map):
    """
    Update the `image` field for existing posts in posts.js.

    image_map: dict of { post_id: image_url }

    For each post in posts.js:
      - If it already has an `image:` line → replace with new URL
      - If it has no `image:` line yet    → insert one after the `url:` line
    """
    if not image_map:
        return 0

    with open(POSTS_JS, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    updated_count = 0

    # We work post-by-post using a regex that captures each object block
    # then replace the image field within it.
    def replace_image_in_block(m):
        nonlocal updated_count
        block = m.group(0)

        # Find this post's id
        id_match = re.search(r'id:\s*"([^"]+)"', block)
        if not id_match:
            return block
        post_id = id_match.group(1)

        if post_id not in image_map:
            return block

        new_image = image_map[post_id]
        new_image_line = '    image: ' + json.dumps(new_image) + ','

        if re.search(r'\bimage:\s*["\']', block):
            # Replace existing image field
            new_block = re.sub(
                r'[ \t]*image:\s*(?:"[^"]*"|\'[^\']*\')[ \t]*,?[ \t]*\n',
                new_image_line + '\n',
                block
            )
        else:
            # Insert image field after the url: line
            new_block = re.sub(
                r'([ \t]*url:\s*"[^"]*",?\n)',
                r'\1' + new_image_line + '\n',
                block
            )

        if new_block != block:
            updated_count += 1
        return new_block

    # Match each { … } object in the array (non-greedy, handles nested braces loosely)
    content = re.sub(r'\{[^{}]+\}', replace_image_in_block, content, flags=re.DOTALL)

    if not DRY_RUN and content != original:
        with open(POSTS_JS, "w", encoding="utf-8") as f:
            f.write(content)

    return updated_count

# ── Sources ───────────────────────────────────────────────────────────────────

def fetch_medium():
    """
    Fetch all posts from Medium RSS.
    Returns list of dicts, each with an `image` field pulled from the feed.
    """
    print("Fetching Medium RSS …")
    posts = []
    try:
        req = urllib.request.Request(MEDIUM_RSS, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()

        root = ET.fromstring(xml_data)
        channel = root.find("channel")
        if channel is None:
            print("  No <channel> element found.")
            return posts

        for item in channel.findall("item"):
            title = (item.findtext("title") or "").strip()
            link  = canonical_url((item.findtext("link") or "").strip())
            pub   = (item.findtext("pubDate") or "").strip()
            desc  = (item.findtext("description") or "").strip()
            if not title or not link:
                continue

            date_iso, date_display = parse_rfc2822(pub)
            image = extract_image(item)

            posts.append({
                "id":          slug_from_url(link),
                "title":       title,
                "dateISO":     date_iso,
                "dateDisplay": date_display,
                "platform":    "Medium",
                "excerpt":     clean_html(desc),
                "url":         link,
                "image":       image,
            })

        print(f"  Found {len(posts)} Medium post(s).")
    except Exception as e:
        print(f"  Medium fetch failed: {e}")
    return posts

def fetch_kumparan():
    """
    Attempt to scrape Kumparan profile for article links.
    Returns empty list silently if the page blocks scraping.
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

        links = re.findall(
            r'href="(https://kumparan\.com/marcel-bonifacio-tirta-wijata/[^"]+)"',
            html
        )
        seen = set()
        for url in links:
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
                "image":       "",
            })
        print(f"  Found {len(posts)} Kumparan post(s).")
    except Exception as e:
        print(f"  Kumparan fetch failed: {e}")
    return posts

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if DRY_RUN:
        print("=== DRY RUN — no files will be changed ===\n")

    existing_ids = load_existing_ids()
    print(f"Existing posts in posts.js: {len(existing_ids)}\n")

    # 1. Fetch all Medium posts (includes image URLs from RSS)
    medium_posts   = fetch_medium()
    kumparan_posts = fetch_kumparan()
    all_fetched    = medium_posts + kumparan_posts

    # 2. Add NEW posts
    new_posts = [p for p in all_fetched if p["id"] not in existing_ids]
    if new_posts:
        added = append_new_posts(new_posts)
        print(f"\nAdded {added} new post(s):")
        for p in new_posts:
            img_tag = " [+image]" if p.get("image") else ""
            print(f"  + [{p['platform']}] {p['title']}{img_tag}")
    else:
        print("\nNo new posts to add.")

    # 3. Refresh images for existing Medium posts
    #    Build a map of { slug → image_url } from RSS data
    image_map = {
        p["id"]: p["image"]
        for p in medium_posts
        if p.get("image")
    }

    print(f"\nRefreshing images for {len(image_map)} Medium post(s) …")
    refreshed = refresh_images_in_js(image_map)
    if refreshed:
        print(f"  Updated image field on {refreshed} post(s).")
    else:
        print("  All images already up to date.")

    print("\nDone. Review posts.js — set featured:true, adjust tags/excerpts as needed.")

if __name__ == "__main__":
    main()
