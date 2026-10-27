"""What happens to the Gulf of Cadiz food web when feeding links (edges) are cut.

    python code/build_network.py     # first, to make output/
    python code/edge_removal.py      # ~2 min

A cut link is a feeding interaction that stops (the predator no longer eats
that prey), while both groups survive the cut itself. The same extinction
rules as node_removal.py then apply: a consumer starves once its remaining
links carry no more than (1 - theta) of its diet; theta = 1 is "all prey
lost", 0.5 is "half of diet lost". Cannibalistic self-loops are left alone.

1. Single-link knockouts: cut each of the 397 links on its own. Which single
   interactions does the web depend on? Also edge betweenness and bridges.
2. Link-removal sequences: cut links one after another (random x500,
   strongest first, weakest first, highest edge betweenness first (static and
   recalculated, Girvan & Newman 2002 / Holme et al. 2002), links from the
   lowest-trophic-level prey first (bottom-up), links into the
   highest-trophic-level predators first (top-down)). L50 = fraction of links
   cut before half of all living groups are lost.
3. Giant component while links are cut, with and without starvation (bond
   percolation).

Writes output/cadiz_link_knockouts.csv, cadiz_link_robustness_summary.csv,
cadiz_link_robustness_curves.csv, edge_removal.txt and the results workbook.
Figures (one per idea, PDF + PNG) in figures/06_edge_removal/.
"""
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.stats import spearmanr
from foodweb import (OUT, SEED, load_web, simple, Cascade, LinkRemoval, largest_wcc,
                     use_style, save, tidy, wrap_label, plain_log_ticks, update_results_workbook,
                     COLUMN, INK, INK2,
                     GRID, BLUE, ORANGE, GREY)

FOLDER = "06_edge_removal"
N_RANDOM = 500
CHECK_EVERY = 10                       # giant component measured every 10 cuts in random runs
G, traits = load_web()
H = simple(G)
cas = Cascade(G)
S = G.number_of_nodes()
LIVING = sorted(n for n in G if G.nodes[n]["living"])
S_LIV = len(LIVING)
LINKS = sorted((p, n) for n, d in cas.diet.items() for p in d)
NL = len(LINKS)
share = {(p, n): cas.diet[n][p] for p, n in LINKS}
tl = traits.trophic_level
RULES = [(1.0, "all prey lost"), (0.5, "half of diet lost")]
SENSITIVITY = [(1.0, "all prey lost"), (0.75, "3/4 of diet lost"),
               (0.5, "half of diet lost"), (0.25, "1/4 of diet lost")]
report = []
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    report.append(line)

# ---------------------------------------------------------------- 1. single links
ebw = nx.edge_betweenness_centrality(H)
bridges = {tuple(sorted(e)) for e in nx.bridges(H.to_undirected())}
rows = []
for p, n in LINKS:
    row = dict(prey=p, predator=n, diet_share=share[(p, n)],
               prey_trophic_level=tl[p], predator_trophic_level=tl[n],
               predator_n_prey=len(cas.diet[n]), edge_betweenness=ebw[(p, n)],
               only_prey_of_predator=len(cas.diet[n]) == 1,
               bridge=tuple(sorted((p, n))) in bridges)
    for theta, label in RULES:
        present, sec = cas.run([], theta, removed_links=[(p, n)])
        key = "topological" if theta == 1 else "weighted"
        row[f"secondary_{key}"] = len(sec)
        row[f"secondary_{key}_groups"] = "; ".join(sorted(sec))
    rows.append(row)
lk = pd.DataFrame(rows).sort_values(["secondary_weighted", "secondary_topological", "diet_share"],
                                    ascending=False)
# What the rules imply, checked: under "all prey lost" a single cut kills the
# predator only if it was its sole prey link; under "half" only if the link
# left no more than half of the (non-cannibal) diet.
kills_t = lk[lk.secondary_topological > 0]
assert (kills_t.only_prey_of_predator).all() and lk[lk.only_prey_of_predator].secondary_topological.gt(0).all()
kills_w = lk[lk.secondary_weighted > 0]
left_after = lk.predator.map(lambda n: sum(cas.diet[n].values())) - lk.diet_share   # cannibalism excluded
assert set(kills_w.index) == set(lk.index[left_after <= 0.5 + 1e-12])
lk.round(5).to_csv(OUT / "cadiz_link_knockouts.csv", index=False)
log("== single-link knockouts ==")
log(f"feeding links (no cannibalism): {NL}")
log(f"links whose loss alone causes >= 1 extinction: {len(kills_t)} (all prey lost), "
    f"{len(kills_w)} (half of diet lost)")
