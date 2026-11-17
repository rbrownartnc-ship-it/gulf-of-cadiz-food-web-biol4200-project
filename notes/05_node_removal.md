# Removing groups (nodes)

Methods: [`code/README.md`](../code/README.md). Figures: [`figures/05_node_removal/`](../figures/05_node_removal/README.md).

## Single knockouts

Only 4 of the 43 groups cause a secondary extinction when removed alone. All four have a trophic level of 2.1 or lower ([`cadiz_node_knockouts.csv`](../output/cadiz_node_knockouts.csv)):

| group removed | lost, all-prey rule | lost, half-diet rule |
|---|---|---|
| Detritus | 1 | 33 |
| Phytoplankton | 3 | 15 |
| Meso and microzooplankton | 1 | 11 |
| Macrozooplankton | 0 | 2 |

The removal of Benthic cephalopods decreases the largest feeding loop from 23 groups to 11. No single removal splits the web: without secondary extinctions, the remaining 42 groups stay connected.

## Guild removals

Source: [`cadiz_guild_removal.csv`](../output/cadiz_guild_removal.csv).
| guild removed | groups | lost, all-prey | lost, half-diet | living left (of 41), all-prey / half-diet |
|---|---|---|---|---|
| primary producers (phytoplankton) | 1 | 3 | 15 | 37 / 25 |
| detritus and discards | 2 | 1 | 34 | 40 / 7 |
| primary consumers (TL < 2.5) | 6 | 1 | 34 | 34 / 1 |
| mid-level consumers (2.5 ≤ TL < 3.5) | 19 | 0 | 14 | 22 / 8 |
| upper consumers (TL ≥ 3.5) | 15 | 0 | 0 | 26 / 26 |
| top predators (no predators) | 6 | 0 | 0 | 35 / 35 |
| invertebrates (excl. phytoplankton) | 16 | 10 | 24 | 15 / 1 |
| fishes | 20 | 0 | 6 | 21 / 15 |
| marine mammals, birds, turtles | 4 | 0 | 0 | 37 / 37 |

The removal of predators (upper consumers, top predators, or marine mammals, birds and turtles) causes no extinctions. The extinction rule partly causes this result, because the rule works only bottom-up and cannot show predator release.

## R50 by removal order

R50 is the fraction of living groups that you must remove before half of them are lost. A lower R50 means that the web fails after fewer removals ([`cadiz_node_robustness_summary.csv`](../output/cadiz_node_robustness_summary.csv)).

| order | R50, all prey lost | R50, 3/4 of diet lost | R50, half of diet lost | R50, 1/4 of diet lost |
|---|---|---|---|---|
| random | 0.48 | 0.40 | 0.27 | 0.15 |
| most connected first | 0.44 | 0.27 | 0.17 | 0.12 |
| least connected first | 0.44 | 0.44 | 0.22 | 0.15 |
| highest trophic level first | 0.51 | 0.51 | 0.51 | 0.51 |
| lowest trophic level first | 0.39 | 0.15 | 0.07 | 0.02 |
| most important prey first | 0.39 | 0.10 | 0.05 | 0.05 |
| highest PageRank importance first | 0.32 | 0.10 | 0.07 | 0.02 |
| highest betweenness first | 0.49 | 0.34 | 0.29 | 0.17 |
| most connected first (recalculated) | 0.46 | 0.34 | 0.22 | 0.12 |
| highest betweenness first (recalculated) | 0.44 | 0.32 | 0.27 | 0.15 |

95% range of R50 for the random orders: 0.44–0.51 (all prey lost), 0.22–0.51 (3/4 of diet lost), 0.10–0.46 (half of diet lost) and 0.02–0.32 (1/4 of diet lost).

## Against random orders

R50 changes in steps of 1/41. Thus, many random orders have the same R50 as a targeted order. For example, under all prey lost, the most connected groups first give an R50 of 0.44. Only 1.1% of random orders have a lower R50, but 22.8% have a lower or equal R50 (columns `frac_random_below` and `frac_random_at_or_below` in [`cadiz_node_robustness_summary.csv`](../output/cadiz_node_robustness_summary.csv)).

The R50 table in the panel figure `node_removal_results` shows an order in bold only when fewer than 5% of random orders do as badly, with ties counted. Thus, most links first, fewest links first and recalculated betweenness first (all 0.44 under all prey lost) are not bold. Under both rules, the bold orders are most important prey first, PageRank importance first and lowest trophic level first.

The area under the share-lost curve has no ties, and it gives the same result ([`compare_webs_stats_removal.csv`](../output/compare_webs_stats_removal.csv)). The most connected groups first is not different from random (p = 0.11 for all prey lost, 0.71 for half of diet lost). The highest betweenness groups first is also not different from random (p = 0.19 and 0.60). The lowest trophic levels first and the most important prey first are different from random under both rules (p = 0.002).

## When does the surviving web split?

Each value is the fraction of living groups removed when the surviving groups first stop being one connected web. The random values are the median of 1000 orders ([`cadiz_node_fragmentation.csv`](../output/cadiz_node_fragmentation.csv)).

| rule | order | first split |
|---|---|---|
| no secondary extinctions | random | 0.76 (95%: 0.39–0.93) |
| no secondary extinctions | most connected first | 0.39 |
| no secondary extinctions | least connected first | 0.83 |
| no secondary extinctions | highest trophic level first | 0.80 |
| no secondary extinctions | lowest trophic level first | 0.63 |
| no secondary extinctions | most important prey first | 0.44 |
| no secondary extinctions | highest PageRank importance first | 0.66 |
| no secondary extinctions | highest betweenness first | 0.56 |
| no secondary extinctions | most connected first (recalculated) | 0.46 |
| no secondary extinctions | highest betweenness first (recalculated) | 0.46 |
| all prey lost | random | 0.76 (95%: 0.39–0.90) |
| all prey lost | most connected first | 0.66 |
| all prey lost | least connected first | 0.76 |
| all prey lost | highest trophic level first | 0.80 |
| all prey lost | lowest trophic level first | 0.51 |
| all prey lost | most important prey first | 0.61 |
| all prey lost | highest PageRank importance first | 0.49 |
| all prey lost | highest betweenness first | 0.63 |
| all prey lost | most connected first (recalculated) | 0.51 |
| all prey lost | highest betweenness first (recalculated) | 0.59 |
| half of diet lost | random | 0.37 (95%: 0.17–0.59) |
| half of diet lost | most connected first | 0.37 |
| half of diet lost | least connected first | 0.34 |
| half of diet lost | highest trophic level first | 0.80 |
| half of diet lost | lowest trophic level first | 0.10 |
| half of diet lost | most important prey first | 0.15 |
| half of diet lost | highest PageRank importance first | 0.10 |
| half of diet lost | highest betweenness first | 0.49 |
| half of diet lost | most connected first (recalculated) | 0.32 |
| half of diet lost | highest betweenness first (recalculated) | 0.34 |

## Limitations
- The extinction rule works only bottom-up. Consumers can starve, but no prey increases when its predator goes. Top-down effects need a dynamic model.
- The rule has no prey switching. A consumer cannot replace the prey that it loses.
- The code ranks each removal order once on the intact web, except the two recalculated orders.
- The value of θ changes how fragile the web looks. The R50 table above shows which results stay the same for all values of θ.
