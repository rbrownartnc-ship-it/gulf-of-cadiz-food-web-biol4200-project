"""Uncertainty and significance for the paper's results, on the three webs the paper keeps.

    python code/compare_webs.py      # first: this script checks itself against its outputs
    python code/significance.py      # ~20 s

Feedback on the results draft asked for (a) more statistical comparison, with
repeated trials rather than a single run, (b) clearer error representation in
the figures and explicit evidence that lines and groups do or do not differ,
(c) three webs only (Gulf of Cadiz, Angolan shelf, Mondego estuary), compared
on baseline statistics, centralization, node removal by degree and by
betweenness, diet diversity and robustness, and (d) a better picture of the
trophic-level relationships than a bare Spearman coefficient.

What this script adds, for each of the three webs:

1. Baseline table: nodes, links, connectance, mean degree, trophic levels, and
   Freeman centralization (degree, in-degree, out-degree, betweenness), each
   centralization compared with 1000 random directed graphs that have the same
   number of nodes and links.
2. Trophic level against number of prey, effective number of prey, number of
   predators, total degree and betweenness (consumers only): Spearman rho with
   a bootstrap 95% interval (10,000 resamples of the groups), a permutation
   p-value, and a least-squares line with a bootstrap 95% band. Differences in
   rho between webs get a bootstrap interval and a Fisher z test.
3. Differences between groups of nodes: Kruskal-Wallis across trophic bands
   (and, for Cadiz, across the taxonomic categories used in the figures), with
   pairwise Mann-Whitney tests, Holm-corrected, and Cliff's delta.
4. Node removal. Random order is 1000 trials. A targeted order is a fixed
   ranking, so one run is the whole answer *except* where groups tie on the
   ranking score; each targeted order is therefore run 200 times with ties
   broken at random. Every targeted order is tested against the 1000 random
   orders (Monte Carlo p-value), on two statistics: R50, and the area under
   the share-lost curve, which does not move in steps of 1/n the way R50 does.
   The two extinction rules are compared on the same 1000 random orders
   (paired), and the webs are compared with each other.

Nothing in output/cadiz_* or output/compare_webs_* is touched. Before writing
anything, the script checks that it reproduces compare_webs.py exactly: the
correlations, the degree centralization, and every R50 (random and targeted).

This is the second half of the cross-ecosystem comparison, so everything goes
where compare_webs.py puts its results: tables in output/compare_webs_stats_*.csv,
figures in figures/08_comparison/ (named compare_*), and the notes as the last
part of notes/07_cross_ecosystem.md.
"""
from itertools import combinations

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.stats import (rankdata, spearmanr, norm, kruskal, mannwhitneyu,
                         wilcoxon)

from foodweb import (OUT, FIG, ROOT, SEED, simple, Cascade, use_style, save, tidy,
                     wrap_label, COLUMN, INK, INK2, GRID, BLUE, ORANGE, AQUA, GREY)
from compare_webs import build, centrality, global_properties, WEBS

FOLDER = "08_comparison"          # the same folder as compare_webs.py
P = "compare_"                    # and the same prefix on every figure name
PAPER = [net for net, _ in WEBS]                   # Cadiz, Angolan shelf, Mondego estuary
assert PAPER == ["FW_005", "FW_003", "FW_016_01"]
STYLE = {"FW_005": (BLUE, "o"), "FW_003": (ORANGE, "s"), "FW_016_01": (AQUA, "^")}
TAG = {"FW_005": "cadiz", "FW_003": "angolan", "FW_016_01": "mondego"}   # in file names
RULES = [(1.0, "all prey lost"), (0.5, "half of diet lost")]
MEASURES = [("n_prey", "number of prey"),
            ("effective_prey", "effective number of prey"),
            ("n_predators", "number of predators"),
            ("total_degree", "total degree"),
            ("betweenness", "betweenness centrality")]
ORDERS = ["most connected first", "highest betweenness first", "most important prey first",
          "lowest trophic level first", "highest trophic level first", "least connected first"]
N_BOOT = 10_000        # bootstrap resamples and permutations for the correlations
N_NULL = 1000          # random graphs for the centralization baseline
N_RANDOM = 1000        # random removal orders (the same ones compare_webs.py uses)
N_TIES = 200           # tie-break trials per targeted order
ALPHA = 0.05

def stream(k):
    """A separate, reproducible random stream per analysis, so adding one
    analysis never changes the numbers of another."""
    return np.random.default_rng([SEED, k])

def ptxt(p):
    return "p < 0.001" if p < 0.001 else f"p = {p:.3f}" if p < 0.1 else f"p = {p:.2f}"

def minus(s):
    return s.replace("-", "−")

def holm(p):
    p = np.asarray(p, float)
    adj, run, m = np.empty(len(p)), 0.0, len(p)
    for rank, i in enumerate(np.argsort(p)):
        run = max(run, (m - rank) * p[i])
        adj[i] = min(1.0, run)
    return adj

# ---------------------------------------------------------------- webs
webs = {}
for net, site in WEBS:
    w = build(net)
    w["site"] = site
    webs[net] = w
cents = {net: centrality(webs[net]) for net in PAPER}
SITE = {net: webs[net]["site"] for net in PAPER}
cadiz_cat = pd.read_csv(OUT / "cadiz_node_traits.csv", index_col=0).category
assert set(cadiz_cat.index) == set(webs["FW_005"]["names"])

# ---------------------------------------------------------------- 1. baseline
def centralization(H):
    """Freeman centralization of a directed graph without self-loops: how far
    the most central node stands above the rest, as a share of the most
    unequal graph possible (a star = 1). Degree is taken on the undirected
    version, as in compare_webs.py."""
    S = H.number_of_nodes()
    deg = np.array([d for _, d in H.to_undirected().degree()])
    ind = np.array([d for _, d in H.in_degree()])
    outd = np.array([d for _, d in H.out_degree()])
    btw = np.array(list(nx.betweenness_centrality(H).values()))
    return {"degree centralization": (deg.max() * S - deg.sum()) / ((S - 1) * (S - 2)),
            "in-degree centralization (prey)": (ind.max() * S - ind.sum()) / (S - 1) ** 2,
            "out-degree centralization (predators)": (outd.max() * S - outd.sum()) / (S - 1) ** 2,
            "betweenness centralization": (btw.max() * S - btw.sum()) / (S - 1)}

