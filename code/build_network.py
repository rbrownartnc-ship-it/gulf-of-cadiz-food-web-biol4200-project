"""Gulf of Cadiz food web (Web of Life FW_005): clean, build, and profile a weighted directed predator-prey network.

Source: Torres et al. 2013, Ecological Modelling 265:26-44, via the Web of Life database (www.web-of-life.es). Run from anywhere:

    python code/build_network.py

Reads  data/cadiz_FW_005/diet_matrix.csv Writes output/  (culled matrix, cleaning log, node traits, edge list, GraphML)
       figures/01_web/ (diet matrix heatmap, food web drawn by trophic level)
"""
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, LinearSegmentedColormap, to_rgb
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from foodweb import draw_food_web

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "cadiz_FW_005"
OUT = ROOT / "output"
FIG = ROOT / "figures" / "01_web"
OUT.mkdir(exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

def log(*a):
    print(" ".join(str(x) for x in a))

cleaning = []
def record(action, target, detail, links_before, links_after):
    cleaning.append(dict(step=len(cleaning) + 1, action=action, target=target,
                         detail=detail, links_before=links_before,
                         links_after=links_after))

# ---------------------------------------------------------------- load
# diet_matrix.csv is a labeled 44x44 matrix. Rows are prey (resources), columns are predators (consumers), and each cell is the fraction of the column group's diet made up of the row group (Ecopath diet composition).
raw = pd.read_csv(RAW / "diet_matrix.csv", index_col=0)
assert raw.shape == (44, 44)
assert list(raw.index) == list(raw.columns), "row and column labels differ"
names = list(raw.index)
M = raw.to_numpy(dtype=float)
idx = {n: i for i, n in enumerate(names)}
L0 = int((M > 0).sum())

log("== raw ==")
log(f"groups: {len(names)}   links (nonzero cells): {L0}")

# every consumer's diet should sum to 1, which also confirms columns = predators
colsum = M.sum(axis=0)
consumers = [n for n in names if colsum[idx[n]] > 0]
dev = max(abs(colsum[idx[n]] - 1) for n in consumers)
assert dev < 0.01
log(f"consumers: {len(consumers)}   max |diet sum - 1| = {dev:.4f}")
record("check", "all consumer columns",
       f"{len(consumers)} consumer diets each sum to 1 (max deviation "
       f"{dev:.4f}), so rows = prey and columns = predators. No change.",
       L0, L0)
diet_total_original = dict(zip(names, colsum))

# ---------------------------------------------------------------- clean
# "Import" is not a functional group. In Ecopath it is the share of a predator's diet eaten outside the model area. The paper's model has 43 groups; Import is the 44th row (and an all-zero column: it eats nothing).
log("\n== cleaning ==")
imp = M[idx["Import"]]
import_share = {n: float(imp[idx[n]]) for n in names if imp[idx[n]] > 0}
for n, s in import_share.items():
    log(f"Import in diet of {n}: {s:.3f}")
assert M[:, idx["Import"]].sum() == 0
keep = [n for n in names if n != "Import"]
M = M[np.ix_([idx[n] for n in keep], [idx[n] for n in keep])]
names = keep
idx = {n: i for i, n in enumerate(names)}
L1 = int((M > 0).sum())
record("remove", "Import (row and column)",
       "Not a functional group: Ecopath's share of a predator's diet eaten "
       "outside the model area. Nonzero only as prey of "
       + ", ".join(f"{n} ({s:.3f})" for n, s in import_share.items())
       + ". Its column is all zero.", L0, L1)
log(f"dropped Import -> {len(names)} groups, {L1} links")

record("check", "exports / emigration",
       "Searched for any other row or column that is not a living or "
       "detrital group (e.g. export, emigration, fishery). None: Import was "
       "the only boundary flow in the matrix. Fishery catches and exports "
       "live in the paper's tables, not in the diet matrix.", L1, L1)
record("renormalize", "diets of " + " and ".join(import_share),
       "Without Import these diets sum to "
       + ", ".join(f"{1 - s:.3f}" for s in import_share.values())
       + ". For trophic level, omnivory index and diet diversity every diet is "
       "rescaled to sum to 1 (column diet_share_renorm in the edge list), which "
       "assumes food eaten outside the area has the same make-up as the local "
       "diet. The culled matrix keeps the original shares.", L1, L1)

NONLIVING = {"Detritus", "Discard"}
VERTEBRATES = {"Seabirds", "Killer whales", "Dolphins", "Loggerhead turtles"}
FISHES = {"Sharks", "Demersal piscivores", "Anglerfishes", "Skates",
          "Adult hake", "Juvenile hake", "Mackerels", "Horse mackerels",
          "Deep-sea fishes", "Large benthopelagic fishes",
          "Small benthopelagic fishes", "Flatfishes", "Demersal fishes",
          "Mullets", "Commercial sparids 1", "Commercial sparids 2",
          "Blue whiting", "Small demersal fishes", "Anchovy", "Sardine"}
def group(n):
    if n in NONLIVING:   return "non-living"
    if n in VERTEBRATES: return "marine mammals, birds, turtles"
    if n in FISHES:      return "fishes"
    return "invertebrates & plankton"
assert sum(group(n) == "invertebrates & plankton" for n in names) == 17

# ---------------------------------------------------------------- build
# Edge direction prey -> predator, i.e. the direction energy flows. Reverse the graph (G.reverse()) for the "who eats whom" convention.
G = nx.DiGraph()
for n in names:
    G.add_node(n, group=group(n))
for i, j in zip(*np.nonzero(M)):
    G.add_edge(names[i], names[j], weight=float(M[i, j]))

N, L = G.number_of_nodes(), G.number_of_edges()
loops = sorted(nx.nodes_with_selfloops(G))
log("\n== network ==")
log(f"nodes {N}   edges {L}   self-loops (cannibalism) {len(loops)}")
log("cannibals:", ", ".join(loops))
log(f"isolates: {list(nx.isolates(G)) or 'none'}")
log(f"weakly connected components: {nx.number_weakly_connected_components(G)}")
scc = max(nx.strongly_connected_components(G), key=len)
log(f"largest strongly connected component: {len(scc)} of {N}")
log(f"directed connectance L/N^2 = {L / N**2:.3f}   "
    f"(Web of Life's 0.437 uses L/(S(S-1)/2) with S=44)")

w = np.array([d["weight"] for *_, d in G.edges(data=True)])
log(f"weights: min {w.min():g}  median {np.median(w):.3f}  max {w.max():g}")
log(f"links < 0.01: {(w < 0.01).sum()}   < 0.001: {(w < 0.001).sum()}")

record("keep", "Detritus, Discard",
       "Non-living basal groups kept as nodes. Detritus is the most-eaten "
       "group in the web (summed diet share 5.13). Removing both leaves 41 nodes / 396 links, still one "
       "weakly connected component with no isolates.", L, L)
record("keep", f"{len(loops)} cannibalistic self-loops",
       "Kept in the matrix and the graph. Excluded when counting prey and "
       "predators (n_prey, n_predators) and from diet diversity.", L, L)
record("keep", "weak links",
       f"No weight threshold: smallest share {w.min():g}; "
       f"{(w < 0.01).sum()} links below 0.01 and {(w < 0.001).sum()} below "
       "0.001 are kept.", L, L)

# ---------------------------------------------------------------- nodes
# Trophic level, Ecopath style: TL_i = 1 + sum_j D_ji TL_j over prey j, with basal groups = 1 and D the diet matrix rescaled so every diet sums to 1.
D = M / np.where(M.sum(axis=0) > 0, M.sum(axis=0), 1)   # columns sum to 1
TL = np.linalg.solve(np.eye(N) - D.T, np.ones(N))

# Omnivory index (Christensen & Pauly 1992): diet-weighted variance of the prey trophic levels around TL_i - 1. Zero for a consumer feeding on one level.
OI = np.array([(D[:, i] * (TL - (TL[i] - 1)) ** 2).sum() for i in range(N)])

# Diet diversity: exp(Shannon entropy) of the diet without cannibalism, i.e. "how many equally used prey" the diet is equivalent to.
def effective_prey(i):
    p = np.delete(D[:, i], i)
    p = p[p > 0] / p[p > 0].sum() if p.sum() > 0 else p[p > 0]
    return float(np.exp(-(p * np.log(p)).sum())) if len(p) else np.nan

in_loop = set().union(*(c for c in nx.strongly_connected_components(G)
                        if len(c) > 1))
nodes = pd.DataFrame({
    "category": [group(n) for n in names],
    "living": [n not in NONLIVING for n in names],
    "trophic_level": TL.round(3),
    "omnivory_index": OI.round(3),
    # generality / vulnerability, not counting the self-loop
    "n_prey": [G.in_degree(n) - (n in loops) for n in names],
    "n_predators": [G.out_degree(n) - (n in loops) for n in names],
    "effective_prey": [round(effective_prey(i), 3) for i in range(N)],
    # out-strength: summed share of predator diets this group makes up
    "diet_share_sum": [round(G.out_degree(n, weight="weight"), 4) for n in names],
    "cannibal": [n in loops for n in names],
    "cannibalism_share": [float(M[i, i]) for i in range(N)],
    "import_share_removed": [import_share.get(n, 0.0) for n in names],
    "diet_total_original": [round(float(diet_total_original[n]), 4) for n in names],
    "in_feeding_loop": [n in in_loop for n in names],
}, index=pd.Index(names, name="group_name"))
nodes.insert(2, "role", np.select(
    [nodes.n_prey == 0, nodes.n_predators == 0],
    ["basal", "top predator"], "intermediate"))
nodes.insert(7, "total_degree", nodes.n_prey + nodes.n_predators)
nodes.loc[nodes.role == "basal", "effective_prey"] = np.nan

log("\nbasal:", ", ".join(nodes.index[nodes.role == "basal"]))
log("top predators (eaten by no other group):",
    ", ".join(nodes.index[nodes.role == "top predator"]))
log("\nmost prey groups (generalists):")
for n, r in nodes.nlargest(5, "n_prey").iterrows():
    log(f"  {n:28s} {r.n_prey}")
log("most predator groups:")
for n, r in nodes.nlargest(5, "n_predators").iterrows():
    log(f"  {n:28s} {r.n_predators}")
log("largest summed diet share (out-strength):")
for n, r in nodes.nlargest(5, "diet_share_sum").iterrows():
    log(f"  {n:28s} {r.diet_share_sum:.2f}")
log("highest trophic level:")
for n, r in nodes.nlargest(5, "trophic_level").iterrows():
    log(f"  {n:28s} {r.trophic_level:.2f}")
log(f"\ngroups in feeding loops (strongly connected, size > 1): {len(in_loop)}")

# How fragile is the web to the modeling choice of keeping detritus?
H = G.copy()
H.remove_nodes_from(NONLIVING)
log(f"\nwithout Detritus/Discard: {H.number_of_nodes()} nodes, "
    f"{H.number_of_edges()} edges, isolates {list(nx.isolates(H)) or 'none'}, "
    f"weak components {nx.number_weakly_connected_components(H)}")

# ---------------------------------------------------------------- save
culled = pd.DataFrame(M, index=pd.Index(names, name="prey \\ predator"),
                      columns=names)
edges = pd.DataFrame(
    [(u, v, d["weight"], D[idx[u], idx[v]]) for u, v, d in G.edges(data=True)],
    columns=["prey", "predator", "diet_share", "diet_share_renorm"])
edges["diet_share_renorm"] = edges["diet_share_renorm"].round(6)
edges = edges.sort_values(["predator", "diet_share"], ascending=[True, False])
log_df = pd.DataFrame(cleaning)

culled.to_csv(OUT / "cadiz_diet_matrix_culled.csv")
log_df.to_csv(OUT / "cadiz_cleaning_log.csv", index=False)
nodes.to_csv(OUT / "cadiz_node_traits.csv")
edges.to_csv(OUT / "cadiz_edges.csv", index=False)
for n in G:
    G.nodes[n]["trophic_level"] = float(nodes.at[n, "trophic_level"])
nx.write_graphml(G, OUT / "cadiz_food_web.graphml")


# ---------------------------------------------------------------- figures
# Both figures are drawn at the size they print in the paper: 7 in is the full text width of the two-column article template (a figure* float), and no text is smaller than 6.5 pt at that size. Each is saved twice: a vector PDF for LaTeX/Overleaf and a 300-dpi PNG for Word, Google Docs, slides and GitHub. Insert them at 7 in wide (\textwidth), as shrinking them further makes the labels unreadable.
WIDTH = 7.0
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e1e0d9"
GROUP_COLOR = {"invertebrates & plankton": "#2a78d6", "fishes": "#eb6834",
               "marine mammals, birds, turtles": "#1baf7a",
               "non-living": "#898781"}
plt.rcParams.update({"font.family": "sans-serif", "font.size": 8,
                     "axes.labelsize": 8, "xtick.labelsize": 7,
                     "ytick.labelsize": 7, "legend.fontsize": 7,
                     "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2,
                     "pdf.fonttype": 42})     # editable, embedded TrueType text

def save(fig, stem):
    fig.savefig(FIG / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.04,
                metadata={"CreationDate": None})          # reproducible bytes
    fig.savefig(FIG / f"{stem}.png", dpi=300, bbox_inches="tight",
                pad_inches=0.04)
    plt.close(fig)

group_handles = [Line2D([], [], marker="s", ls="", color=c, markersize=6, label=g)
                 for g, c in GROUP_COLOR.items()]

# 1. Diet matrix, both axes ordered by trophic level. Group identity sits in a color strip beside each axis so the labels can stay in ink.
order = list(nodes.sort_values("trophic_level").index)
A = M[np.ix_([idx[n] for n in order], [idx[n] for n in order])]
cmap = LinearSegmentedColormap.from_list(
    "blue", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
strip = np.array([[to_rgb(GROUP_COLOR[group(n)])] for n in order])

fig, ax = plt.subplots(figsize=(WIDTH - 0.25, 7.9))  # tight crop lands at 7 in
im = ax.imshow(np.ma.masked_equal(A, 0), cmap=cmap,
               norm=LogNorm(vmin=1e-4, vmax=1), interpolation="none")
div = make_axes_locatable(ax)
sl = div.append_axes("left", size="1.8%", pad=0.03, sharey=ax)
sb = div.append_axes("bottom", size="1.8%", pad=0.03, sharex=ax)
sl.imshow(strip, aspect="auto", interpolation="none")
sb.imshow(strip.transpose(1, 0, 2), aspect="auto", interpolation="none")
sl.set_yticks(range(N), order, fontsize=6.5)
sl.set_xticks([])
sb.set_xticks(range(N), order, rotation=90, fontsize=6.5)
sb.set_yticks([])
sl.set_ylabel("prey (resource)")
sb.set_xlabel("predator (consumer)")
ax.tick_params(labelleft=False, labelbottom=False, left=False, bottom=False)
for a in (sl, sb):
    a.tick_params(length=0, pad=2)
    for sp in a.spines.values():
        sp.set_visible(False)
ax.set_xticks(np.arange(-.5, N), minor=True)
ax.set_yticks(np.arange(-.5, N), minor=True)
ax.grid(which="minor", color=GRID, lw=0.3)
ax.tick_params(which="minor", length=0)
for sp in ax.spines.values():
    sp.set_color(GRID)
for k, n in enumerate(order):               # outline cannibalism cells
    if n in loops:
        ax.add_patch(Rectangle((k - .5, k - .5), 1, 1, fill=False,
                               edgecolor=INK, lw=0.7))
cax = div.append_axes("right", size="2.2%", pad=0.12)
cb = fig.colorbar(im, cax=cax)
cb.set_label("share of predator's diet (log scale; values below 0.0001 drawn at the floor)",
             fontsize=7)
cb.set_ticks([1e-4, 1e-3, 1e-2, 1e-1, 1], labels=["0.0001", "0.001", "0.01", "0.1", "1"])
cb.ax.minorticks_off()
cb.ax.tick_params(labelsize=7)
cb.outline.set_visible(False)
handles = group_handles + [Line2D([], [], marker="s", ls="", markersize=6.5,
                                  markerfacecolor="none", markeredgecolor=INK,
                                  label="cannibalism (diagonal)")]
fig.subplots_adjust(left=0.2, right=0.92, top=0.995, bottom=0.235)
fig.canvas.draw()                           # hang the legend just under the axis title
title_bottom = sb.xaxis.label.get_window_extent().y0 / fig.bbox.height
fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False,
           handletextpad=0.3, columnspacing=1.2,
           bbox_to_anchor=(0.5, title_bottom - 0.008))
save(fig, "diet_matrix")

# 2. Food web drawn by trophic level (foodweb.draw_food_web, shared with compare_webs.py).
draw_food_web(G, {n: TL[idx[n]] for n in G}, {n: GROUP_COLOR[group(n)] for n in G},
              list(GROUP_COLOR.items()), FIG / "food_web")
