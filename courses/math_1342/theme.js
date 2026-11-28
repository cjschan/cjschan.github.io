/* Auto / Light / Dark color theme for the Math 1342 syllabi and lecture slides.

   Pages are written in one dark palette. In light mode this script swaps every palette color
   (in <style> blocks, style="" attributes and SVG fill/stroke, including graphs drawn later by
   statgraphs.js / statkey.js) for its light counterpart, and restores the originals in dark mode.

   Choice: localStorage "m1342-theme" = auto | light | dark (default dark), shared by every page
   on the site. ?theme=light|dark|auto in the URL overrides it for that visit.
   Load it in <head> right after the page's own <style>:
     <link rel="stylesheet" href="theme.css?v=1"><script src="theme.js?v=1" data-placement="page"></script>
   data-placement: "page" (fixed top right) or "deck" (bottom right, beside the slide number). */
(function () {
  'use strict';
  var KEY = 'm1342-theme';
  var CHOICES = ['auto', 'light', 'dark'];
  var DEFAULT = 'dark';   // pages keep their original dark look until a student picks Auto or Light
  var root = document.documentElement;
  var script = document.currentScript;
  var placement = (script && script.dataset.placement) || 'page';

  // Dark palette -> light palette. One pass, so swapped pairs (#475569 <-> #cbd5e1) are safe.
  var HEX = {
    '#0f172a': '#ffffff', '#1e293b': '#f1f5f9', '#334155': '#e2e8f0', '#475569': '#cbd5e1',
    '#f1f5f9': '#0f172a', '#f8fafc': '#0f172a', '#e2e8f0': '#1e293b', '#cbd5e1': '#475569',
    '#94a3b8': '#475569', '#64748b': '#475569',
    '#38bdf8': '#075985', '#fbbf24': '#92400e', '#34d399': '#065f46', '#fb7185': '#9f1239',
    '#818cf8': '#4338ca', '#a78bfa': '#5b21b6', '#e879f9': '#86198f',
    '#7dd3fc': '#0369a1', '#0284c7': '#0c4a6e', '#fde68a': '#78350f',
    '#a5b4fc': '#3730a3', '#f59e0b': '#92400e', '#1e1b4b': '#e0e7ff'
  };
  function rgbOf(h) { return [1, 3, 5].map(function (i) { return parseInt(h.substr(i, 2), 16); }).join(','); }
  var RGB = {};
  Object.keys(HEX).forEach(function (k) { RGB[rgbOf(k)] = rgbOf(HEX[k]); });
  RGB['15,23,42'] = '203,213,225';     // dark inset panels -> soft gray insets
  RGB['30,41,59'] = '241,245,249';
  RGB['148,163,184'] = '71,85,105';

  var HEX_RE = /#[0-9a-fA-F]{6}\b/g;
  var RGB_RE = /(rgba?\(\s*)(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/g;
  function mapText(s) {
    if (!s) return s;
    return s.replace(HEX_RE, function (m) { return HEX[m.toLowerCase()] || m; })
            .replace(RGB_RE, function (m, pre, r, g, b) {
              var t = RGB[r + ',' + g + ',' + b];
              return t ? pre + t.split(',').join(', ') : m;
            });
  }

  // ---- choice and effective theme
  function stored() {
    try { var v = localStorage.getItem(KEY); return CHOICES.indexOf(v) >= 0 ? v : DEFAULT; } catch (e) { return DEFAULT; }
  }
  var choice = stored();
  try {
    var q = new URLSearchParams(location.search).get('theme');
    if (CHOICES.indexOf(q) >= 0) choice = q;
  } catch (e) {}
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function effective() { return choice === 'auto' ? (mq && !mq.matches ? 'light' : 'dark') : choice; }
  var mode = null;   // currently applied: 'light' | 'dark'

  // ---- remapping with originals remembered
  var ATTRS = ['style', 'fill', 'stroke', 'stop-color', 'flood-color'];
  var orig = new Map();      // element -> {attr: original value}
  var written = new Map();   // element -> {attr: value this script wrote}
  var styleOrig = new Map(); // <style> -> original text
  var styleWritten = new Map();
  var busy = false;

  function setAttr(el, a, v) {
    var w = written.get(el); if (!w) { w = {}; written.set(el, w); }
    w[a] = v; el.setAttribute(a, v);
  }
  function doAttr(el, a) {
    var cur = el.getAttribute(a);
    if (cur === null) return;
    var w = written.get(el);
    if (w && w[a] === cur) return;                    // our own write
    var o = orig.get(el); if (!o) { o = {}; orig.set(el, o); }
    o[a] = cur;                                        // new original from the page
    if (mode === 'light') { var m = mapText(cur); if (m !== cur) setAttr(el, a, m); }
  }
  function doStyleEl(st) {
    if (st.id === 'theme-fixed') return;
    var cur = st.textContent;
    if (styleWritten.get(st) === cur) return;
    styleOrig.set(st, cur);
    if (mode === 'light') { var m = mapText(cur); if (m !== cur) { styleWritten.set(st, m); st.textContent = m; } }
  }
  function walk(node) {
    if (node.nodeType !== 1) return;
    if (node.tagName === 'STYLE') { doStyleEl(node); return; }
    for (var i = 0; i < ATTRS.length; i++) if (node.hasAttribute(ATTRS[i])) doAttr(node, ATTRS[i]);
    var kids = node.querySelectorAll('style,[style],[fill],[stroke],[stop-color],[flood-color]');
    for (var j = 0; j < kids.length; j++) {
      var k = kids[j];
      if (k.tagName === 'STYLE') { doStyleEl(k); continue; }
      for (var a = 0; a < ATTRS.length; a++) if (k.hasAttribute(ATTRS[a])) doAttr(k, ATTRS[a]);
    }
  }
  function applyAll() {
    busy = true;
    styleOrig.forEach(function (text, st) {
      var v = mode === 'light' ? mapText(text) : text;
      styleWritten.set(st, v); if (st.textContent !== v) st.textContent = v;
    });
    orig.forEach(function (o, el) {
      Object.keys(o).forEach(function (a) {
        var v = mode === 'light' ? mapText(o[a]) : o[a];
        if (el.getAttribute(a) !== v) setAttr(el, a, v); else { var w = written.get(el) || {}; w[a] = v; written.set(el, w); }
      });
    });
    busy = false;
  }

  function apply() {
    var next = effective();
    root.setAttribute('data-theme', next);
    root.setAttribute('data-theme-choice', choice);
    if (next !== mode) { mode = next; applyAll(); }
    updateToggle();
  }

  // ---- first pass: head styles are already parsed; hide the body until the rest is mapped
  mode = effective();
  root.setAttribute('data-theme', mode);
  root.setAttribute('data-theme-choice', choice);
  if (mode === 'light') root.classList.add('theme-pending');
  walk(document.head);

  var obs = new MutationObserver(function (list) {
    if (busy) return;
    for (var i = 0; i < list.length; i++) {
      var r = list[i];
      if (r.type === 'attributes') doAttr(r.target, r.attributeName);
      else if (r.type === 'characterData') { var p = r.target.parentNode; if (p && p.tagName === 'STYLE') doStyleEl(p); }
      else {
        for (var j = 0; j < r.addedNodes.length; j++) walk(r.addedNodes[j]);
        if (r.target.tagName === 'STYLE') doStyleEl(r.target);
      }
    }
  });
  obs.observe(root, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ATTRS });

  // ---- toggle
  var ICONS = {
    auto: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor"/></svg>',
    light: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5" fill="currentColor"/><g stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></g></svg>',
    dark: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z" fill="currentColor"/></svg>'
  };
  var LABELS = { auto: 'Auto', light: 'Light', dark: 'Dark' };
  var HINTS = { auto: 'Match my device setting', light: 'Light mode', dark: 'Dark mode' };
  var group = null;
  function updateToggle() {
    if (!group) return;
    var bs = group.querySelectorAll('button');
    for (var i = 0; i < bs.length; i++) bs[i].setAttribute('aria-pressed', String(bs[i].dataset.choice === choice));
  }
  function buildToggle() {
    group = document.createElement('div');
    group.className = 'theme-toggle theme-toggle--' + placement;
    group.setAttribute('role', 'group');
    group.setAttribute('aria-label', 'Color theme');
    CHOICES.forEach(function (c) {
      var b = document.createElement('button');
      b.type = 'button';
      b.dataset.choice = c;
      b.title = HINTS[c];
      b.innerHTML = ICONS[c] + '<span class="theme-toggle__label">' + LABELS[c] + '</span>';
      b.addEventListener('click', function (ev) {
        choice = c;
        try { localStorage.setItem(KEY, c); } catch (e) {}
        apply();
        if (ev.detail > 0) b.blur();   // mouse click: give the keys back to the slide deck
      });
      group.appendChild(b);
    });
    // Arrow/space keys pressed while the toggle has focus must not also flip slides.
    group.addEventListener('keydown', function (ev) { ev.stopPropagation(); });
    var mount = document.getElementById('theme-toggle');
    if (mount) mount.appendChild(group); else document.body.appendChild(group);
    updateToggle();
  }

  function ready() {
    walk(document.body);
    root.classList.remove('theme-pending');
    buildToggle();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready); else ready();

  if (mq) {
    var onChange = function () { if (choice === 'auto') apply(); };
    if (mq.addEventListener) mq.addEventListener('change', onChange); else if (mq.addListener) mq.addListener(onChange);
  }
  // Another tab changed the setting.
  window.addEventListener('storage', function (e) { if (e.key === KEY) { choice = stored(); apply(); } });
})();
