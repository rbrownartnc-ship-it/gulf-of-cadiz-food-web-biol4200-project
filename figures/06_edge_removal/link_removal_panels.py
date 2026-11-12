"""Results figures and table for the link-removal subsection, from the group's own output tables.
    python make_link_removal_panels.py <repo_root> <out_dir>
Figure 1 (link_removal_results): A/B  fraction of living groups lost as links are cut (two extinction rules),
                                  C    L50 table (fraction of the 397 links cut before half of the 41 living groups are lost)
Figure 2 (critical_single_links): the 14 single links whose loss alone causes an extinction, under both rules
Also writes l50_table.tex / l50_table.csv.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e1e0d9"
BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#898781"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 7, "axes.labelsize": 7, "axes.titlesize": 7.5,
    "xtick.labelsize": 6.5, "ytick.labelsize": 6.5, "legend.fontsize": 6.5, "text.color": INK,
    "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "axes.edgecolor": GRID,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})
STRICT, HALF = "all prey lost", "half of diet lost"

def title(ax, letter, text):
    ax.set_title(f"{letter}  {text}" if letter else text, loc="left", fontsize=7.5, fontweight="bold", color=INK, pad=4)
def tidy(ax, axis="both"):
    ax.grid(axis=axis, color=GRID, lw=0.4); ax.set_axisbelow(True); ax.tick_params(length=2, pad=1.5)

curves = pd.read_csv(REPO / "output/cadiz_link_robustness_curves.csv")
summ = pd.read_csv(REPO / "output/cadiz_link_robustness_summary.csv")
knock = pd.read_csv(REPO / "output/cadiz_link_knockouts.csv")

# =============== Figure 1 ===============
fig = plt.figure(figsize=(7.0, 5.6))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.0], left=0.07, right=0.995, top=0.95, bottom=0.03, wspace=0.28, hspace=0.45)
series = [("strongest links first", "strongest links", BLUE, "-"),
          ("weakest links first", "weakest links", AQUA, "-"),
          ("links from lowest-trophic-level prey first", "links from lowest-level prey", ORANGE, "-"),
          ("highest edge betweenness first (recalculated)", "highest edge betweenness (recalculated)", INK, (0, (4, 1.5)))]
for k, (rule, letter) in enumerate(((STRICT, "A"), (HALF, "B"))):
    ax = fig.add_subplot(gs[0, k]); sel = curves[curves.rule == rule]
    ax.plot([0, 1], [0, 0], color=GRID, lw=0.9, zorder=1)
    ax.axhline(0.5, color=GRID, lw=0.6, zorder=1)
    r = sel[sel.order == "random (mean of 500)"]
    ax.fill_between(r.frac_cut, r.frac_lost_lo, r.frac_lost_hi, color=GREY, alpha=0.25, lw=0, zorder=2)
    ax.plot(r.frac_cut, r.frac_lost, color=GREY, lw=1.2, zorder=3)
    for key, lab, col, ls in series:
        d = sel[sel.order == key]; assert len(d), (rule, key)
        ax.plot(d.frac_cut, d.frac_lost, color=col, lw=1.3, ls=ls, zorder=4)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
    ax.set_xlabel("share of links cut", labelpad=2)
    if k == 0: ax.set_ylabel("share of groups lost", labelpad=2)
    tidy(ax); title(ax, letter, f"Rule: {rule}")
handles = [Line2D([], [], color=GREY, lw=1.6, label="random orders (band: 95% range)")] + \
          [Line2D([], [], color=c, lw=1.6, ls=ls, label=l) for _, l, c, ls in series]
fig.legend(handles=handles, loc="lower left", ncol=3, frameon=False, handlelength=2.0, handletextpad=0.4,
           columnspacing=1.4, labelspacing=0.25, bbox_to_anchor=(0.07, 0.462))

labels = {"random": "random (500 orders)", "strongest links first": "strongest links first",
          "weakest links first": "weakest links first", "highest edge betweenness first": "highest edge betweenness first",
          "highest edge betweenness first (recalculated)": "highest edge betweenness first (recalc.)",
          "links from lowest-trophic-level prey first": "links from lowest-level prey first",
          "links into highest-trophic-level predators first": "links into highest-level predators first"}
rows, bold, tex_rows = [], [], []
for o, lab in labels.items():
    cells, b_, tc = [lab], [False], []
    for rule in (STRICT, HALF):
        s_ = summ[summ.rule == rule].set_index("order"); v = s_.loc[o, "L50"]
        if o == "random":
            cells.append(f"{v:.2f}  ({s_.loc[o,'random_L50_lo']:.2f}–{s_.loc[o,'random_L50_hi']:.2f})"); b_.append(False)
            tc.append(f"{v:.2f} ({s_.loc[o,'random_L50_lo']:.2f}--{s_.loc[o,'random_L50_hi']:.2f})")
        else:
            bd = bool(s_.loc[o, "frac_random_below"] < 0.05)
            cells.append(f"{v:.2f}"); b_.append(bd); tc.append(f"\\textbf{{{v:.2f}}}" if bd else f"{v:.2f}")
    rows.append(cells); bold.append(b_); tex_rows.append(f"{lab} & {tc[0]} & {tc[1]} \\\\")
axT = fig.add_subplot(gs[1, :]); axT.axis("off")
title(axT, "C", "L50: share of links cut when half of the groups are lost")
t = axT.table(cellText=rows, colLabels=["Cutting order", "L50, all prey lost", "L50, half of diet lost"],
              colWidths=[0.44, 0.28, 0.28], loc="upper center", cellLoc="center", bbox=[0, 0.0, 1, 0.9])
t.auto_set_font_size(False); t.set_fontsize(7)
for (i, j), c in t.get_celld().items():
    c.set_edgecolor(GRID); c.set_linewidth(0.5)
    if j == 0: c.set_text_props(ha="left"); c.get_text().set_x(0.03)
    if i == 0: c.set_facecolor("#f1f0eb"); c.set_text_props(fontweight="bold", color=INK)
    else:
        c.set_text_props(color=INK, fontweight="bold" if bold[i-1][j] else "normal")
        if i == 1: c.set_facecolor("#f7f6f2")
fig.savefig(OUT / "link_removal_results.pdf", bbox_inches="tight", pad_inches=0.04)
fig.savefig(OUT / "link_removal_results.png", dpi=300, bbox_inches="tight", pad_inches=0.04)
tex = ("\\begin{tabular}{lcc}\n\\hline\nCutting order & L50, all prey lost & L50, half of diet lost \\\\\n\\hline\n"
       + "\n".join(tex_rows) + "\n\\hline\n\\end{tabular}\n")
(OUT / "l50_table.tex").write_text(tex)
pd.DataFrame([r for r in rows], columns=["order", "L50 all prey lost", "L50 half of diet lost"]).to_csv(OUT / "l50_table.csv", index=False)

# =============== Figure 2: single links whose loss alone causes an extinction ===============
crit = knock[(knock.secondary_topological > 0) | (knock.secondary_weighted > 0)].copy()
crit = crit.sort_values(["secondary_weighted", "secondary_topological"], ascending=True).reset_index(drop=True)
n_all = len(knock)
fig2, ax = plt.subplots(figsize=(6.6, 3.6))
y = np.arange(len(crit))
lab = [f"{p} → {q}" for p, q in zip(crit.prey, crit.predator)]
ax.hlines(y, crit.secondary_topological, crit.secondary_weighted, color=GRID, lw=1.2, zorder=2)
ax.scatter(crit.secondary_weighted, y, s=30, facecolor="white", edgecolor=INK2, linewidth=0.8, zorder=3)
ax.scatter(crit.secondary_topological, y, s=14, color=INK2, zorder=4)
ax.set_yticks(y); ax.set_yticklabels(lab)
ax.set_xlim(-0.5, crit.secondary_weighted.max() + 1); ax.set_ylim(-0.7, len(crit) - 0.3)
ax.set_xlabel("groups lost after cutting this one link", labelpad=2)
ax.legend(handles=[Line2D([], [], marker="o", color="none", markerfacecolor=INK2, markeredgecolor=INK2, markersize=4, label=STRICT),
                   Line2D([], [], marker="o", color="none", markerfacecolor="white", markeredgecolor=INK2, markersize=5.5, label=HALF)],
          loc="lower right", frameon=False, handletextpad=0.2, labelspacing=0.2)
tidy(ax, "x"); title(ax, "", f"Single links whose loss alone causes an extinction ({len(crit)} of {n_all} links)")
fig2.tight_layout()
fig2.savefig(OUT / "critical_single_links_panel.pdf", bbox_inches="tight", pad_inches=0.04)
fig2.savefig(OUT / "critical_single_links_panel.png", dpi=300, bbox_inches="tight", pad_inches=0.04)
print(tex); print(len(crit), "critical links of", n_all)
