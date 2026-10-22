"""Cross-check the structure numbers with igraph, a separate network library.

    python code/checks/verify_with_igraph.py

Recomputes clustering, transitivity, path length, diameter, the largest
strongly connected component, degree assortativity, node betweenness and edge
betweenness from output/cadiz_edges.csv, and compares them with what
network_structure.py, distributions.py and edge_removal.py wrote.
"""
import sys
from pathlib import Path
import pandas as pd
import igraph as ig

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from foodweb import OUT

e = pd.read_csv(OUT / "cadiz_edges.csv")
e = e[e.prey != e.predator]
g = ig.Graph.TupleList(e[["prey", "predator"]].itertuples(index=False), directed=True)
u = g.as_undirected(mode="collapse")
glob = pd.read_csv(OUT / "cadiz_global_structure.csv").set_index("measure").value.astype(float)
pairs = set(zip(e.prey, e.predator))
checks = {
    "average clustering (undirected, binary)": u.transitivity_avglocal_undirected(mode="zero"),
    "transitivity (undirected, binary)": u.transitivity_undirected(),
    "characteristic path length (undirected)": u.average_path_length(directed=False),
    "diameter (undirected)": u.diameter(directed=False),
    "largest strongly connected component": max(g.connected_components(mode="strong").sizes()),
    "degree assortativity (undirected)": u.assortativity_degree(directed=False),
    "mutual predation pairs": sum(1 for a, b in pairs if (b, a) in pairs) / 2,
}
bad = 0
for k, v in checks.items():
    ok = abs(v - glob[k]) < 1e-6
    bad += not ok
    print(f"{k:42s} igraph {v:9.4f}   repo {glob[k]:9.4f}   {'OK' if ok else 'MISMATCH'}")

n = g.vcount()
cent = pd.read_csv(OUT / "cadiz_centrality.csv", index_col=0)
b = dict(zip(g.vs["name"], g.betweenness(directed=True)))
diff = max(abs(b[k] / ((n - 1) * (n - 2)) - cent.at[k, "betweenness"]) for k in b)
print(f"node betweenness, max |difference|: {diff:.1e} (CSV rounded to 5 decimals)")
bad += diff > 1e-4

links = pd.read_csv(OUT / "cadiz_link_knockouts.csv").set_index(["prey", "predator"]).edge_betweenness
eb = g.edge_betweenness(directed=True)
names = g.vs["name"]
diff = max(abs(v / (n * (n - 1)) - links[(names[ed.source], names[ed.target])]) for ed, v in zip(g.es, eb))
print(f"edge betweenness, max |difference|: {diff:.1e} (CSV rounded to 5 decimals)")
bad += diff > 1e-4
if bad:
    raise SystemExit(f"{bad} mismatches")
print("all igraph cross-checks agree")
