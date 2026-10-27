"""What happens to the Gulf of Cadiz food web when groups (nodes) are removed.

    python code/build_network.py     # first, to make output/
    python code/node_removal.py      # ~1 min

Extinction rules (see foodweb.Cascade): after a removal, a consumer goes
secondarily extinct once it has lost
  - all of its prey            (topological rule, Dunne et al. 2002), or
  - half of its diet           (weighted rule, using the diet shares).
Phytoplankton, Detritus and Discard have no prey and never starve.

1. Single knockouts: remove each group on its own.
2. Guild removals: remove a whole trophic band or taxonomic group at once
   (does the web need every level, as the proposal hypothesises?).
3. Removal sequences: remove living groups one after another (random x1000,
   most/least connected, top-down, bottom-up, most important prey, PageRank
   importance, betweenness) and track how many groups are lost. Two targeted
   attacks are also run "recalculated": after every removal the next target is
   re-ranked on the surviving web (Holme et al. 2002). R50 = fraction of groups
   that must be removed before half of all living groups are gone (Dunne et
   al. 2002), at extinction thresholds of all, 3/4, 1/2 and 1/4 of the diet.
4. Giant component: size of the largest connected part of the web during
   the same removals, with and without secondary extinctions (the
   percolation view of Albert et al. 2000 and Lab 7).

Writes output/cadiz_node_knockouts.csv, cadiz_guild_removal.csv,
cadiz_node_robustness_summary.csv, cadiz_node_robustness_curves.csv,
node_removal.txt and the results workbook. Figures (one per idea, PDF + PNG)
in figures/05_node_removal/.
"""
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from foodweb import (OUT, SEED, load_web, simple, Cascade, largest_wcc, largest_scc,
                     pagerank_importance, use_style, save, tidy, wrap_label, update_results_workbook,
                     COLUMN, FULL, INK, INK2, GRID, BLUE, ORANGE, GREY)

FOLDER = "05_node_removal"
N_RANDOM = 1000
G, traits = load_web()
H = simple(G)
cas = Cascade(G)
S = G.number_of_nodes()
LIVING = sorted(n for n in G if G.nodes[n]["living"])
S_LIV = len(LIVING)
RULES = [(1.0, "all prey lost"), (0.5, "half of diet lost")]
SENSITIVITY = [(1.0, "all prey lost"), (0.75, "3/4 of diet lost"),
               (0.5, "half of diet lost"), (0.25, "1/4 of diet lost")]
report = []
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    report.append(line)

# Sanity checks on the extinction rule, on cases that can be read off the data.
assert cas.run([], 1.0)[1] == set() and cas.run([], 0.5)[1] == set()
assert set(G.predecessors("Anchovy")) - {"Anchovy"} == {"Meso and microzooplankton"}
assert "Anchovy" in cas.run(["Meso and microzooplankton"], 1.0)[1]
only_phyto = set(G.predecessors("Meso and microzooplankton")) - {"Meso and microzooplankton"} == {"Phytoplankton"}
assert ("Meso and microzooplankton" in cas.run(["Phytoplankton"], 1.0)[1]) == only_phyto

# ---------------------------------------------------------------- 1. knockouts
rows = []
for n in G:
    preds = [q for q in G.successors(n) if q != n]
    loss = {q: G[n][q]["d"] for q in preds}
    worst = max(loss, key=loss.get) if loss else ""
    row = dict(group=n, category=traits.at[n, "category"],
               trophic_level=traits.at[n, "trophic_level"], n_predators=len(preds),
               max_diet_loss=loss.get(worst, 0.0), max_diet_loss_predator=worst,
               predators_losing_half_diet=sum(v >= 0.5 for v in loss.values()))
    for theta, label in RULES:
        present, sec = cas.run([n], theta)
        key = "topological" if theta == 1 else "weighted"
        row[f"secondary_{key}"] = len(sec)
        row[f"secondary_{key}_groups"] = "; ".join(sorted(sec))
        row[f"lwcc_after_{key}"] = largest_wcc(G, present)
    row["lwcc_after_no_cascade"] = largest_wcc(G, set(G) - {n})
    row["lscc_after_no_cascade"] = largest_scc(H, set(G) - {n})
    rows.append(row)
