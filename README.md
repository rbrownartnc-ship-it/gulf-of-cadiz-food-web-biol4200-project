# Network analysis of marine food webs from a species-centric approach

The repository contains code accompanying the following paper: Robert Brown, Ava Foulk, Emma Nordberg, and Lilly Wu, Network analysis of marine food webs from a species-centric approach (2026). BIOL 4200/4559, Networks in Biology, University of Virginia, Fall 2026.

If you use this repository in any fashion in your own work, please cite our work according to the [`CITATION.cff`](CITATION.cff).

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
| [`data/`](data/README.md) | Raw data exactly as downloaded from Web of Life: the Gulf of Cadiz food web (`FW_005`) and the two webs we compare it with. Never edited. |
| [`code/`](code/README.md) | All analysis code. Its README covers the methods, equations and references. |
| [`output/`](output/README.md) | Every table the code writes: the cleaned diet matrix, the cleaning log, node traits and the results of each analysis |
| [`figures/`](figures/README.md) | Every figure as PDF and PNG at print size, one folder per analysis |
| [`notes/`](notes/README.md) | The key numbers from each analysis |
| [`manuscript/`](manuscript/README.md) | Our submitted drafts as PDFs |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Milestones, the feedback we still have to address and our open decisions |
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

This rebuilds the cleaned web from `data/`, reruns every analysis and runs the checks. It takes about 2 minutes, and running it twice gives the same files. To run one script at a time, see [`code/README.md`](code/README.md).

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
