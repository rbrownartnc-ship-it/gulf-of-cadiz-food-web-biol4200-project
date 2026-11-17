# Post-processed data

Everything in this folder comes from the raw data, either by cleaning or by analysis, and the code writes every file. So, if a table needs to change, change the code and rerun it (see [`code/README.md`](../code/README.md)) instead of editing the table.

The first set of tables is for the Gulf of Cadiz only.

| File | Contents |
|---|---|
| `cadiz_diet_matrix_culled.csv` | The culled dataset, a 43 × 43 diet matrix with `Import` removed. Rows are prey, columns are predators, and each cell is the share of the predator's diet. The original shares are kept (not rescaled). 411 nonzero cells. |
| `cadiz_cleaning_log.csv` | Every change made to the original download, one row per step, with link counts before and after |
| `cadiz_node_traits.csv` | One row per group with its trophic level and other traits (columns defined below) |
| `cadiz_edges.csv` | One row per feeding link: `prey`, `predator`, `diet_share` (original) and `diet_share_renorm` (diet rescaled to sum to 1). 411 rows, 14 of them self-loops (cannibalism). |
| `cadiz_food_web.graphml` | The network as a weighted `DiGraph` with edges prey → predator and `weight` = diet share. Nodes have `group` and `trophic_level`. Opens in networkx (`nx.read_graphml`), Gephi or Cytoscape. |
| `cadiz_global_structure.csv` | Whole-web measures (size, connectance, giant and strongly connected components, clustering, path length, assortativity and trophic coherence), each with a definition |
| `cadiz_structure_vs_null.csv` | The same measures against random (ER), degree-preserving and niche-model webs, with the null mean, SD, z-score and fraction of null webs below |
| `cadiz_centrality.csv` | One row per group with degree, out-strength, betweenness (binary and weighted), clustering (binary, weighted and directed) and PageRank importance |
| `cadiz_centrality_vs_tl.csv` | Spearman ρ and p of each centrality against trophic level (for the 40 consumers and for all 43 groups) |
| `cadiz_distribution_stats.csv` | Mean, median, SD, range, skewness and variance/mean of every node and link property, with random-web values for the degrees |
| `cadiz_node_knockouts.csv` | Each group removed by itself, with the diet its predators lose, secondary extinctions under both rules (with names) and component sizes afterwards |
| `cadiz_guild_removal.csv` | A whole guild (trophic band or taxonomic group) removed at once, with secondary extinctions and living groups left |
| `cadiz_node_robustness_summary.csv` | R50 for every group-removal order (including the recalculated ones) and extinction threshold (θ = 1, 0.75, 0.5 and 0.25), with the 95% range of the random orders |
| `cadiz_node_robustness_curves.csv` | The group-removal curves step by step, with the fraction lost and giant component size after each removal |
| `cadiz_node_fragmentation.csv` | When the surviving web first splits into pieces, for each removal order and rule |
| `cadiz_link_knockouts.csv` | Each feeding link cut by itself, with its diet share, edge betweenness, whether it is a bridge or a predator's only prey, and secondary extinctions under both rules |
| `cadiz_link_robustness_summary.csv` | L50 for every link-cutting order and threshold, with the 95% range of the random orders |
| `cadiz_link_robustness_curves.csv` | The link-cutting curves step by step, with the fraction of groups lost and giant component size |
| `cadiz_link_fragmentation.csv` | When the surviving web first splits while links are cut |
| `cadiz_r50_table.tex`, `cadiz_l50_table.tex` | The R50 and L50 tables from the two panel figures for LaTeX, with the same orders in bold |

`compare_webs.py` writes these tables for all three webs (Gulf of Cadiz, Angolan shelf and Mondego estuary):

| File | Contents |
|---|---|
| `compare_webs_global.csv` | One row per web with size, connectance, degree centralization, components, clustering, path length and the other whole-web measures |
| `compare_webs_nodes.csv` | One row per group in every web, with the same traits as `cadiz_node_traits.csv` plus the centralities |
| `compare_webs_centrality_vs_tl.csv` | Spearman ρ and p of each centrality against trophic level for each web (consumers and all groups) |
| `compare_webs_distributions.csv`, `compare_webs_extremes.csv` | Summary statistics of every node and link property for each web, and the group at each extreme |
| `compare_webs_knockouts.csv`, `compare_webs_guild_removal.csv` | Single-group and whole-guild removals for each web, under both rules |
| `compare_webs_robustness.csv` | R50 and L50 for every removal order and rule in each web, with the 95% range of the random orders (`measure` says which one a row is) |

