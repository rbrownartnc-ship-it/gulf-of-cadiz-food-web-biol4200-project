# Comparison with other ecosystems

This note has the same measurements for the Gulf of Cadiz, the Angolan shelf and the Mondego estuary, and then the intervals and tests on them. The methods are in [`code/README.md`](../code/README.md), the figures are in [`figures/08_comparison/`](../figures/08_comparison/README.md), and the tables are `output/compare_webs_*.csv`.

## The webs

| network | site | reference | groups | links |
|---|---|---|---|---|
| FW_005 | Gulf of Cadiz | Torres MA., Coll M., Heymans JJ., Christensen V,. Sobrino I. | 43 | 411 |
| FW_003 | Angolan shelf | Angelini, R., Velho, VF. | 28 | 127 |
| FW_016_01 | Mondego estuary | Baeta, A. , Niquil, A., Marques, J. C., Patrício, J. | 36 | 240 |

All three record the share of each predator's diet made up of each prey, so the same methods work for all of them. Each one is cleaned the same way, by dropping the Ecopath `Import` row, keeping detritus, cannibalism and weak links, and rescaling every diet to sum to 1.

The Angolan shelf and Mondego estuary food webs are drawn the same way as the Gulf of Cadiz in [`compare_angola_food_web`](../figures/08_comparison/compare_angola_food_web.png) and [`compare_mondego_food_web`](../figures/08_comparison/compare_mondego_food_web.png). The Mondego estuary has 19 groups at trophic level 2 and nothing above 3.04.

## Baseline statistics

The main rows of this table are also shown as a figure in [`compare_baseline_statistics`](../figures/08_comparison/compare_baseline_statistics.png).

| Statistic | Gulf of Cadiz | Angolan shelf | Mondego estuary |
|---|---|---|---|
| nodes (groups) | 43 | 28 | 36 |
| living groups | 41 | 27 | 35 |
| links (incl. cannibalism) | 411 | 127 | 240 |
| links (excl. cannibalism) | 397 | 124 | 234 |
| connectance L/S^2 | 0.222 | 0.162 | 0.185 |
| mean number of prey = mean number of predators | 9.233 | 4.429 | 6.500 |
| SD number of prey | 6.782 | 2.645 | 8.507 |
| SD number of predators | 7.813 | 4.316 | 4.937 |
| mean total degree | 18.465 | 8.857 | 13 |
| SD total degree | 8.373 | 3.768 | 8.479 |
| max total degree | 39 | 15 | 30 |
| basal groups | 3 | 2 | 5 |
| top predators | 6 | 4 | 0 |
| mean trophic level | 3.142 | 2.897 | 2.039 |
| max trophic level | 4.836 | 4.321 | 3.041 |
| mean effective number of prey (consumers) | 5.257 | 4.141 | 3.569 |
| median share of diet from largest prey | 0.394 | 0.310 | 0.680 |
| clustering coefficient | 0.571 | 0.357 | 0.562 |
| mean path length | 1.594 | 1.780 | 1.681 |
| degree centralization | 0.403 | 0.245 | 0.533 |
| in-degree centralization (prey) | 0.384 | 0.176 | 0.573 |
| out-degree centralization (predators) | 0.433 | 0.329 | 0.691 |
| betweenness centralization | 0.168 | 0.029 | 0.026 |

## Centralization against random graphs

Each centralization is compared against 1000 random directed graphs with the same nodes and links. Betweenness should be read carefully, though. The Angolan shelf web has no feeding loops while the random graphs do, so betweenness is more spread out in the random graphs for a reason that has nothing to do with which groups are central. Degree centralization does not have this problem.

