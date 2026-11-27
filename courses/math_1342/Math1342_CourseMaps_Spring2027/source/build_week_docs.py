# -*- coding: utf-8 -*-
"""Write the two Blackboard Documents for each Week module (Math 1342, Spring 2027):
  "Week N Introduction, Objectives, and Learning Guide"  -> week_docs/WeekNN_intro.html
  "Week N Learning Materials to Review"                  -> week_docs/WeekNN_materials.html
Content comes from course_map_data.py (same data as the course maps), plus a short introduction per week below.
Run:  /usr/bin/python3 build_week_docs.py   (also writes week_docs/preview.html with all 32 documents)
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "week_docs")
sys.path.insert(0, HERE)
import course_map_data as D  # noqa: E402

SITE = "https://cjschan.github.io/courses/math_1342/Math1342_CourseMaps_Spring2027"

# Introduction paragraph for each week: what it covers, how it connects, and a tip.
INTRO = {
1: "Welcome to Elementary Statistics! This first class asks a simple question: what is statistics for? We will collect "
   "real data from our own class, summarize it with a mean, a median and a boxplot, and ask whether a surprising result "
   "could have happened just by chance. That question, “could it be chance?”, comes back all semester and is the heart of "
   "hypothesis testing in Weeks 9–15. Before class on Wednesday, take the Start Here tour and read the syllabus: the Syllabus Quiz, the first of your 9 quizzes, is taken in class that day. After class, post in the Introductions and Statistics in Your Life discussion by Friday and reply to two classmates by Sunday.",
2: "This week we learn the language of data. In 1.1 you will identify cases and variables and decide whether each variable "
   "is categorical or quantitative. In 1.2 we ask how a sample can tell us about a whole population, and how a biased "
   "sampling method can ruin that. A common mistake: zip codes, phone numbers and ID numbers are categorical, even though "
   "they are written with digits. Ask whether it makes sense to average the values.",
3: "Last week we looked at how data are sampled. This week we look at how they are produced. In 1.3 you will tell an "
   "experiment from an observational study and see why only randomized experiments can show cause and effect. In 2.1 we "
   "start describing data, beginning with categorical variables: proportions, two-way tables and bar charts. Watch out for "
   "the difference between random sampling (who is in the study) and random assignment (who gets which treatment).",
4: "Now we describe one quantitative variable. In 2.2 you will describe the shape of a distribution and compare the mean and "
   "median, and you will read the standard deviation as a typical distance from the mean. In 2.3 we use z-scores, "
   "percentiles, the five-number summary and boxplots. Remember: the median resists outliers and skewness, but the mean "
   "is pulled toward the tail. Take-Home Quiz 1 is due Monday.",
5: "This week we move from one variable to two. In 2.4 you will compare groups with side-by-side boxplots and describe "
   "scatterplots with direction, form, strength and the correlation r. In 2.5 (Part 1) we fit a regression line, interpret "
   "its slope and intercept, make predictions and compute residuals. Correlation is not causation. A strong r alone never "
   "shows that x causes y.",
6: "We finish regression and begin probability. In 2.5 (Part 2) you will use technology to find the least-squares line and "
   "learn when a prediction should not be trusted (extrapolation). In P.1 we cover the probability rules: complement, "
   "addition, conditional probability and independence. Test 1 (Intro through 2.5) is this weekend. Use the study guide and "
   "the optional practice test.",
7: "This is where inference begins. In 3.1 you will see that a statistic changes from sample to sample, and that the "
   "sampling distribution and its standard error measure that variability. In 3.2 we use the standard error to build a "
   "confidence interval and interpret it correctly. The most common mistake: a 95% CI does not mean there is a 95% chance "
   "the parameter is in this particular interval. The 95% describes the method.",
8: "Last week we needed many samples to see a sampling distribution. This week the bootstrap lets us estimate one from a "
   "single sample. In 3.3 you will build a bootstrap distribution in StatKey and use its standard error for a 95% interval. "
   "In 3.4 you will use percentiles for 90%, 95% and 99% intervals. A bootstrap can't fix a biased sample. Spring Break "
   "follows this week.",
9: "Welcome back from Spring Break! This week starts hypothesis testing. In 4.1 you will define the parameter and write the "
   "null and alternative hypotheses. In 4.2 we build a randomization distribution, assuming H₀ is true, and measure the "
   "evidence with a p-value. Hypotheses are always about population parameters (p, μ), never about sample statistics "
   "(p̂, x̄).",
10: "Now that you can find a p-value, this week is about what to do with it. In 4.3 you will compare the p-value to a "
    "significance level α and write a conclusion in context. Never say “accept H₀”. In 4.4 we look at Type I and Type II "
    "errors, multiple testing, and statistical versus practical significance. Test 2 (P.1 through 4.3) is this weekend.",
11: "This week ties the course together. In 4.5 you will see how a confidence interval and a two-tailed test lead to the "
    "same decision, and when each fits a question. In 5.1 we replace the randomization distribution with the normal "
    "distribution, compute a z statistic and find p-values as areas under the normal curve. Draw and shade the curve "
    "every time you find a tail area.",
12: "We now apply formulas to specific parameters, starting with proportions. In 6.1 you will check conditions, build a CI "
    "and run a z test for one proportion. In 6.3 we compare two proportions with a pooled test and a CI for p₁ − p₂. "
    "Note that the CI's standard error uses p̂, while the test uses the null value p₀ (or the pooled p̂). Take-Home Quiz 5 "
    "is due Monday.",
13: "This week moves from proportions to means. In 6.2 you will use the t distribution (df = n − 1) for a confidence "
    "interval and a test about one mean. In 6.4 we compare two independent means. The order of the groups sets the sign "
    "of the difference, so define it clearly and keep it consistent from the hypotheses to the conclusion.",
14: "Two new designs this week. In 6.5 you will analyze paired data by computing the differences first and then running a "
    "one-sample t procedure on them. In 7.2 the chi-square test checks for an association between two categorical "
    "variables in a two-way table. Check that every expected count is at least 5. Monday is the last day to withdraw, and "
    "Test 3 (4.4 through 6.5) is this weekend.",
15: "This is the last week of new material. In 8.1, ANOVA compares the means of three or more groups using an F statistic, "
    "the ratio of variability between groups to variability within groups. In 9.1 we return to regression and test whether "
    "the slope (or correlation) in the population is really different from zero. A significant ANOVA tells you that some "
    "means differ, not which ones.",
16: "Putting it all together. Monday's review practices the key skill on the final: reading a research question and "
    "choosing the right procedure, then carrying out a complete test or interval and stating the conclusion in context. "
    "Use the review slides, the earlier Interactive Lectures and StatKey to prepare. The cumulative Final Exam runs Wed May "
    "12 – Fri May 14 in Blackboard.",
}

# Quizzes and tests that happen during each week (Mon–Sun).
DUE = {
1: ["Syllabus Quiz (Blackboard, taken in class Wed Jan 20, due at the end of class) – 10 multiple-choice questions on course dates and policies",
    "Discussion: Introductions and Statistics in Your Life (Blackboard, Participation, 10 points) – introduce yourself and describe where statistics shows up in your life; initial post due Fri Jan 22, 11:59 PM, two replies due Sun Jan 24, 11:59 PM"],
4: ["Take-Home Quiz 1 (due Mon Feb 8, 11:59 PM) – covers Intro, 1.1–1.3, 2.1"],
6: ["Take-Home Quiz 2 (due Mon Feb 22, 11:59 PM) – covers 2.2–2.4",
    "Test 1 Study Guide and Practice Test 1 (optional; due Thu Feb 25)",
    "Test 1 (Fri Feb 26 – Sun Feb 28, proctored) – covers Intro, 1.1–2.5"],
7: ["Test 1 Retake (optional; Mon Mar 1 – Sun Mar 7; higher score counts)"],
8: ["Take-Home Quiz 3 (due Mon Mar 8, 11:59 PM) – covers 2.5, P.1, 3.1–3.2"],
10: ["Take-Home Quiz 4 (due Mon Mar 29, 11:59 PM) – covers 3.3–3.4, 4.1–4.2",
     "Test 2 Study Guide and Practice Test 2 (optional; due Thu Apr 1)",
     "Test 2 (Fri Apr 2 – Sun Apr 4, proctored) – covers P.1, 3.1–4.3"],
11: ["Test 2 Retake (optional; Mon Apr 5 – Sun Apr 11; higher score counts)"],
12: ["Take-Home Quiz 5 (due Mon Apr 12, 11:59 PM) – covers 4.3–4.5, 5.1"],
14: ["Take-Home Quiz 6 (due Mon Apr 26, 11:59 PM) – covers 6.1–6.4",
     "Test 3 Study Guide and Practice Test 3 (optional; due Thu Apr 29)",
     "Test 3 (Fri Apr 30 – Sun May 2, proctored) – covers 4.4–6.5"],
15: ["Take-Home Quiz 7 (due Mon May 3, 11:59 PM) – covers 6.5, 7.2",
     "Test 3 Retake (optional; Mon May 3 – Sun May 9; higher score counts)"],
16: ["Take-Home Quiz 8 (due Mon May 10, 11:59 PM) – covers 8.1, 9.1",
     "Final Exam (Wed May 12 – Fri May 14; Blackboard, proctored, 2 hours, cumulative; no retake)"],
}

ALT = {}
with open(os.path.join(os.path.dirname(HERE), "module_images", "alt_text.txt"), encoding="utf-8") as fh:
    for line in fh:
        k, v = line.rstrip("\n").split("\t", 1)
        ALT[k] = v


def e(s):
    return html.escape(s, quote=True)


NOTES = "https://cjschan.github.io/courses/math_1342/lecture_notes/"
_FILES = sorted(os.listdir(os.path.join(HERE, "..", "..", "lecture_notes")))


def slide_url(item):
    """Lecture-notes slide deck URL for a Slides item, or None."""
    if "Introduction Slides" in item:
        return NOTES + "Sec0-1_Introduction_to_Statistics.html"
    if "Review Slides: Putting" in item:
        return NOTES + "Review_Sampling_to_Hypothesis_Testing.html"
    m = re.search(r"Slides: ([0-9P])\.(\d)", item)
    if not m:
        return None
    pre = f"Sec{m.group(1)}-{m.group(2)}_"
    part = re.search(r"\(Part (\d)\)", item)
    if part:   # a section taught over two days has one deck per day, e.g. Sec2-5_..._Part1.html
        f = next((x for x in _FILES if x.startswith(pre) and x.endswith(f"_Part{part.group(1)}.html")), None)
    else:
        f = next((x for x in _FILES if x.startswith(pre) and x.endswith(".html") and "_Part" not in x), None)
    return NOTES + f if f else None


def li(i):
    u = slide_url(i)
    return f'<li><a href="{u}" target="_blank">{e(i)}</a></li>' if u else f"<li>{e(i)}</li>"


def ul(items, tag="ul"):
    return f"<{tag}>" + "".join(li(i) for i in items) + f"</{tag}>"


def is_participation(a):
    return a.startswith("Participation:")


def intro_doc(w):
    n = w["num"]
    rows = w["rows"]
    guide = []
    for r in rows:
        mats = [m for m in r["materials"] if not m.startswith("StatKey")]
        verb = lambda m: ("Read " if m.startswith("e-Text") else "Work through " if m.startswith("Interactive") else "Review ")
        guide += [verb(m) + m for m in mats if not m.startswith("START HERE")]
        if r["key"] == "Intro":
            guide.insert(0, "Review the START HERE module: Welcome, Syllabus, Textbook and Wiley Course Resources, Online Tutoring, College Policies")
        guide += [f"In class: {a}" for a in r["activities"]]
        guide += [a for a in r["assessments"] if a.startswith("Online Homework")]
    guide += DUE.get(n, [])
    guide += [a for a in w["also"] if "Retake" not in a]
    mlos, k = [], 0
    for r in rows:
        for text, clos in r["mos"]:
            k += 1
            mlos.append(f"<li><strong>MLO {k}:</strong> {e(text)} (CLO {', '.join(map(str, clos))})</li>")
    img = f"{SITE}/module_images/Week{n:02d}.png"
    return (f"<h3>Introduction</h3><p>{e(INTRO[n])}</p>"
            f"<p>This week covers: {e('; '.join(w['sections']))}.</p>"
            f"<h3>Learning Guide</h3>"
            f"<p>Below is the list of activities to complete this week to reach the objectives. All of the content you need "
            f"is listed on the Week {n} Learning Materials to Review page and in this week's module.</p>"
            f"<p>By the deadlines in the Course Schedule, complete the following:</p>{ul(guide, 'ol')}"
            f"<h3>Objectives</h3>"
            f"<p>The Week Level Objectives (MLOs) below state what you will be able to do by the end of this week. Each one "
            f"builds toward the Course Level Objectives (CLOs) shown in parentheses. The "
            f'<a href="{SITE}/Sec029/Week{n:02d}.pdf" target="_blank">Week {n} Course Map</a> shows how this week\'s '
            f"materials and activities line up with these objectives.</p>"
            f"<ul>{''.join(mlos)}</ul>"
            f'<p><img src="{img}" alt="{e(ALT[f"Week{n:02d}"])}" width="300" height="300"></p>')


def materials_doc(w):
    n = w["num"]
    req, prac, opt = [], [], []
    for r in w["rows"]:
        for m in r["materials"]:
            if m.startswith("START HERE"):
                req.append("START HERE module: Welcome; Syllabus; Textbook and Wiley Course Resources; Online Tutoring; College Policies & Student Support Services")
            elif m.startswith("StatKey") or m == "StatKey":
                prac.append(m if m != "StatKey" else "StatKey (lock5stat.com/statkey)")
            else:
                req.append(m)
        prac += r["activities"]
    if any("Test" in d and "Study Guide" in d for d in DUE.get(n, [])):
        t = next(d for d in DUE[n] if "Study Guide" in d)
        opt.append(t)
    if n == 16:
        opt.append("Practice Tests 1–3 and Study Guides 1–3 from earlier weeks")
    out = (f"<h3>Required Readings and Lectures</h3>"
           f"<p>Read the e-Text section, then work through its Interactive Lecture. The Slides are the ones we use in class.</p>"
           f"{ul(req)}"
           f"<h3>Practice and Class Activities</h3>"
           f"<p>These are the activities we do in class this week. Participation items are completed in class.</p>{ul(prac)}")
    if opt:
        out += f"<h3>Optional</h3>{ul(opt)}"
    out += ("<h3>Week References</h3><p>Lock, R. H., Lock, P. F., Lock Morgan, K., Lock, E. F., &amp; Lock, D. F. "
            "<em>Statistics: Unlocking the Power of Data</em> (4th ed.). Wiley (WileyPlus). StatKey: lock5stat.com/statkey.</p>")
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    preview = ['<!doctype html><meta charset="utf-8"><style>body{font-family:Arial;max-width:900px;margin:20px auto}'
               'section{border:2px solid #ccc;padding:10px 20px;margin:20px 0}</style>']
    for w in D.WEEKS:
        n = w["num"]
        for kind, fn, title in (("intro", intro_doc, f"Week {n} Introduction, Objectives, and Learning Guide"),
                                ("materials", materials_doc, f"Week {n} Learning Materials to Review")):
            body = fn(w)
            with open(os.path.join(OUT, f"Week{n:02d}_{kind}.html"), "w", encoding="utf-8") as fh:
                fh.write(body)
            preview.append(f"<section><h2>{e(title)}</h2>{body}</section>")
    # Blocks for pasting into the Blackboard document template (header, then one HTML string per text block).
    blocks = {}
    for w in D.WEEKS:
        n = w["num"]
        parts = intro_doc(w).split("<h3>")
        img = parts[3].split("<p><img", 1)
        obj = img[0].replace("<h3>", "")
        blocks[n] = {
            "intro": [f"<h2>Week {n} Introduction, Objectives, and Learning Guide</h2>",
                      "<h3>" + parts[1], "<h3>" + parts[2], "<h3>" + obj,
                      "<p><img" + img[1]],
            "materials": [f"<h2>Week {n} Learning Materials to Review</h2>", materials_doc(w)],
        }
    with open(os.path.join(OUT, "blocks.json"), "w", encoding="utf-8") as fh:
        json.dump(blocks, fh, ensure_ascii=False)
    with open(os.path.join(OUT, "preview.html"), "w", encoding="utf-8") as fh:
        fh.write("".join(preview))
    print("wrote", len(D.WEEKS) * 2, "documents to", OUT)


if __name__ == "__main__":
    main()
