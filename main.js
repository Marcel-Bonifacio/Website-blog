/**
 * main.js — Shared site behaviour
 *
 * Handles: theme toggle, footer year, and post-list rendering
 * for the homepage (#posts-main, #sidebar-recent) and the
 * blog listing (#blog-list). Post data comes from posts.js.
 *
 * Load order: posts.js first, then main.js (both with `defer`).
 */
(function () {
  'use strict';

  /* ── Helpers ── */

  function esc(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function linkAttr(post) {
    return post.external ? ' target="_blank" rel="noopener"' : '';
  }

  function badge(platform) {
    var icon = '';
    if (platform === 'Medium') {
      icon = '<img src="assets/images/medium.svg" class="icon-medium" alt="">';
    } else if (platform === 'Kumparan') {
      icon = '<img src="assets/images/kumparan.svg" alt="">';
    }
    return '<span class="platform-badge">' + icon + esc(platform) + '</span>';
  }

  function renderTags(tags) {
    if (!tags || !tags.length) return '';
    return '<div class="article-tags">' + tags.map(function (t) {
      return '<span class="tag">' + esc(t) + '</span>';
    }).join('') + '</div>';
  }

  function sortedPosts() {
    return (window.POSTS || []).slice().sort(function (a, b) {
      return new Date(b.dateISO) - new Date(a.dateISO);
    });
  }

  /* ── Footer year ── */

  var yearEl = document.getElementById('footer-year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ── Theme toggle ── */

  var toggleBtn = document.getElementById('theme-toggle');
  if (toggleBtn) {
    var getTheme = function () {
      return document.documentElement.getAttribute('data-theme') ||
        (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    };
    var setIcon = function (theme) {
      toggleBtn.innerHTML = theme === 'dark' ? '&#9728;' : '&#9790;';
    };
    setIcon(getTheme());
    toggleBtn.addEventListener('click', function () {
      var next = getTheme() === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) { /* private mode */ }
      setIcon(next);
    });
  }

  /* ── Homepage: featured + recent + sidebar ── */

  var main = document.getElementById('posts-main');
  var sidebarRecent = document.getElementById('sidebar-recent');

  if (main) {
    var sorted = sortedPosts();

    if (!sorted.length) {
      main.innerHTML = '<p class="empty-state">No posts yet.</p>';
      if (sidebarRecent) {
        sidebarRecent.innerHTML =
          '<h2 class="widget-title">Recent Posts</h2><p class="widget-body">No posts yet.</p>';
      }
    } else {
      var featured = null;
      for (var i = 0; i < sorted.length; i++) {
        if (sorted[i].featured) { featured = sorted[i]; break; }
      }
      if (!featured) featured = sorted[0];
      var rest = sorted.filter(function (p) { return p.id !== featured.id; });

      var html = '<article class="article-featured">';
      if (featured.image) {
        html += '<img src="' + esc(featured.image) + '" class="article-featured-img" alt="" loading="lazy">';
      }
      html += '<div class="article-featured-inner">';
      html += '<span class="featured-label">Featured</span>';
      html += '<h2 class="article-title"><a href="' + esc(featured.url) + '"' + linkAttr(featured) + '>' +
        esc(featured.title) + (featured.external ? ' &#8599;' : '') + '</a></h2>';
      html += '<div class="article-meta"><span>' + esc(featured.dateDisplay) + '</span>' + badge(featured.platform) + '</div>';
      html += '<p class="article-body">' + esc(featured.excerpt) + '</p>';
      html += renderTags(featured.tags);
      html += '<a href="' + esc(featured.url) + '"' + linkAttr(featured) + ' class="article-read-more">Continue Reading</a>';
      html += '</div></article>';

      rest.slice(0, 4).forEach(function (post) {
        html += '<article class="article-recent">';
        if (post.image) {
          html += '<img src="' + esc(post.image) + '" class="article-recent-img" alt="" loading="lazy">';
        }
        html += '<div class="article-recent-main">';
        html += '<h2 class="article-title"><a href="' + esc(post.url) + '"' + linkAttr(post) + '>' +
          esc(post.title) + (post.external ? ' &#8599;' : '') + '</a></h2>';
        html += '<div class="article-meta"><span>' + esc(post.dateDisplay) + '</span>' + badge(post.platform) + '</div>';
        html += '<p class="article-body">' + esc(post.excerpt) + '</p>';
        html += '</div></article>';
      });

      if (rest.length) {
        html += '<p class="view-all-link"><a href="blog.html">View all posts &rarr;</a></p>';
      }

      main.innerHTML = html;

      if (sidebarRecent) {
        var sbHtml = '<h2 class="widget-title">Recent Posts</h2>';
        sorted.slice(0, 4).forEach(function (post) {
          sbHtml += '<div class="widget-recent-post">';
          sbHtml += '<p class="widget-recent-post-title"><a href="' + esc(post.url) + '"' + linkAttr(post) + '>' +
            esc(post.title) + '</a></p>';
          sbHtml += '<p class="widget-recent-post-date">' + esc(post.dateDisplay) + '</p>';
          sbHtml += '</div>';
        });
        sidebarRecent.innerHTML = sbHtml;
      }
    }
  }

  /* ── Blog listing ── */

  var list = document.getElementById('blog-list');
  if (list) {
    var posts = sortedPosts();

    if (!posts.length) {
      list.innerHTML = '<p class="empty-state">No posts yet.</p>';
    } else {
      var listHtml = '';
      posts.forEach(function (post) {
        listHtml += '<article class="blog-card">';
        if (post.image) {
          listHtml += '<img src="' + esc(post.image) + '" class="blog-card-img" alt="" loading="lazy">';
        }
        listHtml += '<div class="blog-card-body">';
        listHtml += '<h2><a href="' + esc(post.url) + '"' + linkAttr(post) + '>' +
          esc(post.title) + (post.external ? ' &#8599;' : '') + '</a></h2>';
        listHtml += '<div class="meta"><span>' + esc(post.dateDisplay) + '</span>' + badge(post.platform) + '</div>';
        listHtml += '<p class="excerpt">' + esc(post.excerpt) + '</p>';
        listHtml += renderTags(post.tags);
        listHtml += '</div></article>';
      });
      list.innerHTML = listHtml;
    }
  }
}());
