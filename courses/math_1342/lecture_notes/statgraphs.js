// Lightweight SVG chart helpers for Math 1342 lecture decks.
//
// Charts share the slate-dark palette used by the slides.
// Usage:
//   <div id="chart-1"></div>
//   <script>StatGraphs.histogram('#chart-1', [/* data */], { xLabel: 'x' });</script>

const StatGraphs = (() => {
  const SVG = 'http://www.w3.org/2000/svg';
  const COLORS = {
    bg: '#0f172a', axis: '#94a3b8', grid: '#334155', text: '#cbd5e1',
    primary: '#38bdf8', amber: '#fbbf24', green: '#34d399', rose: '#fb7185',
    purple: '#818cf8',
  };

  function el(tag, attrs = {}, kids = []) {
    const n = document.createElementNS(SVG, tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v !== undefined && v !== null) n.setAttribute(k, v);
    }
    for (const c of kids) {
      if (typeof c === 'string') n.appendChild(document.createTextNode(c));
      else if (c) n.appendChild(c);
    }
    return n;
  }

  function frame(opts = {}) {
    const W = opts.width || 460, H = opts.height || 280;
    const PL = opts.padLeft || 38, PR = opts.padRight || 14;
    const PT = opts.padTop || 14, PB = opts.padBottom || 30;
    const plotW = W - PL - PR, plotH = H - PT - PB;
    const svg = el('svg', {
      xmlns: SVG, viewBox: `0 0 ${W} ${H}`, width: W, height: H,
      style: 'background:#0f172a; border-radius:8px; max-width:100%; display:block;',
    });
    return { svg, W, H, PL, PR, PT, PB, plotW, plotH };
  }

  function axisX(svg, sx, fr, ticks, label) {
    svg.appendChild(el('line', {
      x1: fr.PL, y1: fr.PT + fr.plotH, x2: fr.PL + fr.plotW, y2: fr.PT + fr.plotH,
      stroke: COLORS.axis, 'stroke-width': 1.25,
    }));
    for (const t of ticks) {
      svg.appendChild(el('text', {
        x: sx(t), y: fr.PT + fr.plotH + 16,
        fill: COLORS.text, 'font-size': 11, 'text-anchor': 'middle',
        'font-family': 'Work Sans, sans-serif',
      }, [String(typeof t === 'number' ? roundNice(t) : t)]));
    }
    if (label) {
      svg.appendChild(el('text', {
        x: fr.PL + fr.plotW / 2, y: fr.H - 4,
        fill: COLORS.text, 'font-size': 12, 'text-anchor': 'middle',
        'font-family': 'Work Sans, sans-serif', 'font-style': 'italic',
      }, [label]));
    }
  }

  function axisY(svg, sy, fr, ticks, label) {
    svg.appendChild(el('line', {
      x1: fr.PL, y1: fr.PT, x2: fr.PL, y2: fr.PT + fr.plotH,
      stroke: COLORS.axis, 'stroke-width': 1.25,
    }));
    for (const t of ticks) {
      svg.appendChild(el('text', {
        x: fr.PL - 6, y: sy(t) + 4,
        fill: COLORS.text, 'font-size': 11, 'text-anchor': 'end',
        'font-family': 'Work Sans, sans-serif',
      }, [String(typeof t === 'number' ? roundNice(t) : t)]));
    }
    if (label) {
      svg.appendChild(el('text', {
        x: 12, y: fr.PT + fr.plotH / 2,
        fill: COLORS.text, 'font-size': 12, 'text-anchor': 'middle',
        'font-family': 'Work Sans, sans-serif', 'font-style': 'italic',
        transform: `rotate(-90 12 ${fr.PT + fr.plotH / 2})`,
      }, [label]));
    }
  }

  function roundNice(v) {
    if (Math.abs(v) < 1e-9) return 0;
    if (Math.abs(v - Math.round(v)) < 1e-6) return Math.round(v);
    return Math.round(v * 100) / 100;
  }

  function makeTicks(min, max, n = 5) {
    const span = max - min;
    const step = span / n;
    const out = [];
    for (let i = 0; i <= n; i++) out.push(min + i * step);
    return out;
  }

  function host(target) {
    return typeof target === 'string' ? document.querySelector(target) : target;
  }

  // ─── Histogram ──────────────────────────────────────────────────────
  function histogram(target, data, opts = {}) {
    const fr = frame(opts);
    const min = opts.min !== undefined ? opts.min : Math.min(...data);
    const max = opts.max !== undefined ? opts.max : Math.max(...data);
    const numBins = opts.bins || Math.max(6, Math.min(15, Math.round(Math.sqrt(data.length))));
    const binWidth = (max - min) / numBins;
    const bins = new Array(numBins).fill(0);
    for (const v of data) {
      let i = Math.floor((v - min) / binWidth);
      if (i === numBins) i = numBins - 1;
      if (i >= 0 && i < numBins) bins[i]++;
    }
    const maxCount = Math.max(...bins);
    const sx = (v) => fr.PL + ((v - min) / (max - min)) * fr.plotW;
    const sy = (c) => fr.PT + fr.plotH - (c / maxCount) * fr.plotH;
    for (let i = 0; i < numBins; i++) {
      const x = sx(min + i * binWidth);
      const w = sx(min + (i + 1) * binWidth) - x - 1;
      const y = sy(bins[i]);
      const h = fr.PT + fr.plotH - y;
      fr.svg.appendChild(el('rect', {
        x, y, width: Math.max(w, 1), height: h,
        fill: opts.color || COLORS.primary, opacity: 0.85,
      }));
    }
    axisX(fr.svg, sx, fr, makeTicks(min, max, 5), opts.xLabel);
    axisY(fr.svg, sy, fr, makeTicks(0, maxCount, Math.min(maxCount, 5)), opts.yLabel || 'Frequency');
    host(target).innerHTML = ''; host(target).appendChild(fr.svg);
  }

  // ─── Dot plot ───────────────────────────────────────────────────────
  function dotplot(target, data, opts = {}) {
    const fr = frame(Object.assign({ height: 200, padBottom: 28 }, opts));
    const min = opts.min !== undefined ? opts.min : Math.min(...data);
    const max = opts.max !== undefined ? opts.max : Math.max(...data);
    const span = Math.max(max - min, 1e-9);
    // Use unique-value stacking when discrete
    const round = (v) => Math.round(v * 1e6) / 1e6;
    const uniq = [...new Set(data.map(round))].sort((a, b) => a - b);
    let centers, counts;
    if (uniq.length <= 30) {
      centers = uniq;
      const idx = new Map();
      uniq.forEach((c, i) => idx.set(c, i));
      counts = uniq.map(() => 0);
      for (const v of data) counts[idx.get(round(v))]++;
    } else {
      const numBins = Math.max(8, Math.min(25, Math.round(Math.sqrt(data.length) * 1.5)));
      const bw = span / numBins;
      counts = new Array(numBins).fill(0);
      centers = new Array(numBins);
      for (let i = 0; i < numBins; i++) centers[i] = min + (i + 0.5) * bw;
      for (const v of data) {
        let i = Math.floor((v - min) / bw);
        if (i >= numBins) i = numBins - 1;
        if (i < 0) i = 0;
        counts[i]++;
      }
    }
    const maxCount = Math.max(...counts);
    const sx = (v) => fr.PL + ((v - min) / (max - min || 1)) * fr.plotW;
    const axisYY = fr.PT + fr.plotH;
    const dotPitch = fr.plotH / Math.max(maxCount, 6);
    const dotR = Math.max(1.2, Math.min(5, dotPitch * 0.45));
    fr.svg.appendChild(el('line', { x1: fr.PL, y1: axisYY, x2: fr.PL + fr.plotW, y2: axisYY, stroke: COLORS.axis, 'stroke-width': 1 }));
    for (let i = 0; i < centers.length; i++) {
      const cx = sx(centers[i]);
      for (let k = 0; k < counts[i]; k++) {
        const cy = axisYY - dotPitch * (k + 0.5);
        if (cy < fr.PT) break;
        fr.svg.appendChild(el('circle', { cx, cy, r: dotR, fill: opts.color || COLORS.primary, opacity: 0.92 }));
      }
    }
    for (const t of makeTicks(min, max, 5)) {
      fr.svg.appendChild(el('text', {
        x: sx(t), y: axisYY + 16, fill: COLORS.text,
        'font-size': 11, 'text-anchor': 'middle', 'font-family': 'Work Sans, sans-serif',
      }, [String(roundNice(t))]));
    }
    if (opts.xLabel) {
      fr.svg.appendChild(el('text', {
        x: fr.PL + fr.plotW / 2, y: fr.H - 4, fill: COLORS.text,
        'font-size': 12, 'text-anchor': 'middle', 'font-family': 'Work Sans, sans-serif', 'font-style': 'italic',
      }, [opts.xLabel]));
    }
    host(target).innerHTML = ''; host(target).appendChild(fr.svg);
  }

  // ─── Boxplot helpers ────────────────────────────────────────────────
  function quartiles(data) {
    const s = [...data].sort((a, b) => a - b);
    const q = (p) => {
      const idx = (s.length - 1) * p;
      const lo = Math.floor(idx), hi = Math.ceil(idx);
      return s[lo] + (s[hi] - s[lo]) * (idx - lo);
    };
    return { min: s[0], q1: q(0.25), median: q(0.5), q3: q(0.75), max: s[s.length - 1] };
  }

  function boxplot(target, data, opts = {}) {
    return boxplots(target, [data], [opts.label || ''], opts);
  }

  function boxplots(target, datasets, labels, opts = {}) {
    // Reserve enough left padding for the longest label.
    const longest = (labels || []).reduce((m, s) => Math.max(m, (s || '').length), 0);
    const autoPadLeft = Math.max(40, longest * 7 + 14);
    const fr = frame(Object.assign({ height: 220, padLeft: autoPadLeft }, opts));
    const allFlat = datasets.flat();
    const min = opts.min !== undefined ? opts.min : Math.min(...allFlat);
    const max = opts.max !== undefined ? opts.max : Math.max(...allFlat);
    const sx = (v) => fr.PL + ((v - min) / (max - min || 1)) * fr.plotW;
    const N = datasets.length;
    const slotH = fr.plotH / N;
    const boxH = Math.min(slotH * 0.55, 36);
    const palette = [COLORS.primary, COLORS.amber, COLORS.green, COLORS.purple, COLORS.rose];
    for (let i = 0; i < N; i++) {
      const stats = quartiles(datasets[i]);
      const yMid = fr.PT + slotH * (i + 0.5);
      const color = palette[i % palette.length];
      // Whiskers
      fr.svg.appendChild(el('line', { x1: sx(stats.min), y1: yMid, x2: sx(stats.q1), y2: yMid, stroke: color, 'stroke-width': 1.5 }));
      fr.svg.appendChild(el('line', { x1: sx(stats.q3), y1: yMid, x2: sx(stats.max), y2: yMid, stroke: color, 'stroke-width': 1.5 }));
      // Whisker caps
      for (const x of [stats.min, stats.max]) {
        fr.svg.appendChild(el('line', { x1: sx(x), y1: yMid - boxH * 0.4, x2: sx(x), y2: yMid + boxH * 0.4, stroke: color, 'stroke-width': 1.5 }));
      }
      // Box
      fr.svg.appendChild(el('rect', {
        x: sx(stats.q1), y: yMid - boxH / 2,
        width: sx(stats.q3) - sx(stats.q1), height: boxH,
        fill: color, opacity: 0.20, stroke: color, 'stroke-width': 1.5,
      }));
      // Median
      fr.svg.appendChild(el('line', {
        x1: sx(stats.median), y1: yMid - boxH / 2, x2: sx(stats.median), y2: yMid + boxH / 2,
        stroke: color, 'stroke-width': 2.5,
      }));
      // Label
      if (labels && labels[i]) {
        fr.svg.appendChild(el('text', {
          x: fr.PL - 6, y: yMid + 4, fill: COLORS.text,
          'font-size': 11, 'text-anchor': 'end', 'font-family': 'Work Sans, sans-serif',
        }, [labels[i]]));
      }
    }
    axisX(fr.svg, sx, fr, makeTicks(min, max, 5), opts.xLabel);
    host(target).innerHTML = ''; host(target).appendChild(fr.svg);
  }

  // ─── Scatter (with optional regression line) ─────────────────────────
  function scatter(target, xs, ys, opts = {}) {
    const fr = frame(opts);
    const xMin = opts.xMin !== undefined ? opts.xMin : Math.min(...xs);
    const xMax = opts.xMax !== undefined ? opts.xMax : Math.max(...xs);
    const yMin = opts.yMin !== undefined ? opts.yMin : Math.min(...ys);
    const yMax = opts.yMax !== undefined ? opts.yMax : Math.max(...ys);
    const padX = (xMax - xMin) * 0.06, padY = (yMax - yMin) * 0.06;
    const sx = (v) => fr.PL + ((v - (xMin - padX)) / ((xMax + padX) - (xMin - padX))) * fr.plotW;
    const sy = (v) => fr.PT + fr.plotH - ((v - (yMin - padY)) / ((yMax + padY) - (yMin - padY))) * fr.plotH;
    axisX(fr.svg, sx, fr, makeTicks(xMin, xMax, 5), opts.xLabel);
    axisY(fr.svg, sy, fr, makeTicks(yMin, yMax, 5), opts.yLabel);
    if (opts.regression) {
      // Compute least-squares line
      const n = xs.length;
      const xMean = xs.reduce((a, b) => a + b, 0) / n;
      const yMean = ys.reduce((a, b) => a + b, 0) / n;
      let num = 0, den = 0;
      for (let i = 0; i < n; i++) { num += (xs[i] - xMean) * (ys[i] - yMean); den += (xs[i] - xMean) ** 2; }
      const m = num / den, b = yMean - m * xMean;
      fr.svg.appendChild(el('line', {
        x1: sx(xMin - padX), y1: sy(m * (xMin - padX) + b),
        x2: sx(xMax + padX), y2: sy(m * (xMax + padX) + b),
        stroke: COLORS.amber, 'stroke-width': 2,
      }));
    }
    for (let i = 0; i < xs.length; i++) {
      fr.svg.appendChild(el('circle', {
        cx: sx(xs[i]), cy: sy(ys[i]), r: opts.dotR || 3.5,
        fill: opts.color || COLORS.primary, opacity: 0.9,
      }));
    }
    host(target).innerHTML = ''; host(target).appendChild(fr.svg);
  }

  // ─── Bar chart ──────────────────────────────────────────────────────
  function barChart(target, labels, values, opts = {}) {
    const fr = frame(opts);
    const max = opts.max || Math.max(...values);
    const sy = (v) => fr.PT + fr.plotH - (v / max) * fr.plotH;
    const slotW = fr.plotW / labels.length;
    const barW = slotW * 0.7;
    const palette = [COLORS.primary, COLORS.amber, COLORS.green, COLORS.purple, COLORS.rose];
    for (let i = 0; i < labels.length; i++) {
      const cx = fr.PL + slotW * (i + 0.5);
      const x = cx - barW / 2;
      const y = sy(values[i]);
      const h = fr.PT + fr.plotH - y;
      fr.svg.appendChild(el('rect', {
        x, y, width: barW, height: h,
        fill: opts.color || palette[i % palette.length], opacity: 0.85,
      }));
      fr.svg.appendChild(el('text', {
        x: cx, y: fr.PT + fr.plotH + 16, fill: COLORS.text,
        'font-size': 11, 'text-anchor': 'middle', 'font-family': 'Work Sans, sans-serif',
      }, [labels[i]]));
      // Value label on top of bar
      fr.svg.appendChild(el('text', {
        x: cx, y: y - 4, fill: COLORS.text,
        'font-size': 11, 'text-anchor': 'middle', 'font-family': 'Work Sans, sans-serif',
      }, [String(values[i])]));
    }
    fr.svg.appendChild(el('line', {
      x1: fr.PL, y1: fr.PT + fr.plotH, x2: fr.PL + fr.plotW, y2: fr.PT + fr.plotH,
      stroke: COLORS.axis, 'stroke-width': 1.25,
    }));
    if (opts.yLabel) {
      axisY(fr.svg, sy, fr, makeTicks(0, max, Math.min(max, 5)), opts.yLabel);
    }
    host(target).innerHTML = ''; host(target).appendChild(fr.svg);
  }

  // ─── Normal curve (with optional shading) ────────────────────────────
  function normalCurve(target, opts = {}) {
    const mean = opts.mean !== undefined ? opts.mean : 0;
    const sd = opts.sd !== undefined ? opts.sd : 1;
    const xMin = opts.xMin !== undefined ? opts.xMin : mean - 4 * sd;
    const xMax = opts.xMax !== undefined ? opts.xMax : mean + 4 * sd;
    const fr = frame(Object.assign({ height: 240 }, opts));
    const pdf = (x) => Math.exp(-((x - mean) ** 2) / (2 * sd * sd)) / (sd * Math.sqrt(2 * Math.PI));
    const yMax = pdf(mean) * 1.05;
    const sx = (v) => fr.PL + ((v - xMin) / (xMax - xMin)) * fr.plotW;
    const sy = (v) => fr.PT + fr.plotH - (v / yMax) * fr.plotH;

    // Shading regions (array of {from, to, color})
    if (opts.shade) {
      for (const region of opts.shade) {
        const a = Math.max(region.from ?? xMin, xMin);
        const b = Math.min(region.to ?? xMax, xMax);
        let path = `M ${sx(a)} ${sy(0)}`;
        const steps = 40;
        for (let i = 0; i <= steps; i++) {
          const x = a + ((b - a) * i) / steps;
          path += ` L ${sx(x)} ${sy(pdf(x))}`;
        }
        path += ` L ${sx(b)} ${sy(0)} Z`;
        fr.svg.appendChild(el('path', {
          d: path, fill: region.color || COLORS.amber, opacity: 0.35,
        }));
      }
    }

    // Curve
    let path = '';
    const N = 200;
    for (let i = 0; i <= N; i++) {
      const x = xMin + ((xMax - xMin) * i) / N;
      path += (i === 0 ? 'M' : ' L') + sx(x) + ',' + sy(pdf(x));
    }
    fr.svg.appendChild(el('path', {
      d: path, fill: 'none', stroke: opts.color || COLORS.primary, 'stroke-width': 2,
    }));

    // Vertical markers
    if (opts.markers) {
      for (const m of opts.markers) {
        fr.svg.appendChild(el('line', {
          x1: sx(m.x), y1: sy(0), x2: sx(m.x), y2: sy(pdf(m.x)),
          stroke: m.color || COLORS.amber, 'stroke-width': 2, 'stroke-dasharray': '4 3',
        }));
        if (m.label) {
          fr.svg.appendChild(el('text', {
            x: sx(m.x), y: fr.PT + 14, fill: m.color || COLORS.amber,
            'font-size': 11, 'text-anchor': 'middle', 'font-family': 'Work Sans, sans-serif',
          }, [m.label]));
        }
      }
    }

    // X axis with mean and ±1, ±2, ±3 SD ticks
    const ticks = [];
    for (let k = -3; k <= 3; k++) ticks.push(mean + k * sd);
    axisX(fr.svg, sx, fr, ticks, opts.xLabel);
    host(target).innerHTML = ''; host(target).appendChild(fr.svg);
  }

  // ─── Generic line/point chart for sampling distributions etc. ────────
  // Wrapper: feed it a list of {points: [[x,y]...]} or {fn: x=>y} curves.
  function lineChart(target, opts) {
    const fr = frame(opts);
    const xMin = opts.xMin, xMax = opts.xMax, yMin = opts.yMin, yMax = opts.yMax;
    const sx = (v) => fr.PL + ((v - xMin) / (xMax - xMin)) * fr.plotW;
    const sy = (v) => fr.PT + fr.plotH - ((v - yMin) / (yMax - yMin)) * fr.plotH;
    axisX(fr.svg, sx, fr, makeTicks(xMin, xMax, 5), opts.xLabel);
    axisY(fr.svg, sy, fr, makeTicks(yMin, yMax, 5), opts.yLabel);
    for (const c of opts.curves || []) {
      let path = '';
      if (c.points) {
        c.points.forEach(([x, y], i) => path += (i === 0 ? 'M' : ' L') + sx(x) + ',' + sy(y));
      } else if (c.fn) {
        const N = 200;
        for (let i = 0; i <= N; i++) {
          const x = xMin + ((xMax - xMin) * i) / N;
          const y = c.fn(x);
          if (isFinite(y)) path += (path === '' ? 'M' : ' L') + sx(x) + ',' + sy(y);
        }
      }
      fr.svg.appendChild(el('path', {
        d: path, fill: 'none', stroke: c.color || COLORS.primary, 'stroke-width': 2,
        'stroke-dasharray': c.dashed ? '4 3' : null,
      }));
    }
    host(target).innerHTML = ''; host(target).appendChild(fr.svg);
  }

  return { histogram, dotplot, boxplot, boxplots, scatter, barChart, normalCurve, lineChart };
})();
