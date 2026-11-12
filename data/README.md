# Raw Data

Torres, M. Á., Coll, M., Heymans, J. J., Christensen, V., & Sobrino, I. (2013). Food-web structure of and fishing impacts on the Gulf of Cadiz ecosystem (South-western Spain). *Ecological Modelling*, 265, 26–44. https://doi.org/10.1016/j.ecolmodel.2013.05.019

Via the Web of Life database, network **FW_005**: https://www.web-of-life.es/map.php?type=7
(database paper: Fortuna, M. A., Ortega, R., & Bascompte, J. (2014). The Web of Life. arXiv:1403.2575. https://doi.org/10.48550/arXiv.1403.2575)

Web of Life asks every user to state: "This work has used the Web of Life database (www.web-of-life.es)".

The files here are **exactly as downloaded** on 2026-10-15 and are never edited. All of the cleaning happens in [`code/build_network.py`](../code/build_network.py), so if you want to know what changed, every step is listed in [`output/cadiz_cleaning_log.csv`](../output/cadiz_cleaning_log.csv).

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

The four comparison webs for the cross-ecosystem analysis, plus the Gulf of Cadiz again as a
control, downloaded on 2026-11-11 **exactly as the Web of Life API serves them** and never edited.
All cleaning happens in [`code/compare_webs.py`](../code/compare_webs.py).

| Network | Site | Source | Groups | Links |
|---|---|---|---|---|
| `FW_005` | Gulf of Cadiz, Spain | Torres et al. 2013, *Ecological Modelling* 265, 26–44 | 43 | 411 |
| `FW_003` | Angolan shelf | Angelini & Velho 2011, *Scientia Marina* 75(2) | 28 | 127 |
| `FW_006` | Alvarado lagoon, Gulf of Mexico | Cruz-Escalona et al. 2007, *Estuarine, Coastal and Shelf Science* 72, 155–167 | 30 | 229 |
| `FW_007` | St Marks seagrass, Florida | Christian & Luczkovich 1999, *Ecological Modelling* 117, 99–124 | 48 | 221 |
| `FW_016_01` | Mondego estuary, Portugal | Baeta et al. 2011, *Ecological Modelling* 222, 1209–1221 | 36 | 240 |

Group and link counts are after cleaning (the Ecopath `Import` row removed where present).

Each network has three files, plus one catalogue file for the whole database:

| File | Contents |
|---|---|
| `<network>_edges.json` | `get_networks.php?network_name=<network>` — one record per nonzero cell: `species1` = prey, `species2` = predator, `connection_strength` = the share of the predator's diet. Checked against `FW_005.csv` in the 2026-10-15 folder: the 43 × 43 culled matrices are identical. |
| `<network>_info.csv` | `get_network_info.php?network_name=<network>` — citation, cell-value meaning, location, coordinates |
| `<network>_species.csv` | `get_species_info.php?network_name=<network>` — per node: kingdom, order, family and **taxonomic resolution** (Species / Genus / Family / Group) |
| `_all_networks_catalogue.csv` | `get_network_info.php` with no filter — metadata for **all 330 networks in Web of Life**, 39 of them food webs. This is what the choice of comparison webs was made from. |

**Node resolution, from Web of Life's own `taxonomic resolution` field.** This is why Mondego
behaves differently from the rest, and it is the database's judgement rather than ours:

| Network | Species | Genus | Family | Subclass | Group | blank |
|---|---|---|---|---|---|---|
| FW_005 Gulf of Cadiz | – | – | – | – | 6 | 38 |
| FW_003 Angolan shelf | 2 | 6 | 5 | – | 15 | – |
| FW_006 Alvarado lagoon | – | – | – | – | 30 | – |
| FW_007 St Marks seagrass | – | 1 | – | – | 47 | – |
| **FW_016_01 Mondego estuary** | **28** | **2** | – | **1** | 6 | – |

All five say the cell is "the relative frequency of prey species/group in the diet of each predator
species/group", which is why the same methods apply to all of them.

**Two quirks, handled in the code and listed in [`notes/07_cross_ecosystem.md`](../notes/07_cross_ecosystem.md):**
FW_007 is recorded in percent rather than fractions, and 9 of its consumers have diets that do not
add up (as little as 6.5%).

## What else is in the database, and why it was not used

Of the 39 food webs in `_all_networks_catalogue.csv`:

- **Same data type as ours (Ecopath diet fractions):** FW_001 to FW_010 and FW_016_01. These are the
  only ones our weighted methods can be applied to unchanged.
- **FW_011, FW_012_0\*, FW_013_0\*, FW_014_0\*, FW_015_0\*** (15 webs, Thompson & Townsend stream
  webs) are `is_weighted = 0` — binary presence/absence. The diet-share weights, the half-diet
  extinction rule, strong-vs-weak link removal and weighted betweenness are all undefined on them.
- **FW_017 and FW_017_01 to _06** record "standardized frequency of prey in gut content"
  (Pozas-Schacre et al. 2021 coral reefs), a different measurement, not a diet-composition matrix.
- **FW_012, FW_013, FW_014, FW_016, FW_017** are umbrella entries, not networks:
  `get_networks.php?network_name=FW_016` returns an empty set. FW_016_01 is the only Mondego network.
- **FW_008** (Caribbean, Bascompte et al. 2005, 249 species) is the right data type but its diet
  columns sum to between 0.05 and 1.83, so the weights are not comparable.
- **FW_001 Paraná floodplain (40 groups), FW_002 Cerrado river (14), FW_004 Itaipu reservoir (32),
  FW_009 and FW_010 Pantanal oxbow lakes (40, 39)** are clean and would run unchanged — diets sum
  to 1, `Import` handled by the existing rule, no short diets — but they are **freshwater**, so they
  are an out-group rather than a like-for-like marine comparison. Available if the group wants one.

## How to re-download the comparison webs

```bash
curl -s "https://www.web-of-life.es/get_network_info.php" -o _all_networks_catalogue.csv
for n in FW_005 FW_003 FW_006 FW_007 FW_016_01; do
  curl -s "https://www.web-of-life.es/get_networks.php?network_name=$n"      -o "${n}_edges.json"
  curl -s "https://www.web-of-life.es/get_network_info.php?network_name=$n"  -o "${n}_info.csv"
  curl -s "https://www.web-of-life.es/get_species_info.php?network_name=$n"  -o "${n}_species.csv"
done
```

`get_network_info.php` ignores any `network_type` filter and always returns all 330 networks, so
filter locally on the `network_type` column. The same networks are on the website at
<https://www.web-of-life.es/map.php?type=7>, where they download as CSV matrices instead; the
values are the same, which is what the FW_005 control in `code/compare_webs.py` proves.
