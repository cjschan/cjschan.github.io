"""Structural edits applied to a practice test's pandoc blocks before rendering.

Practice Test 2 was cut from 19 to 14 questions (still 100 points) and given correlation
parts, to match the Spring 2027 online Test 2 / Practice Test 2 in Blackboard.
"""
import re

from convert import inl

SEC = re.compile(r"\*\*Section ([A-Z])\.(.*?)\((\d+) points\)\*\*")
QNUM = re.compile(r"\*\*(\d+)\.\*\*\s*")
PTS = re.compile(r"\*\*\((\d+) pts\)\*\*")


def S(text):
    """A pandoc Para whose single Str carries wslib markup (rendered by practice_test)."""
    return {"t": "Para", "c": [{"t": "Str", "c": text}]}


def part(letter, text):
    return S(f"**({letter})** {text}")


def parse(items):
    """-> list of sections: {'head': block, 'qs': [{'head': text, 'blocks': [...]}]}, plus tail blocks."""
    secs, tail = [], []
    for b in items:
        text = inl(b["c"]).strip() if b["t"] == "Para" else ""
        if b["t"] == "Para" and SEC.fullmatch(text):
            secs.append({"title": text, "qs": []})
        elif b["t"] == "Para" and text.strip("*").startswith("End of"):
            tail.append(b)
        elif b["t"] == "Para" and QNUM.match(text):
            secs[-1]["qs"].append({"head": QNUM.sub("", text, count=1), "blocks": []})
        else:
            secs[-1]["qs"][-1]["blocks"].append(b)
    return secs, tail


def parts_of(q):
    """Lettered-part texts of a question (from its BlockQuotes)."""
    out = []
    for b in q["blocks"]:
        if b["t"] == "BlockQuote":
            for x in b["c"]:
                if x["t"] in ("Para", "Plain"):
                    out.append(inl(x["c"]).strip())
    return out


def last_letter(q):
    ls = [re.match(r"\*\*\(([a-z])\)\*\*", p) for p in parts_of(q)]
    ls = [m.group(1) for m in ls if m]
    return ls[-1] if ls else None


def add_parts(q, texts):
    """Append new lettered parts (continuing the question's letters)."""
    nxt = ord(last_letter(q)) + 1
    paras = [part(chr(nxt + k), t) for k, t in enumerate(texts)]
    bqs = [b for b in q["blocks"] if b["t"] == "BlockQuote"]
    if bqs:
        bqs[-1]["c"].extend(paras)
    else:
        q["blocks"].append({"t": "BlockQuote", "c": paras})


def merge(target, src):
    """Move src into target: src's stem becomes a plain line, its parts are relettered to continue."""
    nxt = ord(last_letter(target)) + 1
    stem = PTS.sub("", src["head"]).strip()
    src_parts = parts_of(src)
    new = []
    if src_parts:
        new.append(S(stem))
        for p in src_parts:
            m = re.match(r"\*\*\(([a-z])\)\*\*\s*(.*)", p)
            new.append(part(chr(nxt), m.group(2)) if m else S(p))
            nxt += 1
    else:
        new.append(part(chr(nxt), stem))
    bqs = [b for b in target["blocks"] if b["t"] == "BlockQuote"]
    bqs[-1]["c"].extend(new)
    # carry over any non-text blocks (figures, tables) from src
    target["blocks"].extend(b for b in src["blocks"] if b["t"] != "BlockQuote")


def set_pts(q, n):
    q["head"] = PTS.sub(f"**({n} pts)**", q["head"]) if PTS.search(q["head"]) else q["head"] + f" **({n} pts)**"


def rebuild(secs, tail):
    out = []
    for s in secs:
        total = sum(int(PTS.search(q["head"]).group(1)) for q in s["qs"])
        m = SEC.fullmatch(s["title"])
        out.append(S(f"**Section {m.group(1)}.{m.group(2)}({total} points)**"))
        for k, q in enumerate(s["qs"], 1):
            out.append(S(f"**{k}.** {q['head']}"))
            out.extend(q["blocks"])
    return out + tail


def pt2(items):
    secs, tail = parse(items)
    A, B, C, D, E = (s["qs"] for s in secs)

    # Section A: drop Q1 (repeats Q2); Q2 gets a correlation part
    a2 = A[1]
    add_parts(a2, ["The correlation between hours of screen time and hours of sleep, computed from a random sample of 90 teenagers."])
    set_pts(a2, 5)
    secs[0]["qs"] = [a2, A[2]]

    # Section B: Q1 absorbs Q2 (+ a correlation CI part); Q4 absorbs Q6
    merge(B[0], B[1])
    add_parts(B[0], ["r = 0.38, the correlation between hours of exercise and hours of sleep for a random sample of adults, with standard error 0.12."])
    set_pts(B[0], 10)
    merge(B[3], B[5])
    set_pts(B[3], 9)
    secs[1]["qs"] = [B[0], B[2], B[3], B[4]]

    # Section C: hypotheses get a correlation part
    add_parts(C[0], ["Test whether there is a negative correlation between hours of screen time per day and hours of sleep per night for teenagers."])
    set_pts(C[0], 8)

    # Section D: drop Q4 (multiple-choice conclusion); Q3 gets a correlation CI part
    add_parts(D[2], ["A 95% confidence interval for ρ, the correlation between daily temperature and ice-cream sales, is −0.08 to 0.41. Testing H₀: ρ = 0 vs Hₐ: ρ ≠ 0."])
    set_pts(D[2], 8)
    secs[3]["qs"] = D[:3]

    # Section E: Q2 absorbs Q3
    merge(E[1], E[2])
    set_pts(E[1], 8)
    secs[4]["qs"] = E[:2]

    return rebuild(secs, tail)


