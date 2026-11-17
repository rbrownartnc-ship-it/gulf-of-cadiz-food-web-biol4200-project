# Code

To run all scripts in order, with the checks at the end (about 2 minutes):

```bash
python code/run_all.py               # add --no-checks to skip code/checks/
```

To run one script at a time, from the repository root:

```bash
python code/build_network.py         # data/ -> cleaned web, traits, web figures     (~5 s)
python code/distributions.py         # histograms of node and link properties       (~5 s)
python code/network_structure.py     # structure, null models, centralities         (~30 s)
python code/node_removal.py          # removing groups: knockouts, sequences, R50    (~40 s)
python code/link_removal.py          # cutting links: knockouts, sequences, L50      (~15 s)
python code/compare_webs.py          # the same measurements on two other webs     (~30 s)
python code/compare_webs_stats.py    # intervals and tests on that comparison       (~20 s)
python code/node_removal_panels.py   # panel figure and R50 table for the results draft
python code/link_removal_panels.py   # panel figure and L50 table for the results draft
python code/explainer.py             # the methods explainer figure
python code/connectivity_panels.py   # trophic level against connectivity, four panels
python code/checks/verify_cascade.py      # independent check of the extinction rule
python code/checks/verify_with_igraph.py  # structure numbers redone in igraph
```

Run `build_network.py` first. All other scripts read the cleaned web that it writes to `output/`. The order of the other analysis scripts is not important, with two exceptions. `compare_webs.py` checks its results against the Gulf of Cadiz outputs, and `compare_webs_stats.py` checks its results against `compare_webs.py`. Thus, run these two scripts after the other analyses, in this order. The four figure scripts read only `output/`, so run them last.

| Script | Writes (in `output/` unless noted) | Figures |
|---|---|---|
| `build_network.py` | cleaned web, cleaning log, node traits, edge list, GraphML | `figures/01_web/` |
| `distributions.py` | `cadiz_distribution_stats.csv` | `figures/02_distributions/` |
| `network_structure.py` | `cadiz_global_structure.csv`, `cadiz_structure_vs_null.csv`, `cadiz_centrality.csv`, `cadiz_centrality_vs_tl.csv` | `figures/03_structure/`, `figures/04_centrality/` |
| `node_removal.py` | `cadiz_node_knockouts.csv`, `cadiz_guild_removal.csv`, `cadiz_node_robustness_summary.csv`, `cadiz_node_robustness_curves.csv`, `cadiz_node_fragmentation.csv` | `figures/05_node_removal/` |
| `link_removal.py` | `cadiz_link_knockouts.csv`, `cadiz_link_robustness_summary.csv`, `cadiz_link_robustness_curves.csv`, `cadiz_link_fragmentation.csv` | `figures/06_link_removal/` |
| `compare_webs.py` | `compare_webs_*.csv` | `figures/08_comparison/` |
| `compare_webs_stats.py` | `compare_webs_stats_*.csv`, `compare_webs_stats_baseline_table.tex` | `figures/08_comparison/` |
| `node_removal_panels.py` | `cadiz_r50_table.tex` | `figures/05_node_removal/node_removal_results` |
| `link_removal_panels.py` | `cadiz_l50_table.tex` | `figures/06_link_removal/link_removal_results` |
| `explainer.py` | | `figures/07_explainer/` |
| `connectivity_panels.py` | | `figures/09_connectivity_and_diet_diversity/` |
| `checks/verify_cascade.py` | nothing (stops with an error if a result is different) | |
| `checks/verify_with_igraph.py` | nothing (stops with an error if a result is different) | |
| `foodweb.py` | shared functions: web loading, extinction cascade, null models, PageRank importance, figure style, food web drawing | |
| `run_all.py` | runs all scripts above in order | |

Each script finds the repository from its own location. Thus, you can run a script from any folder. Each random step uses a fixed seed (4200, and 4 for the food web layout). Thus, a new run gives identical files.