base_rows, cz_rows = {}, []
rng = stream(2)
for net in PAPER:
    w = webs[net]
    G, t = w["G"], w["traits"]
    H = simple(G)
    gp = global_properties(w)
    cz = centralization(H)
    assert abs(cz["degree centralization"] - gp["degree_centralization"]) < 1e-12
    S, m = H.number_of_nodes(), H.number_of_edges()
    null = pd.DataFrame([centralization(nx.gnm_random_graph(S, m, seed=int(rng.integers(2**31)),
                                                            directed=True))
                         for _ in range(N_NULL)])
    for k, v in cz.items():
        x = null[k].to_numpy()
        hi, lo = (1 + (x >= v).sum()) / (N_NULL + 1), (1 + (x <= v).sum()) / (N_NULL + 1)
        cz_rows.append(dict(network=net, site=SITE[net], measure=k, observed=v,
                            random_mean=x.mean(), random_sd=x.std(ddof=1),
                            random_lo=np.percentile(x, 2.5), random_hi=np.percentile(x, 97.5),
                            z=(v - x.mean()) / x.std(ddof=1), p_two_sided=min(1.0, 2 * min(hi, lo))))
    base_rows[SITE[net]] = {
        "nodes (groups)": S,
        "living groups": int(t.living.sum()),
        "links (incl. cannibalism)": G.number_of_edges(),
        "links (excl. cannibalism)": m,
        "connectance L/S^2": gp["connectance"],
        "mean number of prey = mean number of predators": m / S,
        "SD number of prey": t.n_prey.std(ddof=1),
        "SD number of predators": t.n_predators.std(ddof=1),
        "mean total degree": t.total_degree.mean(),
        "SD total degree": t.total_degree.std(ddof=1),
        "max total degree": int(t.total_degree.max()),
        "basal groups": int((t.role == "basal").sum()),
        "top predators": int((t.role == "top predator").sum()),
        "mean trophic level": t.trophic_level.mean(),
        "max trophic level": t.trophic_level.max(),
        "mean effective number of prey (consumers)": t.effective_prey.mean(),
        "median share of diet from largest prey": t.top_prey_share.median(),
        "clustering coefficient": gp["clustering"],
        "mean path length": gp["path_length"],
        **cz}
baseline = pd.DataFrame(base_rows)
baseline.index.name = "statistic"
centz = pd.DataFrame(cz_rows)

