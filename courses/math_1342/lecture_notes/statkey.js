// StatKey-style randomization & bootstrap simulator for Math 1342 lectures.
//
// Usage:
//   <div id="sim1"></div>
//   <script>StatKey.create('#sim1', { mode: 'one-prop-rand', n: 40, x: 24, p0: 0.5,
//                                       direction: 'two-tailed', label: 'Coin flip test' });</script>
//
// Modes:
//   'one-prop-rand'    Randomization test for a single proportion.
//                      Inputs: n, x (observed count), p0 (null proportion), direction.
//   'one-prop-boot'    Bootstrap CI for a single proportion.
//                      Inputs: n, x (observed count).
//   'two-prop-rand'    Randomization test for difference of two proportions.
//                      Inputs: n1, x1, n2, x2, direction.
//
// Each panel includes: input boxes, "Generate One" (single trial), "Run 1000",
// "Reset", running list of simulated stats, histogram, and a p-value or CI readout.

const StatKey = (() => {
  const SVG_NS = 'http://www.w3.org/2000/svg';

  function el(tag, attrs = {}, kids = []) {
    const node = document.createElementNS(SVG_NS, tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v !== undefined && v !== null) node.setAttribute(k, v);
    }
    for (const c of kids) {
      if (typeof c === 'string') node.appendChild(document.createTextNode(c));
      else if (c) node.appendChild(c);
    }
    return node;
  }

  function html(tag, props = {}, kids = []) {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(props)) {
      if (k === 'class') n.className = v;
      else if (k === 'style') n.style.cssText = v;
      else if (k.startsWith('on')) n.addEventListener(k.slice(2).toLowerCase(), v);
      else if (k === 'value') n.value = v;
      else n.setAttribute(k, v);
    }
    for (const c of kids) {
      if (typeof c === 'string') n.appendChild(document.createTextNode(c));
      else if (c) n.appendChild(c);
    }
    return n;
  }

  // ── Simulation core ─────────────────────────────────────────────────
  function bernoulliCount(n, p) {
    let k = 0;
    for (let i = 0; i < n; i++) if (Math.random() < p) k++;
    return k;
  }

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function simulateOnce(opts) {
    const m = opts.mode;
    if (m === 'one-prop-rand') {
      // Under H0: each draw is Bernoulli(p0). Stat: sample proportion = k / n.
      const k = bernoulliCount(opts.n, opts.p0);
      return k / opts.n;
    }
    if (m === 'one-prop-boot') {
      // Bootstrap from the observed sample (proportion x/n).
      const phat = opts.x / opts.n;
      const k = bernoulliCount(opts.n, phat);
      return k / opts.n;
    }
    if (m === 'two-prop-rand') {
      // Pool both groups, then redistribute. Stat: p1 - p2.
      const total = opts.x1 + opts.x2;
      const N = opts.n1 + opts.n2;
      // Build pool: total successes (=1), N - total failures (=0)
      const pool = new Array(N);
      for (let i = 0; i < N; i++) pool[i] = i < total ? 1 : 0;
      shuffle(pool);
      let s1 = 0, s2 = 0;
      for (let i = 0; i < opts.n1; i++) s1 += pool[i];
      for (let i = opts.n1; i < N; i++) s2 += pool[i];
      return s1 / opts.n1 - s2 / opts.n2;
    }
    return NaN;
  }

  // ── Histogram ───────────────────────────────────────────────────────
  function drawHistogram(svgHost, samples, opts) {
    if (!samples.length) {
      svgHost.innerHTML = '<div style="color:#94a3b8; font-size:13px; padding:18px; text-align:center;">No simulations yet. Click <b>Generate One</b> or <b>Run 1000</b> to begin.</div>';
      return;
    }
    const W = 460, H = 220;
    const PL = 38, PR = 12, PT = 10, PB = 28;
    const plotW = W - PL - PR;
    const plotH = H - PT - PB;

    // Determine bins
    const min = Math.min(...samples);
    const max = Math.max(...samples);
    const span = Math.max(max - min, 1e-9);
    const desired = Math.min(40, Math.max(8, Math.round(Math.sqrt(samples.length))));
    const binWidth = span / desired || 0.01;
    const xMin = min - binWidth / 2;
    const xMax = max + binWidth / 2;
    const numBins = Math.ceil((xMax - xMin) / binWidth);
    const bins = new Array(numBins).fill(0);
    for (const v of samples) {
      let i = Math.floor((v - xMin) / binWidth);
      if (i >= numBins) i = numBins - 1;
      if (i < 0) i = 0;
      bins[i]++;
    }
    const maxCount = Math.max(...bins);

    const sx = (x) => PL + ((x - xMin) / (xMax - xMin)) * plotW;
    const sy = (y) => PT + plotH - (y / maxCount) * plotH;

    const svg = el('svg', {
      xmlns: SVG_NS, viewBox: `0 0 ${W} ${H}`, width: W, height: H,
      style: 'background:#0f172a; border-radius:6px; max-width:100%;',
    });

    // Axis line
    svg.appendChild(el('line', {
      x1: PL, y1: PT + plotH, x2: PL + plotW, y2: PT + plotH,
      stroke: '#94a3b8', 'stroke-width': 1,
    }));

    // Bars: highlight bars beyond observed (for p-value visualization)
    const obs = opts.observed;
    const dir = opts.direction || 'two-tailed';
    const obsAbsDist = obs !== undefined ? Math.abs(obs - opts.center) : null;
    for (let i = 0; i < numBins; i++) {
      const v = xMin + (i + 0.5) * binWidth;
      let highlighted = false;
      if (obs !== undefined) {
        if (dir === 'right') highlighted = v >= obs;
        else if (dir === 'left') highlighted = v <= obs;
        else if (dir === 'two-tailed') highlighted = Math.abs(v - opts.center) >= obsAbsDist - 1e-9;
      }
      const x = sx(xMin + i * binWidth);
      const w = sx(xMin + (i + 1) * binWidth) - x - 1;
      const y = sy(bins[i]);
      const h = PT + plotH - y;
      svg.appendChild(el('rect', {
        x: x, y: y, width: Math.max(w, 1), height: h,
        fill: highlighted ? '#fb7185' : '#38bdf8',
        opacity: 0.85,
      }));
    }

    // Tick labels (just min, mid, max)
    const ticks = [xMin, (xMin + xMax) / 2, xMax];
    for (const t of ticks) {
      svg.appendChild(el('text', {
        x: sx(t), y: PT + plotH + 16,
        fill: '#cbd5e1', 'font-size': 11, 'text-anchor': 'middle',
        'font-family': 'Work Sans, sans-serif',
      }, [String(Math.round(t * 1000) / 1000)]));
    }

    // Observed marker (gold vertical line)
    if (obs !== undefined && obs >= xMin && obs <= xMax) {
      const xObs = sx(obs);
      svg.appendChild(el('line', {
        x1: xObs, y1: PT, x2: xObs, y2: PT + plotH,
        stroke: '#fbbf24', 'stroke-width': 2, 'stroke-dasharray': '4 3',
      }));
      svg.appendChild(el('text', {
        x: xObs, y: PT + 14,
        fill: '#fbbf24', 'font-size': 11, 'text-anchor': 'middle',
        'font-family': 'Work Sans, sans-serif',
      }, ['observed']));
    }

    svgHost.innerHTML = '';
    svgHost.appendChild(svg);
  }

  // ── Stats: p-value and percentiles ──────────────────────────────────
  function pValue(samples, observed, direction, center) {
    if (!samples.length) return null;
    const N = samples.length;
    if (direction === 'right') {
      let c = 0;
      for (const v of samples) if (v >= observed - 1e-12) c++;
      return c / N;
    }
    if (direction === 'left') {
      let c = 0;
      for (const v of samples) if (v <= observed + 1e-12) c++;
      return c / N;
    }
    // two-tailed
    const dist = Math.abs(observed - center);
    let c = 0;
    for (const v of samples) if (Math.abs(v - center) >= dist - 1e-12) c++;
    return c / N;
  }

  function percentile(samples, p) {
    const sorted = [...samples].sort((a, b) => a - b);
    const idx = (sorted.length - 1) * p;
    const lo = Math.floor(idx), hi = Math.ceil(idx);
    if (lo === hi) return sorted[lo];
    return sorted[lo] + (sorted[hi] - sorted[lo]) * (idx - lo);
  }

  // ── UI assembly ─────────────────────────────────────────────────────
  function modeMeta(mode) {
    if (mode === 'one-prop-rand') return {
      title: 'Randomization Test — One Proportion',
      stat: 'âsample proportion p̂',
      summary: (opts) => {
        const phat = opts.x / opts.n;
        return [
          `Observed: <b>${opts.x}/${opts.n} = ${phat.toFixed(3)}</b>`,
          `Null: <b>p = ${opts.p0}</b>`,
          `Direction: <b>${opts.direction}</b>`,
        ];
      },
      observed: (opts) => opts.x / opts.n,
      center: (opts) => opts.p0,
    };
    if (mode === 'one-prop-boot') return {
      title: 'Bootstrap Distribution — One Proportion',
      stat: 'sample proportion p̂',
      summary: (opts) => {
        const phat = opts.x / opts.n;
        return [
          `Original sample: <b>${opts.x}/${opts.n} = ${phat.toFixed(3)}</b>`,
          'Each bootstrap sample resamples <i>n</i> values with replacement.',
        ];
      },
      observed: (opts) => opts.x / opts.n,
      center: (opts) => opts.x / opts.n,
    };
    if (mode === 'two-prop-rand') return {
      title: 'Randomization Test — Difference of Two Proportions',
      stat: 'p̂₁ − p̂₂',
      summary: (opts) => {
        const p1 = opts.x1 / opts.n1, p2 = opts.x2 / opts.n2;
        return [
          `Group 1: <b>${opts.x1}/${opts.n1} = ${p1.toFixed(3)}</b>`,
          `Group 2: <b>${opts.x2}/${opts.n2} = ${p2.toFixed(3)}</b>`,
          `Difference: <b>${(p1 - p2).toFixed(3)}</b>`,
          `Direction: <b>${opts.direction}</b>`,
        ];
      },
      observed: (opts) => opts.x1 / opts.n1 - opts.x2 / opts.n2,
      center: () => 0,
    };
    return null;
  }

  function create(target, opts) {
    const host = typeof target === 'string' ? document.querySelector(target) : target;
    if (!host) return;
    const meta = modeMeta(opts.mode);
    if (!meta) {
      host.textContent = `[StatKey: unknown mode "${opts.mode}"]`;
      return;
    }

    const samples = [];

    // Layout
    const card = html('div', { style: 'background:#1e293b; border:1px solid #475569; border-radius:12px; padding:18px; color:#f1f5f9; font-family:Work Sans,sans-serif; margin:14px 0; max-width:520px;' });
    const heading = html('div', { style: 'font-weight:700; color:#38bdf8; font-size:13px; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:8px;' }, [meta.title]);
    const summaryDiv = html('div', { style: 'color:#cbd5e1; font-size:14px; line-height:1.55; margin-bottom:10px;' });
    const summaryLines = meta.summary(opts);
    summaryDiv.innerHTML = summaryLines.join(' &nbsp;·&nbsp; ');
    const buttonRow = html('div', { style: 'display:flex; gap:8px; flex-wrap:wrap; margin-bottom:10px;' });
    const btnStyle = 'padding:6px 14px; border:1px solid #475569; background:rgba(56,189,248,0.15); color:#38bdf8; font-weight:600; font-size:13px; border-radius:6px; cursor:pointer; font-family:inherit;';
    const btnOne = html('button', { style: btnStyle }, ['Generate One']);
    const btnMany = html('button', { style: btnStyle }, ['Run 1000']);
    const btnReset = html('button', { style: btnStyle.replace('rgba(56,189,248,0.15)', 'rgba(251,113,133,0.15)').replace('#38bdf8', '#fb7185') }, ['Reset']);
    buttonRow.appendChild(btnOne);
    buttonRow.appendChild(btnMany);
    buttonRow.appendChild(btnReset);
    const histDiv = html('div', { style: 'min-height:220px; margin-bottom:10px;' });
    const readoutDiv = html('div', { style: 'color:#cbd5e1; font-size:14px; line-height:1.6;' });
    card.appendChild(heading);
    card.appendChild(summaryDiv);
    card.appendChild(buttonRow);
    card.appendChild(histDiv);
    card.appendChild(readoutDiv);
    host.innerHTML = '';
    host.appendChild(card);

    function refresh() {
      const observed = meta.observed(opts);
      const center = meta.center(opts);
      drawHistogram(histDiv, samples, {
        observed, center, direction: opts.direction || 'two-tailed',
      });
      const lines = [];
      lines.push(`<b>Simulations:</b> ${samples.length}`);
      if (samples.length >= 5) {
        const mean = samples.reduce((a, b) => a + b, 0) / samples.length;
        const sd = Math.sqrt(samples.reduce((a, b) => a + (b - mean) ** 2, 0) / Math.max(samples.length - 1, 1));
        lines.push(`<b>Sim mean:</b> ${mean.toFixed(3)} &nbsp; <b>Sim SD:</b> ${sd.toFixed(3)}`);
      }
      if (opts.mode === 'one-prop-boot' && samples.length >= 50) {
        const lo = percentile(samples, 0.025);
        const hi = percentile(samples, 0.975);
        lines.push(`<b>95% bootstrap CI:</b> (${lo.toFixed(3)}, ${hi.toFixed(3)})`);
      }
      if (opts.mode !== 'one-prop-boot' && samples.length >= 5) {
        const dir = opts.direction || 'two-tailed';
        const p = pValue(samples, observed, dir, center);
        lines.push(`<b>Estimated p-value:</b> ${p.toFixed(3)} &nbsp; <span style="color:#94a3b8;">(proportion of simulated values <i>${dir === 'right' ? '≥ observed' : dir === 'left' ? '≤ observed' : 'as far from null as observed'}</i>)</span>`);
      }
      readoutDiv.innerHTML = lines.join('<br>');
    }

    btnOne.addEventListener('click', () => {
      samples.push(simulateOnce(opts));
      refresh();
    });
    btnMany.addEventListener('click', () => {
      for (let i = 0; i < 1000; i++) samples.push(simulateOnce(opts));
      refresh();
    });
    btnReset.addEventListener('click', () => {
      samples.length = 0;
      refresh();
    });

    refresh();
  }

  return { create };
})();
