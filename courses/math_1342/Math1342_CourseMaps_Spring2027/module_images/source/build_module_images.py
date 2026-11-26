# -*- coding: utf-8 -*-
"""Draw one square statistics image per Week module (Math 1342, Spring 2027) and render it to PNG.

Standard library only. Each week is an inline SVG (800x800); headless Chrome screenshots it to ../WeekNN.png.
Simulated data uses fixed seeds, so rebuilding gives identical images.
Run:  /usr/bin/python3 build_module_images.py
"""
import math
import re
import os
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
HTML_DIR = os.path.join(HERE, "html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W = H = 800
BG = "#f6f4ee"
INK = "#191919"
MUTED = "#8a8a8a"
GRID = "#d9d6cc"
BLUE = "#257de0"
ORANGE = "#f47230"
AQUA = "#00b894"
PALE = "#b9c7d8"   # unhighlighted marks
FONT = "Arial, 'Helvetica Neue', Helvetica, sans-serif"

# Plot area shared by most weeks
X0, X1, Y0, Y1 = 90, 710, 120, 610


# ---------- helpers ----------
def svg(body, caption):
    plain = re.sub(r"&[a-z]+;", "x", caption)
    size = min(58, int(700 / (0.56 * len(plain))))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{BG}"/>{body}'
            f'<text x="{W/2}" y="725" text-anchor="middle" font-family="{FONT}" font-size="{size}" '
            f'font-weight="700" fill="{INK}">{caption}</text></svg>')


def axis(y=Y1, x0=X0, x1=X1):
    return f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'


def yaxis(x=X0, y0=Y0, y1=Y1):
    return f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'


def dot(x, y, r, fill, ring=True):
    s = f' stroke="{BG}" stroke-width="2"' if ring else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{s}/>'


