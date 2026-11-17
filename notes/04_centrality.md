# Centrality and trophic level

The methods are in [`code/README.md`](../code/README.md), and the figures are in [`figures/04_centrality/`](../figures/04_centrality/README.md).

## Correlation with trophic level

We report the 40-consumer column. Detritus, Discard and Phytoplankton have no prey and are at trophic level 1 by definition, so in the all-43 column they are tied at the bottom of both rankings. They push ρ for number of prey from +0.75 up to +0.80 and move total degree from −0.07 to +0.10 without adding any information, so we only keep the all-43 column as a sensitivity check.

| measure | ρ (40 consumers) | p | ρ (all 43) | p |
|---|---|---|---|---|
| number of prey (in-degree) | 0.75 | 2.9e-08 | 0.80 | 1.6e-10 |
| number of predators (out-degree) | −0.65 | 4.7e-06 | −0.60 | 2.1e-05 |
| total degree | −0.07 | 0.67 | 0.10 | 0.52 |
| importance as prey (out-strength) | −0.67 | 2.8e-06 | −0.69 | 3.3e-07 |
| betweenness | 0.00 | 1 | 0.15 | 0.32 |
| betweenness (weighted) | −0.18 | 0.26 | −0.01 | 0.95 |
| clustering coefficient | 0.42 | 0.0069 | 0.44 | 0.0035 |
| clustering (weighted) | −0.16 | 0.33 | −0.22 | 0.15 |
| clustering (directed) | 0.47 | 0.0021 | 0.49 | 0.00078 |
| PageRank importance | −0.68 | 1.5e-06 | −0.71 | 8.6e-08 |

Number of prey, the clustering coefficient and directed clustering go up with trophic level (p < 0.05 for the consumers), while number of predators, importance as prey and PageRank importance go down. Total degree, betweenness, weighted betweenness and weighted clustering show no significant relationship.

## Highest-scoring groups

The top four groups for each centrality:

| Centrality | Top four groups |
|---|---|
| number of prey (in-degree) | Sharks (25), Demersal piscivores (23), Adult hake (21), Demersal fishes (20) |
| number of predators (out-degree) | Shrimps (27), Benthic cephalopods (24), Macrozooplankton (24), Suprabenthos (24) |
| total degree | Benthic cephalopods (39), Shrimps (36), Crabs (34), Benthopelagic cephalopods (29) |
| importance as prey (out-strength) | Detritus (5.13), Meso and microzooplankton (4.24), Macrozooplankton (3.89), Suprabenthos (3.31) |
| betweenness | Benthic cephalopods (0.179), Benthopelagic cephalopods (0.178), Demersal fishes (0.0481), Commercial sparids 2 (0.044) |
| betweenness (weighted) | Benthopelagic cephalopods (0.209), Benthic cephalopods (0.181), Commercial sparids 2 (0.0616), Demersal fishes (0.0604) |
| clustering coefficient | Large benthopelagic fishes (0.939), Blue whiting (0.872), Anglerfishes (0.861), Skates (0.802) |
| clustering (weighted) | Detritus (0.134), Killer whales (0.0784), Mantis shrimp (0.0483), Phytoplankton (0.0466) |
| clustering (directed) | Large benthopelagic fishes (0.545), Blue whiting (0.5), Anglerfishes (0.486), Juvenile hake (0.444) |
| PageRank importance | Phytoplankton (0.165), Detritus (0.107), Meso and microzooplankton (0.0837), Suprabenthos (0.0404) |

## Intervals on the correlations

The bootstrap 95% intervals for the 40 consumers ([`compare_webs_stats_correlations.csv`](../output/compare_webs_stats_correlations.csv)) are +0.75 [+0.53, +0.88] for number of prey, +0.69 [+0.46, +0.83] for effective number of prey and −0.65 [−0.83, −0.39] for number of predators. Total degree (−0.07 [−0.38, +0.25]) and betweenness (+0.00 [−0.34, +0.35]) both have intervals that include 0, so neither one shows a relationship with trophic level that we can detect.

The four-panel figure in the results draft is [`09_connectivity_and_diet_diversity/tl_vs_connectivity`](../figures/09_connectivity_and_diet_diversity/README.md), and each relationship with its fitted line is in `figures/08_comparison/compare_cadiz_tl_vs_*`.

## Limitations
- Trophic level and number of prey are not independent, as a group that eats lots of different prey usually ends up higher in the web.
- Betweenness depends on link direction. With edges pointing prey → predator, it counts how often a group is on the shortest paths energy takes through the web.
