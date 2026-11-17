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
| [`data/`](data/README.md) | The raw data from Web of Life, with one folder per web (the Gulf of Cadiz and the two webs we compare it to). We never edit these files. |
| [`code/`](code/README.md) | All of the code, including the scripts for the panel figures. Its README goes over the methods, equations and references. |
| [`output/`](output/README.md) | Every table the code makes, from the cleaned diet matrix and node traits to the results of each analysis |
| [`figures/`](figures/README.md) | Every figure as a PDF and a PNG at print size, with one folder per analysis |
| [`notes/`](notes/README.md) | The main numbers from each analysis |
| [`manuscript/`](manuscript/README.md) | Our drafts as submitted |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Milestones, feedback we still need to address, and open decisions |
| `requirements.txt` | Pinned Python packages |
| `CITATION.cff` | How to cite this repository |

## Naming

Each web has a short name that we use in every folder and file name: `cadiz` for the Gulf of Cadiz (`FW_005`), `angola` for the Angolan shelf (`FW_003`) and `mondego` for the Mondego estuary (`FW_016_01`). The figure folders and the notes share numbers too, so 05 is node removal in both, for example.

In `output/`, the `cadiz_*` tables come from the Gulf of Cadiz analysis, while `compare_webs_*` and `compare_webs_stats_*` come from the two comparison scripts of the same names. A comparison figure that shows a single web has that web's name right after `compare_`. The two extinction rules show up in file names as `all_prey` (all prey lost) and `half_diet` (half of diet lost).

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

This rebuilds the cleaned web from `data/`, reruns every analysis and then runs the checks. It takes about 2 minutes, and running it again gives the exact same files. To run the scripts one at a time, see [`code/README.md`](code/README.md).

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
