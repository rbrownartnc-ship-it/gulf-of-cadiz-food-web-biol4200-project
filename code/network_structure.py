"""Structure of the Gulf of Cadiz food web, and how each group's position in it
relates to trophic level.

    python code/build_network.py        # first, to make output/
    python code/network_structure.py    # ~1-2 min (null models)

1. Whole-web measures: size, connectance, components (giant weak / strong),
   clustering (binary, weighted, directed), path length, assortativity,
   trophic coherence.
2. The same measures on three null models: random webs (Erdos-Renyi, same
   size and links), degree-preserving rewired webs (every group keeps its
   number of prey and predators), and the niche model (Williams & Martinez
   2000), the standard null for food webs.
3. Centralities for every group (degree, strength, betweenness, clustering,
   PageRank importance), each rank-correlated with trophic level.

Writes output/cadiz_global_structure.csv, cadiz_structure_vs_null.csv,
cadiz_centrality.csv, cadiz_centrality_vs_tl.csv, network_structure.txt,
the results workbook, and figures/cadiz_centrality_vs_tl and
figures/cadiz_degree_distributions (PDF + PNG).
"""
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import spearmanr
from foodweb import (OUT, SEED, NONLIVING, load_web, simple, food_web_properties,
                     prey_averaged_tl, niche_model, acceptable_niche_web, use_style,
                     pagerank_importance,
                     save, update_results_workbook, CATEGORY_STYLE, INK, INK2, GRID,
                     BLUE, ORANGE, GREY)

N_ER, N_SWAP, N_NICHE = 1000, 300, 1000
G, traits = load_web()
H = simple(G)                      # no cannibalism, no weights
U = H.to_undirected()
S, L = G.number_of_nodes(), G.number_of_edges()
report = []
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    report.append(line)

# ---------------------------------------------------------------- 1. whole web
def weighted_undirected(G):
    """Undirected web, weight = diet share summed over both directions."""
    W = nx.Graph()
    W.add_nodes_from(G)
    for u, v, d in G.edges(data=True):
        if u != v:
            w = W[u][v]["weight"] if W.has_edge(u, v) else 0
            W.add_edge(u, v, weight=w + d["d"])
    return W

W = weighted_undirected(G)
props = food_web_properties(G)
wccs = list(nx.weakly_connected_components(H))
sccs = list(nx.strongly_connected_components(H))
reach = sum(len(nx.descendants(H, n)) for n in H) / (S * (S - 1))
directed_lengths = [d for n, dd in nx.shortest_path_length(H) for m, d in dd.items() if m != n]
mutual_pairs = sorted({tuple(sorted((u, v))) for u, v in H.edges if H.has_edge(v, u)})

rows = [
    ("groups (nodes)", S, "functional groups, incl. Detritus and Discard"),
    ("living groups", S - len(NONLIVING), ""),
    ("links", L, "nonzero diet shares, incl. cannibalism"),
    ("cannibalistic self-loops", L - H.number_of_edges(), ""),
    ("connectance L/S^2", props["connectance"], "directed connectance"),
    ("link density L/S", props["link_density"], "mean number of prey (= mean number of predators)"),
    ("fraction basal", props["frac_basal"], "no prey"),
    ("fraction intermediate", props["frac_intermediate"], ""),
    ("fraction top", props["frac_top"], "no predators"),
    ("fraction cannibal", props["frac_cannibal"], ""),
    ("fraction omnivore", props["frac_omnivore"], "prey sit at different shortest-chain trophic levels"),
    ("weakly connected components", len(wccs), ""),
    ("largest weakly connected component", max(map(len, wccs)), "the giant component, ignoring direction"),
    ("strongly connected components", len(sccs), "incl. single groups"),
    ("largest strongly connected component", max(map(len, sccs)), "the largest feeding loop: every member can reach every other"),
    ("fraction of groups in feeding loops", props["frac_in_loops"], "in a strongly connected component larger than one"),
    ("mutual predation pairs", len(mutual_pairs), "A eats B and B eats A: " + "; ".join(f"{a} / {b}" for a, b in mutual_pairs)),
    ("fraction of links reciprocated", props["frac_mutual_links"], ""),
    ("directed reachability", reach, "fraction of ordered pairs (A, B) with a feeding path A -> ... -> B"),
    ("mean directed path length", float(np.mean(directed_lengths)), "over pairs connected by a feeding path"),
    ("characteristic path length (undirected)", props["path_length"], "mean shortest path, direction ignored"),
    ("diameter (undirected)", nx.diameter(U), ""),
    ("average clustering (undirected, binary)", props["clustering"], "mean local clustering coefficient"),
    ("transitivity (undirected, binary)", nx.transitivity(U), "3 x triangles / connected triples"),
    ("average clustering (undirected, weighted)", nx.average_clustering(W, weight="weight"),
     "Onnela et al. 2005 weighted clustering; weight = rescaled diet share"),
    ("average clustering (directed, binary)", nx.average_clustering(H),
     "Fagiolo 2007 directed clustering, all triangle types"),
    ("degree assortativity (undirected)", props["assortativity"], "Pearson r of degrees at either end of a link"),
    ("trophic coherence q", props["trophic_coherence_q"],
     "SD of trophic-level differences across links (Johnson et al. 2014); 0 = perfectly layered"),
    ("mean trophic level (weighted)", traits.trophic_level.mean(), "Ecopath-style, diet-weighted"),
    ("max trophic level (weighted)", traits.trophic_level.max(), traits.trophic_level.idxmax()),
    ("mean trophic level (unweighted)", props["mean_trophic_level"], "prey-averaged, ignoring diet shares"),
    ("generality SD (normalized)", props["generality_sd"], "SD of number of prey / (L/S)"),
    ("vulnerability SD (normalized)", props["vulnerability_sd"], "SD of number of predators / (L/S)"),
]
glob = pd.DataFrame(rows, columns=["measure", "value", "note"])
glob.to_csv(OUT / "cadiz_global_structure.csv", index=False)
log("== whole web ==")
for r in glob.itertuples():
    v = f"{r.value:.3f}" if isinstance(r.value, float) else r.value
    log(f"{r.measure:44s} {v}")

