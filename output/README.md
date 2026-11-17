# Post-processed data

The code makes all files in this folder from the raw data. To change a table, change the code and run it again (see [`code/README.md`](../code/README.md)). Do not edit a table by hand, because the table will then not agree with the code.

These tables are for the Gulf of Cadiz only:

| File | Contents |
|---|---|
| `cadiz_diet_matrix_culled.csv` | The culled dataset: a 43 × 43 diet matrix without `Import`. Rows are prey, columns are predators, and each cell is the share of the predator's diet. The shares are the original shares (not rescaled). The matrix has 411 nonzero cells. |
| `cadiz_cleaning_log.csv` | Each change to the original download, one row for each step, with the link counts before and after |
| `cadiz_node_traits.csv` | One row for each group, with trophic level and other traits (columns defined below) |
| `cadiz_edges.csv` | One row for each feeding link: `prey`, `predator`, `diet_share` (original) and `diet_share_renorm` (diet rescaled to sum to 1). 411 rows, of which 14 are self-loops (cannibalism). |
| `cadiz_food_web.graphml` | The network as a weighted `DiGraph`. Edges point from prey to predator, and `weight` is the diet share. Each node has `group` and `trophic_level`. Opens in networkx (`nx.read_graphml`), Gephi or Cytoscape. |
| `cadiz_global_structure.csv` | Whole-web measures (size, connectance, giant and strongly connected components, clustering, path length, assortativity and trophic coherence), each with a definition |
| `cadiz_structure_vs_null.csv` | The same measures compared with random (ER), degree-preserving and niche-model webs: null mean, SD, z-score and fraction of null webs below the real value |
| `cadiz_centrality.csv` | One row for each group: degree, out-strength, betweenness (binary and weighted), clustering (binary, weighted and directed) and PageRank importance |
| `cadiz_centrality_vs_tl.csv` | Spearman ρ and p of each centrality against trophic level, for the 40 consumers and for all 43 groups |
| `cadiz_distribution_stats.csv` | Mean, median, SD, range, skewness and variance/mean of each node and link property, with random-web values for the degrees |
| `cadiz_node_knockouts.csv` | Each group removed alone: diet lost by its predators, secondary extinctions under both rules (with names), and component sizes after the removal |
| `cadiz_guild_removal.csv` | A full guild (trophic band or taxonomic group) removed at one time: secondary extinctions and living groups left |
| `cadiz_node_robustness_summary.csv` | R50 for each group-removal order (recalculated orders included) and each extinction threshold (θ = 1, 0.75, 0.5 and 0.25), with the 95% range of the random orders |
| `cadiz_node_robustness_curves.csv` | Group-removal curves, step by step: fraction of groups lost and giant component size after each removal |
| `cadiz_node_fragmentation.csv` | The point where the surviving web first splits, for each removal order and rule |
| `cadiz_link_knockouts.csv` | Each feeding link cut alone: diet share, edge betweenness, bridge or not, only prey of the predator or not, and secondary extinctions under both rules |
| `cadiz_link_robustness_summary.csv` | L50 for each link-cut order and threshold, with the 95% range of the random orders |
| `cadiz_link_robustness_curves.csv` | Link-cut curves, step by step: fraction of groups lost and giant component size |
| `cadiz_link_fragmentation.csv` | The point where the surviving web first splits during link cuts |
| `cadiz_r50_table.tex`, `cadiz_l50_table.tex` | The R50 and L50 tables from the two panel figures, in LaTeX, with the same values in bold |

`compare_webs.py` writes these tables for all three webs (Gulf of Cadiz, Angolan shelf and Mondego estuary):

| File | Contents |
|---|---|
| `compare_webs_global.csv` | One row for each web: size, connectance, degree centralization, components, clustering, path length and the other whole-web measures |
| `compare_webs_nodes.csv` | One row for each group in each web, with the same traits as `cadiz_node_traits.csv` plus the centralities |
| `compare_webs_centrality_vs_tl.csv` | Spearman ρ and p of each centrality against trophic level for each web (consumers and all groups) |
| `compare_webs_distributions.csv`, `compare_webs_extremes.csv` | Summary statistics of each node and link property for each web, and the group at each extreme |
| `compare_webs_knockouts.csv`, `compare_webs_guild_removal.csv` | Single-group removals and trophic-band removals for each web, under both rules |
| `compare_webs_robustness.csv` | R50 and L50 for each removal order and rule in each web, with the 95% range of the random orders. The `measure` column shows R50 or L50. |

