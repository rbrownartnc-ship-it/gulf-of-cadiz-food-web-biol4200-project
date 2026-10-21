"""What happens to the Gulf of Cadiz food web when groups are removed.

    python code/build_network.py     # first, to make output/
    python code/robustness.py        # ~1 min

Extinction rules (see foodweb.Cascade): after a removal, a consumer goes
secondarily extinct once it has lost
  - all of its prey            (topological rule, Dunne et al. 2002), or
  - half of its diet           (weighted rule, using the diet shares).
Phytoplankton, Detritus and Discard have no prey and never starve.

1. Single knockouts: remove each group on its own.
2. Guild removals: remove a whole trophic band or taxonomic group at once
   (does the web need every level, as the proposal hypothesises?).
3. Removal sequences: remove living groups one after another in a fixed
   order (random x1000, most/least connected, top-down, bottom-up, most
   important prey, PageRank importance, betweenness) and track how many
   groups are lost. R50 = fraction of groups that must be removed before
   half of all living groups are gone (Dunne et al. 2002).
4. Giant component: size of the largest connected part of the web during
   the same removals, with and without secondary extinctions (the
   percolation view of Albert et al. 2000 and Lab 7).

Writes output/cadiz_knockouts.csv, cadiz_guild_removal.csv,
cadiz_robustness_summary.csv, cadiz_robustness_curves.csv, robustness.txt,
the results workbook, and figures/cadiz_removal_effects,
figures/cadiz_robustness and figures/cadiz_giant_component (PDF + PNG).
"""
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from foodweb import (OUT, SEED, load_web, simple, Cascade, largest_wcc, largest_scc,
                     pagerank_importance, use_style, save, update_results_workbook,
                     INK, INK2, GRID, BLUE, ORANGE, GREY)

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
ko.round(4).to_csv(OUT / "cadiz_knockouts.csv", index=False)
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

ORDERS = {
    "most connected first": ranked(traits.total_degree),
    "least connected first": ranked(traits.total_degree, descending=False),
    "highest trophic level first": ranked(tl),
    "lowest trophic level first": ranked(tl, descending=False),
    "most important prey first": ranked(traits.diet_share_sum),
    "highest PageRank importance first": ranked(pr),
    "highest betweenness first": ranked(btw),
}

def sequence(order, theta=None):
    """Remove living groups in `order` (skipping any already lost). theta =
    None means no secondary extinctions (removal only). One row per step."""
    present = set(G)
    rows = [dict(primary_removed=0, frac_lost=0.0, n_present=S, lwcc=S,
                 lscc=largest_scc(H, present))]
    k = 0
    for n in order:
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
curves.round(5).to_csv(OUT / "cadiz_robustness_curves.csv", index=False)
summary.round(4).to_csv(OUT / "cadiz_robustness_summary.csv", index=False)
log("\n== removal sequences: R50 (fraction of living groups removed before half are lost) ==")
for r in summary.itertuples():
    extra = (f"  random 95% range {r.random_R50_lo:.3f}-{r.random_R50_hi:.3f}" if r.order == "random"
             else f"  ({r.frac_random_below:.0%} of random orders lower)")
    log(f"  {r.rule:18s} {r.order:36s} R50 {r.R50:.3f}{extra}")

log("\n== giant component: when does the surviving web first break into pieces? ==")
log("   (fraction of living groups removed; random = median and 95% range of 1000 orders)")
for rule in ["no secondary extinctions", "all prey lost", "half of diet lost"]:
    x = split_random[rule]
    log(f"  {rule:26s} random                       {np.nanmedian(x):.2f} "
        f"({np.nanpercentile(x, 2.5):.2f}-{np.nanpercentile(x, 97.5):.2f}), never in {np.isnan(x).mean():.0%}")
    for name in ["most connected first", "lowest trophic level first"]:
        c = curves[(curves.rule == rule) & (curves.order == name)]
        broken = c[c.lwcc_of_present < 1]
        when = f"{broken.frac_removed.iloc[0]:.2f}" if len(broken) else "never"
        log(f"  {rule:26s} {name:28s} {when}")

(OUT / "robustness.txt").write_text("\n".join(report) + "\n")
update_results_workbook()

# ---------------------------------------------------------------- figures
use_style()
RULE_COLOR = {"all prey lost": BLUE, "half of diet lost": ORANGE}

# Removal effects: single knockouts (left) and whole guilds (right).
kshow = ko[(ko.secondary_weighted > 0) | (ko.secondary_topological > 0)].iloc[::-1]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.1),
                             gridspec_kw=dict(width_ratios=[1, 1.15], wspace=0.95))
for ax, df, lab in ((a1, kshow, "group"), (a2, guild.iloc[::-1], "guild")):
    y = np.arange(len(df))
    for off, (key, rule) in zip((0.19, -0.19), (("topological", "all prey lost"),
                                               ("weighted", "half of diet lost"))):
        v = df[f"secondary_{key}"].to_numpy()
        ax.barh(y + off, v, height=0.36, color=RULE_COLOR[rule], edgecolor="white", lw=0.5)
        for yi, vi in zip(y + off, v):
            ax.text(vi + 0.15, yi, str(vi), va="center", fontsize=6, color=INK2)
    names = df[lab].tolist()
    if lab == "guild":
        names = [f"{g} ({k})" for g, k in zip(names, df.n_removed)]
    ax.set_yticks(y, names, fontsize=6.5)
    ax.set_xlabel("secondary extinctions (groups)")
    ax.grid(axis="x", color=GRID, lw=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
a1.set_title("a  remove one group", loc="left", color=INK)
a2.set_title("b  remove a whole guild (number of groups removed)", loc="left", color=INK)
fig.legend(handles=[Patch(color=BLUE, label="consumer dies when all its prey are gone"),
                    Patch(color=ORANGE, label="consumer dies when half its diet is gone")],
           loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.09))