# ---------------------------------------------------------------- Practice Test 3
# Give the same things Test 3 gives in every computation question: the SE formula,
# z*/t* and df, and the single tail area beyond the actual test statistic.
PT3_REPLACE = [
    ("(Areas in one tail of the standard normal curve are about 0.012 beyond z = 2.25, 0.007 beyond z = 2.45, and 0.004 beyond z = 2.65.)",
     "(In a standard normal curve, the area beyond z = 2.45 in one tail is about 0.007.)"),
    ("(In a t-distribution with df = 17, the area in one tail is about 0.146 beyond t = 1.09, 0.107 beyond t = 1.29, and 0.077 beyond t = 1.49.)",
     "(In a t-distribution with df = 17, the area beyond t = 1.29 in one tail is about 0.107.)"),
    ("For 99% confidence, t* = 2.797 when df = 24 and t* = 2.787 when df = 25.",
     "For 99% confidence with df = 24, use t* = 2.797."),
    ("Why do we use a t-distribution here, and which df is correct?",
     "Why do we use a t-distribution here instead of the normal distribution?"),
    ("(Areas in one tail of the standard normal curve are about 0.027 beyond z = 1.93, 0.017 beyond z = 2.13, and 0.010 beyond z = 2.33.)",
     "(The pooled proportion is 252/2700 = 0.0933, and the area beyond z = 2.13 in one tail is about 0.017.)"),
    ("Use the conservative degrees of freedom.", "Use df = 21."),
    ("(In a t-distribution with df = 21, the area in one tail is about 0.073 beyond t = 1.51, 0.051 beyond t = 1.71, and 0.035 beyond t = 1.91.)",
     "(In a t-distribution with df = 21, the area beyond t = 1.71 in one tail is about 0.051.)"),
    ("(In a t-distribution with df = 9, the area in one tail is about 0.008 beyond t = 2.96, 0.006 beyond t = 3.16, and 0.004 beyond t = 3.36.)",
     "(In a t-distribution with df = 9, the area beyond t = 3.16 in one tail is about 0.006.)"),
]

# (section, question number) -> the "Use ..." line added under the question stem
PT3_USE = {
    ("B", 1): "Use SE = √( p₀(1 − p₀) / n ).",
    ("B", 2): "For 95% confidence, use z* = 1.96. Use SE = √( p̂(1 − p̂) / n ).",
    ("B", 3): "Use n = (z* / ME)² · p̂(1 − p̂), where p̂ is the estimate from the previous survey.",
    ("C", 1): "Use SE = s / √n.",
    ("C", 2): "Use SE = s / √n.",
    ("D", 1): "Use SE = √( p̂(1 − p̂)(1/n_{A} + 1/n_{B}) ), where p̂ is the pooled proportion.",
    ("D", 2): "For 95% confidence, use z* = 1.96. Use SE = √( p̂_{A}(1 − p̂_{A})/n_{A} + p̂_{B}(1 − p̂_{B})/n_{B} ).",
    ("E", 1): "Use SE = √( s₁²/n₁ + s₂²/n₂ ).",
    ("E", 2): "Use SE = s_{d} / √n_{d}.",
}


def _fix(text):
    for o, n in PT3_REPLACE:
        text = text.replace(o, n)
    return text


def pt3(items):
    secs, tail = parse(items)
    for s in secs:
        letter = SEC.fullmatch(s["title"]).group(1)
        for k, q in enumerate(s["qs"], 1):
            q["head"] = _fix(q["head"])
            for b in q["blocks"]:
                if b["t"] == "BlockQuote":
                    b["c"] = [S(_fix(inl(x["c"]).strip())) if x["t"] in ("Para", "Plain") else x for x in b["c"]]
            use = PT3_USE.get((letter, k))
            if use:
                q["blocks"].insert(0, {"t": "BlockQuote", "c": [S(use)]})
    return rebuild(secs, tail)


pt3.instructions = lambda items: [
    it.replace("Each problem gives you any curve areas and t* values you need",
               "Each problem gives you the standard error formula, the z* or t* value, and any curve areas you need")
    for it in items]
