// Small SVG plotter for Math 1314 lecture notes.
//
// Usage: place a target element such as <div class="plot" data-config="..."></div>
// and call Lvplot.renderAll() once on DOMContentLoaded, OR call
// Lvplot.draw(target, opts) directly with a JS opts object.
//
// opts:
//   width, height          (px)               default 360 x 280
//   xMin, xMax, yMin, yMax (math coords)      default -5..5
//   xStep, yStep           grid spacing       default 1
//   xLabel, yLabel         axis labels        default "x", "y"
//   showGrid               default true
//   showAxes               default true
//   curves: [
//     { fn: x => ..., from?, to?, color?, dashed?, samples? }     // explicit y = f(x)
//     { param: t => [x,y], from, to, color?, dashed?, samples? }  // parametric
//     { points: [[x,y], ...], color?, dashed? }                   // polyline
//   ]
//   points:  [{ x, y, label?, color? }, ...]                      // labeled points
//   asymptotes: [{ x?, y?, dashed? }]                             // vertical/horizontal asymptote lines

const Lvplot = (() => {
  const SVG_NS = 'http://www.w3.org/2000/svg';

  const COLORS = {
    grid:       '#334155',
    gridMajor:  '#475569',
    axis:       '#94a3b8',
    text:       '#cbd5e1',
    curve:      '#38bdf8',
    curveAlt:   '#fbbf24',
    point:      '#fb7185',
  };

  function el(tag, attrs = {}, children = []) {
    const node = document.createElementNS(SVG_NS, tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v !== undefined && v !== null) node.setAttribute(k, v);
    }
    for (const c of children) {
      if (typeof c === 'string') node.appendChild(document.createTextNode(c));
      else if (c) node.appendChild(c);
    }
    return node;
  }

  function draw(target, opts) {
    if (typeof target === 'string') target = document.querySelector(target);
    if (!target) return null;

    const o = Object.assign({
      width: 360, height: 280,
      xMin: -5, xMax: 5, yMin: -5, yMax: 5,
      xStep: 1, yStep: 1,
      xLabel: 'x', yLabel: 'y',
      showGrid: true, showAxes: true,
      curves: [], points: [], asymptotes: [],
      pad: { left: 30, right: 14, top: 14, bottom: 26 },
    }, opts);

    const W = o.width, H = o.height;
    const PL = o.pad.left, PR = o.pad.right, PT = o.pad.top, PB = o.pad.bottom;
    const plotW = W - PL - PR;
    const plotH = H - PT - PB;
    const xRange = o.xMax - o.xMin;
    const yRange = o.yMax - o.yMin;

    const sx = (x) => PL + ((x - o.xMin) / xRange) * plotW;
    const sy = (y) => PT + (1 - (y - o.yMin) / yRange) * plotH;

    const svg = el('svg', {
      xmlns: SVG_NS,
      viewBox: `0 0 ${W} ${H}`,
      width: W, height: H,
      class: 'lvplot',
    });

    // Background
    svg.appendChild(el('rect', {
      x: 0, y: 0, width: W, height: H, fill: '#0f172a', rx: 8,
    }));

    // Grid
    if (o.showGrid) {
      const gGrid = el('g', { stroke: COLORS.grid, 'stroke-width': 1, opacity: 0.55 });
      // vertical lines
      for (let x = Math.ceil(o.xMin / o.xStep) * o.xStep; x <= o.xMax + 1e-9; x += o.xStep) {
        gGrid.appendChild(el('line', { x1: sx(x), y1: sy(o.yMin), x2: sx(x), y2: sy(o.yMax) }));
      }
      // horizontal lines
      for (let y = Math.ceil(o.yMin / o.yStep) * o.yStep; y <= o.yMax + 1e-9; y += o.yStep) {
        gGrid.appendChild(el('line', { x1: sx(o.xMin), y1: sy(y), x2: sx(o.xMax), y2: sy(y) }));
      }
      svg.appendChild(gGrid);
    }

    // Axes (drawn at math 0 if visible, else at edges)
    if (o.showAxes) {
      const axisX = (o.yMin <= 0 && o.yMax >= 0) ? 0 : o.yMin;
      const axisY = (o.xMin <= 0 && o.xMax >= 0) ? 0 : o.xMin;
      svg.appendChild(el('line', {
        x1: sx(o.xMin), y1: sy(axisX), x2: sx(o.xMax), y2: sy(axisX),
        stroke: COLORS.axis, 'stroke-width': 1.5,
      }));
      svg.appendChild(el('line', {
        x1: sx(axisY), y1: sy(o.yMin), x2: sx(axisY), y2: sy(o.yMax),
        stroke: COLORS.axis, 'stroke-width': 1.5,
      }));
      // Tick labels: a few values
      const xTickStep = o.xStep * Math.max(1, Math.round(xRange / o.xStep / 8));
      const yTickStep = o.yStep * Math.max(1, Math.round(yRange / o.yStep / 6));
      for (let x = Math.ceil(o.xMin / xTickStep) * xTickStep; x <= o.xMax + 1e-9; x += xTickStep) {
        if (Math.abs(x) < 1e-9) continue;
        svg.appendChild(el('text', {
          x: sx(x), y: sy(axisX) + 14,
          fill: COLORS.text, 'text-anchor': 'middle',
          'font-size': 11, 'font-family': 'Work Sans, sans-serif',
        }, [String(roundNice(x))]));
      }
      for (let y = Math.ceil(o.yMin / yTickStep) * yTickStep; y <= o.yMax + 1e-9; y += yTickStep) {
        if (Math.abs(y) < 1e-9) continue;
        svg.appendChild(el('text', {
          x: sx(axisY) - 6, y: sy(y) + 4,
          fill: COLORS.text, 'text-anchor': 'end',
          'font-size': 11, 'font-family': 'Work Sans, sans-serif',
        }, [String(roundNice(y))]));
      }
      // Origin label "0"
      if (o.xMin <= 0 && o.xMax >= 0 && o.yMin <= 0 && o.yMax >= 0) {
        svg.appendChild(el('text', {
          x: sx(0) - 6, y: sy(0) + 14,
          fill: COLORS.text, 'text-anchor': 'end',
          'font-size': 11, 'font-family': 'Work Sans, sans-serif',
        }, ['0']));
      }
      // Axis labels
      svg.appendChild(el('text', {
        x: W - 4, y: sy(axisX) - 4,
        fill: COLORS.text, 'text-anchor': 'end',
        'font-size': 12, 'font-style': 'italic', 'font-family': 'Work Sans, sans-serif',
      }, [o.xLabel]));
      svg.appendChild(el('text', {
        x: sx(axisY) + 6, y: PT + 10,
        fill: COLORS.text, 'text-anchor': 'start',
        'font-size': 12, 'font-style': 'italic', 'font-family': 'Work Sans, sans-serif',
      }, [o.yLabel]));
    }

    // Asymptotes
    for (const a of (o.asymptotes || [])) {
      const dash = a.dashed === false ? null : '4 4';
      if (a.x !== undefined) {
        svg.appendChild(el('line', {
          x1: sx(a.x), y1: sy(o.yMin), x2: sx(a.x), y2: sy(o.yMax),
          stroke: a.color || '#fb7185', 'stroke-width': 1.2,
          'stroke-dasharray': dash, opacity: 0.85,
        }));
      } else if (a.y !== undefined) {
        svg.appendChild(el('line', {
          x1: sx(o.xMin), y1: sy(a.y), x2: sx(o.xMax), y2: sy(a.y),
          stroke: a.color || '#fb7185', 'stroke-width': 1.2,
          'stroke-dasharray': dash, opacity: 0.85,
        }));
      }
    }

    // Curves
    for (const c of o.curves) {
      const color = c.color || COLORS.curve;
      const dash = c.dashed ? '5 4' : null;
      let pathData = '';
      if (c.points) {
        for (let i = 0; i < c.points.length; i++) {
          const [x, y] = c.points[i];
          pathData += (i === 0 ? 'M' : ' L') + sx(x) + ',' + sy(y);
        }
      } else if (c.fn) {
        const samples = c.samples || 200;
        const from = c.from !== undefined ? c.from : o.xMin;
        const to = c.to !== undefined ? c.to : o.xMax;
        let started = false;
        let lastY = null;
        for (let i = 0; i <= samples; i++) {
          const x = from + (to - from) * (i / samples);
          let y;
          try { y = c.fn(x); } catch (_) { y = NaN; }
          if (!isFinite(y) || y > o.yMax * 5 || y < o.yMin * 5) {
            started = false; lastY = null; continue;
          }
          if (lastY !== null && Math.abs(y - lastY) > yRange * 0.9) {
            started = false; lastY = null;
          }
          pathData += (started ? ' L' : 'M') + sx(x) + ',' + sy(y);
          started = true;
          lastY = y;
        }
      } else if (c.param) {
        const samples = c.samples || 200;
        const from = c.from, to = c.to;
        for (let i = 0; i <= samples; i++) {
          const t = from + (to - from) * (i / samples);
          const [x, y] = c.param(t);
          pathData += (i === 0 ? 'M' : ' L') + sx(x) + ',' + sy(y);
        }
      }
      if (pathData) {
        svg.appendChild(el('path', {
          d: pathData, fill: 'none', stroke: color, 'stroke-width': 2.2,
          'stroke-dasharray': dash, 'stroke-linejoin': 'round', 'stroke-linecap': 'round',
        }));
      }
    }

    // Points
    for (const p of (o.points || [])) {
      svg.appendChild(el('circle', {
        cx: sx(p.x), cy: sy(p.y), r: p.r || 4,
        fill: p.color || COLORS.point, stroke: '#0f172a', 'stroke-width': 1.5,
      }));
      if (p.label) {
        svg.appendChild(el('text', {
          x: sx(p.x) + (p.dx || 6),
          y: sy(p.y) + (p.dy || -6),
          fill: COLORS.text,
          'font-size': 11,
          'font-family': 'Work Sans, sans-serif',
        }, [p.label]));
      }
    }

    target.innerHTML = '';
    target.appendChild(svg);
    return svg;
  }

  function roundNice(v) {
    if (Math.abs(v) < 1e-9) return 0;
    if (Math.abs(v - Math.round(v)) < 1e-6) return Math.round(v);
    return Math.round(v * 100) / 100;
  }

  function renderAll(root = document) {
    for (const node of root.querySelectorAll('[data-plot]')) {
      try {
        const opts = parseDataPlot(node.getAttribute('data-plot'));
        draw(node, opts);
      } catch (err) {
        console.error('Lvplot render error:', err, node);
      }
    }
  }

  // Allow data-plot attribute to be JSON OR contain function strings
  // (we eval functions from "fn" strings like "x => x*x").
  function parseDataPlot(raw) {
    const cfg = JSON.parse(raw);
    if (cfg.curves) cfg.curves = cfg.curves.map(reviveCurve);
    return cfg;
  }
  function reviveCurve(c) {
    const out = Object.assign({}, c);
    if (typeof c.fn === 'string')   out.fn   = new Function('x', 'return (' + c.fn + ');');
    if (typeof c.param === 'string') out.param = new Function('t', 'return (' + c.param + ');');
    return out;
  }

  return { draw, renderAll };
})();

document.addEventListener('DOMContentLoaded', () => Lvplot.renderAll());