Each figure has the size that it will have in print. The food webs, the explainer and the panel figures are 7 in wide (full page width). All other figures are 3.4 in wide (one column). No text in a figure is smaller than 6.5 pt. Each figure is saved as a PDF for LaTeX and as a 300-dpi PNG.

## `build_network.py`

1. Reads the labeled 44 × 44 diet matrix and checks that the row labels and column labels agree. Checks that each consumer's column sums to 1. This check confirms that rows are prey and columns are predators.
2. Removes `Import`. `Import` is food eaten outside the model area, not a group. The script records each cleaning step in `output/cadiz_cleaning_log.csv`.
3. Builds a `networkx.DiGraph`. Edges point from prey to predator, which is the direction of energy flow. The weight of an edge is the share of the predator's diet. For the "who eats whom" direction, use `G.reverse()`.
4. Calculates the node traits with the equations below. [`output/README.md`](../output/README.md) defines each column.
5. Saves the CSV tables and the GraphML file.
6. Draws the diet matrix heatmap and the food web by trophic level.

### Equations

`D[j, i]` is the share of predator *i*'s diet that comes from prey *j*. The diet of each consumer is rescaled to sum to 1.

Trophic level uses the Ecopath convention: basal groups have trophic level 1. The script solves the equation exactly as a linear system. Cannibalism is included.

$$
TL_i = 1 + \sum_j D_{ji} TL_j
\quad\Longleftrightarrow\quad
(\mathbf{I} - \mathbf{D}^\top) \mathbf{TL} = \mathbf{1}
$$

The omnivory index (Christensen & Pauly 1992) shows how much the prey of a consumer differ in trophic level. The index is 0 when all prey have the same trophic level.

$$
OI_i = \sum_j D_{ji} \left( TL_j - (TL_i - 1) \right)^2
$$

Diet diversity is the effective number of prey: the number of equally eaten prey that gives the same diversity. `p_j` is the diet without cannibalism, rescaled to sum to 1.

$$
\mathrm{effective\ prey}_i = \exp\left( -\sum_j p_j \ln p_j \right)
$$

Number of prey (in-degree, or generality) and number of predators (out-degree, or vulnerability) do not count self-loops.

Importance as prey is the weighted out-degree. It uses the original diet shares, not the rescaled shares.

$$
s_j = \sum_i D^{\mathrm{orig}}_{ji}
$$

## `network_structure.py`

`network_structure.py` measures the structure of the whole web, compares it with null models and calculates the centralities of each group.

`cadiz_global_structure.csv` contains the whole-web measures. Each measure treats a link as present or absent (binary), unless its name says weighted or directed. Paths and clustering do not include cannibalistic self-loops.

| Measure | Definition |
|---|---|
| connectance | L / S² (directed, self-loops included) |
| largest weakly connected component | the largest connected part of the web, with link direction ignored |
| largest strongly connected component | the largest feeding loop, where each member can reach each other member along feeding links |
| characteristic path length | mean shortest path between pairs of groups, with direction ignored (Williams et al. 2002) |
| clustering, binary | mean local clustering coefficient, with direction ignored |
| clustering, weighted | Onnela et al. (2005), with link weight = diet share summed over both directions |
| clustering, directed | Fagiolo (2007), with all directed triangle types |
| trophic coherence q | SD across links of (predator TL − prey TL) (Johnson et al. 2014). q = 0 means a perfectly layered web. A lower q goes with a more stable web. |
| omnivore | a consumer with prey at different shortest-chain trophic levels |

A null model is a set of artificial webs. These webs keep some properties of the real web and make the other properties random. If the real web is different from the null webs for a measure, the kept properties do not explain that measure. `cadiz_structure_vs_null.csv` gives the real value, the null mean and SD, a z-score, and the fraction of null webs below the real value. The table does not include a measure that a null model keeps fixed.

