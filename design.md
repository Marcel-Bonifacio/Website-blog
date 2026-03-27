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
All values are in `styles.css`. No named CSS variables are used — colours are intentionally flat and close to neutral.

| Role | Value |
|---|---|
| Background | `#fff` |
| Primary text | `#333` |
| Secondary text | `#777` / `#999` |
| Muted / labels | `#aaa` / `#bbb` |
| Borders | `#e8e8e8` |
| Header borders | `#e8e8e8` |
| Links | `#333` (inherit) |

No accent colour. No blue, no green.

---

## Layout
- **Max width:** 1060px, centered, `padding: 0 1.75rem`
- **Two-column (desktop ≥ 700px):** `main` (flex: 1) + `.sidebar` (220px fixed)
- **Single column (mobile < 700px):** stacked, sidebar below content

---

## Components

### Header
- White background, `border-bottom: 1px solid #e8e8e8`
- Site title left (name + tagline), nav right
- Nav links: uppercase, 0.78rem, `#999` default → `#111` active/hover

### Article Cards (home + blog listing)
- `border: 1px solid #e8e8e8`, `border-radius: 6px`, `padding: 1.25–1.5rem`
- Matches the card/button aesthetic of the original tirtawijata.com profile

### Sidebar Widgets
- Same card style: `border: 1px solid #e8e8e8`, `border-radius: 6px`
- **Profile image:** 110×110px circle (`border-radius: 50%`), centered
- About Me text is center-aligned

### Profile Images (About page)
- 130×130px circle (`border-radius: 50%`)

### Platform Badges
- Tiny bordered label: `font-size: 0.68rem`, `border: 1px solid #e0e0e0`, `padding: 0.1rem 0.45rem`, `border-radius: 2px`

### Tags
- Same border style as badges, `color: #999`

---

## Responsive Breakpoint
`@media (max-width: 700px)` — single column, header stacks vertically, profile image shrinks to 110px circle.

---

## Files
| File | Purpose |
|---|---|
| `styles.css` | All styles — single file, no framework |
| `index.html` | Homepage (JS-rendered from `posts.js`) |
| `about.html` | Static about page |
| `blog.html` | All posts listing (JS-rendered) |
| `posts.js` | Post data array shared across all pages |