# ---------------------------------------------------------------- 2. correlations
def rowwise_r(a, b):
    a = a - a.mean(1, keepdims=True)
    b = b - b.mean(1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        return (a * b).sum(1) / np.sqrt((a * a).sum(1) * (b * b).sum(1))

def bootstrap(x, y, rng):
    """Resample the groups with replacement: rho, slope and intercept each time."""
    idx = rng.integers(0, len(x), (N_BOOT, len(x)))
    xb, yb = x[idx], y[idx]
    rho = rowwise_r(rankdata(xb, axis=1), rankdata(yb, axis=1))
    xc = xb - xb.mean(1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        slope = (xc * (yb - yb.mean(1, keepdims=True))).sum(1) / (xc * xc).sum(1)
    return rho, slope, yb.mean(1) - slope * xb.mean(1)

published = pd.read_csv(OUT / "compare_webs_centrality_vs_tl.csv")
published = published[published.groups == "consumers"].set_index(["network", "measure"]).rho
corr_rows, boots, fits = [], {}, {}
rng = stream(1)
for net in PAPER:
    c = cents[net]
    c = c[c.n_prey > 0]
    for mkey, mlabel in MEASURES:
        x, y = c.trophic_level.to_numpy(float), c[mkey].to_numpy(float)
        rho, p = spearmanr(x, y)
        assert abs(rho - published[(net, mkey)]) < 6e-6, (net, mkey)      # published to 5 dp
        brho, bslope, bicpt = bootstrap(x, y, rng)
        ok = np.isfinite(brho) & np.isfinite(bslope)
        brho, bslope, bicpt = brho[ok], bslope[ok], bicpt[ok]
        perm = rowwise_r(np.tile(rankdata(x), (N_BOOT, 1)),
                         rng.permuted(np.tile(rankdata(y), (N_BOOT, 1)), axis=1))
        slope, icpt = np.polyfit(x, y, 1)
        grid = np.linspace(x.min(), x.max(), 60)
        band = bicpt[:, None] + bslope[:, None] * grid[None, :]
        boots[(net, mkey)] = brho
        fits[(net, mkey)] = (x, y, grid, icpt + slope * grid,
                             np.percentile(band, 2.5, 0), np.percentile(band, 97.5, 0))
        corr_rows.append(dict(
            network=net, site=SITE[net], measure=mkey, label=mlabel, n=len(x), rho=rho,
            rho_lo=np.percentile(brho, 2.5), rho_hi=np.percentile(brho, 97.5),
            p_spearman=p, p_permutation=(1 + (np.abs(perm) >= abs(rho) - 1e-12).sum()) / (N_BOOT + 1),
            slope_per_trophic_level=slope, slope_lo=np.percentile(bslope, 2.5),
            slope_hi=np.percentile(bslope, 97.5), intercept=icpt,
            r_squared=np.corrcoef(x, y)[0, 1] ** 2, bootstrap_resamples_used=int(ok.sum())))
corr = pd.DataFrame(corr_rows)
corr["rho_interval_excludes_zero"] = (corr.rho_lo > 0) | (corr.rho_hi < 0)

diff_rows = []
for mkey, mlabel in MEASURES:
    for a, b in combinations(PAPER, 2):
        ra, rb = (corr[(corr.network == n_) & (corr.measure == mkey)].iloc[0] for n_ in (a, b))
        k = min(len(boots[(a, mkey)]), len(boots[(b, mkey)]))
        d = boots[(a, mkey)][:k] - boots[(b, mkey)][:k]      # independent resamples of each web
        z = (np.arctanh(ra.rho) - np.arctanh(rb.rho)) / np.sqrt(1.06 / (ra.n - 3) + 1.06 / (rb.n - 3))
        diff_rows.append(dict(measure=mkey, web_a=SITE[a], web_b=SITE[b], rho_a=ra.rho, rho_b=rb.rho,
                              difference=ra.rho - rb.rho, diff_lo=np.percentile(d, 2.5),
                              diff_hi=np.percentile(d, 97.5), fisher_z=z, p_fisher=2 * norm.sf(abs(z))))
cdiff = pd.DataFrame(diff_rows)
cdiff["interval_excludes_zero"] = (cdiff.diff_lo > 0) | (cdiff.diff_hi < 0)

# ---------------------------------------------------------------- 3. groups of nodes
BANDS = [("primary consumers (TL < 2.5)", lambda tl: tl < 2.5),
         ("mid-level consumers (2.5 ≤ TL < 3.5)", lambda tl: (tl >= 2.5) & (tl < 3.5)),
         ("upper consumers (TL ≥ 3.5)", lambda tl: tl >= 3.5)]

def group_tests(net, grouping, labels, c):
    rows = []
    for mkey, mlabel in MEASURES:
        samples = {g: c.loc[labels == g, mkey].to_numpy(float) for g in pd.unique(labels)}
        samples = {g: v for g, v in samples.items() if len(v) >= 3}     # too few to test otherwise
        if len(samples) < 2:
            continue
        n = sum(len(v) for v in samples.values())
        desc = "; ".join(f"{g}: n {len(v)}, median {np.median(v):.3g}" for g, v in samples.items())
        if len(samples) > 2:
            Hs, p = kruskal(*samples.values())
            rows.append(dict(network=net, site=SITE[net], grouping=grouping, measure=mkey,
                             test="Kruskal-Wallis", groups=desc, n=n, statistic=Hs, p=p,
                             p_holm=np.nan, effect=Hs / (n - 1), effect_name="epsilon squared"))
        pairs = []
        for g1, g2 in combinations(samples, 2):
            U, p = mannwhitneyu(samples[g1], samples[g2], alternative="two-sided")
            pairs.append(dict(network=net, site=SITE[net], grouping=grouping, measure=mkey,
                              test="Mann-Whitney", groups=f"{g1} vs {g2}",
                              n=len(samples[g1]) + len(samples[g2]), statistic=U, p=p,
                              effect=2 * U / (len(samples[g1]) * len(samples[g2])) - 1,
                              effect_name="Cliff's delta (first minus second)"))
        for row, ph in zip(pairs, holm([r["p"] for r in pairs])):
            row["p_holm"] = ph
        rows += pairs
    return rows

grp_rows = []
for net in PAPER:
    c = cents[net]
    c = c[c.n_prey > 0]
    band = pd.Series(np.select([f(c.trophic_level) for _, f in BANDS], [b for b, _ in BANDS], default=""),
                     index=c.index)
    grp_rows += group_tests(net, "trophic band", band, c)
c = cents["FW_005"]
c = c[c.n_prey > 0]
grp_rows += group_tests("FW_005", "taxonomic category", cadiz_cat.reindex(c.index), c)
groups = pd.DataFrame(grp_rows)

# ---------------------------------------------------------------- 4. node removal
# The 1000 random orders are the ones compare_webs.py draws: one generator,
# seeded once, used for the webs in turn. Drawing them the same way keeps the
# random R50 here identical to the one in compare_webs_robustness.csv.
rng = np.random.default_rng(SEED)
random_orders = {}
for net, _ in WEBS:
    living = sorted(n for n in webs[net]["G"] if webs[net]["G"].nodes[n]["living"])
    random_orders[net] = [list(rng.permutation(living)) for _ in range(N_RANDOM)]

def r50_of(lost):
    return np.argmax(lost >= 0.5) / (len(lost) - 1)

def area_of(lost):
    """Area under the share-lost curve. 0.5 = no secondary extinctions at all
    (the diagonal); 1 = everything is lost at the first removal."""
    return (lost[:-1] + lost[1:]).sum() / 2 / (len(lost) - 1)      # trapezoid rule

pub_rob = pd.read_csv(OUT / "compare_webs_robustness.csv")              # published to 4 dp
pub_rob = pub_rob[pub_rob.measure == "R50"].set_index(["network", "rule", "order"])
rem_rows, curve_rows, rand_stats = [], [], {}
tie_rng = stream(3)
for net in PAPER:
    w = webs[net]
    G, t = w["G"], w["traits"]
    cas = Cascade(G)
    living = sorted(n for n in G if G.nodes[n]["living"])
    n_liv = len(living)
    btw = nx.betweenness_centrality(simple(G))
    # (score, descending?) for each targeted order; scores rounded so that
    # floating-point noise does not hide a tie
    scores = {"most connected first": (t.total_degree.to_dict(), True),
              "least connected first": (t.total_degree.to_dict(), False),
              "highest betweenness first": ({n: round(v, 12) for n, v in btw.items()}, True),
              "most important prey first": ({n: round(v, 12) for n, v in t.out_strength.items()}, True),
              "lowest trophic level first": (t.trophic_level.to_dict(), False),
              "highest trophic level first": (t.trophic_level.to_dict(), True)}

    def sequence(order, theta):
        """Share of living groups lost after 0, 1, ..., n_liv removals."""
        present, lost = set(G), [0.0]
        for n in order:
            if n not in present:
                continue                       # already lost to a secondary extinction
            present, _ = cas.run([n], theta, present)
            lost.append(sum(1 for m in living if m not in present) / n_liv)
        return np.array(lost + [lost[-1]] * (n_liv + 1 - len(lost)))

    def ranked(score, descending, tiebreak):
        sign = -1 if descending else 1
        return sorted(living, key=lambda n: (sign * score[n], tiebreak[n]))

    x = np.arange(n_liv + 1) / n_liv
    for theta, rule in RULES:
        rand = np.array([sequence(o, theta) for o in random_orders[net]])
        rr50 = np.array([r50_of(c) for c in rand])
        rarea = np.array([area_of(c) for c in rand])
        rand_stats[(net, rule)] = (rr50, rarea)
        pub = pub_rob.loc[(net, rule, "random")]
        assert abs(rr50.mean() - pub.value) < 6e-5 and abs(np.percentile(rr50, 2.5) - pub.random_lo) < 6e-5 \
            and abs(np.percentile(rr50, 97.5) - pub.random_hi) < 6e-5, (net, rule)
        rem_rows.append(dict(network=net, site=SITE[net], rule=rule, order="random", trials=N_RANDOM,
                             groups_tied=np.nan, R50=rr50.mean(), R50_lo=np.percentile(rr50, 2.5),
                             R50_hi=np.percentile(rr50, 97.5), R50_sd=rr50.std(ddof=1),
                             area=rarea.mean(), area_lo=np.percentile(rarea, 2.5),
                             area_hi=np.percentile(rarea, 97.5), area_sd=rarea.std(ddof=1)))
        curve_rows.append(pd.DataFrame(dict(network=net, site=SITE[net], rule=rule, order="random",
                                            frac_removed=x, frac_lost=rand.mean(0),
                                            lo=np.percentile(rand, 2.5, 0), hi=np.percentile(rand, 97.5, 0))))
        for name in ORDERS:
            score, desc = scores[name]
            canon = sequence(ranked(score, desc, {n: n for n in living}), theta)   # ties by name, as published
            assert abs(r50_of(canon) - pub_rob.loc[(net, rule, name)].value) < 6e-5, (net, rule, name)
            counts = pd.Series([score[n] for n in living]).value_counts()
            tied = int(counts[counts > 1].sum())
            trials = np.array([sequence(ranked(score, desc, dict(zip(living, tie_rng.random(n_liv)))), theta)
                               for _ in range(N_TIES)]) if tied else canon[None, :]
            t50 = np.array([r50_of(c) for c in trials])
            tarea = np.array([area_of(c) for c in trials])
            row = dict(network=net, site=SITE[net], rule=rule, order=name, trials=len(trials),
                       groups_tied=tied, R50=r50_of(canon), R50_lo=t50.min(), R50_hi=t50.max(),
                       R50_sd=t50.std(ddof=1) if tied else 0.0, R50_tie_mean=t50.mean(),
                       area=area_of(canon), area_lo=tarea.min(), area_hi=tarea.max(),
                       area_sd=tarea.std(ddof=1) if tied else 0.0, area_tie_mean=tarea.mean())
            # Monte Carlo test against the random orders, on the run with ties
            # broken by name (the one in the published tables and figures).
            # A random order that ties with the targeted order counts as "at
            # least as extreme" (<=, >=): the conservative choice. It matters
            # for R50, where many random orders land on the same step, so the
            # share that tie is reported too. The same test on every tie-break
            # trial gives the range of p-values the ties could produce.
            def mc_p(obs, null):
                lo = (1 + (null <= obs + 1e-12).sum()) / (N_RANDOM + 1)
                hi = (1 + (null >= obs - 1e-12).sum()) / (N_RANDOM + 1)
                return min(1.0, 2 * min(lo, hi))
            for stat, obs, tr, null in (("R50", r50_of(canon), t50, rr50),
                                        ("area", area_of(canon), tarea, rarea)):
                ps = [mc_p(v, null) for v in tr]
                row[f"{stat}_z"] = (obs - null.mean()) / null.std(ddof=1)
                row[f"{stat}_p_two_sided"] = mc_p(obs, null)
                row[f"{stat}_p_min_over_ties"], row[f"{stat}_p_max_over_ties"] = min(ps), max(ps)
                row[f"{stat}_frac_random_strictly_below"] = (null < obs - 1e-12).mean()
                row[f"{stat}_frac_random_equal"] = (np.abs(null - obs) <= 1e-12).mean()
            rem_rows.append(row)
            curve_rows.append(pd.DataFrame(dict(network=net, site=SITE[net], rule=rule, order=name,
                                                frac_removed=x, frac_lost=trials.mean(0),
                                                lo=trials.min(0), hi=trials.max(0))))
removal = pd.DataFrame(rem_rows)
curves = pd.concat(curve_rows, ignore_index=True)

con_rows = []
for net in PAPER:                      # the two rules, on the same 1000 random orders (paired)
    for stat, i in (("R50", 0), ("area", 1)):
        a, b = rand_stats[(net, RULES[0][1])][i], rand_stats[(net, RULES[1][1])][i]
        d = b - a
        W, p = wilcoxon(a, b) if np.any(d != 0) else (np.nan, 1.0)
        con_rows.append(dict(contrast="half of diet lost minus all prey lost (same random orders)",
                             statistic=stat, a=SITE[net], b=SITE[net], median_a=np.median(a),
                             median_b=np.median(b), median_difference=np.median(d),
                             test="Wilcoxon signed-rank", test_statistic=W, p=p,
                             effect=(d < 0).mean() if stat == "R50" else (d > 0).mean(),
                             effect_name="share of random orders in which the half-diet rule is the more damaging"))
for theta, rule in RULES:              # the webs against each other, random orders
    for stat, i in (("R50", 0), ("area", 1)):
        for a, b in combinations(PAPER, 2):
            xa, xb = rand_stats[(a, rule)][i], rand_stats[(b, rule)][i]
            U, p = mannwhitneyu(xa, xb, alternative="two-sided")
            con_rows.append(dict(contrast=f"between webs, random orders, rule: {rule}", statistic=stat,
                                 a=SITE[a], b=SITE[b], median_a=np.median(xa), median_b=np.median(xb),
                                 median_difference=np.median(xa) - np.median(xb), test="Mann-Whitney",
                                 test_statistic=U, p=p, effect=2 * U / (len(xa) * len(xb)) - 1,
                                 effect_name="Cliff's delta (a minus b)"))
contrasts = pd.DataFrame(con_rows)

# ---------------------------------------------------------------- write tables
baseline.round(4).to_csv(OUT / "compare_webs_stats_baseline.csv")
centz.round(4).to_csv(OUT / "compare_webs_stats_centralization_vs_random.csv", index=False)
corr.round(5).to_csv(OUT / "compare_webs_stats_correlations.csv", index=False)
cdiff.round(5).to_csv(OUT / "compare_webs_stats_correlation_differences.csv", index=False)
groups.round(5).to_csv(OUT / "compare_webs_stats_group_tests.csv", index=False)
removal.round(5).to_csv(OUT / "compare_webs_stats_removal.csv", index=False)
curves.round(5).to_csv(OUT / "compare_webs_stats_removal_curves.csv", index=False)
contrasts.round(5).to_csv(OUT / "compare_webs_stats_removal_contrasts.csv", index=False)

def fmt(v):
    if isinstance(v, (int, np.integer)) or float(v).is_integer():
        return f"{int(v)}"
    return f"{v:.3f}" if abs(v) < 10 else f"{v:.2f}"
tex = ("\\begin{tabular}{l" + "c" * len(PAPER) + "}\n\\hline\n & "
       + " & ".join(SITE[n] for n in PAPER) + " \\\\\n\\hline\n"
       + "\n".join(f"{k.replace('^2', '$^2$')} & " + " & ".join(fmt(baseline.at[k, SITE[n]]) for n in PAPER)
                   + " \\\\" for k in baseline.index)
       + "\n\\hline\n\\end{tabular}\n")
(OUT / "compare_webs_stats_baseline_table.tex").write_text(tex)

# ---------------------------------------------------------------- figures
use_style()
figs = []                                        # file names, for the README

def web_legend(ax, y, extra=()):
    h = [Line2D([], [], ls="", marker=STYLE[n][1], color=STYLE[n][0], markersize=4.5, label=SITE[n])
         for n in PAPER] + list(extra)
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.4, y), frameon=False,
              ncol=1, handletextpad=0.3)