ko = pd.DataFrame(rows).sort_values(["secondary_weighted", "secondary_topological",
                                     "max_diet_loss"], ascending=False)
for r in ko.itertuples():           # the weighted rule is stricter, so it can only lose more
    assert set(filter(None, r.secondary_topological_groups.split("; "))) <= \
           set(filter(None, r.secondary_weighted_groups.split("; ")))
ko.round(4).to_csv(OUT / "cadiz_node_knockouts.csv", index=False)
log("== single knockouts ==")
log(f"groups whose loss causes >= 1 secondary extinction: "
    f"{(ko.secondary_topological > 0).sum()} (all prey lost), "
    f"{(ko.secondary_weighted > 0).sum()} (half of diet lost), of {S}")
for r in ko[(ko.secondary_weighted > 0) | (ko.secondary_topological > 0)].itertuples():
    log(f"  {r.group:28s} all-prey {r.secondary_topological:2d} | half-diet "
        f"{r.secondary_weighted:2d}: {r.secondary_weighted_groups}")
log(f"largest weak component after any single removal (no cascade): "
    f"min {ko.lwcc_after_no_cascade.min()} of {S - 1}; largest feeding loop "
    f"after removal: min {ko.lscc_after_no_cascade.min()} "
    f"({ko.loc[ko.lscc_after_no_cascade.idxmin(), 'group']})")

# ---------------------------------------------------------------- 2. guilds
tl, cat, role = traits.trophic_level, traits.category, traits.role
liv = traits.living
GUILDS = [
    ("primary producers (phytoplankton)", ["Phytoplankton"]),
    ("detritus and discards", ["Detritus", "Discard"]),
    ("primary consumers (TL < 2.5)", list(traits.index[liv & (tl > 1) & (tl < 2.5)])),
    ("mid-level consumers (2.5 ≤ TL < 3.5)", list(traits.index[liv & (tl >= 2.5) & (tl < 3.5)])),
    ("upper consumers (TL ≥ 3.5)", list(traits.index[liv & (tl >= 3.5)])),
    ("top predators (no predators)", list(traits.index[role == "top predator"])),
    ("invertebrates (excl. phytoplankton)",
     list(traits.index[(cat == "invertebrates & plankton") & (traits.index != "Phytoplankton")])),
    ("fishes", list(traits.index[cat == "fishes"])),
    ("marine mammals, birds, turtles", list(traits.index[cat == "marine mammals, birds, turtles"])),
]
rows = []
for name, members in GUILDS:
    row = dict(guild=name, n_removed=len(members), removed="; ".join(sorted(members)))
    for theta, label in RULES:
        present, sec = cas.run(members, theta)
        key = "topological" if theta == 1 else "weighted"
        row[f"secondary_{key}"] = len(sec)
        row[f"secondary_{key}_groups"] = "; ".join(sorted(sec))
        row[f"living_left_{key}"] = sum(1 for m in LIVING if m in present)
        row[f"lwcc_after_{key}"] = largest_wcc(G, present)
    rows.append(row)
guild = pd.DataFrame(rows)
guild.to_csv(OUT / "cadiz_guild_removal.csv", index=False)
log("\n== guild removals ==")
for r in guild.itertuples():
    log(f"  {r.guild:38s} remove {r.n_removed:2d} -> secondary: all-prey "
        f"{r.secondary_topological:2d}, half-diet {r.secondary_weighted:2d}; "
        f"living left {r.living_left_topological}/{r.living_left_weighted} of {S_LIV}")

# ---------------------------------------------------------------- 3. sequences
pr = pagerank_importance(H)
btw = nx.betweenness_centrality(H)
def ranked(score, descending=True):
    """Living groups by a score from the intact web; ties broken by name."""
    key = (lambda n: (-score[n], n)) if descending else (lambda n: (score[n], n))
    return sorted(LIVING, key=key)

