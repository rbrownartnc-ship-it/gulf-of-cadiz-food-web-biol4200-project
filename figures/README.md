# Figures

Every figure is drawn by a script, so to change one, change the script and rerun it. Each folder has its own README with a preview of every figure in it.

| Folder | Contents | Figures |
|---|---|---|
| [`01_web/`](01_web/README.md) | The web itself | 2 |
| [`02_distributions/`](02_distributions/README.md) | Distributions | 11 |
| [`03_structure/`](03_structure/README.md) | Structure against null models | 3 |
| [`04_centrality/`](04_centrality/README.md) | Centrality against trophic level | 10 |
| [`05_node_removal/`](05_node_removal/README.md) | Removing groups | 16 |
| [`06_edge_removal/`](06_edge_removal/README.md) | Cutting links | 12 |
| [`07_explainer_figure/`](07_explainer_figure/README.md) | The explainer figure | 1 |
| [`08_comparison/`](08_comparison/README.md) | Comparison with other ecosystems | 48 |
| [`09_connectivity&diet_diversity/`](09_connectivity&diet_diversity/README.md) | Connectivity and Diet Diversity Panels | 1 |

## Figures in the results draft

Our results draft (11/12) uses six figures. Three of them are panel figures, which put several of the single figures together. The last column is where the intervals and tests for the same result are.

| Draft figure | File | Intervals and tests |
|---|---|---|
| 1 · methods explainer | [`07_explainer_figure/explainer_figure`](07_explainer_figure/explainer_figure.png) | none needed |
| 2 · the network | [`01_web/cadiz_foodweb`](01_web/cadiz_foodweb.png) | baseline numbers in `output/compare_webs_stats_baseline.csv` |
| 3 · trophic level against connectivity | [`09_connectivity&diet_diversity/tl_vs_connectivity`](09_connectivity&diet_diversity/tl_vs_connectivity.png) | [`08_comparison/compare_rho_intervals`](08_comparison/compare_rho_intervals.png) and the `08_comparison/compare_fit_cadiz_*` figures |
| 4 · single knockouts | [`05_node_removal/single_group_knockouts`](05_node_removal/single_group_knockouts.png) | none, as a single removal has no random order to compare with |
| 5 · node removal | [`05_node_removal/node_removal_results`](05_node_removal/node_removal_results.png) | `08_comparison/compare_removal_cadiz_*`, [`compare_r50_intervals_*`](08_comparison/compare_r50_intervals_all_prey.png) and [`compare_area_intervals_*`](08_comparison/compare_area_intervals_all_prey.png) |
| 6 · link removal | [`06_edge_removal/link_removal_results`](06_edge_removal/link_removal_results.png) | not done yet |

Out of the 67 figures, panels to analyze connectivity and diet diversity, effects of node removal on robustness, and effects of edge removal on robustness were created. 

## Using the figures

Every figure is saved twice from the same drawing: a vector `.pdf` for LaTeX, and a 300-dpi `.png` for slides, Word and GitHub.

Each one is drawn at the size it prints, and no text is smaller than 6.5 pt at that size. So, insert them at that size, as shrinking a figure shrinks its text with it.

- **7 in wide** (the full text width of the two-column template): the `01_web/` figures, the explainer figure and the three panel figures (`node_removal_results`, `link_removal_results`, `tl_vs_connectivity`).
- **3.4 in wide** (one column): every other figure.

```latex
% one column (most figures)
\begin{figure}
  \includegraphics[width=\columnwidth]{figures/05_node_removal/r50_summary.pdf}
  \caption{...}
\end{figure}

% full width (01_web, the explainer and the panel figures)
\begin{figure*}
  \includegraphics[width=\textwidth]{figures/01_web/cadiz_foodweb.pdf}
  \caption{...}
\end{figure*}
```