# trophic level against each measure: points, least-squares line, bootstrap band
for net in PAPER:
    col, mk = STYLE[net]
    tag = TAG[net]
    for mkey, mlabel in MEASURES:
        x, y, grid, line, lo, hi = fits[(net, mkey)]
        r = corr[(corr.network == net) & (corr.measure == mkey)].iloc[0]
        fig, ax = plt.subplots(figsize=(COLUMN, 2.5))
        ax.fill_between(grid, lo, hi, color=GREY, alpha=0.28, lw=0)
        ax.plot(grid, line, color=INK, lw=1.2)
        ax.scatter(x, y, s=15, color=col, marker=mk, edgecolor="white", linewidth=0.3, zorder=3)
        ax.set_xlabel("trophic level")
        ax.set_ylabel(mlabel)
        ax.set_ylim(bottom=-0.04 * y.max())      # none of the measures can be negative; room for points at 0
        ax.text(0, 1.03, minus(f"{SITE[net]}, {r.n} consumer groups\nSpearman ρ = {r.rho:+.2f} "
                               f"(95% interval {r.rho_lo:+.2f} to {r.rho_hi:+.2f})"),
                transform=ax.transAxes, fontsize=6.5, color=INK2, va="bottom", linespacing=1.25)
        tidy(ax)
        ax.legend(handles=[Line2D([], [], ls="", marker=mk, color=col, markersize=4.5,
                                  label=wrap_label("one consumer group", 40)),
                           Line2D([], [], color=INK, lw=1.2, label=wrap_label("least-squares line", 40)),
                           Patch(color=GREY, alpha=0.28, label=wrap_label("95% bootstrap band for the line", 40))],
                  loc="upper center", bbox_to_anchor=(0.4, -0.2), frameon=False)
        stem = f"{P}fit_{tag}_{mkey}"
        save(fig, FOLDER, stem)
        figs.append(stem)

