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
h1 { font-size: 1.9em; margin: 0; font-weight: 700; }
h2 { font-size: 1.15em; margin: 0 0 2px 0; font-weight: 700; }
ul.clo { margin: 0 0 8px 0; padding-left: 2.2em; }
ul.clo li { margin: 1px 0; padding-left: 0.4em; }
table.map { width: calc(100%% - 3px); margin-left: 1px; border-collapse: collapse; table-layout: fixed; }
table.map th { border: 1.5px solid #000; background: #d9d9d9; font-weight: 700; padding: 6px 4px; text-align: center; vertical-align: middle; }
table.map td { border: 1.5px solid #000; vertical-align: top; padding: 4px 6px; line-height: 1.25; }
table.map td p { margin: 0; }
table.map td.assess p + p { margin-top: 0.9em; }
.mo-n { font-weight: 700; }
.gray { color: #555; }
.also { margin-top: 6px; line-height: 1.25; }
"""

def esc(s):
    return H.escape(s, quote=False)

def tools_for(text):
    t = text.lower()
    if text.startswith("Interactive Lecture") or text.startswith("All "):
        return ["WileyPLUS", "StatKey"]
    if text.startswith(("e-Text", "Online Homework")):
        return ["WileyPLUS"]
    if text.startswith("StatKey"):
        return ["StatKey"]
    if "Guide" in text.split("(")[0]:
        return ["Blackboard"]
    if re.match(r"(Practice )?Test|Final Exam", text):
        return ["Blackboard", "Respondus"]
    if "slides" in t.split(":")[0] or text.startswith(("START HERE", "Take-Home Quiz")):
        return ["Blackboard"] + (["StatKey"] if "statkey" in t else [])
    out = []
    if "kahoot" in t:
        out.append("Kahoot!")
    if "statkey" in t:
        out.append("StatKey")
    return out or ([D.LIVE_TOOL] if D.LIVE_TOOL else [])

GRAY_TAIL = re.compile(r"^(.*) (\((?:all objectives|objectives? [^()]+)\))$")

def item_html(text):
    """Escape one item; a trailing '(all objectives)' / '(objectives 9–12)' is shown in gray."""
    m = GRAY_TAIL.match(text)
    if m:
        return f'{esc(m.group(1))} <span class="gray">{esc(m.group(2))}</span>'
    return esc(text)

def item_cell(items):
    return "".join(f"<p>{item_html(t)}</p>" for t in items)

def tools_cell(r):
    seen = []
    for kind in ("materials", "activities", "assessments"):
        for text in r[kind]:
            for tool in tools_for(text):
                if tool not in seen:
                    seen.append(tool)
    return "".join(f"<p>{esc(t)}</p>" for t in seen)

def week_rows(w):
    html, n = [], 0
    for r in w["rows"]:
        mo_html = []
        for text, clos in r["mos"]:
            n += 1
            tag = ", ".join(f"CLO {c}" for c in clos)
            mo_html.append(f'<p><span class="mo-n">{n}.</span> {esc(text)} ({tag})</p>')
        html.append(f"<tr><td>{''.join(mo_html)}</td><td>{item_cell(r['materials'])}</td>"
                    f"<td>{item_cell(r['activities'])}</td><td class=\"assess\">{item_cell(r['assessments'])}</td>"
                    f"<td>{tools_cell(r)}</td></tr>")
    return "".join(html)

def week_page(w, fs=None):
    used = sorted({c for r in w["rows"] for _, clos in r["mos"] for c in clos})
    clos = "".join(f"<li>{esc(D.COURSE_OBJECTIVES[c - 1])} (CLO {c})</li>" for c in used)
    also = ""
    if w["also"]:
        also = '<div class="also"><b>Also this week:</b> ' + " &nbsp;•&nbsp; ".join(esc(a) for a in w["also"]) + "</div>"
    return f"""
<div class="page"{f' style="font-size:{fs}pt"' if fs else ''}>
  <h1>Week {w['num']}</h1>
  <h2>Course Level Objectives:</h2>
  <ul class="clo">{clos}</ul>
  <table class="map">
    <colgroup>
      <col style="width:29%"><col style="width:26%"><col style="width:15%"><col style="width:17%"><col style="width:13%">
    </colgroup>
    <thead><tr>
      <th>Module Objectives</th><th>Instructional Materials</th><th>Learning Activities</th><th>Assessments</th><th>Tools</th>
    </tr></thead>
    <tbody>{week_rows(w)}</tbody>
  </table>
  {also}
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

SIZES = (12.0, 11.5, 11.0, 10.5, 10.0, 9.5, 9.0, 8.5, 8.0, 7.5, 7.0)
FLOOR = 9.0   # a week that only fits below this size gets its own size instead of shrinking every page

def write_week(w, fs):
    name = f"Week{w['num']:02d}"
    html_path = os.path.join(HTML_DIR, name + ".html")
    pdf_path = os.path.join(OUT, name + ".pdf")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(document([week_page(w)], fs))
    print_pdf(html_path, pdf_path)
    return page_count(pdf_path)

def best_size(w, start):
    """Largest size from start down that fits the week on one page."""
    for fs in SIZES[SIZES.index(start):]:
        if write_week(w, fs) == 1:
            return fs
    return SIZES[-1]

def main():
    os.makedirs(HTML_DIR, exist_ok=True)
    # Shrink the common size until every week fits, except weeks that need less than FLOOR.
    common, best = SIZES[0], {}
    for w in D.WEEKS:
        fs = best_size(w, common)
        best[w["num"]] = fs
        if fs >= FLOOR and fs < common:
            common = fs
    size = {n: min(fs, common) for n, fs in best.items()}
    for w in D.WEEKS:
        n = write_week(w, size[w["num"]])
        note = "" if size[w["num"]] == common else " (own size)"
        print(f"Week{w['num']:02d}: {size[w['num']]}pt{note}, {n} page(s)")
    print(f"Common size: {common}pt")

    all_html = os.path.join(HTML_DIR, "All.html")
    with open(all_html, "w", encoding="utf-8") as f:
        f.write(document([week_page(w, size[w["num"]] if size[w["num"]] != common else None) for w in D.WEEKS], common))
    all_pdf = os.path.join(OUT, "Math1342_CourseMap_All.pdf")
    print_pdf(all_html, all_pdf)
    print(f"Math1342_CourseMap_All.pdf: {page_count(all_pdf)} pages")

if __name__ == "__main__":
    main()
