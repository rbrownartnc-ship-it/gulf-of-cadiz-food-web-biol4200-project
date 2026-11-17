# Link removal: cutting feeding links

Methods: [`code/README.md`](../code/README.md). Figures: [`figures/06_link_removal/`](../figures/06_link_removal/README.md).

## Single links ([`cadiz_link_knockouts.csv`](../output/cadiz_link_knockouts.csv))
- Links whose loss alone causes an extinction: 3 under the all-prey rule, 14 under the half-diet rule.
- Bridges: 0. No single link splits the web.

| link (prey → predator) | diet share | lost, all-prey | lost, half-diet |
|---|---|---|---|
| Phytoplankton → Meso and microzooplankton | 1.00 | 2 | 12 |
| Detritus → Macrozooplankton | 0.80 | 0 | 3 |
| Detritus → Benthic invertebrates FDS | 1.00 | 1 | 1 |
| Meso and microzooplankton → Anchovy | 1.00 | 1 | 1 |
| Meso and microzooplankton → Sardine | 0.95 | 0 | 1 |
| Detritus → Polychaetes | 0.90 | 0 | 1 |
| Detritus → Suprabenthos | 0.85 | 0 | 1 |
| Macrozooplankton → Horse mackerels | 0.85 | 0 | 1 |
| Meso and microzooplankton → Gelatinous zooplankton | 0.80 | 0 | 1 |
| Meso and microzooplankton → Small benthopelagic fishes | 0.51 | 0 | 1 |
| Macrozooplankton → Mackerels | 0.50 | 0 | 1 |
| Detritus → Bivalves | 0.50 | 0 | 1 |
| Phytoplankton → Bivalves | 0.50 | 0 | 1 |
| Meso and microzooplankton → Small demersal fishes | 0.50 | 0 | 1 |

- Highest edge betweenness: Benthopelagic cephalopods → Benthic cephalopods (0.116); Commercial sparids 2 → Benthopelagic cephalopods (0.056); Sharks → Benthopelagic cephalopods (0.050); Demersal fishes → Benthopelagic cephalopods (0.029); Juvenile hake → Benthic cephalopods (0.028).
- Edge betweenness against link strength: Spearman ρ = −0.20 (p = 4.8e-05): a weak negative relation, so links on many shortest paths are, on average, slightly weaker links.

## L50 by cutting order ([`cadiz_link_robustness_summary.csv`](../output/cadiz_link_robustness_summary.csv))
Lower L50 = the web collapses after fewer cuts.

| order | L50, all prey lost | L50, 3/4 of diet lost | L50, half of diet lost | L50, 1/4 of diet lost |
|---|---|---|---|---|
| random | 0.72 | 0.38 | 0.21 | 0.08 |
| strongest links first | 0.57 | 0.02 | 0.01 | 0.01 |
| weakest links first | 0.92 | 0.90 | 0.81 | 0.67 |
| highest edge betweenness first | 0.38 | 0.26 | 0.21 | 0.17 |
| highest edge betweenness first (recalculated) | 0.16 | 0.10 | 0.07 | 0.05 |
| links from lowest-trophic-level prey first | 0.41 | 0.02 | 0.01 | 0.01 |
| links into highest-trophic-level predators first | 0.67 | 0.23 | 0.13 | 0.06 |

- Random orders, all prey lost: 95% of L50 values fall between 0.62 and 0.82.
- Random orders, 3/4 of diet lost: 95% of L50 values fall between 0.22 and 0.52.
- Random orders, half of diet lost: 95% of L50 values fall between 0.08 and 0.33.
- Random orders, 1/4 of diet lost: 95% of L50 values fall between 0.02 and 0.16.

## When does the surviving web split? ([`cadiz_link_fragmentation.csv`](../output/cadiz_link_fragmentation.csv))
Values are the fraction of links cut when the surviving web first stops being one connected piece. A single group left with no links counts as a split. Random = median, measured every 10 cuts.

| rule | order | first split |
|---|---|---|
| no starvation (links cut only) | random | 0.68 (95%: 0.38–0.83) |
| no starvation (links cut only) | strongest links first | 0.26 |
| no starvation (links cut only) | weakest links first | 0.82 |
| no starvation (links cut only) | highest edge betweenness first | 0.51 |
| no starvation (links cut only) | highest edge betweenness first (recalculated) | 0.43 |
| no starvation (links cut only) | links from lowest-trophic-level prey first | 0.04 |
| no starvation (links cut only) | links into highest-trophic-level predators first | 0.02 |
| all prey lost | random | 0.68 (95%: 0.40–0.81) |
| all prey lost | strongest links first | 0.21 |
| all prey lost | weakest links first | 0.91 |
| all prey lost | highest edge betweenness first | 0.38 |
| all prey lost | highest edge betweenness first (recalculated) | 0.16 |
| all prey lost | links from lowest-trophic-level prey first | 0.04 |
| all prey lost | links into highest-trophic-level predators first | 0.85 |
| half of diet lost | random | 0.23 (95%: 0.13–0.35) |

## Limitations
- Link removal has no tests against random orders yet, only the 95% range of the 500 random orders. Counting ties does not change which L50 values the panel figure `link_removal_results` bolds.
- Diets are fixed, so a predator cannot shift effort to its remaining prey. Adaptive foraging (Kondoh 2003) is the dynamic alternative.
- Strongest and weakest are measured as the share of the predator's diet, which is not the amount of biomass flowing through the link.
- Recalculated edge betweenness is computed on the surviving web after each cut; all other orders are ranked once on the intact web.
