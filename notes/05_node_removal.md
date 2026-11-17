# Removing groups (nodes)

Methods: [`code/README.md`](../code/README.md). Figures: [`figures/05_node_removal/`](../figures/05_node_removal/README.md).

## Single knockouts ([`cadiz_node_knockouts.csv`](../output/cadiz_node_knockouts.csv))
- Only 4 of 43 groups cause any secondary extinction when removed alone:

| group removed | lost, all-prey rule | lost, half-diet rule |
|---|---|---|
| Detritus | 1 | 33 |
| Phytoplankton | 3 | 15 |
| Meso and microzooplankton | 1 | 11 |
| Macrozooplankton | 0 | 2 |

- Removing Benthic cephalopods cuts the largest feeding loop from 23 groups to 11.
- No single removal splits the web: the largest connected component is always all 42 remaining groups.

## Guild removals ([`cadiz_guild_removal.csv`](../output/cadiz_guild_removal.csv))
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

- Removing predators (upper consumers, top predators, marine mammals/birds/turtles) never causes an extinction. The rule only works bottom-up, so it cannot show predator release.

## R50 by removal order ([`cadiz_node_robustness_summary.csv`](../output/cadiz_node_robustness_summary.csv))
Lower R50 = the web collapses after fewer removals.

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

- Random orders, all prey lost: 95% of R50 values fall between 0.44 and 0.51.
- Random orders, 3/4 of diet lost: 95% of R50 values fall between 0.22 and 0.51.
- Random orders, half of diet lost: 95% of R50 values fall between 0.10 and 0.46.
- Random orders, 1/4 of diet lost: 95% of R50 values fall between 0.02 and 0.32.

## When does the surviving web split? ([`cadiz_node_fragmentation.csv`](../output/cadiz_node_fragmentation.csv))
Values are the fraction of living groups removed when the surviving groups first stop forming one connected web. Random = median of 1000 orders.

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
- The rule only works bottom-up, as consumers starve but no prey ever increases when its predator is removed. Top-down effects would need a dynamic model.
- No prey switching: a consumer cannot replace lost prey.
- Removal orders are ranked once on the intact web, except the two recalculated attacks.
- The choice of θ changes how fragile the web looks. The sensitivity table shows which conclusions survive every θ.
