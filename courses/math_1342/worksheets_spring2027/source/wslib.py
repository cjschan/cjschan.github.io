"""Shared look for every Spring 2027 Math 1342 handout (worksheets, answer keys,
practice tests, study guides, solutions).

Every document is built through the Doc class below, so they all share one header
band, directions box, problem/step layout, table style, callouts and footer.

Inline markup in strings:  **bold**   ~~italic~~   _{subscript}   ^{superscript}
(Single * is left alone so z*, t* print literally.)
"""
import re
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Inches, RGBColor, Emu

# ---------------------------------------------------------------- palette
SLATE = "0F172A"      # header band, headings
SLATE_2 = "334155"    # body accents
MUTED = "64748B"      # footer, labels
ACCENT = "0284C7"     # sky-600: readable on white (site accent #38bdf8 is the light tint)
ACCENT_LIGHT = "38BDF8"
TINT = "E0F2FE"       # sky-100 fill for directions
RULE = "CBD5E1"       # light borders
TABLE_HEAD = "F1F5F9"
GREEN = "047857"      # answer text
GREEN_TINT = "ECFDF5"
AMBER = "B45309"
AMBER_TINT = "FFFBEB"
FONT = "Calibri"
MATH_FONT = "Cambria Math"

CONTENT_W = 7.0  # inches (Letter with 0.75" margins)


def rgb(h):
    return RGBColor.from_string(h)


# ---------------------------------------------------------------- low-level xml helpers
def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def cell_borders(cell, **edges):
    """edges: top/left/bottom/right = (size_eighths, color) or None for nil."""
    tcPr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        spec = edges.get(edge, None)
        if spec is None:
            el.set(qn("w:val"), "nil")
        else:
            sz, color = spec
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(sz))
            el.set(qn("w:color"), color)
            el.set(qn("w:space"), "0")
        b.append(el)
    tcPr.append(b)


def cell_margins(cell, top=60, bottom=60, left=110, right=110):
    tcPr = cell._tc.get_or_add_tcPr()
    m = OxmlElement("w:tcMar")
    for k, v in (("top", top), ("bottom", bottom), ("start", left), ("end", right)):
        el = OxmlElement(f"w:{k}")
        el.set(qn("w:w"), str(v))
        el.set(qn("w:type"), "dxa")
        m.append(el)
    tcPr.append(m)


def table_no_borders(table):
    tblPr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "nil")
        b.append(el)
    tblPr.append(b)


def table_width(table, inches):
    tblPr = table._tbl.tblPr
    w = OxmlElement("w:tblW")
    w.set(qn("w:w"), str(int(inches * 1440)))
    w.set(qn("w:type"), "dxa")
    tblPr.append(w)
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)


def set_col_widths(table, widths):
    grid = table._tbl.tblGrid
    for i, gc in enumerate(grid.findall(qn("w:gridCol"))):
        gc.set(qn("w:w"), str(int(widths[i] * 1440)))
    for row in table.rows:
        for i, c in enumerate(row.cells):
            c.width = Inches(widths[i])


def para_border_bottom(p, color=RULE, sz=6, space=1):
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    el = OxmlElement("w:bottom")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(sz))
    el.set(qn("w:space"), str(space))
    el.set(qn("w:color"), color)
    bdr.append(el)
    pPr.append(bdr)


def keep_next(p, on=True):
    p.paragraph_format.keep_with_next = on


