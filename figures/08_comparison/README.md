# Comparison with other ecosystems

The Gulf of Cadiz beside the Angolan shelf and the Mondego estuary. Each web keeps its color and marker in every figure (Gulf of Cadiz blue circles, Angolan shelf orange squares, Mondego estuary green triangles). The numbers behind these figures are in [`notes/07_cross_ecosystem.md`](../../notes/07_cross_ecosystem.md).

## Measurements

Drawn by [`code/compare_webs.py`](../../code/compare_webs.py).

| Figure | What it shows |
|---|---|
| [`compare_clustering_vs_density`](compare_clustering_vs_density.png) · [pdf](compare_clustering_vs_density.pdf) | Average clustering against a random web of the same density; the ratio is printed above each pair. |
| [`compare_degree_unevenness`](compare_degree_unevenness.png) · [pdf](compare_degree_unevenness.pdf) | Variance/mean of total degree, number of prey and number of predators, against a random web of the same size and density. |
| [`compare_diet_concentration`](compare_diet_concentration.png) · [pdf](compare_diet_concentration.pdf) | Cumulative distribution of the share of a consumer's diet carried by its single largest prey; 1 = a single-prey diet. |
| [`compare_diet_diversity`](compare_diet_diversity.png) · [pdf](compare_diet_diversity.pdf) | Cumulative distribution of diet diversity (effective number of prey), consumers only. |
| [`compare_fragmentation`](compare_fragmentation.png) · [pdf](compare_fragmentation.pdf) | Share of groups removed before the web breaks into more than one piece, with no secondary extinctions. |
| [`compare_global_structure`](compare_global_structure.png) · [pdf](compare_global_structure.pdf) | Six whole-web measures for the three webs. |
| [`compare_guild_removal`](compare_guild_removal.png) · [pdf](compare_guild_removal.pdf) | Secondary extinctions after removing a whole trophic band, half-of-diet rule. |
| [`compare_knockouts`](compare_knockouts.png) · [pdf](compare_knockouts.pdf) | The worst single-group loss in each web, and how many groups cause any secondary extinction at all. |
| [`compare_l50_link_strength`](compare_l50_link_strength.png) · [pdf](compare_l50_link_strength.pdf) | L50 for cutting the strongest, random and weakest links first, half-of-diet rule. |
| [`compare_link_strength`](compare_link_strength.png) · [pdf](compare_link_strength.pdf) | Cumulative distribution of link strength (share of the predator's diet), log axis. |
| [`compare_trophic_level`](compare_trophic_level.png) · [pdf](compare_trophic_level.pdf) | Cumulative distribution of trophic level. |

## Intervals and tests

Drawn by [`code/significance.py`](../../code/significance.py). A filled marker means the result is different from random (or the interval excludes 0), and an open marker means it is not. In the file names, `<web>` is `cadiz`, `angolan` or `mondego`, and `<rule>` is `all_prey` or `half_diet`. Unfortunately, only node removal is covered so far, not link removal.

| Figure | What it shows |
|---|---|
| [`compare_rho_intervals`](compare_rho_intervals.png) | Spearman ρ of each of five measures with trophic level for the three webs, with its bootstrap 95% interval. |
| `compare_fit_<web>_<measure>` (15) | One measure against trophic level for the consumers of one web: every point, a least-squares line with a 95% bootstrap band, and ρ with its interval. The measures are `n_prey`, `effective_prey`, `n_predators`, `total_degree` and `betweenness`. |
| [`compare_centralization_vs_random`](compare_centralization_vs_random.png) | Degree and betweenness centralization of each web against the 95% range of 1000 random directed graphs with the same nodes and links. |
| `compare_removal_<web>_<rule>_centrality` (6) | Share of living groups lost as groups are removed, most connected first and highest betweenness first, against the mean and 95% range of 1000 random orders. The band on a targeted line is the range over 200 tie-breaks. |
| `compare_removal_<web>_<rule>_trophic` (6) | The same for lowest and highest trophic level first. |
| `compare_area_intervals_<rule>` (2) | Area under the share-lost curve for each removal order in the three webs. The thick bar on the random row is the 95% range of the random orders, and a thin bar is the range over the tie-breaks. |
| `compare_r50_intervals_<rule>` (2) | The same plot for R50. R50 moves in steps, so lots of random orders tie with a targeted order, and the area plot is the one to read first. |
| `compare_groups_cadiz_<measure>_by_category` (4) | One measure for the Gulf of Cadiz consumers by taxonomic category, with the median, the quartiles and the Kruskal–Wallis result. |

## Previews

### compare_area_intervals_all_prey

![compare_area_intervals_all_prey](compare_area_intervals_all_prey.png)

### compare_area_intervals_half_diet

![compare_area_intervals_half_diet](compare_area_intervals_half_diet.png)

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

### compare_fit_angolan_betweenness

![compare_fit_angolan_betweenness](compare_fit_angolan_betweenness.png)

### compare_fit_angolan_effective_prey

![compare_fit_angolan_effective_prey](compare_fit_angolan_effective_prey.png)

### compare_fit_angolan_n_predators

![compare_fit_angolan_n_predators](compare_fit_angolan_n_predators.png)

### compare_fit_angolan_n_prey

![compare_fit_angolan_n_prey](compare_fit_angolan_n_prey.png)

### compare_fit_angolan_total_degree

![compare_fit_angolan_total_degree](compare_fit_angolan_total_degree.png)

### compare_fit_cadiz_betweenness

![compare_fit_cadiz_betweenness](compare_fit_cadiz_betweenness.png)

### compare_fit_cadiz_effective_prey

![compare_fit_cadiz_effective_prey](compare_fit_cadiz_effective_prey.png)

### compare_fit_cadiz_n_predators

![compare_fit_cadiz_n_predators](compare_fit_cadiz_n_predators.png)

### compare_fit_cadiz_n_prey

![compare_fit_cadiz_n_prey](compare_fit_cadiz_n_prey.png)

### compare_fit_cadiz_total_degree

![compare_fit_cadiz_total_degree](compare_fit_cadiz_total_degree.png)

### compare_fit_mondego_betweenness

![compare_fit_mondego_betweenness](compare_fit_mondego_betweenness.png)

### compare_fit_mondego_effective_prey

![compare_fit_mondego_effective_prey](compare_fit_mondego_effective_prey.png)

### compare_fit_mondego_n_predators

![compare_fit_mondego_n_predators](compare_fit_mondego_n_predators.png)

### compare_fit_mondego_n_prey

![compare_fit_mondego_n_prey](compare_fit_mondego_n_prey.png)

### compare_fit_mondego_total_degree

![compare_fit_mondego_total_degree](compare_fit_mondego_total_degree.png)

### compare_fragmentation

![compare_fragmentation](compare_fragmentation.png)

### compare_global_structure

![compare_global_structure](compare_global_structure.png)

### compare_groups_cadiz_effective_prey_by_category

![compare_groups_cadiz_effective_prey_by_category](compare_groups_cadiz_effective_prey_by_category.png)

### compare_groups_cadiz_n_predators_by_category

![compare_groups_cadiz_n_predators_by_category](compare_groups_cadiz_n_predators_by_category.png)

### compare_groups_cadiz_n_prey_by_category

![compare_groups_cadiz_n_prey_by_category](compare_groups_cadiz_n_prey_by_category.png)

### compare_groups_cadiz_total_degree_by_category

![compare_groups_cadiz_total_degree_by_category](compare_groups_cadiz_total_degree_by_category.png)

### compare_guild_removal

![compare_guild_removal](compare_guild_removal.png)

### compare_knockouts

![compare_knockouts](compare_knockouts.png)

### compare_l50_link_strength

![compare_l50_link_strength](compare_l50_link_strength.png)

### compare_link_strength

![compare_link_strength](compare_link_strength.png)

### compare_r50_intervals_all_prey

![compare_r50_intervals_all_prey](compare_r50_intervals_all_prey.png)

### compare_r50_intervals_half_diet

![compare_r50_intervals_half_diet](compare_r50_intervals_half_diet.png)

### compare_removal_angolan_all_prey_centrality

![compare_removal_angolan_all_prey_centrality](compare_removal_angolan_all_prey_centrality.png)

### compare_removal_angolan_all_prey_trophic

![compare_removal_angolan_all_prey_trophic](compare_removal_angolan_all_prey_trophic.png)

### compare_removal_angolan_half_diet_centrality

![compare_removal_angolan_half_diet_centrality](compare_removal_angolan_half_diet_centrality.png)

### compare_removal_angolan_half_diet_trophic

![compare_removal_angolan_half_diet_trophic](compare_removal_angolan_half_diet_trophic.png)

### compare_removal_cadiz_all_prey_centrality

![compare_removal_cadiz_all_prey_centrality](compare_removal_cadiz_all_prey_centrality.png)

### compare_removal_cadiz_all_prey_trophic

![compare_removal_cadiz_all_prey_trophic](compare_removal_cadiz_all_prey_trophic.png)

### compare_removal_cadiz_half_diet_centrality

![compare_removal_cadiz_half_diet_centrality](compare_removal_cadiz_half_diet_centrality.png)

### compare_removal_cadiz_half_diet_trophic

![compare_removal_cadiz_half_diet_trophic](compare_removal_cadiz_half_diet_trophic.png)

### compare_removal_mondego_all_prey_centrality

![compare_removal_mondego_all_prey_centrality](compare_removal_mondego_all_prey_centrality.png)

### compare_removal_mondego_all_prey_trophic

![compare_removal_mondego_all_prey_trophic](compare_removal_mondego_all_prey_trophic.png)

### compare_removal_mondego_half_diet_centrality

![compare_removal_mondego_half_diet_centrality](compare_removal_mondego_half_diet_centrality.png)

### compare_removal_mondego_half_diet_trophic

![compare_removal_mondego_half_diet_trophic](compare_removal_mondego_half_diet_trophic.png)

### compare_rho_intervals

![compare_rho_intervals](compare_rho_intervals.png)

### compare_trophic_level

![compare_trophic_level](compare_trophic_level.png)
