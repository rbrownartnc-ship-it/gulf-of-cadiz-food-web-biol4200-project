# Code

To run everything in order, with the checks at the end (about 2 minutes):

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

`build_network.py` has to run first, as everything after it reads what it writes. After that, the order mostly does not matter. The exceptions are `compare_webs.py`, which checks itself against the Gulf of Cadiz outputs, and `compare_webs_stats.py`, which checks itself against `compare_webs.py`, so those two run after the other analyses and in that order. The four figure scripts only read `output/`, so they go last.

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
| `checks/verify_cascade.py` | nothing (it stops with an error if anything disagrees) | |
| `checks/verify_with_igraph.py` | nothing (it stops with an error if anything disagrees) | |
| `foodweb.py` | shared functions for loading the web, the extinction cascade, null models, PageRank importance, figure style and drawing the food webs | |
| `run_all.py` | runs everything above in order | |

Each script finds the repo from its own location, so you can run it from any folder. Every random step uses a fixed seed (4200, and 4 for the layout of the food web figures), so rerunning gives the same files.

The figures are drawn at the size they print. The food webs, the explainer and the panel figures are 7 in wide (full page width), and everything else is 3.4 in (one column). No text in any figure is smaller than 6.5 pt, and each figure is saved as a PDF for LaTeX and a 300-dpi PNG for everything else. See [`figures/README.md`](../figures/README.md).

## What `build_network.py` does

1. It reads the labeled 44 × 44 matrix and checks that the row and column labels match. It also checks that every consumer's column sums to 1, which tells us the rows are prey and the columns are predators.
2. It removes `Import` (food eaten outside the model area). Every other cleaning decision is written to `output/cadiz_cleaning_log.csv`, with one row per step.
3. It builds a `networkx.DiGraph` with edges pointing prey → predator (the direction energy flows), where the weight is the share of the predator's diet. If you want the "who eats whom" direction instead, use `G.reverse()`.
4. It works out the node traits, using the equations below. The column definitions are in [`output/README.md`](../output/README.md).
5. It saves the CSVs and the GraphML file.
6. It draws the diet matrix heatmap and the food web by trophic level, 7 in wide, as a PDF and a 300-dpi PNG.

### Equations

`D[j, i]` is the share of predator *i*'s diet that is prey *j*, rescaled so each consumer's diet sums to 1.

Trophic level follows the Ecopath convention (basal groups = 1) and is solved exactly as a linear system, with cannibalism included:

$$
TL_i = 1 + \sum_j D_{ji} TL_j
\quad\Longleftrightarrow\quad
(\mathbf{I} - \mathbf{D}^\top) \mathbf{TL} = \mathbf{1}
$$

The omnivory index (Christensen & Pauly 1992) is 0 when every prey item is on the same trophic level:

$$
OI_i = \sum_j D_{ji} \left( TL_j - (TL_i - 1) \right)^2
$$

Diet diversity is the effective number of prey, where `p_j` is the diet without the self-loop, rescaled to sum to 1:

$$
\mathrm{effective\ prey}_i = \exp\left( -\sum_j p_j \ln p_j \right)
$$

Generality and vulnerability are the number of prey (in-degree) and the number of predators (out-degree), not counting self-loops.

Importance as prey is the weighted out-degree, using the original (not rescaled) diet shares:

$$
s_j = \sum_i D^{\mathrm{orig}}_{ji}
$$

## What `network_structure.py` does

The whole-web measures go in `cadiz_global_structure.csv`. They are binary (a link is there or not) unless the name says weighted or directed, and cannibalistic self-loops are left out of paths and clustering.

| Measure | Definition |
|---|---|
| connectance | L / S² (directed, self-loops included) |
| largest weakly connected component | the giant component, ignoring link direction |
| largest strongly connected component | the largest feeding loop, where every member can reach every other along feeding links |
| characteristic path length | mean shortest path between pairs of groups, ignoring direction (Williams et al. 2002) |
| clustering, binary | mean local clustering coefficient, ignoring direction |
| clustering, weighted | Onnela et al. (2005), with link weight = diet share summed over both directions |
| clustering, directed | Fagiolo (2007), all directed triangle types |
| trophic coherence q | SD across links of predator TL − prey TL (Johnson et al. 2014). 0 means perfectly layered, and lower q goes with more stable webs. |
| omnivore | a consumer whose prey are at different shortest-chain trophic levels |

