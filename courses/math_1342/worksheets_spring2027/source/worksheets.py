"""The 10 participation worksheets (and their answer keys) for Spring 2027 Math 1342.

Problems and data are kept from the original Fall worksheets (originals/ folder).
Answer-key numbers come from compute_keys.py (formulas, and seeded StatKey-style
simulations on the Lock5 datasets) and are rounded here.
"""
from wslib import Doc

UPLOAD = "Type your answers into this file. When you're done, save it and upload it to the Blackboard activity as a .docx or PDF."
STATKEY = "Use StatKey (lock5stat.com/StatKey) where the problem asks for it, and paste a screenshot of your dotplot in the space given."


def w08(d: Doc):
    d.directions(["Work with a neighbor, but write your own answers.", STATKEY, UPLOAD])
    d.problem("Problem 1. Body Temperature",
              "Is normal body temperature really 98.6°F? A sample of body temperatures for 50 healthy individuals was taken. "
              "Find this dataset in StatKey under **Confidence Interval for a Mean** (or as **BodyTemp50** in the textbook datasets).")
    d.step("(a)", "What is the sample mean? What is the sample standard deviation?",
           ["x̄ = 98.26°F and s = 0.765°F."], lines=1)
    d.step("(b)", "Generate a bootstrap distribution using at least 1,000 simulated statistics. What is the standard error? Paste a screenshot of your dotplot.",
           ["SE ≈ 0.11°F (your StatKey value should be close to 0.107).",
            "The bootstrap distribution is bell-shaped and centered at the sample mean, 98.26."], box=2.0)
    d.step("(c)", "Use the standard error to find a 95% confidence interval. Show your work. Is 98.6 in the interval?",
           ["x̄ ± 2·SE = 98.26 ± 2(0.11) = 98.26 ± 0.22, so about **98.04°F to 98.48°F**.",
            "98.6 is **not** in the interval, so 98.6°F is not a plausible value for the mean body temperature."], lines=2)
    d.step("(d)", "Using the same distribution, find a 95% confidence interval with the **Two-Tail** option in StatKey (the percentile method). Paste a screenshot and give your interval.",
           ["Put 0.95 in the middle box; the endpoints are the 2.5th and 97.5th percentiles.",
            "95% percentile interval ≈ **98.05°F to 98.47°F**."], box=2.0)
    d.step("(e)", "Compare the two 95% confidence intervals. Are they similar?",
           ["Yes. Both are about 98.05 to 98.47. When the bootstrap distribution is symmetric and bell-shaped, "
            "the two methods give nearly the same interval."], lines=1)
    d.step("(f)", "Still using the same bootstrap distribution, give a 99% confidence interval.",
           ["Put 0.99 in the middle box: the 0.5th and 99.5th percentiles give about **97.99°F to 98.55°F**."], lines=1)
    d.step("(g)", "Is the 99% confidence interval wider or narrower than the 95% confidence interval?",
           ["**Wider.** To be more confident, we need to include a wider range of plausible values."], lines=1)
    d.step("(h)", "Clearly interpret the 99% confidence interval in context.",
           ["We are 99% sure that the mean body temperature of **all healthy people** is between about 97.99°F and 98.55°F. "
            "(98.6 is still outside this interval.)"], lines=2)

    d.problem("Problem 2. Do Ovulating Women Affect Men's Speech?",
              "In a study (Exercise B.18), men were paired with a woman who was either in a fertile phase of her cycle or in a not-fertile phase. "
              "For men paired with a woman in a less fertile stage, 38 of the 61 men copied their partner's sentence construction. "
              "For men paired with a woman at peak fertility, 30 of the 62 men copied their partner's sentence construction.")
    d.step("", "Use StatKey (**CI for Difference in Proportions**; enter the counts with **Edit Data**) to find a 90% confidence interval for the difference in the proportion who match their partner's sentence construction, "
              "not fertile minus fertile. Is zero in the interval? Interpret the interval in context.",
           ["Sample statistic: p̂_{N} − p̂_{F} = 38/61 − 30/62 = 0.623 − 0.484 = **0.139**.",
            "90% percentile interval (5th and 95th percentiles) ≈ **−0.007 to 0.285** (bootstrap SE ≈ 0.088).",
            "**Zero is (just barely) inside the interval**, so \"no difference\" is a plausible value.",
            "We are 90% sure that the proportion of men who copy their partner's sentence construction is between 0.007 lower and 0.285 higher "
            "when paired with a not-fertile woman than when paired with a fertile woman."], box=2.4, indent=0)

    d.problem("Problem 3. Problems with Bootstrap Distributions",
              "If a bootstrap distribution is not relatively symmetric, it is not appropriate to use the methods of this section to build a confidence interval. "
              "Consider this dataset:   **5, 6, 7, 8, 25, 100**")
    d.step("(a)", "What is the standard deviation of this dataset?",
           ["s ≈ **37.41**."], lines=1)
    d.step("(b)", "Use StatKey (**CI for Single Mean, Median, Std. Dev.**, then choose Standard Deviation) to create a bootstrap distribution for the standard deviation. "
                  "Describe the distribution and paste a screenshot. Is it symmetric and bell-shaped?",
           ["It is **not** symmetric or bell-shaped. It has two separate clumps: one near 0 to 10 (bootstrap samples that leave out the 100) "
            "and a larger one near 35 to 50 (samples that include the 100), with a gap in between."], box=2.0)
    d.step("(c)", "Is it appropriate to use the methods of this section to find a bootstrap confidence interval for this standard deviation?",
           ["**No.** The percentile and ±2·SE methods only work when the bootstrap distribution is reasonably symmetric and bell-shaped."], lines=1)
    d.step("(d)", "Discuss with a neighbor why the bootstrap distribution might look the way it does.",
           ["The value 100 is an extreme outlier and the sample is tiny (n = 6). Each bootstrap sample either includes 100 or doesn't, "
            "and that one value decides whether the standard deviation is large or small, which splits the distribution into two clumps."], lines=2)
    d.end("End of worksheet")