save(fig, "cadiz_removal_effects")

# Robustness curves: rows = extinction rule, columns = pairs of removal orders.
PAIRS = [("connectivity", "most connected first", "least connected first"),
         ("trophic position", "highest trophic level first", "lowest trophic level first"),
         ("importance", "most important prey first", "highest PageRank importance first")]
fig, axes = plt.subplots(2, 3, figsize=(7.0, 4.7), sharex=True, sharey=True)
for i, (theta, rule) in enumerate(RULES):
    cr = curves[curves.rule == rule]
    rnd = cr[cr.order.str.startswith("random")]
    for j, (title, o1, o2) in enumerate(PAIRS):
        ax = axes[i, j]
        ax.plot([0, 1], [0, 1], color=GRID, lw=0.8, ls=(0, (2, 2)))
        ax.axhline(0.5, color=GRID, lw=0.6)
        ax.fill_between(rnd.frac_removed, rnd.frac_lost_lo, rnd.frac_lost_hi,
                        color=GREY, alpha=0.25, lw=0)
        ax.plot(rnd.frac_removed, rnd.frac_lost, color=GREY, lw=1.2)
        for o, c, ls in ((o1, BLUE, "-"), (o2, ORANGE, (0, (4, 1.5)))):
            d = cr[cr.order == o]
            ax.plot(d.frac_removed, d.frac_lost, color=c, lw=1.4, ls=ls)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.02)
        ax.grid(color=GRID, lw=0.4)
        ax.set_axisbelow(True)
        ax.tick_params(length=2, pad=1.5)
        if i == 0:
            ax.set_title(f"by {title}", loc="left", color=INK)
        if j == 0:
            ax.set_ylabel(f"rule: {rule}\nfraction of living groups lost")
        if i == 1:
            ax.set_xlabel("fraction of living groups removed")
            r = summary[summary.rule == rule].set_index("order").R50
            ax.legend(handles=[
                Line2D([], [], color=BLUE, lw=1.4, label=o1),
                Line2D([], [], color=ORANGE, lw=1.4, ls=(0, (4, 1.5)), label=o2),
                Line2D([], [], color=GREY, lw=1.2, label="random order (mean, 95% range)")],
                loc="upper center", bbox_to_anchor=(0.5, -0.3), frameon=False, handlelength=2.2)
for i, (theta, rule) in enumerate(RULES):          # R50 values, top-left of each panel
    r = summary[summary.rule == rule].set_index("order").R50
    for j, (title, o1, o2) in enumerate(PAIRS):
        axes[i, j].text(0.97, 0.04, f"R50  solid {r[o1]:.2f} · dashed {r[o2]:.2f}\n"
                        f"random {r['random']:.2f}", transform=axes[i, j].transAxes,
                        ha="right", va="bottom", fontsize=6.5, color=INK2, linespacing=1.3)
fig.tight_layout(h_pad=1.2, w_pad=0.6)
save(fig, "cadiz_robustness")

# Giant component during removal, without and with secondary extinctions.
fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.5), sharey=True)
for ax, rule, title in ((axes[0], "no secondary extinctions", "a  removal only (percolation)"),
                        (axes[1], "all prey lost", "b  with secondary extinctions (all prey lost)")):
    cr = curves[curves.rule == rule]
    rnd = cr[cr.order.str.startswith("random")]
    f = np.linspace(0, 1, 50)                  # every group not yet removed, in one piece
    ax.plot(f, (S - f * S_LIV) / S, color=INK2, lw=0.8, ls=(0, (1, 1.5)))
    ax.fill_between(rnd.frac_removed, rnd.lwcc_frac_lo, rnd.lwcc_frac_hi, color=GREY, alpha=0.25, lw=0)
    ax.plot(rnd.frac_removed, rnd.lwcc_frac, color=GREY, lw=1.2)
    for o, c, ls in (("most connected first", BLUE, "-"),
                     ("lowest trophic level first", ORANGE, (0, (4, 1.5)))):
        d = cr[cr.order == o]
        ax.plot(d.frac_removed, d.lwcc_frac, color=c, lw=1.4, ls=ls)
    ax.set_title(title, loc="left", color=INK)
    ax.set_xlabel("fraction of living groups removed")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.grid(color=GRID, lw=0.4)
    ax.set_axisbelow(True)
axes[0].set_ylabel("largest connected component\n(fraction of all 43 groups)")
fig.legend(handles=[Line2D([], [], color=BLUE, lw=1.4, label="most connected first"),
                    Line2D([], [], color=ORANGE, lw=1.4, ls=(0, (4, 1.5)), label="lowest trophic level first"),
                    Line2D([], [], color=GREY, lw=1.2, label="random order (mean, 95% range)"),
                    Line2D([], [], color=INK2, lw=0.8, ls=(0, (1, 1.5)),
                           label="all groups not yet removed (no splitting, no extinctions)")],
           loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.2))
fig.tight_layout(w_pad=1.5)
save(fig, "cadiz_giant_component")
