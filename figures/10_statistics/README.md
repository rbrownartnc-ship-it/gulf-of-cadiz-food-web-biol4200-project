# Uncertainty and significance

Drawn by [`code/significance.py`](../../code/significance.py) for the three webs the paper keeps (Gulf of Cadiz, Angolan shelf and Mondego estuary). If a figure needs changing, change the code and not the image. The numbers behind every figure are in `output/stats_*.csv`, and the notes are in [`notes/08_significance.md`](../../notes/08_significance.md).

Every figure is one column wide (3.4 in). In all of them a filled marker means the result is different from random (or the interval excludes 0) and an open marker means it is not, so you can read off what is and is not significant without the table. Unfortunately, only node removal is covered so far, not link removal.

## All three webs in one plot

Look at these first, as each one puts the three webs side by side.

| figure | what it shows |
|---|---|
| [`rho_intervals`](rho_intervals.png) · [pdf](rho_intervals.pdf) | Spearman ρ of each measure with trophic level for the three webs, with its bootstrap 95% interval. A filled marker means the interval excludes 0. That is the case in all three webs for number of prey, effective number of prey and number of predators. For total degree, the interval includes 0 in the Gulf of Cadiz and Angolan shelf. For betweenness centrality, the interval includes 0 in the Gulf of Cadiz and Angolan shelf. |
| [`area_intervals_all_prey`](area_intervals_all_prey.png) · [pdf](area_intervals_all_prey.pdf) | Area under the share-lost curve for each removal order in the three webs, under the rule “all prey lost”. The thick bar on the random row is the 95% range of 1000 random orders, and a thin bar is the range over the 200 tie-breaks. A filled marker means the order is different from random (p < 0.05). Different from random: Gulf of Cadiz (most important prey first, lowest trophic level first and highest trophic level first); Angolan shelf (most connected first, highest betweenness first, most important prey first and lowest trophic level first); Mondego estuary (none). |
| [`area_intervals_half_diet`](area_intervals_half_diet.png) · [pdf](area_intervals_half_diet.pdf) | Area under the share-lost curve for each removal order in the three webs, under the rule “half of diet lost”. The thick bar on the random row is the 95% range of 1000 random orders, and a thin bar is the range over the 200 tie-breaks. A filled marker means the order is different from random (p < 0.05). Different from random: Gulf of Cadiz (most important prey first, lowest trophic level first and highest trophic level first); Angolan shelf (lowest trophic level first and highest trophic level first); Mondego estuary (highest betweenness first, most important prey first, lowest trophic level first and highest trophic level first). |
| [`r50_intervals_all_prey`](r50_intervals_all_prey.png) · [pdf](r50_intervals_all_prey.pdf) | The same plot for R50, under the rule “all prey lost”. R50 moves in steps, so lots of random orders tie with a targeted order and the area version is the safer one to read. Different from random: Gulf of Cadiz (most important prey first and lowest trophic level first); Angolan shelf (most connected first, most important prey first and lowest trophic level first); Mondego estuary (none). |
| [`r50_intervals_half_diet`](r50_intervals_half_diet.png) · [pdf](r50_intervals_half_diet.pdf) | The same plot for R50, under the rule “half of diet lost”. R50 moves in steps, so lots of random orders tie with a targeted order and the area version is the safer one to read. Different from random: Gulf of Cadiz (most important prey first, lowest trophic level first and highest trophic level first); Angolan shelf (highest trophic level first); Mondego estuary (most important prey first). |
| [`centralization_vs_random`](centralization_vs_random.png) · [pdf](centralization_vs_random.pdf) | Degree and betweenness centralization of each web (marker) against the 95% range of 1000 random directed graphs with the same nodes and links (bar). Degree centralization is 0.40 in the Gulf of Cadiz, 0.25 in the Angolan shelf and 0.53 in the Mondego estuary, against 0.17 to 0.19 on average for the random graphs. |

## Trophic level against each measure: Gulf of Cadiz

Every consumer group as a point, with a least-squares line and its bootstrap 95% band.

