# Project status

Last updated 2026-11-17. The numbers for every analysis are in [`notes/`](notes/README.md). The Canvas due dates are the ones to go by, as several of them differ from the syllabus.

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

All three are Ecopath diet matrices from Web of Life, so the same methods work for each of them.

| Network | Site | Groups | Links | Nodes are |
|---|---|---|---|---|
| `FW_005` | Gulf of Cadiz | 43 | 411 | functional groups |
| `FW_003` | Angolan shelf | 28 | 127 | mostly groups |
| `FW_016_01` | Mondego estuary | 36 | 240 | mostly species (28 of them) |

- The Mondego estuary has no top predators (its highest trophic level is 3.04), and it is the only web where total degree goes up with trophic level.
- We hand-coded the taxonomic categories (fishes, invertebrates, etc.) for the Gulf of Cadiz only, so between webs we use the trophic-level bands instead.
- ⬜ We still need the differences in harvesting between the sites, which have to come from the three source papers (Torres et al. 2013, Angelini & Velho 2011, Baeta et al. 2011).

## What the tests change in the results draft

- In the Gulf of Cadiz, removing the groups with the most links first is not different from a random order under either rule (p = 0.11 with all prey lost and 0.71 with half of diet lost). Its R50 of 0.44 was bold in our R50 table, as the table only counted random orders strictly below it (1.1%), but 21.7% of random orders tie with it exactly. The table in `node_removal_results` counts ties now, so 0.44 is no longer bold, and the text and caption in the draft need to change too.
- Removing the highest betweenness groups first is not different from random in the Gulf of Cadiz either (p = 0.19 and 0.60).
- Removing the lowest trophic level first and the most important prey first are different from random under both rules (p = 0.002).
- Removing the highest trophic level first causes no secondary extinctions in any of the three webs.
- The correlations with trophic level do not differ between the three webs for number of prey, effective number of prey or number of predators. Total degree and betweenness only differ for the Mondego estuary.
- Unfortunately, link removal has not been tested this way yet, so the L50 numbers only have the random-order range behind them.

## Feedback

Proposal (10/4):

- [ ] Weighted, directed networks. We need to say how each method handles weights and direction. The code does this ([`code/README.md`](code/README.md)), but the methods text does not yet.
- [x] Other ecosystems. Done (see above).
- [ ] Robustness with an equilibrium model (Kondoh 2003, *Science* 299:1388, https://doi.org/10.1126/science.1079154). We have the structural part (notes 05 and 06) but not the dynamic model. Our extinction rule only works bottom-up, so it cannot show a top-down effect, and the paper should say that.
- [x] Centrality beyond degree. We have ten centralities, each against trophic level.

Methods draft (11/8):

- [ ] Section II.B needs to be framed in network terms only: what a functional group is, how the representation changes, and the `Import` row and column in the main text.
- [ ] Visualization is not structure. For example, "directed edges, represented with arrows in Fig. 1", and the same for node size, thickness and color.
- [ ] Each methods subsection should give the why first, then the method.
- [ ] Add a summary paragraph before the Data subsection.
- [ ] Define total degree (in-degree + out-degree, unweighted, without self-loops).
- [ ] The explainer figure needs one caption, the LaTeX one. The figure in the repo has four panels now, but our Overleaf caption still describes panels A to G.
- [x] A scatterplot with a regression line. These are the `compare_<web>_tl_vs_*` figures in `figures/08_comparison/`.

## Open decisions

- [ ] Edge direction. The code and the data go prey → predator, but Section II.A of our draft says the source node is the predator.
- [ ] Which "connectedness" we mean: number of prey (ρ = +0.75), number of predators (−0.65) or total degree (−0.07). All three are over the 40 consumers, which is the n we should give.
- [ ] Whether Detritus and Discard stay as nodes (they do right now).
- [ ] "Predators consume prey but not vice versa." In the data, 23 of the 43 groups are part of feeding loops.
- [ ] Which extinction rule we lead with, all prey lost or half of diet lost. Both are computed.
- [ ] Which robustness numbers answer research question 1: the guild removals, the removal orders, or both.

## Fixes for the revised introduction

- [ ] Ref [7]: the DOI 10.1371/journal.pone.0019374 is Gravel, Canard, Guichard & Mouquet (2011), *PLoS ONE* 6(5): e19374, not Rooney, McCann & Moore 2012.
- [ ] Ref [8]: Gilbert, *Ecological Indicators* 9:72–80 is from 2009.

## Figures

[`figures/README.md`](figures/README.md) lists the six figures in our results draft and where the intervals and tests for each one are.
