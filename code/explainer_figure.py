"""Explainer (workflow) figure built only from the group's own output tables.
Reads the repo read-only; writes to the folder given as argv[2]."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Rectangle
from matplotlib.lines import Line2D
from scipy.stats import spearmanr

REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2])
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e1e0d9"
BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#898781"
CAT = {"invertebrates & plankton": (BLUE, "o"), "fishes": (ORANGE, "s"),
       "marine mammals, birds, turtles": (AQUA, "^"), "non-living": (GREY, "X")}
plt.rcParams.update({"font.family": "sans-serif", "font.size": 7, "axes.labelsize": 7,
    "axes.titlesize": 7.5, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "legend.fontsize": 6.5, "text.color": INK, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.edgecolor": GRID,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})

# ---------- data (all from the repo) ----------
raw = pd.read_csv(REPO / "data/web-of-life_2026-10-15_210043/FW_005.csv", index_col=0)
traits = pd.read_csv(REPO / "output/cadiz_node_traits.csv").set_index("group_name")
edges = pd.read_csv(REPO / "output/cadiz_edges.csv")
cent = pd.read_csv(REPO / "output/cadiz_centrality.csv")
null = pd.read_csv(REPO / "output/cadiz_structure_vs_null.csv")
node_curves = pd.read_csv(REPO / "output/cadiz_node_robustness_curves.csv")
node_sum = pd.read_csv(REPO / "output/cadiz_node_robustness_summary.csv")
assert raw.shape == (44, 44) and int((raw.values > 0).sum()) == 413
assert len(traits) == 43 and len(edges) == 411

def title(ax, num, text, x=0.0):
    ax.set_title(f"{num}  {text}", loc="left", fontsize=7.5, fontweight="bold", color=INK, pad=3)

BASE_H, CAP_H = 5.6, 2.2          # figure height for the panels, extra height reserved for the caption (inches)
H = BASE_H + CAP_H
def fy(y):                        # convert a y position from the old 5.6-inch layout to the taller figure
    return (y * BASE_H + CAP_H) / H

fig = plt.figure(figsize=(7.0, H))
top = fig.add_gridspec(1, 3, left=0.04, right=0.995, top=fy(0.925), bottom=fy(0.625),
                       width_ratios=[1, 0.85, 1.25], wspace=0.42)
bot = fig.add_gridspec(1, 4, left=0.075, right=0.995, top=fy(0.435), bottom=fy(0.115), wspace=0.7)

# ---------- A Data: raw diet matrix ----------
ax = fig.add_subplot(top[0])
M = raw.values
ax.imshow(np.sqrt(M), cmap="Greys", aspect="equal", interpolation="nearest")
imp = list(raw.index).index("Import")
ax.axvspan(imp - .5, imp + .5, color=ORANGE, alpha=0.45, lw=0)
ax.axhspan(imp - .5, imp + .5, color=ORANGE, alpha=0.45, lw=0)
ax.text(imp, -1.6, "Import", color=ORANGE, ha="center", va="bottom", fontsize=6.5)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(True); s.set_color(GRID)
ax.set_xlabel("predator", labelpad=2); ax.set_ylabel("prey", labelpad=2)
ax.text(0.5, -0.17, "44 × 44 diet matrix\n413 links, Web of Life FW_005", transform=ax.transAxes,
        ha="center", va="top", fontsize=6.5, color=INK2, linespacing=1.15)
title(ax, "A", "Data")

# ---------- B Clean ----------
ax = fig.add_subplot(top[1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
def box(y, h, lines, ec=INK2):
    ax.add_patch(FancyBboxPatch((0.05, y), 0.9, h, boxstyle="round,pad=0.01,rounding_size=0.03",
                                fc="white", ec=ec, lw=0.8))
    ax.text(0.5, y + h / 2, lines, ha="center", va="center", fontsize=6.8, linespacing=1.25)
box(0.72, 0.2, "44 groups\n413 links")
ax.add_patch(FancyArrowPatch((0.5, 0.71), (0.5, 0.52), arrowstyle="-|>", mutation_scale=7, color=INK2, lw=0.8))
ax.text(0.5, 0.615, "remove Import", ha="center", va="center", fontsize=6.5, color=ORANGE,
        bbox=dict(fc="white", ec="none", pad=1.2))
box(0.32, 0.2, "43 groups\n411 links")
ax.add_patch(FancyArrowPatch((0.5, 0.31), (0.5, 0.15), arrowstyle="-|>", mutation_scale=7, color=INK2, lw=0.8))
ax.text(0.5, 0.06, "directed, weighted\nprey → predator\nweight = diet share", ha="center", va="center",
        fontsize=6.5, color=INK2, linespacing=1.2)
title(ax, "B", "Clean")

# ---------- C Network (layout = same idea as the group's figure: y = trophic level) ----------
ax = fig.add_subplot(top[2])
names = list(traits.index)
y = traits["trophic_level"].to_dict()
rng = np.random.default_rng(4)
x = {n: rng.uniform(-1, 1) for n in names}
nb = {n: set() for n in names}
for p, q in zip(edges.prey, edges.predator):
    if p != q: nb[p].add(q); nb[q].add(p)
for _ in range(400):
    for n in names:
        pull = np.mean([x[m] for m in nb[n]])
        push = sum(np.sign(x[n] - x[m]) * 0.012 / (abs(x[n] - x[m]) + 0.05)
                   for m in names if m != n and abs(y[n] - y[m]) < 0.35)
        x[n] = 0.85 * x[n] + 0.15 * pull + push
xs = np.array(list(x.values())); x = {n: (x[n] - xs.min()) / (xs.max() - xs.min()) for n in names}
for p, q, w in zip(edges.prey, edges.predator, edges.diet_share):
    if p == q: continue
    ax.plot([x[p], x[q]], [y[p], y[q]], color=INK2, lw=0.15 + 2.2 * w, alpha=0.10 + 0.5 * w, zorder=1,
            solid_capstyle="round")
for cat, (c, mk) in CAT.items():
    ns = [n for n in names if traits.loc[n, "category"] == cat]
    ax.scatter([x[n] for n in ns], [y[n] for n in ns], s=14, color=c, marker=mk, zorder=3,
               edgecolor="white", linewidth=0.3, label=cat)
ax.set_ylabel("trophic level", labelpad=2); ax.set_xticks([])
ax.set_ylim(0.8, 5.0)
ax.grid(axis="y", color=GRID, lw=0.4); ax.set_axisbelow(True); ax.tick_params(length=2, pad=1.5)
ax.spines["bottom"].set_visible(False)
ax.legend(handles=[Line2D([], [], ls="", marker=mk, color=c, markersize=3.8, label=cat.replace("marine mammals, birds, turtles", "mammals, birds, turtles"))
                   for cat, (c, mk) in CAT.items()],
          loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2, frameon=False,
          handletextpad=0.2, columnspacing=0.8, fontsize=6.5)
title(ax, "C", "Network")


# ---------- Analyses (bottom row): D, E answer question 2 / rule; F, G are the removal results ----------
# D connectivity vs trophic level: Spearman rho of each measure with trophic level.
# Computed over the 40 CONSUMERS, not all 43 groups, to match
# output/cadiz_centrality_vs_tl.csv and the paper's figures 4-5. Detritus, Discard
# and Phytoplankton have no prey and sit at TL 1 by definition, so they are tied at
# the bottom of both rankings and are perfectly rank-concordant by construction:
# including them raises rho(n_prey) from +0.75 to +0.80 and flips rho(total_degree)
# from -0.07 to +0.10 without adding any information.
ax = fig.add_subplot(bot[0])
meas = [("n_prey", "prey\n(diet breadth)"), ("n_predators", "predators"),
        ("total_degree", "total links"), ("betweenness", "between-\nness")]
consumers = cent[cent.n_prey > 0]
assert len(consumers) == 40, f"expected 40 consumers, got {len(consumers)}"
res = [spearmanr(consumers.trophic_level, consumers[m]) for m, _ in meas]
rhos = [r[0] for r in res]; sig = [r[1] < 0.05 for r in res]
ypos = np.arange(len(meas))[::-1]
ax.axvline(0, color=INK2, lw=0.6)
ax.hlines(ypos, 0, rhos, color=GRID, lw=1.2)
ax.scatter(rhos, ypos, s=18, zorder=3, color=[BLUE if g else "white" for g in sig],
           edgecolor=[BLUE if g else GREY for g in sig], linewidth=0.8)
ax.set_yticks(ypos); ax.set_yticklabels([lab for _, lab in meas])
ax.set_xlabel("Spearman ρ with TL, n = 40 consumers", labelpad=2)
ax.set_xlim(-1, 1); ax.set_ylim(-0.6, len(meas) - 0.4)
ax.grid(axis="x", color=GRID, lw=0.4); ax.set_axisbelow(True); ax.tick_params(length=2, pad=1.5)
ax.text(0.03, 0.02, "open:\np ≥ 0.05", transform=ax.transAxes, ha="left", va="bottom",
        fontsize=6.5, color=INK2, linespacing=1.15)
title(ax, "D", "Links vs TL")
rho, rho_pred = rhos[0], rhos[1]

# E extinction rule schematic: before / after
ax = fig.add_subplot(bot[1]); ax.set_xlim(0, 2.75); ax.set_ylim(-0.3, 3.1); ax.axis("off")
nodes = {"P1": (0.30, 0.15), "P2": (0.90, 0.15), "C1": (0.30, 1.25), "C2": (0.90, 1.25), "T": (0.60, 2.35)}
links = [("P1", "C1"), ("P1", "C2"), ("P2", "C2"), ("C1", "T"), ("C2", "T")]
def draw(off, state):
    for a, b in links:
        (xa, ya), (xb, yb) = nodes[a], nodes[b]
        dead = state.get(a) in ("removed", "extinct")
        ax.add_patch(FancyArrowPatch((xa + off, ya + 0.1), (xb + off, yb - 0.12), arrowstyle="-|>", mutation_scale=5,
                                     color=GRID if dead else INK2, lw=0.8, shrinkA=0, shrinkB=0))
    for n, (nx_, ny_) in nodes.items():
        s = state.get(n, "alive")
        if s == "alive":
            ax.add_patch(Circle((nx_ + off, ny_), 0.12, fc=BLUE if n[0] == "P" else ORANGE, ec="white", lw=0.4, zorder=3))
        elif s == "removed":
            ax.add_patch(Circle((nx_ + off, ny_), 0.12, fc="white", ec=INK, lw=0.9, zorder=3))
            ax.plot([nx_ + off - .08, nx_ + off + .08], [ny_ - .08, ny_ + .08], color=INK, lw=0.9, zorder=4)
            ax.plot([nx_ + off - .08, nx_ + off + .08], [ny_ + .08, ny_ - .08], color=INK, lw=0.9, zorder=4)
        else:
            ax.add_patch(Circle((nx_ + off, ny_), 0.12, fc="white", ec=ORANGE, lw=0.9, ls=(0, (2, 1.2)), zorder=3))
draw(0.0, {})
draw(1.55, {"P1": "removed", "C1": "extinct"})
ax.add_patch(FancyArrowPatch((1.17, 1.25), (1.50, 1.25), arrowstyle="-|>", mutation_scale=8, color=INK, lw=1.0))
ax.text(0.45, 2.85, "before", ha="center", va="center", fontsize=6.5, color=INK2)
ax.text(2.0, 2.85, "after", ha="center", va="center", fontsize=6.5, color=INK2)
ax.text(1.35, -0.12, "× removed\ndashed = lost all prey", ha="center", va="top", fontsize=6.5, color=INK2, linespacing=1.15)
title(ax, "E", "Extinction rule")

# F guild removal: groups lost (beyond the removed ones) when a whole trophic role is removed
ax = fig.add_subplot(bot[2])
guild = pd.read_csv(REPO / "output/cadiz_guild_removal.csv").set_index("guild")
roles = [("primary producers (phytoplankton)", "phyto-\nplankton"), ("detritus and discards", "detritus,\ndiscards"),
         ("primary consumers (TL < 2.5)", "primary\nconsumers"), ("mid-level consumers (2.5 ≤ TL < 3.5)", "mid-level\nconsumers"),
         ("upper consumers (TL ≥ 3.5)", "upper\nconsumers"), ("top predators (no predators)", "top\npredators")]
ypos = np.arange(len(roles))[::-1]
all_prey = [guild.loc[g, "secondary_topological"] for g, _ in roles]    # rule: a consumer dies when ALL prey are gone
half_diet = [guild.loc[g, "secondary_weighted"] for g, _ in roles]      # rule: a consumer dies when HALF its diet is gone
ax.hlines(ypos, all_prey, half_diet, color=GRID, lw=1.2)
ax.scatter(half_diet, ypos, s=30, facecolor="white", edgecolor=BLUE, linewidth=0.8, zorder=3, label="half of diet lost")
ax.scatter(all_prey, ypos, s=14, color=BLUE, zorder=4, label="all prey lost")
ax.set_yticks(ypos); ax.set_yticklabels([lab for _, lab in roles])
ax.set_xlabel("groups lost after removal", labelpad=2)
ax.set_xlim(-2, 38); ax.set_ylim(-0.6, len(roles) - 0.4)
ax.grid(axis="x", color=GRID, lw=0.4); ax.set_axisbelow(True); ax.tick_params(length=2, pad=1.5)
ax.legend(loc="lower right", frameon=False, handletextpad=0.1, borderaxespad=0.1, labelspacing=0.2, fontsize=6.5)
title(ax, "F", "Role removal")

# G node-removal robustness
ax = fig.add_subplot(bot[3])
rule = "all prey lost"
sel = node_curves[node_curves.rule == rule]
series = [("random (mean of 1000)", "random", GREY, "-"),
          ("most connected first", "most links", BLUE, "-"),
          ("lowest trophic level first", "lowest TL", ORANGE, "-"),
          ("highest trophic level first", "highest TL", AQUA, "-")]
ax.plot([0, 1], [0, 1], color=GRID, lw=0.8, ls=(0, (3, 2)))
ax.axhline(0.5, color=GRID, lw=0.6)
for key, lab, col, ls in series:
    d = sel[sel.order == key]
    ax.plot(d.frac_removed, d.frac_lost, color=col, lw=1.2, ls=ls, label=lab)
ax.set_xlabel("groups removed", labelpad=2); ax.set_ylabel("groups lost", labelpad=2)
ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
ax.legend(loc="upper left", frameon=False, handlelength=0.8, handletextpad=0.3, labelspacing=0.15, borderaxespad=0.1, fontsize=6.5)
ax.text(0.02, 0.52, "50 % lost", fontsize=6.5, color=INK2, va="bottom")
ax.tick_params(length=2, pad=1.5); ax.set_axisbelow(True)
title(ax, "G", "Removal curves")

# stage-4 header
fig.text(0.04, fy(0.497), "Analyses", fontsize=7.5, fontweight="bold", ha="left", va="center")
fig.add_artist(Line2D([0.04, 0.995], [fy(0.477), fy(0.477)], transform=fig.transFigure, color=GRID, lw=0.8))
fig.canvas.draw()
inv = fig.transFigure.inverted()
def fpt(ax_, fx, fy):
    return inv.transform(ax_.transAxes.transform((fx, fy)))
ax1, ax2, ax3 = fig.axes[0], fig.axes[1], fig.axes[2]
def arrow(p0, p1):
    fig.add_artist(FancyArrowPatch(p0, p1, transform=fig.transFigure, arrowstyle="-|>",
                                   mutation_scale=9, color=INK, lw=1.1, shrinkA=0, shrinkB=0))
# 1 -> 2: from the matrix edge into the "44 groups" box
y_top = fpt(ax2, 0, 0.82)[1]
arrow((inv.transform((ax1.get_window_extent().x1, 0))[0] + 0.006, y_top), (fpt(ax2, 0.05, 0.82)[0] - 0.006, y_top))
# 2 -> 3: from the "43 groups" box to the network's axis label
y_bot = fpt(ax2, 0, 0.42)[1]
lab_left = inv.transform((ax3.yaxis.label.get_window_extent().x0, 0))[0]
arrow((fpt(ax2, 0.95, 0.42)[0] + 0.006, y_bot), (lab_left - 0.006, y_bot))
# caption (edit the text here; panel letters are bold through $\\mathbf{...}$)
CAPTION = (
    r"$\mathbf{(A)}$ The raw Gulf of Cadiz diet matrix (44×44), with columns representing predators and rows representing prey. "
    r"Darker cells indicate that a prey group makes up a larger proportion of a predator’s diet. "
    r"The “Import” row and column represent food sources originating outside the Gulf of Cadiz. "
    r"$\mathbf{(B)}$ The processed diet matrix after removing the “Import” row and column, leaving 43 functional groups and 411 feeding links. "
    r"$\mathbf{(C)}$ Network visualization of the processed food web, with each node representing a functional group and each edge representing a feeding relationship. "
    r"Edge thickness indicates the proportion of a predator’s diet contributed by its prey. "
    r"Nodes are arranged vertically by trophic level, with primary producers at the bottom and top predators near the top. "
    r"$\mathbf{(D)}$ Each row ranks the 40 consumer groups by trophic level and by one count of connections, and the dot shows how closely the two rankings match. The three basal groups are left out because they have no prey by definition. "
    r"Groups higher in the web eat more kinds of prey and have fewer predators, but these cancel out in total links and betweenness, showing no clear trend. "
    r"$\mathbf{(E)}$ Diagram showing the extinction rule: a consumer group will die out when it loses its prey. "
    r"$\mathbf{(F)}$ Effects of removing entire trophic roles from the food web. "
    r"Each row represents the removal of a trophic role, and the points indicate the number of additional groups that go extinct as a result. "
    r"Filled points represent groups that lose all their prey, while open points represent groups that lose at least half of their prey. "
    r"Removing lower trophic roles triggers extinction cascades, whereas removing upper trophic roles causes few or no additional extinctions. "
    r"$\mathbf{(G)}$ Each line removes groups one at a time, applies the extinction rule so that groups with no prey left also die, "
    r"and plots the share of the web lost against the share removed, so curves above the dashed diagonal mean cascades are happening. "
    r"Removing the lowest trophic levels first does the most damage, while removing the highest first causes no extra losses."
)
# the caption sits just under the bottom row; wrap=True breaks lines at the right edge of the figure
fig.text(0.04, (CAP_H + 0.115 * BASE_H - 0.55) / H, CAPTION, ha="left", va="top",
         fontsize=6.5, color=INK, linespacing=1.35, wrap=True)
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "explainer_figure.pdf", bbox_inches="tight", pad_inches=0.04, metadata={"CreationDate": None})
fig.savefig(OUT / "explainer_figure.png", dpi=300, bbox_inches="tight", pad_inches=0.04)
print("ok", f"rho(n_prey)={rho:.2f}", f"rho(n_pred)={rho_pred:.2f}")