# ---------------------------------------------------------------- 2. null models
rng = np.random.default_rng(SEED)
def summarise(name, empirical, samples):
    df = pd.DataFrame(samples)
    out = []
    for m in df.columns:
        x = df[m].dropna()
        if len(x) < 0.9 * len(df) or pd.isna(empirical[m]):
            continue                      # undefined for most null webs (e.g. no basal species)
        sd = x.std()
        if sd < 1e-9:
            continue                      # fixed by construction (e.g. connectance)
        out.append(dict(null_model=name, measure=m, empirical=empirical[m],
                        null_mean=x.mean(), null_sd=sd,
                        z=(empirical[m] - x.mean()) / sd,
                        frac_null_below=(x < empirical[m]).mean(), n_webs=len(x)))
    return out

# ER and rewired webs have no cannibalism, so compare them with the web minus its self-loops.
emp_simple = food_web_properties(H)
er = []
for _ in range(N_ER):
    R = nx.gnm_random_graph(S, H.number_of_edges(), directed=True, seed=int(rng.integers(2**31)))
    er.append(food_web_properties(R))
swap = []
for _ in range(N_SWAP):
    R = H.copy()
    nx.directed_edge_swap(R, nswap=5 * R.number_of_edges(), max_tries=10**6,
                          seed=int(rng.integers(2**31)))
    swap.append(food_web_properties(R))
C = props["connectance"]
niche, tries = [], 0
while len(niche) < N_NICHE:
    tries += 1
    R = niche_model(S, C, rng)
    if acceptable_niche_web(R, C):
        niche.append(food_web_properties(R))
null = pd.DataFrame(summarise("random (ER)", emp_simple, er)
                    + summarise("degree-preserving", emp_simple, swap)
                    + summarise("niche model", props, niche))
null.to_csv(OUT / "cadiz_structure_vs_null.csv", index=False)
log(f"\n== vs null models == (ER {N_ER}, rewired {N_SWAP}, niche {N_NICHE} accepted of {tries})")
for r in null.itertuples():
    log(f"{r.null_model:18s} {r.measure:20s} emp {r.empirical:7.3f}  null {r.null_mean:7.3f} "
        f"± {r.null_sd:6.3f}  z {r.z:+6.2f}")

# ---------------------------------------------------------------- 3. centrality
# Weighted betweenness needs a distance: a strong link (large diet share) is a
# short hop, so distance = -ln(diet share).
for u, v, d in H.edges(data=True):
    d["dist"] = -np.log(G[u][v]["d"]) if G[u][v]["d"] > 0 else np.inf

cent = pd.DataFrame({
    "category": traits.category,
    "trophic_level": traits.trophic_level,
    "n_prey": traits.n_prey,
    "n_predators": traits.n_predators,
    "total_degree": traits.total_degree,
    "out_strength": traits.diet_share_sum,
    "betweenness": pd.Series(nx.betweenness_centrality(H)),
    "betweenness_weighted": pd.Series(nx.betweenness_centrality(H, weight="dist")),
    "clustering": pd.Series(nx.clustering(U)),
    "clustering_weighted": pd.Series(nx.clustering(W, weight="weight")),
    "clustering_directed": pd.Series(nx.clustering(H)),
    "pagerank_importance": pd.Series(pagerank_importance(H)),
})
cent.index.name = "group_name"
cent.round(5).to_csv(OUT / "cadiz_centrality.csv")

