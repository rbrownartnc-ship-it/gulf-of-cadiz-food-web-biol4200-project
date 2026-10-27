# Network analysis of marine food webs from a species-centric approach

The repository contains code accompanying the following paper: Robert Brown, Ava Foulk, Emma Nordberg, and Lilly Wu, Network analysis of marine food webs from a species-centric approach (2026). BIOL 4200/4559, Networks in Biology, University of Virginia, Fall 2026.

If you use this repository in any fashion in your own work, please cite our work according to the [`CITATION.cff`](CITATION.cff).

Project milestones and open to-dos are in [`PROJECT_STATUS.md`](PROJECT_STATUS.md).

# Contents

- [Contents](#contents)
- [Getting Started](#getting-started)
  - [Repository layout](#repository-layout)
  - [Installation](#installation)
  - [Reproducing the results](#reproducing-the-results)
- [Other Information](#other-information)
  - [Data](#data)
  - [Authors](#authors)
  - [License](#license)

# Getting started

## Repository layout

| Path | Role |
|---|---|
| [`notes/`](notes/README.md) | **Start here.** Bullet-point notes on every analysis, with the key numbers (generated from the results, so always current) |
| [`data/`](data/) | Raw data exactly as downloaded from Web of Life (Gulf of Cadiz food web, `FW_005`). Never edited. |
| [`code/`](code/README.md) | All analysis code; methods, equations and references in its README |
| `code/build_network.py` | Cleans the raw matrix, builds the weighted directed network, derives trophic level and other node traits |
| `code/distributions.py` | Histograms of degree, link strength, trophic level, clustering and other properties |
| `code/network_structure.py` | Whole-web structure (components, clustering, path length, trophic coherence) against random, degree-preserving and niche-model webs; centralities against trophic level |
| `code/node_removal.py` | Removing groups: knockouts, guild removals, targeted and recalculated attacks with secondary extinctions (R50), giant component |
| `code/edge_removal.py` | Cutting feeding links: link knockouts, strong vs weak links, edge-betweenness attacks (L50), bond percolation |
| `code/write_docs.py` | Writes `notes/` and the figure READMEs from the results |
| `code/checks/` | Independent verification of the extinction rule and the structure numbers |
| `code/run_all.py` | Runs everything in order |
| [`output/`](output/README.md) | Every derived table: culled diet matrix, cleaning log, node traits (trophic level etc.), and every analysis result |
| [`output/cadiz_foodweb_data.xlsx`](output/cadiz_foodweb_data.xlsx) | The cleaned data tables, one sheet each, for Excel |
| [`output/cadiz_analysis_results.xlsx`](output/cadiz_analysis_results.xlsx) | Every analysis result table, one sheet each |
| [`figures/`](figures/README.md) | 52 single-panel figures in six folders (web, distributions, structure, centrality, node removal, edge removal), plus the methods explainer figure in `07_explainer_figure/`, each as PDF + PNG at print size, with previews in each folder's README. **The ten chosen for the paper are marked ★ and listed at the top of [`figures/README.md`](figures/README.md).** |
| [`manuscript/`](manuscript/) | Submitted drafts (proposal, introduction) as PDFs |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Milestones, instructor feedback to address, open decisions |
| `requirements.txt` | Pinned Python packages |
| `CITATION.cff` | How to cite this repository |

## Installation

Python 3.13.

```bash
pip install -r requirements.txt
```

or, with conda:

```bash
conda create -n biol4559 python=3.13
conda activate biol4559
pip install -r requirements.txt
```

## Reproducing the results

From the repository root:

```bash
python code/run_all.py
```

This rebuilds the cleaned web from `data/`, reruns every analysis, rewrites `notes/` and the figure READMEs, and runs the checks. It takes about 3 minutes, and reruns reproduce the same files. To run one script at a time, see [`code/README.md`](code/README.md).

# Other information

## Data

Torres, M. Á., Coll, M., Heymans, J. J., Christensen, V., & Sobrino, I. (2013). Food-web structure of and fishing impacts on the Gulf of Cadiz ecosystem (South-western Spain). *Ecological Modelling*, 265, 26–44. https://doi.org/10.1016/j.ecolmodel.2013.05.019

Obtained from the Web of Life database, network `FW_005`. This work has used the Web of Life database (www.web-of-life.es). Details: [`data/README.md`](data/README.md).

## Authors

- Robert Brown
- Ava Foulk
- Emma Nordberg
- Lilly Wu

## License

This project is licensed under the [BSD-3 License](LICENSE) - see the [LICENSE](LICENSE) file for details.