| Web | Measure | Observed | Random mean (95% range) | z | p |
|---|---|---|---|---|---|
| Gulf of Cadiz | degree centralization | 0.403 | 0.174 (0.112 to 0.256) | 6.2 | 0.002 |
| Gulf of Cadiz | in-degree centralization (prey) | 0.384 | 0.149 (0.092 to 0.214) | 7.1 | 0.002 |
| Gulf of Cadiz | out-degree centralization (predators) | 0.433 | 0.149 (0.092 to 0.214) | 8.5 | 0.002 |
| Gulf of Cadiz | betweenness centralization | 0.168 | 0.027 (0.017 to 0.045) | 18.5 | 0.002 |
| Angolan shelf | degree centralization | 0.245 | 0.192 (0.114 to 0.305) | 1.2 | 0.21 |
| Angolan shelf | in-degree centralization (prey) | 0.176 | 0.161 (0.099 to 0.252) | 0.4 | 0.97 |
| Angolan shelf | out-degree centralization (predators) | 0.329 | 0.160 (0.099 to 0.252) | 4.0 | 0.014 |
| Angolan shelf | betweenness centralization | 0.029 | 0.089 (0.048 to 0.150) | −2.2 | 0.002 |
| Mondego estuary | degree centralization | 0.533 | 0.181 (0.121 to 0.272) | 8.6 | 0.002 |
| Mondego estuary | in-degree centralization (prey) | 0.573 | 0.152 (0.103 to 0.220) | 11.9 | 0.002 |
| Mondego estuary | out-degree centralization (predators) | 0.691 | 0.151 (0.103 to 0.250) | 14.8 | 0.002 |
| Mondego estuary | betweenness centralization | 0.026 | 0.048 (0.028 to 0.080) | −1.6 | 0.020 |

## Other whole-web measures

The ratios are against a random graph of the same size and density.

| measure | Gulf of Cadiz | Angolan shelf | Mondego estuary |
|---|---|---|---|
| share of groups in feeding loops | 0.535 | 0.000 | 0.250 |
| clustering / random | 1.34 | 1.09 | 1.59 |
| path length / random | 1.22 | 1.17 | 1.18 |
| diameter | 3 | 3 | 3 |
| degree assortativity | −0.096 | −0.137 | −0.379 |
| trophic coherence q | 0.786 | 0.498 | 0.546 |

## Diets, degrees and trophic level

Each cell is the median of that property, with the mean in parentheses.

