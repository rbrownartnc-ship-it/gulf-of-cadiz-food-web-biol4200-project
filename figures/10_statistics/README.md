# Uncertainty and significance

Drawn by [`code/significance.py`](../../code/significance.py) from the three webs the paper keeps (Gulf of Cadiz, Angolan shelf, Mondego estuary). If a figure needs changing, change the code and not the image. Numbers behind every figure: `output/stats_*.csv`. Notes: [`notes/08_significance.md`](../../notes/08_significance.md).

| figure | what it shows |
|---|---|
| [`rho_intervals`](rho_intervals.png) · [pdf](rho_intervals.pdf) | Spearman ρ of each measure with trophic level, with its bootstrap 95% interval, for the three webs. Filled = the interval excludes 0. |
| [`area_intervals_half_diet`](area_intervals_half_diet.png) · [pdf](area_intervals_half_diet.pdf) | Area under the share-lost curve for each removal order, three webs, rule “half of diet lost”. Thick bar = 95% range of random orders; thin bar = range over tie-breaks; open marker = not different from random orders. |
| [`area_intervals_all_prey`](area_intervals_all_prey.png) · [pdf](area_intervals_all_prey.pdf) | Area under the share-lost curve for each removal order, three webs, rule “all prey lost”. Thick bar = 95% range of random orders; thin bar = range over tie-breaks; open marker = not different from random orders. |
| [`r50_intervals_half_diet`](r50_intervals_half_diet.png) · [pdf](r50_intervals_half_diet.pdf) | R50 for each removal order, three webs, rule “half of diet lost”. Thick bar = 95% range of random orders; thin bar = range over tie-breaks; open marker = not different from random orders. |
| [`r50_intervals_all_prey`](r50_intervals_all_prey.png) · [pdf](r50_intervals_all_prey.pdf) | R50 for each removal order, three webs, rule “all prey lost”. Thick bar = 95% range of random orders; thin bar = range over tie-breaks; open marker = not different from random orders. |
| [`centralization_vs_random`](centralization_vs_random.png) · [pdf](centralization_vs_random.pdf) | Degree and betweenness centralization of each web against random directed graphs with the same number of nodes and links. |
| [`fit_cadiz_n_prey`](fit_cadiz_n_prey.png) · [pdf](fit_cadiz_n_prey.pdf) | Gulf of Cadiz: trophic level against number of prey, 40 consumers. ρ = +0.75 [+0.53, +0.88], permutation p < 0.001; slope +6.2 per trophic level [+3.91, +8.87]. |
| [`fit_cadiz_effective_prey`](fit_cadiz_effective_prey.png) · [pdf](fit_cadiz_effective_prey.pdf) | Gulf of Cadiz: trophic level against effective number of prey, 40 consumers. ρ = +0.69 [+0.46, +0.83], permutation p < 0.001; slope +2.87 per trophic level [+1.83, +4.15]. |
| [`fit_cadiz_n_predators`](fit_cadiz_n_predators.png) · [pdf](fit_cadiz_n_predators.pdf) | Gulf of Cadiz: trophic level against number of predators, 40 consumers. ρ = -0.65 [-0.83, -0.39], permutation p < 0.001; slope -7.34 per trophic level [-9.43, -5.3]. |
| [`fit_cadiz_total_degree`](fit_cadiz_total_degree.png) · [pdf](fit_cadiz_total_degree.pdf) | Gulf of Cadiz: trophic level against total degree, 40 consumers. ρ = -0.07 [-0.38, +0.25], permutation p = 0.67; slope -1.14 per trophic level [-4.11, +2.39]. |
| [`fit_cadiz_betweenness`](fit_cadiz_betweenness.png) · [pdf](fit_cadiz_betweenness.pdf) | Gulf of Cadiz: trophic level against betweenness centrality, 40 consumers. ρ = +0.00 [-0.34, +0.35], permutation p = 1.00; slope +0.0112 per trophic level [+0.000443, +0.0292]. |
| [`fit_angolan_n_prey`](fit_angolan_n_prey.png) · [pdf](fit_angolan_n_prey.pdf) | Angolan shelf: trophic level against number of prey, 26 consumers. ρ = +0.82 [+0.61, +0.93], permutation p < 0.001; slope +2.73 per trophic level [+1.91, +3.52]. |
| [`fit_angolan_effective_prey`](fit_angolan_effective_prey.png) · [pdf](fit_angolan_effective_prey.pdf) | Angolan shelf: trophic level against effective number of prey, 26 consumers. ρ = +0.87 [+0.69, +0.94], permutation p < 0.001; slope +2.5 per trophic level [+1.86, +3.13]. |
| [`fit_angolan_n_predators`](fit_angolan_n_predators.png) · [pdf](fit_angolan_n_predators.pdf) | Angolan shelf: trophic level against number of predators, 26 consumers. ρ = -0.61 [-0.84, -0.27], permutation p = 0.001; slope -3.69 per trophic level [-6.23, -1.58]. |
| [`fit_angolan_total_degree`](fit_angolan_total_degree.png) · [pdf](fit_angolan_total_degree.pdf) | Angolan shelf: trophic level against total degree, 26 consumers. ρ = -0.13 [-0.60, +0.35], permutation p = 0.52; slope -0.958 per trophic level [-3.85, +1.54]. |
| [`fit_angolan_betweenness`](fit_angolan_betweenness.png) · [pdf](fit_angolan_betweenness.pdf) | Angolan shelf: trophic level against betweenness centrality, 26 consumers. ρ = -0.02 [-0.48, +0.45], permutation p = 0.93; slope +0.00335 per trophic level [-0.00197, +0.00948]. |
| [`fit_mondego_n_prey`](fit_mondego_n_prey.png) · [pdf](fit_mondego_n_prey.pdf) | Mondego estuary: trophic level against number of prey, 31 consumers. ρ = +0.79 [+0.57, +0.89], permutation p < 0.001; slope +21.5 per trophic level [+13.2, +31.9]. |
| [`fit_mondego_effective_prey`](fit_mondego_effective_prey.png) · [pdf](fit_mondego_effective_prey.pdf) | Mondego estuary: trophic level against effective number of prey, 31 consumers. ρ = +0.80 [+0.55, +0.92], permutation p < 0.001; slope +9.26 per trophic level [+6.54, +11.3]. |
| [`fit_mondego_n_predators`](fit_mondego_n_predators.png) · [pdf](fit_mondego_n_predators.pdf) | Mondego estuary: trophic level against number of predators, 31 consumers. ρ = -0.36 [-0.65, -0.01], permutation p = 0.051; slope -2.87 per trophic level [-5, -0.115]. |
| [`fit_mondego_total_degree`](fit_mondego_total_degree.png) · [pdf](fit_mondego_total_degree.pdf) | Mondego estuary: trophic level against total degree, 31 consumers. ρ = +0.70 [+0.41, +0.87], permutation p < 0.001; slope +18.6 per trophic level [+10.1, +30.1]. |
| [`fit_mondego_betweenness`](fit_mondego_betweenness.png) · [pdf](fit_mondego_betweenness.pdf) | Mondego estuary: trophic level against betweenness centrality, 31 consumers. ρ = +0.66 [+0.39, +0.83], permutation p < 0.001; slope +0.0156 per trophic level [+0.00525, +0.0281]. |
| [`removal_cadiz_all_prey_centrality`](removal_cadiz_all_prey_centrality.png) · [pdf](removal_cadiz_all_prey_centrality.pdf) | Gulf of Cadiz, rule “all prey lost”: most connected first and highest betweenness first against 1000 random orders. Coloured bands = range over 200 random tie-breaks; p = Monte Carlo test of the area under the curve against random orders. |
| [`removal_cadiz_all_prey_trophic`](removal_cadiz_all_prey_trophic.png) · [pdf](removal_cadiz_all_prey_trophic.pdf) | Gulf of Cadiz, rule “all prey lost”: lowest trophic level first and highest trophic level first against 1000 random orders. Coloured bands = range over 200 random tie-breaks; p = Monte Carlo test of the area under the curve against random orders. |
| [`removal_cadiz_half_diet_centrality`](removal_cadiz_half_diet_centrality.png) · [pdf](removal_cadiz_half_diet_centrality.pdf) | Gulf of Cadiz, rule “half of diet lost”: most connected first and highest betweenness first against 1000 random orders. Coloured bands = range over 200 random tie-breaks; p = Monte Carlo test of the area under the curve against random orders. |
| [`removal_cadiz_half_diet_trophic`](removal_cadiz_half_diet_trophic.png) · [pdf](removal_cadiz_half_diet_trophic.pdf) | Gulf of Cadiz, rule “half of diet lost”: lowest trophic level first and highest trophic level first against 1000 random orders. Coloured bands = range over 200 random tie-breaks; p = Monte Carlo test of the area under the curve against random orders. |
| [`removal_angolan_all_prey_centrality`](removal_angolan_all_prey_centrality.png) · [pdf](removal_angolan_all_prey_centrality.pdf) | Angolan shelf, rule “all prey lost”: most connected first and highest betweenness first against 1000 random orders. Coloured bands = range over 200 random tie-breaks; p = Monte Carlo test of the area under the curve against random orders. |
| [`removal_angolan_all_prey_trophic`](removal_angolan_all_prey_trophic.png) · [pdf](removal_angolan_all_prey_trophic.pdf) | Angolan shelf, rule “all prey lost”: lowest trophic level first and highest trophic level first against 1000 random orders. Coloured bands = range over 200 random tie-breaks; p = Monte Carlo test of the area under the curve against random orders. |
| [`removal_angolan_half_diet_centrality`](removal_angolan_half_diet_centrality.png) · [pdf](removal_angolan_half_diet_centrality.pdf) | Angolan shelf, rule “half of diet lost”: most connected first and highest betweenness first against 1000 random orders. Coloured bands = range over 200 random tie-breaks; p = Monte Carlo test of the area under the curve against random orders. |
| [`removal_angolan_half_diet_trophic`](removal_angolan_half_diet_trophic.png) · [pdf](removal_angolan_half_diet_trophic.pdf) | Angolan shelf, rule “half of diet lost”: lowest trophic level first and highest trophic level first against 1000 random orders. Coloured bands = range over 200 random tie-breaks; p = Monte Carlo test of the area under the curve against random orders. |
| [`removal_mondego_all_prey_centrality`](removal_mondego_all_prey_centrality.png) · [pdf](removal_mondego_all_prey_centrality.pdf) | Mondego estuary, rule “all prey lost”: most connected first and highest betweenness first against 1000 random orders. Coloured bands = range over 200 random tie-breaks; p = Monte Carlo test of the area under the curve against random orders. |
| [`removal_mondego_all_prey_trophic`](removal_mondego_all_prey_trophic.png) · [pdf](removal_mondego_all_prey_trophic.pdf) | Mondego estuary, rule “all prey lost”: lowest trophic level first and highest trophic level first against 1000 random orders. Coloured bands = range over 200 random tie-breaks; p = Monte Carlo test of the area under the curve against random orders. |
| [`removal_mondego_half_diet_centrality`](removal_mondego_half_diet_centrality.png) · [pdf](removal_mondego_half_diet_centrality.pdf) | Mondego estuary, rule “half of diet lost”: most connected first and highest betweenness first against 1000 random orders. Coloured bands = range over 200 random tie-breaks; p = Monte Carlo test of the area under the curve against random orders. |
| [`removal_mondego_half_diet_trophic`](removal_mondego_half_diet_trophic.png) · [pdf](removal_mondego_half_diet_trophic.pdf) | Mondego estuary, rule “half of diet lost”: lowest trophic level first and highest trophic level first against 1000 random orders. Coloured bands = range over 200 random tie-breaks; p = Monte Carlo test of the area under the curve against random orders. |
| [`groups_cadiz_n_prey_by_category`](groups_cadiz_n_prey_by_category.png) · [pdf](groups_cadiz_n_prey_by_category.pdf) | Gulf of Cadiz consumers: number of prey by taxonomic category. Kruskal–Wallis H = 5.1, p = 0.077. |
| [`groups_cadiz_effective_prey_by_category`](groups_cadiz_effective_prey_by_category.png) · [pdf](groups_cadiz_effective_prey_by_category.pdf) | Gulf of Cadiz consumers: effective number of prey by taxonomic category. Kruskal–Wallis H = 0.9, p = 0.64. |
| [`groups_cadiz_n_predators_by_category`](groups_cadiz_n_predators_by_category.png) · [pdf](groups_cadiz_n_predators_by_category.pdf) | Gulf of Cadiz consumers: number of predators by taxonomic category. Kruskal–Wallis H = 17.4, p < 0.001. |
| [`groups_cadiz_total_degree_by_category`](groups_cadiz_total_degree_by_category.png) · [pdf](groups_cadiz_total_degree_by_category.pdf) | Gulf of Cadiz consumers: total degree by taxonomic category. Kruskal–Wallis H = 7.6, p = 0.022. |

### rho_intervals

![rho_intervals](rho_intervals.png)

### area_intervals_half_diet

![area_intervals_half_diet](area_intervals_half_diet.png)

### area_intervals_all_prey

![area_intervals_all_prey](area_intervals_all_prey.png)

### r50_intervals_half_diet

![r50_intervals_half_diet](r50_intervals_half_diet.png)

### r50_intervals_all_prey

![r50_intervals_all_prey](r50_intervals_all_prey.png)

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
