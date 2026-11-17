# Project status

Last updated 2026-11-17. The summaries of all analyses are in [`notes/`](notes/README.md). Use the Canvas due dates, because some of them are different from the syllabus.

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

All three webs are Ecopath diet matrices from Web of Life. Thus, the same methods apply to each web.

| Network | Site | Groups | Links | Nodes are |
|---|---|---|---|---|
| `FW_005` | Gulf of Cadiz | 43 | 411 | functional groups |
| `FW_003` | Angolan shelf | 28 | 127 | mostly groups |
| `FW_016_01` | Mondego estuary | 36 | 240 | mostly species (28 of them) |

- The Mondego estuary has no top predators. Its highest trophic level is 3.04. It is the only web where total degree increases with trophic level.
- We assigned taxonomic categories (fishes, invertebrates and others) only for the Gulf of Cadiz. Comparisons between webs use trophic-level bands.
- ⬜ We must get the differences in harvesting between the sites from the three source papers (Torres et al. 2013, Angelini & Velho 2011, Baeta et al. 2011).

## Changes to the results draft from the tests

- In the Gulf of Cadiz, removal of the groups with the most links first is not different from random order. This is true under both extinction rules (p = 0.11 for all prey lost, p = 0.71 for half of diet lost).
- Our R50 table showed this R50 (0.44) in bold, because the table counted only random orders with a lower R50 (1.1%). But 21.7% of random orders have the same R50. The table in `node_removal_results` now counts these ties, so 0.44 is not bold. The text and caption in the draft must also change.
- Removal of the groups with the highest betweenness first is also not different from random (p = 0.19 and 0.60).
- Removal of the lowest trophic levels first and of the most important prey first is different from random under both rules (p = 0.002).
- Removal of the highest trophic levels first causes no secondary extinctions in any of the three webs.
- For number of prey, effective number of prey and number of predators, the correlation with trophic level is the same in the three webs. For total degree and betweenness, only the Mondego estuary is different.
- We did not yet test link removal against random orders. Thus, the L50 values have only the 95% range of the random orders for comparison.

## Feedback

Proposal (10/4):

- [ ] Weighted, directed networks. The methods text must show how each measure uses weights and direction. The code already does this ([`code/README.md`](code/README.md)).
- [x] Other ecosystems. Done (see above).
- [ ] Robustness with an equilibrium model (Kondoh 2003, *Science* 299:1388, https://doi.org/10.1126/science.1079154). The structural analysis is done (notes 05 and 06). The dynamic model is not done. Our extinction rule works only bottom-up, so it cannot show top-down effects. The paper must state this limit.
- [x] Centrality beyond degree. We calculated ten centralities and compared each with trophic level.

Methods draft (11/8):

- [ ] Write Section II.B in network terms only: what a functional group is, how the representation changes, and the `Import` row and column.
- [ ] Keep visualization separate from structure. For example: "directed edges, represented with arrows in Fig. 1". Do the same for node size, link width and color.
- [ ] In each methods subsection, give the reason for the method before the method.
- [ ] Add a summary paragraph before the Data subsection.
- [ ] Define total degree: in-degree plus out-degree, unweighted, without self-loops.
- [ ] Use one caption for the explainer figure (the LaTeX caption). The figure in the repo has four panels, but the Overleaf caption describes panels A to G.
- [x] A scatterplot with a regression line. See the `compare_<web>_tl_vs_*` figures in `figures/08_comparison/`.

## Open decisions

- [ ] Edge direction. The code and the data use prey → predator. Section II.A of the draft says that the source node is the predator.
- [ ] The meaning of "connectedness": number of prey (ρ = +0.75), number of predators (−0.65) or total degree (−0.07). All three use the 40 consumers. Report n = 40.
- [ ] Detritus and Discard as nodes. They are nodes now.
- [ ] "Predators consume prey but not vice versa." In the data, 23 of the 43 groups are in feeding loops.
- [ ] The main extinction rule: all prey lost or half of diet lost. The code calculates both.
- [ ] The robustness results for research question 1: the guild removals, the removal orders, or both.

## Fixes for the revised introduction

- [ ] Ref [7]: the DOI 10.1371/journal.pone.0019374 is Gravel, Canard, Guichard & Mouquet (2011), *PLoS ONE* 6(5): e19374, not Rooney, McCann & Moore 2012.
- [ ] Ref [8]: Gilbert, *Ecological Indicators* 9:72–80 is from 2009.

## Figures

[`figures/README.md`](figures/README.md) lists the six figures in the results draft. It also shows where to find the intervals and tests for each figure.
