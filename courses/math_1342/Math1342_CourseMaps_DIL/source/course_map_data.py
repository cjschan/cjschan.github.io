# -*- coding: utf-8 -*-
"""
Content for the Math 1342 weekly course maps (Fall 2026, TTh Section 036).
Edit this file and re-run build_course_maps.py to regenerate the PDFs.

Each week dict:
  num, title, dates, sections (list of str)
  rows: table rows; each row has mos (list of (objective_text, [CLO numbers])) and the materials,
        activities and assessments (lists of str) that align to those objectives. Objectives are
        numbered across rows. A Take-Home Quiz goes in every row it covers, with "(all objectives)"
        or "(objectives a–b)" at the end of its text.
  also: items that week that are not tied to its objectives (tests, retakes), printed under the table
"""

COURSE = "MATH 1342 – Elementary Statistics"
TERM = "Fall 2026 · Section 036 · TTh 6:00–7:20 PM (DIL)"

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
LIVE_TOOL = "Zoom"

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
def etext(sec, title=None, suffix=""):   return f"e-Text: {sec} {TITLES[sec]}{suffix}"
def lecture(sec, suffix=""):             return f"Interactive Lecture: {sec} {TITLES[sec]}{suffix}"
def slides(sec, suffix=""):              return f"Slides: {sec} {TITLES[sec]}{suffix}"
def hw(sec, due, suffix=""):             return f"Online Homework: {sec} {TITLES[sec]}{suffix} (due Sun {due}, 11:59 PM)"
def part(topic):        return f"Participation: {topic}"