def text(x, y, s, size=40, fill=INK, anchor="middle", weight="700", italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{st}>{s}</text>')


def curve_pts(f, a, b, xmap, ymap, n=240):
    return [(xmap(a + (b - a) * i / n), ymap(f(a + (b - a) * i / n))) for i in range(n + 1)]


def path(pts, stroke=INK, width=6, fill="none"):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'


def area(f, a, b, xmap, ymap, base, fill, opacity=1.0):
    pts = curve_pts(f, a, b, xmap, ymap, 120)
    d = f"M{pts[0][0]:.1f},{base} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts) + f" L{pts[-1][0]:.1f},{base} Z"
    return f'<path d="{d}" fill="{fill}" fill-opacity="{opacity}"/>'


def lin(a, b, c, d):
    return lambda v: c + (v - a) * (d - c) / (b - a)


def npdf(z):
    return math.exp(-z * z / 2) / math.sqrt(2 * math.pi)


def tpdf(t, df):
    return math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(df * math.pi) * (1 + t * t / df) ** (-(df + 1) / 2)


def chipdf(x, k):
    if x <= 0:
        return 0.0
    return math.exp((k / 2 - 1) * math.log(x) - x / 2 - (k / 2) * math.log(2) - math.lgamma(k / 2))


def stacked_dots(values, lo, hi, nbins, x0, x1, ybase, r, color_fn):
    """Dotplot: bin values, stack dots upward from ybase. color_fn(bin_center) -> color."""
    out, w = [], (hi - lo) / nbins
    counts = [0] * nbins
    for v in values:
        b = min(nbins - 1, max(0, int((v - lo) / w)))
        counts[b] += 1
    xm = lin(lo, hi, x0, x1)
    for b, c in enumerate(counts):
        cx = xm(lo + (b + 0.5) * w)
        for k in range(c):
            out.append(dot(cx, ybase - r - k * 2 * r, r - 1, color_fn(lo + (b + 0.5) * w)))
    return "".join(out), counts


def boxplot(x0, x1, y, h, q, fill):
    """Horizontal boxplot; q = (min, q1, med, q3, max) already in pixels."""
    mn, q1, md, q3, mx = q
    return (f'<line x1="{mn}" y1="{y}" x2="{q1}" y2="{y}" stroke="{INK}" stroke-width="4"/>'
            f'<line x1="{q3}" y1="{y}" x2="{mx}" y2="{y}" stroke="{INK}" stroke-width="4"/>'
            f'<line x1="{mn}" y1="{y-h/3}" x2="{mn}" y2="{y+h/3}" stroke="{INK}" stroke-width="4"/>'
            f'<line x1="{mx}" y1="{y-h/3}" x2="{mx}" y2="{y+h/3}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{q1}" y="{y-h/2}" width="{q3-q1}" height="{h}" rx="6" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
            f'<line x1="{md}" y1="{y-h/2}" x2="{md}" y2="{y+h/2}" stroke="{INK}" stroke-width="6"/>')


def vboxplot(x, w, q, fill):
    """Vertical boxplot; q = (min, q1, med, q3, max) in pixel y (min is the bottom)."""
    mn, q1, md, q3, mx = q
    return (f'<line x1="{x}" y1="{mn}" x2="{x}" y2="{q1}" stroke="{INK}" stroke-width="4"/>'
            f'<line x1="{x}" y1="{q3}" x2="{x}" y2="{mx}" stroke="{INK}" stroke-width="4"/>'
            f'<line x1="{x-w/4}" y1="{mn}" x2="{x+w/4}" y2="{mn}" stroke="{INK}" stroke-width="4"/>'
            f'<line x1="{x-w/4}" y1="{mx}" x2="{x+w/4}" y2="{mx}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{x-w/2}" y="{q3}" width="{w}" height="{q1-q3}" rx="6" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
            f'<line x1="{x-w/2}" y1="{md}" x2="{x+w/2}" y2="{md}" stroke="{INK}" stroke-width="6"/>')


# ---------- weeks ----------
def week01():
    # Coin-flip null distribution (heads in 20 flips) and one surprising observed result far in the tail.
    rng = random.Random(1)
    vals = [sum(rng.random() < 0.5 for _ in range(20)) for _ in range(110)]
    body, _ = stacked_dots(vals, 2.5, 19.5, 17, X0 + 10, X1 - 10, Y1, 10, lambda c: PALE)
    xm = lin(2.5, 19.5, X0 + 10, X1 - 10)
    ox = xm(18)
    body += dot(ox, Y1 - 14, 18, ORANGE)
    body += (f'<path d="M{ox},{Y1-46} L{ox},{Y1-190}" stroke="{ORANGE}" stroke-width="6" stroke-linecap="round"/>'
             f'<path d="M{ox-16},{Y1-70} L{ox},{Y1-46} L{ox+16},{Y1-70}" fill="none" stroke="{ORANGE}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    body += text(ox, Y1 - 210, "?", 110, ORANGE)
    body += axis()
    # coins
    for i, s in enumerate("HTHHTHTH"):
        cx = 135 + i * 76
        body += (f'<circle cx="{cx}" cy="150" r="30" fill="{"#f2a600" if s == "H" else "#d9d6cc"}" stroke="{INK}" stroke-width="3"/>'
                 + text(cx, 164, s, 36))
    return svg(body, "Could It Be Chance?")


def week02():
    # Population grid with a random sample highlighted, plus a small data table.
    rng = random.Random(2)
    n, gap = 11, 44
    sx, sy = 400 - (n - 1) * gap / 2 - 110, 140
    picks = set(rng.sample(range(n * n), 14))
    body = ""
    for i in range(n * n):
        r_, c_ = divmod(i, n)
        body += dot(sx + c_ * gap, sy + r_ * gap, 15 if i in picks else 12, BLUE if i in picks else PALE)
    # data table (cases x variables)
    tx, ty, cw, ch = 560, 170, 60, 50
    for r_ in range(8):
        for c_ in range(3):
            fill = INK if r_ == 0 else ("#ffffff" if r_ % 2 else "#ebe8df")
            body += f'<rect x="{tx+c_*cw}" y="{ty+r_*ch}" width="{cw-4}" height="{ch-4}" rx="4" fill="{fill}"/>'
    body += (f'<path d="M500,360 L545,360" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
             f'<path d="M530,345 L548,360 L530,375" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    return svg(body, "Data &amp; Sampling")


def week03():
    # Random assignment into two groups, then a segmented bar chart of outcomes.
    rng = random.Random(3)
    body = ""
    people = list(range(12))
    rng.shuffle(people)
    for i in range(12):
        body += dot(130 + i * 49, 150, 16, MUTED)
    # arrows to groups
    for gx, col in ((235, BLUE), (565, ORANGE)):
        body += (f'<path d="M400,185 Q400,230 {gx},250" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
        for k in range(6):
            body += dot(gx - 100 + k * 40, 280, 15, col)
    # segmented bars: success share differs
    by0, by1 = 340, 610
    for gx, col, share in ((235, BLUE, 0.68), (565, ORANGE, 0.38)):
        hgt = by1 - by0
        top = by1 - hgt * share
        body += f'<rect x="{gx-80}" y="{top}" width="160" height="{by1-top}" rx="4" fill="{col}"/>'
        body += f'<rect x="{gx-80}" y="{by0}" width="160" height="{top-by0-4}" rx="4" fill="{col}" fill-opacity="0.3"/>'
    body += axis(by1, 120, 680)
    return svg(body, "Experiments")


def week04():
    # Right-skewed histogram with mean (orange) and median (blue), boxplot underneath.
    rng = random.Random(4)
    vals = sorted(rng.gammavariate(2.0, 1.4) for _ in range(400))
    lo, hi, nb = 0, 12, 16
    counts = [0] * nb
    for v in vals:
        counts[min(nb - 1, int((v - lo) / (hi - lo) * nb))] += 1
    xm = lin(lo, hi, X0, X1)
    top = max(counts)
    hb = 470
    ym = lin(0, top, hb, Y0 + 20)
    body = ""
    bw = (X1 - X0) / nb
    for b, c in enumerate(counts):
        if c:
            body += f'<rect x="{X0+b*bw+1}" y="{ym(c)}" width="{bw-2}" height="{hb-ym(c)}" rx="4" fill="{PALE}"/>'
    med = vals[len(vals) // 2]
    mean = sum(vals) / len(vals)
    for v, col in ((med, BLUE), (mean, ORANGE)):
        body += f'<line x1="{xm(v)}" y1="{Y0}" x2="{xm(v)}" y2="{hb}" stroke="{col}" stroke-width="7" stroke-linecap="round"/>'
    body += axis(hb)
    q = lambda p: xm(vals[int(p * (len(vals) - 1))])
    body += boxplot(X0, X1, 560, 70, (q(0), q(0.25), q(0.5), q(0.75), q(0.995)), "#ffffff")
    return svg(body, "Center &amp; Spread")


def week05():
    rng = random.Random(5)
    xs = [rng.uniform(0, 10) for _ in range(40)]
    ys = [2 + 0.75 * x + rng.gauss(0, 1.1) for x in xs]
    mx, my = sum(xs) / 40, sum(ys) / 40
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    xm, ym = lin(-0.5, 10.5, X0 + 10, X1), lin(0, 12, Y1 - 10, Y0)
    body = axis() + yaxis()
    for x, y in zip(xs, ys):
        body += dot(xm(x), ym(y), 13, BLUE)
    body += f'<line x1="{xm(-0.3)}" y1="{ym(a+b*-0.3)}" x2="{xm(10.3)}" y2="{ym(a+b*10.3)}" stroke="{ORANGE}" stroke-width="8" stroke-linecap="round"/>'
    body += text(500, 175, "ŷ = a + bx", 46, INK, italic=True, weight="400")
    return svg(body, "Linear Regression")


def week06():
    # Residual plot (left) and a probability tree (right).
    rng = random.Random(6)
    body = ""
    rx0, rx1, ry = 70, 420, 370
    body += f'<line x1="{rx0}" y1="{ry}" x2="{rx1}" y2="{ry}" stroke="{ORANGE}" stroke-width="6" stroke-dasharray="14 10" stroke-linecap="round"/>'
    body += yaxis(rx0, 150, 590)
    for i in range(26):
        x = rx0 + 20 + i * (rx1 - rx0 - 30) / 25
        e = rng.gauss(0, 60)
        body += f'<line x1="{x}" y1="{ry}" x2="{x}" y2="{ry+e}" stroke="{PALE}" stroke-width="3"/>'
        body += dot(x, ry + e, 10, BLUE)
    # tree
    tx = 480
    nodes = [(tx, 370)]
    body += dot(tx, 370, 14, INK, False)
    for dy1 in (-130, 130):
        x2, y2 = tx + 110, 370 + dy1
        body += f'<line x1="{tx}" y1="370" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="5"/>'
        for dy2 in (-60, 60):
            x3, y3 = x2 + 110, y2 + dy2
            col = AQUA if dy2 < 0 else ORANGE
            body += f'<line x1="{x2}" y1="{y2}" x2="{x3}" y2="{y3}" stroke="{INK}" stroke-width="5"/>'
            body += dot(x3, y3, 14, col, False)
        body += dot(x2, y2, 14, BLUE, False)
    body += text(tx + 55, 290, "P", 40, MUTED, italic=True, weight="400")
    return svg(body, "Residuals · Probability")


def week07():
    # Many sample means stack into a sampling distribution; a few samples shown as short strips above.
    rng = random.Random(7)
    body = ""
    for s in range(3):
        y = 140 + s * 50
        xs = [rng.gauss(400, 90) for _ in range(8)]
        for x in xs:
            body += dot(x, y, 9, PALE)
        m = sum(xs) / 8
        body += f'<line x1="{m}" y1="{y-22}" x2="{m}" y2="{y+22}" stroke="{BLUE}" stroke-width="6" stroke-linecap="round"/>'
    means = [rng.gauss(0, 1) for _ in range(120)]
    d, _ = stacked_dots(means, -3, 3, 21, X0 + 20, X1 - 20, Y1, 9, lambda c: BLUE)
    body += d + axis()
    return svg(body, "Sampling Distributions")


def week08():
    rng = random.Random(8)
    vals = sorted(rng.gauss(0, 1) for _ in range(150))
    lo_c, hi_c = vals[4], vals[145]
    d, counts = stacked_dots(vals, -3, 3, 27, X0 + 10, X1 - 10, Y1, 8,
                             lambda c: BLUE if lo_c <= c <= hi_c else PALE)
    xm = lin(-3, 3, X0 + 10, X1 - 10)
    body = d + axis()
    # bracket for 95% interval
    a, b = xm(lo_c), xm(hi_c)
    body += (f'<path d="M{a},{Y1+30} L{a},{Y1+45} L{b},{Y1+45} L{b},{Y1+30}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             + text(400, Y0 + 30, "95%", 64, BLUE))
    return svg(body, "Bootstrap Intervals")


def week09():
    rng = random.Random(9)
    vals = [rng.gauss(0, 1) for _ in range(150)]
    obs = 1.9
    d, _ = stacked_dots(vals, -3.2, 3.2, 27, X0 + 10, X1 - 10, Y1, 8,
                        lambda c: ORANGE if c >= obs else PALE)
    xm = lin(-3.2, 3.2, X0 + 10, X1 - 10)
    body = d + axis()
    body += f'<line x1="{xm(obs)}" y1="{Y0+60}" x2="{xm(obs)}" y2="{Y1}" stroke="{INK}" stroke-width="6" stroke-dasharray="12 10" stroke-linecap="round"/>'
    body += text(xm(obs) + 10, Y0 + 40, "observed", 34, INK, weight="400")
    body += text(200, Y0 + 40, "p-value", 50, ORANGE, italic=True)
    return svg(body, "Hypothesis Tests")


def week10():
    xm, ym = lin(-3.6, 3.6, X0, X1), lin(0, 0.42, Y1, Y0 + 40)
    crit = 1.645
    body = area(npdf, crit, 3.6, xm, ym, Y1, ORANGE)
    body += area(npdf, -3.6, crit, xm, ym, Y1, BLUE, 0.15)
    body += path(curve_pts(npdf, -3.6, 3.6, xm, ym), INK, 7)
    body += f'<line x1="{xm(crit)}" y1="{Y0+40}" x2="{xm(crit)}" y2="{Y1}" stroke="{INK}" stroke-width="5"/>'
    body += axis()
    body += text(xm(2.55), ym(0.06) - 70, "α", 80, ORANGE, italic=True)
    body += text(xm(-1.3), Y0 + 40, "don’t reject", 36, BLUE)
    body += text(xm(2.6), Y0 + 40, "reject", 36, ORANGE)
    return svg(body, "Significance")


def week11():
    xm, ym = lin(-3.5, 3.5, X0, X1), lin(0, 0.42, Y1, Y0)
    body = area(npdf, -1, 1, xm, ym, Y1, BLUE, 0.85)
    body += area(npdf, -2, -1, xm, ym, Y1, BLUE, 0.45) + area(npdf, 1, 2, xm, ym, Y1, BLUE, 0.45)
    body += area(npdf, -3, -2, xm, ym, Y1, BLUE, 0.18) + area(npdf, 2, 3, xm, ym, Y1, BLUE, 0.18)
    body += path(curve_pts(npdf, -3.5, 3.5, xm, ym), INK, 7) + axis()
    for z in range(-3, 4):
        body += f'<line x1="{xm(z)}" y1="{Y1}" x2="{xm(z)}" y2="{Y1+16}" stroke="{INK}" stroke-width="4"/>'
        body += text(xm(z), Y1 + 46, str(z), 30, INK, weight="400")
    body += text(xm(0), ym(0.2), "68%", 46, "#ffffff")
    return svg(body, "Normal Distribution")


def week12():
    # Two sample proportions with confidence-interval whiskers.
    ym = lin(0, 1, Y1, Y0 + 30)
    body = yaxis(130, Y0 + 30, Y1)
    for gx, col, p, me in ((300, BLUE, 0.62, 0.09), (540, ORANGE, 0.41, 0.10)):
        body += f'<rect x="{gx-75}" y="{ym(p)}" width="150" height="{Y1-ym(p)}" rx="4" fill="{col}"/>'
        body += (f'<line x1="{gx}" y1="{ym(p+me)}" x2="{gx}" y2="{ym(p-me)}" stroke="{INK}" stroke-width="6"/>'
                 f'<line x1="{gx-28}" y1="{ym(p+me)}" x2="{gx+28}" y2="{ym(p+me)}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                 f'<line x1="{gx-28}" y1="{ym(p-me)}" x2="{gx+28}" y2="{ym(p-me)}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    body += text(300, ym(0.62 + 0.09) - 24, "p̂₁", 50, INK, italic=True, weight="400")
    body += text(540, ym(0.41 + 0.10) - 24, "p̂₂", 50, INK, italic=True, weight="400")
    body += axis(Y1, 130, 690)
    return svg(body, "Proportions")


def week13():
    xm, ym = lin(-4, 4, X0, X1), lin(0, 0.42, Y1, Y0 + 40)
    body = path(curve_pts(npdf, -4, 4, xm, ym), PALE, 7)
    body += path(curve_pts(lambda t: tpdf(t, 2), -4, 4, xm, ym), BLUE, 8)
    body += axis()
    body += text(xm(0), ym(0.42) - 10, "normal", 34, MUTED, weight="400")
    body += text(xm(2.9), ym(0.06) - 20, "t", 90, BLUE, italic=True)
    body += text(xm(-2.9), ym(0.06) - 20, "x̄", 80, INK, italic=True, weight="400")
    return svg(body, "Means &amp; the t-Distribution")


def week14():
    # Two groups' dot strips with means (top) and a chi-square curve with an upper tail (bottom).
    rng = random.Random(14)
    body = ""
    for y, col, mu in ((160, BLUE, 330), (230, ORANGE, 470)):
        for _ in range(14):
            body += dot(rng.gauss(mu, 70), y, 11, col)
        body += f'<line x1="{mu}" y1="{y-30}" x2="{mu}" y2="{y+30}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    xm, ym = lin(0, 16, X0, X1), lin(0, 0.2, Y1, 330)
    f = lambda x: chipdf(x, 4)
    body += area(f, 9.5, 16, xm, ym, Y1, ORANGE)
    body += path(curve_pts(f, 0.001, 16, xm, ym), INK, 7) + axis()
    body += text(xm(11.5), 420, "χ²", 80, INK, italic=True, weight="400")
    return svg(body, "Two Means · Chi-Square")


def week15():
    # Side-by-side boxplots (ANOVA) with group means at different heights.
    ym = lin(0, 10, Y1, Y0)
    body = axis() + yaxis()
    groups = ((230, BLUE, (1.5, 3.2, 4.2, 5.3, 7.0)),
              (400, ORANGE, (3.0, 4.8, 5.9, 6.9, 8.8)),
              (570, AQUA, (2.0, 3.6, 4.6, 5.8, 7.6)))
    for gx, col, q in groups:
        body += vboxplot(gx, 110, tuple(ym(v) for v in q), col)
    body += text(400, Y0 + 10, "F", 80, INK, italic=True)
    return svg(body, "ANOVA · Slope Inference")


def week16():
    # Collage of the term's pictures: histogram, scatter + line, bell curve, bootstrap dotplot.
    rng = random.Random(16)
    body = ""
    panes = ((60, 80), (420, 80), (60, 380), (420, 380))
    pw, ph = 320, 270
    for (px, py) in panes:
        body += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="18" fill="#ffffff" stroke="{GRID}" stroke-width="3"/>'
    # histogram
    px, py = panes[0]
    hs = [2, 5, 9, 12, 10, 6, 4, 2, 1]
    for i, hgt in enumerate(hs):
        body += f'<rect x="{px+30+i*29}" y="{py+ph-30-hgt*17}" width="26" height="{hgt*17}" rx="3" fill="{PALE}"/>'
    # scatter
    px, py = panes[1]
    for _ in range(18):
        x = rng.uniform(0, 1)
        y = 0.15 + 0.7 * x + rng.gauss(0, 0.08)
        body += dot(px + 30 + x * 260, py + ph - 30 - y * 210, 8, BLUE)
    body += f'<line x1="{px+30}" y1="{py+ph-30-0.15*210}" x2="{px+290}" y2="{py+ph-30-0.85*210}" stroke="{ORANGE}" stroke-width="6" stroke-linecap="round"/>'
    # bell curve
    px, py = panes[2]
    xm, ymm = lin(-3.2, 3.2, px + 25, px + pw - 25), lin(0, 0.42, py + ph - 30, py + 30)
    body += area(npdf, -1.96, 1.96, xm, ymm, py + ph - 30, BLUE, 0.35)
    body += path(curve_pts(npdf, -3.2, 3.2, xm, ymm), INK, 6)
    # boxplots
    px, py = panes[3]
    yb = lin(0, 10, py + ph - 30, py + 30)
    body += vboxplot(px + 100, 70, tuple(yb(v) for v in (1, 3, 4.5, 6, 8)), BLUE)
    body += vboxplot(px + 220, 70, tuple(yb(v) for v in (3, 5, 6.5, 7.5, 9.5)), ORANGE)
    return svg(body, "Putting It All Together")


def start_here():
    # A rising staircase of bars (the semester's 16 weeks) with a flag on the first one and a "you are here" dot.
    n = 16
    bw = (X1 - X0) / n
    ym = lin(0, n, Y1, Y0 + 60)
    body = ""
    for i in range(n):
        top = ym(i + 1)
        col = ORANGE if i == 0 else PALE
        body += f'<rect x="{X0+i*bw+2}" y="{top}" width="{bw-4}" height="{Y1-top}" rx="4" fill="{col}"/>'
    fx = X0 + bw / 2
    ftop = ym(1) - 170
    body += (f'<line x1="{fx}" y1="{ym(1)}" x2="{fx}" y2="{ftop}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
             f'<path d="M{fx},{ftop} L{fx+90},{ftop+30} L{fx},{ftop+60} Z" fill="{BLUE}"/>')
    body += text(fx + 20, ftop - 30, "you are here", 36, INK, anchor="start", weight="400", italic=True)
    body += axis()
    body += text(X1 - 10, Y0 + 30, "Week 16", 34, MUTED, anchor="end", weight="400")
    return svg(body, "Start Here")


WEEKS = [week01, week02, week03, week04, week05, week06, week07, week08,
         week09, week10, week11, week12, week13, week14, week15, week16]


def main():
    os.makedirs(HTML_DIR, exist_ok=True)
    jobs = [("StartHere", start_here)] + [(f"Week{i:02d}", fn) for i, fn in enumerate(WEEKS, start=1)]
    for name, fn in jobs:
        html = os.path.join(HTML_DIR, name + ".html")
        with open(html, "w", encoding="utf-8") as fh:
            fh.write('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;padding:0;overflow:hidden}</style>'
                     + fn())
        png = os.path.join(OUT, name + ".png")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--window-size={W},{H}",
                        f"--screenshot={png}", "file://" + html],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        print(png)


if __name__ == "__main__":
    main()
