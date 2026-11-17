# Code

To run every script in order, with the checks at the end (about 2 minutes):

```bash
python code/run_all.py               # add --no-checks to skip code/checks/
```

Or one script at a time, from the repository root:

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

`build_network.py` has to run first, as every other script reads the cleaned web it writes to `output/`. The order of the other analysis scripts does not matter, with two exceptions. `compare_webs.py` checks itself against the Gulf of Cadiz outputs, and `compare_webs_stats.py` checks itself against `compare_webs.py`, so those two run after the other analyses and in that order. The four figure scripts only read `output/`, so they run last.

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
| `checks/verify_cascade.py` | nothing (stops with an error if any result disagrees) | |
| `checks/verify_with_igraph.py` | nothing (stops with an error if any result disagrees) | |
| `foodweb.py` | shared functions: loading the web, the extinction cascade, null models, PageRank importance, figure style and the food web drawing | |
| `run_all.py` | runs every script above in order | |

Each script finds the repository from its own location, so it can be run from any folder. Every random step uses a fixed seed (4200, and 4 for the food web layout), so rerunning a script gives identical files.

Every figure is drawn at the size it prints: 7 in wide (the full page width) for the food webs, the explainer and the panel figures, and 3.4 in wide (one column) for the rest. No text in a figure is smaller than 6.5 pt. Each figure is saved as a PDF for LaTeX and as a 300-dpi PNG.

## What `build_network.py` does

1. Reads the labeled 44 × 44 diet matrix and checks that the row and column labels match. It also checks that every consumer's column sums to 1, which confirms that rows are prey and columns are predators.
2. Removes `Import`, which is food eaten outside the model area and not a group. Every cleaning step is recorded in `output/cadiz_cleaning_log.csv`.
3. Builds a `networkx.DiGraph` with edges pointing prey → predator (the direction energy flows) and weights equal to the share of the predator's diet. `G.reverse()` gives the opposite, "who eats whom" direction.
4. Calculates the node traits with the equations below. The column definitions are in [`output/README.md`](../output/README.md).
5. Saves the CSV tables and the GraphML file.
6. Draws the diet matrix heatmap and the food web by trophic level.

### Equations

`D[j, i]` is the share of predator *i*'s diet that comes from prey *j*, rescaled so each consumer's diet sums to 1.

Trophic level follows the Ecopath convention, where basal groups have a trophic level of 1. It is solved exactly as a linear system, with cannibalism included:

$$
TL_i = 1 + \sum_j D_{ji} TL_j
\quad\Longleftrightarrow\quad
(\mathbf{I} - \mathbf{D}^\top) \mathbf{TL} = \mathbf{1}
$$

The omnivory index (Christensen & Pauly 1992) measures how spread out a consumer's prey are across trophic levels. It is 0 when all of the prey are on the same level:

$$
OI_i = \sum_j D_{ji} \left( TL_j - (TL_i - 1) \right)^2
$$

Diet diversity is the effective number of prey, or how many equally eaten prey a diet is equivalent to. `p_j` is the diet without cannibalism, rescaled to sum to 1:

$$
\mathrm{effective\ prey}_i = \exp\left( -\sum_j p_j \ln p_j \right)
$$

Number of prey (in-degree, or generality) and number of predators (out-degree, or vulnerability) do not count self-loops.

Importance as prey is the weighted out-degree, using the original (not rescaled) diet shares:

$$
s_j = \sum_i D^{\mathrm{orig}}_{ji}
$$

## What `network_structure.py` does

`network_structure.py` measures the structure of the whole web, compares it with null models, and calculates centralities for every group.

The whole-web measures are in `cadiz_global_structure.csv`. They treat each link as present or absent (binary) unless the name says weighted or directed, and they leave cannibalistic self-loops out of paths and clustering.

| Measure | Definition |
|---|---|
| connectance | L / S² (directed, self-loops included) |
| largest weakly connected component | the largest connected piece of the web, ignoring link direction |
| largest strongly connected component | the largest feeding loop, where every member can reach every other member along feeding links |
| characteristic path length | mean shortest path between pairs of groups, ignoring direction (Williams et al. 2002) |
| clustering, binary | mean local clustering coefficient, ignoring direction |
| clustering, weighted | Onnela et al. (2005), with link weight = diet share summed over both directions |
| clustering, directed | Fagiolo (2007), counting all directed triangle types |
| trophic coherence q | SD across links of (predator TL − prey TL) (Johnson et al. 2014). q = 0 means perfectly layered, and lower q goes with more stable webs. |
| omnivore | a consumer whose prey are at different shortest-chain trophic levels |