| Null model | Keeps | Webs |
|---|---|---|
| random (ER) | number of groups and links | 1000 |
| degree-preserving | number of prey and predators of each group (`networkx.directed_edge_swap`, 5 × L swaps) | 300 |
| niche model (Williams & Martinez 2000) | groups and connectance (accepted within ±3%, connected, each group reachable from a basal group) | 1000 |

Random webs and degree-preserving webs cannot have cannibalism. Thus, the script compares them with the real web without its 14 self-loops. The script skips the measures that need trophic levels for a null model if most of its webs have no basal group.

`cadiz_centrality.csv` has one row for each group, with these centralities:
- number of prey, number of predators, total degree, and out-strength (importance as prey)
- betweenness, binary and weighted. The weighted version uses −ln(diet share) as the distance, so a strong link is a short step.
- local clustering (binary, weighted and directed)
- PageRank importance (Allesina & Pascual 2009). This measure runs PageRank on links from consumer to resource. A root node points to each group, and each basal group points to the root. A group has a high score when important groups depend on it (damping factor 0.99).

`cadiz_centrality_vs_tl.csv` gives the Spearman correlation of each centrality with trophic level, for the 40 consumers and for all 43 groups.

## `node_removal.py`

`node_removal.py` removes groups from the web and counts the secondary extinctions, which are the consumers that starve after a removal. A consumer starves when it loses θ or more of its rescaled diet (`foodweb.Cascade`). Cannibalism never keeps a group alive. The cascade continues until no more groups starve.
- θ = 1 is "all prey lost", the topological rule of Dunne, Williams & Martinez (2002).
- θ = 0.5 is "half of diet lost", the weighted rule.
- θ = 0.25 and 0.75 are a sensitivity check (R50 only).

Phytoplankton, Detritus and Discard have no prey, so they never starve. The rule works only bottom-up: the removal of a predator never causes an extinction. Top-down effects, such as predator release, need a dynamic model.

| Analysis | Output |
|---|---|
| Single knockouts: the script removes each of the 43 groups alone. | `cadiz_node_knockouts.csv` |
| Guild removals: the script removes a full trophic band or taxonomic group at one time. | `cadiz_guild_removal.csv` |
| Removal sequences: the script removes living groups one at a time, in a random order (1000 times) or in a ranked order from the intact web. The rankings are most and least connected, highest and lowest trophic level, most important prey (out-strength), PageRank importance and betweenness. The recalculated versions of the degree and betweenness rankings rank the remaining groups again after each removal (Holme et al. 2002). The script skips groups that a secondary extinction already removed. | `cadiz_node_robustness_curves.csv` |
| R50: the fraction of the 41 living groups that the script must remove before half of them are lost, with removals and secondary extinctions counted (Dunne et al. 2002). The maximum R50 is 21/41 = 0.51, which means no secondary extinctions. A lower R50 means a more fragile web. | `cadiz_node_robustness_summary.csv` |
| Giant component: the size of the largest connected part of the web during the same removals, with and without secondary extinctions (Albert et al. 2000). The table also gives the point where the surviving web first splits. | `cadiz_node_robustness_curves.csv`, `cadiz_node_fragmentation.csv` |

## `link_removal.py`

`link_removal.py` cuts feeding links instead of removing groups. After a cut, the predator does not eat that prey, but both groups stay alive. Then the same extinction rule applies (`foodweb.LinkRemoval`, a faster version of `foodweb.Cascade` for long sequences of cuts). The script never cuts cannibalistic self-loops.

| Analysis | Output |
|---|---|
| Single-link knockouts: the script cuts each of the 397 feeding links alone. The table also gives the edge betweenness of each link (the share of shortest feeding paths that use the link) and shows if the link is a bridge (a link whose loss splits the web). | `cadiz_link_knockouts.csv` |
| Link-removal sequences: random (500 times), strongest first, weakest first (the weak-link idea of McCann et al. 1998), highest edge betweenness first (static and recalculated; Girvan & Newman 2002, Holme et al. 2002), links from the lowest trophic level prey first, and links into the highest trophic level predators first. The script skips links that are already gone because a group starved. | `cadiz_link_robustness_curves.csv` |
| L50: the fraction of the 397 links that the script must cut before half of the 41 living groups are lost, at θ = 1, 0.75, 0.5 and 0.25. A lower L50 means a more fragile web. | `cadiz_link_robustness_summary.csv` |
| Giant component during link cuts, with and without starvation (bond percolation), and the point where the surviving web first splits | `cadiz_link_robustness_curves.csv`, `cadiz_link_fragmentation.csv` |

