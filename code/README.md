# Code

Everything, in order, with the checks at the end (about 3 minutes):

```bash
python code/run_all.py               # add --no-checks to skip code/checks/
```

Or one script at a time, from the repository root:

```bash
python code/build_network.py         # data/ -> cleaned web, traits, web figures     (~5 s)
python code/rq_feasibility.py        # trophic level vs degree and diet diversity
python code/distributions.py         # histograms of node and link properties       (~5 s)
python code/network_structure.py     # structure, null models, centralities         (~30 s)
python code/node_removal.py          # removing groups: knockouts, sequences, R50    (~40 s)
python code/edge_removal.py          # cutting links: knockouts, sequences, L50      (~20 s)
python code/write_docs.py            # notes/ and figure READMEs from the results
python code/checks/verify_cascade.py      # independent check of the extinction rule
python code/checks/verify_with_igraph.py  # structure numbers re-done in igraph
```

`build_network.py` has to run first. Everything after it only reads what it wrote, so the order of the analysis scripts does not matter, and `write_docs.py` goes last as it reads all of their results.

| Script | Writes (in `output/` unless noted) | Figures |
|---|---|---|
| `build_network.py` | cleaned web, cleaning log, node traits, edge list, GraphML, `cadiz_foodweb_data.xlsx` | `figures/01_web/` |
| `rq_feasibility.py` | `rq_feasibility.txt` | |
| `distributions.py` | `cadiz_distribution_stats.csv` | `figures/02_distributions/` |
| `network_structure.py` | `cadiz_global_structure.csv`, `cadiz_structure_vs_null.csv`, `cadiz_centrality.csv`, `cadiz_centrality_vs_tl.csv`, `network_structure.txt` | `figures/03_structure/`, `figures/04_centrality/` |
| `node_removal.py` | `cadiz_node_knockouts.csv`, `cadiz_guild_removal.csv`, `cadiz_node_robustness_summary.csv`, `cadiz_node_robustness_curves.csv`, `cadiz_node_fragmentation.csv`, `node_removal.txt` | `figures/05_node_removal/` |
| `edge_removal.py` | `cadiz_link_knockouts.csv`, `cadiz_link_robustness_summary.csv`, `cadiz_link_robustness_curves.csv`, `cadiz_link_fragmentation.csv`, `edge_removal.txt` | `figures/06_edge_removal/` |
| `write_docs.py` | `notes/*.md`, `figures/README.md`, `figures/*/README.md` | |
| `checks/verify_cascade.py` | nothing; fails loudly on any disagreement | |
| `checks/verify_with_igraph.py` | nothing; fails loudly on any disagreement | |
| `foodweb.py` | shared helpers: loading the web, the extinction cascade (groups and links), null models, PageRank importance, figure style, results workbook | |
| `run_all.py` | runs everything above in order | |

Every analysis script also rebuilds `output/cadiz_analysis_results.xlsx`, which holds every result table as a sheet.

Each script finds the repo from its own path, so you can run it from any folder. Every random step uses a fixed seed (4200, and 4 for the food-web figure layout), so rerunning gives identical files. The two Excel workbooks are the one exception, as they store the time they were saved.

**Figures** are drawn at the size they actually print, which is 3.4 in (one column) for everything except `01_web/` at 7 in (full width). No text in any figure is smaller than 6.5 pt, and each one is saved twice: a PDF for LaTeX and a 300-dpi PNG for everything else. See [`figures/README.md`](../figures/README.md).

## What `build_network.py` does

1. **Load and check.** Reads the labelled 44 × 44 matrix and confirms that row and column labels match. Also confirms every consumer's column sums to 1, which establishes rows = prey and columns = predators.
2. **Clean.** Removes `Import` (food eaten outside the model area). The other cleaning decisions are written to `output/cadiz_cleaning_log.csv`, one row per step.
3. **Build.** `networkx.DiGraph` with **edges pointing prey → predator** (the direction energy flows), and weight = share of the predator's diet. Use `G.reverse()` for the "who eats whom" convention.
4. **Derive node traits.** See the equations below and the column definitions in [`output/README.md`](../output/README.md).
5. **Save** CSVs, GraphML, a text summary, and an Excel workbook with one sheet per table.
6. **Draw** the diet-matrix heatmap and the food web by trophic level, at their printed size (7 in wide), each as a vector PDF and a 300-dpi PNG. See [`figures/README.md`](../figures/README.md).

Every output is reproducible byte for byte apart from the Excel workbook, as it stores the time it was saved. So it shows up as changed after every run even when nothing inside it is actually different.

### Equations

Notation: `D[j, i]` is the share of predator *i*'s diet that is prey *j*, rescaled so each consumer's diet sums to 1.

**Trophic level** (Ecopath convention, basal groups = 1). It is solved exactly as a linear system, with cannibalism included:

$$
TL_i = 1 + \sum_j D_{ji} TL_j
\quad\Longleftrightarrow\quad
(\mathbf{I} - \mathbf{D}^\top) \mathbf{TL} = \mathbf{1}
$$