`compare_webs_stats.py` writes the intervals and tests for the same three webs:

| File | Contents |
|---|---|
| `compare_webs_stats_baseline.csv`, `compare_webs_stats_baseline_table.tex` | The baseline table (nodes, links, connectance, mean and SD of degree, trophic levels, clustering, path length and the four centralizations), with one column per web. The `.tex` file is the same table for LaTeX. |
| `compare_webs_stats_centralization_vs_random.csv` | Each centralization against 1000 random graphs with the same nodes and links, with the random mean, SD, 95% range, z-score and p-value |
| `compare_webs_stats_correlations.csv` | Trophic level against five measures in each web, with ρ, its bootstrap 95% interval (`rho_lo`, `rho_hi`), the permutation p-value, and the least-squares slope with its interval |
| `compare_webs_stats_correlation_differences.csv` | The difference in ρ between each pair of webs, with its bootstrap interval and a Fisher z test |
| `compare_webs_stats_group_tests.csv` | Kruskal–Wallis and pairwise Mann–Whitney tests between the trophic bands and between the Gulf of Cadiz taxonomic categories, with Holm-corrected p-values and effect sizes |
| `compare_webs_stats_removal.csv` | One row per web, rule and removal order, with R50, the area under the share-lost curve, their spread and the test against random orders |
| `compare_webs_stats_removal_curves.csv` | The removal curves behind the figures, with the 95% range for random orders and the range over tie-breaks for targeted ones (`lo`, `hi`) |
| `compare_webs_stats_removal_contrasts.csv` | The two extinction rules compared on the same random orders, and the webs compared with each other |

## Changes made to the original dataset

`cadiz_cleaning_log.csv` has the full record. In short:

| Step | Change | Links |
|---|---|---|
| Remove `Import` | `Import` is not a functional group. It is Ecopath's share of a diet eaten outside the model area, and it only shows up in the diets of Loggerhead turtles (0.448) and Seabirds (0.404). Its column (what Import eats) is empty. | 413 → 411 |
| Exports / emigration | We checked for any other boundary flow, and there is none in the diet matrix. Fishery catches and exports are in the tables of Torres et al. (2013) instead. | no change |
| Rescale diets | Without Import, the turtle and seabird diets sum to 0.552 and 0.596, so every diet is rescaled to sum to 1 for trophic level, omnivory index and diet diversity. | no change |
| Keep Detritus, Discard | These are non-living basal groups, and we keep them as nodes. Without them the web is still connected (41 nodes, 396 links). | no change |
| Keep cannibalism | The 14 self-loops are kept, but they are left out of the prey and predator counts and diet diversity. | no change |
| Keep weak links | There is no threshold. Shares go down to 1e-6, and 120 links are below 0.01. | no change |

## `cadiz_node_traits.csv` columns

| Column | Definition |
|---|---|
| `group_name` | Functional group (node). These are groups, not species. |
| `category` | Broad type, assigned from the group name: fishes, invertebrates & plankton, marine mammals, birds, turtles, or non-living |
| `living` | False for Detritus and Discard |
| `role` | `basal` eats nothing, `top predator` is eaten by no other group, and everything else is `intermediate` (cannibalism ignored) |
| `trophic_level` | $1 + \sum_j D_{ji} TL_j$ over prey $j$, with basal groups = 1. Uses the rescaled diets. |
| `omnivory_index` | Diet-weighted variance of prey trophic levels around $TL_i - 1$ (Christensen & Pauly 1992). 0 means a group feeds on one level. |
| `n_prey` | Number of prey groups (in-degree, "generality"), not counting itself |
| `n_predators` | Number of predator groups (out-degree, "vulnerability"), not counting itself |
| `total_degree` | `n_prey + n_predators` |
| `effective_prey` | Diet diversity, exp(Shannon entropy) of the rescaled diet without cannibalism. Empty for basal groups. |
| `diet_share_sum` | Sum of this group's share across all predators' diets (weighted out-degree), which we call importance as prey |
| `cannibal` | True if the group eats itself |
| `cannibalism_share` | Share of the group's own diet that is itself |
| `import_share_removed` | Share of the diet that was `Import` and was removed (nonzero for 2 groups) |
| `diet_total_original` | Sum of the diet column before cleaning (about 1 for consumers and 0 for basal groups) |
| `in_feeding_loop` | True if the group is part of a feeding loop, meaning a strongly connected component larger than one group (23 groups) |

