# Comparison with other ecosystems

These figures compare the Gulf of Cadiz with the Angolan shelf and the Mondego estuary. Each web has the same color and marker in all figures: blue circles for the Gulf of Cadiz, orange squares for the Angolan shelf and green triangles for the Mondego estuary. The name of a figure that shows one web has the short name of the web after `compare_` (`cadiz`, `angola` or `mondego`). All other figures show the three webs. In the file names, `<rule>` is `all_prey` or `half_diet`. Results: [`notes/08_comparison.md`](../../notes/08_comparison.md).

## The webs

| Figure | What it shows |
|---|---|
| [`compare_angola_food_web`](compare_angola_food_web.png) · [pdf](compare_angola_food_web.pdf) | The Angolan shelf food web, drawn by trophic level in the same way as the Gulf of Cadiz in [`01_web/food_web`](../01_web/food_web.png). Node size shows importance as prey, arrow width shows diet share, and a ring shows cannibalism. Width 7 in. |
| [`compare_mondego_food_web`](compare_mondego_food_web.png) · [pdf](compare_mondego_food_web.pdf) | The Mondego estuary food web, drawn in the same way. 19 groups are at trophic level 2, so their names are vertical, below the nodes. Width 7 in. |
| [`compare_baseline_statistics`](compare_baseline_statistics.png) · [pdf](compare_baseline_statistics.pdf) | The baseline statistics of the three webs as a table (groups, links, connectance, mean degree, basal groups, top predators, trophic levels, diet diversity, clustering, path length and degree centralization). The full table is `output/compare_webs_stats_baseline.csv`. |

## Measurements

Script: [`code/compare_webs.py`](../../code/compare_webs.py).