| figure | what it shows |
|---|---|
| [`fit_cadiz_n_prey`](fit_cadiz_n_prey.png) · [pdf](fit_cadiz_n_prey.pdf) | Number of prey against trophic level for the 40 consumers. ρ = +0.75 (95% interval +0.53 to +0.88, permutation p < 0.001). The line changes by +6.20 per trophic level (+3.91 to +8.87). |
| [`fit_cadiz_effective_prey`](fit_cadiz_effective_prey.png) · [pdf](fit_cadiz_effective_prey.pdf) | Effective number of prey against trophic level for the 40 consumers. ρ = +0.69 (95% interval +0.46 to +0.83, permutation p < 0.001). The line changes by +2.87 per trophic level (+1.83 to +4.15). |
| [`fit_cadiz_n_predators`](fit_cadiz_n_predators.png) · [pdf](fit_cadiz_n_predators.pdf) | Number of predators against trophic level for the 40 consumers. ρ = −0.65 (95% interval −0.83 to −0.39, permutation p < 0.001). The line changes by −7.34 per trophic level (−9.43 to −5.30). |
| [`fit_cadiz_total_degree`](fit_cadiz_total_degree.png) · [pdf](fit_cadiz_total_degree.pdf) | Total degree against trophic level for the 40 consumers. ρ = −0.07 (95% interval −0.38 to +0.25, permutation p = 0.67). The line changes by −1.14 per trophic level (−4.11 to +2.39). |
| [`fit_cadiz_betweenness`](fit_cadiz_betweenness.png) · [pdf](fit_cadiz_betweenness.pdf) | Betweenness centrality against trophic level for the 40 consumers. ρ = +0.00 (95% interval −0.34 to +0.35, permutation p = 1.00). The line changes by +0.0112 per trophic level (+0.000443 to +0.0292). |

## Trophic level against each measure: Angolan shelf

Every consumer group as a point, with a least-squares line and its bootstrap 95% band.

| figure | what it shows |
|---|---|
| [`fit_angolan_n_prey`](fit_angolan_n_prey.png) · [pdf](fit_angolan_n_prey.pdf) | Number of prey against trophic level for the 26 consumers. ρ = +0.82 (95% interval +0.61 to +0.93, permutation p < 0.001). The line changes by +2.73 per trophic level (+1.91 to +3.52). |
| [`fit_angolan_effective_prey`](fit_angolan_effective_prey.png) · [pdf](fit_angolan_effective_prey.pdf) | Effective number of prey against trophic level for the 26 consumers. ρ = +0.87 (95% interval +0.69 to +0.94, permutation p < 0.001). The line changes by +2.50 per trophic level (+1.86 to +3.13). |
| [`fit_angolan_n_predators`](fit_angolan_n_predators.png) · [pdf](fit_angolan_n_predators.pdf) | Number of predators against trophic level for the 26 consumers. ρ = −0.61 (95% interval −0.84 to −0.27, permutation p = 0.001). The line changes by −3.69 per trophic level (−6.23 to −1.58). |
| [`fit_angolan_total_degree`](fit_angolan_total_degree.png) · [pdf](fit_angolan_total_degree.pdf) | Total degree against trophic level for the 26 consumers. ρ = −0.13 (95% interval −0.60 to +0.35, permutation p = 0.52). The line changes by −0.96 per trophic level (−3.85 to +1.54). |
| [`fit_angolan_betweenness`](fit_angolan_betweenness.png) · [pdf](fit_angolan_betweenness.pdf) | Betweenness centrality against trophic level for the 26 consumers. ρ = −0.02 (95% interval −0.48 to +0.45, permutation p = 0.93). The line changes by +0.00335 per trophic level (−0.00197 to +0.00948). |

## Trophic level against each measure: Mondego estuary

Every consumer group as a point, with a least-squares line and its bootstrap 95% band.

| figure | what it shows |
|---|---|
| [`fit_mondego_n_prey`](fit_mondego_n_prey.png) · [pdf](fit_mondego_n_prey.pdf) | Number of prey against trophic level for the 31 consumers. ρ = +0.79 (95% interval +0.57 to +0.89, permutation p < 0.001). The line changes by +21.47 per trophic level (+13.19 to +31.94). |
| [`fit_mondego_effective_prey`](fit_mondego_effective_prey.png) · [pdf](fit_mondego_effective_prey.pdf) | Effective number of prey against trophic level for the 31 consumers. ρ = +0.80 (95% interval +0.55 to +0.92, permutation p < 0.001). The line changes by +9.26 per trophic level (+6.54 to +11.29). |
| [`fit_mondego_n_predators`](fit_mondego_n_predators.png) · [pdf](fit_mondego_n_predators.pdf) | Number of predators against trophic level for the 31 consumers. ρ = −0.36 (95% interval −0.65 to −0.01, permutation p = 0.051). The line changes by −2.87 per trophic level (−5.00 to −0.11). |
| [`fit_mondego_total_degree`](fit_mondego_total_degree.png) · [pdf](fit_mondego_total_degree.pdf) | Total degree against trophic level for the 31 consumers. ρ = +0.70 (95% interval +0.41 to +0.87, permutation p < 0.001). The line changes by +18.60 per trophic level (+10.11 to +30.14). |
| [`fit_mondego_betweenness`](fit_mondego_betweenness.png) · [pdf](fit_mondego_betweenness.pdf) | Betweenness centrality against trophic level for the 31 consumers. ρ = +0.66 (95% interval +0.39 to +0.83, permutation p < 0.001). The line changes by +0.0156 per trophic level (+0.00525 to +0.0281). |

