// Click-to-zoom for slide images.
// Usage: <img class="zoomable" src="small.jpg" data-zoom-src="large.jpg" alt="..."> and <script src="zoom.js"></script>
// First click opens a full-screen view (fit to screen). Clicking the image there toggles full size, which you
// can scroll around. Esc, the close button, or a click on the dark background closes it. While it is open,
// keys are kept away from the deck so the arrow keys don't change slides.
(() => {
  const css = `
    img.zoomable { cursor: zoom-in; }
    .zoom-overlay { position: fixed; inset: 0; z-index: 1000; background: rgba(2, 6, 23, 0.92); display: none;
      overflow: auto; padding: 48px 24px 56px; }
    .zoom-overlay.open { display: block; }
    .zoom-overlay .zoom-stage { min-height: 100%; display: flex; align-items: center; justify-content: center; }
    .zoom-overlay img { display: block; max-width: 96vw; max-height: calc(100vh - 120px); object-fit: contain;
      background: #fff; border-radius: 6px; cursor: zoom-in; }
    .zoom-overlay.full .zoom-stage { display: block; }
    .zoom-overlay.full img { max-width: none; max-height: none; cursor: zoom-out; margin: 0 auto; }
    .zoom-overlay .zoom-close { position: fixed; top: 12px; right: 18px; font: 600 28px/1 Inter, sans-serif; color: #f1f5f9;
      background: rgba(30, 41, 59, 0.9); border: 1px solid #475569; border-radius: 8px; width: 40px; height: 40px; cursor: pointer; }
    .zoom-overlay .zoom-caption { position: fixed; left: 0; right: 0; bottom: 0; padding: 10px 20px; font: 14px/1.4 Inter, sans-serif;
      color: #cbd5e1; background: rgba(2, 6, 23, 0.85); text-align: center; }`;
  const style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  const overlay = document.createElement('div');
  overlay.className = 'zoom-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.innerHTML = '<button class="zoom-close" aria-label="Close zoomed image">&times;</button>' +
    '<div class="zoom-stage"><img alt=""></div><div class="zoom-caption"></div>';
  const big = overlay.querySelector('img');
  const caption = overlay.querySelector('.zoom-caption');
  const closeBtn = overlay.querySelector('.zoom-close');

  function open(img) {
    big.src = img.dataset.zoomSrc || img.src;
    big.alt = img.alt;
    caption.textContent = (img.alt ? img.alt + ' — ' : '') + 'Click the image to see full size. Esc to close.';
    overlay.classList.remove('full');
    overlay.classList.add('open');
    overlay.scrollTop = 0;
    closeBtn.focus();
  }
  function close() { overlay.classList.remove('open', 'full'); }

  big.addEventListener('click', (e) => { e.stopPropagation(); overlay.classList.toggle('full'); });
  closeBtn.addEventListener('click', (e) => { e.stopPropagation(); close(); });
  overlay.addEventListener('click', close);
  // Capture phase, so the deck's own arrow-key listener never sees keys while the image is open.
  document.addEventListener('keydown', (e) => {
    if (!overlay.classList.contains('open')) return;
    e.stopImmediatePropagation();
    if (e.key === 'Escape') { e.preventDefault(); close(); }
  }, true);

  function init() {
    document.body.appendChild(overlay);
    document.querySelectorAll('img.zoomable').forEach((img) => {
      img.setAttribute('tabindex', '0');
      img.setAttribute('title', 'Click to zoom');
      img.addEventListener('click', () => open(img));
      img.addEventListener('keydown', (e) => { if (e.key === 'Enter') open(img); });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
