"""Final Exam Study Guide + Solutions (Spring 2027 Math 1342).

Practice Problems 1-13 mirror the 13 Final Exam questions one-to-one (new scenarios and
numbers); Problem 14 adds ANOVA (8.1). Every number in the solutions is computed here,
and the four figures are drawn here with matplotlib (needs matplotlib + scipy).

    called from build_docs.py
"""
from pathlib import Path

import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from wslib import Doc, keep_next  # noqa: E402


def keep_table(t):
    """Keep a table on one page (keep-with-next on every row but the last)."""
    for row in t.rows[:-1]:
        for c in row.cells:
            for p in c.paragraphs:
                keep_next(p)

HERE = Path(__file__).resolve().parent
FIG = HERE / "media" / "final"
FLOWCHART = HERE / "media" / "sg3" / "media" / "image2.png"   # Test 3 guide's decision chart

NAVY, LIGHT, ORANGE, RED = "#1f4e79", "#cfe0f0", "#a86b1d", "#c0392b"


def r2(x):
    return f"{x:.2f}"


def r3(x):
    return f"{x:.3f}"


def r4(x):
    return f"{x:.4f}"


def pv(p):
    """p-value text: 4 decimals, or '< 0.0001'."""
    return "less than 0.0001" if p < 0.0001 else f"{p:.4f}"


def _style(ax):
    ax.grid(axis="y", color="#dddddd", lw=0.8)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_color("#444444")


def dotplot(ax, values, step, color=NAVY, highlight=None):
    """Stacked dotplot. highlight(value) -> True colors that dot red."""
    vals = np.round(np.asarray(values) / step) * step
    counts = {}
    for v in sorted(vals):
        counts[v] = counts.get(v, 0) + 1
        c = RED if (highlight and highlight(v)) else color
        ax.plot(v, counts[v], "o", ms=5.2, mfc=c, mec=c)
    ax.set_yticks([])
    ax.spines[["left", "right", "top"]].set_visible(False)
    return counts


# ---------------------------------------------------------------- the 14 problems' data
class Data:
    def __init__(self):
        # P2 boxplot: hours of sleep, five-number summary
        self.box = dict(mn=4.0, q1=6.0, med=7.0, q3=7.5, mx=9.0)

        # P3 regression: lawn size (1,000 sq ft) -> mowing time (min); line 12 + 8x
        self.reg_b0, self.reg_b1 = 12, 8
        rng = np.random.default_rng(3)
        x = np.array([1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5.5, 6, 6.5, 7, 8])
        self.reg_x, self.reg_y = x, self.reg_b0 + self.reg_b1 * x + rng.normal(0, 4, x.size)
        self.reg_x0, self.reg_actual = 5, 47
        self.reg_pred = self.reg_b0 + self.reg_b1 * self.reg_x0
        self.reg_resid = self.reg_actual - self.reg_pred

        # P4 sampling distribution: 500 samples of n=150, true p = 0.35
        rng = np.random.default_rng(42)
        self.sd_n, self.sd_p, self.sd_reps = 150, 0.35, 500
        self.sd_props = rng.binomial(self.sd_n, self.sd_p, self.sd_reps) / self.sd_n
        self.sd_center = self.sd_props.mean()
        self.sd_se = self.sd_props.std(ddof=1)
        self.sd_check = 0.45
        self.sd_z = (self.sd_check - self.sd_center) / self.sd_se

        # P5 CI from SE
        self.ci_phat, self.ci_se = 0.62, 0.025

        # P6 randomization: 50 simulated sample means assuming mu = 70; observed 74
        self.rz_null, self.rz_obs, self.rz_k = 70, 74, 50
        for seed in range(500):
            m = np.round(np.random.default_rng(seed).normal(70, 1.9, self.rz_k) * 2) / 2
            if (m >= self.rz_obs).sum() == 2 and abs(m.mean() - 70) < 0.25:
                self.rz_means, self.rz_seed = m, seed
                break
        self.rz_count = int((self.rz_means >= self.rz_obs).sum())
        self.rz_p = self.rz_count / self.rz_k

        # P7 one-proportion z
        self.p7 = dict(n=500, x=145, p0=0.25)
        n, x, p0 = self.p7["n"], self.p7["x"], self.p7["p0"]
        self.p7["phat"] = x / n
        self.p7["se"] = np.sqrt(p0 * (1 - p0) / n)
        self.p7["z"] = (self.p7["phat"] - p0) / self.p7["se"]
        self.p7["p"] = 2 * stats.norm.sf(abs(self.p7["z"]))

        # P8 t-interval
        self.p8 = dict(n=20, xbar=32, s=8)
        self.p8["df"] = self.p8["n"] - 1
        self.p8["tstar"] = stats.t.ppf(0.975, self.p8["df"])
        self.p8["se"] = self.p8["s"] / np.sqrt(self.p8["n"])
        self.p8["me"] = self.p8["tstar"] * self.p8["se"]

        # P9 difference in means (right-tailed)
        self.p9 = dict(n1=36, x1=8.2, s1=3.5, n2=30, x2=6.4, s2=3.0)
        q = self.p9
        q["diff"] = q["x1"] - q["x2"]
        q["se"] = np.sqrt(q["s1"] ** 2 / q["n1"] + q["s2"] ** 2 / q["n2"])
        q["t"] = q["diff"] / q["se"]
        q["df"] = min(q["n1"], q["n2"]) - 1
        q["p"] = stats.t.sf(q["t"], q["df"])

        # P10 paired (left-tailed: heart rate decreases)
        self.p10_before = np.array([78, 82, 70, 75, 68, 80, 73, 85])
        self.p10_d = np.array([-4, -6, -1, -3, 0, -5, -2, -7])
        self.p10_after = self.p10_before + self.p10_d
        d = self.p10_d
        self.p10 = dict(n=d.size, dbar=d.mean(), sd=d.std(ddof=1))
        q = self.p10
        q["se"] = q["sd"] / np.sqrt(q["n"])
        q["t"] = q["dbar"] / q["se"]
        q["df"] = q["n"] - 1
        q["p"] = stats.t.cdf(q["t"], q["df"])

        # P12 chi-square: grade level x preferred study time
        self.p12_obs = np.array([[20, 30, 50], [35, 30, 35]])
        chi2, p, df, exp = stats.chi2_contingency(self.p12_obs, correction=False)
        self.p12 = dict(chi2=chi2, p=p, df=df, exp=exp,
                        contrib=(self.p12_obs - exp) ** 2 / exp)

        # P13 inference for slope
        self.p13 = dict(n=30, b1=4.2, se=1.5)
        q = self.p13
        q["df"] = q["n"] - 2
        q["t"] = q["b1"] / q["se"]
        q["p"] = 2 * stats.t.sf(abs(q["t"]), q["df"])
        q["tstar"] = stats.t.ppf(0.975, q["df"])

        # P14 ANOVA
        self.p14 = dict(k=3, n=30, ssg=120.0, sse=540.0)
        q = self.p14
        q["dfg"], q["dfe"] = q["k"] - 1, q["n"] - q["k"]
        q["sst"], q["dft"] = q["ssg"] + q["sse"], q["n"] - 1
        q["msg"], q["mse"] = q["ssg"] / q["dfg"], q["sse"] / q["dfe"]
        q["F"] = q["msg"] / q["mse"]
        q["p"] = stats.f.sf(q["F"], q["dfg"], q["dfe"])