## Node removal curves: Gulf of Cadiz

One figure for the two centrality orders and one for the two trophic-level orders, under each rule.

| figure | what it shows |
|---|---|
| [`removal_cadiz_all_prey_centrality`](removal_cadiz_all_prey_centrality.png) · [pdf](removal_cadiz_all_prey_centrality.pdf) | Rule “all prey lost”. Share of living groups lost as groups are removed, with most connected first in blue and highest betweenness first in orange (dashed), against 1000 random orders in gray (mean and 95% range). The colored bands are the range over the 200 tie-breaks, so no band means the ties do not matter. Against random orders: most connected first p = 0.11, highest betweenness first p = 0.19. |
| [`removal_cadiz_all_prey_trophic`](removal_cadiz_all_prey_trophic.png) · [pdf](removal_cadiz_all_prey_trophic.pdf) | Rule “all prey lost”. Share of living groups lost as groups are removed, with lowest trophic level first in blue and highest trophic level first in orange (dashed), against 1000 random orders in gray (mean and 95% range). The colored bands are the range over the 200 tie-breaks, so no band means the ties do not matter. Against random orders: lowest trophic level first p = 0.002, highest trophic level first p = 0.030. |
| [`removal_cadiz_half_diet_centrality`](removal_cadiz_half_diet_centrality.png) · [pdf](removal_cadiz_half_diet_centrality.pdf) | Rule “half of diet lost”. Share of living groups lost as groups are removed, with most connected first in blue and highest betweenness first in orange (dashed), against 1000 random orders in gray (mean and 95% range). The colored bands are the range over the 200 tie-breaks, so no band means the ties do not matter. Against random orders: most connected first p = 0.71, highest betweenness first p = 0.60. |
| [`removal_cadiz_half_diet_trophic`](removal_cadiz_half_diet_trophic.png) · [pdf](removal_cadiz_half_diet_trophic.pdf) | Rule “half of diet lost”. Share of living groups lost as groups are removed, with lowest trophic level first in blue and highest trophic level first in orange (dashed), against 1000 random orders in gray (mean and 95% range). The colored bands are the range over the 200 tie-breaks, so no band means the ties do not matter. Against random orders: lowest trophic level first p = 0.002, highest trophic level first p = 0.002. |

## Node removal curves: Angolan shelf

One figure for the two centrality orders and one for the two trophic-level orders, under each rule.

| figure | what it shows |
|---|---|
| [`removal_angolan_all_prey_centrality`](removal_angolan_all_prey_centrality.png) · [pdf](removal_angolan_all_prey_centrality.pdf) | Rule “all prey lost”. Share of living groups lost as groups are removed, with most connected first in blue and highest betweenness first in orange (dashed), against 1000 random orders in gray (mean and 95% range). The colored bands are the range over the 200 tie-breaks, so no band means the ties do not matter. Against random orders: most connected first p = 0.004, highest betweenness first p = 0.026. |
| [`removal_angolan_all_prey_trophic`](removal_angolan_all_prey_trophic.png) · [pdf](removal_angolan_all_prey_trophic.pdf) | Rule “all prey lost”. Share of living groups lost as groups are removed, with lowest trophic level first in blue and highest trophic level first in orange (dashed), against 1000 random orders in gray (mean and 95% range). The colored bands are the range over the 200 tie-breaks, so no band means the ties do not matter. Against random orders: lowest trophic level first p = 0.002, highest trophic level first p = 0.14. |
| [`removal_angolan_half_diet_centrality`](removal_angolan_half_diet_centrality.png) · [pdf](removal_angolan_half_diet_centrality.pdf) | Rule “half of diet lost”. Share of living groups lost as groups are removed, with most connected first in blue and highest betweenness first in orange (dashed), against 1000 random orders in gray (mean and 95% range). The colored bands are the range over the 200 tie-breaks, so no band means the ties do not matter. Against random orders: most connected first p = 0.47, highest betweenness first p = 0.52. |
| [`removal_angolan_half_diet_trophic`](removal_angolan_half_diet_trophic.png) · [pdf](removal_angolan_half_diet_trophic.pdf) | Rule “half of diet lost”. Share of living groups lost as groups are removed, with lowest trophic level first in blue and highest trophic level first in orange (dashed), against 1000 random orders in gray (mean and 95% range). The colored bands are the range over the 200 tie-breaks, so no band means the ties do not matter. Against random orders: lowest trophic level first p = 0.030, highest trophic level first p = 0.002. |

