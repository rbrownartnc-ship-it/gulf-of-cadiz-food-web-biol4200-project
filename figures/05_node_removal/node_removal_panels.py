"""Results figure and table for the node-removal (persistence) subsection, from the group's own output tables.
    python make_node_removal_panels.py <repo_root> <out_dir>
Figure: A/B removal curves (two extinction rules), C = R50 table.  Also writes r50_table.tex/.csv.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e1e0d9"
BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#898781"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 7, "axes.labelsize": 7, "axes.titlesize": 7.5,
    "xtick.labelsize": 6.5, "ytick.labelsize": 6.5, "legend.fontsize": 6.5, "text.color": INK,
    "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "axes.edgecolor": GRID,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})
STRICT, HALF = "all prey lost", "half of diet lost"

def title(ax, letter, text):
    ax.set_title(f"{letter}  {text}", loc="left", fontsize=7.5, fontweight="bold", color=INK, pad=4)
def tidy(ax, axis="both"):
    ax.grid(axis=axis, color=GRID, lw=0.4); ax.set_axisbelow(True); ax.tick_params(length=2, pad=1.5)

curves = pd.read_csv(REPO / "output/cadiz_node_robustness_curves.csv")
summ = pd.read_csv(REPO / "output/cadiz_node_robustness_summary.csv")
guild = pd.read_csv(REPO / "output/cadiz_guild_removal.csv").set_index("guild")

fig = plt.figure(figsize=(7.0, 6.2))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.05], left=0.07, right=0.995, top=0.95, bottom=0.03, wspace=0.28, hspace=0.42)
series = [("most connected first", "most links", BLUE),
          ("lowest trophic level first", "lowest trophic level", ORANGE),
          ("highest trophic level first", "highest trophic level", AQUA)]
for k, (rule, letter) in enumerate(((STRICT, "A"), (HALF, "B"))):
    ax = fig.add_subplot(gs[0, k]); sel = curves[curves.rule == rule]
    ax.plot([0, 1], [0, 1], color=GRID, lw=0.9, ls=(0, (3, 2)), zorder=1)
    ax.axhline(0.5, color=GRID, lw=0.6, zorder=1)
    r = sel[sel.order == "random (mean of 1000)"]
    ax.fill_between(r.frac_removed, r.frac_lost_lo, r.frac_lost_hi, color=GREY, alpha=0.25, lw=0, zorder=2)
    ax.plot(r.frac_removed, r.frac_lost, color=GREY, lw=1.2, zorder=3)
    for key, lab, col in series:
        d = sel[sel.order == key]; assert len(d), (rule, key)
        ax.plot(d.frac_removed, d.frac_lost, color=col, lw=1.3, zorder=4)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
    ax.set_xlabel("share of groups removed", labelpad=2)
    if k == 0: ax.set_ylabel("share of groups lost", labelpad=2)
    tidy(ax); title(ax, letter, f"Rule: {rule}")
handles = [Line2D([], [], color=GREY, lw=1.6, label="random orders (band: 95% range)")] + \
          [Line2D([], [], color=c, lw=1.6, label=l) for _, l, c in series]
fig.legend(handles=handles, loc="lower left", ncol=2, frameon=False, handlelength=1.4, handletextpad=0.4,
           columnspacing=1.4, labelspacing=0.25, bbox_to_anchor=(0.07, 0.468))

# ---- R50 table (panel C). bold = fewer than 5% of random orders do as badly (frac_random_below < 0.05)
labels = {"random": "random (1000 orders)", "most connected first": "most links first",
          "least connected first": "fewest links first", "highest betweenness first": "highest betweenness first",
          "most important prey first": "most important prey first", "highest PageRank importance first": "highest PageRank first",
          "lowest trophic level first": "lowest trophic level first", "highest trophic level first": "highest trophic level first",
          "most connected first (recalculated)": "most links first (recalc.)",
          "highest betweenness first (recalculated)": "highest betweenness first (recalc.)"}
rows, bold, tex_rows = [], [], []
for o, lab in labels.items():
    cells, b_, tc = [lab], [False], []
    for rule in (STRICT, HALF):
        s_ = summ[summ.rule == rule].set_index("order"); v = s_.loc[o, "R50"]
        if o == "random":
            cells.append(f"{v:.2f}  ({s_.loc[o,'random_R50_lo']:.2f}–{s_.loc[o,'random_R50_hi']:.2f})"); b_.append(False)
            tc.append(f"{v:.2f} ({s_.loc[o,'random_R50_lo']:.2f}--{s_.loc[o,'random_R50_hi']:.2f})")
        else:
            bd = s_.loc[o, "frac_random_below"] < 0.05
            cells.append(f"{v:.2f}"); b_.append(bool(bd)); tc.append(f"\\textbf{{{v:.2f}}}" if bd else f"{v:.2f}")
    rows.append(cells); bold.append(b_); tex_rows.append(f"{lab} & {tc[0]} & {tc[1]} \\\\")
axT = fig.add_subplot(gs[1, :]); axT.axis("off")
title(axT, "C", "R50: share of groups removed when half of the web is lost")
t = axT.table(cellText=rows, colLabels=["Removal order", "R50, all prey lost", "R50, half of diet lost"],
              colWidths=[0.44, 0.28, 0.28], loc="upper center", cellLoc="center", bbox=[0, 0, 1, 0.95])
t.auto_set_font_size(False); t.set_fontsize(7)
for (i, j), c in t.get_celld().items():
    c.set_edgecolor(GRID); c.set_linewidth(0.5)
    if j == 0: c.set_text_props(ha="left"); c.get_text().set_x(0.03)
    if i == 0: c.set_facecolor("#f1f0eb"); c.set_text_props(fontweight="bold", color=INK)
    else:
        c.set_text_props(color=INK, fontweight="bold" if bold[i-1][j] else "normal")
        if i == 1: c.set_facecolor("#f7f6f2")
fig.savefig(OUT / "node_removal_results.pdf", bbox_inches="tight", pad_inches=0.04)
fig.savefig(OUT / "node_removal_results.png", dpi=300, bbox_inches="tight", pad_inches=0.04)
tex = ("\\begin{tabular}{lcc}\n\\hline\nRemoval order & R50, all prey lost & R50, half of diet lost \\\\\n\\hline\n"
       + "\n".join(tex_rows) + "\n\\hline\n\\end{tabular}\n")
(OUT / "r50_table.tex").write_text(tex)
pd.DataFrame([[r[0], r[1], r[2]] for r in rows], columns=["order", "R50 all prey lost", "R50 half of diet lost"]).to_csv(OUT / "r50_table.csv", index=False)
print(tex)