def recalculated(score_on):
    """A chooser for a recalculated attack: after every removal, take the
    surviving living group that scores highest on the surviving web."""
    def choose(present):
        score = score_on(H.subgraph(present))
        return min((n for n in LIVING if n in present), key=lambda n: (-score[n], n))
    return choose

ORDERS = {
    "most connected first": ranked(traits.total_degree),
    "least connected first": ranked(traits.total_degree, descending=False),
    "highest trophic level first": ranked(tl),
    "lowest trophic level first": ranked(tl, descending=False),
    "most important prey first": ranked(traits.diet_share_sum),
    "highest PageRank importance first": ranked(pr),
    "highest betweenness first": ranked(btw),
    "most connected first (recalculated)": recalculated(lambda W: dict(W.degree())),
    "highest betweenness first (recalculated)": recalculated(nx.betweenness_centrality),
}

def sequence(order, theta=None):
    """Remove living groups in `order` (a list, skipping any already lost, or
    a chooser called on the surviving groups before every removal). theta =
    None means no secondary extinctions (removal only). One row per step."""
    present = set(G)
    rows = [dict(primary_removed=0, frac_lost=0.0, n_present=S, lwcc=S,
                 lscc=largest_scc(H, present))]
    k = 0
    def targets():
        if callable(order):
            while any(m in present for m in LIVING):
                yield order(present)
        else:
            yield from order
    for n in targets():
        if n not in present:
            continue                         # already lost to a secondary extinction
        k += 1
        if theta is None:
            present.discard(n)
        else:
            present, _ = cas.run([n], theta, present)
        rows.append(dict(primary_removed=k,
                         frac_lost=sum(1 for m in LIVING if m not in present) / S_LIV,
                         n_present=len(present), lwcc=largest_wcc(G, present),
                         lscc=largest_scc(H, present)))
    return pd.DataFrame(rows)

def r50(curve):
    hit = curve[curve.frac_lost >= 0.5]
    return hit.primary_removed.iloc[0] / S_LIV

def on_grid(curve, col):
    """Values at primary_removed = 0..S_LIV, carrying the last value forward
    once every living group is gone."""
    s = curve.set_index("primary_removed")[col]
    return s.reindex(range(S_LIV + 1)).ffill().to_numpy()

rng = np.random.default_rng(SEED)
random_orders = [list(rng.permutation(LIVING)) for _ in range(N_RANDOM)]
def first_split(curve):
    """Fraction of living groups removed when the surviving web first breaks
    into more than one piece (nan if it never does)."""
    split = curve[curve.lwcc < curve.n_present]
    return split.primary_removed.iloc[0] / S_LIV if len(split) else np.nan

curves, summary, split_random = [], [], {}
for theta, label in SENSITIVITY + [(None, "no secondary extinctions")]:
    rand = [sequence(o, theta) for o in random_orders]
    split_random[label] = np.array([first_split(c) for c in rand])
    lost = np.array([on_grid(c, "frac_lost") for c in rand])
    lw = np.array([on_grid(c, "lwcc") for c in rand])
    r50_rand = np.array([r50(c) for c in rand])
    x = np.arange(S_LIV + 1)
    # Curves only for the two rules in the figures plus removal-only;
    # the other thresholds feed the R50 sensitivity check.
    keep_curve = label in dict(RULES).values() or theta is None
    if keep_curve:
        present = np.array([on_grid(c, "n_present") for c in rand])
        curves.append(pd.DataFrame(dict(
            order="random (mean of 1000)", rule=label, primary_removed=x,
            frac_removed=x / S_LIV, frac_lost=lost.mean(0),
            frac_lost_lo=np.percentile(lost, 2.5, 0), frac_lost_hi=np.percentile(lost, 97.5, 0),
            lwcc_frac=lw.mean(0) / S, lwcc_frac_lo=np.percentile(lw, 2.5, 0) / S,
            lwcc_frac_hi=np.percentile(lw, 97.5, 0) / S,
            lwcc_of_present=(lw / present).mean(0))))
    if theta is not None:
        summary.append(dict(order="random", rule=label, R50=r50_rand.mean(),
                            random_R50_lo=np.percentile(r50_rand, 2.5),
                            random_R50_hi=np.percentile(r50_rand, 97.5),
                            frac_random_below=np.nan))
    for name, order in ORDERS.items():
        c = sequence(order, theta)
        if keep_curve:
            curves.append(pd.DataFrame(dict(
                order=name, rule=label, primary_removed=c.primary_removed,
                frac_removed=c.primary_removed / S_LIV, frac_lost=c.frac_lost,
                lwcc_frac=c.lwcc / S, lwcc_of_present=c.lwcc / c.n_present,
                lscc_frac=c.lscc / S)))
        if theta is not None:
            v = r50(c)
            summary.append(dict(order=name, rule=label, R50=v,
                                random_R50_lo=np.nan, random_R50_hi=np.nan,
                                frac_random_below=(r50_rand < v).mean()))