# ---------------------------------------------------------------- figures
def make_figures(D):
    FIG.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 12, "font.family": "DejaVu Sans"})

    # P2 boxplot
    b = D.box
    fig, ax = plt.subplots(figsize=(7.2, 2.4), dpi=150)
    ax.bxp([dict(med=b["med"], q1=b["q1"], q3=b["q3"], whislo=b["mn"], whishi=b["mx"], fliers=[])],
           vert=False, widths=0.5, patch_artist=True, showfliers=False,
           boxprops=dict(facecolor=LIGHT, edgecolor=NAVY, lw=1.6),
           medianprops=dict(color="#333333", lw=1.6), whiskerprops=dict(color="#444444", lw=1.4),
           capprops=dict(color="#444444", lw=1.4))
    ax.set_xlim(3, 10)
    ax.set_xticks(np.arange(3, 10.5, 0.5), minor=True)
    ax.set_xticks(range(3, 11))
    ax.set_yticks([])
    ax.set_xlabel("Hours of sleep on a school night")
    ax.grid(axis="x", which="both", color="#e4e4e4", lw=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(FIG / "p2_boxplot.png")
    plt.close(fig)

    # P3 scatter + line
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=150)
    ax.scatter(D.reg_x, D.reg_y, s=36, facecolor=LIGHT, edgecolor=NAVY, lw=1.3, zorder=3)
    xs = np.linspace(0, 9, 10)
    ax.plot(xs, D.reg_b0 + D.reg_b1 * xs, color=RED, lw=1.8,
            label=f"Predicted Time = {D.reg_b0} + {D.reg_b1}·Size")
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 90)
    ax.set_xlabel("Lawn size (thousands of sq ft)")
    ax.set_ylabel("Time to mow (minutes)")
    ax.legend(loc="upper left", frameon=False, fontsize=11)
    _style(ax)
    ax.grid(axis="x", color="#eeeeee", lw=0.8)
    fig.tight_layout()
    fig.savefig(FIG / "p3_regression.png")
    plt.close(fig)

    # P4 sampling distribution dotplot (500 dots, bins of 0.01)
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=150)
    vals = np.round(D.sd_props, 2)
    uniq, cnt = np.unique(vals, return_counts=True)
    for v, c in zip(uniq, cnt):
        ax.plot([v] * c, np.arange(1, c + 1), "o", ms=2.4, color=NAVY)
    ax.set_ylim(0, cnt.max() + 2)
    ax.set_xlim(0.22, 0.48)
    ax.set_xticks(np.arange(0.22, 0.481, 0.02))
    ax.set_xticklabels([f"{t:.2f}" for t in np.arange(0.22, 0.481, 0.02)], fontsize=10)
    ax.set_yticks([])
    ax.spines[["left", "right", "top"]].set_visible(False)
    ax.set_xlabel("Sample proportion who use coupons (n = 150 per sample)")
    fig.tight_layout()
    fig.savefig(FIG / "p4_sampling.png")
    plt.close(fig)

    # P6 randomization dotplot (50 dots), dots >= 74 in red
    fig, ax = plt.subplots(figsize=(7.2, 2.6), dpi=150)
    dotplot(ax, D.rz_means, 0.5, highlight=lambda v: v >= D.rz_obs)
    ax.axvline(D.rz_obs, color=RED, ls="--", lw=1.2)
    ax.text(D.rz_obs + 0.1, ax.get_ylim()[1] * 0.85, f"x̄ = {D.rz_obs}", color=RED, fontsize=11)
    ax.set_xlim(64, 76)
    ax.set_xticks(range(64, 77))
    ax.set_xlabel("Simulated sample mean score (assuming μ = 70)")
    fig.tight_layout()
    fig.savefig(FIG / "p6_randomization.png")
    plt.close(fig)


