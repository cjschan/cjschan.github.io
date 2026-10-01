# -*- coding: utf-8 -*-
"""
Content for the Math 1342 weekly course maps (Fall 2026, TTh Section 036).
Edit this file and re-run build_course_maps.py to regenerate the PDFs.

Each week dict:
  num, title, dates, sections (list of str), notes (str or None)
  mos:  list of (objective_text, [course objective numbers])
  materials / activities / assessments: list of (item_text, "MO codes")
"""

COURSE = "MATH 1342 – Elementary Statistics"
TERM = "Fall 2026 · Section 036 · TTh 6:00–7:20 PM (DIL)"

COURSE_OBJECTIVES = [
    "Interpret ideas of population versus sample, random variables, and techniques of descriptive statistics including frequency distributions, histograms, boxplots, and scatterplots.",
    "Calculate and interpret measures of central tendency and dispersion, including mean, median, standard deviation, and quartiles.",
    "Find and use empirical probabilities in bootstrap distributions to find confidence intervals and in randomization distributions to test hypotheses.",
    "Find and use theoretical probabilities from normal, t, chi-squared and F distributions to form confidence intervals and test hypotheses. Apply the 95% rule to normal and to approximately normal distributions.",
    "Analyze relationships between two quantitative variables using correlation and linear regression.",
    "Analyze data presented in two-way tables to provide information about relationships between categorical variables.",
    "Apply ideas of appropriate sampling techniques and experimental design to data production.",
    "Use the sampling distributions of sample proportions and sample means to answer appropriate questions.",
    "Estimate single means, difference of two means, single proportions and difference of two proportions using confidence intervals. Interpret the results.",
    "Demonstrate skills in hypothesis testing for means and proportions, for single populations and comparison of two populations.",
    "Demonstrate skills in hypothesis testing using chi-squared tests.",
    "Demonstrate skills in inference for regression and ANOVA techniques.",
]

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
}
def etext(sec, title=None, suffix=""):   return f"e-Text: {sec} {TITLES[sec]}{suffix}"
def lecture(sec, suffix=""):             return f"Interactive Lecture: {sec} {TITLES[sec]}{suffix}"
def slides(sec, suffix=""):              return f"Slides: {sec} {TITLES[sec]}{suffix}"
def hw(sec, due, suffix=""):             return f"Online Homework: {sec} {TITLES[sec]}{suffix} (due Sun {due}, 11:59 PM)"
def quiz(n, due):       return f"Take-Home Quiz {n} (due Tue {due}, 11:59 PM)"
def part(topic):        return f"Participation: {topic}"
def proposed(topic):    return f"Participation: {topic}"