curves = pd.concat(curves, ignore_index=True)
summary = pd.DataFrame(summary)
curves.round(5).to_csv(OUT / "cadiz_node_robustness_curves.csv", index=False)
summary.round(4).to_csv(OUT / "cadiz_node_robustness_summary.csv", index=False)
log("\n== removal sequences: R50 (fraction of living groups removed before half are lost) ==")
for r in summary.itertuples():
    extra = (f"  random 95% range {r.random_R50_lo:.3f}-{r.random_R50_hi:.3f}" if r.order == "random"
             else f"  ({r.frac_random_below:.0%} of random orders lower)")
    log(f"  {r.rule:18s} {r.order:42s} R50 {r.R50:.3f}{extra}")

frag = []
for rule in ["no secondary extinctions", "all prey lost", "half of diet lost"]:
    x = split_random[rule]
    frag.append(dict(rule=rule, order="random", first_split=np.nanmedian(x),
                     random_lo=np.nanpercentile(x, 2.5), random_hi=np.nanpercentile(x, 97.5)))
    for name in ORDERS:
        c = curves[(curves.rule == rule) & (curves.order == name)]
        broken = c[c.lwcc_of_present < 1]
        frag.append(dict(rule=rule, order=name,
                         first_split=broken.frac_removed.iloc[0] if len(broken) else np.nan,
                         random_lo=np.nan, random_hi=np.nan))
pd.DataFrame(frag).round(4).to_csv(OUT / "cadiz_node_fragmentation.csv", index=False)
log("\n== giant component: when does the surviving web first break into pieces? ==")
log("   (fraction of living groups removed; random = median and 95% range of 1000 orders)")
for rule in ["no secondary extinctions", "all prey lost", "half of diet lost"]:
    x = split_random[rule]
    log(f"  {rule:26s} random                       {np.nanmedian(x):.2f} "
        f"({np.nanpercentile(x, 2.5):.2f}-{np.nanpercentile(x, 97.5):.2f}), never in {np.isnan(x).mean():.0%}")
    for name in ["most connected first", "most connected first (recalculated)",
                 "highest betweenness first (recalculated)", "lowest trophic level first"]:
        c = curves[(curves.rule == rule) & (curves.order == name)]
        broken = c[c.lwcc_of_present < 1]
        when = f"{broken.frac_removed.iloc[0]:.2f}" if len(broken) else "never"
        log(f"  {rule:26s} {name:40s} {when}")

(OUT / "node_removal.txt").write_text("\n".join(report) + "\n")
update_results_workbook()

# ---------------------------------------------------------------- figures
use_style()
RULE_COLOR = {"all prey lost": BLUE, "half of diet lost": ORANGE}
RULE_LEGEND = [Patch(color=BLUE, label="consumer dies when all its prey are gone"),
               Patch(color=ORANGE, label="consumer dies when half its diet is gone")]
DASH = (0, (4, 1.5))

