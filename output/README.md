# Post-processed data

This folder contains all of the secondary data derived from cleaning or analyzing the raw data. Every file is written by the code. **Do not edit by hand**: change the code and rerun it (see [`code/README.md`](../code/README.md)), or the CSVs and the workbook will disagree.

| File | Contents |
|---|---|
| `cadiz_diet_matrix_culled.csv` | **The culled dataset.** 43 × 43 diet matrix with `Import` removed. Rows = prey, columns = predators, cell = share of the predator's diet. The original shares are kept (not rescaled). 411 nonzero cells. |
| `cadiz_cleaning_log.csv` | **Every change made to the original download**, one row per step, with link counts before and after |
| `cadiz_node_traits.csv` | **One row per group, with trophic level and other derived traits.** Columns defined below. |
| `cadiz_edges.csv` | One row per feeding link: `prey`, `predator`, `diet_share` (original), `diet_share_renorm` (diet rescaled to sum to 1). 411 rows, 14 of them self-loops (cannibalism). |
| `cadiz_foodweb.graphml` | The network: weighted `DiGraph`, edges prey → predator, `weight` = diet share. Nodes carry `group` and `trophic_level`. Opens in networkx (`nx.read_graphml`), Gephi, or Cytoscape. |
| `cadiz_foodweb_data.xlsx` | All of the above in one Excel workbook. Sheets: `README`, `culled_diet_matrix`, `cleaning_log`, `node_traits`, `edge_list`, `original_matrix` (the download as-is, with the removed `Import` row shaded). |
| `summary.txt` | Every number `build_network.py` prints (network size, components, top groups by each measure) |
| `rq_feasibility.txt` | Correlations of trophic level with degree and diet diversity (from `rq_feasibility.py`) |

## Changes made to the original dataset

The full record is `cadiz_cleaning_log.csv`. In short:

| Step | Change | Links |
|---|---|---|
| Remove `Import` | Not a functional group: Ecopath's share of a diet eaten **outside the model area**. It appears only in the diets of Loggerhead turtles (0.448) and Seabirds (0.404). Its column (what Import eats) is empty. | 413 → 411 |
| Exports / emigration | Checked for any other boundary flow. There is none in the diet matrix: fishery catches and exports are in the paper's tables, not here. | no change |
| Rescale diets | Without Import, the turtle and seabird diets sum to 0.552 and 0.596. For trophic level, omnivory index and diet diversity, every diet is rescaled to sum to 1. | no change |
| Keep Detritus, Discard | Non-living basal groups, kept as nodes. Without them the web is still connected (41 nodes, 396 links). | no change |
| Keep cannibalism | 14 self-loops are kept, but excluded from prey and predator counts and from diet diversity. | no change |
| Keep weak links | No threshold. Shares go down to 1e-6; 120 links are below 0.01. | no change |

## `cadiz_node_traits.csv` columns

| Column | Definition |
|---|---|
| `group_name` | Functional group (node). These are groups, not species. |
| `category` | Broad type, assigned from the group name: fishes · invertebrates & plankton · marine mammals, birds, turtles · non-living |
| `living` | False for Detritus and Discard |
| `role` | `basal` = eats nothing · `top predator` = eaten by no other group · otherwise `intermediate` (cannibalism ignored) |
| `trophic_level` | $1 + \sum_j D_{ji} TL_j$ over prey $j$; basal = 1. Uses the rescaled diets. |
| `omnivory_index` | Diet-weighted variance of prey trophic levels around $TL_i - 1$ (Christensen & Pauly 1992). 0 = feeds on one level. |
| `n_prey` | Number of prey groups (in-degree, "generality"), self not counted |
| `n_predators` | Number of predator groups (out-degree, "vulnerability"), self not counted |
| `total_degree` | `n_prey + n_predators` |
| `effective_prey` | Diet diversity: exp(Shannon entropy) of the rescaled diet without cannibalism. Empty for basal groups. |
| `diet_share_sum` | Sum of this group's share across all predators' diets (weighted out-degree): importance as prey |
| `cannibal` | True if the group eats itself |
| `cannibalism_share` | Share of the group's own diet that is itself |
| `import_share_removed` | Share of the diet that was `Import` and was removed (nonzero for 2 groups) |
| `diet_total_original` | Sum of the diet column before cleaning (≈1 for consumers, 0 for basal) |
| `in_feeding_loop` | True if the group is in a feeding loop, i.e. a strongly connected component larger than one group (23 groups) |

⚠️ The **trophic levels of Loggerhead turtles (3.18) and Seabirds (3.09)** depend on the rescaling step. That step assumes food eaten outside the area has the same make-up as the local diet. Both groups also get about 45% of their diet from Discard (trophic level 1), which is why their omnivory index is high (1.30 and 1.09).
