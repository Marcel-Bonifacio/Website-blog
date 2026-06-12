/**
 * main.js / Shared site behaviour
 *
 * Theme toggle, footer year, scroll reveals, post-list rendering
 * (homepage + posts page), and tag filtering. Post data: posts.js.
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

  function platformHtml(platform) {
    var icon = '';
    if (platform === 'Medium') {
      icon = '<img src="assets/images/medium.svg" class="icon-medium" alt="">';
    } else if (platform === 'Kumparan') {
      icon = '<img src="assets/images/kumparan.svg" alt="">';
    }
    return '<span class="platform">' + icon + esc(platform) + '</span>';
  }

  function metaHtml(post) {
    return '<div class="entry-meta"><time datetime="' + esc(post.dateISO) + '">' +
      esc(post.dateDisplay) + '</time><span class="dot">·</span>' +
      platformHtml(post.platform) + '</div>';
  }

  function tagsHtml(tags) {
    if (!tags || !tags.length) return '';
    return '<div class="entry-tags">' + tags.map(function (t) {
      return '<span class="tag">' + esc(t) + '</span>';
    }).join('') + '</div>';
  }

  function titleHtml(post, cls, tag) {
    return '<' + tag + ' class="' + cls + '"><a href="' + esc(post.url) + '"' + linkAttr(post) + '>' +
      esc(post.title) + (post.external ? ' <span aria-hidden="true">&#8599;</span>' : '') + '</a></' + tag + '>';
  }

  function entryHtml(post, withTags) {
    var html = '<article class="entry reveal">';
    html += '<div class="entry-body">';
    html += titleHtml(post, 'entry-title', 'h3');
    html += metaHtml(post);
    html += '<p class="entry-excerpt">' + esc(post.excerpt) + '</p>';
    if (withTags) html += tagsHtml(post.tags);
    html += '</div>';
    if (post.image) {
      html += '<a class="entry-thumb" href="' + esc(post.url) + '"' + linkAttr(post) + ' tabindex="-1" aria-hidden="true">' +
        '<img src="' + esc(post.image) + '" alt="" loading="lazy"></a>';
    }
    html += '</article>';
    return html;
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

  /* ── Scroll reveals (progressive enhancement) ── */

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initReveals(root) {
    var els = (root || document).querySelectorAll('.reveal:not(.in)');
    if (reduceMotion || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (items) {
      items.forEach(function (item) {
        if (item.isIntersecting) {
          item.target.classList.add('in');
          io.unobserve(item.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    var delay = 0;
    els.forEach(function (el) {
      el.style.setProperty('--reveal-delay', (delay % 360) + 'ms');
      delay += 60;
      io.observe(el);
    });
  }

  /* ── Homepage ── */

  var main = document.getElementById('posts-main');
  var sidebarRecent = document.getElementById('sidebar-recent');

  if (main) {
    var sorted = sortedPosts();

    if (!sorted.length) {
      main.innerHTML = '<p class="empty-state">No essays yet. New writing appears here first.</p>';
    } else {
      var featured = null;
      for (var i = 0; i < sorted.length; i++) {
        if (sorted[i].featured) { featured = sorted[i]; break; }
      }
      if (!featured) featured = sorted[0];
      var rest = sorted.filter(function (p) { return p.id !== featured.id; });

      var html = '<article class="feature reveal">';
      if (featured.image) {
        html += '<a class="feature-media" href="' + esc(featured.url) + '"' + linkAttr(featured) + ' tabindex="-1" aria-hidden="true">' +
          '<img src="' + esc(featured.image) + '" alt=""></a>';
      }
      html += '<p class="kicker">Featured essay</p>';
      html += titleHtml(featured, 'feature-title', 'h2');
      html += metaHtml(featured);
      html += '<p class="feature-excerpt">' + esc(featured.excerpt) + '</p>';
      html += tagsHtml(featured.tags);
      html += '<a href="' + esc(featured.url) + '"' + linkAttr(featured) + ' class="text-link">Read the essay <span class="arrow">&rarr;</span></a>';
      html += '</article>';

      if (rest.length) {
        html += '<h2 class="section-label">Latest essays</h2>';
        html += '<div class="entry-list">';
        rest.slice(0, 4).forEach(function (post) { html += entryHtml(post, false); });
        html += '</div>';
        html += '<p class="view-all-link"><a href="blog.html" class="text-link">All essays <span class="arrow">&rarr;</span></a></p>';
      }

      main.innerHTML = html;

      if (sidebarRecent) {
        var sbHtml = '<h2 class="widget-title">Recent</h2>';
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

  /* ── Posts page: list + tag filter ── */

  var list = document.getElementById('blog-list');
  var filterBar = document.getElementById('tag-filter');

  if (list) {
    var posts = sortedPosts();

    var renderList = function (items) {
      if (!items.length) {
        list.innerHTML = '<p class="empty-state">Nothing under this topic yet.</p>';
        return;
      }
      var html = '<div class="entry-list">';
      items.forEach(function (post) { html += entryHtml(post, true); });
      html += '</div>';
      list.innerHTML = html;
      initReveals(list);
    };

    if (!posts.length) {
      list.innerHTML = '<p class="empty-state">No essays yet.</p>';
    } else if (filterBar) {
      // Collect tags ordered by frequency
      var counts = {};
      posts.forEach(function (p) {
        (p.tags || []).forEach(function (t) { counts[t] = (counts[t] || 0) + 1; });
      });
      var tags = Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a] || a.localeCompare(b); });

      var current = 'All';
      var fromHash = decodeURIComponent((location.hash.match(/^#topic=(.+)$/) || [, ''])[1]);
      if (fromHash && counts[fromHash]) current = fromHash;

      var applyFilter = function (tag) {
        current = tag;
        filterBar.querySelectorAll('.filter-chip').forEach(function (b) {
          b.setAttribute('aria-pressed', b.dataset.tag === tag ? 'true' : 'false');
        });
        var items = tag === 'All' ? posts : posts.filter(function (p) {
          return (p.tags || []).indexOf(tag) !== -1;
        });
        renderList(items);
        var count = document.getElementById('filter-count');
        if (count) {
          count.textContent = items.length + (items.length === 1 ? ' essay' : ' essays') +
            (tag === 'All' ? '' : ' on ' + tag);
        }
        if (history.replaceState) {
          history.replaceState(null, '', tag === 'All' ? location.pathname : '#topic=' + encodeURIComponent(tag));
        }
      };

      var chips = '<button class="filter-chip" data-tag="All" aria-pressed="true">All</button>';
      tags.forEach(function (t) {
        chips += '<button class="filter-chip" data-tag="' + esc(t) + '" aria-pressed="false">' + esc(t) + '</button>';
      });
      filterBar.innerHTML = chips;
      filterBar.addEventListener('click', function (e) {
        var btn = e.target.closest('.filter-chip');
        if (btn) applyFilter(btn.dataset.tag);
      });

      applyFilter(current);
    } else {
      renderList(posts);
    }
  }

  /* ── Activate reveals for everything rendered so far ── */
  initReveals(document);
}());