def paired_bars(df, labels, stem, width, xlabel="secondary extinctions (groups)"):
    """Horizontal bars, one pair per row: all-prey rule and half-diet rule."""
    fig, ax = plt.subplots(figsize=(width, 0.36 * len(df) + 0.8))
    y = np.arange(len(df))
    for off, key, rule in ((0.19, "topological", "all prey lost"),
                           (-0.19, "weighted", "half of diet lost")):
        v = df[f"secondary_{key}"].to_numpy()
        ax.barh(y + off, v, height=0.36, color=RULE_COLOR[rule], edgecolor="white", lw=0.5)
        for yi, vi in zip(y + off, v):
            ax.text(vi + 0.3, yi, str(vi), va="center", fontsize=6.5, color=INK2)
    ax.set_yticks(y, [wrap_label(t, 26) for t in labels], fontsize=6.5)
    ax.set_xlabel(xlabel)
    tidy(ax, "x")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    gap = 0.42 / (fig.get_figheight() * 0.77)          # 0.42 in below the axes
    ax.legend(handles=RULE_LEGEND, loc="upper center", bbox_to_anchor=(0.4, -gap),
              frameon=False, ncol=1)
    save(fig, FOLDER, stem)

kshow = ko[(ko.secondary_weighted > 0) | (ko.secondary_topological > 0)].iloc[::-1]
paired_bars(kshow, kshow.group.tolist(), "single_group_knockouts", COLUMN)
g = guild.iloc[::-1]
paired_bars(g, [f"{a} ({k})" for a, k in zip(g.guild, g.n_removed)], "guild_removal", COLUMN)

# One robustness chart per pair of removal orders and extinction rule.
PAIRS = [("connectivity", "most connected first", "least connected first"),
         ("trophic_position", "highest trophic level first", "lowest trophic level first"),
         ("importance", "most important prey first", "highest PageRank importance first"),
         ("recalculated_degree", "most connected first", "most connected first (recalculated)"),
         ("recalculated_betweenness", "highest betweenness first", "highest betweenness first (recalculated)")]
for theta, rule in RULES:
    cr = curves[curves.rule == rule]
    rnd = cr[cr.order.str.startswith("random")]
    r = summary[summary.rule == rule].set_index("order").R50
    for tag, o1, o2 in PAIRS:
        fig, ax = plt.subplots(figsize=(COLUMN, 2.5))
        ax.plot([0, 1], [0, 1], color=GRID, lw=0.8, ls=(0, (2, 2)))
        ax.axhline(0.5, color=GRID, lw=0.6)
        ax.fill_between(rnd.frac_removed, rnd.frac_lost_lo, rnd.frac_lost_hi, color=GREY, alpha=0.25, lw=0)
        ax.plot(rnd.frac_removed, rnd.frac_lost, color=GREY, lw=1.2)
        for o, c, ls in ((o1, BLUE, "-"), (o2, ORANGE, DASH)):
            d = cr[cr.order == o]
            ax.plot(d.frac_removed, d.frac_lost, color=c, lw=1.4, ls=ls)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.02)
        ax.set_xlabel("fraction of living groups removed")
        ax.set_ylabel("fraction of living groups lost")
        ax.text(0, 1.03, f"rule: {rule}", transform=ax.transAxes, fontsize=6.5, color=INK2)
        tidy(ax)
        ax.legend(handles=[Line2D([], [], color=BLUE, lw=1.4, label=f"{o1}  (R50 {r[o1]:.2f})"),
                           Line2D([], [], color=ORANGE, lw=1.4, ls=DASH, label=f"{o2}  (R50 {r[o2]:.2f})"),
                           Line2D([], [], color=GREY, lw=1.2,
                                  label=f"random order, mean and 95% range  (R50 {r['random']:.2f})")],
                  loc="upper center", bbox_to_anchor=(0.45, -0.2), frameon=False)
        stem_rule = "all_prey_rule" if theta == 1 else "half_diet_rule"
        save(fig, FOLDER, f"robustness_{stem_rule}_{tag}")

