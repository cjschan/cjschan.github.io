"""Builds W01_Introductions_Rubric.pdf from the rubric table in W01_Introductions.md.
Headless Chrome prints a tagged PDF (title, language, headings, table header cells), which Word's
"Save as PDF" on the Mac does not. Run: python3 build_rubric.py"""
from pathlib import Path

HERE = Path(__file__).resolve().parent

md = (HERE / "W01_Introductions.md").read_text()
rows = [[c.strip() for c in line.strip("|").split("|")]
        for line in md[md.index("## Rubric"):].splitlines() if line.startswith("|") and not line.startswith("|---")]
table = [["Criterion"] + rows[0][1:5]] + [[f"{r[0]}: {r[5]}"] + r[1:5] for r in rows[1:]]

# ---- accessible PDF: an HTML version printed by headless Chrome (tagged PDF with headings + table headers)
import html as H  # noqa: E402
import subprocess  # noqa: E402
cols = table[0]
trs = "".join("<tr><th scope=\"row\">" + H.escape(r[0]) + "</th>" + "".join(f"<td>{H.escape(c)}</td>" for c in r[1:]) + "</tr>"
              for r in table[1:])
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Discussion Rubric: Introductions and Statistics in Your Life (MATH 1342, Spring 2027)</title>
<style>@page{{size:Letter landscape;margin:0.6in 0.7in}}
body{{font-family:Calibri,Arial,sans-serif;color:#1e293b;font-size:10.5pt}}
.band{{background:#1e293b;color:#fff;padding:5px 9px;font-weight:bold;font-size:10pt}}
h1{{font-size:19pt;margin:10px 0 2px}} .sub{{color:#0f5d8a;font-weight:bold;margin:0 0 10px}}
table{{border-collapse:collapse;width:100%}} th,td{{border:1px solid #94a3b8;padding:5px 7px;vertical-align:top;text-align:left}}
thead th{{background:#e2e8f0}} tbody th{{width:16%}} thead th+th,td{{width:21%}} h2{{font-size:13pt;margin:14px 0 4px}}</style></head><body>
<div class="band">MATH 1342 · Elementary Statistics · Spring 2027</div>
<h1>Discussion Rubric: Introductions and Statistics in Your Life</h1>
<p class="sub">Week 1 discussion · 10 points · Initial post due Fri Jan 22, 11:59 PM · Two replies due Sun Jan 24, 11:59 PM</p>
<p>Each criterion earns the percentage of its points shown in the column headings. The four criteria add up to 10 points.</p>
<table><caption style="text-align:left;font-weight:bold;padding-bottom:4px">Rubric: four criteria scored at four levels</caption>
<thead><tr>{''.join(f'<th scope="col">{H.escape(c)}</th>' for c in cols)}</tr></thead><tbody>{trs}</tbody></table>
<h2>Scoring</h2><ul><li>Comprehension: 40% (4 points)</li><li>Timeliness: 10% (1 point)</li>
<li>Engagement: 30% (3 points)</li><li>Clear Communication: 20% (2 points)</li></ul></body></html>"""
(HERE / "W01_Introductions_Rubric.html").write_text(page)
subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless", "--disable-gpu",
                "--no-pdf-header-footer", f"--print-to-pdf={HERE / 'W01_Introductions_Rubric.pdf'}",
                (HERE / "W01_Introductions_Rubric.html").as_uri()], check=True, capture_output=True)
print("pdf ok")