for r in kills_w.head(12).itertuples():
    log(f"  {r.prey:26s} -> {r.predator:26s} share {r.diet_share:.2f}  lost: all-prey "
        f"{r.secondary_topological:2d} | half-diet {r.secondary_weighted:2d}")
log(f"bridges (cutting the link splits the web): {lk.bridge.sum()}")
rho, pv = spearmanr(lk.edge_betweenness, lk.diet_share)
log(f"edge betweenness vs link strength: Spearman rho {rho:+.2f}, p {pv:.2g}")
top_ebw = lk.nlargest(5, "edge_betweenness")
log("highest edge betweenness: " + "; ".join(f"{r.prey} -> {r.predator} ({r.edge_betweenness:.3f})"
                                             for r in top_ebw.itertuples()))

# ---------------------------------------------------------------- 2. sequences
def ranked(key):
    return sorted(LINKS, key=key)

def recalculated_betweenness(state):
    """Next cut: the surviving link with the highest edge betweenness on the surviving web."""
    W = state.graph(G)
    e = nx.edge_betweenness_centrality(W)
    return min(e, key=lambda l: (-e[l], l)) if e else None

ORDERS = {
    "strongest links first": ranked(lambda l: (-share[l], l)),
    "weakest links first": ranked(lambda l: (share[l], l)),
    "highest edge betweenness first": ranked(lambda l: (-ebw[l], l)),
    "highest edge betweenness first (recalculated)": recalculated_betweenness,
    "links from lowest-trophic-level prey first": ranked(lambda l: (tl[l[0]], -share[l], l)),
    "links into highest-trophic-level predators first": ranked(lambda l: (-tl[l[1]], -share[l], l)),
}

def sequence(order, theta, every=1):
    """Cut links in `order` (a list, or a chooser called on the current
    state). Links already gone because one end starved are skipped and not
    counted as cuts. Returns one row per cut; the giant component is measured
    every `every` cuts (nan in between)."""
    st = LinkRemoval(cas, theta)
    rows = [dict(cut=0, frac_lost=0.0, n_alive=S, lwcc=S)]
    k, i = 0, 0
    while True:
        if callable(order):
            link = order(st)
            if link is None:
                break
        else:
            # skip links that are already gone because an end starved
            while i < len(order) and not (order[i][0] in st.alive and order[i][1] in st.alive):
                i += 1
            if i >= len(order):
                break
            link = order[i]
            i += 1
        st.remove_link(*link)
        k += 1
        measure = k % every == 0 or k == NL
        rows.append(dict(cut=k, frac_lost=sum(1 for m in LIVING if m not in st.alive) / S_LIV,
                         n_alive=len(st.alive),
                         lwcc=largest_wcc(st.graph(G), st.alive) if measure else np.nan))
        if callable(order) and not any(l for l in st.links if l[0] in st.alive and l[1] in st.alive):
            break
    return pd.DataFrame(rows)

def l50(curve):
    hit = curve[curve.frac_lost >= 0.5]
    return hit.cut.iloc[0] / NL if len(hit) else np.nan

def first_split(curve):
    c = curve.dropna(subset=["lwcc"])
    split = c[c.lwcc < c.n_alive]
    return split.cut.iloc[0] / NL if len(split) else np.nan