`compare_webs_stats.py` writes the intervals and tests for the same three webs:

| File | Contents |
|---|---|
| `compare_webs_stats_baseline.csv`, `compare_webs_stats_baseline_table.tex` | The baseline table (nodes, links, connectance, mean and SD of degree, trophic levels, clustering, path length and four centralizations), with one column for each web. The `.tex` file is the same table in LaTeX. |
| `compare_webs_stats_centralization_vs_random.csv` | Each centralization compared with 1000 random graphs with the same nodes and links: random mean, SD, 95% range, z-score and p-value |
| `compare_webs_stats_correlations.csv` | Trophic level against five measures in each web: ρ, its bootstrap 95% interval (`rho_lo`, `rho_hi`), the permutation p-value, and the least-squares slope with its interval |
| `compare_webs_stats_correlation_differences.csv` | The difference in ρ between each pair of webs, with its bootstrap interval and a Fisher z test |
| `compare_webs_stats_group_tests.csv` | Kruskal–Wallis and pairwise Mann–Whitney tests between the trophic bands and between the Gulf of Cadiz taxonomic categories, with Holm-corrected p-values and effect sizes |
| `compare_webs_stats_removal.csv` | One row for each web, rule and removal order: R50, area under the share-lost curve, their spread, and the test against random orders |
| `compare_webs_stats_removal_curves.csv` | The removal curves in the figures, with the 95% range for random orders and the range over tie-breaks for targeted orders (`lo`, `hi`) |
| `compare_webs_stats_removal_contrasts.csv` | The two extinction rules compared on the same random orders, and the three webs compared with each other |

## Changes to the original dataset

`cadiz_cleaning_log.csv` contains the full record. Summary:

| Step | Change | Links |
|---|---|---|
| Remove `Import` | `Import` is not a functional group. It is Ecopath's share of a diet eaten outside the model area. It occurs only in the diets of Loggerhead turtles (0.448) and Seabirds (0.404). Its column (what Import eats) is empty. | 413 → 411 |
| Exports / emigration | The diet matrix has no other boundary flow. Torres et al. (2013) give fishery catches and exports in separate tables. | no change |
| Rescale diets | Without Import, the turtle and seabird diets sum to 0.552 and 0.596. Thus, each diet is rescaled to sum to 1 for trophic level, omnivory index and diet diversity. | no change |
| Keep Detritus, Discard | These non-living basal groups stay as nodes. Without them, the web is still connected (41 nodes, 396 links). | no change |
| Keep cannibalism | The 14 self-loops stay, but the prey counts, predator counts and diet diversity do not include them. | no change |
| Keep weak links | No threshold. Diet shares go down to 1e-6, and 120 links are below 0.01. | no change |

## `cadiz_node_traits.csv` columns

| Column | Definition |
|---|---|
| `group_name` | Functional group (node). These are groups, not species. |
| `category` | Broad type, from the group name: fishes, invertebrates & plankton, marine mammals, birds, turtles, or non-living |
| `living` | False for Detritus and Discard |
| `role` | `basal` eats nothing, `top predator` has no predator, and all other groups are `intermediate` (cannibalism ignored) |
| `trophic_level` | $1 + \sum_j D_{ji} TL_j$ over prey $j$, with basal groups = 1. Uses the rescaled diets. |
| `omnivory_index` | Diet-weighted variance of prey trophic levels around $TL_i - 1$ (Christensen & Pauly 1992). 0 means that all prey have the same trophic level. |
| `n_prey` | Number of prey groups (in-degree, "generality"), without the group itself |
| `n_predators` | Number of predator groups (out-degree, "vulnerability"), without the group itself |
| `total_degree` | `n_prey + n_predators` |
| `effective_prey` | Diet diversity: exp(Shannon entropy) of the rescaled diet without cannibalism. Empty for basal groups. |
| `diet_share_sum` | Sum of the group's share across all predator diets (weighted out-degree), or importance as prey |
| `cannibal` | True if the group eats itself |
| `cannibalism_share` | Share of the group's diet that is the group itself |
| `import_share_removed` | Share of the diet that was `Import` and that cleaning removed (nonzero for 2 groups) |
| `diet_total_original` | Sum of the diet column before cleaning (about 1 for consumers, 0 for basal groups) |
| `in_feeding_loop` | True if the group is in a feeding loop, which is a strongly connected component of more than one group (23 groups) |