# R50 at a glance (both rules); random shows its 95% range.
# The figure shows only the orders the paper argues from. The trophic-level
# orders are left out because the trophic_position figure already makes that
# comparison, and the recalculated and least-connected orders are sensitivity
# checks, as is PageRank importance, which ranks almost the same groups as
# importance as prey. Every order is still in cadiz_node_robustness_summary.csv.
SUMMARY_FIGURE_ORDERS = [
    "most connected first",
    "highest betweenness first",
    "most important prey first",
]
order_names = ["random"] + SUMMARY_FIGURE_ORDERS
assert all(o in ORDERS for o in SUMMARY_FIGURE_ORDERS), "unknown order in SUMMARY_FIGURE_ORDERS"
fig, ax = plt.subplots(figsize=(COLUMN, 0.34 * len(order_names) + 0.9))
y = np.arange(len(order_names))[::-1]
for (theta, rule), mk, off in zip(RULES, ("o", "s"), (0.12, -0.12)):
    r = summary[summary.rule == rule].set_index("order")
    vals = [r.at[o, "R50"] for o in order_names]
    ax.scatter(vals, y + off, color=RULE_COLOR[rule], marker=mk, s=16, zorder=3)
    lo, hi = r.at["random", "random_R50_lo"], r.at["random", "random_R50_hi"]
    ax.plot([lo, hi], [y[0] + off] * 2, color=RULE_COLOR[rule], lw=1.2, zorder=2)
ax.axvline(21 / 41, color=INK2, lw=0.6, ls=(0, (1, 1.5)))
ax.text(21 / 41, y[0] + 0.7, "no secondary\nextinctions", fontsize=6.5, color=INK2, ha="center", va="bottom")
ax.set_yticks(y, [wrap_label(o, 26) for o in order_names], fontsize=6.5)
ax.set_xlim(0, 0.56)
ax.set_xlabel("R50: fraction of living groups removed\nbefore half of them are lost (lower = more fragile)")
tidy(ax, "x")
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.legend(handles=[Line2D([], [], ls="", marker="o", color=BLUE, label="rule: all prey lost"),
                   Line2D([], [], ls="", marker="s", color=ORANGE, label="rule: half of diet lost")],
          loc="upper center", bbox_to_anchor=(0.3, -0.25), frameon=False)
save(fig, FOLDER, "r50_summary")

# Giant component during removal: removal only, and with secondary extinctions.
for rule, stem in (("no secondary extinctions", "giant_component_removal_only"),
                   ("all prey lost", "giant_component_with_extinctions")):
    cr = curves[curves.rule == rule]
    rnd = cr[cr.order.str.startswith("random")]
    fig, ax = plt.subplots(figsize=(COLUMN, 2.5))
    f = np.linspace(0, 1, 50)                  # every group not yet removed, in one piece
    ax.plot(f, (S - f * S_LIV) / S, color=INK2, lw=0.8, ls=(0, (1, 1.5)))
    ax.fill_between(rnd.frac_removed, rnd.lwcc_frac_lo, rnd.lwcc_frac_hi, color=GREY, alpha=0.25, lw=0)
    ax.plot(rnd.frac_removed, rnd.lwcc_frac, color=GREY, lw=1.2)
    for o, c, ls in (("most connected first", BLUE, "-"),
                     ("most connected first (recalculated)", ORANGE, DASH)):
        d = cr[cr.order == o]
        ax.plot(d.frac_removed, d.lwcc_frac, color=c, lw=1.4, ls=ls)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("fraction of living groups removed")
    ax.set_ylabel("largest connected component\n(fraction of all 43 groups)")
    ax.text(0, 1.03, "removal only (percolation)" if rule.startswith("no") else
            "with secondary extinctions (rule: all prey lost)",
            transform=ax.transAxes, fontsize=6.5, color=INK2)
    tidy(ax)
    ax.legend(handles=[Line2D([], [], color=BLUE, lw=1.4, label="most connected first"),
                       Line2D([], [], color=ORANGE, lw=1.4, ls=DASH, label="most connected first (recalculated)"),
                       Line2D([], [], color=GREY, lw=1.2, label="random order, mean and 95% range"),
                       Line2D([], [], color=INK2, lw=0.8, ls=(0, (1, 1.5)),
                              label="all groups not yet removed, in one piece")],
              loc="upper center", bbox_to_anchor=(0.45, -0.2), frameon=False)
    save(fig, FOLDER, stem)
