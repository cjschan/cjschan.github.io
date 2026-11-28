"""Blackboard instruction text ("prelude") for the 10 worksheet participation assignments.

    python3 instructions.py      ->  ../instructions/<stem>.html

Each snippet is pasted into the assignment's Instructions, above the attached worksheet.
Sections follow the ACC assignment template: title, what/how to submit, criteria for success,
resources permitted / not permitted.
"""
from pathlib import Path

from worksheets import WORKSHEETS

OUT = Path(__file__).resolve().parent.parent / "instructions"

# stem -> (total points, [(problem label, points)], extra-credit note or None, uses StatKey screenshots?)
POINTS = {
    "W08_CI_Using_Percentiles": (15, [
        ("Problem 1. Body Temperature, parts (a)–(h)", "8 (1 per part)"),
        ("Problem 2. Ovulating Women and Men's Speech", "3"),
        ("Problem 3. Problems with Bootstrap Distributions, parts (a)–(d)", "4 (1 per part)")], None, True),
    "W10_Determining_Statistical_Significance": (15, [
        ("Problem 1. Red Wine and Weight Loss, parts (a)–(c)", "3 (1 per part)"),
        ("Problem 2. Multiple Sclerosis and Sunlight", "2"),
        ("Problem 3. Determining Significance, parts (a)–(b)", "4 (2 per part)"),
        ("Problem 4. Making Conclusions, questions 1–2", "2 (1 each)"),
        ("Problem 5. Playing with StatKey, parts (a)–(d)", "4 (1 per part)")], None, True),
    "W12_Proportion_Test_and_CI": (9, [
        ("Mendel's Green Peas, Steps 1–9", "9 (1 per step)")], None, False),
    "W12_Difference_in_Proportions": (10, [
        ("Part (a). Conditions (Step 1)", "1"),
        ("Part (b). Sample proportions (Step 2)", "1"),
        ("Part (c). Hypothesis test (Steps 3–10)", "6"),
        ("Part (d). Confidence interval (Steps 11–12)", "2")], None, False),
    "W13_Inference_for_a_Mean": (17, [
        ("Problem 1. Cell Phone Calls, Steps 1–8", "8 (1 per step)"),
        ("Problem 2. Penalty Minutes in Hockey Games, Steps 1–9", "9 (1 per step)")], None, False),
    "W13_Difference_in_Means": (10, [
        ("Problem 1. Music While Studying, Steps 1–10", "10 (1 per step)")],
        "<b>Problem 2 (Smiles and Leniency) is extra credit:</b> up to 5 more points, on top of the 10.", False),
    "W14_Paired_Difference_in_Means": (15, [
        ("Problem 1. Why Paired Data?", "1"),
        ("Problem 2. Hypothesis Test, Steps 1–9", "9 (1 per step)"),
        ("Problem 3. Confidence Interval, Steps 1–5", "5 (1 per step)")], None, False),
    "W14_Association_Two_Categorical": (9, [
        ("Study Method and Passing the Exam, parts (a)–(i)", "9 (1 per part)")], None, False),
    "W15_Analysis_of_Variance": (9, [
        ("Fiber in Breakfast Cereals, Steps 1–9", "9 (1 per step)")], None, False),
    "W15_Inference_for_Slope_and_Correlation": (7, [
        ("Alcohol and Missed Classes, parts (a)–(g)", "7 (1 per part)")], None, False),
}


# Assignments where Blackboard's "Prohibit late submissions" is OFF (so don't claim it).
LATE_OK = set()


def html(stem, title, sub):
    total, rows, extra, statkey = POINTS[stem]
    week_sec = " · ".join(sub.split("  ·  ")[:2])
    def pts(b):
        n, _, rest = b.partition(" ")
        return f"{n} point{'s' if n != '1' else ''}" + (f" {rest}" if rest else "")
    table = "".join(f"<li>{a}: <strong>{pts(b)}</strong></li>" for a, b in rows)
    shot = "<li>StatKey screenshots pasted where the worksheet asks for them</li>" if statkey else ""
    shot_do = (" Where a problem asks for it, paste a screenshot of your StatKey output into the worksheet." if statkey else "")
    return f"""<h4>Participation: {title}</h4>
<p><em>{week_sec}</em></p>
<p><strong>What to do and submit</strong></p>
<ul>
<li>We work through this worksheet in class. Work with a neighbor, but write your own answers.</li>
<li>Download the worksheet below and type your answers into it.{shot_do}</li>
<li>Upload <strong>one file</strong> to this assignment: the completed worksheet, saved as a .docx or PDF.</li>
<li>Submit by the due date shown on this assignment.{" Late submissions aren't accepted." if stem not in LATE_OK else ""}</li>
</ul>
<p><strong>Criteria for success ({total} points)</strong></p>
<p>This is graded on completion and effort. A part earns its points when you attempt it and show your work; your answers don't have to be perfect.</p>
<p>Points:</p>
<ul>{table}</ul>
{f"<p>{extra}</p>" if extra else ""}
<p>Before you submit, check that you have:</p>
<ul>
<li>attempted every part</li>
<li>shown the formula and the numbers you plugged in on each calculation</li>
{shot}
<li>written hypotheses and conclusions in the context of the problem</li>
</ul>
<p>The answer key opens at 12:00 AM the day after the due date. Use it to check your work.</p>
<p><strong>Resources</strong></p>
<ul>
<li><strong>Allowed:</strong> your notes, the e-Text, StatKey, a scientific calculator, and help from classmates and me during class.</li>
<li><strong>Generative AI:</strong> allowed on un-proctored work like this, under the course GAI policy in the syllabus. Use it with caution; the answers you submit must be your own.</li>
<li><strong>Not allowed:</strong> copying another student's worksheet, or submitting work you didn't do.</li>
</ul>
<p><strong>Worksheet:</strong></p>"""


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for stem, title, sub, _ in WORKSHEETS:
        (OUT / f"{stem}.html").write_text(html(stem, title, sub).replace("\n\n", "\n"))
    print("wrote", len(WORKSHEETS), "snippets to", OUT)
