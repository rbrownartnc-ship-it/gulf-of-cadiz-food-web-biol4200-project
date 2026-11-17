# The web: data, cleaning and trophic levels

The data is [`data/cadiz_FW_005/diet_matrix.csv`](../data/README.md), the methods are in [`code/README.md`](../code/README.md), and the figures are in [`figures/01_web/`](../figures/01_web/README.md).

## Cleaning steps

The full record is in [`cadiz_cleaning_log.csv`](../output/cadiz_cleaning_log.csv).

- We first checked the consumer columns. All 40 consumer diets sum to 1 (the largest deviation is 0.0020), which tells us the rows are prey and the columns are predators. Nothing changed here (413 links).
- We removed the `Import` row and column (413 → 411 links). `Import` is not a functional group, as it is Ecopath's share of a predator's diet eaten outside the model area. It only shows up as prey of Loggerhead turtles (0.448) and Seabirds (0.404), and its column is all zero.
- We checked for any other row or column that is not a living or detrital group (export, emigration, fishery, etc.), and there are none. Import was the only boundary flow in the matrix, as fishery catches and exports are in the tables of Torres et al. (2013) and not in the diet matrix.
- Without Import, the Loggerhead turtle and Seabird diets only sum to 0.552 and 0.596, respectively. So, for trophic level, omnivory index and diet diversity, every diet is rescaled to sum to 1 (the `diet_share_renorm` column in the edge list). This assumes the food eaten outside the area is the same mix as the local diet. The culled matrix keeps the original shares.
- We kept Detritus and Discard as nodes, even though they are not living. Detritus is the most eaten group in the web (summed diet share of 5.13), and without both of them the web still has 41 nodes and 396 links in one connected piece.
- We kept the 14 cannibalistic self-loops in the matrix and the graph, but they are left out when counting prey and predators and from diet diversity.
- We kept every weak link, with no threshold. The smallest share is 1e-06, and 120 links are below 0.01 (22 are below 0.001).

## The cleaned network

The cleaned web has 43 groups (41 living) and 411 links, and 14 of those links are cannibalistic self-loops. Edges point prey → predator (the direction energy flows), and each weight is the share of the predator's diet. The basal groups (no prey) are Detritus, Discard and Phytoplankton, and the top predators (no predators) are Anglerfishes, Dolphins, Killer whales, Loggerhead turtles, Seabirds and Skates. The whole web is one weakly connected component, and the largest strongly connected component (feeding loop) has 23 groups.

## Trophic levels

Trophic level is calculated the Ecopath way, as 1 plus the diet-weighted mean trophic level of the prey, with basal groups set to 1 ([`cadiz_node_traits.csv`](../output/cadiz_node_traits.csv)). It ranges from 1.00 to 4.84, with a mean of 3.14. The highest groups are Anglerfishes (4.84), Killer whales (4.54), Dolphins (4.49), Demersal piscivores (4.29) and Adult hake (4.12).

| Category | Groups | Mean TL | Range |
|---|---|---|---|
| fishes | 20 | 3.58 | 2.95–4.84 |
| invertebrates & plankton | 17 | 2.71 | 1.00–3.92 |
| marine mammals, birds, turtles | 4 | 3.83 | 3.09–4.54 |
| non-living | 2 | 1.00 | 1.00–1.00 |

## Limitations

- The trophic levels of Loggerhead turtles and Seabirds depend on rescaling their diets after removing `Import`, which assumes the food they eat outside the area is the same mix as the local diet.
- Diet shares are normalized for each predator, so a predator's in-strength is about 1 no matter what. A 0.5 share of a killer whale's diet and a 0.5 share of zooplankton's diet are not the same amount of biomass, for example.
- The model is one snapshot (2009) and uses functional groups instead of species, so we cannot say much about individual species.
