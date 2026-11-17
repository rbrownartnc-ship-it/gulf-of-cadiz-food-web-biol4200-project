# Network analysis of marine food webs from a species-centric approach

The repository contains code accompanying the following paper: Robert Brown, Ava Foulk, Emma Nordberg, and Lilly Wu, Network analysis of marine food webs from a species-centric approach (2026). BIOL 4200/4559, Networks in Biology, University of Virginia, Fall 2026.

If you use this repository in any fashion in your own work, please cite our work according to the [`CITATION.cff`](CITATION.cff).

# Contents

- [Contents](#contents)
- [Getting Started](#getting-started)
  - [Repository layout](#repository-layout)
  - [Naming](#naming)
  - [Installation](#installation)
  - [Reproducing the results](#reproducing-the-results)
- [Other Information](#other-information)
  - [Data](#data)
  - [Authors](#authors)
  - [License](#license)

# Getting started

## Repository layout

| Path | What it holds |
|---|---|
| [`data/`](data/README.md) | Raw data from Web of Life, in one folder per web (the Gulf of Cadiz and the two comparison webs). These files are never edited. |
| [`code/`](code/README.md) | All analysis and figure scripts. The code README describes the methods, equations and references. |
| [`output/`](output/README.md) | Every table the code produces, from the cleaned diet matrix and node traits to the results of each analysis |
| [`figures/`](figures/README.md) | Every figure as a PDF and a PNG at print size, in one folder per analysis |
| [`notes/`](notes/README.md) | The main results of each analysis |
| [`manuscript/`](manuscript/README.md) | Our drafts as submitted |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Milestones, feedback still to address, and open decisions |
| `requirements.txt` | Pinned Python packages |
| `CITATION.cff` | How to cite this repository |

## Naming

Each web has a short name that is used in folder and file names: `cadiz` for the Gulf of Cadiz (Web of Life network `FW_005`), `angola` for the Angolan shelf (`FW_003`) and `mondego` for the Mondego estuary (`FW_016_01`). Figure folders and notes are numbered the same way, so `figures/05_node_removal/` and `notes/05_node_removal.md` both cover node removal.

Tables in `output/` start with `cadiz_` for the Gulf of Cadiz analysis, `compare_webs_` for the three-web comparison, and `compare_webs_stats_` for the intervals and tests on that comparison. Similarly, a comparison figure that shows only one web includes that web's short name (for example, `compare_angola_food_web`). The two extinction rules appear in file names as `all_prey` (a consumer dies once all of its prey are gone) and `half_diet` (a consumer dies once half of its diet is gone).

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

`run_all.py` rebuilds the cleaned web from `data/`, reruns every analysis and figure script, and then runs the checks. The full run takes about 2 minutes, and running it twice produces identical files. To run the scripts one at a time, see [`code/README.md`](code/README.md).

# Other information

## Data

Torres, M. Á., Coll, M., Heymans, J. J., Christensen, V., & Sobrino, I. (2013). Food-web structure of and fishing impacts on the Gulf of Cadiz ecosystem (South-western Spain). *Ecological Modelling*, 265, 26–44. https://doi.org/10.1016/j.ecolmodel.2013.05.019

Obtained from the Web of Life database, network `FW_005`. This work has used the Web of Life database (www.web-of-life.es). The two comparison webs and their sources are listed in [`data/README.md`](data/README.md).

## Authors

- Robert Brown
- Ava Foulk
- Emma Nordberg
- Lilly Wu

## License

This project is licensed under the [BSD-3 License](LICENSE) - see the [LICENSE](LICENSE) file for details.