rng = np.random.default_rng(SEED)
random_orders = [[LINKS[i] for i in rng.permutation(NL)] for _ in range(N_RANDOM)]
grid = np.arange(NL + 1)
curves, summary, split_random = [], [], {}
for theta, label in SENSITIVITY + [(None, "no starvation (links cut only)")]:
    keep_curve = label in dict(RULES).values() or theta is None
    rand = [sequence(o, theta, every=CHECK_EVERY if keep_curve else NL + 1) for o in random_orders]
    lost = np.array([c.set_index("cut").frac_lost.reindex(grid).ffill().to_numpy() for c in rand])
    l50_rand = np.array([l50(c) for c in rand])
    if keep_curve:
        split_random[label] = np.array([first_split(c) for c in rand])
        lw = np.array([c.set_index("cut").lwcc.reindex(grid).to_numpy() for c in rand])
        curves.append(pd.DataFrame(dict(
            order=f"random (mean of {N_RANDOM})", rule=label, cut=grid, frac_cut=grid / NL,
            frac_lost=lost.mean(0), frac_lost_lo=np.percentile(lost, 2.5, 0),
            frac_lost_hi=np.percentile(lost, 97.5, 0),
            lwcc_frac=np.nanmean(lw, 0) / S if np.isfinite(lw).any() else np.nan,
            lwcc_frac_lo=np.nanpercentile(lw, 2.5, 0) / S, lwcc_frac_hi=np.nanpercentile(lw, 97.5, 0) / S)))
    if theta is not None:
        summary.append(dict(order="random", rule=label, L50=np.nanmean(l50_rand),
                            random_L50_lo=np.nanpercentile(l50_rand, 2.5),
                            random_L50_hi=np.nanpercentile(l50_rand, 97.5), frac_random_below=np.nan))
    for name, order in ORDERS.items():
        c = sequence(order, theta, every=1 if keep_curve else NL + 1)
        if keep_curve:
            curves.append(pd.DataFrame(dict(order=name, rule=label, cut=c.cut, frac_cut=c.cut / NL,
                                            frac_lost=c.frac_lost, lwcc_frac=c.lwcc / S,
                                            lwcc_of_alive=c.lwcc / c.n_alive)))
            if theta is None or theta == 1.0:
                split_random.setdefault((label, name), first_split(c))
        if theta is not None:
            v = l50(c)
            summary.append(dict(order=name, rule=label, L50=v, random_L50_lo=np.nan,
                                random_L50_hi=np.nan, frac_random_below=(l50_rand < v).mean()))
curves = pd.concat(curves, ignore_index=True)
summary = pd.DataFrame(summary)
curves.round(5).to_csv(OUT / "cadiz_link_robustness_curves.csv", index=False)
summary.round(4).to_csv(OUT / "cadiz_link_robustness_summary.csv", index=False)
log("\n== link-removal sequences: L50 (fraction of links cut before half of living groups are lost) ==")
for r in summary.itertuples():
    extra = (f"  random 95% range {r.random_L50_lo:.3f}-{r.random_L50_hi:.3f}" if r.order == "random"
             else f"  ({r.frac_random_below:.0%} of random orders lower)")
    log(f"  {r.rule:18s} {r.order:48s} L50 {r.L50:.3f}{extra}")
frag = []
for rule in ["no starvation (links cut only)", "all prey lost", "half of diet lost"]:
    x = split_random[rule]
    frag.append(dict(rule=rule, order="random", first_split=np.nanmedian(x),
                     random_lo=np.nanpercentile(x, 2.5), random_hi=np.nanpercentile(x, 97.5)))
    for name in ORDERS:
        if (rule, name) in split_random:
            frag.append(dict(rule=rule, order=name, first_split=split_random[(rule, name)],
                             random_lo=np.nan, random_hi=np.nan))
pd.DataFrame(frag).round(4).to_csv(OUT / "cadiz_link_fragmentation.csv", index=False)
log("\n== giant component: when does the surviving web first break into pieces? ==")
log("   (fraction of links cut; random = median and 95% range)")
for rule in ["no starvation (links cut only)", "all prey lost", "half of diet lost"]:
    x = split_random[rule]
    log(f"  {rule:30s} random {np.nanmedian(x):.2f} ({np.nanpercentile(x, 2.5):.2f}-"
        f"{np.nanpercentile(x, 97.5):.2f})")
    for name in ORDERS:
        if (rule, name) in split_random:
            v = split_random[(rule, name)]
            log(f"  {rule:30s} {name:48s} {'never' if np.isnan(v) else f'{v:.2f}'}")

(OUT / "edge_removal.txt").write_text("\n".join(report) + "\n")
update_results_workbook()

