# How to Write a New Post

You can publish two types of posts:

| Type | When to use |
|---|---|
| **Own post** (hosted here) | Original writing you want to live on tirtawijata.com |
| **External link** (Kumparan / Medium) | Links to articles published elsewhere — added automatically by `sync.py`, or manually |

---

## Option A — Write Your Own Post

### Step 1 — Copy the template

```bash
cp _drafts/_post-template.html _drafts/your-post-slug.html
```

Use a short, lowercase, hyphenated slug (e.g. `indonesia-energy-transition`).

### Step 2 — Fill in the META block

Open the file and edit the `<!-- META -->` comment at the top:

```html
<!-- META
slug:    indonesia-energy-transition
title:   Indonesia's Energy Transition Challenge
date:    2026-03-27
tags:    Indonesia, Renewable Energy, Policy
excerpt: A one or two sentence summary shown in listings. Keep under 260 characters.
-->
```

### Step 3 — Write your content

Below the `<div class="post-content">` section, write in plain HTML:

```html
<p>Your introduction paragraph.</p>

<h2>Section Heading</h2>

<p>Body text with <strong>bold</strong>, <em>italics</em>, or
<a href="https://example.com" target="_blank" rel="noopener">links</a>.</p>
```

Also update the `<title>` tag and the `<h1 class="post-title">` and `<p class="post-meta">` to match your actual title and date.

### Step 4 — Publish

```bash
python new-post.py _drafts/your-post-slug.html
```

This copies the file to `posts/your-post-slug.html` and adds an entry to `posts.js`.

### Step 5 — (Optional) Set as featured

Open `posts.js` and set `featured: true` on your new post if you want it as the homepage hero. Remember to set the old featured post to `featured: false`.

### Step 6 — Deploy

```bash
git add posts.js posts/your-post-slug.html
git commit -m "post: Indonesia's Energy Transition Challenge"
git push
```

The site updates on GitHub Pages within ~60 seconds.

---

## Option B — Add an External Link Manually

Open `posts.js` and add an entry to the `POSTS` array:

```js
{
  id: "your-article-slug",
  title: "Your Article Title",
  dateISO: "2026-03-27",
  dateDisplay: "March 27, 2026",
  platform: "Medium",          // or "Kumparan"
  excerpt: "A short description of the article.",
  url: "https://medium.com/@marcelbonifaciotirtawijata/your-article",
  external: true,
  tags: ["Tag One", "Tag Two"],
  featured: false
},
```

Then push to deploy.

---

## Auto-Sync (Hands-Free)

Medium and Kumparan articles are synced automatically every day by the GitHub Action in `.github/workflows/sync.yml`. You only need to manually add if you want to update tags, the excerpt, or set `featured: true`.

To sync immediately:
```bash
python sync.py
```