The trophic levels of Loggerhead turtles (3.18) and Seabirds (3.09) depend on the rescaling step, which assumes that food eaten outside the area is the same mix as the local diet. Both groups also get about 45% of their diet from Discard (trophic level 1), which is why their omnivory index is high (1.30 and 1.09, respectively).

## Columns in the analysis tables

[`code/README.md`](../code/README.md) explains how each analysis works.

`cadiz_node_knockouts.csv`, `cadiz_guild_removal.csv` and `cadiz_link_knockouts.csv`:

| Column | Meaning |
|---|---|
| `secondary_topological` | Groups that starve under the rule "a consumer dies when all its prey are gone" |
| `secondary_weighted` | Groups that starve under the rule "a consumer dies when half its diet is gone" |
| `..._groups` | Names of those groups |
| `max_diet_loss`, `max_diet_loss_predator` | The largest share of any one predator's diet that the removed group supplied, and which predator that was |
| `predators_losing_half_diet` | Predators for which the removed group was at least half the diet |
| `lwcc_after_...`, `lscc_after_no_cascade` | Size of the largest weakly connected component (and of the largest feeding loop) after the removal |
| `living_left_...` | Living groups still present, out of 41 |
| `edge_betweenness` | (links) Directed edge betweenness, the share of shortest feeding paths that use the link |
| `bridge` | (links) True if cutting the link by itself splits the web (there are none) |
| `only_prey_of_predator` | (links) True if the link is the predator's only prey |

`cadiz_node_robustness_summary.csv` (and `cadiz_link_robustness_summary.csv`, where L50 counts cut links out of 397 instead of removed groups):

| Column | Meaning |
|---|---|
| `order` | Removal order, either random (mean of 1000) or a ranking from the intact web |
| `rule` | Extinction threshold: all prey, 3/4, 1/2 or 1/4 of the diet lost |
| `R50` | Fraction of the 41 living groups removed before half of them are lost (0.51 at most, which means no secondary extinctions) |
| `random_R50_lo`, `random_R50_hi` | 95% range of R50 over the 1000 random orders |
| `frac_random_below` | For a ranked order, the fraction of random orders with a lower (more fragile) R50 |
| `frac_random_at_or_below` | The same, but counting random orders that tie with the ranked order too. The R50 table in the panel figure only bolds an order when this is below 0.05, as R50 moves in steps and lots of random orders tie. |

In `cadiz_node_robustness_curves.csv`, each row is one removal step. The columns are `frac_removed` (primary removals / 41), `frac_lost` (primary plus secondary), `lwcc_frac` (giant component / 43) and `lwcc_of_present` (giant component / groups still present, where 1 means the web is still in one piece). The random rows also have 2.5–97.5% bounds (`_lo`, `_hi`).

In `cadiz_link_robustness_curves.csv`, each row is one cut. The columns are `frac_cut` (cuts / 397), `frac_lost` (living groups lost / 41) and `lwcc_frac` (giant component / 43). For the random rows, `lwcc_frac` is measured every 10 cuts.

In `cadiz_node_fragmentation.csv` and `cadiz_link_fragmentation.csv`, `first_split` is the fraction removed (or cut) when the surviving groups first stop forming one connected web. For random orders it is the median, with the 95% range in `random_lo` and `random_hi`.

`compare_webs_stats_removal.csv`:

| Column | Meaning |
|---|---|
| `trials` | 1000 for random order. For a targeted order it is 200 runs with ties broken at random, or 1 if no groups tie. |
| `groups_tied` | How many living groups share their ranking score with another group |
| `R50`, `area` | The mean for random order. For a targeted order, it is the run with ties broken by name, which is the one in the other tables and figures. |
| `R50_lo`, `R50_hi`, `area_lo`, `area_hi` | The 95% range for random order, or the lowest and highest value over the tie-breaks |
| `area_z` | How many random-order SDs the targeted order is from the random mean |
| `R50_p_two_sided`, `area_p_two_sided` | Monte Carlo p-value against the 1000 random orders, where a random order that ties with the targeted one counts against it |
| `..._p_min_over_ties`, `..._p_max_over_ties` | The lowest and highest p-value the tie-breaks can give |
| `R50_frac_random_strictly_below`, `R50_frac_random_equal` | The share of random orders with a lower R50, and the share with the exact same R50. The second one is often large, as R50 moves in steps. |

The main numbers from these tables are in [`notes/`](../notes/README.md).
