#!/usr/bin/env python3
"""Render the Math 1342 weekly course maps to HTML and print them to PDF with headless Chrome.

Usage:  python3 build_course_maps.py
Output: ../Week01.pdf ... Week16.pdf, ../Math1342_CourseMap_All.pdf, html/*.html
"""
import html as H
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
HTML_DIR = os.path.join(HERE, "html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
sys.path.insert(0, HERE)
import course_map_data as D  # noqa: E402

CSS = """
@page { size: letter landscape; margin: 0.35in 0.4in; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: Arial, "Helvetica Neue", Helvetica, sans-serif; font-size: %(fs)spt; color: #111; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
h1 { font-size: %(fs)spt; margin: 0 0 1px 0; text-align: center; font-weight: 700; }
.sub { text-align: center; font-size: %(fs)spt; color: #333; margin-bottom: 5px; }
.sub b { color: #111; }
table.map { width: 99%%; border-collapse: collapse; table-layout: fixed; margin: 0 auto; }
table.map th { border: 1px solid #000; background: #d9d9d9; font-weight: 700; padding: 5px 4px; text-align: center; vertical-align: middle; }
table.map td { border: 1px solid #000; vertical-align: top; padding: 4px 5px; line-height: 1.2; }
table.map td p { margin: 0 0 4px 0; }
table.map td p:last-child { margin-bottom: 0; }
.mo-n { font-weight: 700; }
.clo { white-space: nowrap; }
.code { color: #555; white-space: nowrap; }
.rowlabel { font-style: italic; color: #333; }
.legend { margin-top: 4px; color: #333; line-height: 1.25; }
.legend b { color: #111; }
"""

def esc(s):
    return H.escape(s, quote=False)

def parse_codes(code, n_mos):
    """'MO1, MO3' / 'MO1–MO5' / 'None' -> set of module objective numbers."""
    out = set()
    for part in code.replace(" ", "").split(","):
        m = re.fullmatch(r"MO(\d+)(?:[–-]MO(\d+))?", part)
        if m:
            a = int(m.group(1)); b = int(m.group(2) or a)
            out.update(range(a, b + 1))
        elif part == "All":
            out.update(range(1, n_mos + 1))
    return out

def mo_groups(w):
    """Group module objectives into table rows: objectives that share a learning material go together."""
    n = len(w["mos"])
    parent = list(range(n + 1))
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for _, code in w["materials"]:
        mos = sorted(parse_codes(code, n))
        for m in mos[1:]:
            parent[find(m)] = find(mos[0])
    groups = {}
    for m in range(1, n + 1):
        groups.setdefault(find(m), []).append(m)
    return sorted(groups.values())

def tools_for(text, kind):
    t = text.lower()
    if text.startswith("Interactive Lecture"):
        return ["WileyPLUS", "StatKey"]
    if text.startswith(("e-Text", "Online Homework")):
        return ["WileyPLUS"]
    if "slides" in t.split(":")[0] or text.startswith("All "):
        return ["Lecture Slides (course website)"]
    if text.startswith("START HERE"):
        return ["Content Area in Blackboard"]
    if text.startswith("StatKey"):
        return ["StatKey"]
    if text.startswith("Take-Home Quiz"):
        return ["Assignment Tool in Blackboard"]
    if re.match(r"(Practice )?Test|Final Exam", text):
        return ["Assessment Tool in Blackboard", "Respondus LockDown Browser and Monitor"]
    out = []
    if "kahoot" in t:
        out.append("Kahoot!")
    if "statkey" in t:
        out.append("StatKey")
    return out or [D.LIVE_TOOL]

def clo_tag(clos):
    return '<span class="clo">(' + ", ".join(f"CLO {c}" for c in clos) + ")</span>"

def item_cell(items, show_codes=False):
    out = []
    for text, code in items:
        extra = f' <span class="code">({esc(code)})</span>' if show_codes else ""
        out.append(f"<p>{esc(text)}{extra}</p>")
    return "".join(out)

def tools_cell(items):
    seen = []
    for kind in ("materials", "activities", "assessments"):
        for text, _ in items[kind]:
            for tool in tools_for(text, kind):
                if tool not in seen:
                    seen.append(tool)
    return "".join(f"<p>{esc(t)}</p>" for t in seen)

def week_rows(w):
    n = len(w["mos"])
    groups = mo_groups(w)
    rows = [dict(mos=g, materials=[], activities=[], assessments=[]) for g in groups]
    spans = dict(materials=[], activities=[], assessments=[])
    other = dict(materials=[], activities=[], assessments=[])
    for kind in ("materials", "activities", "assessments"):
        for text, code in w[kind]:
            mos = parse_codes(code, n)
            home = [r for r in rows if mos and mos <= set(r["mos"])]
            if not mos:
                other[kind].append((text, code))
            elif home:
                home[0][kind].append((text, code))
            else:
                if mos == set(range(1, n + 1)):
                    code = "all objectives"
                spans[kind].append((text, code))
    html = []
    for r in rows:
        mo_html = "".join(f'<p><span class="mo-n">{m}.</span> {esc(w["mos"][m - 1][0])} {clo_tag(w["mos"][m - 1][1])}</p>' for m in r["mos"])
        html.append(f"<tr><td>{mo_html}</td><td>{item_cell(r['materials'])}</td><td>{item_cell(r['activities'])}</td>"
                    f"<td>{item_cell(r['assessments'])}</td><td>{tools_cell(r)}</td></tr>")
    if any(spans.values()):
        html.append('<tr><td><p class="rowlabel">Items that cover objectives from more than one row above (objectives in parentheses)</p></td>'
                    f"<td>{item_cell(spans['materials'], True)}</td><td>{item_cell(spans['activities'], True)}</td>"
                    f"<td>{item_cell(spans['assessments'], True)}</td><td>{tools_cell(spans)}</td></tr>")
    if any(other.values()):
        html.append('<tr><td><p class="rowlabel">Course resources and assessments of earlier weeks (not aligned to this week\'s objectives)</p></td>'
                    f"<td>{item_cell(other['materials'])}</td><td>{item_cell(other['activities'])}</td>"
                    f"<td>{item_cell(other['assessments'])}</td><td>{tools_cell(other)}</td></tr>")
    return "".join(html)

def clo_legend(w):
    used = sorted({c for _, clos in w["mos"] for c in clos})
    return " &nbsp; ".join(f"<b>CLO {c}</b> {esc(D.COURSE_OBJECTIVES[c - 1])}" for c in used)

def week_page(w):
    sections = " &nbsp;•&nbsp; ".join(esc(s) for s in w["sections"])
    return f"""
<div class="page">
  <h1>{esc(D.COURSE)} – Week {w['num']}: {esc(w['title'])}</h1>
  <div class="sub"><b>{esc(w['dates'])}</b> &nbsp;|&nbsp; {sections} &nbsp;|&nbsp; {esc(D.TERM)}</div>
  <table class="map">
    <colgroup>
      <col style="width:29%"><col style="width:22%"><col style="width:20%"><col style="width:16%"><col style="width:13%">
    </colgroup>
    <thead><tr>
      <th>Module Objectives</th><th>Instructional Materials</th><th>Learning Activities</th><th>Assessments</th><th>Tools</th>
    </tr></thead>
    <tbody>{week_rows(w)}</tbody>
  </table>
  <div class="legend">{clo_legend(w)}</div>
</div>"""

def document(pages, fs):
    css = CSS % dict(fs=fs)
    return f"<!doctype html><html><head><meta charset='utf-8'><title>Math 1342 Course Map</title><style>{css}</style></head><body>{''.join(pages)}</body></html>"

def print_pdf(html_path, pdf_path):
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           f"--print-to-pdf={pdf_path}", f"file://{html_path}"]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)

