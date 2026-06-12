# Design Guide

## Philosophy
Editorial with warmth. Content first, navy as the foundation, depth from typography, whitespace, soft gradient washes, and tinted surfaces. The site should read like a well-set publication with a clear identity, not a template.

---

## Typography
Two self-hosted variable fonts (latin subsets, `assets/fonts/`, preloaded):

| Use | Font | Notes |
|---|---|---|
| Headlines, essay body, names | `Newsreader` (serif) | weights 200-800 + italic, negative tracking on display sizes |
| UI, body, labels, meta | `Instrument Sans` | weights 400-700 |

- Base size 1rem, line-height 1.7 (UI) / 1.8 (essay text at 1.12rem)
- Display sizes use `clamp()` for fluid scaling
- `text-wrap: balance` on headings, `tabular-nums` on dates
- Labels: 0.72rem, uppercase, letter-spacing 0.14em

---

## Color Palette
All values live in `styles.css` as CSS variables. Navy is the foundation in both themes; grays are navy-tinted so nothing reads as flat black or white.

| Role | Variable | Light | Dark |
|---|---|---|---|
| Background | `--bg` | `#ffffff` | `#0b1420` |
| Subtle background | `--bg-subtle` | `#f4f8fb` | `#101c2c` |
| Hover background | `--bg-hover` | `#ecf3f9` | `#152334` |
| Tint (chips, tags) | `--tint` | `#e4eef7` | `#16273c` |
| Primary text | `--text` | `#2a3b4d` | `#c3d2e2` |
| Strong text / headings | `--text-strong` | `#0e1d30` | `#eef4fa` |
| Secondary text | `--secondary` | `#56697e` | `#91a6bc` |
| Muted text | `--muted` | `#75889b` | `#7289a1` |
| Labels | `--label` | `#8fa1b3` | `#5d7389` |
| Borders | `--border` | `#dde7f0` | `#1f3046` |
| Soft borders | `--border-soft` | `#cfdde9` | `#2a3e58` |
| Accent (links, active) | `--accent` | `#1f4e79` | `#79a9d8` |
| Accent strong (hover) | `--accent-strong` | `#163a5c` | `#a3c6e8` |
| Accent soft (kickers) | `--accent-soft` | `#4a7fb5` | `#4d7eae` |
| Footer | `--footer-bg` → `--footer-bg2` | `#0e1d30` → `#173455` | `#081120` → `#102342` |

One accent family only (navy/blue). No purple, no multi-color gradients.

### Gradients
- Background: five blurred colour blobs (`--blob1`-`--blob5`, navy through azure to a soft teal-cyan) orbiting independently on a fixed `.gradient-bg` layer injected by `main.js`. Three orbit on offset transform-origins (24s/28s/36s), one drifts vertically (26s), one horizontally (30s). One `blur(42px)` pass on the container; `screen` blend in dark mode, `normal` in light. Inspired by Aceternity's background-gradient-animation
- Hero headline: gradient text with an 8s sheen passing across it
- Hero headline and 404 numeral: linear gradient text from `--text-strong` into the accent
- Active filter chips: `--accent` to `--accent-soft` fill
- Footer: deep navy diagonal gradient block
- Shadows are navy-tinted (`--shadow`), never pure black in light mode

---

## Dark Mode
- Toggle button in the header (`#theme-toggle`), handled by `main.js`
- Persists in `localStorage`; inline head script applies it before first paint
- Follows `prefers-color-scheme` when no choice is stored
- Dark theme is deep navy (`#0b1420` base), not gray or black

---

## Layout
- Max width 1060px, `padding: 0 1.75rem`
- Homepage: full-width hero, then two columns (`main` flex 1 + 230px sidebar)
- Narrow pages: About 760px, essays 700px
- Lists use hairline dividers (1px `--border`) instead of boxed cards
- Single breakpoint: `@media (max-width: 700px)` stacks everything

---

## Motion
- Scroll reveals: `.reveal` elements fade and rise 14px when entering the viewport, staggered 60ms apart (IntersectionObserver in `main.js`; class added only when JS runs, so no-JS users see everything)
- Hovers: image scale 1.025-1.04 inside fixed masks, arrow nudges on text links, 200ms transitions
- Press feedback: small scale-down on buttons and chips
- `prefers-reduced-motion` disables all of it

---

## Components

### Header
- Locked to the top: `position: sticky` with frosted glass (`--bg-glass` + `backdrop-filter: blur(14px) saturate(1.4)`, solid `--bg` fallback via `@supports`)
- Hairline bottom border, serif site name, sans nav
- Active nav link underlined in `--accent`
- Round 30px theme toggle
- Mobile: tagline hidden and padding tightened so the locked header stays compact
- `scroll-padding-top` on `html` keeps anchor targets clear of the header

### Hero (homepage)
- Uppercase kicker, serif display headline (clamp 2-2.9rem), one-paragraph lede, two text links

### Featured essay
- 21:9 image in rounded mask, kicker "Featured essay", serif title, meta row, excerpt, tags, text link

### Entry rows (home + essays page)
- Hairline-divided rows: serif title, date `·` platform meta, excerpt, 168px 4:3 thumbnail right
- Mobile: thumbnail stacks on top at 2:1

### Tag filter (essays page)
- Pill chips built from post tags ordered by frequency, `aria-pressed` state, inverted fill when active
- Selection syncs to `#topic=` hash; result count announced via `aria-live`

### Sidebar
- Borderless widgets under uppercase labels with hairline underline
- 110px circular portrait in full color, navy ring and soft shadow

### About page
- Hero: 140px full-color portrait with navy ring, serif name, bio, bordered social chips
- "What I do": 200px/1fr grid rows per service
- "Selected writing": title + one-line note left, platform `·` year right
- "Focus areas": tag chips

### Essay pages
- 700px column, serif display title, serif body at 1.12rem/1.8
- Blockquotes: 2px dark left rule, italic
- `.post-title` and `.post-content` class names are required by `new-post.py`

### Footer
- Deep navy gradient block, serif name + footer nav row in light text, small copyright line

### 404
- Oversized italic serif "404", short explanation, links home and to essays

---

## SEO
- Self-hosted fonts (no third-party requests), preloaded woff2
- `sitemap.xml` + `robots.txt` (drafts disallowed)
- Canonical, Open Graph, Twitter cards, `theme-color`, JSON-LD (Person / Blog) per page
- One `h1` per page; site name in header is a styled `p`
- SVG favicon (`assets/images/favicon.svg`)
- `aria-label`s and focus-visible outlines (no skip link by owner preference; the locked header keeps nav one tab away)

---

## Files
| File | Purpose |
|---|---|
| `styles.css` | All styles, single file, no framework |
| `main.js` | Theme toggle, reveals, list rendering, tag filter, footer year |
| `posts.js` | Post data array shared across pages |
| `index.html` | Homepage: hero + featured + latest + sidebar |
| `blog.html` | All essays with tag filtering |
| `about.html` | Bio, services, selected writing, focus areas |
| `404.html` | Not-found page (GitHub Pages picks it up automatically) |
| `assets/fonts/` | Newsreader + Instrument Sans variable woff2 |
| `_drafts/_post-template.html` | Template for new self-hosted essays |