## `distributions.py`

`distributions.py` makes one histogram for each property: number of prey, number of predators, total degree, importance as prey, trophic level, clustering, betweenness, omnivory index, diet diversity and link strength (397 links). The three degree histograms also show the expected histogram for a random (ER) web with the same groups and links. The degrees of this random web follow a binomial distribution, B(S − 1, p), with p = L / (S(S − 1)). The script also plots the cumulative degree distribution against an exponential (Camacho et al. 2002). `cadiz_distribution_stats.csv` contains the summary statistics. These include variance/mean, with the random-web value of 1 − p for comparison.

## `compare_webs.py`

`compare_webs.py` applies the same measurements to the Angolan shelf (`FW_003`) and the Mondego estuary (`FW_016_01`) and compares them with the Gulf of Cadiz (`FW_005`). All three webs are Ecopath diet matrices from Web of Life. Thus, the methods apply without changes. [`data/`](../data/README.md) contains the raw data, with one folder for each web.

The script cleans each web with the same steps as `build_network.py`. It removes the Ecopath boundary row (`Import` or `Imports`) after a check that this row eats nothing. It keeps detritus, cannibalism and weak links, and it rescales each diet to sum to 1. The measurements are trophic level, the whole-web measures in `foodweb.food_web_properties`, degree centralization, ten centralities against trophic level, single-group removals, trophic-band removals, R50 for seven removal orders and L50 for three link orders. Each removal analysis uses both extinction rules.

As a control, the script builds the Gulf of Cadiz again from the Web of Life edge list, not from our cleaned files. The script stops if this web does not agree with the Gulf of Cadiz outputs. The script also draws the Angolan shelf and Mondego estuary food webs by trophic level, with the same function as the Gulf of Cadiz web in `figures/01_web/`. It writes `output/compare_webs_*.csv` and 13 figures in `figures/08_comparison/`. It does not change the files in `output/cadiz_*`.

## `compare_webs_stats.py`

`compare_webs_stats.py` adds an interval or a test to each result from `compare_webs.py`, for the same three webs.

- Baseline table: nodes, links, connectance, degrees, trophic levels, clustering, path length and Freeman centralization (degree, in-degree, out-degree and betweenness). Centralization shows how much the most central group stands out from the others (0 = all groups equal, 1 = a star). The script compares each centralization with 1000 random directed graphs of the same size.
- Trophic level against five measures (number of prey, effective number of prey, number of predators, total degree and betweenness) for the consumers of each web. Each Spearman ρ has a bootstrap 95% interval (10,000 resamples) and a permutation p-value. Spearman ρ shows only how well two rankings agree. Thus, each plot also has a least-squares line with a 95% band, which shows the relationship.
- Groups of nodes: a Kruskal–Wallis test across the trophic bands, and across the taxonomic categories for the Gulf of Cadiz. Pairwise Mann–Whitney tests with the Holm correction follow.
- Node removal: the script runs the random order 1000 times. A targeted order is a fixed ranking, so it changes only where groups have the same ranking score. The script runs each targeted order 200 times with ties broken at random (1 time if no groups tie). Then it compares each targeted order with the 1000 random orders (two-sided Monte Carlo p-value). The comparison uses R50 and the area under the share-lost curve. R50 changes in steps of 1/41, so many random orders have the same R50 as a targeted order. The area under the curve does not have this problem. Thus, the area is the better test.
- Self-check: the script stops if its correlations, degree centralization and R50 values are different from those of `compare_webs.py`.