| Figure | What it shows |
|---|---|
| [`compare_clustering_vs_density`](compare_clustering_vs_density.png) · [pdf](compare_clustering_vs_density.pdf) | Average clustering against a random web of the same density, with the ratio printed above each pair. |
| [`compare_degree_unevenness`](compare_degree_unevenness.png) · [pdf](compare_degree_unevenness.pdf) | Variance/mean of total degree, number of prey and number of predators, against a random web of the same size and density. |
| [`compare_diet_concentration`](compare_diet_concentration.png) · [pdf](compare_diet_concentration.pdf) | Cumulative distribution of the share of each consumer's diet that comes from its largest prey. A value of 1 means that the consumer eats only one prey. |
| [`compare_diet_diversity`](compare_diet_diversity.png) · [pdf](compare_diet_diversity.pdf) | Cumulative distribution of diet diversity (effective number of prey) for the consumers. |
| [`compare_fragmentation`](compare_fragmentation.png) · [pdf](compare_fragmentation.pdf) | Share of groups removed before the web splits into more than one part, without secondary extinctions. |
| [`compare_global_structure`](compare_global_structure.png) · [pdf](compare_global_structure.pdf) | Six whole-web measures for the three webs. |
| [`compare_guild_removal`](compare_guild_removal.png) · [pdf](compare_guild_removal.pdf) | Secondary extinctions after removing a whole trophic band, under the half-of-diet rule. |
| [`compare_knockouts`](compare_knockouts.png) · [pdf](compare_knockouts.pdf) | The largest loss from the removal of one group in each web, and the number of groups that cause a secondary extinction. |
| [`compare_l50_link_strength`](compare_l50_link_strength.png) · [pdf](compare_l50_link_strength.pdf) | L50 for cutting the strongest links first, in a random order and the weakest links first, under the half-of-diet rule. |
| [`compare_link_strength`](compare_link_strength.png) · [pdf](compare_link_strength.pdf) | Cumulative distribution of link strength (share of the predator's diet) on a log axis. |
| [`compare_trophic_level`](compare_trophic_level.png) · [pdf](compare_trophic_level.pdf) | Cumulative distribution of trophic level. |

## Intervals and tests

Script: [`code/compare_webs_stats.py`](../../code/compare_webs_stats.py). A filled marker shows a result that is different from random, or an interval that does not include 0. An open marker shows that the result is not different. These tests cover only node removal, not link removal.

| Figure | What it shows |
|---|---|
| [`compare_rho_intervals`](compare_rho_intervals.png) · [pdf](compare_rho_intervals.pdf) | Spearman ρ of each of five measures with trophic level for the three webs, with its bootstrap 95% interval. |
| `compare_<web>_tl_vs_<measure>` (15) | One measure against trophic level for the consumers of one web, showing every point, a least-squares line with a 95% bootstrap band, and ρ with its interval. The measures are `n_prey`, `effective_prey`, `n_predators`, `total_degree` and `betweenness`. |
| [`compare_centralization_vs_random`](compare_centralization_vs_random.png) · [pdf](compare_centralization_vs_random.pdf) | Degree and betweenness centralization of each web against the 95% range of 1000 random directed graphs with the same nodes and links. |
| `compare_<web>_robustness_<rule>_centrality` (6) | Share of living groups lost as groups are removed, most connected first and highest betweenness first, against the mean and 95% range of 1000 random orders. The band around a targeted line is the range across 200 tie-breaks. The p-value compares the area under the curve with the random orders. |
| `compare_<web>_robustness_<rule>_trophic_position` (6) | The same for lowest and highest trophic level first. |
| `compare_area_intervals_<rule>` (2) | Area under the share-lost curve for each removal order in the three webs. The thick bar on the random row is the 95% range of the random orders. A thin bar is the range across the tie-breaks. |
| `compare_r50_intervals_<rule>` (2) | The same plot for R50. R50 changes in steps, so many random orders have the same R50 as a targeted order. Thus, the area plot is the better test. |
| `compare_cadiz_<measure>_by_category` (4) | One measure for the Gulf of Cadiz consumers by taxonomic category, with the median, the quartiles and the Kruskal–Wallis result. |

## Previews

### compare_angola_food_web

![compare_angola_food_web](compare_angola_food_web.png)

### compare_angola_robustness_all_prey_centrality

![compare_angola_robustness_all_prey_centrality](compare_angola_robustness_all_prey_centrality.png)

### compare_angola_robustness_all_prey_trophic_position

![compare_angola_robustness_all_prey_trophic_position](compare_angola_robustness_all_prey_trophic_position.png)

### compare_angola_robustness_half_diet_centrality

![compare_angola_robustness_half_diet_centrality](compare_angola_robustness_half_diet_centrality.png)

### compare_angola_robustness_half_diet_trophic_position

![compare_angola_robustness_half_diet_trophic_position](compare_angola_robustness_half_diet_trophic_position.png)

### compare_angola_tl_vs_betweenness

![compare_angola_tl_vs_betweenness](compare_angola_tl_vs_betweenness.png)

### compare_angola_tl_vs_effective_prey

![compare_angola_tl_vs_effective_prey](compare_angola_tl_vs_effective_prey.png)

### compare_angola_tl_vs_n_predators

![compare_angola_tl_vs_n_predators](compare_angola_tl_vs_n_predators.png)

### compare_angola_tl_vs_n_prey

![compare_angola_tl_vs_n_prey](compare_angola_tl_vs_n_prey.png)

### compare_angola_tl_vs_total_degree

![compare_angola_tl_vs_total_degree](compare_angola_tl_vs_total_degree.png)

### compare_area_intervals_all_prey

![compare_area_intervals_all_prey](compare_area_intervals_all_prey.png)

### compare_area_intervals_half_diet

![compare_area_intervals_half_diet](compare_area_intervals_half_diet.png)

### compare_baseline_statistics

![compare_baseline_statistics](compare_baseline_statistics.png)

### compare_cadiz_effective_prey_by_category

![compare_cadiz_effective_prey_by_category](compare_cadiz_effective_prey_by_category.png)

### compare_cadiz_n_predators_by_category

![compare_cadiz_n_predators_by_category](compare_cadiz_n_predators_by_category.png)

### compare_cadiz_n_prey_by_category

![compare_cadiz_n_prey_by_category](compare_cadiz_n_prey_by_category.png)

### compare_cadiz_robustness_all_prey_centrality

![compare_cadiz_robustness_all_prey_centrality](compare_cadiz_robustness_all_prey_centrality.png)

### compare_cadiz_robustness_all_prey_trophic_position

![compare_cadiz_robustness_all_prey_trophic_position](compare_cadiz_robustness_all_prey_trophic_position.png)

### compare_cadiz_robustness_half_diet_centrality

![compare_cadiz_robustness_half_diet_centrality](compare_cadiz_robustness_half_diet_centrality.png)

### compare_cadiz_robustness_half_diet_trophic_position

![compare_cadiz_robustness_half_diet_trophic_position](compare_cadiz_robustness_half_diet_trophic_position.png)

### compare_cadiz_tl_vs_betweenness

![compare_cadiz_tl_vs_betweenness](compare_cadiz_tl_vs_betweenness.png)

### compare_cadiz_tl_vs_effective_prey

![compare_cadiz_tl_vs_effective_prey](compare_cadiz_tl_vs_effective_prey.png)

### compare_cadiz_tl_vs_n_predators

![compare_cadiz_tl_vs_n_predators](compare_cadiz_tl_vs_n_predators.png)

### compare_cadiz_tl_vs_n_prey

![compare_cadiz_tl_vs_n_prey](compare_cadiz_tl_vs_n_prey.png)

### compare_cadiz_tl_vs_total_degree

![compare_cadiz_tl_vs_total_degree](compare_cadiz_tl_vs_total_degree.png)

### compare_cadiz_total_degree_by_category

![compare_cadiz_total_degree_by_category](compare_cadiz_total_degree_by_category.png)

### compare_centralization_vs_random

![compare_centralization_vs_random](compare_centralization_vs_random.png)

### compare_clustering_vs_density

![compare_clustering_vs_density](compare_clustering_vs_density.png)

### compare_degree_unevenness

![compare_degree_unevenness](compare_degree_unevenness.png)

### compare_diet_concentration

![compare_diet_concentration](compare_diet_concentration.png)

### compare_diet_diversity

![compare_diet_diversity](compare_diet_diversity.png)

### compare_fragmentation

![compare_fragmentation](compare_fragmentation.png)

### compare_global_structure

![compare_global_structure](compare_global_structure.png)

### compare_guild_removal

![compare_guild_removal](compare_guild_removal.png)

### compare_knockouts

![compare_knockouts](compare_knockouts.png)

### compare_l50_link_strength

![compare_l50_link_strength](compare_l50_link_strength.png)

### compare_link_strength

![compare_link_strength](compare_link_strength.png)

### compare_mondego_food_web

![compare_mondego_food_web](compare_mondego_food_web.png)

### compare_mondego_robustness_all_prey_centrality

![compare_mondego_robustness_all_prey_centrality](compare_mondego_robustness_all_prey_centrality.png)

### compare_mondego_robustness_all_prey_trophic_position

![compare_mondego_robustness_all_prey_trophic_position](compare_mondego_robustness_all_prey_trophic_position.png)

### compare_mondego_robustness_half_diet_centrality

![compare_mondego_robustness_half_diet_centrality](compare_mondego_robustness_half_diet_centrality.png)

### compare_mondego_robustness_half_diet_trophic_position

![compare_mondego_robustness_half_diet_trophic_position](compare_mondego_robustness_half_diet_trophic_position.png)

### compare_mondego_tl_vs_betweenness

![compare_mondego_tl_vs_betweenness](compare_mondego_tl_vs_betweenness.png)

### compare_mondego_tl_vs_effective_prey

![compare_mondego_tl_vs_effective_prey](compare_mondego_tl_vs_effective_prey.png)

### compare_mondego_tl_vs_n_predators

![compare_mondego_tl_vs_n_predators](compare_mondego_tl_vs_n_predators.png)

### compare_mondego_tl_vs_n_prey

![compare_mondego_tl_vs_n_prey](compare_mondego_tl_vs_n_prey.png)

### compare_mondego_tl_vs_total_degree

![compare_mondego_tl_vs_total_degree](compare_mondego_tl_vs_total_degree.png)

### compare_r50_intervals_all_prey

![compare_r50_intervals_all_prey](compare_r50_intervals_all_prey.png)

### compare_r50_intervals_half_diet

![compare_r50_intervals_half_diet](compare_r50_intervals_half_diet.png)

### compare_rho_intervals

![compare_rho_intervals](compare_rho_intervals.png)

### compare_trophic_level

![compare_trophic_level](compare_trophic_level.png)
