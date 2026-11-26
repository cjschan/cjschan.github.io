"""Alt text for every image in the handouts (screen-reader descriptions).

Each description gives what a sighted student reads off the figure (axis, scale, key values),
without giving away answers that require reasoning.
"""
ALT = {
    # Practice Test 1
    "pt1/image1.png": "Boxplot of daily water intake in cups, on an axis from 0 to 22. The left whisker starts at 3, the box runs from 6 to 10 with the median at 8, the right whisker ends at 14, and one outlier dot is at 20.",
    "pt1/image2.png": "Side-by-side vertical boxplots of test scores (axis 40 to 100). Lecture: whiskers from 50 to 95, box from 60 to 82, median 70. Hands-on: whiskers from 68 to 96, box from 76 to 88, median 84, and one outlier dot at about 55.",
    "pt1/image3.png": "Scatterplot of resting heart rate in beats per minute (vertical axis, 50 to 90) against hours of exercise per week (horizontal axis, 0 to 8), about 30 points. The points trend downward: more exercise goes with lower heart rate, with moderate scatter. Notable points include about (1, 64), (2.5, 89) and (7.4, 54).",
    "pt1/image4.png": "Scatterplot of typing speed in words per minute (vertical axis, 25 to 90) against weeks of practice (horizontal axis, 0 to 13) for 12 students, with the regression line Speed = 30 + 4·Weeks drawn through the points. The point (5, 56) is circled and labeled; it lies above the line.",
    # Practice Test 2
    "pt2/image1.png": "Dotplot titled 'Sampling distribution: means from 800 samples of size n = 40'. Horizontal axis: sample mean weekly grocery spending in dollars, 100 to 140. The dots form a roughly symmetric mound centered near 120; almost all dots fall between about 107 and 133, with a few as low as 102 and as high as 138.",
    "pt2/image2.png": "Dotplot titled 'Bootstrap distribution: 900 bootstrap sample proportions'. Horizontal axis: bootstrap sample proportion, 0.34 to 0.54. The dots form a symmetric mound centered at about 0.44; most dots fall between about 0.39 and 0.49, ranging from 0.37 to 0.51.",
    "pt2/image3.png": "Dotplot titled 'Randomization distribution: 1000 simulated statistics when H0 is true'. Horizontal axis: randomization difference in means, −7 to 7. The dots form a mound centered at 0, mostly between −4 and 4. A vertical red line marks the sample statistic at 3.6; a small number of dots lie at or beyond it on the right.",
    "pt2/image4.png": "Two unlabeled dotplots side by side, each with horizontal axis 'Simulated mean' from 31 to 45. Distribution A is a mound centered at about 35, spanning roughly 32 to 38. Distribution B is a mound centered at about 40, spanning roughly 36 to 44.",
    # Practice Test 3
    "pt3/image1.png": "Standard normal curve on an axis from −3 to 3, with a vertical line at z = 2.20 and the small area to the right of 2.20 shaded.",
    "pt3/image2.png": "Two bell-shaped curves on an axis from −3 to 3: a standard normal curve (gray) and a t-distribution with df = 4 (dark blue). The t-curve has a lower peak and thicker tails than the normal curve.",
    # Study guides
    "sg1/image1.png": "Labeled boxplot diagram on an axis from 0 to 110. The box runs from Q1 = 35 to Q3 = 55 with the median at 45; the double arrow under the box is labeled IQR = Q3 − Q1. Dashed lines mark the lower fence Q1 − 1.5×IQR at 5 and the upper fence Q3 + 1.5×IQR at 85. The whiskers end at the smallest value that is not an outlier (about 22) and the largest value that is not an outlier (about 72). A dot at 95, beyond the upper fence, is labeled 'Outlier (here it is the maximum)'.",
    "sg2/image1.png": "Three stacked dotplots on a shared axis of simulated statistics from 40 to 56, each with a dashed line at its center. Top: sampling distribution, centered at the population parameter (mu or p), at 48. Middle: bootstrap distribution, centered at the sample statistic (x-bar or p-hat), at 52. Bottom: randomization distribution, centered at the null hypothesis value, at 45.",
    "sg3/image1.png": "Two bell curves on a standardized-value axis from −3 to 3: the normal (z) curve, labeled 'known/large', and a t-distribution with df = 4, labeled 'heavier tails'. The t-curve is lower in the middle and higher in the tails.",
    "sg3/image2.png": "Decision chart titled 'What are you measuring?'. Count or yes-no: a categorical variable, a proportion. One sample: single proportion (z). Two samples: difference in proportions (z). Average: a quantitative variable, a mean. One sample: single mean (t). Two separate groups: difference in means (t). Same subjects measured twice: paired (t). A box at the bottom says: every test, z or t = (statistic − null value) ÷ SE; every interval, statistic ± (z* or t*) × SE; proportions use the normal (z), means use the t-distribution with df from the sample size; check conditions first: proportions need at least 10 in each relevant count, means need rough symmetry with no strong outliers.",
    # Final exam study guide (drawn in final_guide.py)
    "final/p2_boxplot.png": "Horizontal boxplot of hours of sleep on a school night, on an axis from 3 to 10. The left whisker starts at 4, the box runs from 6 to 7.5 with the median at 7, and the right whisker ends at 9.",
    "final/p3_regression.png": "Scatterplot of time to mow in minutes (vertical axis, 0 to 90) against lawn size in thousands of square feet (horizontal axis, 0 to 9) for 12 lawns, with the regression line Predicted Time = 12 + 8·Size. The points rise steadily and lie close to the line.",
    "final/p4_sampling.png": "Dotplot of 500 sample proportions of coupon users, each from a sample of n = 150 shoppers, on an axis from 0.22 to 0.48. The dots form a symmetric mound centered at about 0.35, with nearly all dots between about 0.27 and 0.43.",
    "final/p6_randomization.png": "Dotplot of 50 simulated sample mean scores assuming mu = 70, on an axis from 64 to 76. The dots form a mound centered at 70. A dashed red line marks the sample mean x-bar = 74; the dots at or beyond 74 are colored red.",
}
