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
| `cadiz_global_structure.csv` | Whole-web measures: size, connectance, giant and strongly connected components, clustering (binary, weighted, directed), path length, assortativity, trophic coherence. Each has a definition. |
| `cadiz_structure_vs_null.csv` | The same measures against random (ER), degree-preserving and niche-model webs: null mean, SD, z-score, fraction of null webs below |
| `cadiz_centrality.csv` | One row per group: degree, out-strength, betweenness (binary and weighted), clustering (binary, weighted, directed), PageRank importance |
| `cadiz_centrality_vs_tl.csv` | Spearman ρ and p of each centrality against trophic level (40 consumers, and all 43 groups) |
| `cadiz_distribution_stats.csv` | Mean, median, SD, range, skewness and variance/mean of every node and link property, with random-web values for the degrees |
| `cadiz_node_knockouts.csv` | Each group removed alone: diet lost by its predators, secondary extinctions under both rules (with names), component sizes afterwards |
| `cadiz_guild_removal.csv` | A whole guild removed at once (trophic bands, taxonomic groups): secondary extinctions, living groups left |
| `cadiz_node_robustness_summary.csv` | R50 for every group-removal order (incl. recalculated attacks) and extinction threshold (θ = 1, 0.75, 0.5, 0.25), with the random-order 95% range |
| `cadiz_node_robustness_curves.csv` | Step-by-step group-removal curves: fraction lost and giant-component size after each removal |
| `cadiz_node_fragmentation.csv` | When the surviving web first splits into pieces, per removal order and rule |
| `cadiz_link_knockouts.csv` | Each feeding link cut alone: diet share, edge betweenness, bridge or not, sole prey or not, secondary extinctions under both rules |
| `cadiz_link_robustness_summary.csv` | L50 for every link-cutting order and threshold, with the random-order 95% range |
| `cadiz_link_robustness_curves.csv` | Step-by-step link-cutting curves: fraction of groups lost and giant-component size |
| `cadiz_link_fragmentation.csv` | When the surviving web first splits while links are cut |
| `network_structure.txt`, `node_removal.txt`, `edge_removal.txt` | Everything the analysis scripts print |
| `cadiz_analysis_results.xlsx` | Every analysis table above, one sheet each, plus a README sheet |

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

## Analysis tables: key columns

How each analysis works is in [`code/README.md`](../code/README.md).

**`cadiz_node_knockouts.csv`, `cadiz_guild_removal.csv` and `cadiz_link_knockouts.csv`**

| Column | Meaning |
|---|---|
| `secondary_topological` | Groups that starve under the rule "a consumer dies when all its prey are gone" |
| `secondary_weighted` | Groups that starve under the rule "a consumer dies when half its diet is gone" |
| `..._groups` | Names of those groups |
| `max_diet_loss`, `max_diet_loss_predator` | The largest share of any single predator's diet that the removed group supplied, and which predator that was |
| `predators_losing_half_diet` | Predators for which the removed group was at least half the diet |
| `lwcc_after_...`, `lscc_after_no_cascade` | Size of the largest weakly connected component (and of the largest feeding loop) after the removal |
| `living_left_...` | Living groups still present, out of 41 |
| `edge_betweenness` | (links) Directed edge betweenness: share of shortest feeding paths that use the link |
| `bridge` | (links) True if cutting the link alone splits the web (there are none) |
| `only_prey_of_predator` | (links) True if the link is the predator's only prey |

**`cadiz_node_robustness_summary.csv`** (and `cadiz_link_robustness_summary.csv`, where L50 counts cut links out of 397 instead of removed groups)

| Column | Meaning |
|---|---|
| `order` | Removal order: random (mean of 1000), or a ranking taken from the intact web |
| `rule` | Extinction threshold: all prey, 3/4, 1/2 or 1/4 of the diet lost |
| `R50` | Fraction of the 41 living groups removed before half of them are lost (maximum 0.51 = no secondary extinctions) |
| `random_R50_lo`, `random_R50_hi` | 95% range of R50 over the 1000 random orders |
| `frac_random_below` | For a ranked order, the fraction of random orders with a lower (more fragile) R50 |

**`cadiz_node_robustness_curves.csv`**: one row per removal step. Columns are `frac_removed` (primary removals / 41), `frac_lost` (primary plus secondary), `lwcc_frac` (giant component / 43) and `lwcc_of_present` (giant component / groups still present; 1 = the web is still in one piece). Random rows also carry 2.5–97.5% bounds (`_lo`, `_hi`).

**`cadiz_link_robustness_curves.csv`**: one row per cut. Columns are `frac_cut` (cuts / 397), `frac_lost` (living groups lost / 41) and `lwcc_frac` (giant component / 43). In the random rows, `lwcc_frac` is measured every 10 cuts.

**`cadiz_node_fragmentation.csv` / `cadiz_link_fragmentation.csv`**: `first_split` is the fraction removed (or cut) when the surviving groups first stop forming one connected web. For random orders it is the median, with the 95% range in `random_lo` and `random_hi`.

Bullet-point notes on all of these: [`notes/`](../notes/README.md).

