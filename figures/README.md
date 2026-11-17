# Figures

Every figure is made by a script in `code/`, so to change a figure, edit its script and rerun it instead of editing the image. Each folder has its own README with a description and a preview of every figure in it.

| Folder | Contents | Figures |
|---|---|---|
| [`01_web/`](01_web/README.md) | The web itself | 2 |
| [`02_distributions/`](02_distributions/README.md) | Distributions | 11 |
| [`03_structure/`](03_structure/README.md) | Structure against null models | 3 |
| [`04_centrality/`](04_centrality/README.md) | Centrality against trophic level | 10 |
| [`05_node_removal/`](05_node_removal/README.md) | Removing groups | 16 |
| [`06_link_removal/`](06_link_removal/README.md) | Cutting links | 12 |
| [`07_explainer/`](07_explainer/README.md) | The explainer figure | 1 |
| [`08_comparison/`](08_comparison/README.md) | Comparison with other ecosystems | 51 |
| [`09_connectivity_and_diet_diversity/`](09_connectivity_and_diet_diversity/README.md) | Connectivity and Diet Diversity Panels | 1 |

## Figures in the results draft

The results draft (11/12) uses six figures. Three of them are panel figures, which combine several single figures into one. The last column gives the figures and tables with the intervals and tests for the same result.

| Draft figure | File | Intervals and tests |
|---|---|---|
| 1 · methods explainer | [`07_explainer/explainer`](07_explainer/explainer.png) | none needed |
| 2 · the network | [`01_web/food_web`](01_web/food_web.png) | baseline numbers in `output/compare_webs_stats_baseline.csv` |
| 3 · trophic level against connectivity | [`09_connectivity_and_diet_diversity/tl_vs_connectivity`](09_connectivity_and_diet_diversity/tl_vs_connectivity.png) | [`08_comparison/compare_rho_intervals`](08_comparison/compare_rho_intervals.png) and the `08_comparison/compare_cadiz_tl_vs_*` figures |
| 4 · single knockouts | [`05_node_removal/node_knockouts`](05_node_removal/node_knockouts.png) | none, as a single removal has no random order to compare with |
| 5 · node removal | [`05_node_removal/node_removal_results`](05_node_removal/node_removal_results.png) | `08_comparison/compare_cadiz_robustness_*`, [`compare_r50_intervals_*`](08_comparison/compare_r50_intervals_all_prey.png) and [`compare_area_intervals_*`](08_comparison/compare_area_intervals_all_prey.png) |
| 6 · link removal | [`06_link_removal/link_removal_results`](06_link_removal/link_removal_results.png) | not done yet |

Out of these figures, panels to analyze connectivity and diet diversity, effects of node removal on robustness, and effects of link removal on robustness were created.