# ---------------------------------------------------------------- figures
use_style()
DASH = (0, (4, 1.5))
RULE_COLOR = {"all prey lost": BLUE, "half of diet lost": ORANGE}

# Critical single links: those whose loss alone causes any extinction.
crit = kills_w.head(15).iloc[::-1]
fig, ax = plt.subplots(figsize=(COLUMN, 0.36 * len(crit) + 0.9))
y = np.arange(len(crit))
for off, key, rule in ((0.19, "topological", "all prey lost"), (-0.19, "weighted", "half of diet lost")):
    v = crit[f"secondary_{key}"].to_numpy()
    ax.barh(y + off, v, height=0.36, color=RULE_COLOR[rule], edgecolor="white", lw=0.5)
    for yi, vi in zip(y + off, v):
        ax.text(vi + 0.3, yi, str(vi), va="center", fontsize=6.5, color=INK2)
ax.set_yticks(y, [f"{r.prey} →\n{r.predator} ({r.diet_share:.2f})" for r in crit.itertuples()], fontsize=6.5)
ax.set_xlabel("secondary extinctions after cutting this one link")
tidy(ax, "x")
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
gap = 0.42 / (fig.get_figheight() * 0.77)              # 0.42 in below the axes
ax.legend(handles=[Patch(color=BLUE, label="consumer dies when all its prey are gone"),
                   Patch(color=ORANGE, label="consumer dies when half its diet is gone")],
          loc="upper center", bbox_to_anchor=(0.3, -gap), frameon=False)
save(fig, FOLDER, "critical_single_links")

# Are central links strong links?
fig, ax = plt.subplots(figsize=(COLUMN, 2.4))
ax.scatter(lk.diet_share, lk.edge_betweenness, s=8, color=BLUE, alpha=0.7, edgecolor="white", lw=0.3)
ax.set_xscale("log")
plain_log_ticks(ax.xaxis)
ax.set_xlabel("link strength (share of predator's diet, log scale)")
ax.set_ylabel("edge betweenness")
ax.text(0, 1.02, f"Spearman ρ = {rho:+.2f}, p = {pv:.2g} ({NL} links)".replace("-", "−"),
        transform=ax.transAxes, fontsize=6.5, color=INK2)
tidy(ax)
save(fig, FOLDER, "edge_betweenness_vs_link_strength")

# One robustness chart per pair of link-removal orders and rule.
PAIRS = [("strength", "strongest links first", "weakest links first"),
         ("betweenness", "highest edge betweenness first", "highest edge betweenness first (recalculated)"),
         ("trophic_position", "links from lowest-trophic-level prey first",
          "links into highest-trophic-level predators first")]
for theta, rule in RULES:
    cr = curves[curves.rule == rule]
    rnd = cr[cr.order.str.startswith("random")]
    r = summary[summary.rule == rule].set_index("order").L50
    for tag, o1, o2 in PAIRS:
        fig, ax = plt.subplots(figsize=(COLUMN, 2.5))
        ax.axhline(0.5, color=GRID, lw=0.6)
        ax.fill_between(rnd.frac_cut, rnd.frac_lost_lo, rnd.frac_lost_hi, color=GREY, alpha=0.25, lw=0)
        ax.plot(rnd.frac_cut, rnd.frac_lost, color=GREY, lw=1.2)
        for o, c, ls in ((o1, BLUE, "-"), (o2, ORANGE, DASH)):
            d = cr[cr.order == o]
            ax.plot(d.frac_cut, d.frac_lost, color=c, lw=1.4, ls=ls)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.02)
        ax.set_xlabel("fraction of feeding links cut")
        ax.set_ylabel("fraction of living groups lost")
        ax.text(0, 1.03, f"rule: {rule}", transform=ax.transAxes, fontsize=6.5, color=INK2)
        tidy(ax)
        fmt = lambda v: "never" if np.isnan(v) else f"{v:.2f}"
        ax.legend(handles=[Line2D([], [], color=BLUE, lw=1.4, label=f"{o1}  (L50 {fmt(r[o1])})"),
                           Line2D([], [], color=ORANGE, lw=1.4, ls=DASH, label=f"{o2}  (L50 {fmt(r[o2])})"),
                           Line2D([], [], color=GREY, lw=1.2,
                                  label=f"random order, mean and 95% range  (L50 {fmt(r['random'])})")],
                  loc="upper center", bbox_to_anchor=(0.45, -0.2), frameon=False)
        stem_rule = "all_prey_rule" if theta == 1 else "half_diet_rule"
        save(fig, FOLDER, f"link_robustness_{stem_rule}_{tag}")