## Node removal curves: Mondego estuary

One figure for the two centrality orders and one for the two trophic-level orders, under each rule.

| figure | what it shows |
|---|---|
| [`removal_mondego_all_prey_centrality`](removal_mondego_all_prey_centrality.png) · [pdf](removal_mondego_all_prey_centrality.pdf) | Rule “all prey lost”. Share of living groups lost as groups are removed, with most connected first in blue and highest betweenness first in orange (dashed), against 1000 random orders in gray (mean and 95% range). The colored bands are the range over the 200 tie-breaks, so no band means the ties do not matter. Against random orders: most connected first p = 0.91, highest betweenness first p = 1.00. |
| [`removal_mondego_all_prey_trophic`](removal_mondego_all_prey_trophic.png) · [pdf](removal_mondego_all_prey_trophic.pdf) | Rule “all prey lost”. Share of living groups lost as groups are removed, with lowest trophic level first in blue and highest trophic level first in orange (dashed), against 1000 random orders in gray (mean and 95% range). The colored bands are the range over the 200 tie-breaks, so no band means the ties do not matter. Against random orders: lowest trophic level first p = 0.16, highest trophic level first p = 1.00. |
| [`removal_mondego_half_diet_centrality`](removal_mondego_half_diet_centrality.png) · [pdf](removal_mondego_half_diet_centrality.pdf) | Rule “half of diet lost”. Share of living groups lost as groups are removed, with most connected first in blue and highest betweenness first in orange (dashed), against 1000 random orders in gray (mean and 95% range). The colored bands are the range over the 200 tie-breaks, so no band means the ties do not matter. Against random orders: most connected first p = 0.65, highest betweenness first p = 0.016. |
| [`removal_mondego_half_diet_trophic`](removal_mondego_half_diet_trophic.png) · [pdf](removal_mondego_half_diet_trophic.pdf) | Rule “half of diet lost”. Share of living groups lost as groups are removed, with lowest trophic level first in blue and highest trophic level first in orange (dashed), against 1000 random orders in gray (mean and 95% range). The colored bands are the range over the 200 tie-breaks, so no band means the ties do not matter. Against random orders: lowest trophic level first p = 0.002, highest trophic level first p = 0.016. |

## Gulf of Cadiz consumers by taxonomic category

The three categories that the scatter plots color by, tested as groups.

| figure | what it shows |
|---|---|
| [`groups_cadiz_n_prey_by_category`](groups_cadiz_n_prey_by_category.png) · [pdf](groups_cadiz_n_prey_by_category.pdf) | Number of prey of the Gulf of Cadiz consumers by taxonomic category, with the median and the quartiles. Kruskal–Wallis H = 5.1, p = 0.077. No pair differs after the Holm correction. |
| [`groups_cadiz_effective_prey_by_category`](groups_cadiz_effective_prey_by_category.png) · [pdf](groups_cadiz_effective_prey_by_category.pdf) | Effective number of prey of the Gulf of Cadiz consumers by taxonomic category, with the median and the quartiles. Kruskal–Wallis H = 0.9, p = 0.64. No pair differs after the Holm correction. |
| [`groups_cadiz_n_predators_by_category`](groups_cadiz_n_predators_by_category.png) · [pdf](groups_cadiz_n_predators_by_category.pdf) | Number of predators of the Gulf of Cadiz consumers by taxonomic category, with the median and the quartiles. Kruskal–Wallis H = 17.4, p < 0.001. Pairs that differ after the Holm correction: fishes vs invertebrates & plankton, fishes vs marine mammals, birds, turtles and invertebrates & plankton vs marine mammals, birds, turtles. |
| [`groups_cadiz_total_degree_by_category`](groups_cadiz_total_degree_by_category.png) · [pdf](groups_cadiz_total_degree_by_category.pdf) | Total degree of the Gulf of Cadiz consumers by taxonomic category, with the median and the quartiles. Kruskal–Wallis H = 7.6, p = 0.022. Pairs that differ after the Holm correction: fishes vs marine mammals, birds, turtles and invertebrates & plankton vs marine mammals, birds, turtles. |