WEEKS = [
# ---------------------------------------------------------------- Week 1
dict(num=1, title="Introduction and the Structure of Data", dates="Aug 25 – 27",
     sections=["Introduction: What Is Statistics For?", "1.1 The Structure of Data"],
     notes="First Day™ access: students should open the Wiley course resources this week to keep access.",
     mos=[
      ("Describe statistics as the process of collecting, describing, and analyzing data, and judge a striking result by how likely it is to occur by chance alone.", [1]),
      ("Distinguish a sample from a population and explain how a non-representative sample biases an estimate.", [1, 7]),
      ("Identify the cases and variables in a dataset presented as a table.", [1]),
      ("Classify a variable as categorical or quantitative.", [1]),
      ("Identify the explanatory and response variables in a research question.", [1]),
      ("Compute and compare the mean and median of a small dataset and explain how an outlier affects each.", [2]),
     ],
     materials=[
      ("START HERE: Welcome; Syllabus; Textbook and Wiley Course Resources; Online Tutoring; College Policies & Student Support Services", "None"),
      ("Introduction Slides: What Is Statistics For? (Day 1)", "MO1, MO2, MO6"),
      (etext("1.1"), "MO3, MO4, MO5"),
      (lecture("1.1"), "MO3, MO4, MO5"),
      (slides("1.1"), "MO3, MO4, MO5"),
     ],
     activities=[
      (part("Syllabus") + " – course tour and expectations", "None"),
      ("Day-1 class data activity: collect everyone's age, then find the mean, median, mode and boxplot together; compare the class median to the U.S. median age", "MO1, MO2, MO6"),
      (part("Variables") + " – identify cases, variables and variable types", "MO3, MO4, MO5"),
     ],
     assessments=[
      (hw("1.1", "Aug 30"), "MO3, MO4, MO5"),
     ]),
# ---------------------------------------------------------------- Week 2
dict(num=2, title="Sampling, Experiments and Observational Studies", dates="Sep 1 – 3",
     sections=["1.2 Sampling from a Population", "1.3 Experiments and Observational Studies"],
     notes=None,
     mos=[
      ("Distinguish a population from a sample and describe statistical inference.", [1, 7]),
      ("Identify sampling bias in a described study, classify the sampling method (random, convenience, volunteer), and judge whether the results can be generalized.", [7]),
      ("Recognize bias from question wording, question context, and inaccurate responses.", [7]),
      ("Classify a study as observational or experimental, and identify a plausible confounding variable.", [7]),
      ("Explain how random assignment, a control group, and blinding support cause-and-effect conclusions, and distinguish random sampling (generalize) from random assignment (causation).", [7]),
     ],
     materials=[
      (etext("1.2"), "MO1, MO2, MO3"),
      (lecture("1.2"), "MO1, MO2, MO3"),
      (slides("1.2", " (includes sampling video)"), "MO1, MO2, MO3"),
      (etext("1.3"), "MO4, MO5"),
      (lecture("1.3"), "MO4, MO5"),
      (slides("1.3", " (includes TED-Ed placebo video)"), "MO4, MO5"),
     ],
     activities=[
      (part("Variables in Statistics (Kahoot!)") + " – Tue: review of Week 1", "MO1"),
      (part("Sampling") + " – spot the bias in sample scenarios", "MO2, MO3"),
      (part("Sampling Methods (Kahoot!)") + " – Thu: sampling review", "MO2, MO3"),
      (part("Experiments and Observational Studies") + " – classify studies; confounding; random sampling vs. random assignment", "MO4, MO5"),
     ],
     assessments=[
      (hw("1.2", "Sep 6"), "MO1, MO2, MO3"),
      (hw("1.3", "Sep 6"), "MO4, MO5"),
      (quiz(1, "Sep 8") + " – covers Intro, 1.1–1.3", "MO1–MO5"),
     ]),
# ---------------------------------------------------------------- Week 3
dict(num=3, title="Describing Categorical and Quantitative Variables", dates="Sep 8 – 10",
     sections=["2.1 Categorical Variables", "2.2 One Quantitative Variable: Shape and Center"],
     notes=None,
     mos=[
      ("Construct frequency and relative frequency tables, compute a sample proportion p̂, and distinguish the parameter p from the statistic p̂.", [1]),
      ("Compute and interpret overall and conditional proportions, and a difference in proportions, from a two-way table, choosing the correct denominator.", [6]),
      ("Interpret bar charts, pie charts, side-by-side bar charts, and segmented bar charts.", [1, 6]),
      ("Describe the shape of a distribution (symmetric, left-skewed, right-skewed) from a dotplot or histogram.", [1]),
      ("Compute the mean and median of a dataset and explain how skewness and outliers affect each (resistance).", [2]),
      ("Interpret the standard deviation as the typical distance from the mean and apply the 95% rule to estimate the mean and standard deviation from a bell-shaped dotplot.", [2, 4]),
     ],
     materials=[
      (etext("2.1"), "MO1, MO2, MO3"),
      (lecture("2.1"), "MO1, MO2, MO3"),
      (slides("2.1"), "MO1, MO2, MO3"),
      (etext("2.2"), "MO4, MO5, MO6"),
      (lecture("2.2"), "MO4, MO5, MO6"),
      (slides("2.2"), "MO4, MO5, MO6"),
     ],
     activities=[
      (part("Frequency and Relative Frequency"), "MO1"),
      (part("Finding Proportions from Two-Way Tables"), "MO2, MO3"),
      (part("Quantitative Variables") + " – shape, mean vs. median", "MO4, MO5"),
      ("In-class estimation: estimate the mean and SD of a dotplot without calculating (95% rule)", "MO6"),
     ],
     assessments=[
      (hw("2.1", "Sep 13"), "MO1, MO2, MO3"),
      (hw("2.2", "Sep 13"), "MO4, MO5, MO6"),
     ]),
# ---------------------------------------------------------------- Week 4
dict(num=4, title="Percentiles, Boxplots and Two-Variable Relationships", dates="Sep 15 – 17",
     sections=["2.3 One Quantitative Variable: Percentiles", "2.4 Two Variable Relationships"],
     notes=None,
     mos=[
      ("Compute the sample standard deviation of a small dataset by hand.", [2]),
      ("Compute and interpret z-scores to compare values measured on different scales or in different groups.", [2, 4]),
      ("Find the five-number summary, range, and IQR; apply the 1.5×IQR rule to identify outliers; and construct or interpret a boxplot.", [1, 2]),
      ("Compare a quantitative variable across groups with side-by-side boxplots, and compute and interpret a difference in means.", [1, 2]),
      ("Describe the direction, form, and strength of the relationship in a scatterplot and estimate the correlation r.", [5]),
      ("Use technology to compute r and explain how outliers, nonlinear patterns, and the absence of causation limit its interpretation.", [5]),
     ],
     materials=[
      (etext("2.3"), "MO1, MO2, MO3"),
      (lecture("2.3"), "MO1, MO2, MO3"),
      (slides("2.3"), "MO1, MO2, MO3"),
      (etext("2.4"), "MO4, MO5, MO6"),
      (slides("2.4"), "MO4, MO5, MO6"),
     ],
     activities=[
      (part("One Quantitative Variable (Kahoot!)") + " – Tue: review of 2.2", "MO1"),
      (part("Using Percentiles") + " – Your Turn: comparing heights with z-scores", "MO2, MO3"),
      (part("Box Plots and Outliers") + " – five-number summary, 1.5×IQR rule", "MO3"),
      ("Quick Self-Quizzes: tea vs. coffee boxplots and difference in means; NBA rebounds vs. free-throw % scatterplot; find r with and without an outlier", "MO4, MO5, MO6"),
     ],
     assessments=[
      (hw("2.3", "Sep 20"), "MO1, MO2, MO3"),
      (hw("2.4", "Sep 20"), "MO4, MO5, MO6"),
      (quiz(2, "Sep 22") + " – covers 2.1–2.4", "MO1–MO6"),
     ]),
# ---------------------------------------------------------------- Week 5
dict(num=5, title="Linear Regression", dates="Sep 22 – 24",
     sections=["2.5 Two Quantitative Variables: Linear Regression", "Catch-Up Day (Thu Sep 24)"],
     notes="Interactive Lecture 2.5b is the 3e video labeled “Section 2.6”; it covers 2.5 in the 4e. Test 1 opens Fri Oct 2.",
     mos=[
      ("Interpret the slope and intercept of a regression line in context with correct units, and judge whether the intercept is meaningful.", [5]),
      ("Use a regression equation to predict a response value.", [5]),
      ("Compute and interpret a residual, and locate positive and negative residuals on a scatterplot.", [5]),
      ("Use technology to find the least-squares regression line and explain what “least squares” means.", [5]),
      ("Recognize when a regression prediction is not appropriate: extrapolation, nonlinearity, influential outliers, and causal claims.", [5]),
     ],
     materials=[
      (etext("2.5"), "MO1–MO5"),
      ("Interactive Lecture: Section 2.5 Two Quantitative Variables: Linear Regression (Part 1)", "MO1, MO2, MO3"),
      ("Interactive Lecture: Section 2.5 Two Quantitative Variables: Linear Regression (Part 2)", "MO4, MO5"),
      (slides("2.5"), "MO1–MO5"),
     ],
     activities=[
      (part("Two Variable Relationships") + " – Tue: correlation review, Your Turn: spotting residuals", "MO3"),
      (part("Regression Line") + " – Thu: baseball game length and used-car price problems", "MO1, MO2, MO3, MO5"),
      ("Example 2 (commute distance and time): find the regression line with technology and predict", "MO2, MO4"),
     ],
     assessments=[
      (hw("2.5", "Sep 27"), "MO1–MO5"),
      ("Practice Test 1 (Blackboard, due Thu Oct 1, 11:59 PM; 120 min, proctoring practice)", "None"),
     ]),
# ---------------------------------------------------------------- Week 6
dict(num=6, title="Probability Rules and Sampling Distributions", dates="Sep 29 – Oct 1",
     sections=["P.1 Probability Rules", "3.1 Sampling Distributions"],
     notes="Test 1 window Fri Oct 2 – Sun Oct 4 (covers Intro, 1.1–1.3, 2.1–2.5). P.1 probability rules are not among the 12 Common Course Objectives; they support Student Learning Outcome 3 and underpin CO3/CO4.",
     mos=[
      ("Compute probabilities for equally likely outcomes and apply the complement rule.", []),
      ("Apply the addition, multiplication, and conditional probability rules using a two-way table, and distinguish disjoint events from independent events.", [6]),
      ("Classify a numerical summary as a parameter or a statistic and use the correct notation (μ, σ, p, ρ vs. x̄, s, p̂, r).", [8]),
      ("Describe how a sampling distribution is built from repeated samples, what each dot represents, and its center and shape.", [8]),
      ("Explain the standard error as the variability of a statistic and predict how sample size affects it.", [8]),
     ],
     materials=[
      (etext("P.1"), "MO1, MO2"),
      (lecture("P.1"), "MO1, MO2"),
      (slides("P.1"), "MO1, MO2"),
      (etext("3.1"), "MO3, MO4, MO5"),
      (lecture("3.1"), "MO3, MO4, MO5"),
      (slides("3.1"), "MO3, MO4, MO5"),
     ],
     activities=[
      (part("Probability") + " – Rock and Roll Hall of Fame two-way table; cards with and without replacement", "MO1, MO2"),
      (proposed("Sampling Distributions") + " – M&M activity: each student draws 10 M&Ms, computes p̂ (blue), and adds it to a class dotplot; name the population, sample, and what each dot represents", "MO3, MO4, MO5"),
     ],
     assessments=[
      (hw("P.1", "Oct 4"), "MO1, MO2"),
      (hw("3.1", "Oct 4"), "MO3, MO4, MO5"),
      (quiz(3, "Sep 29") + " – covers 2.5", "None"),
      ("Test 1 – Fri Oct 2 – Sun Oct 4 (Blackboard, proctored, 2 hours). Covers Weeks 1–5.", "None"),
     ]),
# ---------------------------------------------------------------- Week 7
dict(num=7, title="Confidence Intervals and the Bootstrap", dates="Oct 6 – 8",
     sections=["3.2 Understanding and Interpreting Confidence Intervals", "3.3 Constructing Bootstrap Confidence Intervals Using Standard Error"],
     notes="Test 1 Retake window Mon Oct 5 – Sun Oct 11.",
     mos=[
      ("Construct a 95% confidence interval for a mean or proportion as statistic ± 2·SE, given the statistic and its standard error.", [9]),
      ("Interpret a confidence interval in context, explain the confidence level as the long-run capture rate of the method, and identify common misinterpretations.", [9]),
      ("Describe how a bootstrap sample and a bootstrap distribution are created, and explain why the bootstrap distribution is centered at the sample statistic.", [3]),
      ("Use StatKey to generate a bootstrap distribution and estimate the standard error as its standard deviation.", [3]),
      ("Construct and interpret a 95% bootstrap confidence interval using the standard-error method.", [3, 9]),
     ],
     materials=[
      (etext("3.2"), "MO1, MO2"),
      (lecture("3.2"), "MO1, MO2"),
      (slides("3.2"), "MO1, MO2"),
      (etext("3.3"), "MO3, MO4, MO5"),
      (lecture("3.3"), "MO3, MO4, MO5"),
      (slides("3.3", " (embedded StatKey simulator)"), "MO3, MO4, MO5"),
      ("StatKey (lock5stat.com/statkey) – Bootstrap Confidence Intervals", "MO4, MO5"),
     ],
     activities=[
      (proposed("Interpreting Confidence Intervals") + " – which of 20 simulated CIs capture μ; fix three misinterpretations", "MO1, MO2"),
      (proposed("Bootstrap a Proportion") + " – Try It: 32 of 50 prefer Brand A; build the bootstrap distribution, read off SE, form the CI", "MO3, MO4, MO5"),
     ],
     assessments=[
      (hw("3.2", "Oct 11"), "MO1, MO2"),
      (hw("3.3", "Oct 11"), "MO3, MO4, MO5"),
      ("Test 1 Retake – Mon Oct 5 – Sun Oct 11 (optional; higher score counts)", "None"),
     ]),
# ---------------------------------------------------------------- Week 8
dict(num=8, title="Percentile Intervals and Introducing Hypothesis Tests", dates="Oct 13 – 15",
     sections=["3.4 Bootstrap Confidence Intervals Using Percentiles", "4.1 Introducing Hypothesis Tests"],
     notes=None,
     mos=[
      ("Determine which percentiles of a bootstrap distribution bound a 90%, 95%, or 99% confidence interval, and construct the interval with StatKey.", [3, 9]),
      ("Predict how changing the confidence level or the sample size affects the width of an interval.", [9]),
      ("Judge whether a bootstrap confidence interval is trustworthy from the shape of the bootstrap distribution and whether the sample is representative.", [3]),
      ("Identify the parameter of interest and write null and alternative hypotheses from a research question.", [10]),
      ("Classify a test as right-tailed, left-tailed, or two-tailed, and explain the logic of assuming H₀ and asking whether the data are surprising.", [10]),
     ],
     materials=[
      (etext("3.4"), "MO1, MO2, MO3"),
      (lecture("3.4"), "MO1, MO2, MO3"),
      (slides("3.4"), "MO1, MO2, MO3"),
      (etext("4.1"), "MO4, MO5"),
      (lecture("4.1"), "MO4, MO5"),
      (slides("4.1"), "MO4, MO5"),
     ],
     activities=[
      (proposed("Percentile Confidence Intervals") + " – StatKey: 90/95/99% intervals for the same data; compare SE and percentile methods", "MO1, MO2, MO3"),
      (proposed("Writing Hypotheses") + " – Zener-card ESP practice (26 of 50): define the parameter, state H₀ and Hₐ, choose the tail", "MO4, MO5"),
      ("Think about it: is 15 of 16 correct (dolphin study) convincing?", "MO5"),
     ],
     assessments=[
      (hw("3.4", "Oct 18"), "MO1, MO2, MO3"),
      (hw("4.1", "Oct 18"), "MO4, MO5"),
      (quiz(4, "Oct 13") + " – covers P.1, 3.1–3.3", "None"),
     ]),
# ---------------------------------------------------------------- Week 9
dict(num=9, title="P-values and Statistical Significance", dates="Oct 20 – 22",
     sections=["4.2 Measuring Evidence with p-values", "4.3 Determining Statistical Significance"],
     notes=None,
     mos=[
      ("Describe how a randomization distribution is generated assuming H₀ is true, and identify its center as the null value.", [3]),
      ("Compare sampling, bootstrap, and randomization distributions by their center and purpose.", [3, 8]),
      ("Compute a p-value from a randomization distribution as a proportion of simulated statistics, choosing the correct tail(s) from Hₐ.", [3, 10]),
      ("Interpret a p-value in context and relate its size to the strength of evidence against H₀.", [10]),
      ("Compare the p-value to α, decide whether to reject H₀, write a two-step conclusion in context, and avoid saying “accept H₀”.", [10]),
     ],
     materials=[
      (etext("4.2"), "MO1, MO2, MO3, MO4"),
      (lecture("4.2"), "MO1, MO2, MO3, MO4"),
      (slides("4.2"), "MO1, MO2, MO3, MO4"),
      (etext("4.3"), "MO4, MO5"),
      (lecture("4.3"), "MO4, MO5"),
      (slides("4.3", " (includes “What is a p-value?” video)"), "MO4, MO5"),
      ("StatKey – Randomization Hypothesis Tests", "MO1, MO3"),
     ],
     activities=[
      (proposed("Randomization Distributions") + " – StatKey: dolphin study (16 flips) and tea vs. coffee re-randomization; count how many simulated statistics are as extreme as observed", "MO1, MO2, MO3"),
      (proposed("P-values and Conclusions") + " – resveratrol examples (p = 0.04, 0.12, 0.0003): strength of evidence, decision at α, conclusion in context", "MO4, MO5"),
     ],
     assessments=[
      (hw("4.2", "Oct 25"), "MO1, MO2, MO3, MO4"),
      (hw("4.3", "Oct 25"), "MO4, MO5"),
      (quiz(5, "Oct 27") + " – covers 3.4, 4.1–4.3", "MO1–MO5"),
     ]),
# ---------------------------------------------------------------- Week 10
dict(num=10, title="A Closer Look at Testing and Making Connections", dates="Oct 27 – 29",
     sections=["4.4(a) A Closer Look at Testing", "4.5 Making Connections"],
     notes="Test 2 window Fri Oct 30 – Sun Nov 1 (covers P.1, 3.1–3.4, 4.1–4.3).",
     mos=[
      ("Describe Type I and Type II errors in the context of a study, relate α to the probability of a Type I error, and explain the trade-off between the two errors and the effect of sample size.", [10]),
      ("Explain how multiple testing and publication bias produce false positives, and distinguish statistical significance from practical significance.", [10]),
      ("Describe how to generate randomization samples for a given study design (coin flips, re-randomizing groups, shifting data then bootstrapping).", [3]),
      ("Compare bootstrap and randomization distributions by their center and use, identifying each center for given data.", [3]),
      ("Use a 95% confidence interval to reach a two-tailed test conclusion at α = 0.05, and decide whether a confidence interval or a hypothesis test fits a research question.", [9, 10]),
     ],
     materials=[
      (etext("4.4"), "MO1, MO2"),
      (lecture("4.4"), "MO1, MO2"),
      (slides("4.4", " (includes Khan Academy Type I/II video)"), "MO1, MO2"),
      (etext("4.5"), "MO3, MO4, MO5"),
      (lecture("4.5"), "MO3, MO4, MO5"),
      (slides("4.5"), "MO3, MO4, MO5"),
     ],
     activities=[
      (proposed("Errors in Testing") + " – battery-life example (a)–(d): describe each error in context; courtroom analogy matching; vitamin E multiple-testing questions", "MO1, MO2"),
      (proposed("Making Connections") + " – body temperature: test 98.6 using the CI (98.05, 98.47); sleep study (28/50): how to generate randomization samples and where each distribution is centered", "MO3, MO4, MO5"),
     ],
     assessments=[
      (hw("4.4", "Nov 1", " (a)"), "MO1, MO2"),
      (hw("4.5", "Nov 1"), "MO3, MO4, MO5"),
      ("Practice Test 2 (Blackboard, by Sun Nov 1)", "None"),
      ("Test 2 – Fri Oct 30 – Sun Nov 1 (Blackboard, proctored, 2 hours). Covers Weeks 6–9.", "None"),
      (quiz(6, "Nov 3") + " – covers 4.4, 4.5", "MO1–MO5"),
     ]),
# ---------------------------------------------------------------- Week 11
dict(num=11, title="Normal Distributions and Inference for a Proportion", dates="Nov 3 – 5",
     sections=["5.1 Hypothesis Testing Using Normal Distributions", "6.1 Inference for a Proportion (Distribution, CI, Hypothesis Test)"],
     notes="Test 2 Retake window Mon Nov 2 – Sun Nov 8.",
     mos=[
      ("Explain when the Central Limit Theorem justifies replacing a simulated randomization distribution with a normal distribution N(null value, SE).", [4, 8]),
      ("Compute a standardized z statistic and find the p-value as a right-tail, left-tail, or two-tail area of the standard normal distribution.", [4, 10]),
      ("Check the large-sample condition (at least 10 in each category) for inference about one proportion.", [8]),
      ("Construct and interpret a confidence interval for a population proportion with z* for 90%, 95%, or 99% confidence.", [4, 9]),
      ("Carry out a one-proportion z test and conclude in context, and explain why the CI standard error uses p̂ while the test uses p₀.", [4, 10]),
     ],
     materials=[
      (etext("5.1"), "MO1, MO2"),
      (lecture("5.1"), "MO1, MO2"),
      (slides("5.1"), "MO1, MO2"),
      (etext("6.1") + " (6.1-D Distribution, 6.1-CI Confidence Interval, 6.1-HT Hypothesis Test)", "MO3, MO4, MO5"),
      (lecture("6.1"), "MO3, MO4, MO5"),
      (slides("6.1"), "MO3, MO4, MO5"),
      ("StatKey – Theoretical Distributions (Normal)", "MO2, MO4"),
     ],
     activities=[
      (proposed("Normal Distributions and z") + " – malaria/mosquito example: compute z, shade the tail in StatKey, find the p-value", "MO1, MO2"),
      (proposed("Inference for a Proportion") + " – 4-step CI and 4-step test for a proportion (voting example); compare the two SEs", "MO3, MO4, MO5"),
     ],
     assessments=[
      (hw("5.1", "Nov 8"), "MO1, MO2"),
      (hw("6.1", "Nov 8"), "MO3, MO4, MO5"),
      ("Test 2 Retake – Mon Nov 2 – Sun Nov 8 (optional; higher score counts)", "None"),
     ]),
# ---------------------------------------------------------------- Week 12
dict(num=12, title="Inference for Two Proportions and for a Mean", dates="Nov 10 – 12",
     sections=["6.3 Inference for a Difference in Proportions (Distribution, CI, Hypothesis Test)", "6.2 Inference for a Mean (Distribution, CI, Hypothesis Test)"],
     notes=None,
     mos=[
      ("Classify a study as calling for one-proportion or difference-in-proportions inference, and check the conditions.", [8]),
      ("Construct and interpret a confidence interval for p₁ − p₂, including what its sign means and whether it contains 0.", [9]),
      ("Compute the pooled proportion and carry out a two-proportion z test from summary data or a two-way table.", [10]),
      ("Explain why inference for a mean uses the t distribution with df = n − 1, and check the conditions for t procedures.", [4]),
      ("Construct and interpret a t confidence interval for a population mean, and carry out a one-sample t test.", [4, 9, 10]),
     ],
     materials=[
      (etext("6.3") + " (6.3-D, 6.3-CI, 6.3-HT)", "MO1, MO2, MO3"),
      (lecture("6.3"), "MO1, MO2, MO3"),
      (slides("6.3", " (embedded StatKey two-proportion randomization)"), "MO1, MO2, MO3"),
      (etext("6.2") + " (6.2-D, 6.2-CI, 6.2-HT)", "MO4, MO5"),
      (lecture("6.2"), "MO4, MO5"),
      (slides("6.2"), "MO4, MO5"),
      ("StatKey – Theoretical Distributions (t)", "MO4, MO5"),
     ],
     activities=[
      (proposed("Difference in Proportions") + " – Try It: two-proportion randomization (18/30 vs. 12/30); treatment vs. placebo two-way table practice; compare simulation with the formula", "MO1, MO2, MO3"),
      (proposed("Inference for a Mean") + " – gribbles CI and Chips Ahoy test worked in groups", "MO4, MO5"),
     ],
     assessments=[
      (hw("6.3", "Nov 15"), "MO1, MO2, MO3"),
      (hw("6.2", "Nov 15"), "MO4, MO5"),
      (quiz(7, "Nov 17") + " – covers 5.1, 6.1–6.3", "MO1–MO5"),
     ]),
# ---------------------------------------------------------------- Week 13
dict(num=13, title="Inference for Two Means and Paired Data", dates="Nov 17 – 19",
     sections=["6.4 Inference for a Difference in Means (Distribution, CI, Hypothesis Test)", "6.5 Paired Difference in Means"],
     notes="Last day to withdraw: Thu Nov 19. Test 3 window Fri Nov 20 – Sun Nov 22 (covers 4.4, 4.5, 5.1, 6.1–6.5).",
     mos=[
      ("Compute the standard error and conservative degrees of freedom for a difference in two independent means, and check the conditions.", [4, 8]),
      ("Construct and interpret a confidence interval for μ₁ − μ₂, explaining how the order of the groups affects the sign.", [9]),
      ("Carry out a two-sample t test, choosing the tail from the research question.", [10]),
      ("Classify a study design as paired or independent samples by checking for a link between observations.", [7, 10]),
      ("Define the difference variable d, carry out a paired t test and paired t confidence interval, and explain why pairing reduces variability.", [9, 10]),
     ],
     materials=[
      (etext("6.4") + " (6.4-D, 6.4-CI, 6.4-HT)", "MO1, MO2, MO3"),
      (lecture("6.4"), "MO1, MO2, MO3"),
      (slides("6.4"), "MO1, MO2, MO3"),
      (etext("6.5"), "MO4, MO5"),
      (lecture("6.5"), "MO4, MO5"),
      (slides("6.5"), "MO4, MO5"),
     ],
     activities=[
      (proposed("Comparing Two Means") + " – video games and GPA CI; Pygmalion-effect test", "MO1, MO2, MO3"),
      (proposed("Paired or Independent?") + " – class discussion of eight study scenarios (a)–(h); define d and the order of subtraction", "MO4, MO5"),
     ],
     assessments=[
      (hw("6.4", "Nov 22"), "MO1, MO2, MO3"),
      (hw("6.5", "Nov 22"), "MO4, MO5"),
      ("Test 3 – Fri Nov 20 – Sun Nov 22 (Blackboard, proctored, 2 hours). Covers Weeks 10–13.", "MO1–MO5"),
     ]),
# ---------------------------------------------------------------- Week 14
dict(num=14, title="Chi-Square Test for Association", dates="Nov 24 – 26",
     sections=["7.2 Testing for an Association Between Two Categorical Variables", "Thanksgiving Holiday – No Class (Thu Nov 26)"],
     notes="Test 3 Retake window Mon Nov 23 – Sun Nov 29.",
     mos=[
      ("State the hypotheses for a chi-square test of association from a two-way table.", [6, 11]),
      ("Compute expected counts and check that all expected counts are at least 5.", [11]),
      ("Compute the chi-square statistic and df = (r − 1)(c − 1), and interpret the right-tail p-value.", [4, 11]),
      ("Relate the chi-square test on a 2×2 table to the two-proportion z test, and explain that a significant result shows association but not direction or causation.", [11]),
     ],
     materials=[
      (etext("7.2"), "MO1–MO4"),
      (lecture("7.2"), "MO1–MO4"),
      (slides("7.2"), "MO1–MO4"),
      ("StatKey – Theoretical Distributions (χ²)", "MO3"),
     ],
     activities=[
      (proposed("Chi-Square Test") + " – faculty rank × gender: compute expected counts, cell contributions, χ² and df; decide and interpret", "MO1, MO2, MO3, MO4"),
     ],
     assessments=[
      (hw("7.2", "Nov 29"), "MO1–MO4"),
      (quiz(8, "Nov 24") + " – covers 6.4, 6.5", "None"),
      ("Test 3 Retake – Mon Nov 23 – Sun Nov 29 (optional; higher score counts)", "None"),
     ]),
# ---------------------------------------------------------------- Week 15
dict(num=15, title="ANOVA and Putting It All Together", dates="Dec 1 – 3",
     sections=["8.1 Analysis of Variance", "Review: Putting It All Together – From Sampling to Hypothesis Testing"],
     notes=None,
     mos=[
      ("Identify when ANOVA is appropriate and state H₀ and Hₐ in symbols and words.", [12]),
      ("Explain what SSG and SSE measure and how the ratio of between-group to within-group variability gives evidence against H₀.", [12]),
      ("Complete an ANOVA table (df, MS, F) from given sums of squares, interpret the F statistic and p-value, and check the conditions.", [4, 12]),
      ("Choose the correct test among one- and two-proportion z, one- and two-sample t, paired t, and chi-square, and carry out a complete six-step hypothesis test.", [10, 11]),
      ("Explain what the study design (random sampling vs. random assignment) allows a conclusion to claim, and distinguish statistical from practical significance.", [7, 10]),
     ],
     materials=[
      (etext("8.1"), "MO1, MO2, MO3"),
      (lecture("8.1"), "MO1, MO2, MO3"),
      (slides("8.1"), "MO1, MO2, MO3"),
      ("Review Slides: Putting It All Together (with answer key and no-answers versions)", "MO4, MO5"),
      ("StatKey – Theoretical Distributions (F)", "MO3"),
     ],
     activities=[
      (proposed("ANOVA") + " – cuckoo-egg example: build the ANOVA table from given SS, find F, decide", "MO1, MO2, MO3"),
      (proposed("One Complete Test with a Partner") + " – 10 problems, one per pair (narrator/writer roles), 5-minute presentations; extension: build the matching 95% CI", "MO4, MO5"),
     ],
     assessments=[
      (hw("8.1", "Dec 6"), "MO1, MO2, MO3"),
     ]),
# ---------------------------------------------------------------- Week 16
dict(num=16, title="Final Exam", dates="Dec 8 – 10",
     sections=["Review & Catch-Up for the Final Exam (Tue Dec 8)", "Final Exam – Thu Dec 10, online (Blackboard, proctored)"],
     notes="Late WileyPLUS homework closes Tue Dec 8, 11:59 PM. The final exam is cumulative; a higher final replaces the lowest test score.",
     mos=[
      ("Select and justify an appropriate inference procedure (CI or test; proportion, mean, two groups, paired, chi-square, ANOVA) for a new scenario.", [9, 10, 11, 12]),
      ("Carry out and interpret a complete confidence interval or hypothesis test, using simulation or theoretical distributions as appropriate.", [3, 4, 9, 10]),
      ("Interpret results in context, including what the study design allows the conclusion to claim about generalization and causation.", [7]),
     ],
     materials=[
      ("Review Slides: Putting It All Together (answer key)", "MO1, MO2, MO3"),
      ("All Section Slides and Interactive Lectures (Weeks 1–15)", "MO1, MO2, MO3"),
      ("StatKey", "MO2"),
     ],
     activities=[
      ("Review & catch-up session (Tue Dec 8): student-selected problems; choosing-the-right-test table", "MO1, MO2, MO3"),
     ],
     assessments=[
      ("Final Exam – Thu Dec 10 (Blackboard, proctored, 2 hours, cumulative; no retake)", "MO1, MO2, MO3"),
     ]),
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
- P.1 probability rules are not in the 12 Common Course Objectives (they are in Student Learning Outcome 3).
"""
