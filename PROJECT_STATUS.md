# Project status

Last updated 2026-11-16. The numbers for every analysis are in [`notes/`](notes/README.md). Canvas dates are the ones to go by, as the syllabus dates differ for several milestones.

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

All three are Ecopath diet-composition matrices from Web of Life, so the same methods apply to each.

| Network | Site | Groups | Links | Nodes are |
|---|---|---|---|---|
| `FW_005` | Gulf of Cadiz | 43 | 411 | functional groups |
| `FW_003` | Angolan shelf | 28 | 127 | mostly groups |
| `FW_016_01` | Mondego estuary | 36 | 240 | mostly species (28 of them) |

- Mondego has no top predators (maximum trophic level 3.04), and it is the one web where total degree rises with trophic level.
- The taxonomic categories (fishes, invertebrates and so on) are hand-coded for the Gulf of Cadiz only. Between webs, we use the trophic-level bands.
- ⬜ We still need the differing harvesting between the sites from the three source papers (Torres et al. 2013, Angelini & Velho 2011, Baeta et al. 2011), as the code cannot tell us that.

## What the tests change in the results draft

- Removing the groups with the most links first is not distinguishable from random order in the Gulf of Cadiz under either rule (p = 0.11 with all prey lost, 0.71 with half of diet lost). Its R50 of 0.44 is bold in our R50 table, though, as that table only counts the random orders strictly below it (1.1%), and 21.7% of random orders tie with it exactly.
- Highest betweenness first is not different from random in Cadiz either (p = 0.19 and 0.60).
- Lowest trophic level first and most important prey first are different from random in Cadiz under both rules (p = 0.002).
- Highest trophic level first causes no secondary extinctions in any of the three webs.
- The correlations with trophic level do not differ between the three webs for number of prey, effective number of prey or number of predators. Total degree and betweenness only differ for Mondego.
- Unfortunately, link removal has not had the same treatment yet, so the L50 numbers only have the random-order range behind them.

## Feedback

Proposal (10/4):

- [ ] **Weighted, directed networks.** We need to state how each method is extended to weights and direction. The code is done ([`code/README.md`](code/README.md)), but the methods text is not.
- [x] **Other ecosystems.** Done, see above.
- [ ] **Robustness with an equilibrium model** (Kondoh 2003, *Science* 299:1388, https://doi.org/10.1126/science.1079154). The structural part is done (notes 05 and 06), but the dynamic model is not. Our structural rule only works bottom-up, so it cannot show a top-down effect, and we should say so in the paper.
- [x] **Centrality beyond degree.** Ten centralities, each against trophic level.

Methods draft (11/8):

- [ ] **Section II.B.** Frame it in network terms only: what a functional group is, how the representation changes, and the `Import` row and column in the main text.
- [ ] **Visualization is not structure.** "Directed edges, represented with arrows in Fig. 1", and the same for node size, thickness and color.
- [ ] **Why first, then the method**, in each methods subsection.
- [ ] **A summary paragraph before the Data subsection.**
- [ ] **Define total degree.** It is in-degree + out-degree, unweighted, self-loops excluded.
- [ ] **One caption for the explainer figure, the LaTeX one.** The folder now holds the four-panel version, while our Overleaf caption still describes panels A to G.
- [x] **A scatterplot with a regression line.** The `compare_fit_*` figures.

## Open decisions

- [ ] **Edge direction.** The code and the data use prey → predator. Section II.A of our draft says the source node is the predator.
- [ ] **Which "connectedness"?** Number of prey (ρ = +0.75), number of predators (−0.65) or total degree (−0.07). All are over the 40 consumers, which is the n we should quote.
- [ ] **Detritus and Discard as nodes?** We keep them now.
- [ ] **"Predators consume prey but not vice versa."** In the data, 23 of 43 groups sit in feeding loops.
- [ ] **Which extinction rule leads:** all prey lost, or half of the diet lost. Both are computed.
- [ ] **Which robustness numbers answer research question 1:** the guild removals, the removal orders, or both.

## Fixes for the revised introduction

- [ ] Ref [7]: the DOI 10.1371/journal.pone.0019374 is Gravel, Canard, Guichard & Mouquet (2011), *PLoS ONE* 6(5): e19374, not Rooney, McCann & Moore 2012.
- [ ] Ref [8]: Gilbert, *Ecological Indicators* 9:72–80 is dated 2009.

## Figures

[`figures/README.md`](figures/README.md) lists the six figures our results draft uses and where the intervals and tests for each one are.