The trophic levels of Loggerhead turtles (3.18) and Seabirds (3.09) depend on the rescaling step. This step assumes that food eaten outside the area has the same composition as the local diet. Both groups also get about 45% of their diet from Discard (trophic level 1). This gives them a high omnivory index (1.30 and 1.09).

## Columns in the analysis tables

[`code/README.md`](../code/README.md) describes each analysis.

`cadiz_node_knockouts.csv`, `cadiz_guild_removal.csv` and `cadiz_link_knockouts.csv`:

| Column | Meaning |
|---|---|
| `secondary_topological` | Groups that starve under the rule "a consumer dies when all its prey are gone" |
| `secondary_weighted` | Groups that starve under the rule "a consumer dies when half its diet is gone" |
| `..._groups` | Names of those groups |
| `max_diet_loss`, `max_diet_loss_predator` | The largest share of one predator's diet that the removed group supplied, and the name of that predator |
| `predators_losing_half_diet` | Predators for which the removed group was half or more of the diet |
| `lwcc_after_...`, `lscc_after_no_cascade` | Size of the largest weakly connected component (and of the largest feeding loop) after the removal |
| `living_left_...` | Living groups still present, out of 41 |
| `edge_betweenness` | (links) Directed edge betweenness: the share of shortest feeding paths that use the link |
| `bridge` | (links) True if the cut of this link alone splits the web (no link does) |
| `only_prey_of_predator` | (links) True if the link is the only prey of the predator |

`cadiz_node_robustness_summary.csv` (and `cadiz_link_robustness_summary.csv`, where L50 counts cut links out of 397 instead of removed groups):

| Column | Meaning |
|---|---|
| `order` | Removal order: random (mean of 1000) or a ranking from the intact web |
| `rule` | Extinction threshold: all prey, 3/4, 1/2 or 1/4 of the diet lost |
| `R50` | Fraction of the 41 living groups removed before half of them are lost (maximum 0.51, which means no secondary extinctions) |
| `random_R50_lo`, `random_R50_hi` | 95% range of R50 for the 1000 random orders |
| `frac_random_below` | For a ranked order, the fraction of random orders with a lower (more fragile) R50 |
| `frac_random_at_or_below` | The fraction of random orders with a lower or equal R50. The R50 table in the panel figure shows an order in bold only when this value is below 0.05, because R50 changes in steps and many random orders have the same R50. |

`cadiz_node_robustness_curves.csv` has one row for each removal step. The columns are `frac_removed` (removals / 41), `frac_lost` (removals plus secondary extinctions), `lwcc_frac` (giant component / 43) and `lwcc_of_present` (giant component / groups still present, where 1 means the web is still one piece). The random rows also have 2.5–97.5% bounds (`_lo`, `_hi`).

`cadiz_link_robustness_curves.csv` has one row for each cut. The columns are `frac_cut` (cuts / 397), `frac_lost` (living groups lost / 41) and `lwcc_frac` (giant component / 43). For the random rows, the script measures `lwcc_frac` every 10 cuts.

In `cadiz_node_fragmentation.csv` and `cadiz_link_fragmentation.csv`, `first_split` is the fraction removed (or cut) when the surviving groups first stop being one connected web. For random orders, the value is the median, with the 95% range in `random_lo` and `random_hi`.

`compare_webs_stats_removal.csv`:

| Column | Meaning |
|---|---|
| `trials` | 1000 for random order. For a targeted order, 200 runs with ties broken at random, or 1 run if no groups tie. |
| `groups_tied` | Number of living groups that share their ranking score with another group |
| `R50`, `area` | The mean for random order. For a targeted order, the value from the run with ties broken by name, which is the run in the other tables and figures. |
| `R50_lo`, `R50_hi`, `area_lo`, `area_hi` | The 95% range for random order, or the lowest and highest value across the tie-breaks |
| `area_z` | The distance of the targeted order from the random mean, in random-order SDs |
| `R50_p_two_sided`, `area_p_two_sided` | Monte Carlo p-value against the 1000 random orders. A random order with the same value as the targeted order counts against the targeted order. |
| `..._p_min_over_ties`, `..._p_max_over_ties` | The lowest and highest p-value across the tie-breaks |
| `R50_frac_random_strictly_below`, `R50_frac_random_equal` | The fraction of random orders with a lower R50, and the fraction with the same R50. The second value is often large, because R50 changes in steps. |

[`notes/`](../notes/README.md) summarizes the main results from these tables.
