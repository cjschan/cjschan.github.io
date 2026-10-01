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
body { font-family: Calibri, "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: %(fs)spt; color: #111; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
h1 { font-size: %(fs)spt; margin: 0 0 1px 0; text-align: center; font-weight: 700; }
.sub { text-align: center; font-size: %(fs)spt; color: #333; margin-bottom: 5px; }
.sub b { color: #111; }
table.map { width: 99%%; border-collapse: collapse; table-layout: fixed; margin: 0 auto; }
table.map th { border: 1px solid #000; background: #fff; font-weight: 700; padding: 3px 4px; font-size: %(fs)spt; text-align: center; vertical-align: middle; }
table.map th.co { background: #e6e6e6; }
table.map td { border: 1px solid #000; vertical-align: top; padding: 0; }
td.co { background: #e6e6e6; }
td.co ol, td.mo ol { margin: 0; padding: 3px 3px 3px 22px; }
td.co li, td.mo li { margin: 0 0 3px 0; padding-left: 1px; }
td.co { line-height: 1.2; }
td.co li { margin: 0 0 1.5px 0; }
.tag { font-weight: 400; color: #333; white-space: nowrap; }
table.sub { width: 100%%; border-collapse: collapse; table-layout: fixed; }
table.sub td { text-align: left; border: none; border-bottom: 1px solid #000; padding: 3px 4px; vertical-align: top; }
table.sub td.hash { text-align: center; padding-left: 1px; padding-right: 1px; border-left: 1px solid #000; }
table.sub.w21 td.hash { width: 23.81%%; }   /* 5 / (16 + 5)  -> lines up with the header # column */
table.sub.w15 td.hash { width: 33.33%%; }   /* 5 / (10 + 5) */
.prop { color: #8a4b00; font-style: italic; }
.notes { margin-top: 5px; color: #222; }
.notes b { color: #000; }
.legend { margin-top: 2px; color: #444; }
"""

def esc(s):
    return H.escape(s, quote=False)

def mark_proposed(text):
    t = esc(text)
    return t.replace("(proposed)", '<span class="prop">(proposed)</span>')

def rows_html(items, n_mos, cls="w21"):
    rows = []
    for text, code in items:
        if code == f"MO1–MO{n_mos}":
            code = "All"
        rows.append(f'<tr><td class="it">{mark_proposed(text)}</td><td class="hash">{esc(code)}</td></tr>')
    return f'<table class="sub {cls}">' + "".join(rows) + "</table>"

def co_list(active):
    out = []
    for i in active:
        out.append(f'<li value="{i}">{esc(D.COURSE_OBJECTIVES[i - 1])}</li>')
    if not out:
        out.append('<li class="none">Supports Student Learning Outcome 3 (probability); not among the 12 Common Course Objectives.</li>')
    return "<ol>" + "".join(out) + "</ol>"

def mo_list(mos):
    out = []
    for text, cos in mos:
        tag = " (" + ", ".join(f"CO{c}" for c in cos) + ")" if cos else " (SLO 3)"
        out.append(f'<li>{esc(text)} <span class="tag">{tag}</span></li>')
    return "<ol>" + "".join(out) + "</ol>"

def week_page(w):
    active = sorted({c for _, cos in w["mos"] for c in cos})
    sections = " &nbsp;•&nbsp; ".join(esc(s) for s in w["sections"])
    notes = ""  # per-week notes are kept in the data file but not printed
    return f"""
<div class="page">
  <h1>{esc(D.COURSE)} – Week {w['num']}: {esc(w['title'])}</h1>
  <div class="sub"><b>{esc(w['dates'])}</b> &nbsp;|&nbsp; {sections} &nbsp;|&nbsp; {esc(D.TERM)}</div>
  <table class="map">
    <colgroup>
      <col style="width:20%"><col style="width:23%">
      <col style="width:16%"><col style="width:5%">
      <col style="width:16%"><col style="width:5%">
      <col style="width:10%"><col style="width:5%">
    </colgroup>
    <thead><tr>
      <th class="co">Course-level<br>Objectives</th><th>Module-level<br>Objectives</th>
      <th>Learning Materials</th><th>#</th><th>Activities</th><th>#</th><th>Assessments</th><th>#</th>
    </tr></thead>
    <tbody><tr>
      <td class="co">{co_list(active)}</td>
      <td class="mo">{mo_list(w['mos'])}</td>
      <td colspan="2">{rows_html(w['materials'], len(w['mos']))}</td>
      <td colspan="2">{rows_html(w['activities'], len(w['mos']))}</td>
      <td colspan="2">{rows_html(w['assessments'], len(w['mos']), 'w15')}</td>
    </tr></tbody>
  </table>
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
