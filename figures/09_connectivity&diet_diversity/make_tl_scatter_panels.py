"""Four-panel scatter figure: trophic level against four ways of measuring how connected a group is.
Reads only output/cadiz_node_traits.csv (read-only) and writes PDF + PNG into argv[2].

    python make_tl_scatter_panels.py <repo_root> <out_dir>
    e.g.  python code/make_tl_scatter_panels.py . figures/panels

Spearman rank correlation (rho) is computed across the 40 consumers (groups with at least one prey);
the three basal groups (Phytoplankton, Detritus, Discard) have no diet, so effective number of prey
is undefined for them and they are left out of every panel.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import spearmanr

REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

# ---------- style (same colours and minimum font size as the other figures) ----------
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e1e0d9"
BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#898781"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 7, "axes.labelsize": 7,
    "axes.titlesize": 7.5, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "legend.fontsize": 6.5, "text.color": INK, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.edgecolor": GRID,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})

# colour and marker for each group type (as in the repo's own scatter plots)
STYLE = {"invertebrates & plankton": (BLUE, "o"), "fishes": (ORANGE, "s"),
         "marine mammals, birds, turtles": (AQUA, "^")}

def lowess(x, y, frac=0.67, grid=100):
    """Local linear regression with tricube weights (LOWESS, no robustness iterations).
    Each fitted value uses the nearest frac*n points; this draws a smooth trend for the eye only."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    k = int(np.ceil(frac * len(x)))
    gx = np.linspace(x.min(), x.max(), grid)
    gy = np.empty(grid)
    for i, x0 in enumerate(gx):
        d = np.abs(x - x0); h = np.sort(d)[k - 1]
        w = (1 - (d / h) ** 3) ** 3 * (d < h) if h > 0 else (d == 0).astype(float)
        A = np.c_[np.ones_like(x), x - x0]
        beta = np.linalg.lstsq(A * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0]
        gy[i] = beta[0]
    return gx, gy

# ---------- data: the 40 consumers ----------
nodes = pd.read_csv(REPO / "output/cadiz_node_traits.csv", index_col=0)
cons = nodes[nodes.n_prey > 0]
assert len(cons) == 40 and cons.effective_prey.notna().all()

# (column, y-axis label, panel title, where to put the rho label)
panels = [("n_prey",         "number of prey",             "Number of prey",           "upper left"),
          ("effective_prey", "effective number\nof prey",  "Effective number of prey", "upper left"),
          ("n_predators",    "number of predators",        "Number of predators",      "upper right"),
          ("total_degree",   "total degree",               "Total degree",             "upper left")]

fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.3), sharex=True)
for ax, letter, (col, ylab, ttl, where) in zip(axes.flat, "ABCD", panels):
    for cat, (colour, marker) in STYLE.items():
        d = cons[cons.category == cat]
        ax.scatter(d.trophic_level, d[col], s=16, color=colour, marker=marker,
                   edgecolor="white", linewidth=0.3, zorder=3)
    gx, gy = lowess(cons.trophic_level, cons[col])
    ax.plot(gx, gy, color=INK, lw=1.3, zorder=4)          # smoother, for the eye only
    rho, p = spearmanr(cons.trophic_level, cons[col])
    ptxt = "p < 0.001" if p < 0.001 else f"p = {p:.2f}"
    x, ha = (0.03, "left") if where == "upper left" else (0.97, "right")
    ax.text(x, 0.96, f"Spearman ρ = {rho:+.2f}, {ptxt}".replace("-", "−"), transform=ax.transAxes,
            ha=ha, va="top", fontsize=6.5, color=INK2)
    ax.set_ylabel(ylab, labelpad=2)
    ax.set_title(f"{letter}  {ttl}", loc="left", fontsize=7.5, fontweight="bold", color=INK, pad=4)
    ax.grid(color=GRID, lw=0.4); ax.set_axisbelow(True); ax.tick_params(length=2, pad=1.5)
    ax.set_ylim(bottom=0)
for ax in axes[1]:
    ax.set_xlabel("trophic level", labelpad=2)

handles = [Line2D([], [], marker=m, color="none", markerfacecolor=c, markeredgecolor="white",
                  markersize=5.5, label=lab) for lab, (c, m) in STYLE.items()]
handles.append(Line2D([], [], color=INK, lw=1.3, label="trend"))
fig.legend(handles=handles, ncol=4, loc="lower center", frameon=False, handletextpad=0.2,
           columnspacing=1.6, bbox_to_anchor=(0.5, -0.01))
fig.tight_layout(rect=(0, 0.04, 1, 1), h_pad=1.2, w_pad=1.2)

fig.savefig(OUT / "tl_vs_connectivity.pdf", bbox_inches="tight", pad_inches=0.04, metadata={"CreationDate": None})
fig.savefig(OUT / "tl_vs_connectivity.png", dpi=300, bbox_inches="tight", pad_inches=0.04)
for col, *_ in panels:
    r, p = spearmanr(cons.trophic_level, cons[col])
    print(f"{col:15s} rho = {r:+.2f}  p = {p:.2g}  (n = {len(cons)})")