| property | Gulf of Cadiz | Angolan shelf | Mondego estuary |
|---|---|---|---|
| number of prey (in-degree) | 9.00 (9.23) | 5.00 (4.43) | 3.00 (6.50) |
| number of predators (out-degree) | 7.00 (9.23) | 2.00 (4.43) | 6.00 (6.50) |
| total degree | 18.00 (18.47) | 8.00 (8.86) | 10.00 (13.00) |
| importance as prey (out-strength) | 0.34 (0.91) | 0.23 (0.93) | 0.17 (0.85) |
| trophic level | 3.27 (3.14) | 3.13 (2.90) | 2.00 (2.04) |
| clustering coefficient | 0.57 (0.57) | 0.34 (0.36) | 0.57 (0.56) |
| betweenness | 0.00 (0.02) | 0.01 (0.01) | 0.00 (0.00) |
| omnivory index | 0.20 (0.23) | 0.15 (0.18) | 0.00 (0.08) |
| diet diversity (effective number of prey) | 4.69 (5.26) | 4.36 (4.14) | 2.21 (3.57) |
| share of diet from the single largest prey | 0.39 (0.47) | 0.31 (0.45) | 0.68 (0.68) |
| link strength (share of predator's diet) | 0.04 (0.10) | 0.17 (0.21) | 0.03 (0.13) |

The groups at each extreme are in [`compare_webs_extremes.csv`](../output/compare_webs_extremes.csv).

## Trophic level against each measure (consumers)

Each Spearman ρ has a bootstrap 95% interval (10,000 resamples) and a permutation p-value, and the slope is the least-squares slope per unit of trophic level.

| Web | Measure | n | ρ (95% interval) | Permutation p | Slope per trophic level (95% interval) |
|---|---|---|---|---|---|
| Gulf of Cadiz | number of prey | 40 | +0.75 (+0.53 to +0.88) | < 0.001 | 6.2 (3.91 to 8.87) |
| Gulf of Cadiz | effective number of prey | 40 | +0.69 (+0.46 to +0.83) | < 0.001 | 2.87 (1.83 to 4.15) |
| Gulf of Cadiz | number of predators | 40 | −0.65 (−0.83 to −0.39) | < 0.001 | −7.34 (−9.43 to −5.3) |
| Gulf of Cadiz | total degree | 40 | −0.07 (−0.38 to +0.25) | 0.67 | −1.14 (−4.11 to 2.39) |
| Gulf of Cadiz | betweenness | 40 | +0.00 (−0.34 to +0.35) | 1.00 | 0.0112 (0.00044 to 0.0292) |
| Angolan shelf | number of prey | 26 | +0.82 (+0.61 to +0.93) | < 0.001 | 2.73 (1.91 to 3.52) |
| Angolan shelf | effective number of prey | 26 | +0.87 (+0.69 to +0.94) | < 0.001 | 2.5 (1.86 to 3.13) |
| Angolan shelf | number of predators | 26 | −0.61 (−0.84 to −0.27) | 0.001 | −3.69 (−6.23 to −1.58) |
| Angolan shelf | total degree | 26 | −0.13 (−0.60 to +0.35) | 0.52 | −0.958 (−3.85 to 1.54) |
| Angolan shelf | betweenness | 26 | −0.02 (−0.48 to +0.45) | 0.93 | 0.00335 (−0.00197 to 0.00948) |
| Mondego estuary | number of prey | 31 | +0.79 (+0.57 to +0.89) | < 0.001 | 21.5 (13.2 to 31.9) |
| Mondego estuary | effective number of prey | 31 | +0.80 (+0.55 to +0.92) | < 0.001 | 9.26 (6.54 to 11.3) |
| Mondego estuary | number of predators | 31 | −0.36 (−0.65 to −0.01) | 0.051 | −2.87 (−5 to −0.115) |
| Mondego estuary | total degree | 31 | +0.70 (+0.41 to +0.87) | < 0.001 | 18.6 (10.1 to 30.1) |
| Mondego estuary | betweenness | 31 | +0.66 (+0.39 to +0.83) | < 0.001 | 0.0156 (0.00525 to 0.0281) |

None of the webs differ from each other in ρ for number of prey, effective number of prey or number of predators, as every interval for the difference includes 0. Total degree and betweenness only differ between the Mondego estuary and the other two webs ([`compare_webs_stats_correlation_differences.csv`](../output/compare_webs_stats_correlation_differences.csv)).

For the other centralities, `*` marks p < 0.05:

| measure | Gulf of Cadiz | Angolan shelf | Mondego estuary |
|---|---|---|---|
| importance as prey (out-strength) | −0.68\* | −0.69\* | −0.19 |
| betweenness (weighted) | −0.18 | 0.01 | 0.52\* |
| clustering coefficient | 0.42\* | 0.19 | −0.53\* |
| clustering (directed) | 0.47\* | 0.19 | −0.49\* |
| PageRank importance | −0.68\* | −0.63\* | −0.36\* |

## Differences between groups of nodes

We used a Kruskal–Wallis test across the trophic bands and, for the Gulf of Cadiz, across the taxonomic categories. Groups with fewer than 3 members are left out, so the Mondego estuary only has two bands and no test. The pairwise Mann–Whitney tests are in [`compare_webs_stats_group_tests.csv`](../output/compare_webs_stats_group_tests.csv).

| Web | Grouping | Measure | H | p | ε² |
|---|---|---|---|---|---|
| Gulf of Cadiz | trophic band | number of prey | 19.3 | < 0.001 | 0.49 |
| Gulf of Cadiz | trophic band | effective number of prey | 15.6 | < 0.001 | 0.40 |
| Gulf of Cadiz | trophic band | number of predators | 12.3 | 0.002 | 0.32 |
| Gulf of Cadiz | trophic band | total degree | 1.0 | 0.60 | 0.03 |
| Gulf of Cadiz | trophic band | betweenness | 0.5 | 0.77 | 0.01 |
| Angolan shelf | trophic band | number of prey | 14.5 | < 0.001 | 0.58 |
| Angolan shelf | trophic band | effective number of prey | 16.0 | < 0.001 | 0.64 |
| Angolan shelf | trophic band | number of predators | 7.5 | 0.024 | 0.30 |
| Angolan shelf | trophic band | total degree | 0.3 | 0.84 | 0.01 |
| Angolan shelf | trophic band | betweenness | 0.5 | 0.80 | 0.02 |
| Gulf of Cadiz | taxonomic category | number of prey | 5.1 | 0.077 | 0.13 |
| Gulf of Cadiz | taxonomic category | effective number of prey | 0.9 | 0.64 | 0.02 |
| Gulf of Cadiz | taxonomic category | number of predators | 17.4 | < 0.001 | 0.45 |
| Gulf of Cadiz | taxonomic category | total degree | 7.6 | 0.022 | 0.19 |
| Gulf of Cadiz | taxonomic category | betweenness | 10.0 | 0.007 | 0.26 |

## Removing one group at a time

These are the groups whose loss by itself causes a secondary extinction, and the full table is [`compare_webs_knockouts.csv`](../output/compare_webs_knockouts.csv).

With all prey lost:

| web | groups that matter | worst (extinctions) |
|---|---|---|
| Gulf of Cadiz | 3 | Phytoplankton (3), Detritus (1), Meso and microzooplankton (1) |
| Angolan shelf | 1 | Detritus (3) |
| Mondego estuary | 2 | Detritus (7), Phytoplankton (1) |

With half of diet lost:

| web | groups that matter | worst (extinctions) |
|---|---|---|
| Gulf of Cadiz | 4 | Detritus (33), Phytoplankton (15), Meso and microzooplankton (11), Macrozooplankton (2) |
| Angolan shelf | 4 | Phytoplankton (19), Small Zoo (14), Detritus (10), Large Zoo (2) |
| Mondego estuary | 3 | Detritus (25), Phytoplankton (4), Microphytobenthos (1) |

## Removing a whole trophic band

Each cell reads as groups removed → secondary extinctions / living groups left.

With all prey lost:

| band | Gulf of Cadiz | Angolan shelf | Mondego estuary |
|---|---|---|---|
| basal living groups | 1 → 3 / 37 | 1 → 0 / 26 | 4 → 1 / 30 |
| non-living (detritus, discards) | 2 → 1 / 40 | 1 → 3 / 24 | 1 → 7 / 28 |
| primary consumers (TL < 2.5) | 6 → 1 / 34 | 7 → 0 / 20 | 26 → 0 / 9 |
| mid-level consumers (2.5 ≤ TL < 3.5) | 19 → 0 / 22 | 12 → 0 / 15 | 5 → 0 / 30 |
| upper consumers (TL ≥ 3.5) | 15 → 0 / 26 | 7 → 0 / 20 | 0 → 0 / 35 |
| top predators (no predators) | 6 → 0 / 35 | 4 → 0 / 23 | 0 → 0 / 35 |

With half of diet lost:

| band | Gulf of Cadiz | Angolan shelf | Mondego estuary |
|---|---|---|---|
| basal living groups | 1 → 15 / 25 | 1 → 19 / 7 | 4 → 6 / 25 |
| non-living (detritus, discards) | 2 → 34 / 7 | 1 → 10 / 17 | 1 → 25 / 10 |
| primary consumers (TL < 2.5) | 6 → 34 / 1 | 7 → 19 / 1 | 26 → 5 / 4 |
| mid-level consumers (2.5 ≤ TL < 3.5) | 19 → 14 / 8 | 12 → 7 / 8 | 5 → 0 / 30 |
| upper consumers (TL ≥ 3.5) | 15 → 0 / 26 | 7 → 0 / 20 | 0 → 0 / 35 |
| top predators (no predators) | 6 → 0 / 35 | 4 → 0 / 23 | 0 → 0 / 35 |

## Node removal: each order against random orders

The random order is 1000 trials. A targeted order is a fixed ranking, so it only changes where groups tie on the score, and each one is run 200 times with the ties broken at random. The range is the 95% range for the random order and the range over the tie-breaks for a targeted order, and each p-value is a two-sided Monte Carlo test against the 1000 random orders. R50 moves in steps of 1 / (number of living groups), so lots of random orders tie with a targeted one. So, the area under the share-lost curve (where 0.5 means no secondary extinctions) is the better one to go by.

| Web | Rule | Differs from random (area, p < 0.05) | Does not |
|---|---|---|---|
| Gulf of Cadiz | all prey lost | most important prey first, lowest trophic level first and highest trophic level first | most connected first, highest betweenness first and least connected first |
| Gulf of Cadiz | half of diet lost | most important prey first, lowest trophic level first and highest trophic level first | most connected first, highest betweenness first and least connected first |
| Angolan shelf | all prey lost | most connected first, highest betweenness first, most important prey first and lowest trophic level first | highest trophic level first and least connected first |
| Angolan shelf | half of diet lost | lowest trophic level first and highest trophic level first | most connected first, highest betweenness first, most important prey first and least connected first |
| Mondego estuary | all prey lost | none | most connected first, highest betweenness first, most important prey first, lowest trophic level first, highest trophic level first and least connected first |
| Mondego estuary | half of diet lost | highest betweenness first, most important prey first, lowest trophic level first and highest trophic level first | most connected first and least connected first |

| Web | Rule | Order | Groups tied | R50 (range) | R50 p | Area (range) | Area p |
|---|---|---|---|---|---|---|---|
| Gulf of Cadiz | all prey lost | random |  | 0.480 (0.439 to 0.512) |  | 0.536 (0.502 to 0.586) |  |
| Gulf of Cadiz | all prey lost | most connected first | 29 | 0.439 (0.415 to 0.439) | 0.46 | 0.577 (0.577 to 0.582) | 0.11 |
| Gulf of Cadiz | all prey lost | highest betweenness first | 7 | 0.488 (0.488 to 0.488) | 1.00 | 0.571 (0.571 to 0.571) | 0.19 |
| Gulf of Cadiz | all prey lost | most important prey first | 5 | 0.390 (0.390 to 0.390) | 0.002 | 0.645 (0.645 to 0.645) | 0.002 |
| Gulf of Cadiz | all prey lost | lowest trophic level first | 6 | 0.390 (0.390 to 0.390) | 0.002 | 0.626 (0.626 to 0.626) | 0.002 |
| Gulf of Cadiz | all prey lost | highest trophic level first | 6 | 0.512 (0.512 to 0.512) | 0.63 | 0.500 (0.500 to 0.500) | 0.030 |
| Gulf of Cadiz | all prey lost | least connected first | 29 | 0.439 (0.439 to 0.439) | 0.46 | 0.561 (0.561 to 0.561) | 0.36 |
| Gulf of Cadiz | half of diet lost | random |  | 0.267 (0.098 to 0.463) |  | 0.751 (0.603 to 0.892) |  |
| Gulf of Cadiz | half of diet lost | most connected first | 29 | 0.171 (0.171 to 0.220) | 0.51 | 0.788 (0.761 to 0.791) | 0.71 |
| Gulf of Cadiz | half of diet lost | highest betweenness first | 7 | 0.293 (0.293 to 0.293) | 0.91 | 0.701 (0.701 to 0.701) | 0.60 |
| Gulf of Cadiz | half of diet lost | most important prey first | 5 | 0.049 (0.049 to 0.049) | 0.012 | 0.944 (0.944 to 0.944) | 0.002 |
| Gulf of Cadiz | half of diet lost | lowest trophic level first | 6 | 0.073 (0.073 to 0.073) | 0.034 | 0.950 (0.946 to 0.950) | 0.002 |
| Gulf of Cadiz | half of diet lost | highest trophic level first | 6 | 0.512 (0.512 to 0.512) | 0.004 | 0.500 (0.500 to 0.500) | 0.002 |
| Gulf of Cadiz | half of diet lost | least connected first | 29 | 0.220 (0.220 to 0.220) | 0.83 | 0.757 (0.747 to 0.759) | 0.95 |
| Angolan shelf | all prey lost | random |  | 0.509 (0.444 to 0.519) |  | 0.528 (0.500 to 0.596) |  |
| Angolan shelf | all prey lost | most connected first | 21 | 0.370 (0.333 to 0.370) | 0.010 | 0.669 (0.669 to 0.678) | 0.004 |
| Angolan shelf | all prey lost | highest betweenness first | 7 | 0.444 (0.444 to 0.444) | 0.11 | 0.607 (0.607 to 0.607) | 0.026 |
| Angolan shelf | all prey lost | most important prey first | 12 | 0.259 (0.259 to 0.259) | 0.002 | 0.750 (0.750 to 0.750) | 0.002 |
| Angolan shelf | all prey lost | lowest trophic level first | 5 | 0.333 (0.333 to 0.333) | 0.004 | 0.726 (0.726 to 0.726) | 0.002 |
| Angolan shelf | all prey lost | highest trophic level first | 5 | 0.519 (0.519 to 0.519) | 1.00 | 0.500 (0.500 to 0.500) | 0.14 |
| Angolan shelf | all prey lost | least connected first | 21 | 0.519 (0.519 to 0.519) | 1.00 | 0.500 (0.500 to 0.503) | 0.14 |
| Angolan shelf | half of diet lost | random |  | 0.249 (0.037 to 0.481) |  | 0.771 (0.596 to 0.951) |  |
| Angolan shelf | half of diet lost | most connected first | 21 | 0.148 (0.037 to 0.148) | 0.61 | 0.861 (0.854 to 0.932) | 0.47 |
| Angolan shelf | half of diet lost | highest betweenness first | 7 | 0.333 (0.333 to 0.333) | 0.71 | 0.696 (0.696 to 0.711) | 0.52 |
| Angolan shelf | half of diet lost | most important prey first | 12 | 0.074 (0.074 to 0.074) | 0.35 | 0.907 (0.907 to 0.907) | 0.25 |
| Angolan shelf | half of diet lost | lowest trophic level first | 5 | 0.037 (0.037 to 0.037) | 0.18 | 0.954 (0.951 to 0.957) | 0.030 |
| Angolan shelf | half of diet lost | highest trophic level first | 5 | 0.519 (0.519 to 0.519) | 0.022 | 0.500 (0.500 to 0.500) | 0.002 |
| Angolan shelf | half of diet lost | least connected first | 21 | 0.519 (0.444 to 0.519) | 0.022 | 0.603 (0.603 to 0.660) | 0.076 |
| Mondego estuary | all prey lost | random |  | 0.503 (0.486 to 0.514) |  | 0.510 (0.500 to 0.528) |  |
| Mondego estuary | all prey lost | most connected first | 26 | 0.514 (0.514 to 0.514) | 1.00 | 0.507 (0.507 to 0.508) | 0.98 |
| Mondego estuary | all prey lost | highest betweenness first | 15 | 0.514 (0.514 to 0.514) | 1.00 | 0.500 (0.500 to 0.500) | 0.97 |
| Mondego estuary | all prey lost | most important prey first | 0 | 0.486 (0.486 to 0.486) | 0.82 | 0.528 (0.528 to 0.528) | 0.086 |
| Mondego estuary | all prey lost | lowest trophic level first | 23 | 0.486 (0.486 to 0.486) | 0.82 | 0.526 (0.525 to 0.528) | 0.23 |
| Mondego estuary | all prey lost | highest trophic level first | 23 | 0.514 (0.514 to 0.514) | 1.00 | 0.500 (0.500 to 0.500) | 0.97 |
| Mondego estuary | all prey lost | least connected first | 26 | 0.514 (0.514 to 0.514) | 1.00 | 0.500 (0.500 to 0.500) | 0.97 |
| Mondego estuary | half of diet lost | random |  | 0.438 (0.343 to 0.514) |  | 0.578 (0.515 to 0.653) |  |
| Mondego estuary | half of diet lost | most connected first | 26 | 0.486 (0.486 to 0.486) | 0.63 | 0.549 (0.535 to 0.554) | 0.57 |
| Mondego estuary | half of diet lost | highest betweenness first | 15 | 0.514 (0.514 to 0.514) | 0.22 | 0.500 (0.500 to 0.500) | 0.012 |
| Mondego estuary | half of diet lost | most important prey first | 0 | 0.257 (0.257 to 0.257) | 0.002 | 0.736 (0.736 to 0.736) | 0.002 |
| Mondego estuary | half of diet lost | lowest trophic level first | 23 | 0.343 (0.286 to 0.343) | 0.11 | 0.697 (0.687 to 0.718) | 0.002 |
| Mondego estuary | half of diet lost | highest trophic level first | 23 | 0.514 (0.514 to 0.514) | 0.22 | 0.500 (0.500 to 0.500) | 0.012 |
| Mondego estuary | half of diet lost | least connected first | 26 | 0.457 (0.457 to 0.457) | 0.99 | 0.581 (0.564 to 0.585) | 0.87 |

The random-order R50 is lower with half of diet lost than with all prey lost in every web (a median difference of −0.22, −0.26 and −0.06 in the Gulf of Cadiz, Angolan shelf and Mondego estuary, respectively). The comparisons between rules and between webs are in [`compare_webs_stats_removal_contrasts.csv`](../output/compare_webs_stats_removal_contrasts.csv).

Unfortunately, link removal has not been tested this way yet.

## Fragmentation: share of groups removed before the web splits

These are without secondary extinctions, and "never" means the web stayed in one piece the whole time.

| removal order | Gulf of Cadiz | Angolan shelf | Mondego estuary |
|---|---|---|---|
| random | 0.743 | 0.761 | 0.694 |
| most connected first | 0.390 | 0.333 | 0.629 |
| least connected first | 0.829 | never | never |
| highest trophic level first | 0.805 | 0.963 | 0.714 |
| lowest trophic level first | 0.634 | 0.444 | never |
| most important prey first | 0.439 | 0.407 | never |
| highest PageRank importance first | 0.659 | 0.481 | never |
| highest betweenness first | 0.561 | 0.444 | 0.257 |

## L50: fraction of links cut before half the groups are gone

With all prey lost:

| removal order | Gulf of Cadiz | Angolan shelf | Mondego estuary |
|---|---|---|---|
| random | 0.724 | 0.673 | 0.717 |
| strongest links first | 0.569 | 0.500 | 0.235 |
| weakest links first | 0.924 | 0.863 | 0.944 |
| highest edge betweenness first | 0.375 | 0.363 | 0.872 |

With half of diet lost:

| removal order | Gulf of Cadiz | Angolan shelf | Mondego estuary |
|---|---|---|---|
| random | 0.207 | 0.220 | 0.327 |
| strongest links first | 0.013 | 0.048 | 0.073 |
| weakest links first | 0.811 | 0.621 | 0.889 |
| highest edge betweenness first | 0.209 | 0.258 | 0.654 |
