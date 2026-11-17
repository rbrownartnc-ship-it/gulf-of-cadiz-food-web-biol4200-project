# Analysis notes

Each note is a written summary of one analysis. It gives the results, the values that support them, and the limits of the analysis. Each note has the same number as its figure folder. For example, note 05 goes with `figures/05_node_removal/`. There is no note 07 or 09, because those folders contain only the explainer figure and the connectivity panels. [`output/`](../output/README.md) contains the full tables, and [`code/README.md`](../code/README.md) gives the methods, equations and references.

| Note | Contents |
|---|---|
| [01 The web](01_web.md) | data, cleaning steps, the cleaned network and trophic levels |
| [02 Distributions](02_distributions.md) | degree, link strength, trophic level, clustering and other distributions |
| [03 Structure](03_structure.md) | whole-web measures compared with random, degree-preserving and niche-model webs |
| [04 Centrality](04_centrality.md) | ten centralities and their relation to trophic level |
| [05 Node removal](05_node_removal.md) | knockouts, guild removals, R50 by removal order and fragmentation |
| [06 Link removal](06_link_removal.md) | link knockouts, L50 by cut order and fragmentation |
| [08 Comparison with other ecosystems](08_comparison.md) | the Gulf of Cadiz compared with the Angolan shelf and the Mondego estuary: food webs, baseline statistics, the same measurements, and intervals and tests |

We write the notes by hand. The code does not update them. If a new run changes a result, the tables in `output/` are correct, and the note must be updated by hand.