# ---------------------------------------------------------------- problems (shared by guide + solutions)
def problems(d: Doc, D: Data):
    L = 0   # no ruled lines in the guide; answers appear only in the Solutions (key) document

    # 1 ----------------------------------------------------------------
    d.problem("Problem 1. Bike-Share Trips",
              "A city's bike-share program records the following about each trip: a trip ID number, the starting station, "
              "the trip length (in minutes), the rider's age (in years), and whether the rider is a member (yes/no).")
    d.step("(a)", "What are the cases in this dataset?",
           "The cases are the **individual bike-share trips** (one row per trip).", lines=L)
    d.step("(b)", "Classify each variable as categorical, quantitative, or neither: starting station, trip length, member.",
           ["Starting station: **categorical** (it puts each trip into a group).",
            "Trip length: **quantitative** (a measured number of minutes).",
            "Member: **categorical** (yes/no).",
            "(The trip ID number is neither: it's a label, not something we analyze.)"], lines=L)
    d.step("(c)", "The city asks whether being a member affects how long a trip lasts. Identify the explanatory and response variables.",
           "Explanatory: **member (yes/no)**. Response: **trip length**.", lines=L)

    # 2 ----------------------------------------------------------------
    b = D.box
    d.problem("Problem 2. Hours of Sleep",
              "The boxplot shows the hours of sleep on a school night for a sample of college students.")
    d.image(FIG / "p2_boxplot.png", 5.8)
    d.step("(a)", "Find the median.", f"Median = **{b['med']:g} hours** (the line inside the box).", lines=L)
    d.step("(b)", "Find Q1 and Q3.", f"Q1 = **{b['q1']:g}** hours and Q3 = **{b['q3']:g}** hours (the edges of the box).", lines=L)
    d.step("(c)", "Find the range and the IQR.",
           [f"Range = max − min = {b['mx']:g} − {b['mn']:g} = **{b['mx'] - b['mn']:g} hours**.",
            f"IQR = Q3 − Q1 = {b['q3']:g} − {b['q1']:g} = **{b['q3'] - b['q1']:g} hours**."], lines=L)
    d.step("(d)", "Is the distribution most likely symmetric, skewed left, or skewed right? Explain.",
           f"**Skewed left.** The left whisker ({b['mn']:g} to {b['q1']:g}) is much longer than the right whisker "
           f"({b['q3']:g} to {b['mx']:g}), and the median sits closer to Q3. A few students sleep much less than the rest.", lines=L)

    # 3 ----------------------------------------------------------------
    d.problem("Problem 3. Mowing Time",
              f"A landscaping company predicts the time it takes to mow a lawn (in minutes) from the lawn's size (in thousands of square feet) "
              f"using the regression line  Predicted Time = {D.reg_b0} + {D.reg_b1}·Size. The scatterplot and line are shown below.")
    d.image(FIG / "p3_regression.png", 5.0)
    d.step("(a)", f"Predict the mowing time for a lawn of {D.reg_x0} thousand square feet.",
           f"Predicted Time = {D.reg_b0} + {D.reg_b1}({D.reg_x0}) = **{D.reg_pred:g} minutes**.", lines=L)
    d.step("(b)", f"One {D.reg_x0}-thousand-square-foot lawn actually took {D.reg_actual} minutes. Find the residual.",
           f"Residual = actual − predicted = {D.reg_actual} − {D.reg_pred:g} = **{D.reg_resid:g} minutes**. "
           f"(Negative: this lawn took {abs(D.reg_resid):g} minutes less than predicted, so the point is below the line.)", lines=L)
    d.step("(c)", "Interpret the slope in context.",
           f"For each additional **1,000 square feet** of lawn, the predicted mowing time increases by **{D.reg_b1} minutes**.", lines=L)
    d.step("(d)", "Interpret the intercept in context. Does it make sense here?",
           f"A lawn of size 0 is predicted to take **{D.reg_b0} minutes**. It isn't a real lawn, but it can be read as set-up time "
           "(unloading and starting equipment). Size 0 is outside the data, so we shouldn't rely on it much.", lines=L)

    # 4 ----------------------------------------------------------------
    d.problem("Problem 4. Coupon Users",
              f"A market researcher draws {D.sd_reps} random samples of {D.sd_n} shoppers each and records the proportion who use coupons in each sample. "
              "The dotplot shows the resulting sampling distribution.")
    d.image(FIG / "p4_sampling.png", 5.8)
    d.step("(a)", "What does one dot in the dotplot represent?",
           f"One dot is the **sample proportion of coupon users in one random sample of {D.sd_n} shoppers**.", lines=L)
    d.step("(b)", "Use the dotplot to estimate the proportion of ALL shoppers who use coupons.",
           f"The sampling distribution is centered at the population proportion: about **{D.sd_center:.2f}** "
           f"(the true value used to make this plot was {D.sd_p}).", lines=L)
    d.step("(c)", "Estimate the standard error.",
           f"About 95% of the dots fall within 2 SE of the center. The middle 95% of dots runs from about "
           f"{np.percentile(D.sd_props, 2.5):.2f} to {np.percentile(D.sd_props, 97.5):.2f}, a spread of about 4 SE, "
           f"so **SE ≈ {D.sd_se:.2f}**. (The exact standard deviation of these {D.sd_reps} dots is {r3(D.sd_se)}.)", lines=L)
    d.step("(d)", f"Would a sample proportion of {D.sd_check} be unusual for a sample of {D.sd_n} shoppers? Explain.",
           f"**Yes.** {D.sd_check} is out in the right tail with almost no dots. It is about "
           f"({D.sd_check} − {D.sd_center:.2f}) ÷ {D.sd_se:.2f} ≈ {D.sd_z:.1f} standard errors above the center, "
           "more than 2 SE away.", lines=L)

    # 5 ----------------------------------------------------------------
    ph, se = D.ci_phat, D.ci_se
    lo, hi = ph - 2 * se, ph + 2 * se
    d.problem("Problem 5. Driving to Campus",
              f"In a random sample of students at a college, the proportion who drive to campus is p̂ = {ph}, with a standard error of {se}.")
    d.step("(a)", "Construct a 95% confidence interval using statistic ± 2 × SE.",
           f"{ph} ± 2({se}) = {ph} ± {2 * se:.2f}, so **{lo:.2f} to {hi:.2f}**.", lines=L)
    d.step("(b)", "Interpret your interval in context.",
           f"We are 95% sure that the proportion of **all students at this college** who drive to campus is between {lo:.2f} and {hi:.2f}.", lines=L)
    d.step("(c)", "Is 0.60 a plausible value of the population proportion? Is 0.70?",
           [f"**0.60 is plausible**: it is inside the interval.",
            f"**0.70 is not plausible**: it is above {hi:.2f}."], lines=L)
    d.step("(d)", "Would a 99% confidence interval be wider or narrower? Why?",
           "**Wider.** To be more confident that we've captured the true proportion, we need a wider range of plausible values.", lines=L)

    # 6 ----------------------------------------------------------------
    d.problem("Problem 6. Tutoring and Test Scores",
              f"A tutoring center claims its program raises the mean score on a placement test above the usual average of {D.rz_null}. "
              f"A random sample of tutored students has a mean score of x̄ = {D.rz_obs}. Assuming H₀ is true, {D.rz_k} sample means were simulated "
              "to build the randomization distribution below.")
    d.image(FIG / "p6_randomization.png", 5.8)
    d.step("(a)", "State the hypotheses and define the parameter.",
           [f"H₀: μ = {D.rz_null}    Hₐ: μ > {D.rz_null}",
            "μ = the mean placement-test score of **all** students who take the tutoring program."], lines=L)
    d.step("(b)", f"Why is the randomization distribution centered at {D.rz_null}?",
           f"Because it was simulated **assuming H₀ is true**, so it is centered at the null value μ = {D.rz_null}.", lines=L)
    d.step("(c)", "Use the dotplot to find the p-value.",
           f"Hₐ uses >, so count dots at or above the sample statistic {D.rz_obs}: there are **{D.rz_count}** of {D.rz_k}. "
           f"p-value = {D.rz_count} ÷ {D.rz_k} = **{D.rz_p:.2f}**.", lines=L)
    d.step("(d)", "What is your conclusion at a 5% significance level?",
           f"{D.rz_p:.2f} < 0.05, so **reject H₀**. There is evidence that the tutoring program raises the mean placement-test score above {D.rz_null}.", lines=L)

    # 7 ----------------------------------------------------------------
    q = D.p7
    d.problem("Problem 7. Ad Clicks",
              f"A website says {q['p0']:.0%} of its visitors click on a featured ad. In a random sample of {q['n']} visitors, {q['x']} clicked the ad. "
              f"Test, at a 5% level, whether the proportion who click differs from {q['p0']:.0%}. Show all details.")
    d.step("Step 1.", "Define the parameter and state the hypotheses.",
           [f"p = the proportion of **all** visitors who click the featured ad.",
            f"H₀: p = {q['p0']}    Hₐ: p ≠ {q['p0']}   (two-tailed)"], lines=L)
    d.step("Step 2.", "Check the conditions.",
           f"n·p₀ = {q['n']}({q['p0']}) = {q['n'] * q['p0']:g} and n(1 − p₀) = {q['n'] * (1 - q['p0']):g}. Both are at least 10, so the normal distribution works.", lines=L)
    d.step("Step 3.", "Find the sample statistic and the standard error.",
           [f"p̂ = {q['x']} ÷ {q['n']} = **{q['phat']:.2f}**",
            f"SE (uses the null value p₀) = √( {q['p0']}·{1 - q['p0']} ÷ {q['n']} ) = **{r4(q['se'])}**"], lines=L)
    d.step("Step 4.", "Find the standardized test statistic.",
           f"z = ({q['phat']:.2f} − {q['p0']}) ÷ {r4(q['se'])} = **{r2(q['z'])}**", lines=L)
    d.step("Step 5.", "Find the p-value.",
           f"Two-tailed: p-value = 2 × (area above {r2(q['z'])}) = **{pv(q['p'])}**", lines=L)
    d.step("Step 6.", "Make a decision and write a conclusion in context.",
           f"{pv(q['p'])} < 0.05, so **reject H₀**. There is evidence that the proportion of visitors who click the ad differs from {q['p0']:.0%} "
           f"(the sample suggests it is higher).", lines=L)

    # 8 ----------------------------------------------------------------
    q = D.p8
    lo, hi = q["xbar"] - q["me"], q["xbar"] + q["me"]
    d.problem("Problem 8. Commute Times",
              f"A random sample of {q['n']} commuters has a mean commute time of {q['xbar']} minutes with a standard deviation of {q['s']} minutes, "
              f"and the data are reasonably symmetric. For 95% confidence with df = {q['df']}, use t* = {q['tstar']:.3f}.")
    d.step("(a)", "Why do we use a t-distribution here instead of the normal distribution?",
           "We're estimating a **mean** and we only know the **sample** standard deviation s (not σ), so we use t with df = n − 1. "
           "The sample is small, but the data are reasonably symmetric, so t is OK.", lines=L)
    d.step("(b)", "Find the standard error.", f"SE = s ÷ √n = {q['s']} ÷ √{q['n']} = **{r3(q['se'])}**", lines=L)
    d.step("(c)", "Find the 95% confidence interval.",
           [f"Margin of error = t*·SE = {q['tstar']:.3f} × {r3(q['se'])} = {r2(q['me'])}",
            f"{q['xbar']} ± {r2(q['me'])}, so **{r2(lo)} to {r2(hi)} minutes**."], lines=L)
    d.step("(d)", "Interpret the interval in context.",
           f"We are 95% sure that the mean commute time of **all** commuters in this population is between {r2(lo)} and {r2(hi)} minutes.", lines=L)

    # 9 ----------------------------------------------------------------
    q = D.p9
    d.problem("Problem 9. Two Exercise Programs",
              f"Two exercise programs are compared. A random sample of {q['n1']} people in Program A lost a mean of {q['x1']} pounds (s = {q['s1']}), "
              f"and a separate random sample of {q['n2']} people in Program B lost a mean of {q['x2']} pounds (s = {q['s2']}). "
              "Both distributions are reasonably symmetric. Test, at a 5% level, whether Program A leads to a greater mean weight loss.")
    d.step("Step 1.", "Define the parameters and state the hypotheses.",
           ["μ_{A}, μ_{B} = the mean weight loss of **all** people who would use Program A and Program B.",
            "H₀: μ_{A} = μ_{B}    Hₐ: μ_{A} > μ_{B}   (right-tailed)"], lines=L)
    d.step("Step 2.", "Check the conditions.",
           f"Both samples are at least 30 ({q['n1']} and {q['n2']}), and the distributions are reasonably symmetric, so the t-distribution works.", lines=L)
    d.step("Step 3.", "Find the sample statistic and the standard error.",
           [f"x̄_{{A}} − x̄_{{B}} = {q['x1']} − {q['x2']} = **{q['diff']:.1f}** pounds",
            f"SE = √( {q['s1']}²/{q['n1']} + {q['s2']}²/{q['n2']} ) = **{r4(q['se'])}**"], lines=L)
    d.step("Step 4.", "Find the standardized test statistic and the p-value.",
           [f"t = ({q['diff']:.1f} − 0) ÷ {r4(q['se'])} = **{r2(q['t'])}**",
            f"df = smaller n − 1 = {q['df']}. Right-tailed: p-value = area above {r2(q['t'])} = **{pv(q['p'])}**"], lines=L)
    d.step("Step 5.", "Make a decision and write a conclusion in context.",
           f"{pv(q['p'])} < 0.05, so **reject H₀**. There is evidence that Program A leads to a greater mean weight loss than Program B.", lines=L)

    # 10 ---------------------------------------------------------------
    q = D.p10
    d.problem("Problem 10. Yoga and Resting Heart Rate",
              f"{q['n']} adults had their resting heart rate (beats per minute) measured before and after a six-week yoga program. "
              "The table shows each person's rates and the difference d = After − Before. The differences are reasonably symmetric. "
              "Test, at a 5% level, whether the program lowers mean resting heart rate.")
    keep_table(d.table([["Person"] + [chr(65 + i) for i in range(q["n"])],
             ["Before"] + [str(v) for v in D.p10_before],
             ["After"] + [str(v) for v in D.p10_after],
             ["d = After − Before"] + [str(v) for v in D.p10_d]],
            widths=[1.6] + [0.55] * q["n"], font_size=10))
    d.step("Step 1.", "Why is this paired data?",
           "The **same people** were measured twice (before and after), so the two columns are not independent. We analyze the differences.", lines=L)
    d.step("Step 2.", "Define the parameter and state the hypotheses.",
           ["μ_{d} = the mean change (After − Before) in resting heart rate for **all** adults who do the program.",
            "H₀: μ_{d} = 0    Hₐ: μ_{d} < 0   (left-tailed: \"lowers\")"], lines=L)
    d.step("Step 3.", "Find the mean and standard deviation of the differences, and the standard error.",
           [f"x̄_{{d}} = **{q['dbar']:.2f}**, s_{{d}} = **{r3(q['sd'])}**, n_{{d}} = {q['n']}",
            f"SE = s_{{d}} ÷ √n_{{d}} = {r3(q['sd'])} ÷ √{q['n']} = **{r3(q['se'])}**"], lines=L)
    d.step("Step 4.", "Find the standardized test statistic and the p-value.",
           [f"t = ({q['dbar']:.2f} − 0) ÷ {r3(q['se'])} = **{r2(q['t'])}**",
            f"df = {q['df']}. Left-tailed: p-value = area below {r2(q['t'])} = **{pv(q['p'])}**"], lines=L)
    d.step("Step 5.", "Make a decision and write a conclusion in context.",
           f"{pv(q['p'])} < 0.05, so **reject H₀**. There is evidence that the yoga program lowers mean resting heart rate.", lines=L)

    # 11 ---------------------------------------------------------------
    d.problem("Problem 11. Choosing the Right Method",
              "For each study, state whether you should use methods for a single proportion, a single mean, a difference in proportions, "
              "a difference in means, paired data, or a chi-square test for association.")
    picks = [
        ("Does the mean number of hours worked per week differ between full-time and part-time students? (two separate samples)",
         "**Difference in means**: a quantitative response compared across two independent groups."),
        ("Is there an association between a student's major (five categories) and their preferred class time (morning, afternoon, evening)?",
         "**Chi-square test for association**: two categorical variables, and at least one has more than two categories."),
        ("Each of 15 runners is timed on the same course wearing old shoes and then new shoes. Are they faster in new shoes?",
         "**Paired data**: the same runners are measured twice, so analyze the differences."),
        ("What proportion of all ACC students use the campus library at least once a week?",
         "**Single proportion**: one group, one yes/no variable."),
        ("Is the mean daily screen time of adults in a city more than 4 hours?",
         "**Single mean**: one group, one quantitative variable."),
        ("Is the proportion of smokers different for adults under 30 and adults 30 and older?",
         "**Difference in proportions**: a yes/no variable compared across two groups."),
    ]
    for k, (qq, a) in enumerate(picks):
        d.step(f"({chr(97 + k)})", qq, a, lines=L)

    # 12 ---------------------------------------------------------------
    q, o = D.p12, D.p12_obs
    rows_n, cols_n = o.sum(axis=1), o.sum(axis=0)
    d.problem("Problem 12. Grade Level and Study Time",
              f"A college asks {o.sum()} students when they prefer to study. The table shows the observed counts. "
              "Test, at a 5% level, whether preferred study time is associated with grade level.")
    keep_table(d.table([["Observed", "Morning", "Afternoon", "Evening", "Total"],
             ["First-year"] + [str(v) for v in o[0]] + [str(rows_n[0])],
             ["Second-year"] + [str(v) for v in o[1]] + [str(rows_n[1])],
             ["Total"] + [str(v) for v in cols_n] + [str(o.sum())]],
            widths=[1.4, 1.1, 1.1, 1.1, 0.9]))
    d.step("Step 1.", "State the hypotheses.",
           ["H₀: Preferred study time and grade level are **not associated**.",
            "Hₐ: Preferred study time and grade level **are associated**."], lines=L)
    e = q["exp"]
    d.step("Step 2.", "Find the expected counts. Are they all at least 5?",
           [f"Expected = (row total × column total) ÷ grand total, e.g. First-year/Morning = {rows_n[0]} × {cols_n[0]} ÷ {o.sum()} = {e[0, 0]:.1f}.",
            "Expected counts: Morning " + f"{e[0, 0]:.1f}, Afternoon {e[0, 1]:.1f}, Evening {e[0, 2]:.1f} in each row (the rows have equal totals).",
            "**All are at least 5**, so the chi-square test is appropriate."], lines=L)
    c = q["contrib"]
    d.step("Step 3.", "Find the chi-square statistic and the degrees of freedom.",
           ["χ² = Σ (observed − expected)² ÷ expected",
            "Contributions: " + ", ".join(f"{v:.3f}" for v in c.flatten()),
            f"χ² = **{q['chi2']:.2f}**, df = (2 − 1)(3 − 1) = **{q['df']}**"], lines=L)
    d.step("Step 4.", "Find the p-value, make a decision, and write a conclusion in context.",
           [f"p-value = area to the right of {q['chi2']:.2f} in a χ² distribution with df = {q['df']}: **{pv(q['p'])}**",
            f"{pv(q['p'])} < 0.05, so **reject H₀**. There is evidence that preferred study time is associated with grade level: "
            "first-year students prefer evenings more than expected, and second-year students prefer mornings more than expected."], lines=L)

    # 13 ---------------------------------------------------------------
    q = D.p13
    lo, hi = q["b1"] - q["tstar"] * q["se"], q["b1"] + q["tstar"] * q["se"]
    d.problem("Problem 13. House Size and Price",
              f"A real-estate agent uses a random sample of {q['n']} homes to see whether size (in hundreds of square feet) can be used to predict "
              f"price (in thousands of dollars). The regression output gives a slope of {q['b1']} (thousand dollars per hundred square feet) "
              f"with a standard error of {q['se']}.")
    d.step("(a)", "State the hypotheses for testing whether size is an effective predictor of price.",
           ["H₀: β₁ = 0  (size is not a useful predictor)    Hₐ: β₁ ≠ 0",
            "β₁ = the slope of the population regression line for all homes in this market."], lines=L)
    d.step("(b)", "Find the test statistic and the p-value.",
           [f"t = (b₁ − 0) ÷ SE = {q['b1']} ÷ {q['se']} = **{r2(q['t'])}**",
            f"df = n − 2 = {q['df']}. Two-tailed p-value = **{pv(q['p'])}**"], lines=L)
    d.step("(c)", "What is your conclusion at a 5% level?",
           f"{pv(q['p'])} < 0.05, so **reject H₀**. There is evidence that home size is an effective predictor of price.", lines=L)
    d.step("(d)", f"Find a 95% confidence interval for the population slope (use t* = {q['tstar']:.3f}).",
           f"{q['b1']} ± {q['tstar']:.3f}({q['se']}) = {q['b1']} ± {r2(q['tstar'] * q['se'])}, so **{r2(lo)} to {r2(hi)}** thousand dollars per hundred square feet. "
           "0 is not in the interval, which agrees with part (c).", lines=L)

    # 14 ---------------------------------------------------------------
    q = D.p14
    d.problem("Problem 14 (ANOVA). Three Teaching Methods",
              f"{q['n']} students were randomly assigned to one of {q['k']} teaching methods (10 per method), and their final scores were compared. "
              "Use the partial ANOVA table to test, at a 5% level, whether the mean final score differs among the three methods. "
              "The conditions for ANOVA are met.")
    keep_table(d.table([["Source", "df", "SS", "MS", "F"],
             ["Groups", ("ans", q["dfg"]), f"{q['ssg']:g}", ("ans", f"{q['msg']:g}"), ("ans", f"{q['F']:.2f}")],
             ["Error", ("ans", q["dfe"]), f"{q['sse']:g}", ("ans", f"{q['mse']:g}"), ""],
             ["Total", ("ans", q["dft"]), ("ans", f"{q['sst']:g}"), "", ""]],
            widths=[1.2, 0.9, 1.1, 1.1, 1.0]))
    d.step("(a)", "State the hypotheses.",
           ["H₀: μ₁ = μ₂ = μ₃  (all three methods have the same mean final score)",
            "Hₐ: at least one method's mean is different."], lines=L)
    d.step("(b)", "Fill in the missing entries in the table.",
           [f"df Groups = k − 1 = {q['dfg']};  df Error = n − k = {q['dfe']};  df Total = n − 1 = {q['dft']}",
            f"SS Total = {q['ssg']:g} + {q['sse']:g} = {q['sst']:g}",
            f"MSG = SSG ÷ df = {q['ssg']:g} ÷ {q['dfg']} = {q['msg']:g};  MSE = SSE ÷ df = {q['sse']:g} ÷ {q['dfe']} = {q['mse']:g}",
            f"F = MSG ÷ MSE = {q['msg']:g} ÷ {q['mse']:g} = **{q['F']:.2f}**"], lines=L)
    d.step("(c)", "Find the p-value and write a conclusion in context.",
           [f"p-value = area to the right of F = {q['F']:.2f} in an F distribution with df {q['dfg']} and {q['dfe']}: **{pv(q['p'])}**",
            f"{pv(q['p'])} > 0.05, so **do not reject H₀**. The data do not provide evidence that the mean final score differs among the three teaching methods."], lines=L)