def page_count(pdf_path):
    out = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else -1

def main():
    os.makedirs(HTML_DIR, exist_ok=True)
    sizes = (11.0, 10.5, 10.0, 9.5, 9.0, 8.5, 8.0, 7.5, 7.0)
    chosen = None
    for fs in sizes:
        ok = True
        for w in D.WEEKS:
            name = f"Week{w['num']:02d}"
            html_path = os.path.join(HTML_DIR, name + ".html")
            pdf_path = os.path.join(OUT, name + ".pdf")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(document([week_page(w)], fs))
            print_pdf(html_path, pdf_path)
            if page_count(pdf_path) != 1:
                ok = False
                print(f"{fs}pt: {name} needs {page_count(pdf_path)} pages; trying smaller")
                break
        if ok:
            chosen = fs
            break
    if chosen is None:
        chosen = sizes[-1]
    print(f"Using {chosen}pt for every page")
    for w in D.WEEKS:
        name = f"Week{w['num']:02d}"
        print(f"{name}: {page_count(os.path.join(OUT, name + '.pdf'))} page(s)")

    all_html = os.path.join(HTML_DIR, "All.html")
    with open(all_html, "w", encoding="utf-8") as f:
        f.write(document([week_page(w) for w in D.WEEKS], chosen))
    all_pdf = os.path.join(OUT, "Math1342_CourseMap_All.pdf")
    print_pdf(all_html, all_pdf)
    print(f"Math1342_CourseMap_All.pdf: {page_count(all_pdf)} pages")

if __name__ == "__main__":
    main()