We compare those measures against three null models in `cadiz_structure_vs_null.csv`. Each row has the real value, the null mean and SD, a z-score, and the fraction of null webs below the real value. We leave out any measure that a null model holds fixed.

| Null model | Keeps | Webs |
|---|---|---|
| random (ER) | number of groups and links | 1000 |
| degree-preserving | every group's number of prey and predators (`networkx.directed_edge_swap`, 5 × L swaps) | 300 |
| niche model (Williams & Martinez 2000) | groups and connectance (accepted within ±3%, connected, and every group reachable from a basal group) | 1000 |

ER and rewired webs cannot have cannibalism, so we compare them against the web without its 14 self-loops. Measures that need trophic levels are skipped when most null webs have no basal group.

`cadiz_centrality.csv` has one row per group with these centralities:
- number of prey, number of predators, total degree and out-strength (importance as prey)
- betweenness, both binary and weighted, where the distance is −ln(diet share) so a strong link is a short hop
- local clustering (binary, weighted and directed)
- PageRank importance (Allesina & Pascual 2009), which runs PageRank on links pointing consumer → resource, plus a root node that every basal group points to and that points to every group. A group scores high when important groups depend on it (damping factor 0.99).

Each centrality is Spearman-correlated with trophic level, both across the 40 consumers and across all 43 groups (`cadiz_centrality_vs_tl.csv`).

## What `node_removal.py` does

After a group is removed, a consumer goes secondarily extinct once it has lost at least θ of its diet (`foodweb.Cascade`). This uses the rescaled diet shares, and cannibalism never keeps a group alive. It keeps going until nothing else dies.
- θ = 1 is "all prey lost", the topological rule of Dunne, Williams & Martinez (2002).
- θ = 0.5 is "half of diet lost", the weighted version.
- θ = 0.25 and 0.75 are run as a sensitivity check (R50 only).

Phytoplankton, Detritus and Discard have no prey, so they never starve. The rule only works bottom-up, as removing a predator can never cause an extinction here. Top-down effects like predator release would need a dynamic model.

| Analysis | Output |
|---|---|
| Single knockouts, where each of the 43 groups is removed by itself | `cadiz_node_knockouts.csv` |
| Guild removals, where a whole trophic band or taxonomic group is removed at once | `cadiz_guild_removal.csv` |
| Removal sequences, where living groups are removed one at a time in a random order (1000 times) or ranked on the intact web. The rankings are most and least connected, highest and lowest trophic level, most important prey (out-strength), PageRank importance and betweenness. The recalculated versions of the degree and betweenness rankings re-rank the targets on the surviving web after every removal (Holme et al. 2002). Groups that are already gone from a secondary extinction are skipped. | `cadiz_node_robustness_curves.csv` |
| R50, the fraction of the 41 living groups that have to be removed before half of them are lost, counting primary and secondary losses (Dunne et al. 2002). The highest it can be is 21/41 = 0.51, which happens when there are no secondary extinctions. | `cadiz_node_robustness_summary.csv` |
| The giant component during the same removals, with and without secondary extinctions (Albert et al. 2000). This is the largest weakly connected component as a share of all 43 groups and of the groups still present, plus the point where the surviving web first splits. | `cadiz_node_robustness_curves.csv`, `cadiz_node_fragmentation.csv` |

## What `link_removal.py` does

Cutting a link means a feeding interaction stops (the predator no longer eats that prey), while both groups survive the cut itself. The same extinction rule then applies (`foodweb.LinkRemoval`, a faster version of `foodweb.Cascade` for long sequences of cuts). Cannibalistic self-loops are left alone.

| Analysis | Output |
|---|---|
| Single-link knockouts, where each of the 397 feeding links is cut by itself, along with its edge betweenness (directed) and whether it is a bridge | `cadiz_link_knockouts.csv` |
| Link-removal sequences: random (500 times), strongest first, weakest first (the weak-link idea of McCann et al. 1998), highest edge betweenness first both static and recalculated (Girvan & Newman 2002; Holme et al. 2002), links from the lowest trophic level prey first, and links into the highest trophic level predators first. Links that are already gone because one end starved are skipped. | `cadiz_link_robustness_curves.csv` |
| L50, the fraction of the 397 links cut before half of the 41 living groups are lost, at θ = 1, 0.75, 0.5 and 0.25 | `cadiz_link_robustness_summary.csv` |
| The giant component while links are cut, with and without starvation (bond percolation), and the point where the surviving web first splits | `cadiz_link_robustness_curves.csv`, `cadiz_link_fragmentation.csv` |

