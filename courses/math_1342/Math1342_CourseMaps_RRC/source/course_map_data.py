# -*- coding: utf-8 -*-
"""
Content for the Math 1342 weekly course maps – Fall 2026, Section 019 (MW, RRC Room 8210, in person).
Week grouping follows the Blackboard course outline (course _970761_1) and the MW syllabus.
Resource names follow the new Blackboard naming convention:
  e-Text: x.x Title | Interactive Lecture: x.x Title | Slides: x.x Title | Online Homework: x.x Title
Edit this file and re-run build_course_maps.py to regenerate the PDFs.

Each week dict:
  num, title, dates, sections (list of str)
  rows: table rows; each row has mos (list of (objective_text, [CLO numbers])) and the materials,
        activities and assessments (lists of str) that align to those objectives. Objectives are
        numbered across rows. A Take-Home Quiz or test goes in every row it covers, with "(all objectives)"
        or "(objectives a–b)" at the end of its text.
  also: items that week that are not tied to its objectives (test sittings, retakes), printed under the table
"""

COURSE = "MATH 1342 – Elementary Statistics"
TERM = "Fall 2026 · Section 019 · MW 7:30–8:50 PM · RRC Room 8210"

COURSE_OBJECTIVES = [   # Course Level Objectives (CLOs), revised Oct 6, 2026
    "Explain the use of data collection and statistics as tools to reach reasonable conclusions.",
    "Recognize, examine, and interpret the basic principles of describing and presenting data.",
    "Compute and interpret empirical and theoretical probabilities using the rules of probabilities and combinatorics.",
    "Explain the role of probability in statistics.",
    "Examine, analyze, and compare various sampling distributions for both discrete and continuous random variables.",
    "Describe and compute confidence intervals.",
    "Solve linear regression and correlation problems.",
    "Perform hypothesis testing using statistical methods.",
]

# Tool listed for live class activities (Participation items without Kahoot!/StatKey).
LIVE_TOOL = None

TITLES = {
    "1.1": "The Structure of Data", "1.2": "Sampling from a Population", "1.3": "Experiments and Observational Studies",
    "2.1": "Categorical Variables", "2.2": "One Quantitative Variable", "2.3": "One Quantitative Variable: Using Percentiles",
    "2.4": "Two Variable Relationships", "2.5": "Two Quantitative Variables: Linear Regression",
    "P.1": "Probability Rules", "3.1": "Sampling Distributions",
    "3.2": "Understanding and Interpreting Confidence Intervals", "3.3": "Constructing Bootstrap Confidence Intervals",
    "3.4": "Bootstrap Confidence Intervals Using Percentiles", "4.1": "Introducing Hypothesis Tests",
    "4.2": "Measuring Evidence with P-Values", "4.3": "Determining Statistical Significance",
    "4.4": "A Closer Look at Testing", "4.5": "Making Connections", "5.1": "Hypothesis Tests Using Normal Distributions",
    "6.1": "Inference for a Proportion", "6.3": "Inference for a Difference in Proportions", "6.2": "Inference for a Mean",
    "6.4": "Inference for a Difference in Means", "6.5": "Paired Difference in Means",
    "7.2": "Testing for an Association Between Two Categorical Variables", "8.1": "Analysis of Variance",
    "9.1": "Inference for Slope and Correlation",
}
def etext(sec, suffix=""):   return f"e-Text: {sec} {TITLES[sec]}{suffix}"
def lecture(sec, suffix=""): return f"Interactive Lecture: {sec} {TITLES[sec]}{suffix}"
def slides(sec, suffix=""):  return f"Slides: {sec} {TITLES[sec]}{suffix}"
def hw(sec, due, suffix=""): return f"Online Homework: {sec} {TITLES[sec]}{suffix} (due Sun {due}, 11:59 PM)"
def etext3(sec, what):
    """Three separate e-Text items (CI, D, HT) as Blackboard lists them for the 6.x sections."""
    return [f"e-Text: {sec}-CI Confidence Interval for {what}",
            f"e-Text: {sec}-D Distribution of {what}",
            f"e-Text: {sec}-HT Hypothesis Test for {what}"]
def pack(sec, etext_suffix="", slides_suffix=""):
    """e-Text, Interactive Lecture and Slides for one section."""
    return [etext(sec, etext_suffix), lecture(sec), slides(sec, slides_suffix)]
def part(topic):     return f"Participation: {topic}"
def proposed(topic): return f"Participation: {topic}"

