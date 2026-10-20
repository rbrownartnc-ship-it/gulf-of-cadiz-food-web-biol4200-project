# Code

Run from the repository root, in this order:

```bash
python code/build_network.py     # data/ -> output/ and figures/  (~5 s)
python code/rq_feasibility.py    # output/ -> output/rq_feasibility.txt
```

| Script | Reads | Writes |
|---|---|---|
| `build_network.py` | `data/web-of-life_2026-10-15_210043/FW_005.csv` | every file in `output/` except `rq_feasibility.txt`, plus both figures in `figures/` |
| `rq_feasibility.py` | `output/cadiz_node_traits.csv` | `output/rq_feasibility.txt` |

The scripts locate the repo from their own path, so they also work when run from inside `code/`. Both are deterministic: the only randomness is the figure layout, which uses a fixed seed (4).

## What `build_network.py` does

1. **Load and check.** Reads the labelled 44 × 44 matrix and confirms that row and column labels match. Also confirms every consumer's column sums to 1, which establishes rows = prey and columns = predators.
2. **Clean.** Removes `Import` (food eaten outside the model area). The other cleaning decisions are written to `output/cadiz_cleaning_log.csv`, one row per step.
3. **Build.** `networkx.DiGraph` with **edges pointing prey → predator** (the direction energy flows), and weight = share of the predator's diet. Use `G.reverse()` for the "who eats whom" convention.
4. **Derive node traits.** See the equations below and the column definitions in [`output/README.md`](../output/README.md).
5. **Save** CSVs, GraphML, a text summary, and an Excel workbook with one sheet per table.
6. **Draw** the diet-matrix heatmap and the food web by trophic level.

### Equations

Let $D_{ji}$ be the share of predator $i$'s diet that is prey $j$, rescaled so each consumer's diet sums to 1.

- **Trophic level** (Ecopath convention): $TL_i = 1 + \sum_j D_{ji}\,TL_j$, with $TL = 1$ for basal groups. Solved exactly as the linear system $(\mathbf{I} - \mathbf{D}^\top)\,\mathbf{TL} = \mathbf{1}$, cannibalism included.
- **Omnivory index** (Christensen & Pauly 1992): $OI_i = \sum_j D_{ji}\,\big(TL_j - (TL_i - 1)\big)^2$. It is 0 when every prey item sits on one trophic level.
- **Diet diversity** (effective number of prey): $\exp\!\big(-\sum_j p_j \ln p_j\big)$, where $p_j$ is the diet without the self-loop, rescaled to sum to 1.
- **Generality / vulnerability**: number of prey (in-degree) and number of predators (out-degree), self-loops not counted.
- **Importance as prey**: weighted out-degree, $\sum_i D_{ji}$, using the original (not rescaled) shares.

## What `rq_feasibility.py` does

Spearman rank correlation of trophic level against each of four measures, across the 40 consumers (basal groups excluded). Current output:

| Trophic level vs | ρ | p |
|---|---|---|
| number of prey | +0.75 | 2.9e-08 |
| number of predators | −0.65 | 4.7e-06 |
| total degree | −0.07 | 0.67 |
| effective number of prey | +0.69 | 7.8e-07 |
