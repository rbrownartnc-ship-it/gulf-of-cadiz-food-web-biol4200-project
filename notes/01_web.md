# The web: data, cleaning and trophic levels

The raw data is [`data/cadiz_FW_005/diet_matrix.csv`](../data/README.md), the methods are described in [`code/README.md`](../code/README.md), and the figures are in [`figures/01_web/`](../figures/01_web/README.md).

## Cleaning steps

Every step below is recorded in [`cadiz_cleaning_log.csv`](../output/cadiz_cleaning_log.csv).

- All 40 consumer columns sum to 1 (largest deviation 0.0020), which confirms that rows are prey and columns are predators. No links were changed (413 links).
- The `Import` row and column were removed (413 → 411 links). `Import` is not a functional group but Ecopath's share of a predator's diet eaten outside the model area. It only appears as prey of Loggerhead turtles (0.448) and Seabirds (0.404), and its column is all zero.
- No other boundary flow (export, emigration, fishery, etc.) was found in the matrix. Fishery catches and exports are reported in the tables of Torres et al. (2013) instead of the diet matrix.
- Without `Import`, the Loggerhead turtle and Seabird diets only sum to 0.552 and 0.596, respectively. Therefore, every diet was rescaled to sum to 1 for trophic level, omnivory index and diet diversity (the `diet_share_renorm` column in the edge list). This rescaling assumes that food eaten outside the area has the same make-up as the local diet. The culled matrix keeps the original shares.
- Detritus and Discard were kept as nodes even though they are not living. Detritus is the most eaten group in the web (summed diet share of 5.13), and without both groups the web would still be one connected piece of 41 nodes and 396 links.
- The 14 cannibalistic self-loops were kept in the matrix and the graph, but they are left out of the prey and predator counts and out of diet diversity.
- No weak links were removed. The smallest diet share is 1e-06, and 120 links are below 0.01 (22 of them below 0.001).

## The cleaned network

The cleaned web has 43 groups (41 living) and 411 links, 14 of which are cannibalistic self-loops. Edges point prey → predator (the direction energy flows), and each edge weight is the share of the predator's diet. The basal groups, which have no prey, are Detritus, Discard and Phytoplankton. The top predators, which have no predators, are Anglerfishes, Dolphins, Killer whales, Loggerhead turtles, Seabirds and Skates. The whole web is one weakly connected component, and its largest strongly connected component (feeding loop) contains 23 groups.

## Trophic levels

Trophic level was calculated the Ecopath way, as 1 plus the diet-weighted mean trophic level of a group's prey, with basal groups set to 1 ([`cadiz_node_traits.csv`](../output/cadiz_node_traits.csv)). Trophic levels range from 1.00 to 4.84, with a mean of 3.14. The highest groups are Anglerfishes (4.84), Killer whales (4.54), Dolphins (4.49), Demersal piscivores (4.29) and Adult hake (4.12).

| Category | Groups | Mean TL | Range |
|---|---|---|---|
| fishes | 20 | 3.58 | 2.95–4.84 |
| invertebrates & plankton | 17 | 2.71 | 1.00–3.92 |
| marine mammals, birds, turtles | 4 | 3.83 | 3.09–4.54 |
| non-living | 2 | 1.00 | 1.00–1.00 |

## Limitations

- The trophic levels of Loggerhead turtles and Seabirds depend on rescaling their diets after `Import` was removed, which assumes that the food they eat outside the area has the same make-up as their local diet.
- Diet shares are normalized for each predator, so every predator's in-strength is about 1. As a result, a 0.5 share of a killer whale's diet and a 0.5 share of a zooplankton group's diet are not the same amount of biomass.
- The model is a single snapshot (2009) built from functional groups instead of species, which limits what can be concluded about individual species.