def no_split_row(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    trPr.append(el)


def add_field(run, instr):
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = instr
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t"); t.text = "1"
    f3 = OxmlElement("w:fldChar"); f3.set(qn("w:fldCharType"), "end")
    for el in (f1, it, f2, t, f3):
        run._r.append(el)


# ---------------------------------------------------------------- inline markup
TOKEN = re.compile(r"(\*\*.+?\*\*|~~.+?~~|_\{.+?\}|\^\{.+?\})")


def add_runs(p, text, color=None, bold=False, italic=False, size=None, font=None):
    """Add text with **bold**, *italic*, _{sub}, ^{sup} markup to paragraph p."""
    for part in TOKEN.split(text):
        if not part:
            continue
        b, i, sub, sup = bold, italic, False, False
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            part, b = part[2:-2], True
        elif part.startswith("_{") and part.endswith("}"):
            part, sub = part[2:-1], True
        elif part.startswith("^{") and part.endswith("}"):
            part, sup = part[2:-1], True
        elif part.startswith("~~") and part.endswith("~~") and len(part) > 4:
            part, i = part[2:-2], True
        r = p.add_run(part)
        r.bold = b or None
        r.italic = i or None
        if sub:
            r.font.subscript = True
        if sup:
            r.font.superscript = True
        if color:
            r.font.color.rgb = rgb(color)
        if size:
            r.font.size = Pt(size)
        if font:
            r.font.name = font
    return p


# ---------------------------------------------------------------- the document
class Doc:
    """kind: 'Participation Worksheet' | 'Answer Key' | 'Practice Test' | 'Study Guide' | 'Solutions'"""

    def __init__(self, kind, title, subtitle, key=False, name_line=True):
        self.key = key
        self.kind = kind
        self.d = Document()
        sec = self.d.sections[0]
        sec.page_width, sec.page_height = Inches(8.5), Inches(11)
        sec.left_margin = sec.right_margin = Inches(0.75)
        sec.top_margin = Inches(0.6)
        sec.bottom_margin = Inches(0.7)
        sec.footer_distance = Inches(0.35)
        st = self.d.styles["Normal"]
        st.font.name = FONT
        st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        st.font.size = Pt(11)
        st.font.color.rgb = rgb(SLATE)
        st.paragraph_format.space_after = Pt(4)
        st.paragraph_format.line_spacing = 1.1
        self._header(kind, title, subtitle, name_line)
        self._footer(title)

    # ---- header band + title
    def _header(self, kind, title, subtitle, name_line):
        t = self.d.add_table(rows=1, cols=2)
        table_no_borders(t)
        table_width(t, CONTENT_W)
        set_col_widths(t, [4.4, 2.6])
        l, r = t.rows[0].cells
        for c in (l, r):
            shade(c, SLATE)
            cell_margins(c, 90, 90, 160, 160)
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = l.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        add_runs(p, "MATH 1342", color="FFFFFF", bold=True, size=11)
        add_runs(p, "  ·  Elementary Statistics  ·  Spring 2027", color="CBD5E1", size=10)
        p = r.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.paragraph_format.space_after = Pt(0)
        label = kind.upper()
        add_runs(p, label, color=("6EE7B7" if self.key else ACCENT_LIGHT), bold=True, size=10)

        p = self.d.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(0)
        add_runs(p, title, color=SLATE, bold=True, size=20)
        if subtitle:
            p = self.d.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            add_runs(p, subtitle, color=ACCENT, bold=True, size=11)
        rule = self.d.add_paragraph()
        rule.paragraph_format.space_after = Pt(8)
        para_border_bottom(rule, color=ACCENT_LIGHT, sz=18, space=1)
        if self.key:
            self.callout("**Answer key.** Answers and worked solutions are shown in green below each question. "
                         "Values found with StatKey come from random simulations, so yours may differ slightly.",
                         fill=GREEN_TINT, bar=GREEN)
        elif name_line:
            p = self.d.add_paragraph()
            p.paragraph_format.space_after = Pt(10)
            add_runs(p, "Name  ", color=MUTED, bold=True, size=10)
            add_runs(p, "_" * 46, color=RULE)
            add_runs(p, "     Date  ", color=MUTED, bold=True, size=10)
            add_runs(p, "_" * 20, color=RULE)

    def _footer(self, title):
        f = self.d.sections[0].footer
        p = f.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para_border_bottom  # (no rule; keep footer light)
        add_runs(p, f"MATH 1342  ·  {title}  ·  Page ", color=MUTED, size=8.5)
        r = p.add_run(); r.font.size = Pt(8.5); r.font.color.rgb = rgb(MUTED); add_field(r, "PAGE")
        r = p.add_run(" of "); r.font.size = Pt(8.5); r.font.color.rgb = rgb(MUTED)
        r = p.add_run(); r.font.size = Pt(8.5); r.font.color.rgb = rgb(MUTED); add_field(r, "NUMPAGES")

    # ---- boxes
    def _box(self, fill, bar, width=CONTENT_W):
        t = self.d.add_table(rows=1, cols=1)
        table_no_borders(t)
        table_width(t, width)
        set_col_widths(t, [width])
        c = t.rows[0].cells[0]
        shade(c, fill)
        cell_borders(c, left=(24, bar))
        cell_margins(c, 80, 80, 160, 140)
        no_split_row(t.rows[0])
        return c

    def directions(self, items, heading="Directions"):
        c = self._box(TINT, ACCENT)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        add_runs(p, heading, color=ACCENT, bold=True, size=10.5)
        for it in items:
            p = c.add_paragraph()
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.left_indent = Inches(0.18)
            p.paragraph_format.first_line_indent = Inches(-0.18)
            add_runs(p, "•  ", color=ACCENT, bold=True)
            add_runs(p, it, size=10.5)
        self.spacer(6)

    def callout(self, text, fill=AMBER_TINT, bar=AMBER, label=None):
        c = self._box(fill, bar)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        if label:
            add_runs(p, label + "  ", color=bar, bold=True)
        add_runs(p, text, size=10.5)
        self.spacer(6)
        return c

    def spacer(self, pts=4):
        p = self.d.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(pts)
        return p

    # ---- headings
    def section(self, text):
        p = self.d.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        keep_next(p)
        add_runs(p, text, color=SLATE, bold=True, size=14)
        para_border_bottom(p, color=RULE, sz=6, space=2)
        return p

    def subheading(self, text):
        p = self.d.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        keep_next(p)
        add_runs(p, text, color=ACCENT, bold=True, size=12)
        return p

    def problem(self, title, body=None):
        """'Problem 1. Title' heading followed by the scenario text."""
        p = self.d.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(3)
        keep_next(p)
        add_runs(p, title, color=SLATE, bold=True, size=13)
        para_border_bottom(p, color=ACCENT_LIGHT, sz=8, space=2)
        if body:
            for b in ([body] if isinstance(body, str) else body):
                self.para(b)

    def para(self, text, indent=0, size=None, color=None, italic=False, keep=False, after=4):
        p = self.d.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        if indent:
            p.paragraph_format.left_indent = Inches(indent)
        if keep:
            keep_next(p)
        add_runs(p, text, size=size, color=color, italic=italic)
        return p

    def bullets(self, items, indent=0.0):
        for it in items:
            p = self.d.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.left_indent = Inches(indent + 0.25)
            p.paragraph_format.first_line_indent = Inches(-0.17)
            add_runs(p, "•  ", color=ACCENT, bold=True)
            add_runs(p, it)

    def numbered(self, items, start=1, indent=0.0):
        for k, it in enumerate(items, start):
            p = self.d.add_paragraph()
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.left_indent = Inches(indent + 0.3)
            p.paragraph_format.first_line_indent = Inches(-0.3)
            add_runs(p, f"{k}.\t", color=ACCENT, bold=True)
            p.paragraph_format.tab_stops.add_tab_stop(Inches(indent + 0.3))
            add_runs(p, it)

    # ---- student space vs. answers
    def lines(self, n=1, indent=0.3):
        for _ in range(n):
            p = self.d.add_paragraph()
            p.paragraph_format.left_indent = Inches(indent)
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(0)
            para_border_bottom(p, color=RULE, sz=6)

    def workbox(self, height_in=1.2, indent=0.3, label=None):
        w = CONTENT_W - indent
        t = self.d.add_table(rows=1, cols=1)
        table_no_borders(t)
        table_width(t, w)
        tblPr = t._tbl.tblPr
        ind = OxmlElement("w:tblInd"); ind.set(qn("w:w"), str(int(indent * 1440))); ind.set(qn("w:type"), "dxa")
        tblPr.append(ind)
        set_col_widths(t, [w])
        row = t.rows[0]
        trPr = row._tr.get_or_add_trPr()
        h = OxmlElement("w:trHeight"); h.set(qn("w:val"), str(int(height_in * 1440))); h.set(qn("w:hRule"), "atLeast")
        trPr.append(h)
        no_split_row(row)
        c = row.cells[0]
        cell_borders(c, top=(6, RULE), left=(6, RULE), bottom=(6, RULE), right=(6, RULE))
        p = c.paragraphs[0]
        if label:
            add_runs(p, label, color=MUTED, italic=True, size=9)
        self.spacer(4)

    def answer(self, ans, indent=0.3):
        """Green answer block (answer key only)."""
        if not self.key or ans is None:
            return
        items = ans if isinstance(ans, (list, tuple)) else [ans]
        w = CONTENT_W - indent
        t = self.d.add_table(rows=1, cols=1)
        table_no_borders(t)
        table_width(t, w)
        tblPr = t._tbl.tblPr
        ind = OxmlElement("w:tblInd"); ind.set(qn("w:w"), str(int(indent * 1440))); ind.set(qn("w:type"), "dxa")
        tblPr.append(ind)
        set_col_widths(t, [w])
        c = t.rows[0].cells[0]
        shade(c, GREEN_TINT)
        cell_borders(c, left=(18, GREEN))
        cell_margins(c, 50, 50, 140, 120)
        for k, a in enumerate(items):
            p = c.paragraphs[0] if k == 0 else c.add_paragraph()
            p.paragraph_format.space_after = Pt(1)
            add_runs(p, a, color=GREEN)
        self.spacer(5)

    def step(self, label, prompt, ans=None, lines=1, box=None, indent=0.3):
        """A lettered part or numbered step. Students get ruled lines or a box; keys get the answer."""
        p = self.d.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Inches(indent)
        p.paragraph_format.first_line_indent = Inches(-0.3) if indent >= 0.3 else None
        keep_next(p)
        if label:
            add_runs(p, label + "  ", color=ACCENT, bold=True)
        add_runs(p, prompt)
        if self.key:
            self.answer(ans, indent=indent)
        elif box:
            self.workbox(box, indent=indent)
        elif lines:
            self.lines(lines, indent=indent)

    def formula(self, text, indent=0.6):
        p = self.d.add_paragraph()
        p.paragraph_format.left_indent = Inches(indent)
        p.paragraph_format.space_after = Pt(3)
        add_runs(p, text, font=MATH_FONT, size=11.5)
        return p

    # ---- tables
    def table(self, rows, widths=None, header_row=True, header_col=True, center=True, font_size=10.5):
        """rows: list of lists. A cell may be ('ans', value): blank for students, green value in keys."""
        ncol = len(rows[0])
        widths = widths or [min(CONTENT_W, 1.2 * ncol) / ncol] * ncol
        t = self.d.add_table(rows=len(rows), cols=ncol)
        table_width(t, sum(widths))
        set_col_widths(t, widths)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, row in enumerate(rows):
            no_split_row(t.rows[i])
            for j, val in enumerate(row):
                c = t.rows[i].cells[j]
                cell_borders(c, top=(4, RULE), left=(4, RULE), bottom=(4, RULE), right=(4, RULE))
                cell_margins(c, 50, 50, 90, 90)
                c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                is_head = (header_row and i == 0) or (header_col and j == 0)
                if header_row and i == 0:
                    shade(c, TABLE_HEAD)
                p = c.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                if center and not (header_col and j == 0):
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if isinstance(val, tuple) and val[0] == "ans":
                    if self.key:
                        add_runs(p, str(val[1]), color=GREEN, bold=True, size=font_size)
                    else:
                        p.paragraph_format.space_before = Pt(6)
                        p.paragraph_format.space_after = Pt(6)
                    continue
                add_runs(p, str(val), bold=is_head, size=font_size)
        self.spacer(6)
        return t

    def image(self, path, width_in, center=True):
        p = self.d.add_paragraph()
        if center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(6)
        p.add_run().add_picture(str(path), width=Inches(width_in))
        return p

    def page_break(self):
        p = self.d.add_paragraph()
        p.add_run().add_break(WD_BREAK.PAGE)

    def end(self, text="End"):
        p = self.d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(14)
        add_runs(p, f"—  {text}  —", color=MUTED, bold=True, size=10)

    def save(self, path):
        self.d.save(str(path))