A null model is a set of artificial webs that keep some features of the real web and randomize the rest. If the real web differs from the null webs on a measure, that measure is not explained by the features the null model keeps. `cadiz_structure_vs_null.csv` gives the real value, the null mean and SD, a z-score, and the fraction of null webs below the real value for each measure. A measure is left out for a null model that holds it fixed.

| Null model | Keeps | Webs |
|---|---|---|
| random (ER) | number of groups and links | 1000 |
| degree-preserving | every group's number of prey and predators (`networkx.directed_edge_swap`, 5 × L swaps) | 300 |
| niche model (Williams & Martinez 2000) | groups and connectance (accepted within ±3%, connected, and every group reachable from a basal group) | 1000 |

Random and degree-preserving webs cannot have cannibalism, so they are compared with the real web minus its 14 self-loops. Measures that need trophic levels are skipped for a null model when most of its webs have no basal group.

`cadiz_centrality.csv` has one row per group with these centralities:
- number of prey, number of predators, total degree, and out-strength (importance as prey)
- betweenness, both binary and weighted. The weighted version uses −ln(diet share) as the distance, so a strong link counts as a short step.
- local clustering (binary, weighted and directed)
- PageRank importance (Allesina & Pascual 2009). The measure runs PageRank on links pointing consumer → resource, plus a root node that every basal group points to and that points to every group. A group scores high when important groups depend on it (damping factor 0.99).

`cadiz_centrality_vs_tl.csv` gives the Spearman correlation of each centrality with trophic level, across the 40 consumers and across all 43 groups.

## What `node_removal.py` does

`node_removal.py` removes groups from the web and counts the secondary extinctions, meaning the consumers that starve as a result. A consumer starves once it has lost at least θ of its diet, using the rescaled diet shares (`foodweb.Cascade`). Cannibalism never keeps a group alive, and the cascade repeats until no more groups starve.
- θ = 1 is "all prey lost", the topological rule of Dunne, Williams & Martinez (2002).
- θ = 0.5 is "half of diet lost", the weighted version.
- θ = 0.25 and 0.75 are run as a sensitivity check (R50 only).

Phytoplankton, Detritus and Discard have no prey, so they never starve. The rule only works bottom-up, as removing a predator can never cause an extinction. Top-down effects like predator release would need a dynamic model.

| Analysis | Output |
|---|---|
| Single knockouts: each of the 43 groups is removed by itself | `cadiz_node_knockouts.csv` |
| Guild removals: a whole trophic band or taxonomic group is removed at once | `cadiz_guild_removal.csv` |
| Removal sequences: living groups are removed one at a time, either in a random order (1000 times) or ranked on the intact web. The rankings are most and least connected, highest and lowest trophic level, most important prey (out-strength), PageRank importance and betweenness. The recalculated versions of the degree and betweenness rankings re-rank the remaining groups after every removal (Holme et al. 2002). Groups already lost to a secondary extinction are skipped. | `cadiz_node_robustness_curves.csv` |
| R50: the fraction of the 41 living groups that have to be removed before half of them are lost, counting both removals and secondary extinctions (Dunne et al. 2002). R50 is at most 21/41 = 0.51, which means no secondary extinctions, and a lower R50 means a more fragile web. | `cadiz_node_robustness_summary.csv` |
| Giant component: the size of the largest connected piece of the web during the same removals, with and without secondary extinctions (Albert et al. 2000), and the point where the surviving web first splits | `cadiz_node_robustness_curves.csv`, `cadiz_node_fragmentation.csv` |

## What `link_removal.py` does

`link_removal.py` cuts feeding links instead of removing groups. Cutting a link means the predator no longer eats that prey, while both groups survive the cut itself. The same extinction rule then applies (`foodweb.LinkRemoval`, a faster version of `foodweb.Cascade` for long sequences of cuts). Cannibalistic self-loops are never cut.

| Analysis | Output |
|---|---|
| Single-link knockouts: each of the 397 feeding links is cut by itself. The table also gives each link's edge betweenness (the share of shortest feeding paths that use the link) and whether it is a bridge (a link whose loss splits the web). | `cadiz_link_knockouts.csv` |
| Link-removal sequences: random (500 times), strongest first, weakest first (the weak-link idea of McCann et al. 1998), highest edge betweenness first (static and recalculated; Girvan & Newman 2002, Holme et al. 2002), links from the lowest trophic level prey first, and links into the highest trophic level predators first. Links already gone because one end starved are skipped. | `cadiz_link_robustness_curves.csv` |
| L50: the fraction of the 397 links that have to be cut before half of the 41 living groups are lost, at θ = 1, 0.75, 0.5 and 0.25. A lower L50 means a more fragile web. | `cadiz_link_robustness_summary.csv` |
| Giant component while links are cut, with and without starvation (bond percolation), and the point where the surviving web first splits | `cadiz_link_robustness_curves.csv`, `cadiz_link_fragmentation.csv` |