**Omnivory index** (Christensen & Pauly 1992). It is 0 when every prey item sits on one trophic level:

$$
OI_i = \sum_j D_{ji} \left( TL_j - (TL_i - 1) \right)^2
$$

**Diet diversity** (effective number of prey). Here `p_j` is the diet without the self-loop, rescaled to sum to 1:

$$
\mathrm{effective\ prey}_i = \exp\left( -\sum_j p_j \ln p_j \right)
$$

**Generality / vulnerability**: the number of prey (in-degree) and the number of predators (out-degree), not counting self-loops.

**Importance as prey**: weighted out-degree, using the original (not rescaled) diet shares:

$$
s_j = \sum_i D^{\mathrm{orig}}_{ji}
$$

## What `rq_feasibility.py` does

Spearman rank correlation of trophic level against each of four measures, across the 40 consumers (basal groups excluded). Current output:

| Trophic level vs | ρ | p |
|---|---|---|
| number of prey | +0.75 | 2.9e-08 |
| number of predators | −0.65 | 4.7e-06 |
| total degree | −0.07 | 0.67 |
| effective number of prey | +0.69 | 7.8e-07 |

## What `network_structure.py` does

**Whole-web measures** (`cadiz_global_structure.csv`). Measures are binary (presence or absence of a link) unless the name says weighted or directed; cannibalistic self-loops are left out of paths and clustering.

| Measure | Definition |
|---|---|
| connectance | L / S² (directed, self-loops included) |
| largest weakly connected component | the giant component, ignoring link direction |
| largest strongly connected component | the largest feeding loop: every member can reach every other along feeding links |
| characteristic path length | mean shortest path between pairs of groups, direction ignored (Williams et al. 2002) |
| clustering, binary | mean local clustering coefficient, direction ignored |
| clustering, weighted | Onnela et al. (2005); link weight = diet share, summed over both directions |
| clustering, directed | Fagiolo (2007), all directed triangle types |
| trophic coherence q | SD across links of predator TL − prey TL (Johnson et al. 2014). 0 = perfectly layered; lower q goes with more stable webs. |
| omnivore | consumer whose prey sit at different shortest-chain trophic levels |

**Null models** (`cadiz_structure_vs_null.csv`). Each row gives the empirical value, the null mean and SD, a z-score, and the fraction of null webs below the empirical value. Properties a null model keeps fixed by construction are left out.

| Null model | Keeps | Webs |
|---|---|---|
| random (ER) | number of groups and links | 1000 |
| degree-preserving | every group's number of prey and predators (`networkx.directed_edge_swap`, 5 × L swaps) | 300 |
| niche model (Williams & Martinez 2000) | groups and connectance (accepted within ±3%, connected, every group reachable from a basal group) | 1000 |

ER and rewired webs cannot hold cannibalism, so they are compared against the web without its 14 self-loops. Measures that need trophic levels are skipped wherever most null webs have no basal group.

**Centralities** (`cadiz_centrality.csv`), one row per group:
- number of prey, number of predators, total degree, out-strength (importance as prey)
- betweenness: binary, and weighted with distance = −ln(diet share), so a strong link is a short hop
- local clustering: binary, weighted, directed
- PageRank importance (Allesina & Pascual 2009): PageRank on links pointing consumer → resource, plus a root node that every basal group points to and that points to every group. A group scores high when important groups depend on it. Damping factor 0.99.

Each centrality is Spearman-correlated with trophic level, across the 40 consumers and across all 43 groups (`cadiz_centrality_vs_tl.csv`).

## What `node_removal.py` does

**Extinction rule** (`foodweb.Cascade`). After a removal, a consumer goes secondarily extinct once it has lost at least θ of its diet. Diet shares are the rescaled ones, and cannibalism never keeps a group alive. This repeats until nothing more dies.
- θ = 1, "all prey lost": the topological rule of Dunne, Williams & Martinez (2002).
- θ = 0.5, "half of diet lost": the weighted version.
- θ = 0.25 and 0.75 are run as a sensitivity check (R50 only).

Phytoplankton, Detritus and Discard have no prey, so they never starve. The rule only works bottom-up, as removing a predator can never cause an extinction here. Predator release and the other top-down effects would need a dynamic model rather than a topological one.

| Analysis | Output |
|---|---|
| Single knockouts: each of the 43 groups removed alone | `cadiz_node_knockouts.csv` |
| Guild removals: a whole trophic band or taxonomic group at once | `cadiz_guild_removal.csv` |
| Removal sequences: living groups removed one by one, in a random order (1000×) or ranked on the intact web. Rankings: most / least connected, highest / lowest trophic level, most important prey (out-strength), PageRank importance, betweenness. **Recalculated** variants of the degree and betweenness attacks re-rank the targets on the surviving web after every removal (Holme et al. 2002). Groups already lost to a secondary extinction are skipped. | `cadiz_node_robustness_curves.csv` |
| R50: fraction of the 41 living groups that must be removed before half of them are lost, counting primary and secondary losses (Dunne et al. 2002). The maximum is 21/41 = 0.51, reached when there are no secondary extinctions. | `cadiz_node_robustness_summary.csv` |
| Giant component during the same removals, with and without secondary extinctions (Albert et al. 2000). Measured as the largest weakly connected component, as a share of all 43 groups and of the groups still present, plus the point where the surviving web first splits. | `cadiz_node_robustness_curves.csv`, `cadiz_node_fragmentation.csv` |