# Take-Home Quizzes: due date (Blackboard) and the sections each quiz covers (from quizzes_fall2026/).
# A quiz is listed in every row whose objectives it covers, in the week that teaches them.
QUIZZES = {
    1: ("Wed Sep 9", "Intro, 1.1–1.3"), 2: ("Mon Sep 21", "2.1–2.3"), 3: ("Mon Oct 5", "2.4–2.5"),
    4: ("Mon Oct 12", "3.1–3.3"), 5: ("Mon Oct 26", "4.1–4.3"), 6: ("Mon Nov 2", "4.4–4.5"),
    7: ("Mon Nov 16", "6.1–6.3"), 8: ("Mon Nov 23", "6.5"),
}
def quiz(n, objectives="all objectives"):
    """objectives is shown in gray after the quiz, e.g. 'all objectives' or 'objectives 9–12'."""
    due, covers = QUIZZES[n]
    return f"Take-Home Quiz {n} (due {due}, 11:59 PM) – covers {covers} ({objectives})"

# Test N, its study guide and practice test go in every row whose objectives the test covers.
TESTS = {   # n: (test dates, practice test due, sections covered)
    1: ("Fri Oct 2 – Sun Oct 4", "Thu Oct 1", "Intro, 1.1–2.5"),
    2: ("Fri Oct 30 – Sun Nov 1", "Thu Oct 29", "P.1, 3.1–4.3"),
    3: ("Fri Nov 20 – Sun Nov 22", "Thu Nov 19", "4.4–6.5"),
}
def test(n, objectives="all objectives"):
    dates, practice, covers = TESTS[n]
    return [f"Test {n} ({dates}, proctored) – covers {covers} ({objectives})",
            f"Test {n} Study Guide ({objectives})",
            f"Practice Test {n} (optional; due {practice}) ({objectives})"]

def row(mos, materials, activities, assessments):
    return dict(mos=mos, materials=materials, activities=activities, assessments=assessments)