def w10(d: Doc):
    d.directions(["Use a 5% significance level unless a question says otherwise.", STATKEY, UPLOAD])
    d.problem("Problem 1. Red Wine and Weight Loss",
              "Resveratrol, an ingredient in red wine and grapes, has been shown to promote weight loss in animals. In one study, a sample of lemurs had various "
              "measurements taken before and after receiving resveratrol supplements for 4 weeks. For each p-value, give the formal conclusion and a conclusion in context. Use a 5% significance level.")
    d.step("(a)", "In the test to see if the mean resting metabolic rate is higher after treatment, the p-value is 0.013.",
           ["0.013 < 0.05, so **reject H₀**.",
            "There is evidence that the mean resting metabolic rate of lemurs is higher after 4 weeks of resveratrol."], lines=2)
    d.step("(b)", "In the test to see if the mean body mass is lower after treatment, the p-value is 0.007.",
           ["0.007 < 0.05, so **reject H₀**.",
            "There is evidence that the mean body mass of lemurs is lower after 4 weeks of resveratrol."], lines=2)
    d.step("(c)", "Which of the two results above are significant at a 1% level?",
           ["Only **(b)**: 0.007 < 0.01, but 0.013 > 0.01."], lines=1)

    d.problem("Problem 2. Multiple Sclerosis and Sunlight",
              "It is believed that sunlight offers some protection against multiple sclerosis (MS), but the reason is unknown. In an experiment, mice were injected with a substance "
              "to give them MS and were randomly assigned to a control group (no treatment), a group that received vitamin D supplements, or a group that was regularly exposed to UV light. "
              "Mice exposed to UV light were significantly less likely to get MS than the control mice, but vitamin D did not seem to reduce the likelihood of MS compared to the control group. "
              "For these two tests, one p-value was 0.470 and one was 0.002.")
    d.step("", "Which p-value goes with which test? For each test, do we \"Reject H₀\" or \"Do not reject H₀\"?",
           ["**UV light vs. control: p-value = 0.002** (significant). Reject H₀.",
            "**Vitamin D vs. control: p-value = 0.470** (not significant). Do not reject H₀."], lines=2, indent=0)

    d.problem("Problem 3. Determining Significance",
              "Here are the p-values for four different tests:   Test A: 0.23     Test B: 0.008     Test C: 0.03     Test D: 0.094")
    d.step("(a)", "Which tests are significant at a 10% level? At a 5% level? At a 1% level?",
           ["10% level: **B, C, D**.   5% level: **B, C**.   1% level: **B** only."], lines=2)
    d.step("(b)", "Using a 5% significance level, give the formal conclusion for each test.",
           ["A: Do not reject H₀.   B: Reject H₀.   C: Reject H₀.   D: Do not reject H₀."], lines=2)

    d.problem("Problem 4. Making Conclusions")
    d.step("1.", "In a hypothesis test of H₀: μ = 18 vs Hₐ: μ > 18, we obtain a p-value of 0.016. Using α = 0.05, we conclude:     "
                 "(a) Reject H₀     (b) Do not reject H₀     (c) Reject Hₐ     (d) Do not reject Hₐ",
           ["**(a) Reject H₀**, since 0.016 < 0.05. (We never \"reject Hₐ.\")"], lines=1)
    d.step("2.", "For the same test and p-value, we conclude:     (a) There is evidence that μ = 18     (b) There is evidence that μ > 18     (c) There is no evidence of anything",
           ["**(b) There is evidence that μ > 18.**"], lines=1)

    d.problem("Problem 5. Playing with StatKey",
              "Is there evidence of a difference in mean time spent exercising between males and females? In the sample, the 20 males exercise a mean of 12.4 hours a week "
              "and the 30 females a mean of 9.4 hours a week.")
    d.step("(a)", "What is the observed (sample) statistic?",
           ["x̄_{M} − x̄_{F} = 12.4 − 9.4 = **3.0 hours**."], lines=1)
    d.step("(b)", "State the hypotheses. Define the parameters.",
           ["H₀: μ_{M} = μ_{F}     Hₐ: μ_{M} ≠ μ_{F}",
            "μ_{M} and μ_{F} are the mean hours of exercise per week for all male and all female students."], lines=2)
    d.step("(c)", "Use the **ExerciseHours** dataset in StatKey (**Test for Difference in Means**) to generate a randomization distribution and find the p-value. Paste a screenshot.",
           ["The randomization distribution is centered at 0. The test is two-tailed, so use Two-Tail at 3.0 (or double the right-tail proportion).",
            "p-value ≈ **0.21** (about 2 × 0.105; values from 0.19 to 0.23 are typical)."], box=2.0)
    d.step("(d)", "Make a conclusion in context.",
           ["0.21 > 0.05, so **do not reject H₀**. The data do not provide evidence that the mean exercise time differs between male and female students."], lines=2)
    d.end("End of worksheet")


