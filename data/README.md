# Raw Data

Torres, M. Á., Coll, M., Heymans, J. J., Christensen, V., & Sobrino, I. (2013). Food-web structure of and fishing impacts on the Gulf of Cadiz ecosystem (South-western Spain). *Ecological Modelling*, 265, 26–44. https://doi.org/10.1016/j.ecolmodel.2013.05.019

Via the Web of Life database, network **FW_005**: https://www.web-of-life.es/map.php?type=7
(database paper: Fortuna, M. A., Ortega, R., & Bascompte, J. (2014). The Web of Life. arXiv:1403.2575. https://doi.org/10.48550/arXiv.1403.2575)

Web of Life asks every user to state: "This work has used the Web of Life database (www.web-of-life.es)".

The files here are **exactly as downloaded** on 2026-10-15 and are never edited. All of the cleaning happens in [`code/build_network.py`](../code/build_network.py), and every step is listed in [`output/cadiz_cleaning_log.csv`](../output/cadiz_cleaning_log.csv).

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

On https://www.web-of-life.es/map.php?type=7, select network FW_005 and download it as CSV **with species names**. Its values were cross-checked against an earlier unlabeled download (2026-09-28) and against the names served by the Web of Life API (`get_networks.php?network_name=FW_005`). The values are identical and the group names match.

## `web-of-life_2026-11-11_comparison/`

The two webs we compare the Gulf of Cadiz with, plus the Gulf of Cadiz again as a control. They were downloaded on 2026-11-11 exactly as the Web of Life API serves them and are never edited. All cleaning happens in [`code/compare_webs.py`](../code/compare_webs.py).

| Network | Site | Source | Groups | Links |
|---|---|---|---|---|
| `FW_005` | Gulf of Cadiz, Spain | Torres et al. 2013, *Ecological Modelling* 265, 26–44 | 43 | 411 |
| `FW_003` | Angolan shelf | Angelini & Velho 2011, *Scientia Marina* 75(2) | 28 | 127 |
| `FW_016_01` | Mondego estuary, Portugal | Baeta et al. 2011, *Ecological Modelling* 222, 1209–1221 | 36 | 240 |

Group and link counts are after cleaning (the Ecopath `Import` row removed where present). All three say the cell is "the relative frequency of prey species/group in the diet of each predator species/group", which is why the same methods apply to all of them.

| File | Contents |
|---|---|
| `<network>_edges.json` | One record per nonzero cell: `species1` = prey, `species2` = predator, `connection_strength` = the share of the predator's diet. For `FW_005` this matches `FW_005.csv` in the 2026-10-15 folder exactly. |
| `<network>_info.csv` | Citation, cell-value meaning, location, coordinates |
| `<network>_species.csv` | Per node: kingdom, order, family and taxonomic resolution |
| `_all_networks_catalogue.csv` | Metadata for all 330 networks in Web of Life, 39 of them food webs. We chose the comparison webs from this. |

Only the Ecopath diet-fraction webs (`FW_001` to `FW_010` and `FW_016_01`) can take our weighted methods, as the other food webs are unweighted or record gut-content frequency. Of those, the Angolan shelf and the Mondego estuary are marine or estuarine like the Gulf of Cadiz.

The nodes are not the same kind of thing in all three, though, and this comes from Web of Life's own `taxonomic resolution` field:

| Network | Species | Genus | Family | Subclass | Group | blank |
|---|---|---|---|---|---|---|
| `FW_005` Gulf of Cadiz | – | – | – | – | 6 | 38 |
| `FW_003` Angolan shelf | 2 | 6 | 5 | – | 15 | – |
| `FW_016_01` Mondego estuary | 28 | 2 | – | 1 | 6 | – |

## How to re-download the comparison webs

```bash
curl -s "https://www.web-of-life.es/get_network_info.php" -o _all_networks_catalogue.csv
for n in FW_005 FW_003 FW_016_01; do
  curl -s "https://www.web-of-life.es/get_networks.php?network_name=$n"      -o "${n}_edges.json"
  curl -s "https://www.web-of-life.es/get_network_info.php?network_name=$n"  -o "${n}_info.csv"
  curl -s "https://www.web-of-life.es/get_species_info.php?network_name=$n"  -o "${n}_species.csv"
done
```
