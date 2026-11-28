/* Touch and on-screen navigation for the lecture-note slide decks.
   Adds ‹ › buttons (bottom left) and left/right swipes. Both send the same ArrowLeft / ArrowRight
   key the deck already listens for, so each deck's own renderSlide() stays in charge.
   Vertical swipes still scroll a long slide on a phone; swipes that start on a button, input,
   slider or a sideways-scrolling box are left alone.
   Load at the end of <head>:  <script src="decknav.js?v=1" defer></script> */
(function () {
  'use strict';
  function press(key) {
    document.dispatchEvent(new KeyboardEvent('keydown', { key: key, bubbles: true, cancelable: true }));
  }

  var css = '' +
    '.deck-nav { position: fixed; left: 12px; bottom: 10px; display: flex; gap: 8px; z-index: 300; }' +
    '.deck-nav button { width: 40px; height: 34px; border-radius: 10px; border: 1px solid var(--border); background: var(--surface); color: var(--text);' +
    '  font: 700 20px/1 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; cursor: pointer; opacity: 0.75; padding: 0 0 2px; }' +
    '.deck-nav button:hover, .deck-nav button:focus-visible { opacity: 1; }' +
    '.deck-nav button:focus-visible { outline: 2px solid var(--amber); outline-offset: 2px; }' +
    '.nav-hint { left: 116px !important; }' +
    '@media (pointer: coarse), (max-width: 900px) {' +
    '  .deck-nav button { width: 48px; height: 44px; font-size: 24px; opacity: 0.9; }' +
    '  .nav-hint { display: none !important; }' +
    '}' +
    '@media print { .deck-nav { display: none; } }';

  function build() {
    if (!document.querySelector('.slide')) return;
    var st = document.createElement('style');
    st.id = 'deck-nav-style';
    st.textContent = css;
    document.head.appendChild(st);

    var nav = document.createElement('nav');
    nav.className = 'deck-nav';
    nav.setAttribute('aria-label', 'Slide navigation');
    [['ArrowLeft', '‹', 'Previous slide'], ['ArrowRight', '›', 'Next slide']].forEach(function (b) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = b[1];
      btn.setAttribute('aria-label', b[2]);
      btn.title = b[2];
      btn.addEventListener('click', function (ev) {
        press(b[0]);
        if (ev.detail > 0) btn.blur();   // tap/click: don't leave focus on the button
      });
      nav.appendChild(btn);
    });
    document.body.appendChild(nav);

    var hint = document.querySelector('.nav-hint');
    if (hint && /arrow keys/i.test(hint.textContent)) hint.textContent = 'Use the arrow keys or the ‹ › buttons to navigate';
  }

  // ---- swipe
  var x0 = null, y0 = null, t0 = 0;
  function blocked(el) {
    for (var e = el; e && e !== document.body; e = e.parentElement) {
      if (e.matches && e.matches('button, a, input, select, textarea, label, [role="slider"], [contenteditable], .deck-nav, .theme-toggle, .no-swipe')) return true;
      var cs = getComputedStyle(e);
      if ((cs.overflowX === 'auto' || cs.overflowX === 'scroll') && e.scrollWidth > e.clientWidth + 2) return true;
    }
    return false;
  }
  document.addEventListener('touchstart', function (ev) {
    if (ev.touches.length !== 1 || blocked(ev.target)) { x0 = null; return; }
    x0 = ev.touches[0].clientX; y0 = ev.touches[0].clientY; t0 = Date.now();
  }, { passive: true });
  document.addEventListener('touchend', function (ev) {
    if (x0 === null) return;
    var t = ev.changedTouches[0], dx = t.clientX - x0, dy = t.clientY - y0;
    x0 = null;
    if (Date.now() - t0 > 800) return;                         // slow drag, not a swipe
    if (Math.abs(dx) < 50 || Math.abs(dx) < 1.5 * Math.abs(dy)) return;   // mostly vertical: scrolling
    press(dx < 0 ? 'ArrowRight' : 'ArrowLeft');
  }, { passive: true });

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