## What `distributions.py` does

`distributions.py` makes one histogram per property: number of prey, number of predators, total degree, importance as prey, trophic level, clustering, betweenness, omnivory index, diet diversity and link strength (for the 397 links). The three degree histograms also show the expected histogram for a random (ER) web with the same groups and links, whose degrees follow a binomial distribution, B(S − 1, p) with p = L / (S(S − 1)). The script also plots the cumulative degree distribution against an exponential (Camacho et al. 2002). The summary statistics, including variance/mean against the random-web value of 1 − p, are in `cadiz_distribution_stats.csv`.

## What `compare_webs.py` does

`compare_webs.py` runs the same measurements on the Angolan shelf (`FW_003`) and the Mondego estuary (`FW_016_01`) and puts them next to the Gulf of Cadiz (`FW_005`). All three are Ecopath diet matrices from Web of Life, so the methods carry over without changes. The raw data is in [`data/`](../data/README.md), with one folder per web.

Each web is cleaned the same way as in `build_network.py`. The Ecopath boundary row (`Import` or `Imports`) is dropped after checking that it eats nothing, detritus, cannibalism and weak links are kept, and every diet is rescaled to sum to 1. The measurements are trophic level, the whole-web measures in `foodweb.food_web_properties`, degree centralization, ten centralities against trophic level, single-group and whole-band removals, R50 for seven removal orders and L50 for three link orders, all under both extinction rules.

As a control, `compare_webs.py` rebuilds the Gulf of Cadiz from the Web of Life edge list instead of our cleaned files, and it stops if the rebuilt web does not match the Gulf of Cadiz outputs. It also draws the Angolan shelf and Mondego estuary food webs by trophic level, with the same function that draws the Gulf of Cadiz in `figures/01_web/`. It writes `output/compare_webs_*.csv` and 13 figures in `figures/08_comparison/`, and it does not change anything in `output/cadiz_*`.

## What `compare_webs_stats.py` does

`compare_webs_stats.py` adds an interval or a test to each result from `compare_webs.py`, for the same three webs.

- Baseline table: nodes, links, connectance, degrees, trophic levels, clustering, path length and Freeman centralization (degree, in-degree, out-degree and betweenness). Centralization measures how much the most central group stands out from the rest (0 = all groups equal, 1 = a star). Each centralization is compared with 1000 random directed graphs of the same size.
- Trophic level against five measures (number of prey, effective number of prey, number of predators, total degree and betweenness), for the consumers in each web. Each Spearman ρ gets a bootstrap 95% interval (10,000 resamples) and a permutation p-value. Since ρ only measures how well two rankings agree, each plot also has a least-squares line with a 95% band to show the relationship itself.
- Groups of nodes: a Kruskal–Wallis test across the trophic bands (and, for the Gulf of Cadiz, across the taxonomic categories), followed by pairwise Mann–Whitney tests with the Holm correction.
- Node removal: a random order is run 1000 times. A targeted order is a fixed ranking, so it only varies where groups tie on the ranking score, and each targeted order is run 200 times with the ties broken at random. Each targeted order is then compared with the 1000 random orders (a two-sided Monte Carlo p-value) on R50 and on the area under the share-lost curve. R50 moves in steps of 1/41, so lots of random orders tie with a targeted order exactly. The area under the curve does not have this problem, so it is the better test.
- A self-check: the script stops unless it gets the same correlations, degree centralization and R50 values as `compare_webs.py`.

`compare_webs_stats.py` writes `output/compare_webs_stats_*.csv`, the baseline table for LaTeX and 38 figures in `figures/08_comparison/` (including the baseline table as a figure). So far, these tests only cover node removal, not link removal.

## Checks (`code/checks/`)

`verify_cascade.py` redoes the extinction rule as matrix algebra, without sharing any code with `foodweb.py`. At θ = 1, 0.75, 0.5 and 0.25, it compares every single-group removal and 300 random multi-group removals, every single-link cut and 300 random sets of cut links, and the faster link-cutting code against the full cascade along 50 random cutting sequences. All 7,160 comparisons agree. The script then runs a deliberately broken copy of itself (a strict threshold instead of a non-strict one) and checks that the broken copy fails, which shows the check can catch an error.

`verify_with_igraph.py` recomputes clustering, transitivity, path length, diameter, the largest strongly connected component, assortativity, mutual predation pairs, and node and edge betweenness in igraph, a separate network library. All of them agree to rounding. Running the whole pipeline twice also gives identical tables and figures.

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
