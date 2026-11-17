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

| Path | Contents |
|---|---|
| [`data/`](data/README.md) | Raw data from Web of Life, with one folder for each web. We do not edit these files. |
| [`code/`](code/README.md) | All analysis and figure scripts. The code README describes the methods, equations and references. |
| [`output/`](output/README.md) | All tables that the code makes: the cleaned diet matrix, the node traits and the results of each analysis |
| [`figures/`](figures/README.md) | All figures as PDF and PNG at print size, with one folder for each analysis |
| [`notes/`](notes/README.md) | A written summary of each analysis, with the main results and their values |
| [`manuscript/`](manuscript/README.md) | Our drafts as submitted |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Milestones, feedback to address and open decisions |
| `requirements.txt` | Pinned Python packages |
| `CITATION.cff` | How to cite this repository |

## Naming

Each web has a short name in folder and file names:
- `cadiz`: Gulf of Cadiz (Web of Life network `FW_005`)
- `angola`: Angolan shelf (`FW_003`)
- `mondego`: Mondego estuary (`FW_016_01`)

Figure folders and notes use the same numbers. For example, `figures/05_node_removal/` and `notes/05_node_removal.md` both show node removal.

Table names in `output/` start with `cadiz_` (Gulf of Cadiz analysis), `compare_webs_` (comparison of the three webs) or `compare_webs_stats_` (intervals and tests for the comparison). A comparison figure of one web has the short name of that web, for example `compare_angola_food_web`. File names show the two extinction rules as `all_prey` and `half_diet`. Under `all_prey`, a consumer dies when it loses all of its prey. Under `half_diet`, a consumer dies when it loses half of its diet.

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

`run_all.py` builds the cleaned web from `data/`, runs all analysis and figure scripts, and then runs the checks. The full run takes about 2 minutes. Two runs give identical files. To run the scripts one at a time, see [`code/README.md`](code/README.md).

# Other information

## Data

Torres, M. Á., Coll, M., Heymans, J. J., Christensen, V., & Sobrino, I. (2013). Food-web structure of and fishing impacts on the Gulf of Cadiz ecosystem (South-western Spain). *Ecological Modelling*, 265, 26–44. https://doi.org/10.1016/j.ecolmodel.2013.05.019

Obtained from the Web of Life database, network `FW_005`. This work has used the Web of Life database (www.web-of-life.es). The sources of the two comparison webs are in [`data/README.md`](data/README.md).

## Authors

- Robert Brown
- Ava Foulk
- Emma Nordberg
- Lilly Wu

## License

This project is licensed under the [BSD-3 License](LICENSE) - see the [LICENSE](LICENSE) file for details.