`compare_webs_stats.py` writes `output/compare_webs_stats_*.csv`, the baseline table for LaTeX and 38 figures in `figures/08_comparison/`, which include the baseline table as a figure. The tests cover only node removal at this time, not link removal.

## Checks (`code/checks/`)

`verify_cascade.py` calculates the extinction rule again as matrix algebra. It shares no code with `foodweb.py`. At θ = 1, 0.75, 0.5 and 0.25, it compares:
- each single-group removal and 300 random multi-group removals
- each single-link cut and 300 random sets of cut links
- the fast link-cut code against the full cascade, along 50 random sequences of cuts

All 7,160 comparisons agree. Then the script runs a broken copy of itself, with a strict threshold instead of a non-strict threshold. The broken copy fails, which shows that the check can find an error.

`verify_with_igraph.py` calculates clustering, transitivity, path length, diameter, the largest strongly connected component, assortativity, mutual predation pairs, and node and edge betweenness again in igraph, a different network library. All values agree to rounding. Two runs of the full pipeline also give identical tables and figures.

## References for the methods

- Albert, R., Jeong, H. & Barabási, A.-L. (2000). Error and attack tolerance of complex networks. *Nature* 406, 378–382. https://doi.org/10.1038/35019019
- Allesina, S. & Pascual, M. (2009). Googling food webs: can an eigenvector measure species' importance for coextinctions? *PLoS Computational Biology* 5, e1000494. https://doi.org/10.1371/journal.pcbi.1000494
- Camacho, J., Guimerà, R. & Amaral, L. A. N. (2002). Robust patterns in food web structure. *Physical Review Letters* 88, 228102. https://doi.org/10.1103/PhysRevLett.88.228102
- Christensen, V. & Pauly, D. (1992). ECOPATH II: a software for balancing steady-state ecosystem models and calculating network characteristics. *Ecological Modelling* 61, 169–185. https://doi.org/10.1016/0304-3800(92)90016-8
- Dunne, J. A., Williams, R. J. & Martinez, N. D. (2002). Network structure and biodiversity loss in food webs: robustness increases with connectance. *Ecology Letters* 5, 558–567. https://doi.org/10.1046/j.1461-0248.2002.00354.x
- Fagiolo, G. (2007). Clustering in complex directed networks. *Physical Review E* 76, 026107. https://doi.org/10.1103/PhysRevE.76.026107
- Girvan, M. & Newman, M. E. J. (2002). Community structure in social and biological networks. *PNAS* 99, 7821–7826. https://doi.org/10.1073/pnas.122653799
- Holme, P., Kim, B. J., Yoon, C. N. & Han, S. K. (2002). Attack vulnerability of complex networks. *Physical Review E* 65, 056109. https://doi.org/10.1103/PhysRevE.65.056109
- Johnson, S., Domínguez-García, V., Donetti, L. & Muñoz, M. A. (2014). Trophic coherence determines food-web stability. *PNAS* 111, 17923–17928. https://doi.org/10.1073/pnas.1409077111
- McCann, K., Hastings, A. & Huxel, G. R. (1998). Weak trophic interactions and the balance of nature. *Nature* 395, 794–798. https://doi.org/10.1038/27427
- Onnela, J.-P., Saramäki, J., Kertész, J. & Kaski, K. (2005). Intensity and coherence of motifs in weighted complex networks. *Physical Review E* 71, 065103. https://doi.org/10.1103/PhysRevE.71.065103
- Williams, R. J. & Martinez, N. D. (2000). Simple rules yield complex food webs. *Nature* 404, 180–183. https://doi.org/10.1038/35004572
- Williams, R. J., Berlow, E. L., Dunne, J. A., Barabási, A.-L. & Martinez, N. D. (2002). Two degrees of separation in complex food webs. *PNAS* 99, 12913–12916. https://doi.org/10.1073/pnas.192448799