def w12a(d: Doc):
    d.directions(["Use a 5% significance level.", "Show the formula with the numbers plugged in on every calculation.",
                  "Find normal-curve areas with StatKey (**Theoretical Distributions → Normal**) or a calculator.", UPLOAD])
    d.problem("Mendel's Green Peas",
              "One of Gregor Mendel's famous genetic experiments dealt with raising pea plants. According to Mendel's genetic theory, under a certain set of conditions the proportion of "
              "pea plants that produce smooth green peas should be p = 3/16 = 0.1875. A sample of n = 556 plants from the experiment had 108 with smooth green peas. "
              "Does this provide evidence of a problem with Mendel's theory, that is, that the proportion is different from 3/16?")
    d.step("Step 1.", "Identify the parameter. In words, p is…",
           ["p = the proportion of **all** such pea plants (grown under these conditions) that produce smooth green peas."])
    d.step("Step 2.", "State the hypotheses. Is the test left-tailed, right-tailed, or two-tailed?",
           ["H₀: p = 0.1875     Hₐ: p ≠ 0.1875     **Two-tailed**."], lines=2)
    d.step("Step 3.", "Find the sample statistic:  p̂ = 108 ÷ 556 =",
           ["p̂ = 108 ÷ 556 = **0.194**"])
    d.step("Step 4.", "Check the conditions for using a normal distribution:  n·p₀ = 556 × 0.1875 = ___   and   n·(1 − p₀) = 556 × 0.8125 = ___ .  Are both at least 10?",
           ["n·p₀ = 104.25 and n·(1 − p₀) = 451.75. **Both are at least 10**, so the normal distribution is appropriate."], lines=2)
    d.step("Step 5.", "Find the standard error, using the null value p₀:   SE = √( p₀(1 − p₀) ÷ n )",
           ["SE = √(0.1875 × 0.8125 ÷ 556) = **0.0166**"], lines=2)
    d.step("Step 6.", "Find the standardized test statistic:   z = (sample statistic − null value) ÷ SE",
           ["z = (0.194 − 0.1875) ÷ 0.0166 ≈ **0.41**"], lines=2)
    d.step("Step 7.", "Find the p-value. Since the test is two-tailed, the p-value is the area beyond z in both tails.",
           ["Area above 0.41 is about 0.342, so p-value = 2 × 0.342 ≈ **0.68**."], lines=1)
    d.step("Step 8.", "Make a decision at α = 0.05. Is the p-value less than 0.05? Reject H₀ or do not reject H₀?",
           ["0.68 > 0.05, so **do not reject H₀**."])
    d.step("Step 9.", "Write a conclusion in context.",
           ["The data do not provide evidence that the proportion of plants with smooth green peas differs from 3/16. "
            "These results are consistent with Mendel's theory."], lines=2)
    d.end("End of worksheet")


def w12b(d: Doc):
    d.directions(["Use a 5% significance level.", "Show the formula with the numbers plugged in on every calculation.",
                  "Find normal-curve areas with StatKey (**Theoretical Distributions → Normal**) or a calculator.", UPLOAD])
    d.problem("Accuracy of Lie Detectors",
              "Participants in a study to evaluate the accuracy of lie detectors were divided into two groups: one group read true material and the other read false material, "
              "while connected to a lie detector. Both groups received electric shocks to add stress. The two-way table shows whether the participants were lying or telling the truth, "
              "and whether the lie detector said they were lying.")
    d.table([["", "Detector says lying", "Detector says not lying", "Total"],
             ["Person lying", "31", "17", "48"],
             ["Person not lying", "27", "21", "48"],
             ["Total", "58", "38", "96"]], widths=[1.7, 1.75, 1.95, 0.8])
    d.subheading("Part (a). Check the conditions for using a normal distribution")
    d.step("Step 1.", "Each group needs at least 10 \"successes\" and 10 \"failures.\" List the counts for the lying group and the truthful group. Are all four counts at least 10?",
           ["Lying group: 31 and 17.   Truthful group: 27 and 21.",
            "**All four counts are at least 10**, so the normal distribution is appropriate."], lines=2)
    d.subheading("Part (b). Find the three sample proportions")
    d.step("Step 2.", "Find the proportion of times the detector says \"lying\" in each group, and overall:   p̂_{L} = 31 ÷ 48,   p̂_{T} = 27 ÷ 48,   pooled p̂ = 58 ÷ 96",
           ["p̂_{L} = **0.646**     p̂_{T} = **0.563**     pooled p̂ = **0.604**"], lines=2)
    d.subheading("Part (c). Test for a difference")
    d.step("Step 3.", "Identify the parameters. In words, p_{L} and p_{T} are…",
           ["p_{L} = the proportion of **all** lying people the detector says are lying; p_{T} = the proportion of **all** truthful people the detector says are lying."], lines=2)
    d.step("Step 4.", "State the hypotheses. Is the test left-tailed, right-tailed, or two-tailed?",
           ["H₀: p_{L} = p_{T}     Hₐ: p_{L} ≠ p_{T}     **Two-tailed**."], lines=2)
    d.step("Step 5.", "Find the sample statistic:   p̂_{L} − p̂_{T} =",
           ["p̂_{L} − p̂_{T} = 0.646 − 0.563 = **0.083**"])
    d.step("Step 6.", "Find the standard error, using the pooled proportion:   SE = √( p̂(1 − p̂)(1/n_{L} + 1/n_{T}) )",
           ["SE = √(0.604 × 0.396 × (1/48 + 1/48)) = **0.0998**"], lines=2)
    d.step("Step 7.", "Find the standardized test statistic:   z = (sample statistic − null value) ÷ SE",
           ["z = (0.083 − 0) ÷ 0.0998 ≈ **0.83**"], lines=1)
    d.step("Step 8.", "Find the p-value. Since the test is two-tailed, the p-value is the area beyond z in both tails.",
           ["Area above 0.83 is about 0.202, so p-value = 2 × 0.202 ≈ **0.40**."], lines=1)
    d.step("Step 9.", "Make a decision at α = 0.05. Reject H₀ or do not reject H₀?",
           ["0.40 > 0.05, so **do not reject H₀**."])
    d.step("Step 10.", "Write a conclusion in context.",
           ["The data do not provide evidence that the lie detector says \"lying\" more (or less) often for people who are lying than for people telling the truth. "
            "In other words, there is no evidence that the detector can tell the difference."], lines=2)
    d.subheading("Part (d). Confidence interval for the difference")
    d.step("Step 11.", "Find a 95% confidence interval for p_{L} − p_{T}. For an interval, use each group's own proportion:   SE = √( p̂_{L}(1 − p̂_{L})/n_{L} + p̂_{T}(1 − p̂_{T})/n_{T} ),   z* = 1.96",
           ["SE = √(0.646 × 0.354/48 + 0.563 × 0.437/48) = 0.0995",
            "0.083 ± 1.96(0.0995) = 0.083 ± 0.195, so **−0.112 to 0.278**."], lines=3)
    d.step("Step 12.", "Does the interval include 0? What does that suggest?",
           ["**Yes, 0 is in the interval**, so \"no difference\" is plausible. This matches our decision not to reject H₀ in Part (c)."], lines=2)
    d.end("End of worksheet")


