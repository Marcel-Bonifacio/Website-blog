# Site Workflow

## How the Site Works

This is a **static HTML site** hosted on GitHub Pages at `tirtawijata.com`.

- No backend, no database, no build step required
- All post data lives in `posts.js` as a plain JavaScript array
- Pages read `posts.js` at runtime and render content with vanilla JS
- Pushing to the `main` branch automatically deploys to GitHub Pages

---

## Auto-Sync (Medium & Kumparan)

A GitHub Actions workflow runs `sync.py` daily at **07:00 UTC**.

**What it does:**
1. Fetches the Medium RSS feed: `https://medium.com/feed/@marcelbonifaciotirtawijata`
2. Attempts to scrape new article links from the Kumparan profile
3. Compares against existing post IDs in `posts.js`
4. Appends any new posts as `featured: false` entries
5. Commits the updated `posts.js` automatically

**To run manually:**
```bash
python sync.py
```

**After sync:**
- Open `posts.js` and review the new entries
- Fix titles, excerpts, or tags if needed
- Set `featured: true` on the post you want as the homepage hero
- Commit and push

**GitHub Actions file:** `.github/workflows/sync.yml`

---

## Writing Your Own Post

See `NEW_POST.md` for the full step-by-step guide.

**Short version:**
```bash
cp _drafts/_post-template.html _drafts/my-post-slug.html
# edit the file
python new-post.py _drafts/my-post-slug.html
git add posts.js posts/my-post-slug.html
git commit -m "post: My Post Title"
git push
```

---

## Deployment

The site deploys automatically via GitHub Pages.

1. Go to your repo → **Settings → Pages**
2. Set **Source** to `Deploy from a branch`, branch `main`, folder `/` (root)
3. Add your custom domain (`tirtawijata.com`) under **Custom domain**
4. The `CNAME` file in the repo root already contains `tirtawijata.com`

Any `git push` to `main` triggers a new deployment within ~60 seconds.

---

## File Structure

```
/
├── index.html          Homepage
├── about.html          About page
├── blog.html           All posts listing
├── posts.js            Post data (source of truth)
├── styles.css          All styles
├── sync.py             Auto-sync Medium + Kumparan → posts.js
├── new-post.py         Publish a draft from _drafts/
├── CNAME               Custom domain for GitHub Pages
├── assets/
│   └── images/         Profile photo, icons, OG card image
├── posts/
│   └── *.html          Self-hosted post pages
├── _drafts/
│   └── _post-template.html   Copy this to write a new post
└── .github/
    └── workflows/
        └── sync.yml    Daily auto-sync GitHub Action
```