# rho with its interval, every measure, three webs
fig, ax = plt.subplots(figsize=(COLUMN, 0.5 * len(MEASURES) + 0.9))
ybase = np.arange(len(MEASURES))[::-1]
for (net, off) in zip(PAPER, (0.24, 0.0, -0.24)):
    col, mk = STYLE[net]
    for yb, (mkey, _) in zip(ybase, MEASURES):
        r = corr[(corr.network == net) & (corr.measure == mkey)].iloc[0]
        ax.plot([r.rho_lo, r.rho_hi], [yb + off] * 2, color=col, lw=1.1, zorder=2)
        ax.scatter([r.rho], [yb + off], s=18, marker=mk, zorder=3, linewidth=0.9, edgecolor=col,
                   color=col if r.rho_interval_excludes_zero else "white")
ax.axvline(0, color=INK2, lw=0.6, ls=(0, (1, 1.5)))
ax.set_yticks(ybase, [wrap_label(l, 16) for _, l in MEASURES], fontsize=6.5)
ax.set_xlim(-1, 1)
ax.set_xlabel("Spearman ρ with trophic level\n(bar: bootstrap 95% interval)")
tidy(ax, "x")
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
web_legend(ax, -0.2, [Line2D([], [], ls="", marker="o", color=INK2, markerfacecolor="white",
                             markersize=4.5, label=wrap_label("open marker: interval includes 0", 40))])
save(fig, FOLDER, P + "rho_intervals")
figs.append(P + "rho_intervals")

# removal curves with their spread
DASH = (0, (4, 1.5))
SETS = [("centrality", "most connected first", "highest betweenness first"),
        ("trophic", "lowest trophic level first", "highest trophic level first")]
for net in PAPER:
    tag = TAG[net]
    for theta, rule in RULES:
        cr = curves[(curves.network == net) & (curves.rule == rule)]
        rs = removal[(removal.network == net) & (removal.rule == rule)].set_index("order")
        rnd = cr[cr.order == "random"]
        for stag, o1, o2 in SETS:
            fig, ax = plt.subplots(figsize=(COLUMN, 2.5))
            ax.plot([0, 1], [0, 1], color=INK2, lw=0.7, ls=(0, (1, 1.5)))
            ax.axhline(0.5, color=GRID, lw=0.6)
            ax.fill_between(rnd.frac_removed, rnd.lo, rnd.hi, color=GREY, alpha=0.25, lw=0)
            ax.plot(rnd.frac_removed, rnd.frac_lost, color=GREY, lw=1.2)
            handles = []
            for o, c_, ls in ((o1, BLUE, "-"), (o2, ORANGE, DASH)):
                d = cr[cr.order == o]
                ax.fill_between(d.frac_removed, d.lo, d.hi, color=c_, alpha=0.22, lw=0)
                ax.plot(d.frac_removed, d.frac_lost, color=c_, lw=1.4, ls=ls)
                handles.append(Line2D([], [], color=c_, lw=1.4, ls=ls,
                                      label=f"{o}\nR50 {rs.at[o, 'R50']:.2f}; against random orders, {ptxt(rs.at[o, 'area_p_two_sided'])}"))
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1.02)
            ax.set_xlabel("share of living groups removed")
            ax.set_ylabel("share of living groups lost")
            ax.text(0, 1.03, f"{SITE[net]} · rule: {rule}", transform=ax.transAxes, fontsize=6.5, color=INK2)
            tidy(ax)
            handles += [Line2D([], [], color=GREY, lw=1.2,
                               label=wrap_label(f"random order, mean and 95% range of {N_RANDOM} (R50 {rs.at['random', 'R50']:.2f})", 40)),
                        Line2D([], [], color=INK2, lw=0.7, ls=(0, (1, 1.5)), label=wrap_label("no secondary extinctions", 40))]
            ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.45, -0.2), frameon=False)
            stem = f"{P}removal_{tag}_{'all_prey' if theta == 1 else 'half_diet'}_{stag}"
            save(fig, FOLDER, stem)
            figs.append(stem)

