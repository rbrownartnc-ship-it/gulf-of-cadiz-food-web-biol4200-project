# Raw Data

Torres, M. Á., Coll, M., Heymans, J. J., Christensen, V., & Sobrino, I. (2013). Food-web structure of and fishing impacts on the Gulf of Cadiz ecosystem (South-western Spain). *Ecological Modelling*, 265, 26–44. https://doi.org/10.1016/j.ecolmodel.2013.05.019

Via the Web of Life database, network **FW_005**: https://www.web-of-life.es/map.php?type=7
(database paper: Fortuna, M. A., Ortega, R., & Bascompte, J. (2014). The Web of Life. arXiv:1403.2575. https://doi.org/10.48550/arXiv.1403.2575)

Web of Life asks every user to state: "This work has used the Web of Life database (www.web-of-life.es)".

The files here are **exactly as downloaded** on 2026-10-15 and are never edited. All cleaning happens in [`code/build_network.py`](../code/build_network.py), and every change is listed in [`output/cadiz_cleaning_log.csv`](../output/cadiz_cleaning_log.csv).

## `web-of-life_2026-10-15_210043/`

| File | Contents |
|---|---|
| `FW_005.csv` | 44 × 44 diet matrix with group names. **Rows = prey, columns = predators.** Each cell is the fraction of the column group's diet made up of the row group (Ecopath diet composition), so every consumer's column sums to 1 (within 0.002). 413 nonzero cells. |
| `references.csv` | Web of Life's metadata for the network: citation, size, location (36.53° N, 6.29° W) |
| `README` | Web of Life's download notes and terms of use |

## What the data is

- An **Ecopath with Ecosim (EwE 6) mass-balance model** of the Gulf of Cadiz, representing **2009**, with **43 functional groups** plus `Import`.
- **Nodes are functional groups, not species.** Some are one species (Anchovy, Sardine, Norway lobster); others are pools (Detritus, Suprabenthos, Meso and microzooplankton).
- **"413 interactions" means 413 nonzero cells**, not 413 observed feeding events.
- `Import` is not a group. It is the share of a predator's diet eaten outside the model area, and it is removed in cleaning.
- Web of Life's connectance (0.437) uses L / (S(S−1)/2) with S = 44. The directed connectance of the cleaned web, L/N², is 0.222.

## How to re-download

On https://www.web-of-life.es/map.php?type=7, select network FW_005 and download it as CSV **with species names**. Its values were cross-checked against an earlier unlabelled download (2026-09-28) and against the names served by the Web of Life API (`get_networks.php?network_name=FW_005`). The values are identical and the group names match.