def w13a(d: Doc):
    d.directions(["Use a 5% significance level unless a problem says otherwise.", "Show the formula with the numbers plugged in on every calculation.",
                  "Find t* and t-distribution areas with StatKey (**Theoretical Distributions → t**) or a calculator.", UPLOAD])
    d.problem("Problem 1. Cell Phone Calls",
              "A survey of 1,917 cell phone users in May 2010 asked, \"On an average day, about how many cell phone calls do you make and receive on your cell phone?\" "
              "The mean number of calls was 13.10, with a standard deviation of about 10.2. Find and interpret a 99% confidence interval for the mean number of cell phone calls for all cell phone users.")
    d.step("Step 1.", "Identify the parameter. In words, μ is…",
           ["μ = the mean number of calls made and received per day by **all** cell phone users."])
    d.step("Step 2.", "Identify the sample statistics:   n = ___     x̄ = ___     s = ___",
           ["n = 1,917     x̄ = 13.10     s = 10.2"])
    d.step("Step 3.", "Check the conditions for using a t-distribution. Is the sample size large enough, or is the data reasonably normal?",
           ["**Yes.** n = 1,917 is far more than 30, so the t-distribution works even if the data are skewed."])
    d.step("Step 4.", "Find the standard error:   SE = s ÷ √n",
           ["SE = 10.2 ÷ √1917 = **0.233**"])
    d.step("Step 5.", "Find t* for 99% confidence. Degrees of freedom = n − 1 =",
           ["df = 1,916, so t* ≈ **2.578**."])
    d.step("Step 6.", "Find the margin of error:   Margin of error = t* · SE",
           ["2.578 × 0.233 = **0.60**"])
    d.step("Step 7.", "Build the confidence interval:   x̄ ± margin of error",
           ["13.10 ± 0.60, so **12.50 to 13.70 calls**."])
    d.step("Step 8.", "Interpret the interval in context.",
           ["We are 99% sure that the mean number of cell phone calls made and received per day by all cell phone users is between 12.50 and 13.70."], lines=2)

    d.problem("Problem 2. Penalty Minutes in Hockey Games",
              "In the 2010–11 NHL regular season, the number of penalty minutes per game for each of the 30 teams ranged from 8.8 (Florida Panthers) to 18.0 (New York Islanders). "
              "The mean for all 30 teams is 12.20 penalty minutes per game with a standard deviation of 2.25. Assume this is a sample of all teams in all seasons, and test whether "
              "it provides evidence that the mean number of penalty minutes per game for a hockey team is less than 13. Show all details of the test.")
    d.step("Step 1.", "Identify the parameter. In words, μ is…",
           ["μ = the mean number of penalty minutes per game for **all** NHL teams in all seasons."])
    d.step("Step 2.", "State the hypotheses. Is the test left-tailed, right-tailed, or two-tailed?",
           ["H₀: μ = 13     Hₐ: μ < 13     **Left-tailed**."], lines=2)
    d.step("Step 3.", "Identify the sample statistics:   n = ___     x̄ = ___     s = ___",
           ["n = 30     x̄ = 12.20     s = 2.25"])
    d.step("Step 4.", "Check the conditions for using a t-distribution.",
           ["**Yes.** n = 30, and the values (8.8 to 18.0) show no extreme outliers."])
    d.step("Step 5.", "Find the standard error:   SE = s ÷ √n",
           ["SE = 2.25 ÷ √30 = **0.411**"])
    d.step("Step 6.", "Find the standardized test statistic:   t = (sample statistic − null value) ÷ SE",
           ["t = (12.20 − 13) ÷ 0.411 ≈ **−1.95**"])
    d.step("Step 7.", "Find the p-value. Degrees of freedom = n − 1. Since the test is left-tailed, the p-value is the area below t.",
           ["df = 29. Area below −1.95 ≈ **0.031**."])
    d.step("Step 8.", "Make a decision at α = 0.05.",
           ["0.031 < 0.05, so **reject H₀**."])
    d.step("Step 9.", "Write a conclusion in context.",
           ["There is evidence that the mean number of penalty minutes per game for hockey teams is less than 13."], lines=2)
    d.end("End of worksheet")


