# Distributions of node and link properties

The methods are described in [`code/README.md`](../code/README.md), and the figures are in [`figures/02_distributions/`](../figures/02_distributions/README.md).

| Property | Mean | Median | SD | Range | Skewness | Variance/mean (random web) |
|---|---|---|---|---|---|---|
| number of prey (in-degree) | 9.23 | 9.00 | 6.78 | 0–25 | 0.47 | 4.98 (0.78) |
| number of predators (out-degree) | 9.23 | 7.00 | 7.81 | 0–27 | 0.65 | 6.61 (0.78) |
| total degree | 18.47 | 18.00 | 8.37 | 4–39 | 0.44 | 3.80 (0.78) |
| importance as prey (out-strength) | 0.91 | 0.34 | 1.26 | 0.00–5.13 | 1.82 | |
| trophic level | 3.14 | 3.27 | 0.91 | 1.00–4.84 | −0.70 | |
| clustering coefficient | 0.57 | 0.57 | 0.15 | 0.17–0.94 | 0.03 | |
| betweenness | 0.02 | 0.00 | 0.04 | 0.00–0.18 | 3.67 | |
| omnivory index | 0.23 | 0.20 | 0.26 | 0.00–1.30 | 2.63 | |
| diet diversity (effective number of prey) | 5.26 | 4.69 | 3.17 | 1.00–13.30 | 0.52 | |
| link strength (share of predator's diet) | 0.10 | 0.04 | 0.16 | 0.00–1.00 | 3.19 | |

The full summary statistics are in [`cadiz_distribution_stats.csv`](../output/cadiz_distribution_stats.csv).

Most links are weak, as 28% of links carry less than 0.01 of the predator's diet and only 3% carry at least half of it. The degrees are also much more uneven than in a random web of the same size, since the variance/mean of each degree measure (3.80 to 6.61) is far above the random-web value of 0.78. In other words, a few groups have many prey or many predators, while most groups have far fewer.
