# Centrality and trophic level

Methods: [`code/README.md`](../code/README.md). Figures: [`figures/04_centrality/`](../figures/04_centrality/README.md).

## Correlation with trophic level

We report the 40-consumer column. Detritus, Discard and Phytoplankton have no prey and sit at trophic level 1 by definition, so in the all-43 column they are tied at the bottom of both rankings. They raise ρ for number of prey from +0.75 to +0.80 and move total degree from −0.07 to +0.10 without adding information. So, the all-43 column is kept only as a sensitivity check.

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

- Rises with trophic level (p < 0.05, consumers): number of prey (in-degree), clustering coefficient, clustering (directed).
- Falls with trophic level (p < 0.05, consumers): number of predators (out-degree), importance as prey (out-strength), PageRank importance.
- No significant relation: total degree, betweenness, betweenness (weighted), clustering (weighted).

## Highest-scoring groups
- **number of prey (in-degree)**: Sharks (25); Demersal piscivores (23); Adult hake (21); Demersal fishes (20)
- **number of predators (out-degree)**: Shrimps (27); Benthic cephalopods (24); Macrozooplankton (24); Suprabenthos (24)
- **total degree**: Benthic cephalopods (39); Shrimps (36); Crabs (34); Benthopelagic cephalopods (29)
- **importance as prey (out-strength)**: Detritus (5.13); Meso and microzooplankton (4.24); Macrozooplankton (3.89); Suprabenthos (3.31)
- **betweenness**: Benthic cephalopods (0.179); Benthopelagic cephalopods (0.178); Demersal fishes (0.0481); Commercial sparids 2 (0.044)
- **betweenness (weighted)**: Benthopelagic cephalopods (0.209); Benthic cephalopods (0.181); Commercial sparids 2 (0.0616); Demersal fishes (0.0604)
- **clustering coefficient**: Large benthopelagic fishes (0.939); Blue whiting (0.872); Anglerfishes (0.861); Skates (0.802)
- **clustering (weighted)**: Detritus (0.134); Killer whales (0.0784); Mantis shrimp (0.0483); Phytoplankton (0.0466)
- **clustering (directed)**: Large benthopelagic fishes (0.545); Blue whiting (0.5); Anglerfishes (0.486); Juvenile hake (0.444)
- **PageRank importance**: Phytoplankton (0.165); Detritus (0.107); Meso and microzooplankton (0.0837); Suprabenthos (0.0404)

## Limitations
- Trophic level and number of prey are not independent: a group that eats many different prey usually sits higher in the web.
- Betweenness depends on link direction. With edges pointing prey → predator, it counts how often a group lies on the shortest energy pathways.
