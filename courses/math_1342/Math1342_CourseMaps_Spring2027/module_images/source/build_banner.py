"""Blackboard course image / banner for Math 1342 (used for both sections).

Blackboard Ultra uses one "Course Image" for the banner across the top of the course page and,
center-cropped, for the course card. So the logo and title sit in the middle and the statistical
part (a quiet stacked dotplot with a normal curve) runs along the bottom edge.

Drawn at 1200x240 and saved at 2x: ../CourseBanner.png (2400x480).
Same palette and font as build_module_images.py. Standard library only.
Logo: ACC-District-Color-Logo.png, official full-color logo from austincc.edu (downloaded Nov 2026).
Run:  /usr/bin/python3 build_banner.py
"""
import math
import os
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
HTML_DIR = os.path.join(HERE, "html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W, H, SCALE = 1200, 240, 2
BG = "#f6f4ee"
INK = "#191919"
SUB = "#4a4a4a"
GRID = "#d9d6cc"
ORANGE = "#f47230"
PALE = "#c9d4e2"
FONT = "Arial, 'Helvetica Neue', Helvetica, sans-serif"

LOGO_W, LOGO_H = 754, 504


def zq(p):
    """Standard normal quantile by bisection (standard library only)."""
    lo, hi = -8.0, 8.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def dotplot():
    """A simulated sample (fixed seed) as a stacked dotplot along the bottom, with its normal curve."""
    rng = random.Random(1342)
    base, r, gap, binw = 226, 4.3, 9.6, 11.0
    mu, sd, n = W / 2, 210, 300
    counts = {}
    for i in range(n):
        # evenly spread normal quantiles with a little jitter: data-like, but a tidy bell
        v = mu + sd * zq((i + 0.5) / n) + rng.gauss(0, 0.2 * binw)
        if 18 < v < W - 18:
            b = int((v - 18) // binw)
            counts[b] = counts.get(b, 0) + 1
    out = [f'<line x1="16" y1="{base + 8}" x2="{W - 16}" y2="{base + 8}" stroke="{GRID}" stroke-width="1.5"/>']
    for b, c in sorted(counts.items()):
        cx = 18 + (b + 0.5) * binw
        for k in range(c):
            out.append(f'<circle cx="{cx:.1f}" cy="{base - k * gap:.1f}" r="{r}" fill="{PALE}"/>')
    # expected count per bin, drawn just above the dots
    scale = n * binw / (sd * math.sqrt(2 * math.pi))
    pts = []
    for i in range(241):
        xx = 16 + (W - 32) * i / 240
        yy = base - r - 3 - (scale - 0.5) * gap * math.exp(-0.5 * ((xx - mu) / sd) ** 2)
        pts.append(f"{xx:.1f},{yy:.1f}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{ORANGE}" stroke-width="3" '
               f'stroke-linecap="round" stroke-linejoin="round" opacity="0.85"/>')
    return "".join(out)


def title_block():
    lh = 118
    lw = lh * LOGO_W / LOGO_H
    title_size, sub_size, gap = 60, 27, 30
    text_w = 0.61 * title_size * len("MATH 1342")          # approx. Arial Bold advance
    total = lw + gap * 2 + 2 + text_w
    x0 = (W - total) / 2
    lx, ly = x0, 22
    div_x = lx + lw + gap
    tx = div_x + gap
    return (f'<image href="../ACC-District-Color-Logo.png" x="{lx:.1f}" y="{ly}" width="{lw:.1f}" height="{lh}"/>'
            f'<line x1="{div_x:.1f}" y1="34" x2="{div_x:.1f}" y2="130" stroke="{GRID}" stroke-width="2"/>'
            f'<text x="{tx:.1f}" y="92" font-family="{FONT}" font-size="{title_size}" font-weight="700" '
            f'fill="{INK}" letter-spacing="1">MATH 1342</text>'
            f'<text x="{tx + 2:.1f}" y="128" font-family="{FONT}" font-size="{sub_size}" fill="{SUB}">'
            f'Elementary Statistics</text>')


def build():
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W * SCALE}" height="{H * SCALE}" '
           f'viewBox="0 0 {W} {H}" role="img" aria-label="Math 1342 Elementary Statistics, Austin Community College">'
           f'<rect width="{W}" height="{H}" fill="{BG}"/>{dotplot()}{title_block()}</svg>')
    os.makedirs(HTML_DIR, exist_ok=True)
    html = os.path.join(HTML_DIR, "CourseBanner.html")
    with open(html, "w") as f:
        f.write(f'<!doctype html><meta charset="utf-8"><style>html,body{{margin:0;background:{BG}}}'
                f'svg{{display:block}}</style>{svg}')
    png = os.path.join(OUT, "CourseBanner.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W * SCALE},{H * SCALE}",
                    "--virtual-time-budget=3000", f"--screenshot={png}", "file://" + html],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    print(png)


if __name__ == "__main__":
    build()
