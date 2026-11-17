# Raw data

All three food webs come from the Web of Life database (Fortuna, M. A., Ortega, R., & Bascompte, J. (2014). The Web of Life. arXiv:1403.2575. https://doi.org/10.48550/arXiv.1403.2575). Web of Life asks every user to state: "This work has used the Web of Life database (www.web-of-life.es)".

Every file here is **exactly as downloaded** and is never edited. Only the file names were changed, so that each web has its own folder and the same file names inside it. All of the cleaning happens in the code: [`code/build_network.py`](../code/build_network.py) for the Gulf of Cadiz, with every step listed in [`output/cadiz_cleaning_log.csv`](../output/cadiz_cleaning_log.csv), and [`code/compare_webs.py`](../code/compare_webs.py) for all three webs.

| Folder | Network | Site | Source | Groups | Links |
|---|---|---|---|---|---|
| [`cadiz_FW_005/`](cadiz_FW_005/) | `FW_005` | Gulf of Cadiz, Spain | Torres, M. Á., Coll, M., Heymans, J. J., Christensen, V., & Sobrino, I. (2013). Food-web structure of and fishing impacts on the Gulf of Cadiz ecosystem (South-western Spain). *Ecological Modelling*, 265, 26–44. https://doi.org/10.1016/j.ecolmodel.2013.05.019 | 43 | 411 |
| [`angola_FW_003/`](angola_FW_003/) | `FW_003` | Angolan shelf | Angelini, R., & Velho, V. F. (2011). Ecosystem structure and trophic analysis of Angolan fishery landings. *Scientia Marina*, 75(2). | 28 | 127 |
| [`mondego_FW_016_01/`](mondego_FW_016_01/) | `FW_016_01` | Mondego estuary, Portugal | Baeta, A., Niquil, A., Marques, J. C., & Patrício, J. (2011). Modelling the effects of eutrophication, mitigation measures and an extreme flood event on estuarine benthic food webs. *Ecological Modelling*, 222, 1209–1221. | 36 | 240 |

Group and link counts are after cleaning (the Ecopath `Import` row removed where present). Each folder name starts with the short name the web has in every file name in the repo (`cadiz`, `angola`, `mondego`), followed by its Web of Life network ID.

## Files in each folder

| File | Contents | Downloaded |
|---|---|---|
| `edges.json` | One record per nonzero cell: `species1` = prey, `species2` = predator, `connection_strength` = the share of the predator's diet | 2026-11-11, from the Web of Life API |
| `network_info.csv` | Citation, what a cell value means, location and coordinates | 2026-11-11, API |
| `node_taxonomy.csv` | Per node: kingdom, order, family and taxonomic resolution | 2026-11-11, API |
| `diet_matrix.csv` | Gulf of Cadiz only. The 44 × 44 diet matrix with group names. **Rows = prey, columns = predators.** Each cell is the share of the column group's diet made up of the row group (Ecopath diet composition), so every consumer's column sums to 1 (within 0.002). 413 nonzero cells. | 2026-10-15, from the website |
| `references.csv` | Gulf of Cadiz only. Web of Life's metadata for the network: citation, size, location (36.53° N, 6.29° W) | 2026-10-15, website |
| `download_readme.txt` | Gulf of Cadiz only. Web of Life's download notes and terms of use | 2026-10-15, website |

[`web_of_life_catalogue.csv`](web_of_life_catalogue.csv) holds the metadata for all 330 networks in Web of Life, 39 of them food webs, and we chose the comparison webs from it.

The Gulf of Cadiz is in both formats on purpose. `build_network.py` cleans `diet_matrix.csv`, while `compare_webs.py` rebuilds the same web from `edges.json` and stops unless it gets the same result. That checks that the comparison treats all three webs the way the main analysis treats the Gulf of Cadiz. The values in the two files are identical.

## What the data is

- Each web is an **Ecopath with Ecosim mass-balance model**. All three say a cell is "the relative frequency of prey species/group in the diet of each predator species/group", which is why the same methods apply to all of them.
- The Gulf of Cadiz model represents **2009**, with **43 functional groups** plus `Import`.
- **Nodes are functional groups, not species**, in the Gulf of Cadiz. Some are one species (Anchovy, Sardine, Norway lobster), and others are pools (Detritus, Suprabenthos, Meso and microzooplankton).
- **"413 interactions" means 413 nonzero cells**, not 413 observed feeding events.
- `Import` is not a group. It is the share of a predator's diet eaten outside the model area, and it is removed in cleaning.
- Web of Life's connectance for the Gulf of Cadiz (0.437) uses L / (S(S−1)/2) with S = 44. The directed connectance of the cleaned web, L/S², is 0.222.

The nodes are not the same kind of thing in all three webs, though, which comes from Web of Life's own `taxonomic resolution` field:

| Network | Species | Genus | Family | Subclass | Group | blank |
|---|---|---|---|---|---|---|
| `FW_005` Gulf of Cadiz | – | – | – | – | 6 | 38 |
| `FW_003` Angolan shelf | 2 | 6 | 5 | – | 15 | – |
| `FW_016_01` Mondego estuary | 28 | 2 | – | 1 | 6 | – |

Only the Ecopath diet-share webs (`FW_001` to `FW_010` and `FW_016_01`) can take our weighted methods, as the other food webs are unweighted or record gut-content frequency. Of those, the Angolan shelf and the Mondego estuary are marine or estuarine like the Gulf of Cadiz.

## How to re-download

The Gulf of Cadiz matrix: on https://www.web-of-life.es/map.php?type=7, select network FW_005 and download it as CSV **with species names**. Its values were cross-checked against an earlier unlabeled download (2026-09-28) and against the Web of Life API, and the values and group names match.

The API files, saved under the names used here:

```bash
curl -s "https://www.web-of-life.es/get_network_info.php" -o web_of_life_catalogue.csv
for pair in cadiz:FW_005 angola:FW_003 mondego:FW_016_01; do
  tag=${pair%%:*}; n=${pair#*:}; mkdir -p "${tag}_${n}"
  curl -s "https://www.web-of-life.es/get_networks.php?network_name=$n"      -o "${tag}_${n}/edges.json"
  curl -s "https://www.web-of-life.es/get_network_info.php?network_name=$n"  -o "${tag}_${n}/network_info.csv"
  curl -s "https://www.web-of-life.es/get_species_info.php?network_name=$n"  -o "${tag}_${n}/node_taxonomy.csv"
done
```