## What `edge_removal.py` does

A **cut link** is a feeding interaction that stops: the predator no longer eats that prey, while both groups survive the cut itself. The same extinction rule then applies (`foodweb.LinkRemoval`, an incremental version of `foodweb.Cascade`, so a 400-step sequence is fast). Cannibalistic self-loops are left alone.

| Analysis | Output |
|---|---|
| Single-link knockouts: each of the 397 feeding links cut alone, with edge betweenness (directed) and whether the link is a bridge | `cadiz_link_knockouts.csv` |
| Link-removal sequences: random (500×), strongest first, weakest first (McCann et al. 1998 weak-link idea), highest edge betweenness first, static and recalculated (Girvan & Newman 2002; Holme et al. 2002), links from the lowest-trophic-level prey first, links into the highest-trophic-level predators first. Links already gone because one end starved are skipped. | `cadiz_link_robustness_curves.csv` |
| L50: fraction of the 397 links cut before half of the 41 living groups are lost, at θ = 1, 0.75, 0.5 and 0.25 | `cadiz_link_robustness_summary.csv` |
| Giant component while links are cut, with and without starvation (bond percolation), and the point where the surviving web first splits | `cadiz_link_robustness_curves.csv`, `cadiz_link_fragmentation.csv` |

## What `distributions.py` does

- One histogram per property: number of prey, number of predators, total degree, importance as prey, trophic level, clustering, betweenness, omnivory index, diet diversity, and link strength (397 links).
- The three degree histograms carry the expected histogram of a random (ER) web with the same groups and links. Its degrees are binomial, B(S − 1, p) with p = L / (S(S − 1)), and the expectation is computed per bin.
- Also the cumulative degree distribution against an exponential (Camacho et al. 2002).
- Summary statistics, including variance/mean against the random-web value 1 − p: `cadiz_distribution_stats.csv`.

## Notes and figure READMEs (`write_docs.py`)

`write_docs.py` writes [`notes/`](../notes/README.md), one bullet-point note per analysis, plus the README in each figure folder. Every number is read straight out of `output/`, so rerunning the pipeline rewrites the notes and they cannot drift away from the results.

It also holds the two lists that decide what the paper uses: `SELECTED`, the ten figures chosen for the manuscript and the one-line reason for each, and `EXPLAIN`, the paragraph printed under each of those figures. Keeping them here rather than in the READMEs means a rerun regenerates the ★ marks instead of wiping them, and the script stops if a chosen figure has no explanation or names a figure that does not exist.

The notes and those paragraphs are facts and documentation for the group, not text for the paper. The course does not allow generative AI for any of the writing, so the manuscript gets written from these in our own words.

## Checks (`code/checks/`)

- **`verify_cascade.py`** re-implements the extinction rule as matrix algebra, sharing no code with `foodweb.py`. At θ = 1, 0.75, 0.5 and 0.25 it compares:
  - every single-group removal, plus 300 random multi-group removals
  - every single-link cut, plus 300 random sets of cut links
  - the incremental link remover against the batch cascade along 50 random cutting sequences

  That is 7,160 comparisons and all of them agree. It then runs a deliberately broken copy of itself, using a strict threshold instead of a non-strict one, and confirms that the broken copy fails. Without that, a pass would not really tell you anything.
- **`verify_with_igraph.py`** recomputes clustering, transitivity, path length, diameter, the largest strongly connected component, assortativity, mutual predation pairs, and node and edge betweenness in igraph. All agree to rounding.
- Running the full pipeline twice gives byte-identical CSVs, text files and figures.

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
- Kondoh, M. (2003). Foraging adaptation and the relationship between food-web complexity and stability. *Science* 299, 1388–1391. https://doi.org/10.1126/science.1079154
- McCann, K., Hastings, A. & Huxel, G. R. (1998). Weak trophic interactions and the balance of nature. *Nature* 395, 794–798. https://doi.org/10.1038/27427
- Onnela, J.-P., Saramäki, J., Kertész, J. & Kaski, K. (2005). Intensity and coherence of motifs in weighted complex networks. *Physical Review E* 71, 065103. https://doi.org/10.1103/PhysRevE.71.065103
- Williams, R. J. & Martinez, N. D. (2000). Simple rules yield complex food webs. *Nature* 404, 180–183. https://doi.org/10.1038/35004572
- Williams, R. J., Berlow, E. L., Dunne, J. A., Barabási, A.-L. & Martinez, N. D. (2002). Two degrees of separation in complex food webs. *PNAS* 99, 12913–12916. https://doi.org/10.1073/pnas.192448799