WEEKS = [
# ---------------------------------------------------------------- Week 1
dict(num=1, title="Introduction and the Structure of Data", dates="Aug 24 – 26",
     sections=["Introduction: What Is Statistics For?", "1.1 The Structure of Data"],
     rows=[
      row([("Describe statistics as the process of collecting, describing, and analyzing data.", [1]),
           ("Explain how to judge a striking result by how likely it is to occur by chance alone.", [4]),
           ("Distinguish a sample from a population.", [1]),
           ("Explain how a non-representative sample biases an estimate.", [1]),
           ("Compute the mean and median of a small dataset.", [2]),
           ("Explain how an outlier affects the mean and the median.", [2])],
          ["START HERE: Welcome; Syllabus; Textbook and Wiley Course Resources; Online Tutoring; College Policies & Student Support Services",
           "Introduction Slides: What Is Statistics For? (Day 1)"],
          [part("Syllabus") + " – course tour and expectations",
           "Day-1 class data activity: collect everyone's age, then find the mean, median, mode and boxplot together; compare the class median to the U.S. median age"],
          [quiz(1)] + test(1)),
      row([("Identify the cases and variables in a dataset presented as a table.", [2]),
           ("Classify a variable as categorical or quantitative.", [2]),
           ("Identify the explanatory and response variables in a research question.", [1])],
          pack("1.1"),
          [part("Variables") + " – identify cases, variables and variable types; Your Turn: Used Cars: Cases and Variables"],
          [hw("1.1", "Aug 30"), quiz(1)] + test(1)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 2
dict(num=2, title="Sampling, Experiments and Observational Studies", dates="Aug 31 – Sep 2",
     sections=["1.2 Sampling from a Population", "1.3 Experiments and Observational Studies"],
     rows=[
      row([("Distinguish a population from a sample.", [1]),
           ("Explain how statistical inference uses sample data to draw conclusions about a population.", [1]),
           ("Identify sampling bias and classify the sampling method (random, convenience, or volunteer) in a described study.", [1]),
           ("Evaluate whether a study’s results can be generalized to the population.", [1]),
           ("Recognize bias from question wording, question context, and inaccurate responses.", [1])],
          pack("1.2", slides_suffix=" (includes sampling video)"),
          [part("Variables in Statistics (Kahoot!)") + " – Mon: review of Week 1",
           part("Sampling") + " – spot the bias in sample scenarios; Your Turn: Name the Bias",
           part("Sampling Methods (Kahoot!)") + " – Wed: sampling review"],
          [hw("1.2", "Sep 6"), quiz(1)] + test(1)),
      row([("Classify a study as observational or experimental.", [1]),
           ("Identify a plausible confounding variable in an observational study.", [1]),
           ("Explain how random assignment, a control group, and blinding support cause-and-effect conclusions.", [1]),
           ("Distinguish random sampling from random assignment.", [1])],
          pack("1.3", slides_suffix=" (includes TED-Ed placebo video)"),
          [part("Experiments and Observational Studies") + " – classify studies; confounding; random sampling vs. random assignment; Your Turn: Study Design and Scope of Inference (coffee and depression; vitamin D experiment)"],
          [hw("1.3", "Sep 6"), quiz(1)] + test(1)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 3
dict(num=3, title="Categorical Variables", dates="Sep 7 – 9",
     sections=["Labor Day – No Class (Mon Sep 7)", "2.1 Categorical Variables"],
     rows=[
      row([("Construct frequency and relative frequency tables for a categorical variable.", [2]),
           ("Compute a sample proportion p̂.", [2]),
           ("Distinguish the parameter p from the statistic p̂.", [2]),
           ("Compute overall and conditional proportions from a two-way table, choosing the correct denominator.", [2]),
           ("Compute and interpret a difference in proportions.", [2]),
           ("Interpret bar charts, pie charts, side-by-side bar charts, and segmented bar charts.", [2])],
          pack("2.1"),
          [part("Frequency and Relative Frequency"),
           part("Finding Proportions from Two-Way Tables") + " – Your Turn: Two-Way Table Proportions (pet ownership by housing)"],
          [hw("2.1", "Sep 13"), quiz(2)] + test(1)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 4
dict(num=4, title="One Quantitative Variable: Shape, Center, Spread and Percentiles", dates="Sep 14 – 16",
     sections=["2.2 One Quantitative Variable: Shape and Center", "2.3 One Quantitative Variable: Percentiles"],
     rows=[
      row([("Describe the shape of a distribution (symmetric, left-skewed, right-skewed) from a dotplot or histogram.", [2]),
           ("Compute the mean and median of a dataset.", [2]),
           ("Explain how skewness and outliers affect the mean and the median (resistance).", [2]),
           ("Interpret the standard deviation as the typical distance from the mean.", [2]),
           ("Apply the 95% rule to estimate the mean and standard deviation from a bell-shaped dotplot.", [2])],
          pack("2.2"),
          [part("Quantitative Variables") + " – shape, mean vs. median; estimate the mean and SD of a dotplot without calculating (95% rule); Your Turn: Mean vs. Median with an Outlier (commute times)",
           part("One Quantitative Variable (Kahoot!)") + " – Wed: review of 2.2"],
          [hw("2.2", "Sep 20"), quiz(2)] + test(1)),
      row([("Compute the sample standard deviation of a small dataset by hand.", [2]),
           ("Compute a z-score for a data value.", [2]),
           ("Use z-scores to compare values measured on different scales or in different groups.", [2]),
           ("Compute the five-number summary, range, and IQR of a dataset.", [2]),
           ("Apply the 1.5×IQR rule to identify outliers.", [2]),
           ("Construct a boxplot, marking any outliers.", [2])],
          pack("2.3"),
          [part("Using Percentiles") + " – Your Turn: Comparing Across Groups (heights of men and women with z-scores); five-number summary"],
          [hw("2.3", "Sep 20"), quiz(2)] + test(1)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 5
dict(num=5, title="Two-Variable Relationships and Linear Regression", dates="Sep 21 – 23",
     sections=["2.4 Two Variable Relationships", "2.5 Two Quantitative Variables: Linear Regression"],
     rows=[
      row([("Compare a quantitative variable across groups using side-by-side boxplots.", [2]),
           ("Compute and interpret a difference in means.", [2]),
           ("Describe the direction, form, and strength of the relationship in a scatterplot.", [7]),
           ("Estimate the correlation r from a scatterplot.", [7]),
           ("Use technology to compute the correlation r.", [7]),
           ("Explain how outliers, nonlinear patterns, and the absence of causation limit the interpretation of r.", [7])],
          [etext("2.4"), slides("2.4")],
          [part("Box Plots and Outliers") + " – Mon: 1.5×IQR rule review; side-by-side boxplots (tea vs. coffee); Your Turn: Tea vs. Coffee: Descriptive Statistics",
           part("Two Variable Relationships") + " – Wed: NBA rebounds vs. free-throw % scatterplot; find r with and without an outlier"],
          [hw("2.4", "Sep 27"), quiz(3, "objectives 3–6")] + test(1)),
      row([("Interpret the slope of a regression line in context with correct units.", [7]),
           ("Interpret the intercept of a regression line in context and evaluate whether it is meaningful.", [7]),
           ("Use a regression equation to predict a response value.", [7]),
           ("Compute and interpret a residual.", [7]),
           ("Locate positive and negative residuals on a scatterplot.", [7]),
           ("Use technology to find the least-squares regression line.", [7]),
           ("Explain what “least squares” means.", [7]),
           ("Recognize when a regression prediction is not appropriate: extrapolation, nonlinearity, and influential outliers.", [7]),
           ("Explain why a strong regression relationship does not by itself establish cause and effect.", [7])],
          [etext("2.5"),
           "Interactive Lecture: Section 2.5 Two Quantitative Variables: Linear Regression (Part 1)",
           "Interactive Lecture: Section 2.5 Two Quantitative Variables: Linear Regression (Part 2)",
           slides("2.5")],
          ["Examples: baseball game length and commute-time regression lines (predict, interpret slope, find a residual)"],
          [hw("2.5", "Sep 27"), quiz(3)] + test(1)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 6
dict(num=6, title="Probability Rules and Sampling Distributions", dates="Sep 28 – 30",
     sections=["P.1 Probability Rules", "3.1 Sampling Distributions"],
     rows=[
      row([("List the sample space for a chance process with equally likely outcomes.", [3]),
           ("Compute probabilities by counting equally likely outcomes.", [3]),
           ("Apply the complement rule.", [3]),
           ("Apply the addition rule to find P(A or B) from a two-way table.", [3]),
           ("Compute conditional probabilities from a two-way table.", [3]),
           ("Apply the multiplication rule for draws with and without replacement.", [3]),
           ("Distinguish disjoint events from independent events.", [3])],
          pack("P.1"),
          [part("Regression Line") + " – Mon: wrap-up of 2.5; Your Turn: Putting It All Together (used-car price vs. age: slope, intercept, prediction, residual)",
           part("Probability") + " – Rock and Roll Hall of Fame two-way table; cards with and without replacement; Your Turn: Probabilities from a Table (job by enrollment status)"],
          [hw("P.1", "Oct 4")] + test(2)),
      row([("Classify a numerical summary as a parameter or a statistic.", [5]),
           ("Use the correct notation for parameters (μ, σ, p, ρ) and statistics (x̄, s, p̂, r).", [5]),
           ("Describe how a sampling distribution is built from repeated samples and what each dot represents.", [5]),
           ("Describe the center and shape of a sampling distribution.", [5]),
           ("Explain the standard error as the variability of a statistic.", [5]),
           ("Predict how the sample size affects the standard error.", [5])],
          pack("3.1"),
          [proposed("Sampling Distributions") + " – M&M activity: each student draws 10 M&Ms, computes p̂ (blue), and adds it to a class dotplot; name the population, sample, and what each dot represents; Your Turn: Parameter or Statistic?"],
          [hw("3.1", "Oct 11"), quiz(4)] + test(2)),
     ],
     also=["Test 1 – Fri Oct 2 – Sun Oct 4 (Blackboard, proctored, 2 hours). Covers Weeks 1–5."]),
# ---------------------------------------------------------------- Week 7
dict(num=7, title="Confidence Intervals and the Bootstrap", dates="Oct 5 – 7",
     sections=["3.2 Understanding and Interpreting Confidence Intervals", "3.3 Constructing Bootstrap Confidence Intervals Using Standard Error"],
     rows=[
      row([("Construct a 95% confidence interval as statistic ± 2·SE, given the statistic and its standard error.", [6]),
           ("Interpret a confidence interval in context.", [6]),
           ("Explain the confidence level as the long-run proportion of intervals that capture the parameter.", [4, 6]),
           ("Identify common misinterpretations of a confidence interval.", [6])],
          [etext("3.2"), slides("3.2")],
          [part("Sampling Distribution (Kahoot!)") + " – Mon: review of 3.1",
           part("Confidence Intervals") + " – which of 20 simulated CIs capture μ; fix three misinterpretations; Your Turn: Do These CIs Capture p?"],
          [hw("3.2", "Oct 11"), quiz(4)] + test(2)),
      row([("Describe how a bootstrap sample and a bootstrap distribution are created.", [5, 6]),
           ("Explain why a bootstrap distribution is centered at the sample statistic.", [5]),
           ("Use StatKey to generate a bootstrap distribution.", [5, 6]),
           ("Estimate the standard error as the standard deviation of the bootstrap distribution.", [5, 6]),
           ("Construct and interpret a 95% bootstrap confidence interval using the standard-error method.", [6])],
          [etext("3.3"), slides("3.3", " (embedded StatKey simulator)"), "StatKey (lock5stat.com/statkey) – Bootstrap Confidence Intervals"],
          [part("Bootstrap Confidence Intervals") + " – Wed: Your Turn: Bootstrap a Proportion (32 of 50 prefer Brand A): build the bootstrap distribution, read off SE, form the CI"],
          [hw("3.3", "Oct 11"), quiz(4)] + test(2)),
     ],
     also=["Test 1 Retake – Mon Oct 5 – Sun Oct 11 (optional; higher score counts)"]),
# ---------------------------------------------------------------- Week 8
dict(num=8, title="Percentile Intervals and Introducing Hypothesis Tests", dates="Oct 12 – 14",
     sections=["3.4 Bootstrap Confidence Intervals Using Percentiles", "4.1 Introducing Hypothesis Tests"],
     rows=[
      row([("Determine which percentiles of a bootstrap distribution bound a 90%, 95%, or 99% confidence interval.", [6]),
           ("Construct a percentile bootstrap confidence interval with StatKey.", [6]),
           ("Predict how changing the confidence level affects the width of an interval.", [6]),
           ("Predict how changing the sample size affects the width of an interval.", [6]),
           ("Evaluate whether a bootstrap distribution is symmetric and bell-shaped enough to trust a bootstrap interval.", [6]),
           ("Explain why a bootstrap interval cannot correct for a non-representative sample.", [1, 6])],
          pack("3.4"),
          [part("Confidence Intervals Using Percentiles") + " – Mon: StatKey: 90/95/99% intervals for the same data; compare SE and percentile methods; Your Turn: Percentile CIs (124 of 200 students work)"],
          [hw("3.4", "Oct 18")] + test(2)),
      row([("Identify the parameter of interest in a research question.", [8]),
           ("Write null and alternative hypotheses in symbols and in words.", [8]),
           ("Classify a test as right-tailed, left-tailed, or two-tailed.", [8]),
           ("Explain the logic of a hypothesis test: assume H₀ is true and ask whether the sample data are surprising.", [8])],
          pack("4.1"),
          [proposed("Writing Hypotheses") + " – rock paper scissors practice (9 of 11 wins): define the parameter, state H₀ and Hₐ, choose the tail; Your Turn: Write the Hypotheses (airline on-time rate, SAT prep, and more)",
           "Think about it: is 15 of 16 correct (dolphin study) convincing?"],
          [hw("4.1", "Oct 18"), quiz(5)] + test(2)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 9
dict(num=9, title="P-values and Statistical Significance", dates="Oct 19 – 21",
     sections=["4.2 Measuring Evidence with P-Values", "4.3 Determining Statistical Significance"],
     rows=[
      row([("Describe how a randomization distribution is generated assuming H₀ is true.", [5, 8]),
           ("Identify the center of a randomization distribution as the null value.", [5]),
           ("Compare sampling, bootstrap, and randomization distributions by their center and purpose.", [5]),
           ("Compute a p-value from a randomization distribution as the proportion of simulated statistics at least as extreme as the observed statistic.", [3, 8]),
           ("Determine the correct tail(s) for a p-value from the alternative hypothesis.", [8]),
           ("Interpret a p-value in context.", [4, 8])],
          pack("4.2") + ["StatKey – Randomization Hypothesis Tests"],
          [proposed("Randomization Distributions") + " – StatKey: dolphin study (16 flips); count how many simulated statistics are as extreme as observed; Your Turn: Tea and Immunity in StatKey (re-randomize tea vs. coffee, find the p-value)"],
          [hw("4.2", "Oct 25"), quiz(5)] + test(2)),
      row([("Relate the size of a p-value to the strength of evidence against H₀.", [8]),
           ("Compare a p-value to the significance level α to decide whether to reject H₀.", [8]),
           ("Write a two-step conclusion in context that avoids saying “accept H₀”.", [8])],
          pack("4.3", slides_suffix=" (includes “What is a p-value?” video)"),
          [proposed("P-values and Conclusions") + " – resveratrol examples (p = 0.04, 0.12, 0.0003): strength of evidence, decision at α, conclusion in context; Your Turn: Decide and Conclude"],
          [hw("4.3", "Oct 25"), quiz(5)] + test(2)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 10
dict(num=10, title="A Closer Look at Testing, Making Connections, and Normal Distributions", dates="Oct 26 – 28",
     sections=["4.4 A Closer Look at Testing", "4.5 Making Connections", "5.1 Hypothesis Testing Using Normal Distributions"],
     rows=[
      row([("Describe Type I and Type II errors in the context of a study.", [8]),
           ("Relate the significance level α to the probability of a Type I error.", [4, 8]),
           ("Explain the trade-off between Type I and Type II errors and how sample size affects it.", [8]),
           ("Explain how multiple testing and publication bias produce false positives.", [8]),
           ("Distinguish statistical significance from practical significance.", [8])],
          pack("4.4", slides_suffix=" (includes Khan Academy Type I/II video)"),
          [proposed("Errors in Testing") + " – battery-life example (a)–(d): describe each error in context; courtroom analogy matching; vitamin E multiple-testing questions; Your Turn: Errors and Multiple Tests (ambulance response times)"],
          [hw("4.4", "Nov 1", " (a)"), hw("4.4", "Nov 1", " (b)"), quiz(6)] + test(3)),
      row([("Describe how to generate randomization samples for a given study design (coin flips, re-randomizing groups, shifting data then bootstrapping).", [8]),
           ("Identify the centers of the bootstrap and randomization distributions for given data.", [5]),
           ("Use a 95% confidence interval to reach a two-tailed test conclusion at α = 0.05.", [6, 8]),
           ("Determine whether a confidence interval or a hypothesis test fits a research question.", [6, 8])],
          pack("4.5"),
          [proposed("Making Connections") + " – body temperature: test 98.6 using the CI (98.05, 98.47); sleep study (28/50): how to generate randomization samples; Your Turn: CI or Test? (smart-speaker ownership)"],
          [hw("4.5", "Nov 1"), quiz(6)] + test(3)),
      row([("Explain when the Central Limit Theorem justifies replacing a randomization distribution with a normal distribution N(null value, SE).", [5]),
           ("Compute a standardized z statistic.", [8]),
           ("Determine a p-value as a right-tail, left-tail, or two-tail area under the standard normal curve.", [3, 8])],
          pack("5.1") + ["StatKey – Theoretical Distributions (Normal)"],
          [proposed("Normal Distributions and z") + " – malaria/mosquito example: compute z, shade the tail in StatKey, find the p-value; Your Turn: z-Tests (right-, left-, and two-tailed)"],
          [hw("5.1", "Nov 1")] + test(3)),
     ],
     also=["Test 2 – Fri Oct 30 – Sun Nov 1 (Blackboard, proctored, 2 hours). Covers Weeks 6–9."]),
# ---------------------------------------------------------------- Week 11
dict(num=11, title="Inference for One Proportion and Two Proportions", dates="Nov 2 – 4",
     sections=["6.1 Inference for a Proportion (Distribution, CI, Hypothesis Test)", "6.3 Inference for a Difference in Proportions (Distribution, CI, Hypothesis Test)"],
     rows=[
      row([("Check the large-sample condition (at least 10 in each category) for inference about one proportion.", [5]),
           ("Construct a confidence interval for a population proportion using z* for 90%, 95%, or 99% confidence.", [6]),
           ("Interpret a confidence interval for a proportion in context.", [6]),
           ("Perform a one-proportion z test and state the conclusion in context.", [8]),
           ("Explain why the confidence-interval standard error uses p̂ while the test uses p₀.", [8])],
          etext3("6.1", "a Proportion") + [lecture("6.1"), slides("6.1")],
          [proposed("Inference for a Proportion") + " – 4-step CI and 4-step test for a proportion (voting example); compare the two SEs; Your Turn: Testing a Proportion (60 of 250 live on campus)"],
          [hw("6.1", "Nov 8"), quiz(7)] + test(3)),
      row([("Determine whether a study calls for one-proportion or difference-in-proportions inference.", [5]),
           ("Check the conditions for inference about a difference in proportions.", [5]),
           ("Construct a confidence interval for p₁ − p₂.", [6]),
           ("Interpret a confidence interval for p₁ − p₂, including what its sign means and whether it contains 0.", [6]),
           ("Compute the pooled proportion.", [8]),
           ("Perform a two-proportion z test from summary data or a two-way table.", [8])],
          etext3("6.3", "a Difference in Proportions") + [lecture("6.3"), slides("6.3", " (embedded StatKey two-proportion randomization)")],
          [proposed("Difference in Proportions") + " – two-proportion randomization (18/30 vs. 12/30); compare simulation with the formula; Your Turn: Treatment vs Placebo (two-proportion z test from a two-way table)"],
          [hw("6.3", "Nov 8"), quiz(7)] + test(3)),
     ],
     also=["Test 2 Retake – Mon Nov 2 – Sun Nov 8 (optional; higher score counts)"]),
# ---------------------------------------------------------------- Week 12
dict(num=12, title="Inference for a Mean", dates="Nov 9 – 11",
     sections=["6.2 Inference for a Mean (Distribution, CI, Hypothesis Test)", "Veterans Day – No Class (Wed Nov 11)"],
     rows=[
      row([("Explain why inference for a mean uses the t distribution with df = n − 1.", [5]),
           ("Check the conditions for t procedures.", [5]),
           ("Construct and interpret a t confidence interval for a population mean.", [6]),
           ("Perform a one-sample t test and state the conclusion in context.", [8])],
          etext3("6.2", "a Mean") + [lecture("6.2"), slides("6.2"), "StatKey – Theoretical Distributions (t)"],
          [proposed("Inference for a Mean") + " – gribbles CI and Chips Ahoy test worked in groups; Your Turn: Testing a Mean (juice bottles underfilled?)"],
          [hw("6.2", "Nov 15"), quiz(7)] + test(3)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 13
dict(num=13, title="Inference for Two Means and Paired Data", dates="Nov 16 – 18",
     sections=["6.4 Inference for a Difference in Means (Distribution, CI, Hypothesis Test)", "6.5 Paired Difference in Means"],
     rows=[
      row([("Compute the standard error and conservative degrees of freedom for a difference in two independent means.", [5]),
           ("Check the conditions for two-sample t procedures.", [5]),
           ("Construct and interpret a confidence interval for μ₁ − μ₂.", [6]),
           ("Explain how the order of the groups affects the sign of the difference.", [6]),
           ("Perform a two-sample t test, choosing the tail from the research question.", [8])],
          etext3("6.4", "a Difference in Means") + [lecture("6.4"), slides("6.4")],
          [proposed("Comparing Two Means") + " – video games and GPA CI; Pygmalion-effect test; Your Turn: Exercise and Sleep (two-sample t test and CI)"],
          [hw("6.4", "Nov 22")] + test(3)),
      row([("Classify a study design as paired or independent samples by checking for a link between observations.", [1, 8]),
           ("Define the difference variable d and the order of subtraction.", [8]),
           ("Perform a paired t test.", [8]),
           ("Construct and interpret a paired t confidence interval.", [6]),
           ("Explain why pairing reduces variability.", [8])],
          pack("6.5"),
          [proposed("Paired or Independent?") + " – Your Turn: Paired or Unpaired? (class discussion of study scenarios); define d and the order of subtraction"],
          [hw("6.5", "Nov 22"), quiz(8)] + test(3)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 14
dict(num=14, title="Chi-Square Test for Association", dates="Nov 23 – 25",
     sections=["7.2 Testing for an Association Between Two Categorical Variables", "No Class – College closes at noon (Wed Nov 25)"],
     rows=[
      row([("State the hypotheses for a chi-square test of association from a two-way table.", [8]),
           ("Compute the expected counts for a two-way table.", [8]),
           ("Check that all expected counts are at least 5.", [8]),
           ("Compute the chi-square statistic and its degrees of freedom, (r − 1)(c − 1).", [8]),
           ("Interpret the right-tail p-value of a chi-square test.", [8]),
           ("Relate the chi-square test on a 2×2 table to the two-proportion z test.", [8]),
           ("Explain why a significant result shows association but not direction or causation.", [8])],
          pack("7.2") + ["StatKey – Theoretical Distributions (χ²)"],
          [proposed("Chi-Square Test") + " – Your Turn: Faculty Rank and Gender: compute expected counts, cell contributions, χ² and df; decide and interpret"],
          [hw("7.2", "Nov 29")]),
     ],
     also=["Test 3 Retake – Mon Nov 23 – Sun Nov 29 (optional; higher score counts)"]),
# ---------------------------------------------------------------- Week 15
dict(num=15, title="ANOVA and Inference for Slope and Correlation", dates="Nov 30 – Dec 2",
     sections=["8.1 Analysis of Variance", "9.1 Inference for Slope and Correlation"],
     rows=[
      row([("Identify when ANOVA is appropriate.", [8]),
           ("State H₀ and Hₐ for ANOVA in symbols and in words.", [8]),
           ("Explain what SSG and SSE measure.", [8]),
           ("Explain how the ratio of between-group to within-group variability gives evidence against H₀.", [8]),
           ("Complete an ANOVA table (df, MS, F) from given sums of squares.", [8]),
           ("Interpret the F statistic and p-value in context.", [8]),
           ("Check the conditions for ANOVA.", [8])],
          pack("8.1") + ["StatKey – Theoretical Distributions (F)"],
          [proposed("ANOVA") + " – cuckoo-egg example: build the ANOVA table from given SS, find F, decide; Your Turn: Complete the ANOVA Table (fertilizer and seedling growth)"],
          [hw("8.1", "Dec 6")]),
      row([("State the simple linear model.", [7]),
           ("Distinguish the population slope β₁ and correlation ρ from the sample estimates b₁ and r.", [7]),
           ("Interpret the slope in context.", [7]),
           ("Use regression output to test H₀: β₁ = 0 with a t statistic on n − 2 degrees of freedom.", [7, 8]),
           ("Explain why the tests for slope and for correlation give the same p-value.", [7]),
           ("Construct and interpret a confidence interval for the slope.", [6, 7]),
           ("Interpret R² as the proportion of variability in the response explained by the model.", [7]),
           ("Check the conditions for regression inference with a residual plot.", [7])],
          pack("9.1"),
          [proposed("Inference for Slope and Correlation") + " – SleepStudy: depression score vs. classes missed (test for correlation and slope, CI for slope, R²); Your Turn: Alcohol and Missed Classes (drinks per week vs. classes missed)"],
          [hw("9.1", "Dec 6")]),
     ],
     also=["Course Evaluation (in START HERE) – complete before the end of the semester"]),
# ---------------------------------------------------------------- Week 16
dict(num=16, title="Putting It All Together and Final Exam", dates="Dec 7 – 9",
     sections=["Review: Putting It All Together – From Sampling to Hypothesis Testing (Mon Dec 7)", "Final Exam – Wed Dec 9, online (Blackboard, proctored)"],
     rows=[
      row([("Select the appropriate procedure for a research question among one- and two-proportion z, one- and two-sample t, paired t, chi-square, ANOVA, and regression.", [8]),
           ("Perform a complete hypothesis test, from hypotheses to a conclusion in context.", [8]),
           ("Construct and interpret a confidence interval, using simulation or theoretical distributions as appropriate.", [6]),
           ("Evaluate whether a study’s design allows its conclusion to be generalized to a population.", [1]),
           ("Evaluate whether a study’s design supports a cause-and-effect conclusion.", [1])],
          ["Review Slides: Putting It All Together (with answer key and no-answers versions)",
           "All Slides and Interactive Lectures (Weeks 1–15)", "StatKey"],
          [proposed("One Complete Test with a Partner") + " – 10 problems, one per pair (narrator/writer roles), 5-minute presentations; extension: build the matching 95% CI"],
          ["Final Exam – Wed Dec 9 (Blackboard, proctored, 2 hours, cumulative; no retake) (all objectives)"]),
     ],
     also=[]),
]

DISCREPANCIES = """Blackboard (course _970761_1) vs. MW syllabus and maps, as read on Oct 8, 2026:
- Weeks 1-5 and 9-15 match the maps. Weeks 9-16 are still hidden from students.
- Week 6: Online Homework 3.1 is due Sun Oct 11 in Blackboard (not Oct 4); the maps follow Blackboard.
- Week 7 Participation items are now in Blackboard: Sampling Distribution (Kahoot!) (Mon Oct 5, a 3.1 review),
  Confidence Intervals, and Bootstrap Confidence Intervals (Wed Oct 7). The Confidence Intervals item is
  titled "Participation: Confidence Intervals.docx" and has no due date; the maps drop the ".docx".
- Week 8: "Participation: Confidence Intervals Using Percentiles" (Mon Oct 12) exists but is hidden from
  students. There is no 4.1 participation item yet; "Writing Hypotheses" is still a proposed activity.
- Week 6 has no Blackboard item for the M&M sampling-distribution activity (kept on the map as proposed).
- Week 7 has no Interactive Lecture items for 3.2 and 3.3 (the maps follow Blackboard and omit them).
- Week 15 has no 9.1 items and Week 16 holds only the Final Exam (no Review slides); the maps list them by convention.
- START HERE now also has "Course Evaluation" (listed in Week 15) and "Learn more about your course materials".
- Naming leftovers: Week 2 "1.3 Experiments and Observational Studies" and Week 3 "2.1 Categorical Variables"
  e-text items lack the "e-Text:" prefix; the three Week 11 items for 6.1 are spelled "eText:" (no hyphen).
- Week 5: the 2.5 lecture videos are "Interactive Lecture: Section 2.5 ... (Part 1)" and "(Part 2)".
  There is no Interactive Lecture for 2.4 (intentional).
- Week 10 homework 4.4 is split into "(a)" and "(b)".
- Weeks 1-15 contain "Week N Course Map" items; these are the maps themselves and are not listed on the maps.
"""
