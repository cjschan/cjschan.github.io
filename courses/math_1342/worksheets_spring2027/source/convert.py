"""Rebuild the Fall practice tests and study guides in the shared look.

The original .docx is read with pandoc's JSON AST (text, tables, images kept as-is)
and re-laid-out with wslib.Doc, so no question is retyped by hand.
"""
import json
import re
import subprocess
from pathlib import Path

from wslib import Doc, CONTENT_W, AMBER, AMBER_TINT

SUBS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def _grp(x):
    """Parenthesize a fraction part only when it has a top-level + or - or space."""
    depth = 0
    for ch in x:
        depth += ch in "(["
        depth -= ch in ")]"
        if depth == 0 and ch in "+-− ":
            return f"({x})"
    return x


def tex2u(tex):
    """Tiny TeX -> readable Unicode for the few formulas in these documents.
    Non-digit subscripts and superscripts stay as wslib _{..} / ^{..} markup."""
    s = tex
    s = re.sub(r"\\left|\\right", "", s)
    s = s.replace("\\ ", " ").replace("\\,", " ")
    s = re.sub(r"p\\hat\{\}", "p\u0302", s)
    s = re.sub(r"\\(?:wide)?hat\{(\w)\}", lambda m: m.group(1) + "\u0302", s)
    s = re.sub(r"\\overline\{(\w)\}", lambda m: m.group(1) + "\u0304", s)
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    for k, v in {"\\pm": "±", "\\cdot": "·", "\\times": "×", "\\mu": "μ", "\\sigma": "σ",
                 "\\alpha": "α", "\\neq": "≠", "\\leq": "≤", "\\geq": "≥"}.items():
        s = re.sub(re.escape(k) + r"(?![A-Za-z])", f" {v} " if v in "±·×≠≤≥" else v, s)
    s = re.sub(r"_(\d)", lambda m: m.group(1).translate(SUBS), s)
    s = re.sub(r"_\{(\d+)\}", lambda m: m.group(1).translate(SUBS), s)
    s = re.sub(r"([_^])([A-Za-z*])(?![A-Za-z{])", r"\1{\2}", s)
    for _ in range(6):   # innermost first; protect _{..}/^{..} markup with control chars
        s = re.sub(r"_\{([^{}]*)\}", lambda m: "\x00" + m.group(1) + "\x01", s)
        s = re.sub(r"\^\{([^{}]*)\}", lambda m: "\x02" + m.group(1) + "\x01", s)
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", lambda m: _grp(m.group(1)) + "/" + _grp(m.group(2)), s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", r"√(\1)", s)
    s = re.sub(r"[{}]", "", s)
    s = s.replace("\x00", "_{").replace("\x02", "^{").replace("\x01", "}")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\(\s+", "(", s)
    s = re.sub(r"\s+\)", ")", s)
    s = re.sub(r"(?<=[\w)₀-₉̂̄]) - (?=[\w(√])", " − ", s)
    return s


def inl(xs):
    """pandoc inlines -> wslib markup string."""
    out = []
    for x in xs:
        t, c = x["t"], x.get("c")
        if t == "Str":
            out.append(re.sub(r"(?<![A-Za-z])([μσpsxn])_([A-Za-z0-9])(?![A-Za-z0-9])", r"\1_{\2}", c))
        elif t in ("Space", "SoftBreak"):
            out.append(" ")
        elif t == "LineBreak":
            out.append(" ")
        elif t == "Strong":
            inner = inl(c)
            out.append(f"**{inner}**" if inner.strip() else inner)
        elif t == "Emph":
            inner = inl(c)
            out.append(f"~~{inner}~~" if inner.strip() else inner)
        elif t in ("Underline", "SmallCaps", "Strikeout", "Span"):
            out.append(inl(c if t != "Span" else c[1]))
        elif t == "Subscript":
            out.append("_{" + inl(c) + "}")
        elif t == "Superscript":
            out.append("^{" + inl(c) + "}")
        elif t == "Quoted":
            q = "“%s”" if c[0]["t"] == "DoubleQuote" else "‘%s’"
            out.append(q % inl(c[1]))
        elif t == "Math":
            out.append(tex2u(c[1]))
        elif t == "Link":
            out.append(inl(c[1]))
        elif t == "Code":
            out.append(c[1])
        elif t == "Image":
            pass
    s = "".join(out)
    s = s.replace("****", "")
    s = re.sub(r"(?<=\))(?=[a-z]{3,})", " ", s)      # "…/n)using" -> "…/n) using"
    return s


def images_in(xs):
    res = []
    for x in xs:
        if x["t"] == "Image":
            attr, _alt, (src, _title) = x["c"]
            kv = dict(attr[2])
            w = kv.get("width", "4in")
            w = float(w[:-2]) if w.endswith("in") else 4.0
            res.append((src, w))
        elif isinstance(x.get("c"), list) and x["t"] in ("Strong", "Emph", "Span"):
            res.extend(images_in(x["c"] if x["t"] != "Span" else x["c"][1]))
    return res


def block_inlines(b):
    if b["t"] in ("Para", "Plain"):
        return b["c"]
    return []


def cell_text(cell):
    # cell = [attr, align, rowspan, colspan, blocks]
    return " ".join(inl(block_inlines(b)) for b in cell[4]).strip()


def table_rows(b):
    _attr, _cap, colspecs, head, bodies, foot = b["c"]
    rows, nhead = [], 0
    for r in head[1]:
        rows.append([cell_text(c) for c in r[1]]); nhead += 1
    for body in bodies:
        for r in body[2] + body[3]:
            rows.append([cell_text(c) for c in r[1]])
    widths = []
    for cs in colspecs:
        w = cs[1]
        widths.append(w["c"] if isinstance(w, dict) and w.get("t") == "ColWidth" else None)
    return rows, nhead, widths


def load_ast(docx, media_dir):
    out = subprocess.run(["pandoc", str(docx), "-t", "json", f"--extract-media={media_dir}"],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["blocks"]


def put_table(d: Doc, b, fill_cols_blank=False):
    rows, nhead, wfrac = table_rows(b)
    ncol = len(rows[0])
    if all(wfrac) and sum(wfrac) > 0:
        total = min(CONTENT_W, 6.6 if ncol > 3 else 6.2)
        widths = [total * w / sum(wfrac) for w in wfrac]
    else:
        widths = [min(CONTENT_W, 1.25 * ncol) / ncol] * ncol
    # a two-column reference table with no header row: bold the first column only
    d.table(rows, widths=widths, header_row=nhead > 0, header_col=True,
            center=ncol > 2, font_size=10)


def put_image(d: Doc, src, w):
    from alt_text import ALT
    key = "/".join(Path(src).parts[-3::2])          # media/pt2/media/image1.png -> pt2/image1.png
    d.image(src, min(w, 5.6), alt=ALT[key])


def render_blocks(d: Doc, blocks, indent=0.0, numbered_start=None):
    for b in blocks:
        t = b["t"]
        if t in ("Para", "Plain"):
            imgs = images_in(b["c"])
            text = inl(b["c"]).strip()
            for src, w in imgs:
                put_image(d, src, w)
            if text:
                d.para(text, indent=indent)
        elif t == "BulletList":
            for item in b["c"]:
                first = True
                for ib in item:
                    if ib["t"] in ("Para", "Plain"):
                        d.bullets([inl(ib["c"]).strip()], indent=indent) if first else d.para(inl(ib["c"]).strip(), indent=indent + 0.25)
                        first = False
                    else:
                        render_blocks(d, [ib], indent=indent + 0.25)
        elif t == "OrderedList":
            (start, _style, _delim), items = b["c"]
            start = numbered_start if numbered_start is not None else start
            for k, item in enumerate(items):
                txt = " ".join(inl(block_inlines(ib)).strip() for ib in item if ib["t"] in ("Para", "Plain"))
                d.numbered([txt], start=start + k, indent=indent)
        elif t == "Table":
            put_table(d, b)
        elif t == "BlockQuote":
            render_blocks(d, b["c"], indent=indent + 0.35)
        elif t == "Header":
            d.subheading(inl(b["c"][2]))


def practice_test(d: Doc, docx, media_dir, edit=None):
    blocks = load_ast(docx, media_dir)
    i = 0
    while not (blocks[i]["t"] == "Para" and inl(blocks[i]["c"]).strip("* ") == "Instructions"):
        i += 1
    instr = blocks[i + 1]
    items = [inl(block_inlines(x)).strip().lstrip("•").strip() for x in instr["c"]]
    if edit and hasattr(edit, "instructions"):
        items = edit.instructions(items)
    d.directions(items, heading="Instructions")
    body = blocks[i + 2:]
    if edit:
        body = edit(body)
    for b in body:
        t = b["t"]
        text = inl(b["c"]).strip() if t == "Para" else ""
        if t == "Para" and re.fullmatch(r"\*\*Section [A-Z]\..*\*\*", text):
            d.section(text.strip("*"))
        elif t == "Para" and text.strip("*").startswith("End of"):
            d.end("End of Practice Test")
        elif t == "Para" and re.match(r"\*\*\d+\.\*\*", text):
            num, rest = re.match(r"\*\*(\d+\.)\*\*\s*(.*)", text).groups()
            p = d.d.add_paragraph()
            from wslib import add_runs, keep_next, ACCENT
            from docx.shared import Pt, Inches
            p.paragraph_format.space_before = Pt(9)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.first_line_indent = Inches(-0.3)
            keep_next(p)
            add_runs(p, num + "  ", color=ACCENT, bold=True)
            add_runs(p, rest)
        elif t == "BlockQuote":
            for x in b["c"]:
                if x["t"] in ("Para", "Plain"):
                    xt = inl(x["c"]).strip()
                    m = re.match(r"\*\*(\([a-z]\))\*\*\s*(.*)", xt)
                    if m:
                        from wslib import add_runs, ACCENT
                        from docx.shared import Pt, Inches
                        p = d.d.add_paragraph()
                        p.paragraph_format.space_after = Pt(2)
                        p.paragraph_format.left_indent = Inches(0.65)
                        p.paragraph_format.first_line_indent = Inches(-0.32)
                        add_runs(p, m.group(1) + "  ", color=ACCENT, bold=True)
                        add_runs(p, m.group(2))
                    elif xt:
                        d.para(xt, indent=0.35)
                else:
                    render_blocks(d, [x], indent=0.35)
        else:
            render_blocks(d, [b])


def study_guide(d: Doc, docx, media_dir, n):
    blocks = load_ast(docx, media_dir)
    # leading paragraphs: course line, title, italic intro, "Test basics"
    paras = []
    i = 0
    while blocks[i]["t"] == "Para":
        paras.append(inl(blocks[i]["c"]).strip()); i += 1
    intro = [p for p in paras if p.startswith("~~") or p.startswith("This guide")]
    basics = [p for p in paras if p.startswith("**Test basics")]
    if intro:
        txt = intro[0].strip("~")
        txt = txt.replace("practice problems with answers at the end", "practice problems at the end")
        txt = txt.replace("a set of practice problems at the end", "a set of practice problems at the end")
        d.para(txt + f" Full worked solutions to the practice problems are in the separate **Test {n} Study Guide: Solutions** document.", italic=False)
    if basics:
        d.directions([basics[0].replace("**Test basics:**", "").strip()], heading="Test basics")
    in_practice = False
    for b in blocks[i:]:
        t = b["t"]
        if t == "Header":
            lvl, _attr, xs = b["c"]
            title = inl(xs).strip()
            if title.startswith("Practice Answers"):
                break
            if lvl == 1:
                d.section(title)
            else:
                d.subheading(title)
            in_practice = title.startswith("Practice Problems")
        elif t == "Para" and in_practice and inl(b["c"]).strip().startswith("~~Try these"):
            d.para(f"Try these without notes first, then check your work against the **Test {n} Study Guide: Solutions** document.", italic=True)
        elif t == "BlockQuote" and inl(block_inlines(b["c"][0])).strip().startswith("**Watch out"):
            txt = " ".join(inl(block_inlines(x)).strip() for x in b["c"])
            txt = txt.replace("**Watch out:**", "").strip()
            d.callout(txt, label="Watch out:")
        elif t == "Para" and re.fullmatch(r"\*\*Practice Answers\*\*", inl(b["c"]).strip()):
            break
        else:
            render_blocks(d, [b], numbered_start=1 if (in_practice and t == "OrderedList") else None)
