# tirtawijata.com — Personal Blog

Personal website of Marcel Bonifacio Tirta Wijata. Built with static HTML/CSS/JS, hosted on GitHub Pages.

---

## Quick links

| Page | File |
|------|------|
| Home | `index.html` |
| About | `about.html` |
| Posts | `blog.html` |
| All post data | `posts.js` |
| Styles | `styles.css` |

---

## How articles are added to the website

### Automatic sync (recommended)

Articles you publish on **Medium** are synced automatically every day at 07:00 UTC via GitHub Actions.

What auto-sync does for you:
- Detects new articles from your Medium RSS feed
- Adds them to `posts.js` with the correct title, date, excerpt, and tags
- **Pulls the header image directly from Medium** — if you change your article's cover image on Medium, it will update here on the next daily run
- Runs without any manual action on your part

To trigger a manual sync immediately (instead of waiting for the daily cron):
1. Go to **GitHub → Actions → Sync Posts**
2. Click **Run workflow → Run workflow**

After sync, new posts appear with `featured: false`. If you want to promote one to the homepage hero, edit `posts.js` and set `featured: true` on that post (and `false` on all others).

---

### Adding a Medium or Kumparan article manually

Open `posts.js` and add a new entry to the `POSTS` array:

```js
{
  id: "my-unique-slug",           // short kebab-case ID, no spaces
  title: "Your Article Title",
  dateISO: "2025-03-27",          // YYYY-MM-DD
  dateDisplay: "March 27, 2025",
  platform: "Medium",             // "Medium" | "Kumparan"
  excerpt: "One or two engaging sentences that appear on the card.",
  url: "https://medium.com/@marcelbonifaciotirtawijata/your-article-url",
  image: "",                      // leave blank — sync.py fills this from RSS
  external: true,
  tags: ["Renewable Energy", "Indonesia"],
  featured: false
}
```

> **Tip:** Leave `image` blank for Medium posts. The daily sync will fill it from your Medium RSS feed automatically. For Kumparan posts, paste the article's OG image URL manually.

---

### Writing and publishing your own post (hosted on this site)

1. Copy `_drafts/_post-template.html` to a new file inside `_drafts/`, e.g. `_drafts/my-new-post.html`
2. Fill in the `<!-- META -->` block at the top of the file (title, date, excerpt, tags)
3. Write your article in the `<article>` body
4. Run the publish script from the project root:
   ```bash
   python new-post.py _drafts/my-new-post.html
   ```
   This copies the file to `posts/` and adds an entry to `posts.js` automatically.
5. Commit and push to GitHub — the site updates within ~2 minutes

---

## Setting the featured article

Only **one** post should have `featured: true`. This post appears as the large hero card at the top of the homepage.

To change the featured post, open `posts.js` and:
1. Find the current featured post → set `featured: false`
2. Find the post you want to feature → set `featured: true`
3. Commit and push

---

## How images work

| Source | How image is set |
|--------|-----------------|
| Medium | Pulled automatically from `<media:content>` in the RSS feed — reflects whatever cover image you set on Medium |
| Kumparan | Paste the OG image URL manually in `posts.js` |
| Own post | Add an `image:` field in the `<!-- META -->` block of your draft |

If you update a cover image on Medium, it will be reflected here within 24 hours (next daily sync). To apply it immediately, run the manual sync via GitHub Actions.

---

## Deployment

The site is hosted on **GitHub Pages** from the `main` branch root. Every `git push` to `main` deploys automatically — no build step needed.

```bash
git add .
git commit -m "your message"
git push origin main
```

---

## Light / dark mode

The site supports both modes with persistent preference via `localStorage`. A toggle button (☾) sits in the top-right of the header. The system's `prefers-color-scheme` is used as the default for first-time visitors.

---

## Project structure

```
├── index.html              Homepage (1 featured + 4 recent articles)
├── about.html              About page
├── blog.html               Full posts listing
├── posts.js                Single source of truth for all post metadata
├── styles.css              All styles (light + dark mode via CSS variables)
├── sync.py                 Auto-sync script (Medium RSS + Kumparan scraper)
├── new-post.py             Publish a draft from _drafts/ to posts/
├── _drafts/
│   └── _post-template.html Template for writing your own posts
├── posts/                  Published own posts (HTML files)
├── assets/
│   └── images/             Profile photo, platform icons
├── .github/
│   └── workflows/
│       └── sync.yml        Daily GitHub Actions sync job
├── design.md               Color palette and component guide
├── workflow.md             Full site workflow documentation
└── NEW_POST.md             Step-by-step guide to writing a new post
```
