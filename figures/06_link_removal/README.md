# Cutting links

These figures are drawn by [`code/link_removal.py`](../../code/link_removal.py), except for the panel figure `link_removal_results`, which is drawn by [`code/link_removal_panels.py`](../../code/link_removal_panels.py). The results behind them are summarized in [`notes/06_link_removal.md`](../../notes/06_link_removal.md).

| Figure | What it shows |
|---|---|
| [`link_knockouts`](link_knockouts.png) · [pdf](link_knockouts.pdf) | The feeding links whose loss by itself causes a secondary extinction, with the number of groups lost under each rule. |
| [`edge_betweenness_vs_link_strength`](edge_betweenness_vs_link_strength.png) · [pdf](edge_betweenness_vs_link_strength.pdf) | Edge betweenness against link strength for all 397 links. |
| [`link_giant_component_no_extinctions`](link_giant_component_no_extinctions.png) · [pdf](link_giant_component_no_extinctions.pdf) | Size of the largest connected component as links are cut, without starvation (bond percolation). |
| [`link_giant_component_with_extinctions`](link_giant_component_with_extinctions.png) · [pdf](link_giant_component_with_extinctions.pdf) | Size of the largest connected component as links are cut, with starvation under the all-prey rule. |
| [`l50_summary`](l50_summary.png) · [pdf](l50_summary.pdf) | L50 for random order, highest edge betweenness first and weakest links first under both rules, with the 95% range of the random orders. The L50 of every order is in `cadiz_link_robustness_summary.csv`. |
| [`link_removal_results`](link_removal_results.png) · [pdf](link_removal_results.pdf) | Fraction of living groups lost as links are cut under both rules (A, B), and the L50 table (C). |
| [`link_robustness_all_prey_betweenness`](link_robustness_all_prey_betweenness.png) · [pdf](link_robustness_all_prey_betweenness.pdf) | Fraction of living groups lost as links are cut, highest edge betweenness first, static vs. recalculated, under the all-prey rule. The gray band is the 95% range of 500 random orders. |
| [`link_robustness_all_prey_strength`](link_robustness_all_prey_strength.png) · [pdf](link_robustness_all_prey_strength.pdf) | Fraction of living groups lost as links are cut, strongest vs. weakest links first, under the all-prey rule. The gray band is the 95% range of 500 random orders. |
| [`link_robustness_all_prey_trophic_position`](link_robustness_all_prey_trophic_position.png) · [pdf](link_robustness_all_prey_trophic_position.pdf) | Fraction of living groups lost as links are cut, lowest vs. highest trophic level first, under the all-prey rule. The gray band is the 95% range of 500 random orders. |
| [`link_robustness_half_diet_betweenness`](link_robustness_half_diet_betweenness.png) · [pdf](link_robustness_half_diet_betweenness.pdf) | Fraction of living groups lost as links are cut, highest edge betweenness first, static vs. recalculated, under the half-diet rule. The gray band is the 95% range of 500 random orders. |
| [`link_robustness_half_diet_strength`](link_robustness_half_diet_strength.png) · [pdf](link_robustness_half_diet_strength.pdf) | Fraction of living groups lost as links are cut, strongest vs. weakest links first, under the half-diet rule. The gray band is the 95% range of 500 random orders. |
| [`link_robustness_half_diet_trophic_position`](link_robustness_half_diet_trophic_position.png) · [pdf](link_robustness_half_diet_trophic_position.pdf) | Fraction of living groups lost as links are cut, lowest vs. highest trophic level first, under the half-diet rule. The gray band is the 95% range of 500 random orders. |

### link_knockouts

![link_knockouts](link_knockouts.png)

### edge_betweenness_vs_link_strength

![edge_betweenness_vs_link_strength](edge_betweenness_vs_link_strength.png)

### link_giant_component_no_extinctions

![link_giant_component_no_extinctions](link_giant_component_no_extinctions.png)

### link_giant_component_with_extinctions

![link_giant_component_with_extinctions](link_giant_component_with_extinctions.png)

### l50_summary

![l50_summary](l50_summary.png)

### link_removal_results

![link_removal_results](link_removal_results.png)

### link_robustness_all_prey_betweenness

![link_robustness_all_prey_betweenness](link_robustness_all_prey_betweenness.png)

### link_robustness_all_prey_strength

![link_robustness_all_prey_strength](link_robustness_all_prey_strength.png)

### link_robustness_all_prey_trophic_position

![link_robustness_all_prey_trophic_position](link_robustness_all_prey_trophic_position.png)

### link_robustness_half_diet_betweenness

![link_robustness_half_diet_betweenness](link_robustness_half_diet_betweenness.png)

### link_robustness_half_diet_strength

![link_robustness_half_diet_strength](link_robustness_half_diet_strength.png)

### link_robustness_half_diet_trophic_position

![link_robustness_half_diet_trophic_position](link_robustness_half_diet_trophic_position.png)