def w13b(d: Doc):
    d.directions(["Use a 5% significance level unless a problem says otherwise.", "Show the formula with the numbers plugged in on every calculation.",
                  "For degrees of freedom, use the smaller sample size minus 1. Find t* and t-areas with StatKey or a calculator.", UPLOAD])
    d.problem("Problem 1. Music While Studying",
              "Does listening to music with lyrics affect how well students learn from a reading? An instructor randomly assigned 47 student volunteers to study a short reading passage "
              "either in silence or while listening to music with lyrics, and then gave everyone the same quiz, scored out of 50 points. The 25 students who studied in silence had a mean "
              "score of 38.4 with a standard deviation of 6.2. The 22 students who studied with music had a mean score of 34.9 with a standard deviation of 7.5. Neither group's scores showed "
              "strong skewness or outliers. Find and interpret a 95% confidence interval for the difference in mean quiz score, silence minus music.")
    d.step("Step 1.", "Identify the parameter. In words, μ_{S} − μ_{M} is…",
           ["The difference in mean quiz score between **all** students who study in silence and all students who study with music with lyrics."], lines=2)
    d.step("Step 2.", "Fill in the sample statistics in the table below.", None, lines=0)
    d.table([["Group", "n", "x̄", "s"],
             ["Silence (S)", ("ans", "25"), ("ans", "38.4"), ("ans", "6.2")],
             ["Music (M)", ("ans", "22"), ("ans", "34.9"), ("ans", "7.5")]], widths=[1.6, 1.1, 1.1, 1.1])
    d.step("Step 3.", "Both samples are under 30. Is it still OK to use a t-distribution? Why?",
           ["**Yes.** Neither group shows strong skewness or outliers, so the t-distribution works even with small samples."], lines=2)
    d.step("Step 4.", "Find the sample statistic:   x̄_{S} − x̄_{M} =",
           ["38.4 − 34.9 = **3.5 points**"])
    d.step("Step 5.", "Find the standard error:   SE = √( s_{S}²/n_{S} + s_{M}²/n_{M} )",
           ["SE = √(6.2²/25 + 7.5²/22) = √(1.538 + 2.557) = **2.023**"], lines=2)
    d.step("Step 6.", "Find t* for 95% confidence. Degrees of freedom = smaller sample size − 1 =",
           ["df = 22 − 1 = 21, so t* = **2.080**."])
    d.step("Step 7.", "Find the margin of error:   t* · SE",
           ["2.080 × 2.023 = **4.21**"])
    d.step("Step 8.", "Build the confidence interval:   (x̄_{S} − x̄_{M}) ± margin of error",
           ["3.5 ± 4.21, so **−0.71 to 7.71 points**."])
    d.step("Step 9.", "Interpret the interval in context.",
           ["We are 95% sure that the mean quiz score for students who study in silence is between 0.71 points lower and 7.71 points higher than for students who study with music with lyrics."], lines=2)
    d.step("Step 10.", "Does the interval include 0? What does that suggest?",
           ["**Yes.** \"No difference\" is plausible, so we don't have evidence that music with lyrics changes the mean quiz score (at the 5% level)."], lines=2)

    d.problem("Problem 2 (Extra Credit, up to 5 points). Smiles and Leniency",
              "Does smiling after a mistake make people more forgiving? In a study, 68 participants were shown a photo of a college student accused of academic misconduct and asked to rate "
              "how lenient the punishment should be (higher scores mean more lenient). Participants were randomly assigned to see either a photo of the student smiling or a photo with a neutral "
              "expression. The 34 participants who saw the smiling photo gave a mean leniency score of 4.91 (s = 1.68). The 34 who saw the neutral photo gave a mean of 4.12 (s = 1.52). "
              "Test, using a 5% significance level, whether there is evidence that smiling leads to more leniency.")
    d.step("Step 1.", "Identify the parameters. In words, μ_{S} and μ_{N} are…",
           ["The mean leniency scores **all** people would give after seeing the smiling photo (μ_{S}) and the neutral photo (μ_{N})."], lines=2)
    d.step("Step 2.", "State the hypotheses. Is the test left-tailed, right-tailed, or two-tailed?",
           ["H₀: μ_{S} = μ_{N}     Hₐ: μ_{S} > μ_{N}     **Right-tailed**."], lines=2)
    d.step("Step 3.", "Fill in the sample statistics in the table below.", None, lines=0)
    d.table([["Group", "n", "x̄", "s"],
             ["Smiling (S)", ("ans", "34"), ("ans", "4.91"), ("ans", "1.68")],
             ["Neutral (N)", ("ans", "34"), ("ans", "4.12"), ("ans", "1.52")]], widths=[1.6, 1.1, 1.1, 1.1])
    d.step("Step 4.", "Check the conditions for using a t-distribution. Are both samples large enough?",
           ["**Yes.** Both samples have 34 ≥ 30."])
    d.step("Step 5.", "Find the sample statistic:   x̄_{S} − x̄_{N} =",
           ["4.91 − 4.12 = **0.79**"])
    d.step("Step 6.", "Find the standard error:   SE = √( s_{S}²/n_{S} + s_{N}²/n_{N} )",
           ["SE = √(1.68²/34 + 1.52²/34) = √(0.0830 + 0.0680) = **0.389**"], lines=2)
    d.step("Step 7.", "Find the standardized test statistic:   t = (sample statistic − null value) ÷ SE",
           ["t = (0.79 − 0) ÷ 0.389 ≈ **2.03**"])
    d.step("Step 8.", "Find the p-value. Degrees of freedom = smaller sample size − 1. Since the test is right-tailed, the p-value is the area above t.",
           ["df = 33. Area above 2.03 ≈ **0.025**."])
    d.step("Step 9.", "Make a decision at α = 0.05.",
           ["0.025 < 0.05, so **reject H₀**."])
    d.step("Step 10.", "Write a conclusion in context.",
           ["There is evidence that people give more lenient punishments, on average, when the accused student is smiling."], lines=2)
    d.step("Step 11.", "Can we conclude that smiling **causes** more leniency? Why or why not?",
           ["**Yes.** Participants were **randomly assigned** to the photos, so this is a randomized experiment and we can conclude causation."], lines=2)
    d.end("End of worksheet")