## What `distributions.py` does

It makes one histogram per property: number of prey, number of predators, total degree, importance as prey, trophic level, clustering, betweenness, omnivory index, diet diversity, and link strength (for the 397 links). The three degree histograms also show what a random (ER) web with the same groups and links would look like. Its degrees are binomial, B(S − 1, p) with p = L / (S(S − 1)), and the expected count is worked out for each bin. It also plots the cumulative degree distribution against an exponential (Camacho et al. 2002), and it saves summary statistics, including variance/mean against the random-web value of 1 − p, to `cadiz_distribution_stats.csv`.

## What `compare_webs.py` does

This script runs the same measurements on the Angolan shelf (`FW_003`) and the Mondego estuary (`FW_016_01`) and puts them next to the Gulf of Cadiz (`FW_005`). All three are Ecopath diet matrices from Web of Life, so the methods carry over without any changes. The raw data is in [`data/`](../data/README.md), with one folder per web.

Each web is cleaned the same way as in `build_network.py`. The Ecopath boundary row (`Import` or `Imports`) is dropped after checking that it eats nothing, detritus, cannibalism and weak links are kept, and every diet is rescaled to sum to 1. The measurements are trophic level, the whole-web measures in `foodweb.food_web_properties`, degree centralization, ten centralities against trophic level, single-group and whole-band removals, R50 for seven removal orders, and L50 for three link orders, all under both extinction rules.

The Gulf of Cadiz is also rebuilt here from the Web of Life edge list instead of our cleaned files, as a control, and the script stops if it does not match the Gulf of Cadiz outputs. It also draws the Angolan shelf and Mondego estuary food webs by trophic level, with the same function used for the Gulf of Cadiz in `figures/01_web/`. It writes `output/compare_webs_*.csv` and 13 figures in `figures/08_comparison/`, and does not touch anything in `output/cadiz_*`.

## What `compare_webs_stats.py` does

This script puts an interval or a test on each result from `compare_webs.py`, for the same three webs.

- It makes the baseline table: nodes, links, connectance, degrees, trophic levels, clustering, path length and Freeman centralization (degree, in-degree, out-degree and betweenness). Each centralization is compared against 1000 random directed graphs of the same size.
- It correlates trophic level with five measures (number of prey, effective number of prey, number of predators, total degree and betweenness) for the consumers in each web. Each Spearman ρ gets a bootstrap 95% interval (10,000 resamples) and a permutation p-value. Since ρ only tells you how well two rankings agree, each plot also has a least-squares line with a 95% band, so you can see the actual relationship.
- It compares groups of nodes with a Kruskal–Wallis test across the trophic bands (and, for the Gulf of Cadiz, across the taxonomic categories), followed by pairwise Mann–Whitney tests with the Holm correction.
- For node removal, the random order is 1000 trials. A targeted order is a fixed ranking, though, so it only changes where groups tie on the score, and each one is run 200 times with the ties broken at random. Each targeted order is then tested against the random orders (two-sided Monte Carlo p-value) on R50 and on the area under the share-lost curve. R50 moves in steps, so lots of random orders tie with a targeted one, and the area does not have that problem.
- It stops unless it gets the same correlations, degree centralization and R50 values as `compare_webs.py`.

It writes `output/compare_webs_stats_*.csv`, the baseline table for LaTeX, and 38 figures in `figures/08_comparison/` (including the baseline table as a figure). It only covers node removal so far, not link removal.

## Checks (`code/checks/`)

`verify_cascade.py` redoes the extinction rule as matrix algebra, without sharing any code with `foodweb.py`. At θ = 1, 0.75, 0.5 and 0.25, it compares every single-group removal and 300 random multi-group removals, every single-link cut and 300 random sets of cut links, and the faster link remover against the full cascade along 50 random cutting sequences. That is 7,160 comparisons, and all of them agree. It then runs a deliberately broken copy of itself (a strict threshold instead of a non-strict one) and checks that the broken copy fails.

`verify_with_igraph.py` recomputes clustering, transitivity, path length, diameter, the largest strongly connected component, assortativity, mutual predation pairs, and node and edge betweenness in igraph, and all of them agree to rounding. Running the whole pipeline twice also gives the exact same tables and figures.

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
