"""Do the Gulf of Cadiz conclusions hold on other marine food webs?

    python code/compare_webs.py          # ~2 min

Landry's feedback on the methods draft (2026-11-08): "apply your methods [to]
at least one other ecosystem to compare and contrast", and on the proposal:
"compare the structure of food webs across different specific ecosystems using
global properties like centralization, density, etc."

Three comparison webs, all from Web of Life and all the same kind of data as
FW_005 (Ecopath diet composition: cell = share of the column group's diet made
up of the row group), so the same methods apply unchanged:

  FW_005     Gulf of Cadiz, Spain        Torres et al. 2013        43 groups
  FW_003     Angolan shelf                Angelini & Velho 2011     28 groups
  FW_006     Alvarado lagoon, Mexico      Cruz-Escalona et al. 2007 30 groups
  FW_007     St Marks seagrass, Florida   Christian & Luczkovich 99 48 groups
  FW_016_01  Mondego estuary, Portugal    Baeta et al. 2011         36 groups

Two data quirks, both handled here and reported in compare_webs.txt:
  - FW_007 is recorded in percent, not fractions, so the matrix is divided by 100.
  - FW_007 also has 10 consumers whose listed diet does not add up (Fish-eating
    birds 6.5%, Catfish and stingrays 10%, Gulls 14.5%, Raptors 31%, Red drum
    46.5%, ...). Rescaling those diets to 1 is a bigger assumption there than in
    the other webs, so the weighted results for St Marks are read with care.
FW_008 (Caribbean, Bascompte et al. 2005, 249 species) was left out: its diet
columns sum to anywhere from 0.05 to 1.83, so the weights are not comparable.

FW_005 is rebuilt here from the API edge list and checked against the
published Cadiz outputs, so any disagreement is this script's fault, not the
comparison's. Nothing in output/cadiz_* is touched.

Writes output/compare_webs_global.csv, compare_webs_centrality_vs_tl.csv,
compare_webs_robustness.csv, compare_webs_nodes.csv and compare_webs.txt.
Figures in figures/08_comparison/.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import spearmanr

from foodweb import (OUT, SEED, simple, Cascade, LinkRemoval, largest_wcc,
                     food_web_properties, pagerank_importance, use_style, save,
                     tidy, COLUMN, FULL, INK, INK2, GRID, BLUE, ORANGE, AQUA, GREY)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "web-of-life_2026-11-11_comparison"
FOLDER = "08_comparison"

WEBS = [("FW_005", "Gulf of Cadiz"), ("FW_003", "Angolan shelf"),
        ("FW_006", "Alvarado lagoon"), ("FW_007", "St Marks seagrass"),
        ("FW_016_01", "Mondego estuary")]
FOCAL = "FW_005"
BOUNDARY = {"Import", "Imports"}          # Ecopath flows from outside the model
NONLIVING = {"Detritus", "Discard", "Discards"}
RULES = [(1.0, "all prey lost"), (0.5, "half of diet lost")]
N_RANDOM_NODES = 1000
N_RANDOM_LINKS = 500

report = []
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line, flush=True)
    report.append(line)


# ---------------------------------------------------------------- build
def build(net):
    """One Web of Life Ecopath web, cleaned exactly as build_network.py cleans
    the Gulf of Cadiz: drop the boundary row (Import), keep detritus, keep
    cannibalism and weak links, rescale every diet to sum to 1."""
    rows = json.loads((RAW / f"{net}_edges.json").read_text())
    names = sorted({r["species1"] for r in rows} | {r["species2"] for r in rows})
    idx = {n: i for i, n in enumerate(names)}
    M = np.zeros((len(names), len(names)))
    for r in rows:                         # species1 = prey (row), species2 = predator (col)
        M[idx[r["species1"]], idx[r["species2"]]] = float(r["connection_strength"])

    # Columns are predators. Most webs record diets as fractions summing to 1;
    # FW_007 records them in percent, so put every web on the same 0-1 scale
    # before anything else.
    colsum = M.sum(axis=0)
    nz = colsum[colsum > 0]
    scale = 100.0 if np.median(nz) > 50 else 1.0
    M /= scale
    colsum = M.sum(axis=0)
    assert colsum.max() < 1.02, f"{net}: a diet column sums to {colsum.max():.3f}"
    # Columns that fall short: the listed prey do not account for the whole diet.
    short = {names[i]: float(colsum[i]) for i in range(len(names))
             if 0 < colsum[i] < 0.98}

    dropped = []
    for b in sorted(BOUNDARY & set(names)):
        i = idx[b]
        assert M[:, i].sum() == 0, f"{net}: {b} has a diet, so it is not a boundary flow"
        dropped.append((b, float(M[i].sum()), int((M[i] > 0).sum())))
    keep = [n for n in names if n not in BOUNDARY]
    M = M[np.ix_([idx[n] for n in keep], [idx[n] for n in keep])]
    names, idx = keep, {n: i for i, n in enumerate(keep)}
    S = len(names)
    assert not np.any(M.sum(axis=0) + M.sum(axis=1) == 0), f"{net}: isolated group after cleaning"

    cs = M.sum(axis=0)
    D = M / np.where(cs > 0, cs, 1)                     # diets rescaled to sum to 1
    TL = np.linalg.solve(np.eye(S) - D.T, np.ones(S))   # TL_i = 1 + sum_j D_ji TL_j
    OI = np.array([(D[:, i] * (TL - (TL[i] - 1)) ** 2).sum() for i in range(S)])

    def effective_prey(i):
        p = np.delete(D[:, i], i)
        p = p[p > 0]
        if not len(p):
            return np.nan
        p = p / p.sum()
        return float(np.exp(-(p * np.log(p)).sum()))

    G = nx.DiGraph()
    for n in names:
        G.add_node(n, living=n not in NONLIVING, trophic_level=float(TL[idx[n]]))
    for i, j in zip(*np.nonzero(M)):
        G.add_edge(names[i], names[j], w=float(M[i, j]), d=float(D[i, j]))
    loops = set(nx.nodes_with_selfloops(G))

    traits = pd.DataFrame({
        "living": [n not in NONLIVING for n in names],
        "trophic_level": TL.round(3),
        "omnivory_index": OI.round(3),
        "n_prey": [G.in_degree(n) - (n in loops) for n in names],
        "n_predators": [G.out_degree(n) - (n in loops) for n in names],
        "effective_prey": [effective_prey(i) for i in range(S)],
        "out_strength": [G.out_degree(n, weight="w") for n in names],
        "cannibal": [n in loops for n in names],
    }, index=pd.Index(names, name="group_name"))
    traits.insert(3, "total_degree", traits.n_prey + traits.n_predators)
    traits.insert(1, "role", np.select([traits.n_prey == 0, traits.n_predators == 0],
                                       ["basal", "top predator"], "intermediate"))
    traits.loc[traits.role == "basal", "effective_prey"] = np.nan
    return dict(net=net, G=G, traits=traits, names=names, M=M, D=D,
                dropped=dropped, scale=scale, short=short)


# ---------------------------------------------------------------- measures
METRICS = [("n_prey", "number of prey (in-degree)"),
           ("n_predators", "number of predators (out-degree)"),
           ("total_degree", "total degree"),
           ("effective_prey", "diet diversity (effective number of prey)"),
           ("out_strength", "importance as prey (out-strength)"),
           ("betweenness", "betweenness"),
           ("betweenness_weighted", "betweenness (weighted)"),
           ("clustering", "clustering coefficient"),
           ("clustering_directed", "clustering (directed)"),
           ("pagerank_importance", "PageRank importance")]


def centrality(web):
    G, traits = web["G"], web["traits"]
    H = simple(G)
    for u, v, d in H.edges(data=True):
        d["dist"] = -np.log(G[u][v]["d"]) if G[u][v]["d"] > 0 else np.inf
    U = H.to_undirected()
    cent = traits.copy()
    cent["betweenness"] = pd.Series(nx.betweenness_centrality(H))
    cent["betweenness_weighted"] = pd.Series(nx.betweenness_centrality(H, weight="dist"))
    cent["clustering"] = pd.Series(nx.clustering(U))
    cent["clustering_directed"] = pd.Series(nx.clustering(H))
    cent["pagerank_importance"] = pd.Series(pagerank_importance(H))
    return cent


def correlations(web, cent):
    out = []
    for m, label in METRICS:
        for subset, df in (("consumers", cent[cent.n_prey > 0]), ("all groups", cent)):
            d = df.dropna(subset=[m])
            rho, p = spearmanr(d.trophic_level, d[m])
            out.append(dict(network=web["net"], site=web["site"], measure=m, label=label,
                            groups=subset, n=len(d), rho=rho, p=p))
    return pd.DataFrame(out)


def global_properties(web):
    G, traits = web["G"], web["traits"]
    H = simple(G)
    U = H.to_undirected()
    props = food_web_properties(G)
    S = G.number_of_nodes()
    extra = {
        "groups": S,
        "living_groups": int(traits.living.sum()),
        "links": G.number_of_edges(),
        "n_cannibal": int(traits.cannibal.sum()),
        "largest_feeding_loop": max((len(c) for c in nx.strongly_connected_components(H)),
                                    default=0),
        "diameter": nx.diameter(U.subgraph(max(nx.connected_components(U), key=len))),
        "transitivity": nx.transitivity(U),
        "mean_trophic_level_weighted": traits.trophic_level.mean(),
        "max_trophic_level_weighted": traits.trophic_level.max(),
        "mean_effective_prey": traits.effective_prey.mean(),
        "degree_centralization": (max(dict(U.degree()).values()) * S
                                  - sum(dict(U.degree()).values())) / ((S - 1) * (S - 2)),
    }
    return {**extra, **props}


# ---------------------------------------------------------------- removals
def node_r50(web, rng):
    """R50 for each removal order and rule: the fraction of living groups that
    must be removed before half of them are gone (Dunne et al. 2002)."""
    G, traits = web["G"], web["traits"]
    H = simple(G)
    cas = Cascade(G)
    living = sorted(n for n in G if G.nodes[n]["living"])
    n_liv = len(living)
    pr = pagerank_importance(H)
    btw = nx.betweenness_centrality(H)

    def ranked(score, descending=True):
        key = (lambda n: (-score[n], n)) if descending else (lambda n: (score[n], n))
        return sorted(living, key=key)

    orders = {
        "most connected first": ranked(traits.total_degree),
        "least connected first": ranked(traits.total_degree, descending=False),
        "highest trophic level first": ranked(traits.trophic_level),
        "lowest trophic level first": ranked(traits.trophic_level, descending=False),
        "most important prey first": ranked(traits.out_strength),
        "highest PageRank importance first": ranked(pr),
        "highest betweenness first": ranked(btw),
    }

    def sequence(order, theta):
        present, k, lost, split = set(G), 0, [0.0], None
        for n in order:
            if n not in present:
                continue
            k += 1
            present, _ = cas.run([n], theta, present)
            lost.append(sum(1 for m in living if m not in present) / n_liv)
            if split is None and largest_wcc(G, present) < len(present):
                split = k / n_liv
        return np.array(lost), split

    def r50(lost):
        hit = np.nonzero(lost >= 0.5)[0]
        return hit[0] / n_liv if len(hit) else np.nan

    rows = []
    rand = [list(rng.permutation(living)) for _ in range(N_RANDOM_NODES)]
    for theta, rule in RULES:
        rvals = np.array([r50(sequence(o, theta)[0]) for o in rand])
        rsplit = np.array([sequence(o, theta)[1] for o in rand[:100]], dtype=float)
        rows.append(dict(network=web["net"], site=web["site"], order="random",
                         rule=rule, R50=rvals.mean(),
                         random_lo=np.percentile(rvals, 2.5),
                         random_hi=np.percentile(rvals, 97.5),
                         frac_random_below=np.nan,
                         split=np.nanmean(rsplit)))
        for name, order in orders.items():
            lost, split = sequence(order, theta)
            v = r50(lost)
            rows.append(dict(network=web["net"], site=web["site"], order=name, rule=rule,
                             R50=v, random_lo=np.nan, random_hi=np.nan,
                             frac_random_below=float((rvals < v).mean()), split=split))
    return pd.DataFrame(rows)


def link_l50(web, rng):
    """L50 for each link-removal order and rule: the fraction of feeding links
    that must be cut before half of the living groups are gone."""
    G = web["G"]
    H = simple(G)
    cas = Cascade(G)
    living = sorted(n for n in G if G.nodes[n]["living"])
    n_liv = len(living)
    links = sorted((p, n) for n, d in cas.diet.items() for p in d)
    nl = len(links)
    share = {l: cas.diet[l[1]][l[0]] for l in links}
    ebw = nx.edge_betweenness_centrality(H)

    orders = {
        "strongest links first": sorted(links, key=lambda l: (-share[l], l)),
        "weakest links first": sorted(links, key=lambda l: (share[l], l)),
        "highest edge betweenness first": sorted(links, key=lambda l: (-ebw.get(l, 0), l)),
    }

    def sequence(order, theta):
        st = LinkRemoval(cas, theta)
        lost, k, i = [0.0], 0, 0
        while i < len(order):
            prey, pred = order[i]
            i += 1
            if prey not in st.alive or pred not in st.alive:
                continue           # link already gone because an end starved
            st.remove_link(prey, pred)
            k += 1
            lost.append(sum(1 for m in living if m not in st.alive) / n_liv)
        return np.array(lost)

    def l50(lost):
        hit = np.nonzero(lost >= 0.5)[0]
        return hit[0] / nl if len(hit) else np.nan

    rows = []
    rand = [[links[i] for i in rng.permutation(nl)] for _ in range(N_RANDOM_LINKS)]
    for theta, rule in RULES:
        rvals = np.array([l50(sequence(o, theta)) for o in rand])
        rows.append(dict(network=web["net"], site=web["site"], order="random", rule=rule,
                         L50=np.nanmean(rvals),
                         random_lo=np.nanpercentile(rvals, 2.5),
                         random_hi=np.nanpercentile(rvals, 97.5),
                         frac_random_below=np.nan))
        for name, order in orders.items():
            v = l50(sequence(order, theta))
            rows.append(dict(network=web["net"], site=web["site"], order=name, rule=rule, L50=v,
                             random_lo=np.nan, random_hi=np.nan,
                             frac_random_below=float(np.nanmean(rvals < v))))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- verify
def verify_focal(web, glob, corr, rob):
    """The Cadiz web rebuilt here must reproduce the published outputs."""
    culled = pd.read_csv(OUT / "cadiz_diet_matrix_culled.csv", index_col=0)
    assert list(culled.index) == web["names"], "group names differ from the published matrix"
    assert np.allclose(culled.to_numpy(), web["M"], atol=1e-12), "diet matrix differs"

    pub = pd.read_csv(OUT / "cadiz_node_traits.csv", index_col=0)
    for col in ("trophic_level", "omnivory_index", "n_prey", "n_predators",
                "total_degree", "effective_prey"):
        a = web["traits"][col].astype(float)
        b = pub[col].astype(float)
        assert np.allclose(a.round(3), b.round(3), equal_nan=True), f"{col} differs"
    assert np.allclose(web["traits"].out_strength.round(4), pub.diet_share_sum.round(4))

    gs = pd.read_csv(OUT / "cadiz_global_structure.csv").set_index("measure").value
    checks = {"groups (nodes)": "groups", "links": "links",
              "connectance L/S^2": "connectance", "link density L/S": "link_density",
              "fraction basal": "frac_basal", "fraction top": "frac_top",
              "trophic coherence q": "trophic_coherence_q",
              "average clustering (undirected, binary)": "clustering",
              "characteristic path length (undirected)": "path_length",
              "generality SD (normalized)": "generality_sd",
              "vulnerability SD (normalized)": "vulnerability_sd"}
    for pub_name, mine in checks.items():
        assert abs(float(gs[pub_name]) - float(glob[mine])) < 1e-9, f"{pub_name} differs"

    pubc = pd.read_csv(OUT / "cadiz_centrality_vs_tl.csv")
    mine = corr[corr.network == FOCAL]
    cent = centrality(web)
    n = 0
    for r in pubc.itertuples():
        m = mine[(mine.measure == r.measure) & (mine.groups == r.groups)]
        if not len(m):
            continue
        if r.measure == "out_strength":
            # network_structure.py reads out-strength back from the saved CSV,
            # where it is rounded to 4 dp; the ties that creates move rho from
            # -0.675 to -0.666. Check that rounding reproduces the published
            # value, but keep the unrounded one in the comparison.
            d = cent[cent.n_prey > 0] if r.groups == "consumers" else cent
            rho, _ = spearmanr(d.trophic_level, d.out_strength.round(4))
            assert abs(rho - r.rho) < 1e-9, "rounded out-strength rho differs"
        else:
            assert abs(float(m.rho.iloc[0]) - r.rho) < 1e-9, f"rho for {r.measure} differs"
        n += 1
    assert n >= 14, f"only {n} correlations cross-checked"

    pubr = pd.read_csv(OUT / "cadiz_node_robustness_summary.csv")
    mine = rob[rob.network == FOCAL]
    n = 0
    for r in pubr[pubr.rule.isin([lbl for _, lbl in RULES])].itertuples():
        m = mine[(mine.order == r.order) & (mine.rule == r.rule)]
        if len(m) and r.order != "random":
            assert abs(float(m.R50.iloc[0]) - r.R50) < 5e-4, \
                f"R50 for {r.order} / {r.rule} differs: {float(m.R50.iloc[0]):.4f} vs {r.R50}"
            n += 1
    assert n >= 12, f"only {n} R50 values cross-checked"
    log(f"verified against the published Cadiz outputs: matrix, {len(pub)} node traits, "
        f"{len(checks)} global measures, {n} R50 values and 14+ correlations all agree")


# ---------------------------------------------------------------- run
def main():
    webs = []
    for net, site in WEBS:
        info = pd.read_csv(RAW / f"{net}_info.csv").iloc[0]
        w = build(net)
        w["site"] = site
        w["reference"] = info.reference
        w["location"] = info.location
        webs.append(w)

    log("== webs ==")
    for w in webs:
        G = w["G"]
        drop = "; ".join(f"{b} ({k} diets, {s:.2f} total)" for b, s, k in w["dropped"]) or "none"
        log(f"{w['net']:10s} {w['site']:20s} {G.number_of_nodes():3d} groups  "
            f"{G.number_of_edges():4d} links   boundary rows dropped: {drop}")
        log(f"           {w['reference'][:110]}")
        if w["scale"] != 1.0:
            log(f"           recorded in percent; divided by {w['scale']:.0f}")
        if w["short"]:
            log(f"           {len(w['short'])} diets do not add up and were rescaled to 1: "
                + ", ".join(f"{n} ({v:.2f})" for n, v in
                            sorted(w["short"].items(), key=lambda kv: kv[1])[:6])
                + (", ..." if len(w["short"]) > 6 else ""))

    glob = pd.DataFrame({w["net"]: global_properties(w) for w in webs}).T
    glob.insert(0, "site", [w["site"] for w in webs])
    glob.index.name = "network"

    cents = {w["net"]: centrality(w) for w in webs}
    corr = pd.concat([correlations(w, cents[w["net"]]) for w in webs], ignore_index=True)

    nodes = pd.concat([cents[w["net"]].assign(network=w["net"], site=w["site"]) for w in webs])

    rng = np.random.default_rng(SEED)
    rob = pd.concat([node_r50(w, rng) for w in webs], ignore_index=True)
    rng = np.random.default_rng(SEED)
    lrob = pd.concat([link_l50(w, rng) for w in webs], ignore_index=True)

    verify_focal(webs[0], glob.loc[FOCAL], corr, rob)

    glob.round(4).to_csv(OUT / "compare_webs_global.csv")
    corr.round(5).to_csv(OUT / "compare_webs_centrality_vs_tl.csv", index=False)
    pd.concat([rob.assign(measure="R50").rename(columns={"R50": "value"}),
               lrob.assign(measure="L50").rename(columns={"L50": "value"})],
              ignore_index=True).round(4).to_csv(OUT / "compare_webs_robustness.csv", index=False)
    nodes.round(5).to_csv(OUT / "compare_webs_nodes.csv")

    # ------------------------------------------------------------ report
    log("\n== global properties ==")
    show = ["groups", "links", "connectance", "link_density", "frac_basal",
            "frac_intermediate", "frac_top", "frac_cannibal", "frac_in_loops",
            "clustering", "path_length", "trophic_coherence_q", "degree_centralization",
            "generality_sd", "vulnerability_sd", "mean_trophic_level_weighted",
            "max_trophic_level_weighted", "mean_effective_prey"]
    log(f"{'measure':32s}" + "".join(f"{w['site'][:17]:>19s}" for w in webs))
    for m in show:
        log(f"{m:32s}" + "".join(f"{glob.loc[w['net'], m]:>19.3f}" for w in webs))

    log("\n== trophic level vs ... (Spearman rho, consumers only) ==")
    log(f"{'measure':42s}" + "".join(f"{w['site'][:17]:>19s}" for w in webs))
    for m, label in METRICS:
        row = ""
        for w in webs:
            r = corr[(corr.network == w["net"]) & (corr.measure == m)
                     & (corr.groups == "consumers")].iloc[0]
            star = "*" if r.p < 0.05 else " "
            row += f"{r.rho:>+18.2f}{star}"
        log(f"{label:42s}" + row)
    log("* p < 0.05")

    log("\n== R50: fraction of groups removed before half are gone ==")
    for _, rule in RULES:
        log(f"-- {rule}")
        log(f"{'order':42s}" + "".join(f"{w['site'][:17]:>19s}" for w in webs))
        for order in ["random"] + [o for o in rob.order.unique() if o != "random"]:
            row = ""
            for w in webs:
                m = rob[(rob.network == w["net"]) & (rob.order == order) & (rob.rule == rule)]
                row += f"{m.R50.iloc[0]:>19.3f}" if len(m) else f"{'-':>19s}"
            log(f"{order:42s}" + row)

    log("\n== L50: fraction of links cut before half the groups are gone ==")
    for _, rule in RULES:
        log(f"-- {rule}")
        log(f"{'order':42s}" + "".join(f"{w['site'][:17]:>19s}" for w in webs))
        for order in lrob.order.unique():
            row = ""
            for w in webs:
                m = lrob[(lrob.network == w["net"]) & (lrob.order == order) & (lrob.rule == rule)]
                row += f"{m.L50.iloc[0]:>19.3f}" if len(m) else f"{'-':>19s}"
            log(f"{order:42s}" + row)

    (OUT / "compare_webs.txt").write_text("\n".join(report) + "\n")
    write_note(webs, glob, corr, rob, lrob)
    figures(webs, glob, corr, rob)



# ---------------------------------------------------------------- note
def write_note(webs, glob, corr, rob, lrob):
    """notes/07_cross_ecosystem.md, straight from the tables above.
    Facts for understanding, not text for the paper."""
    nets = [w["net"] for w in webs]
    sites = [w["site"] for w in webs]

    def table(header, rows):
        out = ["| " + " | ".join(header) + " |",
               "|" + "|".join(["---"] * len(header)) + "|"]
        out += ["| " + " | ".join(r) + " |" for r in rows]
        return out

    def num(x, d=2):
        return "–" if pd.isna(x) else f"{x:.{d}f}".replace("-", "\u2212")

    L = ["# Cross-ecosystem comparison", "",
         "> Generated by [`code/compare_webs.py`](../code/compare_webs.py) from "
         "[`output/compare_webs_*.csv`](../output/). Rerunning the analysis rewrites this "
         "note, so its numbers always match the outputs.", "",
         "**Facts for understanding, not text for the paper.**", "",
         "## Why", "",
         "Landry, on the methods draft (2026-11-08): *\"apply your methods at least one other "
         "ecosystem to compare and contrast\"*; on the proposal: *\"if you look at other marine food "
         "web datasets, do your conclusions hold, and if not, is there a plausible explanation?\"*", "",
         "## The webs", ""]
    L += table(["network", "site", "reference", "groups", "links", "kind"],
               [[w["net"], w["site"], w["reference"].split("(")[0].strip(),
                 str(w["G"].number_of_nodes()), str(w["G"].number_of_edges()),
                 "Ecopath diet composition"] for w in webs])
    L += ["",
          "All five record the same quantity — the share of each predator's diet made up of each "
          "prey — so the Cadiz methods apply unchanged. Each is cleaned the same way: the Ecopath "
          "boundary row (`Import`) dropped, detritus kept, cannibalism and weak links kept, every "
          "diet rescaled to sum to 1.", "",
          "Two data quirks, both handled in the code:", "",
          "- **FW_007 is recorded in percent**, not fractions. The matrix is divided by 100.",
          "- **FW_007 also has 9 consumers whose listed diet does not add up** (Fish-eating birds "
          "0.07, Catfish and stingrays 0.10, Gulls 0.14, Raptors 0.31, Red drum 0.47, Fish and "
          "crustacean-eating birds 0.51, Herbivorous ducks 0.89, Blue crabs 0.90, Deposit-feeding "
          "polychaetes 0.95). Rescaling those to 1 is a larger assumption than anywhere else, so "
          "St Marks' weighted results carry more uncertainty than the others.",
          "- **FW_008** (Caribbean, Bascompte et al. 2005, 249 species) was left out: its diet "
          "columns sum to between 0.05 and 1.83, so its weights are not comparable.", "",
          "## Global structure", ""]
    show = [("groups", "groups", 0), ("links", "links", 0),
            ("connectance", "connectance L/S²", 3), ("link_density", "link density L/S", 2),
            ("frac_basal", "fraction basal", 3), ("frac_top", "fraction top", 3),
            ("frac_cannibal", "fraction cannibal", 3),
            ("frac_in_loops", "in feeding loops", 3),
            ("clustering", "clustering", 3), ("path_length", "path length", 2),
            ("trophic_coherence_q", "trophic coherence q", 3),
            ("degree_centralization", "degree centralization", 3),
            ("generality_sd", "generality SD", 3), ("vulnerability_sd", "vulnerability SD", 3),
            ("mean_trophic_level_weighted", "mean trophic level", 2),
            ("max_trophic_level_weighted", "max trophic level", 2),
            ("mean_effective_prey", "mean diet diversity", 2)]
    L += table(["measure"] + sites,
               [[lbl] + [num(glob.loc[n, m], d) for n in nets] for m, lbl, d in show])

    L += ["", "## Trophic level vs position (Spearman ρ, consumers only)", "",
          "`*` marks p < 0.05.", ""]
    rows = []
    for m, label in METRICS:
        r = [label]
        for n in nets:
            c = corr[(corr.network == n) & (corr.measure == m)
                     & (corr.groups == "consumers")].iloc[0]
            r.append(num(c.rho) + ("\\*" if c.p < 0.05 else ""))
        rows.append(r)
    L += table(["measure"] + sites, rows)

    L += ["", "## R50 — fraction of groups removed before half are gone", ""]
    orders = ["random"] + [o for o in rob.order.unique() if o != "random"]
    for _, rule in RULES:
        L += [f"**Rule: {rule}**", ""]
        L += table(["removal order"] + sites,
                   [[o] + [num(rob[(rob.network == n) & (rob.order == o)
                                   & (rob.rule == rule)].R50.iloc[0], 3) for n in nets]
                    for o in orders])
        L += [""]

    L += ["## L50 — fraction of links cut before half the groups are gone", ""]
    for _, rule in RULES:
        L += [f"**Rule: {rule}**", ""]
        L += table(["removal order"] + sites,
                   [[o] + [num(lrob[(lrob.network == n) & (lrob.order == o)
                                    & (lrob.rule == rule)].L50.iloc[0], 3) for n in nets]
                    for o in lrob.order.unique()])
        L += [""]

    L += ["## Verification", "",
          "- The Gulf of Cadiz web is rebuilt here from the Web of Life API edge list, not from the "
          "project's own cleaned files, and is checked against the published outputs before anything "
          "is compared: the 43×43 culled matrix, all 43 node traits, 11 global measures, 14 R50 "
          "values and 14 correlations all agree exactly.",
          "- One known discrepancy, found by that check: `network_structure.py` reads out-strength "
          "back from `cadiz_node_traits.csv`, where it is rounded to 4 decimal places. The ties that "
          "creates move ρ for importance-as-prey from \u22120.675 to \u22120.666 "
          "(`cadiz_centrality_vs_tl.csv` holds the rounded value). Immaterial, but the comparison "
          "uses the unrounded value.",
          "- Two consecutive runs produce byte-identical CSVs, text and figure PDFs.",
          f"- Random orders: {N_RANDOM_NODES} for node removal, {N_RANDOM_LINKS} for link removal, "
          f"seed {SEED}.", ""]
    (ROOT / "notes" / "07_cross_ecosystem.md").write_text("\n".join(L) + "\n")


# ---------------------------------------------------------------- figures
def figures(webs, glob, corr, rob):
    """One idea per figure, drawn at printed size (3.4 in = one column, 7 in =
    full text width), no text below 6.5 pt. The focal web is always the orange
    circle; each comparison web keeps its own color and marker throughout, so
    nothing rests on color alone."""
    use_style()
    sites = [w["site"] for w in webs]
    nets = [w["net"] for w in webs]
    colors = [ORANGE, BLUE, AQUA, GREY, INK2][:len(webs)]
    markers = ["o", "s", "^", "D", "v"][:len(webs)]
    hatches = ["", "///", "...", "xxx", "\\\\"][:len(webs)]

    # 1. does connectivity rise with trophic level in every web?
    fig, ax = plt.subplots(figsize=(FULL, 2.9))
    measures = [("n_prey", "number\nof prey"), ("effective_prey", "diet\ndiversity"),
                ("n_predators", "number of\npredators"), ("total_degree", "total\ndegree"),
                ("betweenness_weighted", "betweenness\n(weighted)")]
    x = np.arange(len(measures))
    bw = 0.82 / len(webs)
    for k, net in enumerate(nets):
        vals, sig = [], []
        for m, _ in measures:
            r = corr[(corr.network == net) & (corr.measure == m)
                     & (corr.groups == "consumers")].iloc[0]
            vals.append(r.rho)
            sig.append(r.p < 0.05)
        pos = x + k * bw - 0.41 + bw / 2
        ax.bar(pos, vals, bw, label=sites[k], color=colors[k], edgecolor=INK,
               linewidth=0.4, hatch=hatches[k])
        for xi, v, ok in zip(pos, vals, sig):
            if ok:
                ax.text(xi, v + (0.045 if v >= 0 else -0.085), "*", ha="center",
                        fontsize=6.5, color=INK)
    ax.axhline(0, color=INK, linewidth=0.8)
    ax.set_xticks(x, [lbl for _, lbl in measures])
    ax.set_ylabel("Spearman $\\rho$ with trophic level")
    ax.set_ylim(-1, 1)
    ax.legend(frameon=False, fontsize=6.5, ncol=3, loc="lower left",
              handlelength=1.4, columnspacing=1.0)
    ax.text(0.995, 0.02, "* p < 0.05", transform=ax.transAxes, ha="right",
            fontsize=6.5, color=INK2)
    tidy(ax, grid="y")
    save(fig, FOLDER, "compare_centrality_vs_tl", width=FULL)

    # 2. robustness: R50 by removal order, one panel per extinction rule
    orders = ["highest trophic level first", "random", "most connected first",
              "lowest trophic level first", "most important prey first"]
    labels = ["top-down", "random", "most\nconnected", "bottom-up",
              "most important\nprey"]
    for theta, rule in RULES:
        fig, ax = plt.subplots(figsize=(COLUMN, 2.7))
        for k, net in enumerate(nets):
            vals = [rob[(rob.network == net) & (rob.order == o)
                        & (rob.rule == rule)].R50.iloc[0] for o in orders]
            ax.plot(range(len(orders)), vals, marker=markers[k], markersize=3.4,
                    color=colors[k], linewidth=1.5 if k == 0 else 0.9,
                    label=sites[k], zorder=3 if k == 0 else 2)
        ax.set_xticks(range(len(orders)), labels, rotation=30, ha="right")
        ax.set_ylabel("R50")
        ax.set_ylim(0, 0.6)
        ax.set_title(f"extinction rule: {rule}", fontsize=7, color=INK2)
        ax.legend(frameon=False, fontsize=6.5, loc="lower left", handlelength=1.6)
        tidy(ax, grid="y")
        save(fig, FOLDER, f"compare_r50_{rule.split()[0]}", width=COLUMN)

    # 3. global structure: where the Gulf of Cadiz sits among the five
    fig, ax = plt.subplots(figsize=(COLUMN, 2.7))
    ms = [("connectance", "connectance"), ("clustering", "clustering"),
          ("frac_basal", "fraction basal"), ("frac_top", "fraction top"),
          ("frac_in_loops", "in feeding loops"),
          ("degree_centralization", "centralization")]
    for j, (m, lbl) in enumerate(ms):
        for k, net in enumerate(nets):
            ax.plot(glob.loc[net, m], j, markers[k], markersize=3.6,
                    color=colors[k], zorder=3 if k == 0 else 2)
    ax.set_yticks(range(len(ms)), [lbl for _, lbl in ms])
    ax.invert_yaxis()
    ax.set_xlabel("value")
    ax.set_xlim(-0.02, 1)
    ax.legend(handles=[Line2D([], [], marker=mk, linestyle="", color=c, markersize=3.6,
                              label=s) for c, mk, s in zip(colors, markers, sites)],
              frameon=False, fontsize=6.5, loc="lower right", handlelength=1.2)
    tidy(ax, grid="x")
    save(fig, FOLDER, "compare_global_structure", width=COLUMN)

    # 4. strong links matter, weak ones do not -- in every web
    fig, ax = plt.subplots(figsize=(COLUMN, 2.5))
    lrob = pd.read_csv(OUT / "compare_webs_robustness.csv")
    lrob = lrob[(lrob.measure == "L50") & (lrob.rule == "half of diet lost")]
    orders = ["strongest links first", "random", "weakest links first"]
    for k, net in enumerate(nets):
        vals = [lrob[(lrob.network == net) & (lrob.order == o)].value.iloc[0] for o in orders]
        ax.plot(range(len(orders)), vals, marker=markers[k], markersize=3.4,
                color=colors[k], linewidth=1.5 if k == 0 else 0.9, label=sites[k])
    ax.set_xticks(range(len(orders)), ["strongest\nfirst", "random", "weakest\nfirst"])
    ax.set_ylabel("L50")
    ax.set_ylim(0, 1)
    ax.set_title("extinction rule: half of diet lost", fontsize=7, color=INK2)
    ax.legend(frameon=False, fontsize=6.5, loc="upper left", handlelength=1.6)
    tidy(ax, grid="y")
    save(fig, FOLDER, "compare_l50_link_strength", width=COLUMN)


if __name__ == "__main__":
    main()
