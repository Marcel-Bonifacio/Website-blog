# Marcel Bonifacio Tirta Wijata — Personal Blog

Personal website and blog at [tirtawijata.com](https://tirtawijata.com), covering renewable energy, climate policy, and sustainability in Indonesia and Southeast Asia.

---

## How the Site Works

- **`index.html`** — Homepage: 1 featured article + 4 most recent articles
- **`blog.html`** — Posts page: all articles listed by date
- **`about.html`** — About page
- **`posts.js`** — The single source of truth for all article data
- **`posts/`** — Self-hosted articles (HTML files)
- **`_drafts/`** — Drafts folder for writing new posts locally

---

## Updating Articles

### Option 1 — Add an External Article (Medium or Kumparan)

Open `posts.js` and add a new entry to the `POSTS` array:

```js
{
  id: "unique-slug",                        // unique, lowercase, hyphenated
  title: "Your Article Title",
  dateISO: "2026-01-15",                    // YYYY-MM-DD format
  dateDisplay: "January 15, 2026",
  platform: "Medium",                       // "Medium" or "Kumparan"
  excerpt: "A one or two sentence summary that hooks the reader.",
  url: "https://medium.com/@marcelbonifaciotirtawijata/your-article",
  external: true,
  tags: ["Renewable Energy", "Indonesia"],
  featured: false                           // set true to pin to homepage hero
}
```

- Only **one** post should have `featured: true` at a time.
- Save the file, commit, and push — the site updates automatically.

---

### Option 2 — Auto-Sync from Medium (Automatic)

A GitHub Actions workflow runs every day at 07:00 UTC and pulls new articles from your Medium RSS feed automatically. No manual steps needed — new Medium posts appear on the site within 24 hours of publishing.

To trigger a sync manually:
1. Go to **Actions** tab on GitHub
2. Select **Sync Posts**
3. Click **Run workflow**

---

### Option 3 — Write and Publish Your Own Post

Use this workflow to write a post hosted directly on this site (not on Medium/Kumparan).

**Step 1 — Copy the template**

```bash
cp _drafts/_post-template.html _drafts/my-new-post.html
```

**Step 2 — Fill in the template**

Open `_drafts/my-new-post.html` and edit the `<!-- META -->` block at the top:

```html
<!-- META
title: Your Post Title
date: 2026-01-15
excerpt: A compelling one-sentence summary.
tags: Renewable Energy, Indonesia
-->
```

Then write your article content in the `<article>` section below.

**Step 3 — Publish**

```bash
python new-post.py _drafts/my-new-post.html
```

This script moves the file to `posts/`, generates the correct HTML, and adds the entry to `posts.js` automatically.

**Step 4 — Commit and push**

```bash
git add posts/ posts.js
git commit -m "post: Your Post Title"
git push
```

---

## Changing the Featured Article

Open `posts.js`, find the post you want to feature, and set `featured: true`. Make sure all other posts have `featured: false`.

```js
// Before
{ id: "old-featured", ..., featured: true  }
{ id: "new-featured", ..., featured: false }

// After
{ id: "old-featured", ..., featured: false }
{ id: "new-featured", ..., featured: true  }
```

---

## Updating Site Content

| What to change | Where |
|---|---|
| Bio text | `about.html` — edit the `<p>` inside `.about-bio` |
| Profile photo | Replace `assets/images/image02_v=de04ef50.jpg` |
| Social links | `about.html` and `index.html` — update `href` attributes in `.social-links` |
| Color palette | `styles.css` — edit CSS variables in `:root` and `[data-theme="dark"]` |
| Site name / title | `index.html`, `about.html`, `blog.html` — update `<title>` and `<h1>` |

---

## Deployment

The site deploys automatically to GitHub Pages whenever you push to `main`.

- **Custom domain**: configured via `CNAME` (set to `tirtawijata.com`)
- **Deploy workflow**: `.github/workflows/static.yml`
- **Sync workflow**: `.github/workflows/sync.yml` (runs daily, auto-commits new posts)

To deploy manually: push any commit to `main`.

---

## Local Preview

```bash
python -m http.server 8080
```

Then open [http://localhost:8080](http://localhost:8080) in your browser.