## Previews

### rho_intervals

![rho_intervals](rho_intervals.png)

### area_intervals_all_prey

![area_intervals_all_prey](area_intervals_all_prey.png)

### area_intervals_half_diet

![area_intervals_half_diet](area_intervals_half_diet.png)

### r50_intervals_all_prey

![r50_intervals_all_prey](r50_intervals_all_prey.png)

### r50_intervals_half_diet

![r50_intervals_half_diet](r50_intervals_half_diet.png)

### centralization_vs_random

![centralization_vs_random](centralization_vs_random.png)

### fit_cadiz_n_prey

![fit_cadiz_n_prey](fit_cadiz_n_prey.png)

### fit_cadiz_effective_prey

![fit_cadiz_effective_prey](fit_cadiz_effective_prey.png)

### fit_cadiz_n_predators

![fit_cadiz_n_predators](fit_cadiz_n_predators.png)

### fit_cadiz_total_degree

![fit_cadiz_total_degree](fit_cadiz_total_degree.png)

### fit_cadiz_betweenness

![fit_cadiz_betweenness](fit_cadiz_betweenness.png)

### fit_angolan_n_prey

![fit_angolan_n_prey](fit_angolan_n_prey.png)

### fit_angolan_effective_prey

![fit_angolan_effective_prey](fit_angolan_effective_prey.png)

### fit_angolan_n_predators

![fit_angolan_n_predators](fit_angolan_n_predators.png)

### fit_angolan_total_degree

![fit_angolan_total_degree](fit_angolan_total_degree.png)

### fit_angolan_betweenness

![fit_angolan_betweenness](fit_angolan_betweenness.png)

### fit_mondego_n_prey

![fit_mondego_n_prey](fit_mondego_n_prey.png)

### fit_mondego_effective_prey

![fit_mondego_effective_prey](fit_mondego_effective_prey.png)

### fit_mondego_n_predators

![fit_mondego_n_predators](fit_mondego_n_predators.png)

### fit_mondego_total_degree

![fit_mondego_total_degree](fit_mondego_total_degree.png)

### fit_mondego_betweenness

![fit_mondego_betweenness](fit_mondego_betweenness.png)

### removal_cadiz_all_prey_centrality

![removal_cadiz_all_prey_centrality](removal_cadiz_all_prey_centrality.png)

### removal_cadiz_all_prey_trophic

![removal_cadiz_all_prey_trophic](removal_cadiz_all_prey_trophic.png)

### removal_cadiz_half_diet_centrality

![removal_cadiz_half_diet_centrality](removal_cadiz_half_diet_centrality.png)

### removal_cadiz_half_diet_trophic

![removal_cadiz_half_diet_trophic](removal_cadiz_half_diet_trophic.png)

### removal_angolan_all_prey_centrality

![removal_angolan_all_prey_centrality](removal_angolan_all_prey_centrality.png)

### removal_angolan_all_prey_trophic

![removal_angolan_all_prey_trophic](removal_angolan_all_prey_trophic.png)

### removal_angolan_half_diet_centrality

![removal_angolan_half_diet_centrality](removal_angolan_half_diet_centrality.png)

### removal_angolan_half_diet_trophic

![removal_angolan_half_diet_trophic](removal_angolan_half_diet_trophic.png)

### removal_mondego_all_prey_centrality

![removal_mondego_all_prey_centrality](removal_mondego_all_prey_centrality.png)

### removal_mondego_all_prey_trophic

![removal_mondego_all_prey_trophic](removal_mondego_all_prey_trophic.png)

### removal_mondego_half_diet_centrality

![removal_mondego_half_diet_centrality](removal_mondego_half_diet_centrality.png)

### removal_mondego_half_diet_trophic

![removal_mondego_half_diet_trophic](removal_mondego_half_diet_trophic.png)

### groups_cadiz_n_prey_by_category

![groups_cadiz_n_prey_by_category](groups_cadiz_n_prey_by_category.png)

### groups_cadiz_effective_prey_by_category

![groups_cadiz_effective_prey_by_category](groups_cadiz_effective_prey_by_category.png)

### groups_cadiz_n_predators_by_category

![groups_cadiz_n_predators_by_category](groups_cadiz_n_predators_by_category.png)

### groups_cadiz_total_degree_by_category

![groups_cadiz_total_degree_by_category](groups_cadiz_total_degree_by_category.png)
