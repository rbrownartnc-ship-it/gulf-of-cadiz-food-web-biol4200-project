# Code

Run from the repository root, in this order:

```bash
python code/build_network.py     # data/ -> output/ and figures/  (~5 s)
python code/rq_feasibility.py    # output/ -> output/rq_feasibility.txt
```

| Script | Reads | Writes |
|---|---|---|
| `build_network.py` | `data/web-of-life_2026-10-15_210043/FW_005.csv` | every file in `output/` except `rq_feasibility.txt`, plus both figures in `figures/` (PDF + PNG) |
| `rq_feasibility.py` | `output/cadiz_node_traits.csv` | `output/rq_feasibility.txt` |

The scripts locate the repo from their own path, so they also work when run from inside `code/`. Both are deterministic: the only randomness is the figure layout, which uses a fixed seed (4).

## What `build_network.py` does

1. **Load and check.** Reads the labelled 44 × 44 matrix and confirms that row and column labels match. Also confirms every consumer's column sums to 1, which establishes rows = prey and columns = predators.
2. **Clean.** Removes `Import` (food eaten outside the model area). The other cleaning decisions are written to `output/cadiz_cleaning_log.csv`, one row per step.
3. **Build.** `networkx.DiGraph` with **edges pointing prey → predator** (the direction energy flows), and weight = share of the predator's diet. Use `G.reverse()` for the "who eats whom" convention.
4. **Derive node traits.** See the equations below and the column definitions in [`output/README.md`](../output/README.md).
5. **Save** CSVs, GraphML, a text summary, and an Excel workbook with one sheet per table.
6. **Draw** the diet-matrix heatmap and the food web by trophic level, at their printed size (7 in wide), each as a vector PDF and a 300-dpi PNG. See [`figures/README.md`](../figures/README.md).

Every output is reproducible byte for byte, except the Excel workbook: it stores the time it was saved, so it shows as changed after every run even when its contents are identical.

### Equations

Notation: `D[j, i]` is the share of predator *i*'s diet that is prey *j*, rescaled so each consumer's diet sums to 1.

**Trophic level** (Ecopath convention, basal groups = 1). It is solved exactly as a linear system, with cannibalism included:

$$
TL_i = 1 + \sum_j D_{ji} TL_j
\quad\Longleftrightarrow\quad
(\mathbf{I} - \mathbf{D}^\top) \mathbf{TL} = \mathbf{1}
$$

**Omnivory index** (Christensen & Pauly 1992). It is 0 when every prey item sits on one trophic level:

$$
OI_i = \sum_j D_{ji} \left( TL_j - (TL_i - 1) \right)^2
$$

**Diet diversity** (effective number of prey). Here `p_j` is the diet without the self-loop, rescaled to sum to 1:

$$
\mathrm{effective\ prey}_i = \exp\left( -\sum_j p_j \ln p_j \right)
$$

**Generality / vulnerability**: the number of prey (in-degree) and the number of predators (out-degree), not counting self-loops.

**Importance as prey**: weighted out-degree, using the original (not rescaled) diet shares:

$$
s_j = \sum_i D^{\mathrm{orig}}_{ji}
$$

## What `rq_feasibility.py` does

Spearman rank correlation of trophic level against each of four measures, across the 40 consumers (basal groups excluded). Current output:

| Trophic level vs | ρ | p |
|---|---|---|
| number of prey | +0.75 | 2.9e-08 |
| number of predators | −0.65 | 4.7e-06 |
| total degree | −0.07 | 0.67 |
| effective number of prey | +0.69 | 7.8e-07 |
