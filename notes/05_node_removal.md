# Removing groups (nodes)

The methods are in [`code/README.md`](../code/README.md), and the figures are in [`figures/05_node_removal/`](../figures/05_node_removal/README.md).

## Single knockouts

Only 4 of the 43 groups cause any secondary extinction when they are removed by themselves ([`cadiz_node_knockouts.csv`](../output/cadiz_node_knockouts.csv)):

| group removed | lost, all-prey rule | lost, half-diet rule |
|---|---|---|
| Detritus | 1 | 33 |
| Phytoplankton | 3 | 15 |
| Meso and microzooplankton | 1 | 11 |
| Macrozooplankton | 0 | 2 |

Removing Benthic cephalopods cuts the largest feeding loop from 23 groups down to 11. Further, no single removal splits the web, as the largest connected component is always all 42 groups that are left.

## Guild removals

From [`cadiz_guild_removal.csv`](../output/cadiz_guild_removal.csv):
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

Removing predators (upper consumers, top predators or marine mammals/birds/turtles) never causes an extinction. That is partly built into the rule, though, as it only works bottom-up and cannot show predator release.

## R50 by removal order

A lower R50 means the web collapses after fewer removals ([`cadiz_node_robustness_summary.csv`](../output/cadiz_node_robustness_summary.csv)).

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

For the random orders, 95% of R50 values fall between 0.44 and 0.51 with all prey lost, 0.22 and 0.51 with 3/4 of the diet lost, 0.10 and 0.46 with half of the diet lost, and 0.02 and 0.32 with 1/4 of the diet lost.

## Against random orders

R50 moves in steps of 1/41, so lots of random orders tie with a targeted order. With all prey lost, for example, most connected first has an R50 of 0.44, and only 1.1% of random orders are lower, but 22.8% are lower or equal (the `frac_random_below` and `frac_random_at_or_below` columns in [`cadiz_node_robustness_summary.csv`](../output/cadiz_node_robustness_summary.csv)).

The R50 table in the panel figure `node_removal_results` now only bolds an order when fewer than 5% of random orders do as badly, counting ties. So, most links first, fewest links first and recalculated betweenness first (all 0.44 with all prey lost) are not bold anymore. The bold orders are most important prey first, PageRank importance first and lowest trophic level first, under both rules.

The area under the share-lost curve tells the same story ([`compare_webs_stats_removal.csv`](../output/compare_webs_stats_removal.csv)). Most connected first is not different from random (p = 0.11 with all prey lost and 0.71 with half of diet lost), and neither is highest betweenness first (p = 0.19 and 0.60, respectively). Lowest trophic level first and most important prey first are different from random under both rules, though (p = 0.002).

## When does the surviving web split?

Each value is the fraction of living groups removed when the surviving groups first stop forming one connected web, and the random values are the median of 1000 orders ([`cadiz_node_fragmentation.csv`](../output/cadiz_node_fragmentation.csv)).

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
- The rule only works bottom-up, as consumers can starve but no prey ever increases when its predator is removed. Top-down effects would need a dynamic model.
- There is no prey switching, so a consumer cannot replace the prey it loses.
- The removal orders are ranked once on the intact web, except for the two recalculated ones.
- The choice of θ changes how fragile the web looks, and the R50 table above shows which results hold for every θ.
