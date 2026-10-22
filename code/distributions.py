"""Distributions of node and link properties in the Gulf of Cadiz food web.

    python code/build_network.py     # first, to make output/
    python code/distributions.py     # ~5 s

One histogram per property, each its own figure in figures/02_distributions/:
number of prey, number of predators and total degree (each against the
random-web expectation), the cumulative degree distribution, link strength
(diet share), importance as prey, trophic level, clustering, betweenness,
omnivory index, and diet diversity.

Writes output/cadiz_distribution_stats.csv and the results workbook.
"""
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.stats import binom, skew
from foodweb import (OUT, load_web, simple, use_style, save, tidy, plain_log_ticks,
                     update_results_workbook, COLUMN, INK2, BLUE, ORANGE, GREY)

FOLDER = "02_distributions"
G, traits = load_web()
H = simple(G)
S, L = H.number_of_nodes(), H.number_of_edges()     # without cannibalism
p_er = L / (S * (S - 1))                              # link probability of a random web
U = H.to_undirected()
nodes = traits.copy()
nodes["clustering"] = pd.Series(nx.clustering(U))
nodes["betweenness"] = pd.Series(nx.betweenness_centrality(H))
links = pd.read_csv(OUT / "cadiz_edges.csv")
links = links[links.prey != links.predator]

# ---------------------------------------------------------------- statistics
ER = {"n_prey": (S - 1, p_er), "n_predators": (S - 1, p_er), "total_degree": (2 * (S - 1), p_er)}
SPECS = [  # (column, label, table)
    ("n_prey", "number of prey (in-degree)", nodes),
    ("n_predators", "number of predators (out-degree)", nodes),
    ("total_degree", "total degree", nodes),
    ("diet_share_sum", "importance as prey (out-strength)", nodes),
    ("trophic_level", "trophic level", nodes),
    ("clustering", "clustering coefficient", nodes),
    ("betweenness", "betweenness", nodes),
    ("omnivory_index", "omnivory index", nodes),
    ("effective_prey", "diet diversity (effective number of prey)", nodes),
    ("diet_share_renorm", "link strength (share of predator's diet)", links),
]
rows = []
for col, label, df in SPECS:
    x = df[col].dropna().to_numpy(float)
    row = dict(measure=col, label=label, level="link" if df is links else "group",
               n=len(x), mean=x.mean(), median=np.median(x), sd=x.std(ddof=1),
               min=x.min(), max=x.max(), skewness=skew(x),
               dispersion_var_over_mean=x.var(ddof=1) / x.mean() if x.mean() else np.nan)
    if col in ER:
        n, p = ER[col]
        row.update(random_web_mean=n * p, random_web_var_over_mean=1 - p)
    rows.append(row)
stats = pd.DataFrame(rows)
stats.round(4).to_csv(OUT / "cadiz_distribution_stats.csv", index=False)
print(stats[["measure", "n", "mean", "median", "sd", "max", "skewness",
             "dispersion_var_over_mean"]].round(3).to_string(index=False))
update_results_workbook()

# ---------------------------------------------------------------- figures
use_style()

def histogram(stem, x, bins, xlabel, ylabel="number of groups", er=None, logx=False):
    fig, ax = plt.subplots(figsize=(COLUMN, 2.3))
    ax.hist(x, bins=bins, color=BLUE, edgecolor="white", linewidth=0.6, zorder=2)
    handles = []
    if er is not None:                        # expected number of groups in each bin
        n, p = er
        k = np.arange(0, n + 1)
        pmf = binom.pmf(k, n, p)
        expected = [S * pmf[(k >= lo) & (k < hi)].sum() for lo, hi in zip(bins[:-1], bins[1:])]
        ax.plot((bins[:-1] + bins[1:]) / 2, expected, color=INK2, lw=1.1,
                ls=(0, (3, 1.5)), marker="o", ms=2, zorder=3)
        handles = [Patch(color=BLUE, label="Gulf of Cadiz web"),
                   Line2D([], [], color=INK2, lw=1.1, ls=(0, (3, 1.5)), marker="o", ms=2,
                          label="random web, same size and links (expected)")]
    if logx:
        ax.set_xscale("log")
        plain_log_ticks(ax.xaxis)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    tidy(ax, "y")
    if handles:
        ax.legend(handles=handles, frameon=False, loc="upper center",
                  bbox_to_anchor=(0.5, -0.24), ncol=1)
    save(fig, FOLDER, stem)

histogram("number_of_prey_histogram", nodes.n_prey, np.arange(-0.5, nodes.n_prey.max() + 1.5),
          "number of prey (in-degree)", er=ER["n_prey"])
histogram("number_of_predators_histogram", nodes.n_predators,
          np.arange(-0.5, nodes.n_predators.max() + 1.5), "number of predators (out-degree)",
          er=ER["n_predators"])
histogram("total_degree_histogram", nodes.total_degree, np.arange(-0.5, nodes.total_degree.max() + 2, 2),
          "total degree (prey + predators)", er=ER["total_degree"])
histogram("link_strength_histogram", links.diet_share_renorm, np.logspace(-6, 0, 25),
          "link strength (share of predator's diet, log scale)", ylabel="number of links", logx=True)
histogram("importance_as_prey_histogram", nodes.diet_share_sum, np.arange(0, 5.5, 0.25),
          "importance as prey (summed share of predators' diets)")
histogram("trophic_level_histogram", nodes.trophic_level, np.arange(1, 5.01, 0.25), "trophic level")
histogram("clustering_histogram", nodes.clustering, np.arange(0, 1.001, 0.05), "clustering coefficient")
histogram("betweenness_histogram", nodes.betweenness, np.arange(0, 0.2001, 0.01), "betweenness (directed)")
histogram("omnivory_index_histogram", nodes.omnivory_index, np.arange(0, 1.41, 0.05), "omnivory index")
histogram("diet_diversity_histogram", nodes.effective_prey.dropna(), np.arange(0.5, 14.5, 1),
          "diet diversity (effective number of prey)", ylabel="number of consumers")

# Cumulative degree distributions, normalised by link density as in Camacho et
# al. (2002), against the exponential that random-assembly models predict.
Lall = G.number_of_edges()
fig, ax = plt.subplots(figsize=(COLUMN, 2.5))
x = np.linspace(0, 4, 100)
ax.plot(x, np.exp(-x), color=GREY, lw=1, ls=(0, (4, 2)), label="exponential, exp(−x)")
for col, label, c, mk in (("n_prey", "number of prey (generality)", BLUE, "o"),
                          ("n_predators", "number of predators (vulnerability)", ORANGE, "s")):
    k = np.sort(traits[col].to_numpy() / (Lall / S))
    ccdf = 1 - np.arange(len(k)) / len(k)
    ax.step(k, ccdf, where="post", color=c, lw=1.2)
    ax.plot(k, ccdf, ls="", marker=mk, ms=2.8, color=c, label=label)
ax.set_yscale("log")
ax.set_ylim(0.02, 1.1)
plain_log_ticks(ax.yaxis)
ax.set_xlabel("degree / link density (k / (L/S))")
ax.set_ylabel("fraction of groups with at least k")
tidy(ax)
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=1)
save(fig, FOLDER, "degree_cumulative_distribution")