# ---------------------------------------------------------------- review section of the guide
def review(d: Doc):
    d.para("This guide covers everything on the Final Exam, in the same order as the exam. For each topic you'll find the key ideas, "
           "what to be able to do, and the mistakes to avoid. There's a formula sheet, a decision guide, and 14 practice problems "
           "(one for each exam question, plus an ANOVA problem). Full worked solutions are in the separate **Final Exam Study Guide: Solutions** document.")
    d.directions(["Comprehensive: Chapters 1–9. 13 questions, 100 points, proctored with Respondus (environment check, ID, and second camera, the same as the tests).",
                  "Show your work on calculations, round to two decimal places unless told otherwise, and use a 5% significance level unless a problem says otherwise."],
                 heading="Exam basics")

    d.section("Part 1. Describing Data (Chapters 1–2)")
    d.subheading("Cases and variables")
    d.bullets(["**Cases** are the people or things the data describe (one row each).",
               "**Categorical** variables put cases into groups (yes/no, breed, station). **Quantitative** variables are measured numbers (weight, minutes).",
               "An ID number is neither: it's a label.",
               "**Explanatory** variable: the one you think affects the other. **Response**: the one being affected."])
    d.subheading("Boxplots and shape")
    d.bullets(["The box runs from Q1 to Q3, with the median inside. Whiskers go to the min and max (or to the last non-outlier).",
               "Range = max − min.  IQR = Q3 − Q1.  Outlier fences: Q1 − 1.5·IQR and Q3 + 1.5·IQR.",
               "The longer whisker (and the side farther from the median) points to the skew: long left side means skewed left."])
    d.callout("The skew is named for the long tail, not for where most of the data are. Most data on the right with a long left tail is skewed LEFT.", label="Watch out:")
    d.subheading("Regression")
    d.bullets(["Predicted y = intercept + slope · x. Plug in x to predict.",
               "**Residual** = actual − predicted. Positive means the point is above the line.",
               "**Slope**: for each 1-unit increase in x, the predicted y changes by the slope (in y's units).",
               "**Intercept**: predicted y when x = 0. It may not make sense if x = 0 is outside the data."])
    d.para("**Be able to:** read a boxplot, name the cases and variable types, predict with a line, find a residual, and interpret slope and intercept in context.")

    d.section("Part 2. Sampling Distributions and Confidence Intervals (Chapter 3)")
    d.bullets(["A **sampling distribution** shows the statistic from many samples of the same size. One dot = one sample's statistic.",
               "It is centered at the **population parameter**. Its standard deviation is the **standard error (SE)**.",
               "About 95% of dots fall within 2 SE of the center, so the middle 95% of the dots spans about 4 SE.",
               "95% confidence interval: **statistic ± 2·SE**. Values inside are plausible; values outside are not.",
               "Higher confidence (99%) gives a wider interval; a bigger sample gives a narrower one."])
    d.callout("A 95% interval is about the population parameter, not about individuals. \"95% of students drive\" is a wrong interpretation.", label="Watch out:")
    d.para("**Interpretation template:** \"We are 95% sure that the [parameter in context] is between [lower] and [upper].\"")

    d.section("Part 3. Hypothesis Tests (Chapter 4)")
    d.bullets(["**H₀** is the no-effect claim with \"=\". **Hₐ** is what you want evidence for: >, <, or ≠ from the wording.",
               "A **randomization distribution** is simulated assuming H₀ is true, so it's centered at the null value.",
               "**p-value** = proportion of simulated statistics at or beyond the sample statistic, in the direction of Hₐ. Double it for a two-tailed test.",
               "Decision: if p-value < α, reject H₀ (\"there is evidence that…\"). Otherwise do not reject H₀ (\"the data do not provide evidence that…\")."])
    d.callout("Never say \"accept H₀\". Not rejecting H₀ means the evidence isn't strong enough, not that H₀ is true.", label="Watch out:")

    d.section("Part 4. Inference with Formulas (Chapters 5–6)")
    d.bullets(["Every test: **z or t = (statistic − null value) ÷ SE**. Every interval: **statistic ± (z* or t*) × SE**.",
               "Proportions use the normal (z). Check at least 10 successes and 10 failures (use p₀ for a test).",
               "Means use the t-distribution: one mean df = n − 1; two means df = smaller n − 1; paired df = n_{d} − 1.",
               "For a one-proportion **test**, the SE uses the null value p₀. For an **interval**, it uses p̂.",
               "**Paired data**: the same subjects measured twice. Subtract to get one list of differences, then do a one-sample t on them."])
    d.callout("Paired vs. two independent samples is the most common Chapter 6 mistake. Ask: are the same people (or matched pairs) measured twice?", label="Watch out:")
    d.subheading("Choosing the right method")
    d.image(FLOWCHART, 4.3)
    d.bullets(["Two categorical variables (a two-way table, more than 2 categories) → **chi-square test for association**.",
               "Two quantitative variables, predicting one from the other → **inference for slope** (regression).",
               "A quantitative response compared across **3 or more** groups → **ANOVA**."])

    d.section("Part 5. Chi-Square, Regression Inference, and ANOVA (Chapters 7–9)")
    d.subheading("Chi-square test for association")
    d.bullets(["H₀: the two variables are not associated. Hₐ: they are associated.",
               "Expected count = row total × column total ÷ grand total. All expected counts should be at least 5.",
               "χ² = Σ (observed − expected)² ÷ expected, with df = (rows − 1)(columns − 1). The p-value is the right-tail area."])
    d.subheading("Inference for slope")
    d.bullets(["H₀: β₁ = 0 (x is not a useful predictor) vs Hₐ: β₁ ≠ 0.",
               "t = slope ÷ SE of slope, with df = n − 2. Interval: b₁ ± t*·SE.",
               "If 0 is outside the interval for the slope, x is an effective predictor."])
    d.subheading("ANOVA for comparing means")
    d.bullets(["H₀: all group means are equal. Hₐ: at least one mean is different.",
               "df Groups = k − 1, df Error = n − k. MS = SS ÷ df. F = MSG ÷ MSE.",
               "A large F (small p-value) means the group means differ more than random variation would explain."])

    d.section("Formula and Rule Quick Reference")
    d.table([["Situation", "Statistic", "Standard error", "Distribution / df"],
             ["One proportion: test", "p̂", "√(p₀(1 − p₀)/n)", "Normal (z)"],
             ["One proportion: interval", "p̂", "√(p̂(1 − p̂)/n)", "Normal (z*)"],
             ["Difference in proportions", "p̂₁ − p̂₂", "test: pooled p̂;  interval: √(p̂₁(1 − p̂₁)/n₁ + p̂₂(1 − p̂₂)/n₂)", "Normal (z)"],
             ["One mean", "x̄", "s/√n", "t, df = n − 1"],
             ["Difference in means", "x̄₁ − x̄₂", "√(s₁²/n₁ + s₂²/n₂)", "t, df = smaller n − 1"],
             ["Paired means", "x̄_{d}", "s_{d}/√n_{d}", "t, df = n_{d} − 1"],
             ["Slope", "b₁", "from regression output", "t, df = n − 2"],
             ["Chi-square association", "χ² = Σ(O − E)²/E", "E = row × column ÷ total", "χ², df = (r − 1)(c − 1)"],
             ["ANOVA", "F = MSG/MSE", "MS = SS/df", "F, df = k − 1 and n − k"]],
            widths=[1.75, 1.1, 2.6, 1.55], font_size=9.5)
    d.table([["Rule", ""],
             ["Test statistic", "(statistic − null value) ÷ SE"],
             ["Confidence interval", "statistic ± (z* or t*) × SE;  quick 95%: statistic ± 2·SE"],
             ["z* values", "90% → 1.645,  95% → 1.96,  99% → 2.576"],
             ["Decision", "reject H₀ when p-value < α"],
             ["Interval ↔ test", "two-tailed test at 5% matches the 95% interval: reject H₀ when the null value is outside it"]],
            widths=[1.8, 5.2], header_row=False, center=False, font_size=10)


# ---------------------------------------------------------------- build
def build(out_dir):
    D = Data()
    make_figures(D)
    sub = "Covers Chapters 1–9  ·  Comprehensive"

    g = Doc("Study Guide", "Final Exam Study Guide", sub, name_line=False)
    review(g)
    g.page_break()
    g.section("Practice Problems")
    g.para("Problems 1–13 match the 13 questions on the Final Exam, in order; Problem 14 practices ANOVA. "
           "Try them without notes first, then check your work against the **Final Exam Study Guide: Solutions** document.", italic=True)
    problems(g, D)
    g.end("End of study guide")
    g.save(out_dir / "Final_Exam_Study_Guide.docx")

    s = Doc("Solutions", "Final Exam Study Guide: Solutions", sub + "  ·  Full worked solutions", name_line=False, key=True)
    s.para("These are complete solutions to the Practice Problems in the **Final Exam Study Guide**. "
           "Try each problem on your own first, then compare your work step by step.")
    problems(s, D)
    s.end("End of solutions")
    s.save(out_dir / "Final_Exam_Study_Guide_Solutions.docx")
    return D