# R50 and area at a glance: every order, three webs, with spread and significance
SHOW = ["random", "most connected first", "highest betweenness first", "most important prey first",
        "lowest trophic level first", "highest trophic level first"]
for stat, xlabel, ref in (("R50", "R50: share of living groups removed\nbefore half are lost (lower = more fragile)", None),
                          ("area", "area under the share-lost curve\n(0.5 = no secondary extinctions; higher = more fragile)", 0.5)):
    for theta, rule in RULES:
        fig, ax = plt.subplots(figsize=(COLUMN, 0.5 * len(SHOW) + 0.9))
        ybase = np.arange(len(SHOW))[::-1]
        for net, off in zip(PAPER, (0.24, 0.0, -0.24)):
            col, mk = STYLE[net]
            rs = removal[(removal.network == net) & (removal.rule == rule)].set_index("order")
            for yb, o in zip(ybase, SHOW):
                r = rs.loc[o]
                ax.plot([r[f"{stat}_lo"], r[f"{stat}_hi"]], [yb + off] * 2, color=col,
                        lw=2.4 if o == "random" else 1.1, alpha=0.45 if o == "random" else 1, zorder=2)
                differs = o == "random" or r[f"{stat}_p_two_sided"] < ALPHA
                ax.scatter([r[stat]], [yb + off], s=18, marker=mk, zorder=3, linewidth=0.9, edgecolor=col,
                           color=col if differs else "white")
        if ref is not None:
            ax.axvline(ref, color=INK2, lw=0.6, ls=(0, (1, 1.5)))
        ax.set_yticks(ybase, [wrap_label(o, 18) for o in SHOW], fontsize=6.5)
        ax.set_xlabel(xlabel)
        tidy(ax, "x")
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
        ax.text(0, 1.03, f"rule: {rule}", transform=ax.transAxes, fontsize=6.5, color=INK2)
        web_legend(ax, -0.2, [Line2D([], [], ls="", marker="o", color=INK2, markerfacecolor="white", markersize=4.5,
                                     label=wrap_label(f"open marker: not different from random (p ≥ {ALPHA})", 40)),
                              Line2D([], [], color=INK2, lw=2.4, alpha=0.45, label=wrap_label(f"95% range of {N_RANDOM} random orders", 40)),
                              Line2D([], [], color=INK2, lw=1.1, label=wrap_label(f"range over {N_TIES} tie-breaks", 40))])
        stem = f"{P}{stat.lower()}_intervals_{'all_prey' if theta == 1 else 'half_diet'}"
        save(fig, FOLDER, stem)
        figs.append(stem)

# centralization against random graphs
CZ = ["degree centralization", "betweenness centralization"]
fig, ax = plt.subplots(figsize=(COLUMN, 0.62 * len(CZ) + 0.9))
ybase = np.arange(len(CZ))[::-1]
for net, off in zip(PAPER, (0.24, 0.0, -0.24)):
    col, mk = STYLE[net]
    for yb, k in zip(ybase, CZ):
        r = centz[(centz.network == net) & (centz.measure == k)].iloc[0]
        ax.plot([r.random_lo, r.random_hi], [yb + off] * 2, color=col, lw=2.4, alpha=0.45, zorder=2)
        ax.scatter([r.observed], [yb + off], s=18, marker=mk, zorder=3, linewidth=0.9, edgecolor=col,
                   color=col if r.p_two_sided < ALPHA else "white")
ax.set_yticks(ybase, [wrap_label(k, 14) for k in CZ], fontsize=6.5)
ax.set_xlim(left=0)
ax.set_xlabel("Freeman centralization (0 = all groups equal, 1 = a star)")
tidy(ax, "x")
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
web_legend(ax, -0.32, [Line2D([], [], color=INK2, lw=2.4, alpha=0.45,
                              label=wrap_label(f"95% range, {N_NULL} random graphs, same nodes and links", 40)),
                       Line2D([], [], ls="", marker="o", color=INK2, markerfacecolor="white", markersize=4.5,
                              label=wrap_label(f"open marker: not different from random (p ≥ {ALPHA})", 40))])
save(fig, FOLDER, P + "centralization_vs_random")
figs.append(P + "centralization_vs_random")

# Cadiz: the taxonomic categories of the scatter plots, as groups
c = cents["FW_005"]
c = c[c.n_prey > 0]
cats = ["invertebrates & plankton", "fishes", "marine mammals, birds, turtles"]
CAT_STYLE = dict(zip(cats, ((BLUE, "o"), (ORANGE, "s"), (AQUA, "^"))))
jit = stream(4)
for mkey, mlabel in MEASURES[:4]:
    kw = groups[(groups.network == "FW_005") & (groups.grouping == "taxonomic category")
                & (groups.measure == mkey) & (groups.test == "Kruskal-Wallis")].iloc[0]
    fig, ax = plt.subplots(figsize=(COLUMN, 2.3))
    for i, cat in enumerate(cats):
        v = c.loc[cadiz_cat.reindex(c.index) == cat, mkey].to_numpy(float)
        col, mk = CAT_STYLE[cat]
        ax.scatter(i + jit.uniform(-0.16, 0.16, len(v)), v, s=15, color=col, marker=mk,
                   edgecolor="white", linewidth=0.3, zorder=3)
        q1, med, q3 = np.percentile(v, [25, 50, 75])
        ax.plot([i - 0.28, i + 0.28], [med, med], color=INK, lw=1.3, zorder=4)
        ax.plot([i + 0.34] * 2, [q1, q3], color=INK2, lw=1.0, zorder=4)
    ax.set_xticks(range(len(cats)), [wrap_label(f"{cat} (n = {(cadiz_cat.reindex(c.index) == cat).sum()})", 18)
                                     for cat in cats], fontsize=6.5)
    ax.set_xlim(-0.6, len(cats) - 0.4)
    ax.set_ylim(bottom=-0.04 * c[mkey].max())          # so groups at 0 are not cut off by the axis
    ax.set_ylabel(mlabel)
    ax.text(0, 1.03, f"Kruskal–Wallis H = {kw.statistic:.1f}, {ptxt(kw.p)}", transform=ax.transAxes,
            fontsize=6.5, color=INK2)
    tidy(ax, "y")
    ax.legend(handles=[Line2D([], [], color=INK, lw=1.3, label=wrap_label("median", 40)),
                       Line2D([], [], color=INK2, lw=1.0, label=wrap_label("middle half of the groups (quartiles)", 40))],
              loc="upper center", bbox_to_anchor=(0.4, -0.22), frameon=False)
    stem = f"{P}groups_cadiz_{mkey}_by_category"
    save(fig, FOLDER, stem)
    figs.append(stem)