# L50 at a glance. Only the orders the paper argues from: edge betweenness,
# which appears in no other figure, plus weakest-first as the least-damaging
# anchor. Strongest-first is left out because the link_robustness strength
# figure already shows it against weakest and random; the recalculated
# betweenness order and the two trophic orders are left out with it. All of
# them stay in cadiz_link_robustness_summary.csv.
SUMMARY_FIGURE_ORDERS = [
    "highest edge betweenness first",
    "weakest links first",
]
order_names = ["random"] + SUMMARY_FIGURE_ORDERS
assert all(o in ORDERS for o in SUMMARY_FIGURE_ORDERS), "unknown order in SUMMARY_FIGURE_ORDERS"
fig, ax = plt.subplots(figsize=(COLUMN, 0.34 * len(order_names) + 0.9))
y = np.arange(len(order_names))[::-1]
for (theta, rule), mk, off in zip(RULES, ("o", "s"), (0.12, -0.12)):
    r = summary[summary.rule == rule].set_index("order")
    ax.scatter([r.at[o, "L50"] for o in order_names], y + off, color=RULE_COLOR[rule], marker=mk, s=16, zorder=3)
    lo, hi = r.at["random", "random_L50_lo"], r.at["random", "random_L50_hi"]
    ax.plot([lo, hi], [y[0] + off] * 2, color=RULE_COLOR[rule], lw=1.2, zorder=2)
ax.set_yticks(y, [wrap_label(o, 26) for o in order_names], fontsize=6.5)
ax.set_xlim(0, 1)
ax.set_xlabel("L50: fraction of links cut before half of\nliving groups are lost (lower = more fragile)")
tidy(ax, "x")
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.legend(handles=[Line2D([], [], ls="", marker="o", color=BLUE, label="rule: all prey lost"),
                   Line2D([], [], ls="", marker="s", color=ORANGE, label="rule: half of diet lost")],
          loc="upper center", bbox_to_anchor=(0.3, -0.25), frameon=False)
save(fig, FOLDER, "l50_summary")

# Giant component while links are cut.
for rule, stem, note in (("no starvation (links cut only)", "giant_component_links_cut_only",
                          "links cut only (bond percolation)"),
                         ("all prey lost", "giant_component_links_with_extinctions",
                          "with starvation (rule: all prey lost)")):
    cr = curves[curves.rule == rule]
    rnd = cr[cr.order.str.startswith("random")].dropna(subset=["lwcc_frac"])
    fig, ax = plt.subplots(figsize=(COLUMN, 2.5))
    ax.fill_between(rnd.frac_cut, rnd.lwcc_frac_lo, rnd.lwcc_frac_hi, color=GREY, alpha=0.25, lw=0)
    ax.plot(rnd.frac_cut, rnd.lwcc_frac, color=GREY, lw=1.2)
    for o, c, ls in (("highest edge betweenness first", BLUE, "-"),
                     ("highest edge betweenness first (recalculated)", ORANGE, DASH)):
        d = cr[cr.order == o]
        ax.plot(d.frac_cut, d.lwcc_frac, color=c, lw=1.4, ls=ls)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("fraction of feeding links cut")
    ax.set_ylabel("largest connected component\n(fraction of all 43 groups)")
    ax.text(0, 1.03, note, transform=ax.transAxes, fontsize=6.5, color=INK2)
    tidy(ax)
    ax.legend(handles=[Line2D([], [], color=BLUE, lw=1.4, label="highest edge betweenness first"),
                       Line2D([], [], color=ORANGE, lw=1.4, ls=DASH,
                              label="highest edge betweenness first (recalculated)"),
                       Line2D([], [], color=GREY, lw=1.2, label="random order, mean and 95% range")],
              loc="upper center", bbox_to_anchor=(0.45, -0.2), frameon=False)
    save(fig, FOLDER, stem)