METRICS = [("n_prey", "number of prey (in-degree)"),
           ("n_predators", "number of predators (out-degree)"),
           ("total_degree", "total degree"),
           ("out_strength", "importance as prey (out-strength)"),
           ("betweenness", "betweenness"),
           ("betweenness_weighted", "betweenness (weighted)"),
           ("clustering", "clustering coefficient"),
           ("clustering_weighted", "clustering (weighted)"),
           ("clustering_directed", "clustering (directed)"),
           ("pagerank_importance", "PageRank importance")]
consumers = cent[cent.n_prey > 0]
corr = []
for m, label in METRICS:
    for subset, df in (("consumers", consumers), ("all groups", cent)):
        rho, p = spearmanr(df.trophic_level, df[m])
        corr.append(dict(measure=m, label=label, groups=subset, n=len(df), rho=rho, p=p))
corr = pd.DataFrame(corr)
corr.to_csv(OUT / "cadiz_centrality_vs_tl.csv", index=False)
log("\n== centrality vs trophic level (Spearman) ==")
for r in corr.itertuples():
    log(f"{r.label:36s} {r.groups:10s} n={r.n}  rho {r.rho:+.2f}  p {r.p:.2g}")
log("\ntop 5 by each centrality:")
for m, label in METRICS[3:]:
    log(f"  {label}: " + ", ".join(f"{n} ({v:.3g})" for n, v in cent[m].nlargest(5).items()))

(OUT / "network_structure.txt").write_text("\n".join(report) + "\n")
update_results_workbook()

# ---------------------------------------------------------------- figures
use_style()
legend_handles = [Line2D([], [], ls="", marker=mk, color=c, markersize=4.5, label=cat)
                  for cat, (c, mk) in CATEGORY_STYLE.items()]

# Centrality vs trophic level, one small panel per measure.
SHOW = ["n_prey", "n_predators", "total_degree", "out_strength",
        "betweenness_weighted", "clustering", "clustering_weighted", "pagerank_importance"]
SHORT = {"n_prey": "number of prey", "n_predators": "number of predators",
         "total_degree": "total degree", "out_strength": "importance as prey",
         "betweenness_weighted": "betweenness (weighted)", "clustering": "clustering",
         "clustering_weighted": "clustering (weighted)", "pagerank_importance": "PageRank importance"}
fig, axes = plt.subplots(2, 4, figsize=(7.0, 3.9), sharex=True)
for ax, m in zip(axes.flat, SHOW):
    for cat, (c, mk) in CATEGORY_STYLE.items():
        d = cent[cent.category == cat]
        ax.scatter(d.trophic_level, d[m], s=11, color=c, marker=mk,
                   edgecolor="white", linewidth=0.4, zorder=3)
    r = corr[(corr.measure == m) & (corr.groups == "consumers")].iloc[0]
    p = "p < 0.001" if r.p < 0.001 else f"p = {r.p:.2g}"
    ax.set_title(SHORT[m], loc="left", pad=11, color=INK)
    ax.text(0, 1.02, f"ρ = {r.rho:+.2f}, {p}".replace("-", "−"), transform=ax.transAxes,
            ha="left", va="bottom", fontsize=6.5, color=INK2)
    ax.grid(color=GRID, lw=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(length=2, pad=1.5)
for ax in axes[1]:
    ax.set_xlabel("trophic level")
fig.legend(handles=legend_handles, loc="lower center", ncol=4, frameon=False,
           bbox_to_anchor=(0.5, -0.06), handletextpad=0.2, columnspacing=1.2)
fig.text(0.5, -0.1, "ρ = Spearman rank correlation with trophic level across the 40 consumers "
         "(basal groups excluded)", ha="center", fontsize=6.5, color=INK2)
fig.tight_layout(h_pad=1.0, w_pad=0.8)
save(fig, "cadiz_centrality_vs_tl")

# Degree distributions, normalised by link density as in Camacho et al. (2002),
# against the exponential that random-assembly models predict.
fig, ax = plt.subplots(figsize=(3.4, 2.5))
x = np.linspace(0, 4, 100)
ax.plot(x, np.exp(-x), color=GREY, lw=1, ls=(0, (4, 2)), label="exponential, e$^{-x}$")
for col, label, c, mk in (("n_prey", "number of prey (generality)", BLUE, "o"),
                          ("n_predators", "number of predators (vulnerability)", ORANGE, "s")):
    k = np.sort(traits[col].to_numpy() / (L / S))
    ccdf = 1 - np.arange(len(k)) / len(k)
    ax.step(k, ccdf, where="post", color=c, lw=1.2)
    ax.plot(k, ccdf, ls="", marker=mk, ms=2.8, color=c, label=label)
ax.set_yscale("log")
ax.set_ylim(0.02, 1.1)
ax.set_xlabel("degree / link density (k / (L/S))")
ax.set_ylabel("fraction of groups with at least k")
ax.grid(color=GRID, lw=0.4)
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=1)
save(fig, "cadiz_degree_distributions")