# ---------------------------------------------------------------- README and note
def num(v):
    """A signed number with two decimals, or three significant figures when it is small."""
    return f"{v:+.2f}" if abs(v) >= 0.1 else f"{v:+.3g}"

def joined(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]

def differs(stat, rule):
    """For each web, the targeted orders that differ from random on this statistic."""
    parts = []
    for net in PAPER:
        rs = removal[(removal.network == net) & (removal.rule == rule) & (removal.order != "random")
                     & removal.order.isin(SHOW)]
        hit = rs[rs[f"{stat}_p_two_sided"] < ALPHA].order.tolist()
        parts.append(f"{SITE[net]} ({joined(hit) if hit else 'none'})")
    return "; ".join(parts) + "."

DESCR = {}
flat = [(l, [SITE[n] for n in PAPER
             if not corr[(corr.network == n) & (corr.measure == k)].rho_interval_excludes_zero.iloc[0]])
        for k, l in MEASURES]
DESCR[P + "rho_intervals"] = (
    "Spearman ρ of each measure with trophic level for the three webs, with its bootstrap 95% interval. "
    "A filled marker means the interval excludes 0. "
    + f"That is the case in all three webs for {joined(l for l, w in flat if not w)}. "
    + " ".join(f"For {l}, the interval includes 0 in the {joined(w)}." for l, w in flat if w))
for theta, rule in RULES:
    tag = "all_prey" if theta == 1 else "half_diet"
    DESCR[f"{P}area_intervals_{tag}"] = (
        f"Area under the share-lost curve for each removal order in the three webs, under the rule “{rule}”. "
        f"The thick bar on the random row is the 95% range of {N_RANDOM} random orders, and a thin bar is the range "
        f"over the {N_TIES} tie-breaks. A filled marker means the order is different from random (p < {ALPHA}). "
        f"Different from random: {differs('area', rule)}")
    DESCR[f"{P}r50_intervals_{tag}"] = (
        f"The same plot for R50, under the rule “{rule}”. R50 moves in steps, so lots of random orders tie with a "
        f"targeted order and the area version is the safer one to read. Different from random: {differs('R50', rule)}")
cz = centz[centz.measure == "degree centralization"].set_index("network")
DESCR[P + "centralization_vs_random"] = (
    f"Degree and betweenness centralization of each web (marker) against the 95% range of {N_NULL} random directed "
    "graphs with the same nodes and links (bar). Degree centralization is "
    + joined(f"{cz.at[n, 'observed']:.2f} in the {SITE[n]}" for n in PAPER)
    + f", against {cz.random_mean.min():.2f} to {cz.random_mean.max():.2f} on average for the random graphs.")
for net in PAPER:
    for mkey, mlabel in MEASURES:
        r = corr[(corr.network == net) & (corr.measure == mkey)].iloc[0]
        DESCR[f"{P}fit_{TAG[net]}_{mkey}"] = minus(
            f"{mlabel.capitalize()} against trophic level for the {r.n} consumers. ρ = {r.rho:+.2f} "
            f"(95% interval {r.rho_lo:+.2f} to {r.rho_hi:+.2f}, permutation {ptxt(r.p_permutation)}). The line "
            f"changes by {num(r.slope_per_trophic_level)} per trophic level ({num(r.slope_lo)} to {num(r.slope_hi)}).")
    for theta, rule in RULES:
        rs = removal[(removal.network == net) & (removal.rule == rule)].set_index("order")
        for stag, o1, o2 in SETS:
            DESCR[f"{P}removal_{TAG[net]}_{'all_prey' if theta == 1 else 'half_diet'}_{stag}"] = (
                f"Rule “{rule}”. Share of living groups lost as groups are removed, with {o1} in blue and {o2} in "
                f"orange (dashed), against {N_RANDOM} random orders in gray (mean and 95% range). The colored bands "
                f"are the range over the {N_TIES} tie-breaks, so no band means the ties do not matter. Against random "
                f"orders: {o1} {ptxt(rs.at[o1, 'area_p_two_sided'])}, {o2} {ptxt(rs.at[o2, 'area_p_two_sided'])}.")
for mkey, mlabel in MEASURES[:4]:
    g = groups[(groups.network == "FW_005") & (groups.grouping == "taxonomic category") & (groups.measure == mkey)]
    kw = g[g.test == "Kruskal-Wallis"].iloc[0]
    pairs = g[(g.test == "Mann-Whitney") & (g.p_holm < ALPHA)].groups.tolist()
    DESCR[f"{P}groups_cadiz_{mkey}_by_category"] = (
        f"{mlabel.capitalize()} of the Gulf of Cadiz consumers by taxonomic category, with the median and the "
        f"quartiles. Kruskal–Wallis H = {kw.statistic:.1f}, {ptxt(kw.p)}. "
        + (f"Pairs that differ after the Holm correction: {joined(pairs)}." if pairs
           else "No pair differs after the Holm correction."))
assert set(DESCR) == set(figs), set(DESCR) ^ set(figs)

# A figure of one web says which web first. write_docs.py reads this table
# when it writes the folder README.
def scope(stem):
    for net in PAPER:
        if f"_{TAG[net]}_" in stem:
            return f"**{SITE[net]}.** "
    return ""
