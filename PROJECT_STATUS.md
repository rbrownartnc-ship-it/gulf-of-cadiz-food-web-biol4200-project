# Project status

Last updated 2026-11-17. Summaries of every analysis are in [`notes/`](notes/README.md). Due dates follow Canvas, as several of them differ from the syllabus.

## Milestones

| Milestone | Due (Eastern) | Status |
|---|---|---|
| Project proposal | Thu 10/1 | ✅ submitted |
| First draft: introduction | Tue 10/13 | ✅ submitted |
| First draft: methods, public repo, data availability | Tue 10/27 | ✅ submitted |
| First draft: results | Thu 11/12 | ✅ submitted |
| First draft: title, abstract, discussion | Tue 11/17, 11:59 PM | ⬜ |
| Peer feedback on another group's draft | Tue 11/24, 11:59 PM | ⬜ individual |
| In-class presentation (20 min + 5 min Q&A), slides PDF | Thu 12/3, 1:30 PM | ⬜ |
| Revised draft (final paper) | Tue 12/8, 11:59 PM | ⬜ |

## The three webs

All three webs are Ecopath diet matrices from Web of Life, so the same methods apply to each.

| Network | Site | Groups | Links | Nodes are |
|---|---|---|---|---|
| `FW_005` | Gulf of Cadiz | 43 | 411 | functional groups |
| `FW_003` | Angolan shelf | 28 | 127 | mostly groups |
| `FW_016_01` | Mondego estuary | 36 | 240 | mostly species (28 of them) |

- The Mondego estuary has no top predators (its highest trophic level is 3.04), and it is the only web where total degree increases with trophic level.
- The taxonomic categories (fishes, invertebrates, etc.) were hand-coded for the Gulf of Cadiz only, so comparisons between webs use the trophic-level bands instead.
- ⬜ The differences in harvesting between the three sites still need to be taken from the source papers (Torres et al. 2013, Angelini & Velho 2011, Baeta et al. 2011).

## What the tests change in the results draft

- In the Gulf of Cadiz, removing the groups with the most links first does not differ from a random removal order under either extinction rule (p = 0.11 with all prey lost and 0.71 with half of diet lost). Its R50 of 0.44 was bold in our R50 table, as the table only counted random orders with a strictly lower R50 (1.1%). However, 21.7% of random orders have exactly the same R50 of 0.44. The table in `node_removal_results` now counts ties as well, so 0.44 is no longer bold, and the text and caption in the draft need the same change.
- Similarly, removing the groups with the highest betweenness first does not differ from random in the Gulf of Cadiz (p = 0.19 and 0.60).
- In contrast, removing the lowest trophic levels first and the most important prey first both differ from random under both rules (p = 0.002).
- Removing the highest trophic levels first causes no secondary extinctions in any of the three webs.
- The correlations with trophic level do not differ between the three webs for number of prey, effective number of prey or number of predators. For total degree and betweenness, only the Mondego estuary differs from the other two.
- Link removal has not been tested against random orders yet, so the L50 values are only compared with the 95% range of the random orders.

## Feedback

Proposal (10/4):

- [ ] Weighted, directed networks. The methods need to state how each measure handles weights and direction. The code already handles weights and direction ([`code/README.md`](code/README.md)), but the methods text does not explain how.
- [x] Other ecosystems. Done (see above).
- [ ] Robustness with an equilibrium model (Kondoh 2003, *Science* 299:1388, https://doi.org/10.1126/science.1079154). The structural robustness analysis is done (notes 05 and 06), but the dynamic model is not. Since our extinction rule only works bottom-up, it cannot show top-down effects, and the paper should state this.
- [x] Centrality beyond degree. Ten centralities were calculated, each against trophic level.

Methods draft (11/8):

- [ ] Section II.B should be framed in network terms only: what a functional group is, how the representation changes, and the `Import` row and column, in the main text.
- [ ] Visualization should be kept separate from structure. For example, "directed edges, represented with arrows in Fig. 1", and the same for node size, link thickness and color.
- [ ] Each methods subsection should explain why the method is used before describing it.
- [ ] A summary paragraph should come before the Data subsection.
- [ ] Total degree needs a definition (in-degree + out-degree, unweighted, without self-loops).
- [ ] The explainer figure needs one caption, the LaTeX one. The figure in the repo now has four panels, while the Overleaf caption still describes panels A to G.
- [x] A scatterplot with a regression line. These are the `compare_<web>_tl_vs_*` figures in `figures/08_comparison/`.

## Open decisions

- [ ] Edge direction. The code and the data use prey → predator, but Section II.A of the draft says the source node is the predator.
- [ ] Which "connectedness" the paper means: number of prey (ρ = +0.75), number of predators (−0.65) or total degree (−0.07). All three are calculated over the 40 consumers, which is the n to report.
- [ ] Whether Detritus and Discard stay as nodes (they currently do).
- [ ] "Predators consume prey but not vice versa." In the data, 23 of the 43 groups are part of feeding loops.
- [ ] Which extinction rule the paper leads with, all prey lost or half of diet lost. Both are calculated.
- [ ] Which robustness results answer research question 1: the guild removals, the removal orders, or both.

## Fixes for the revised introduction

- [ ] Ref [7]: the DOI 10.1371/journal.pone.0019374 belongs to Gravel, Canard, Guichard & Mouquet (2011), *PLoS ONE* 6(5): e19374, not Rooney, McCann & Moore 2012.
- [ ] Ref [8]: Gilbert, *Ecological Indicators* 9:72–80 was published in 2009.

## Figures

[`figures/README.md`](figures/README.md) lists the six figures in the results draft and where the intervals and tests for each one are.
