"""Can the data test "higher consumers are more connected / have more diverse
diets"? Rank-correlates trophic level with each kind of degree and with
weighted diet diversity, across the 40 consumers.

    python code/build_network.py     # first, to make output/
    python code/rq_feasibility.py

Writes output/rq_feasibility.txt.
"""
from pathlib import Path
import pandas as pd
from scipy.stats import spearmanr

OUT = Path(__file__).resolve().parents[1] / "output"
nodes = pd.read_csv(OUT / "cadiz_node_traits.csv", index_col=0)
consumers = nodes[nodes.n_prey > 0]                   # basal groups have no diet

lines = [f"consumers: {len(consumers)}"]
for col in ["n_prey", "n_predators", "total_degree", "effective_prey"]:
    rho, p = spearmanr(consumers.trophic_level, consumers[col])
    lines.append(f"trophic level vs {col:15s} rho = {rho:+.2f}   p = {p:.2g}")

lines += ["", "highest total degree:",
          nodes.nlargest(5, "total_degree")
          [["trophic_level", "n_prey", "n_predators", "total_degree"]].to_string()]

print("\n".join(lines))
(OUT / "rq_feasibility.txt").write_text("\n".join(lines) + "\n")