pd.DataFrame([(st, scope(st) + DESCR[st]) for st in sorted(figs)], columns=["figure", "description"]) \
    .to_csv(OUT / "compare_webs_stats_figures.csv", index=False)

def md(df, cols, floatfmt="{:.3f}"):
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(
            (ptxt(r[c]).replace("p = ", "").replace("p < ", "< ") if c.startswith("p") else
             "" if isinstance(r[c], (float, np.floating)) and np.isnan(r[c]) else
             f"{int(r[c])}" if isinstance(r[c], (float, np.floating)) and float(r[c]).is_integer() and abs(r[c]) >= 2 else
             floatfmt.format(r[c]) if isinstance(r[c], (float, np.floating)) else str(r[c])) for c in cols) + " |")
    return "\n".join(out)

short = pd.DataFrame([dict(web=SITE[n], rule=rule,
                           **{"differs from random": joined(h) if (h := removal[
                               (removal.network == n) & (removal.rule == rule) & (removal.order != "random")
                               & (removal.area_p_two_sided < ALPHA)].order.tolist()) else "none"},
                           **{"does not": joined(h2) if (h2 := removal[
                               (removal.network == n) & (removal.rule == rule) & (removal.order != "random")
                               & (removal.area_p_two_sided >= ALPHA)].order.tolist()) else "none"})
                      for n in PAPER for _, rule in RULES])
MARK = "<!-- three-web statistics: written by code/significance.py -->"
note = [f"""{MARK}
## Intervals and tests

Written by `code/significance.py`. The tables are `output/compare_webs_stats_*.csv`.

### What was run

- Each correlation gets a 95% interval from {N_BOOT:,} bootstrap resamples of the consumer groups, and a p-value from {N_BOOT:,} permutations.
- Each centralization is compared with {N_NULL} random directed graphs that have the same number of nodes and links.
- Random-order removal is {N_RANDOM} trials per web and rule (the same orders as `compare_webs.py`).
- A targeted order is a fixed ranking, so it gives the same curve every time unless groups tie on the score. So, each one was run {N_TIES} times with the ties broken at random. Where no groups tie, there is only one possible run.
- Each targeted order is tested against the {N_RANDOM} random orders. The Monte Carlo p-value is the share of random orders that are at least as extreme (two-sided, with ties counted against the targeted order).
- Every removal curve gets two statistics: R50, and the area under the share-lost curve (0.5 means no secondary extinctions). R50 moves in steps of 1 / (number of living groups), so lots of random orders tie with a targeted order. The area does not have that problem.
- Before anything is written, the script checks that its correlations, degree centralization and every R50 equal the values in `compare_webs_*.csv`.
- Unfortunately, link removal is not covered yet, only node removal.

### Which removal orders differ from random

By the area under the curve, at p < {ALPHA}. The full table is further down.

""" + md(short, ["web", "rule", "differs from random", "does not"]),
        "\n### Baseline statistics\n\n" + md(baseline.reset_index(), ["statistic"] + list(SITE.values())),
        "\n### Centralization against random graphs\n\n"
        "One caution on betweenness. The Angolan shelf web has no feeding loops and random directed graphs do, so "
        "shortest paths (and betweenness) are more spread out in the random graphs for a reason that has nothing to do "
        "with which groups are central. Degree centralization does not have this problem.\n\n"
        + md(centz, ["site", "measure", "observed", "random_mean", "random_lo", "random_hi", "z", "p_two_sided"]),
        "\n### Trophic level against each measure (consumers)\n\n"
        "`rho` is Spearman's ρ, `rho_lo` and `rho_hi` are its bootstrap 95% interval, and the slope is the "
        "least-squares slope per unit of trophic level.\n\n"
        + md(corr, ["site", "measure", "n", "rho", "rho_lo", "rho_hi", "p_permutation",
                    "slope_per_trophic_level", "slope_lo", "slope_hi"]),
        "\n### Do the correlations differ between webs?\n\n"
        "If the interval for the difference includes 0, the two webs cannot be told apart on that measure.\n\n"
        + md(cdiff, ["measure", "web_a", "web_b", "rho_a", "rho_b", "difference", "diff_lo", "diff_hi",
                     "p_fisher", "interval_excludes_zero"]),
        "\n### Differences between groups of nodes\n\n"
        "Kruskal–Wallis across all the groups at once (the effect is epsilon squared). Groups with fewer than 3 "
        "members are left out, so Mondego has only two bands and no test. The pairwise Mann–Whitney tests are in "
        "`compare_webs_stats_group_tests.csv`.\n\n"
        + md(groups[groups.test == "Kruskal-Wallis"], ["site", "grouping", "measure", "groups", "statistic", "p", "effect"]),
        "\n### Node removal: each order against random orders\n\n"
        "`R50_lo`, `R50_hi`, `area_lo` and `area_hi` are the 95% range for random order, and the range over the "
        "tie-breaks for a targeted order.\n\n"
        + md(removal, ["site", "rule", "order", "trials", "groups_tied", "R50", "R50_lo", "R50_hi",
                       "R50_p_two_sided", "area", "area_lo", "area_hi", "area_z", "area_p_two_sided"]),
        "\n### Node removal: rules and webs compared\n\n"
        f"These tests use the {N_RANDOM} simulated random orders as the sample. With simulated data the p-value "
        "shrinks as you run more orders, so read the effect size and not the p-value.\n\n"
        + md(contrasts, ["contrast", "statistic", "a", "b", "median_a", "median_b", "median_difference",
                         "test", "p", "effect"]),
        ""]
note_path = ROOT / "notes" / "07_cross_ecosystem.md"
head = note_path.read_text().split(MARK)[0].rstrip()          # what compare_webs.py wrote
note_path.write_text(head + "\n\n" + "\n".join(note))

print(corr[["site", "measure", "n", "rho", "rho_lo", "rho_hi", "p_permutation"]].round(3).to_string(index=False))
print(removal[["site", "rule", "order", "groups_tied", "R50", "R50_lo", "R50_hi", "R50_p_two_sided",
               "area", "area_p_two_sided"]].round(3).to_string(index=False))
print(f"{len(figs)} figures in figures/{FOLDER}/")
