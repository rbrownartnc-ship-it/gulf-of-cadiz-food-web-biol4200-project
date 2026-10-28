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
assert raw.shape == (44, 44) and int((raw.values > 0).sum()) == 413
assert len(traits) == 43 and len(edges) == 411

def title(ax, num, text, x=0.0):
    ax.set_title(f"{num}  {text}", loc="left", fontsize=7.5, fontweight="bold", color=INK, pad=3, multialignment="left")

BASE_H, CAP_H = 3.2, 1.0          # figure height for the panels, extra height reserved for the caption (inches)
H = BASE_H + CAP_H
def fy(y):                        # convert a y position from the old 5.6-inch layout to the taller figure
    return (y * BASE_H + CAP_H) / H

fig = plt.figure(figsize=(7.0, H))
top = fig.add_gridspec(1, 4, left=0.04, right=0.995, top=fy(0.93), bottom=fy(0.40),
                       width_ratios=[1, 0.85, 1.25, 0.95], wspace=0.42)

# ---------- A Data: raw diet matrix ----------
ax = fig.add_subplot(top[0])
M = raw.values
ax.imshow(np.sqrt(M), cmap="Greys", aspect="equal", interpolation="nearest")
ax.set_anchor("N")   # keep the square matrix at the top of its slot so the title lines up with B, C and D
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
          loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=1, frameon=False,
          handletextpad=0.2, columnspacing=0.8, fontsize=6.5)
title(ax, "C", "Network")


# ---------- D Extinction rule (diagram only, no data) ----------
ax = fig.add_subplot(top[3]); ax.set_xlim(0, 2.75); ax.set_ylim(-0.3, 3.1); ax.axis("off")
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
title(ax, "D", "Extinction rule")

# arrows between the top-row panels (positions are measured from the drawn axes)
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
    r"$\mathbf{(D)}$ Diagram showing the extinction rule: a consumer group will die out when it loses its prey."
)
# the caption sits just under the panels; wrap=True breaks lines at the right edge of the figure
fig.text(0.04, (CAP_H + 0.40 * BASE_H - 0.85) / H, CAPTION, ha="left", va="top",
         fontsize=6.5, color=INK, linespacing=1.35, wrap=True)
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "explainer_figure.pdf", bbox_inches="tight", pad_inches=0.04, metadata={"CreationDate": None})
fig.savefig(OUT / "explainer_figure.png", dpi=300, bbox_inches="tight", pad_inches=0.04)
print("ok")
