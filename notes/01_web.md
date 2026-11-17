# The web: data, cleaning and trophic levels

Raw data: [`data/cadiz_FW_005/diet_matrix.csv`](../data/README.md). Methods: [`code/README.md`](../code/README.md). Figures: [`figures/01_web/`](../figures/01_web/README.md).

## Cleaning steps

[`cadiz_cleaning_log.csv`](../output/cadiz_cleaning_log.csv) records each step.

- All 40 consumer columns sum to 1 (largest difference 0.0020). This confirms that rows are prey and columns are predators. This step changes no links (413 links).
- The code removes the `Import` row and column (413 → 411 links). `Import` is not a functional group. It is Ecopath's share of a predator's diet eaten outside the model area. It occurs only as prey of Loggerhead turtles (0.448) and Seabirds (0.404), and its column is all zero.
- The matrix has no other boundary flow (export, emigration, fishery or other). Torres et al. (2013) give fishery catches and exports in separate tables.
- Without `Import`, the Loggerhead turtle diet sums to 0.552 and the Seabird diet sums to 0.596. Thus, the code rescales each diet to sum to 1 for trophic level, omnivory index and diet diversity (the `diet_share_renorm` column in the edge list). This step assumes that food eaten outside the area has the same composition as the local diet. The culled matrix keeps the original shares.
- Detritus and Discard stay as nodes, although they are not living. Detritus is the most eaten group in the web (summed diet share 5.13). Without these two groups, the web is still one connected part, with 41 nodes and 396 links.
- The 14 cannibalistic self-loops stay in the matrix and the graph. The prey counts, predator counts and diet diversity do not include them.
- The code keeps all weak links. The smallest diet share is 1e-06. 120 links are below 0.01, and 22 of these are below 0.001.

## The cleaned network

The cleaned web has 43 groups (41 living) and 411 links. Of these links, 14 are cannibalistic self-loops. Edges point from prey to predator, which is the direction of energy flow. The weight of each edge is the share of the predator's diet.

- Basal groups (no prey): Detritus, Discard and Phytoplankton.
- Top predators (no predators): Anglerfishes, Dolphins, Killer whales, Loggerhead turtles, Seabirds and Skates.
- The full web is one weakly connected component. Its largest strongly connected component (feeding loop) has 23 groups.

## Trophic levels

The code calculates trophic level with the Ecopath method: 1 plus the diet-weighted mean trophic level of the prey, with basal groups at 1 ([`cadiz_node_traits.csv`](../output/cadiz_node_traits.csv)). Trophic levels go from 1.00 to 4.84, with a mean of 3.14. The highest groups are Anglerfishes (4.84), Killer whales (4.54), Dolphins (4.49), Demersal piscivores (4.29) and Adult hake (4.12).

| Category | Groups | Mean TL | Range |
|---|---|---|---|
| fishes | 20 | 3.58 | 2.95–4.84 |
| invertebrates & plankton | 17 | 2.71 | 1.00–3.92 |
| marine mammals, birds, turtles | 4 | 3.83 | 3.09–4.54 |
| non-living | 2 | 1.00 | 1.00–1.00 |

## Limits

- The trophic levels of Loggerhead turtles and Seabirds depend on the rescaled diets. The rescaling assumes that the food these groups eat outside the area has the same composition as their local diet.
- The code normalizes diet shares for each predator. Thus, the in-strength of each predator is about 1. For example, a 0.5 share of the killer whale diet and a 0.5 share of a zooplankton diet are not the same amount of biomass.
- The model is one snapshot (2009) and uses functional groups, not species. Thus, the results say little about individual species.