def w14a(d: Doc):
    d.directions(["Use a 5% significance level.", "Show the formula with the numbers plugged in on every calculation.",
                  "Find t* and t-areas with StatKey (**Theoretical Distributions → t**) or a calculator.", UPLOAD])
    d.problem("CAOS Exam Scores",
              "The CAOS (Comprehensive Assessment of Outcomes in Statistics) exam is an online multiple-choice test on concepts covered in a typical introductory statistics course. "
              "Students take one version before the course starts and another version after the course ends. The Before and After scores for a random sample of 10 students are shown, "
              "along with each student's difference (After − Before).")
    d.table([["Student", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
             ["Before", "43", "40", "48", "65", "60", "48", "43", "38", "43", "55"],
             ["After", "60", "45", "55", "80", "85", "71", "52", "35", "54", "55"],
             ["Difference", "17", "5", "7", "15", "25", "23", "9", "−3", "11", "0"]],
            widths=[1.1] + [0.55] * 10)
    d.para("The 10 differences have a mean of x̄_{d} = 10.9 points and a standard deviation of s_{d} = 9.219 points. The differences show no strong skewness or outliers.")

    d.problem("Problem 1. Why Paired Data?")
    d.step("", "We want to know whether taking the course increases students' understanding, as measured by this exam. Why should we use a paired design instead of two separate groups?",
           ["The **same students** are measured twice, so each Before score is naturally matched with an After score. Looking at each student's difference removes "
            "the big student-to-student differences in background and ability, which makes the improvement easier to detect."], lines=3, indent=0)

    d.problem("Problem 2. Hypothesis Test",
              "Test, using a 5% significance level, whether scores at the end of the course are higher, on average, than scores at the beginning.")
    d.step("Step 1.", "Identify the parameter. In words, μ_{d} is…",
           ["μ_{d} = the mean difference in CAOS score (After − Before) for **all** students who take the course."], lines=2)
    d.step("Step 2.", "State the hypotheses. Is the test left-tailed, right-tailed, or two-tailed?",
           ["H₀: μ_{d} = 0     Hₐ: μ_{d} > 0     **Right-tailed**."], lines=2)
    d.step("Step 3.", "Identify the sample statistics for the differences:   n_{d} = ___     x̄_{d} = ___     s_{d} = ___",
           ["n_{d} = 10     x̄_{d} = 10.9     s_{d} = 9.219"])
    d.step("Step 4.", "There are only 10 differences. Is it still OK to use a t-distribution? Why?",
           ["**Yes.** The differences show no strong skewness or outliers."], lines=2)
    d.step("Step 5.", "Find the standard error:   SE = s_{d} ÷ √n_{d}",
           ["SE = 9.219 ÷ √10 = **2.915**"])
    d.step("Step 6.", "Find the standardized test statistic:   t = (x̄_{d} − 0) ÷ SE",
           ["t = 10.9 ÷ 2.915 ≈ **3.74**"])
    d.step("Step 7.", "Find the p-value. Degrees of freedom = n_{d} − 1. Since the test is right-tailed, the p-value is the area above t.",
           ["df = 9. Area above 3.74 ≈ **0.002**."])
    d.step("Step 8.", "Make a decision at α = 0.05.",
           ["0.002 < 0.05, so **reject H₀**."])
    d.step("Step 9.", "Write a conclusion in context.",
           ["There is strong evidence that students' mean CAOS score is higher at the end of the course than at the beginning."], lines=2)

    d.problem("Problem 3. Confidence Interval",
              "Find and interpret a 95% confidence interval for the mean improvement in CAOS score from Before to After.")
    d.step("Step 1.", "Find t* for 95% confidence. Degrees of freedom = n_{d} − 1 =",
           ["df = 9, so t* = **2.262**."])
    d.step("Step 2.", "Find the margin of error, using the standard error from Problem 2:   t* · SE",
           ["2.262 × 2.915 = **6.59**"])
    d.step("Step 3.", "Build the confidence interval:   x̄_{d} ± margin of error",
           ["10.9 ± 6.59, so **4.31 to 17.49 points**."])
    d.step("Step 4.", "Interpret the interval in context.",
           ["We are 95% sure that the mean improvement in CAOS score (After − Before) for all students who take the course is between 4.31 and 17.49 points."], lines=2)
    d.step("Step 5.", "Does the interval include 0? How does that fit with your conclusion in Problem 2?",
           ["**No.** Every value in the interval is positive, so an improvement of 0 isn't plausible. That agrees with rejecting H₀ in Problem 2."], lines=2)
    d.end("End of worksheet")


def w14b(d: Doc):
    d.directions(["Use a 5% significance level.", "Round expected counts to two decimals and contributions to three decimals.",
                  "Find the p-value with StatKey (**Theoretical Distributions → Chi-Square**) or a calculator.", UPLOAD])
    d.problem("Study Method and Passing the Exam",
              "A statistics instructor asked 300 students how they mainly studied for the first exam and recorded whether each student passed. (The data are made up for practice.) "
              "Is there an association between study method and passing the exam?")
    d.table([["Observed", "Passed", "Did not pass", "Total"],
             ["Flashcards", "48", "22", "70"],
             ["Practice problems", "96", "24", "120"],
             ["Rereading notes", "62", "48", "110"],
             ["Total", "206", "94", "300"]], widths=[1.9, 1.3, 1.3, 1.1])
    d.step("(a)", "State the null and alternative hypotheses.",
           ["H₀: Study method and passing the exam are **not associated**.",
            "Hₐ: Study method and passing the exam **are associated**."], lines=2)
    d.step("(b)", "What is the expected count for the cell **Practice problems / Did not pass**? Show the formula with the numbers plugged in.",
           ["Expected = (row total × column total) ÷ grand total = (120 × 94) ÷ 300 = **37.6**"], lines=2)
    d.step("(c)", "Find all six expected counts and write them in the table. Are all the expected counts at least 5?", None, lines=0)
    d.table([["Expected", "Passed", "Did not pass", "Total"],
             ["Flashcards", ("ans", "48.07"), ("ans", "21.93"), "70"],
             ["Practice problems", ("ans", "82.40"), ("ans", "37.60"), "120"],
             ["Rereading notes", ("ans", "75.53"), ("ans", "34.47"), "110"],
             ["Total", "206", "94", "300"]], widths=[1.9, 1.3, 1.3, 1.1])
    d.answer(["**Yes**, all six expected counts are at least 5, so the chi-squared test is appropriate."])
    if not d.key:
        d.lines(1)
    d.step("(d)", "What is the contribution to the chi-squared statistic for the cell **Practice problems / Did not pass**?",
           ["(observed − expected)² ÷ expected = (24 − 37.6)² ÷ 37.6 = 184.96 ÷ 37.6 = **4.919**"], lines=2)
    d.step("(e)", "Find all six contributions and write them in the table.", None, lines=0)
    d.table([["Contribution", "Passed", "Did not pass"],
             ["Flashcards", ("ans", "0.000"), ("ans", "0.000")],
             ["Practice problems", ("ans", "2.245"), ("ans", "4.919")],
             ["Rereading notes", ("ans", "2.425"), ("ans", "5.314")]], widths=[1.9, 1.5, 1.5])
    d.step("(f)", "What is the value of the chi-squared test statistic?",
           ["χ² = 0.000 + 0.000 + 2.245 + 4.919 + 2.425 + 5.314 = **14.90**"])
    d.step("(g)", "What are the degrees of freedom? What is the p-value?",
           ["df = (rows − 1)(columns − 1) = (3 − 1)(2 − 1) = **2**.",
            "p-value = area to the right of 14.90 in a χ² distribution with df = 2 ≈ **0.0006**."], lines=2)
    d.step("(h)", "Using α = 0.05, what is your decision and conclusion in context? If there is an association, describe how the two variables are related.",
           ["0.0006 < 0.05, so **reject H₀**. There is evidence of an association between study method and passing the exam.",
            "Students who did practice problems passed more often than expected (96 observed vs. 82.4 expected), students who reread their notes passed less often than expected "
            "(62 vs. 75.5), and flashcard users were right at what we'd expect."], lines=3)
    d.step("(i)", "Can we conclude that doing practice problems **causes** students to pass? Explain.",
           ["**No.** This is an observational study: students chose their own study method. Confounding variables, such as motivation or how much time a student studied, "
            "could explain the association."], lines=2)
    d.end("End of worksheet")


def w15a(d: Doc):
    d.directions(["Use a 5% significance level.", "Show the formula with the numbers plugged in on every calculation.",
                  "Find the p-value with StatKey (**Theoretical Distributions → F**) or a calculator.", UPLOAD])
    d.problem("Fiber in Breakfast Cereals",
              "The dataset **Cereal** gives the number of grams of fiber per serving for 30 breakfast cereals made by three companies. "
              "The summary statistics are shown below. Is there a difference in the mean grams of fiber per serving between the three companies? "
              "Conduct an analysis of variance (ANOVA) test, showing all details.")
    d.table([["Company", "Mean", "Std. Dev.", "Sample Size"],
             ["General Mills", "1.469", "1.248", "13"],
             ["Kellogg's", "1.764", "2.349", "11"],
             ["Quaker", "2.567", "2.174", "6"],
             ["Total", "1.797", "1.880", "30"]], widths=[1.7, 1.1, 1.1, 1.2],
            caption="Grams of fiber per serving by company: mean, standard deviation and sample size for General Mills, Kellogg's, Quaker, and all 30 cereals.")
    d.step("Step 1.", "Identify the parameters. In words, μ₁, μ₂ and μ₃ are…",
           ["μ₁, μ₂, μ₃ = the mean grams of fiber per serving for **all** General Mills, Kellogg's and Quaker cereals."], lines=2)
    d.step("Step 2.", "State the null and alternative hypotheses.",
           ["H₀: μ₁ = μ₂ = μ₃     Hₐ: at least one μᵢ is different from the others."], lines=2)
    d.step("Step 3.", "Check the conditions. Is the largest standard deviation less than twice the smallest? What else should we be careful about?",
           ["2.349 ÷ 1.248 ≈ **1.88 < 2**, so the equal-variability condition is OK.",
            "The samples are small (only 6 Quaker cereals), so we also need the data in each group to be without strong skewness or outliers. We proceed with some caution."], lines=2)
    d.step("Step 4.", "Find the variability **between** groups:   SSG = Σ nᵢ(x̄ᵢ − x̄)², using the overall mean x̄ = 1.797",
           ["SSG = 13(1.469 − 1.797)² + 11(1.764 − 1.797)² + 6(2.567 − 1.797)²",
            "= 1.399 + 0.012 + 3.557 = **4.968**"], lines=3)
    d.step("Step 5.", "Find the variability **within** groups:   SSE = Σ (nᵢ − 1)sᵢ²",
           ["SSE = 12(1.248)² + 10(2.349)² + 5(2.174)²",
            "= 18.690 + 55.178 + 23.631 = **97.499**"], lines=3)
    d.step("Step 6.", "Complete the ANOVA table. (df: groups k − 1, error n − k, total n − 1.   MS = SS ÷ df.   F = MSG ÷ MSE.)", None, lines=0)
    d.table([["Source", "df", "SS", "MS", "F"],
             ["Groups", ("ans", "2"), ("ans", "4.968"), ("ans", "2.484"), ("ans", "0.688")],
             ["Error", ("ans", "27"), ("ans", "97.499"), ("ans", "3.611"), ""],
             ["Total", ("ans", "29"), ("ans", "102.467"), "", ""]], widths=[1.2, 0.8, 1.1, 1.0, 1.0])
    d.step("Step 7.", "Find the p-value: the area to the right of F in an F-distribution with df = 2 and 27.",
           ["p-value = area above 0.688 in F(2, 27) ≈ **0.51**."])
    d.step("Step 8.", "Make a decision at α = 0.05.",
           ["0.51 > 0.05, so **do not reject H₀**."])
    d.step("Step 9.", "Write a conclusion in context.",
           ["The data do not provide evidence of a difference in the mean grams of fiber per serving between General Mills, Kellogg's and Quaker cereals. "
            "The differences between the sample means are small compared with the variability within each company."], lines=2)
    d.end("End of worksheet")


def w15b(d: Doc):
    d.directions(["Use a 5% significance level.", "Show the formula with the numbers plugged in on every calculation.",
                  "Find t* with StatKey (**Theoretical Distributions → t**) or a calculator.", UPLOAD])
    d.problem("Alcohol and Missed Classes",
              "The dataset **SleepStudy** includes **Drinks**, the number of alcoholic drinks a week that each of 253 college students says they have, and **ClassesMissed**, "
              "the number of classes each student missed during the semester. Computer output for the correlation between these two variables and the regression line "
              "to predict classes missed from the number of drinks is shown below.")
    d.para("Pearson correlation of Drinks and ClassesMissed = 0.078     P-Value = 0.215", keep=True)
    d.para("The regression equation is   ClassesMissed = 1.86 + 0.0620 Drinks", keep=True)
    d.table([["Predictor", "Coef", "SE Coef", "T", "P"],
             ["Constant", "1.8644", "0.3439", "5.42", "0.000"],
             ["Drinks", "0.06196", "0.04979", "1.24", "0.215"]], widths=[1.3, 1.0, 1.0, 0.8, 0.8],
            caption="Regression output for predicting ClassesMissed from Drinks: coefficient, standard error, t statistic and p-value for the constant and for Drinks.")
    d.para("S = 3.23679     R-Sq = 0.6%     R-Sq(adj) = 0.2%")
    d.step("(a)", "What is the sample correlation? What is the p-value for testing the correlation? Give the conclusion of the test in context.",
           ["r = **0.078**, p-value = **0.215**.",
            "0.215 > 0.05, so **do not reject H₀: ρ = 0**. There is no evidence of a linear relationship between drinks per week and classes missed for all college students."], lines=3)
    d.step("(b)", "What is the regression line? Find the predicted value and the residual for a student who has 6 alcoholic drinks a week and has missed 2 classes.",
           ["Predicted ClassesMissed = 1.8644 + 0.06196 · Drinks",
            "Predicted: 1.8644 + 0.06196(6) = **2.236 classes**.     Residual = observed − predicted = 2 − 2.236 = **−0.236**."], lines=3)
    d.step("(c)", "Interpret the slope of the line in context.",
           ["Each additional alcoholic drink per week goes with about **0.062 more classes missed**, on average."], lines=2)
    d.step("(d)", "What is the p-value for a test of the slope? Give the conclusion of the test in context.",
           ["p-value = **0.215** for H₀: β₁ = 0 vs Hₐ: β₁ ≠ 0. 0.215 > 0.05, so **do not reject H₀**.",
            "The number of drinks is not an effective predictor of classes missed: there is no evidence that the population slope differs from 0."], lines=3)
    d.step("(e)", "What is the standard error of the slope? Find and interpret a 95% confidence interval for the slope. (df = n − 2 = 251, so t* ≈ 1.969.)",
           ["SE = **0.04979**.",
            "0.06196 ± 1.969(0.04979) = 0.06196 ± 0.098, so **−0.036 to 0.160**.",
            "We are 95% sure that each extra drink per week changes the mean number of classes missed by somewhere between 0.036 fewer and 0.160 more. "
            "The interval contains 0, which matches not rejecting H₀ in (d)."], lines=4)
    d.step("(f)", "Compare the two p-values, from the test for correlation and the test for slope.",
           ["They are **the same (0.215)**. Testing whether the correlation is 0 and testing whether the slope is 0 are equivalent tests."], lines=2)
    d.step("(g)", "What is the value of R² for this model? Interpret it in context.",
           ["R² = **0.6%**. Only 0.6% of the variability in the number of classes missed is explained by the number of alcoholic drinks a week."], lines=2)
    d.end("End of worksheet")


# (file stem, activity title for the header, week · section subtitle, builder)
WORKSHEETS = [
    ("W08_CI_Using_Percentiles", "Confidence Intervals Using Percentiles", "Week 8  ·  Section 3.4  ·  Participation activity", w08),
    ("W10_Determining_Statistical_Significance", "Determining Statistical Significance", "Week 10  ·  Section 4.3  ·  Participation activity", w10),
    ("W12_Proportion_Test_and_CI", "Hypothesis Tests and Confidence Intervals for a Proportion", "Week 12  ·  Section 6.1  ·  Participation activity", w12a),
    ("W12_Difference_in_Proportions", "Hypothesis Tests and CI for a Difference in Proportions", "Week 12  ·  Section 6.3  ·  Participation activity", w12b),
    ("W13_Inference_for_a_Mean", "Inference for a Mean", "Week 13  ·  Section 6.2  ·  Participation activity", w13a),
    ("W13_Difference_in_Means", "Inference for a Difference in Means", "Week 13  ·  Section 6.4  ·  Participation activity", w13b),
    ("W14_Paired_Difference_in_Means", "Inference on Paired Difference in Means", "Week 14  ·  Section 6.5  ·  Participation activity", w14a),
    ("W14_Association_Two_Categorical", "Testing for an Association Between Two Categorical Variables", "Week 14  ·  Section 7.2  ·  Participation activity", w14b),
    ("W15_Analysis_of_Variance", "Analysis of Variance", "Week 15  ·  Section 8.1  ·  Participation activity", w15a),
    ("W15_Inference_for_Slope_and_Correlation", "Inference for Slope and Correlation", "Week 15  ·  Section 9.1  ·  Participation activity", w15b),
]
