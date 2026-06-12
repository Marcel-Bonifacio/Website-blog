# Design Guide

## Philosophy
Minimalistic. The design is intentionally plain — content first, no decorative clutter. Inspired by the [DevAbdurR/Static-Blog](https://github.com/DevAbdurR/Static-Blog) layout.

---

## Typography
- **Font:** Helvetica Neue → Helvetica → Arial (system sans-serif fallback)
- **Base size:** 1rem (16px)
- **Line height:** 1.75
- **Anti-aliasing:** `-webkit-font-smoothing: antialiased`

---

## Color Palette
All values live in `styles.css` as CSS variables (needed for the dark theme). Both themes are strictly grayscale — flat and close to neutral.

| Role | Variable | Light | Dark |
|---|---|---|---|
| Background | `--bg` | `#fff` | `#121212` |
| Card background | `--bg-card` | `#fff` | `#171717` |
| Hover background | `--bg-hover` | `#fafafa` | `#1e1e1e` |
| Primary text | `--text` | `#333` | `#c9c9c9` |
| Strong text / headings | `--text-strong` | `#111` | `#ededed` |
| Secondary text | `--secondary` | `#777` | `#9a9a9a` |
| Muted text | `--muted` | `#999` | `#828282` |
| Labels | `--label` | `#aaa` | `#6e6e6e` |
| Borders | `--border` | `#e8e8e8` | `#2a2a2a` |
| Badge borders | `--border-soft` | `#e0e0e0` | `#333` |

No accent colour. No blue, no green.

---

## Dark Mode
- Toggle button in the header (`#theme-toggle`), handled by `main.js`.
- Choice persists in `localStorage` under `theme`; a tiny inline script in each page's `<head>` applies it before first paint (no flash).
- With no stored choice, the site follows `prefers-color-scheme`.
- Dark theme uses the same grayscale system — never colored.

---

## Layout
- **Max width:** 1060px, centered, `padding: 0 1.75rem`
- **Two-column (desktop ≥ 700px):** `main` (flex: 1) + `.sidebar` (220px fixed)
- **Single column (mobile < 700px):** stacked, sidebar below content
- **Narrow pages** (About, posts): `max-width: 720px` / `680px`

---

## Components

### Header
- Site background, `border-bottom: 1px solid var(--border)`
- Site title left (name + tagline), nav + theme toggle right
- Nav links: uppercase, 0.78rem, muted default → strong on active/hover

### Article Cards (home + blog listing)
- `border: 1px solid var(--border)`, `border-radius: 6px`, `padding: 1.25–1.5rem`
- Hover: border darkens slightly + soft shadow — no color change
- Matches the card/button aesthetic of the original tirtawijata.com profile

### Sidebar Widgets
- Same card style: `border: 1px solid var(--border)`, `border-radius: 6px`
- **Profile image:** 110×110px circle (`border-radius: 50%`), centered
- About Me text is center-aligned

### Profile Images (About page)
- 130×130px circle (`border-radius: 50%`)

### Platform Badges
- Tiny bordered label: `font-size: 0.68rem`, `border: 1px solid var(--border-soft)`, `padding: 0.1rem 0.45rem`, `border-radius: 2px`

### Tags
- Same border style as badges, muted text

### Post Pages
- `.post-wrapper`: 680px max width, centered
- `.post-content` styles paragraphs, headings, lists, blockquotes, inline code, and images

### Footer
- `border-top: 1px solid var(--border)`, centered muted text — no filled background

---

## Responsive Breakpoint
`@media (max-width: 700px)` — single column, header stacks vertically, profile image shrinks to 110px circle.

---

## Accessibility
- `:focus-visible` outlines on all interactive elements
- `prefers-reduced-motion` disables transitions
- Theme toggle has an `aria-label`

---

## Files
| File | Purpose |
|---|---|
| `styles.css` | All styles — single file, no framework |
| `main.js` | Shared behaviour: theme toggle, footer year, post-list rendering |
| `posts.js` | Post data array shared across all pages |
| `index.html` | Homepage (rendered by `main.js` from `posts.js`) |
| `about.html` | Static about page |
| `blog.html` | All posts listing (rendered by `main.js`) |
| `_drafts/_post-template.html` | Template for new self-hosted posts |