# Take-Home Quizzes: due date (Blackboard) and the sections each quiz covers (from quizzes_fall2026/).
# A quiz is listed in every row whose objectives it covers, in the week that teaches them.
QUIZZES = {
    1: ("Tue Sep 8", "Intro, 1.1–1.3"), 2: ("Tue Sep 22", "2.1–2.3"), 3: ("Tue Oct 6", "2.4–2.5"),
    4: ("Tue Oct 13", "3.1–3.3"), 5: ("Tue Oct 27", "4.1–4.3"), 6: ("Tue Nov 3", "4.4–4.5"),
    7: ("Tue Nov 17", "6.1–6.3"), 8: ("Tue Nov 24", "6.5"),
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
dict(num=1, title="Introduction and the Structure of Data", dates="Aug 25 – 27",
     sections=["Introduction: What Is Statistics For?", "1.1 The Structure of Data"],
     rows=[
      row([("Describe statistics as the process of collecting, describing, and analyzing data.", [1]),
           ("Determine whether a surprising result could reasonably have happened by chance alone.", [4]),
           ("Distinguish between a sample and a population.", [1]),
           ("Explain how a non-representative sample can bias an estimate.", [1]),
           ("Compute and compare the mean and median of a small dataset, and explain how an outlier affects each.", [2])],
          ["START HERE: Welcome; Syllabus; Textbook and Wiley Course Resources; Online Tutoring; College Policies & Student Support Services",
           "Introduction Slides: What Is Statistics For? (Day 1)"],
          [part("Syllabus") + " – course tour and expectations",
           "Day-1 class data activity: collect everyone's age, then find the mean, median, mode and boxplot together; compare the class median to the U.S. median age"],
          [quiz(1)] + test(1)),
      row([("Identify the cases and variables in a dataset presented as a table.", [2]),
           ("Classify a variable as categorical or quantitative.", [2]),
           ("Identify the explanatory and response variables in a research question.", [1])],
          [etext("1.1"), lecture("1.1"), slides("1.1")],
          [part("Variables") + " – identify cases, variables and variable types",
           "Your Turn: Used Cars: Cases and Variables"],
          [hw("1.1", "Aug 30"), quiz(1)] + test(1)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 2
dict(num=2, title="Sampling, Experiments and Observational Studies", dates="Sep 1 – 3",
     sections=["1.2 Sampling from a Population", "1.3 Experiments and Observational Studies"],
     rows=[
      row([("Distinguish a population from a sample.", [1]),
           ("Explain how statistical inference uses sample data to draw conclusions about a population.", [1]),
           ("Identify sampling bias and classify the sampling method (random, convenience, or volunteer) in a described study.", [1]),
           ("Evaluate whether a study’s results can be generalized to the population.", [1])],
          [etext("1.2"), lecture("1.2"), slides("1.2", " (includes sampling video)")],
          [part("Variables in Statistics (Kahoot!)") + " – Tue: review of Week 1",
           part("Sampling") + " – spot the bias in sample scenarios",
           "Your Turn: Name the Bias",
           part("Sampling Methods (Kahoot!)") + " – Thu: sampling review"],
          [hw("1.2", "Sep 6"), quiz(1)] + test(1)),
      row([("Classify a study as observational or experimental.", [1]),
           ("Identify a plausible confounding variable in an observational study.", [1]),
           ("Explain how random assignment, a control group, and blinding support cause-and-effect conclusions.", [1]),
           ("Distinguish random sampling from random assignment.", [1])],
          [etext("1.3"), lecture("1.3"), slides("1.3", " (includes TED-Ed placebo video)")],
          [part("Experiments and Observational Studies") + " – classify studies; confounding; random sampling vs. random assignment",
           "Your Turn: Study Design and Scope of Inference (coffee and depression; vitamin D experiment)"],
          [hw("1.3", "Sep 6"), quiz(1)] + test(1)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 3
dict(num=3, title="Describing Categorical and Quantitative Variables", dates="Sep 8 – 10",
     sections=["2.1 Categorical Variables", "2.2 One Quantitative Variable: Shape and Center"],
     rows=[
      row([("Construct frequency and relative frequency tables, compute a sample proportion p̂, and distinguish the parameter p from the statistic p̂.", [2]),
           ("Compute and interpret overall and conditional proportions, and the difference in proportions, from a two-way table.", [2]),
           ("Interpret bar charts, pie charts, side-by-side bar charts, and segmented bar charts.", [2])],
          [etext("2.1"), lecture("2.1"), slides("2.1")],
          [part("Frequency and Relative Frequency"),
           part("Finding Proportions from Two-Way Tables"),
           "Your Turn: Two-Way Table Proportions (pet ownership by housing)"],
          [hw("2.1", "Sep 13"), quiz(2)] + test(1)),
      row([("Describe the shape of a distribution from a dotplot or histogram.", [2]),
           ("Compute the mean and median, and explain each one’s resistance to skewness and outliers.", [2]),
           ("Interpret the standard deviation as the typical distance of data values from the mean.", [2]),
           ("Use the 95% rule to estimate the standard deviation from a bell-shaped dotplot.", [2])],
          [etext("2.2"), lecture("2.2"), slides("2.2")],
          [part("Quantitative Variables") + " – shape, mean vs. median",
           "Your Turn: Mean vs. Median with an Outlier (commute times)",
           "Your Turn: Estimation Activity – estimate the mean and SD of a dotplot without calculating (95% rule)"],
          [hw("2.2", "Sep 13"), quiz(2)] + test(1)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 4
dict(num=4, title="Percentiles, Boxplots and Two-Variable Relationships", dates="Sep 15 – 17",
     sections=["2.3 One Quantitative Variable: Percentiles", "2.4 Two Variable Relationships"],
     rows=[
      row([("Compute the sample standard deviation of a small dataset by hand.", [2]),
           ("Compute and interpret z-scores to compare values on different scales or in different groups.", [2]),
           ("Find the five-number summary, range, and IQR of a dataset.", [2]),
           ("Apply the 1.5 × IQR rule to identify outliers.", [2]),
           ("Interpret a boxplot to describe a distribution’s center, spread, skewness, and outliers.", [2])],
          [etext("2.3"), lecture("2.3"), slides("2.3")],
          [part("One Quantitative Variable (Kahoot!)") + " – Tue: review of 2.2",
           part("Using Percentiles"),
           "Your Turn: Comparing Across Groups (heights of men and women with z-scores)",
           part("Box Plots and Outliers") + " – five-number summary, 1.5×IQR rule"],
          [hw("2.3", "Sep 20"), quiz(2)] + test(1)),
      row([("Compare a quantitative variable across groups using side-by-side boxplots.", [2]),
           ("Compute and interpret a difference in means.", [2]),
           ("Describe the direction, form, and strength of a relationship in a scatterplot.", [7]),
           ("Estimate the correlation r from a scatterplot, and compute it using technology.", [7]),
           ("Explain how outliers and nonlinear patterns affect r.", [7]),
           ("Explain why correlation doesn’t imply causation.", [7])],
          [etext("2.4"), slides("2.4")],
          ["Your Turn: Tea vs. Coffee: Descriptive Statistics (difference in means; can we conclude causation?)"],
          [hw("2.4", "Sep 20"), quiz(3, "objectives 8–11")] + test(1)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 5
dict(num=5, title="Linear Regression", dates="Sep 22 – 24",
     sections=["2.5 Two Quantitative Variables: Linear Regression", "Catch-Up Day (Thu Sep 24)"],
     rows=[
      row([("Interpret the slope of a regression line in context with correct units.", [7]),
           ("Interpret the intercept of a regression line in context and evaluate whether it is meaningful.", [7]),
           ("Use a regression equation to predict a response value.", [7]),
           ("Compute and interpret a residual.", [7]),
           ("Locate cases with positive and negative residuals on a scatterplot.", [7]),
           ("Use technology to find the least-squares regression line.", [7]),
           ("Recognize cases when a regression prediction is not appropriate.", [7])],
          [etext("2.5"),
           "Interactive Lecture: Section 2.5 Two Quantitative Variables: Linear Regression (Part 1)",
           "Interactive Lecture: Section 2.5 Two Quantitative Variables: Linear Regression (Part 2)",
           slides("2.5")],
          [part("Two Variable Relationships") + " – Tue: correlation review",
           part("Regression Line") + " – Thu: baseball game length and commute-time examples",
           "Your Turn: Putting It All Together (used-car price vs. age: slope, intercept, prediction, residual)"],
          [hw("2.5", "Sep 27"), quiz(3)] + test(1)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 6
dict(num=6, title="Probability Rules and Sampling Distributions", dates="Sep 29 – Oct 1",
     sections=["P.1 Probability Rules", "3.1 Sampling Distributions"],
     rows=[
      row([("List the sample space for a chance process with equally likely outcomes.", [3]),
           ("Compute probabilities by counting equally likely outcomes.", [3]),
           ("Apply the complement rule.", [3]),
           ("Apply the addition rule to find P(A or B) from a two-way table.", [3]),
           ("Compute conditional probabilities from a two-way table.", [3]),
           ("Apply the multiplication rule for draws with and without replacement.", [3]),
           ("Distinguish disjoint events from independent events.", [3])],
          [etext("P.1"), lecture("P.1"), slides("P.1")],
          [part("Probability") + " – Rock and Roll Hall of Fame two-way table; cards with and without replacement",
           "Your Turn: Probabilities from a Table (job by enrollment status)"],
          [hw("P.1", "Oct 4")] + test(2)),
      row([("Classify a numerical summary as a parameter or a statistic.", [5]),
           ("Use the correct notation for parameters (μ, σ, p, ρ) and statistics (x̄, s, p̂, r).", [5]),
           ("Describe how a sampling distribution is built from repeated samples and what each dot represents.", [5]),
           ("Describe the center and shape of a sampling distribution.", [5]),
           ("Explain the standard error as the variability of a statistic.", [5]),
           ("Predict how the sample size affects the standard error.", [5])],
          [etext("3.1"), lecture("3.1"), slides("3.1")],
          ["Your Turn: Parameter or Statistic? (name each number as a parameter or statistic and give its symbol)"],
          [hw("3.1", "Oct 11"), quiz(4)] + test(2)),
     ],
     also=["Test 1 – Fri Oct 2 – Sun Oct 4, 11:59 PM (proctored, 120 min). Covers Weeks 1–5."]),
# ---------------------------------------------------------------- Week 7
dict(num=7, title="Confidence Intervals and the Bootstrap", dates="Oct 6 – 8",
     sections=["3.2 Understanding and Interpreting Confidence Intervals", "3.3 Constructing Bootstrap Confidence Intervals Using Standard Error"],
     rows=[
      row([("Construct a 95% confidence interval as statistic ± 2·SE, given the statistic and its standard error.", [6]),
           ("Interpret a confidence interval in context.", [6]),
           ("Explain the confidence level as the long-run proportion of intervals that capture the parameter.", [4, 6]),
           ("Identify common misinterpretations of a confidence interval.", [6])],
          [etext("3.2"), slides("3.2")],
          [part("Sampling Distribution (Kahoot!)") + " – Tue: review of 3.1",
           part("Confidence Intervals") + " – which of 20 simulated CIs capture μ; fix three misinterpretations",
           "Your Turn: Do These CIs Capture p?"],
          [hw("3.2", "Oct 11"), quiz(4)] + test(2)),
      row([("Describe how a bootstrap sample and a bootstrap distribution are created.", [5, 6]),
           ("Explain why a bootstrap distribution is centered at the sample statistic.", [5]),
           ("Use StatKey to generate a bootstrap distribution.", [5, 6]),
           ("Estimate the standard error as the standard deviation of the bootstrap distribution.", [5, 6]),
           ("Construct and interpret a 95% bootstrap confidence interval using the standard-error method.", [6])],
          [etext("3.3"), slides("3.3", " (embedded StatKey simulator)")],
          [part("Bootstrap Confidence Intervals"),
           "Your Turn: Bootstrap a Proportion (32 of 50 prefer Brand A): build the bootstrap distribution in StatKey, read off SE, form the CI"],
          [hw("3.3", "Oct 11"), quiz(4)] + test(2)),
     ],
     also=["Test 1 Retake – due Sun Oct 11, 11:59 PM (optional; proctored, 120 min; higher score counts)"]),
# ---------------------------------------------------------------- Week 8
dict(num=8, title="Percentile Intervals and Introducing Hypothesis Tests", dates="Oct 13 – 15",
     sections=["3.4 Bootstrap Confidence Intervals Using Percentiles", "4.1 Introducing Hypothesis Tests"],
     rows=[
      row([("Determine which percentiles of a bootstrap distribution bound a 90%, 95%, or 99% confidence interval.", [6]),
           ("Construct a percentile bootstrap confidence interval with StatKey.", [6]),
           ("Predict how changing the confidence level and sample size affect the width of an interval.", [6]),
           ("Evaluate whether a bootstrap distribution is symmetric and bell-shaped enough to trust a bootstrap interval.", [6]),
           ("Explain why a bootstrap interval cannot correct for a non-representative sample.", [1, 6])],
          [etext("3.4"), lecture("3.4"), slides("3.4")],
          [part("Confidence Intervals Using Percentiles") + " – StatKey: 90/95/99% intervals for the same data; compare the SE and percentile methods",
           "Your Turn: Percentile CIs (124 of 200 students work)"],
          [hw("3.4", "Oct 18")] + test(2)),
      row([("Identify the parameter of interest in a research question.", [8]),
           ("Write null and alternative hypotheses in symbols and in words.", [8]),
           ("Classify a test as right-tailed, left-tailed, or two-tailed.", [8]),
           ("Explain the logic of a hypothesis test: assume H₀ is true and ask whether the sample data are surprising.", [8])],
          [etext("4.1"), lecture("4.1"), slides("4.1")],
          [part("Introduction to Hypothesis Tests") + " – rock paper scissors (9 of 11 wins): define the parameter, state H₀ and Hₐ, choose the tail",
           "Your Turn: Write the Hypotheses (airline on-time rate, SAT prep, and more)"],
          [hw("4.1", "Oct 18"), quiz(5)] + test(2)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 9
dict(num=9, title="P-values and Statistical Significance", dates="Oct 20 – 22",
     sections=["4.2 Measuring Evidence with p-values", "4.3 Determining Statistical Significance"],
     rows=[
      row([("Describe how a randomization distribution is generated assuming H₀ is true.", [5, 8]),
           ("Identify the center of a randomization distribution as the null value.", [5]),
           ("Compare sampling, bootstrap, and randomization distributions by their center and purpose.", [5]),
           ("Compute a p-value from a randomization distribution.", [3, 8]),
           ("Determine the correct tail(s) for a p-value from the alternative hypothesis.", [8]),
           ("Interpret a p-value in context.", [4, 8])],
          [etext("4.2"), lecture("4.2"), slides("4.2")],
          [part("P-Values") + " – StatKey: dolphin study (16 flips); count how many simulated statistics are as extreme as observed",
           "Your Turn: Tea and Immunity in StatKey (re-randomize tea vs. coffee, find the p-value)"],
          [hw("4.2", "Oct 25"), quiz(5)] + test(2)),
      row([("Relate the size of a p-value to the strength of evidence against H₀.", [8]),
           ("Compare a p-value to the significance level α to decide whether to reject H₀.", [8]),
           ("Write a two-step conclusion in context that avoids saying “accept H₀”.", [8])],
          [etext("4.3"), lecture("4.3"), slides("4.3", " (includes “What is a p-value?” video)")],
          [part("Determining Statistical Significance") + " – resveratrol examples (p = 0.04, 0.12, 0.0003): strength of evidence, decision at α, conclusion in context",
           "Your Turn: Decide and Conclude"],
          [hw("4.3", "Oct 25"), quiz(5)] + test(2)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 10
dict(num=10, title="A Closer Look at Testing and Making Connections", dates="Oct 27 – 29",
     sections=["4.4 A Closer Look at Testing", "4.5 Making Connections"],
     rows=[
      row([("Describe Type I and Type II errors in the context of a study.", [8]),
           ("Relate the significance level α to the probability of a Type I error.", [4, 8]),
           ("Explain the trade-off between Type I and Type II errors and how sample size affects it.", [8]),
           ("Explain how multiple testing and publication bias produce false positives.", [8]),
           ("Distinguish statistical significance from practical significance.", [8])],
          [etext("4.4"), lecture("4.4"), slides("4.4", " (includes Khan Academy Type I/II video)")],
          [part("Errors in Testing") + " – battery-life example (a)–(d): describe each error in context; courtroom analogy matching; vitamin E multiple-testing questions",
           "Your Turn: Errors and Multiple Tests (ambulance response times)"],
          [hw("4.4", "Nov 1"), quiz(6)] + test(3)),
      row([("Describe how to generate randomization samples for a given study design.", [8]),
           ("Identify the centers of the bootstrap and randomization distributions for given data.", [5]),
           ("Use a 95% confidence interval to reach a two-tailed test conclusion at α = 0.05.", [6, 8]),
           ("Determine whether a confidence interval or a hypothesis test fits a research question.", [6, 8])],
          [etext("4.5"), lecture("4.5"), slides("4.5")],
          [part("Making Connections") + " – body temperature: test 98.6 using the CI (98.05, 98.47); sleep study (28/50): how to generate randomization samples and where each distribution is centered",
           "Your Turn: CI or Test? (smart-speaker ownership)"],
          [hw("4.5", "Nov 1"), quiz(6)] + test(3)),
     ],
     also=["Test 2 – Fri Oct 30 – Sun Nov 1 (proctored, 120 min). Covers Weeks 6–9."]),
# ---------------------------------------------------------------- Week 11
dict(num=11, title="Normal Distributions and Inference for a Proportion", dates="Nov 3 – 5",
     sections=["5.1 Hypothesis Testing Using Normal Distributions", "6.1 Inference for a Proportion (Distribution, CI, Hypothesis Test)"],
     rows=[
      row([("Explain when a normal distribution can replace a randomization distribution.", [5]),
           ("Compute a standardized z statistic.", [8]),
           ("Find a p-value as a tail area under the standard normal curve.", [3, 8])],
          [etext("5.1"), lecture("5.1"), slides("5.1"), "StatKey – Theoretical Distributions (Normal)"],
          [part("Normal Distributions and z") + " – malaria/mosquito example: compute z, shade the tail in StatKey, find the p-value",
           "Your Turn: z-Tests (right-, left-, and two-tailed)"],
          [hw("5.1", "Nov 8")] + test(3)),
      row([("Check the conditions for inference about one proportion.", [5]),
           ("Construct a confidence interval for a population proportion.", [6]),
           ("Interpret a confidence interval for a proportion in context.", [6]),
           ("Perform a one-proportion z test and state the conclusion in context.", [8]),
           ("Explain why the confidence-interval standard error uses p̂ while the test uses p₀.", [8])],
          [etext("6.1") + " (6.1-D Distribution, 6.1-CI Confidence Interval, 6.1-HT Hypothesis Test)", lecture("6.1"), slides("6.1"),
           "StatKey – Theoretical Distributions (Normal)"],
          [part("Inference for a Proportion") + " – 4-step CI and 4-step test for a proportion (voting example); compare the two SEs",
           "Your Turn: Testing a Proportion (60 of 250 live on campus)"],
          [hw("6.1", "Nov 8"), quiz(7)] + test(3)),
     ],
     also=["Test 2 Retake – Mon Nov 2 – Sun Nov 8 (optional; higher score counts)"]),
# ---------------------------------------------------------------- Week 12
dict(num=12, title="Inference for Two Proportions and for a Mean", dates="Nov 10 – 12",
     sections=["6.3 Inference for a Difference in Proportions (Distribution, CI, Hypothesis Test)", "6.2 Inference for a Mean (Distribution, CI, Hypothesis Test)"],
     rows=[
      row([("Determine whether a study calls for one-proportion or difference-in-proportions inference.", [5]),
           ("Check the conditions for inference about a difference in proportions.", [5]),
           ("Construct a confidence interval for p₁ − p₂.", [6]),
           ("Interpret a confidence interval for p₁ − p₂ in context.", [6]),
           ("Explain what it means when a confidence interval for p₁ − p₂ contains 0.", [6]),
           ("Compute the pooled proportion.", [8]),
           ("Perform a two-proportion z test from summary data or a two-way table.", [8])],
          [etext("6.3") + " (6.3-D, 6.3-CI, 6.3-HT)", lecture("6.3"), slides("6.3", " (embedded StatKey two-proportion randomization)")],
          [part("Difference in Proportions") + " – two-proportion randomization (18/30 vs. 12/30); compare simulation with the formula",
           "Your Turn: Treatment vs Placebo (two-proportion z test from a two-way table)"],
          [hw("6.3", "Nov 15"), quiz(7)] + test(3)),
      row([("Explain why inference for a mean uses the t distribution with df = n − 1.", [5]),
           ("Check the conditions for t procedures.", [5]),
           ("Construct and interpret a t confidence interval for a population mean.", [6]),
           ("Perform a one-sample t test and state the conclusion in context.", [8])],
          [etext("6.2") + " (6.2-D, 6.2-CI, 6.2-HT)", lecture("6.2"), slides("6.2"), "StatKey – Theoretical Distributions (t)"],
          [part("Inference for a Mean") + " – gribbles CI and Chips Ahoy test worked in groups",
           "Your Turn: Testing a Mean (juice bottles underfilled?)"],
          [hw("6.2", "Nov 15"), quiz(7)] + test(3)),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 13
dict(num=13, title="Inference for Two Means and Paired Data", dates="Nov 17 – 19",
     sections=["6.4 Inference for a Difference in Means (Distribution, CI, Hypothesis Test)", "6.5 Paired Difference in Means"],
     rows=[
      row([("Compute the standard error for a difference in two means.", [5]),
           ("Find the conservative degrees of freedom for a two-sample t procedure.", [5]),
           ("Check the conditions for two-sample t procedures.", [5]),
           ("Construct and interpret a confidence interval for μ₁ − μ₂.", [6]),
           ("Explain how the order of the groups affects the sign of the difference.", [6]),
           ("Perform a two-sample t test, choosing the tail from the research question.", [8])],
          [etext("6.4") + " (6.4-D, 6.4-CI, 6.4-HT)", lecture("6.4"), slides("6.4")],
          [part("Comparing Two Means") + " – video games and GPA CI; Pygmalion-effect test",
           "Your Turn: Exercise and Sleep (two-sample t test and CI)"],
          [hw("6.4", "Nov 22")] + test(3)),
      row([("Classify a study design as paired or independent samples.", [1, 8]),
           ("Define the difference variable d and the order of subtraction.", [8]),
           ("Perform a paired t test.", [8]),
           ("Construct and interpret a paired t confidence interval.", [6]),
           ("Explain why pairing reduces variability.", [8])],
          [etext("6.5"), lecture("6.5"), slides("6.5")],
          [part("Paired or Independent?") + " – define d and the order of subtraction",
           "Your Turn: Paired or Unpaired? (class discussion of study scenarios)"],
          [hw("6.5", "Nov 22"), quiz(8)] + test(3)),
     ],
     also=["Last day to withdraw: Thu Nov 19."]),
# ---------------------------------------------------------------- Week 14
dict(num=14, title="Chi-Square Test for Association", dates="Nov 24 – 26",
     sections=["7.2 Testing for an Association Between Two Categorical Variables", "Thanksgiving Holiday – No Class (Thu Nov 26)"],
     rows=[
      row([("State the hypotheses for a chi-square test of association from a two-way table.", [8]),
           ("Compute the expected counts for a two-way table.", [8]),
           ("Check that all expected counts are at least 5.", [8]),
           ("Compute the chi-square statistic and its degrees of freedom, (r − 1)(c − 1).", [8]),
           ("Interpret the right-tail p-value of a chi-square test.", [8]),
           ("Relate the chi-square test on a 2×2 table to the two-proportion z test.", [8]),
           ("Explain why a significant result shows association but not direction or causation.", [8])],
          [etext("7.2"), lecture("7.2"), slides("7.2"), "StatKey – Theoretical Distributions (χ²)"],
          [part("Chi-Square Test"),
           "Your Turn: Faculty Rank and Gender: compute expected counts, cell contributions, χ² and df; decide and interpret"],
          [hw("7.2", "Nov 29")]),
     ],
     also=["Test 3 Retake – Mon Nov 23 – Sun Nov 29 (optional; higher score counts)"]),
# ---------------------------------------------------------------- Week 15
dict(num=15, title="ANOVA and Inference for Slope and Correlation", dates="Dec 1 – 3",
     sections=["8.1 Analysis of Variance", "9.1 Inference for Slope and Correlation"],
     rows=[
      row([("Identify when ANOVA is appropriate.", [8]),
           ("State H₀ and Hₐ for ANOVA in symbols and in words.", [8]),
           ("Explain what SSG and SSE measure.", [8]),
           ("Explain how the ratio of between-group to within-group variability gives evidence against H₀.", [8]),
           ("Complete an ANOVA table (df, MS, F) from given sums of squares.", [8]),
           ("Interpret the F statistic and p-value in context.", [8]),
           ("Check the conditions for ANOVA.", [8])],
          [etext("8.1"), lecture("8.1"), slides("8.1"), "StatKey – Theoretical Distributions (F)"],
          [part("ANOVA") + " – cuckoo-egg example: build the ANOVA table from given SS, find F, decide",
           "Your Turn: Complete the ANOVA Table (fertilizer and seedling growth)"],
          [hw("8.1", "Dec 6")]),
      row([("State the simple linear model.", [7]),
           ("Distinguish the population slope β₁ and correlation ρ from the sample estimates b₁ and r.", [7]),
           ("Interpret the slope in context.", [7]),
           ("Use regression output to test H₀: β₁ = 0 with a t statistic on n − 2 degrees of freedom.", [7, 8]),
           ("Explain why the tests for slope and for correlation give the same p-value.", [7]),
           ("Construct and interpret a confidence interval for the slope.", [6, 7]),
           ("Interpret R² as the proportion of variability in the response explained by the model.", [7]),
           ("Check the conditions for regression inference with a residual plot.", [7])],
          [etext("9.1"), lecture("9.1"), slides("9.1")],
          [part("Inference for Slope and Correlation") + " – SleepStudy: depression score vs. classes missed (test for correlation and slope, CI for slope, R²)",
           "Your Turn: Alcohol and Missed Classes (drinks per week vs. classes missed)"],
          [hw("9.1", "Dec 6")]),
     ],
     also=[]),
# ---------------------------------------------------------------- Week 16
dict(num=16, title="Putting It All Together and Final Exam", dates="Dec 8 – 10",
     sections=["Review: Putting It All Together – From Sampling to Hypothesis Testing (Tue Dec 8)", "Final Exam – Thu Dec 10, online (Blackboard, proctored)"],
     rows=[
      row([("Select the appropriate inference procedure for a research question.", [8]),
           ("Perform a complete hypothesis test, from hypotheses to a conclusion in context.", [8]),
           ("Construct a confidence interval using simulation or a theoretical distribution.", [6]),
           ("Interpret a confidence interval in context.", [6]),
           ("Evaluate whether a study’s design allows its conclusion to be generalized to a population.", [1]),
           ("Evaluate whether a study’s design supports a cause-and-effect conclusion.", [1])],
          ["Review Slides: Putting It All Together (with answer key and no-answers versions)",
           "All Section Slides and Interactive Lectures (Weeks 1–15)", "StatKey"],
          [part("One Complete Test with a Partner") + " – 10 problems, one per pair (narrator/writer roles), 5-minute presentations; extension: build the matching 95% CI"],
          ["Final Exam – Thu Dec 10 (proctored, 2 hours, cumulative; no retake) (all objectives)"]),
     ],
     also=["Late WileyPLUS homework closes Tue Dec 8, 11:59 PM. A higher final exam score replaces the lowest test score."]),
]

DISCREPANCIES = """Blackboard vs. syllabus discrepancies found on Oct 1, 2026 (while reading the course outline):
- Weeks 1-6 were renamed to the RRC convention on Oct 1, 2026 (e-Text: / Interactive Lecture: / Slides: /
  Online Homework: + section number and title; "Participation: Topic"; Kahoots named by topic).
- Weeks 7-16 are hidden and still use the old naming ("Online Homework x.x - MATH 1342", extra
  "Interactive Lecture: Section x.x: Student PowerPoint" items); the maps use the new convention for them too.
  No Participation items exist yet in Weeks 7-16.
- Week 7 contains a duplicate of 3.1 (already in Week 6). 5.1 sits in Week 10 (syllabus: Week 11).
  6.3 sits in Week 11 (syllabus: Week 12).
- Quiz due dates in the hidden weeks fall on Mondays (10/5, 10/12, 10/26, 11/2, 11/16, 11/23);
  the syllabus says Tuesdays. Quiz 1 is 9/9 (syllabus 9/8); Quiz 3 is 10/5 (syllabus Tue 9/29).
- Test 1 Retake, Test 2 and Test 3 have 90-minute limits; the syllabus says 2 hours per test.
- Final Exam due 12/9 in Blackboard; syllabus says Thu Dec 10. Homework 7.2 due 12/6 (expected Sun 11/29).
- The review slide deck still says the final exam is "Thursday, August 6" (summer carry-over).
"""
