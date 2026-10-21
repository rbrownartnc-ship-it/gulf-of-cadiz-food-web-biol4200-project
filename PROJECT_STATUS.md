# Project status

Last updated 2026-10-21. Canvas dates are authoritative; the syllabus dates differ for several milestones. One person uploads each group milestone to Canvas for all four of us.

## Milestones

| Milestone | Due (Eastern) | Status |
|---|---|---|
| Project proposal | Thu 10/1 | ✅ submitted 9/30 · [`manuscript/`](manuscript/) |
| First draft: introduction | Tue 10/13 | ✅ submitted 10/13 · feedback pending |
| **First draft: methods** + public repo + data availability | **Tue 10/27, 11:59 PM** | ⬜ |
| First draft: results | Tue 11/10, 11:59 PM | ⬜ |
| First draft: title, abstract, discussion | Tue 11/17, 11:59 PM | ⬜ |
| Peer feedback on another group's draft | Tue 11/24, 11:59 PM | ⬜ individual |
| In-class presentation (20 min + 5 min Q&A), slides PDF | Thu 12/3, 1:30 PM | ⬜ |
| Revised draft (final paper) | Tue 12/8, 11:59 PM | ⬜ |

## Instructor feedback on the proposal (10/4): must be addressed in the first draft

- [ ] **Weighted, directed networks.** State how each standard method we use is extended to weights and direction.
  - 🟡 Code done: weighted and directed clustering, weighted betweenness, out-strength, and a weighted extinction rule (dies after losing a set share of its diet). See [`code/README.md`](code/README.md). The methods text is still to write.
- [ ] **Other ecosystems.** Do the conclusions hold for other marine food webs in Web of Life? If they don't, what is the plausible explanation? Also compare global properties (density, centralization) across webs.
  - ⬜ Not started. The analysis code is written so it can be pointed at another web.
- [ ] **Robustness, as a third aim.** Remove a fraction of nodes or links and look at what happens to the system's equilibrium. Suggested model: Kondoh 2003, *Science* 299:1388, https://doi.org/10.1126/science.1079154
  - 🟡 Structural part done: knockouts, guild removals, removal sequences with secondary extinctions (R50), giant component. See [`code/robustness.py`](code/robustness.py).
  - ⬜ The **equilibrium (dynamic) model Landry asked for is not done.** The structural rule is bottom-up only, so removing a predator never causes an extinction there. A dynamic model is what can show top-down effects.
- [ ] **Centrality beyond degree.** Betweenness and other measures, each correlated with trophic level. Generalize degree and clustering accordingly.
  - 🟡 Code done: 10 centralities, each correlated with trophic level ([`output/cadiz_centrality_vs_tl.csv`](output/cadiz_centrality_vs_tl.csv), figure `cadiz_centrality_vs_tl`).
- [ ] Reading suggestion: Jennifer Dunne's food-web papers (e.g. Dunne, Williams & Martinez 2004, *MEPS* 273:291, which is already ref [5]).

## Methods draft checklist (from the rubric, 14 pts)

- [ ] 2–3 pages: overall workflow · dataset · preprocessing · network representation · analyses · why each analysis
- [ ] Citations for the methods; equations where needed
- [ ] **Explainer figure** with a full caption, referenced in the text with `\ref{}`
- [ ] Data availability section linking this repo: https://github.com/rbrownartnc-ship-it/gulf-of-cadiz-food-web-biol4200-project (template text is in the guideline PDF)
- [x] This repo public, code in `code/`, every README updated, renamed to lowercase-with-dashes (done 10/20)
- [ ] Course article template; PDF submitted

## Open decisions for the group

- [ ] **Edge direction.** The code uses **prey → predator** (energy flow). The proposal's dataset section described predator → prey ("shark → tuna"). Pick one, and state it in the methods.
- [ ] **Which "connectedness"?** Trophic level vs number of prey: ρ = +0.75. Vs number of predators: ρ = −0.65. Vs total degree: ρ = −0.07 ([`output/rq_feasibility.txt`](output/rq_feasibility.txt)). The hypothesis needs to name one.
- [ ] Keep **Detritus and Discard** as nodes? (They are kept now. Dropping them still leaves the web connected.)
- [ ] **"Predators consume prey but not vice versa"** (proposal methods). In the data, 23 of 43 groups sit in feeding loops (`in_feeding_loop` in `output/cadiz_node_traits.csv`).
- [ ] **Extinction rule for the robustness results.** The options are "dies when all prey are gone" (topological, as in Dunne et al. 2002) or "dies when half its diet is gone" (weighted). Both are computed, and R50 is also reported at 1/4 and 3/4 of the diet as a sensitivity check. Decide which one leads in the paper.
- [ ] **Which robustness numbers answer research question 1** ("does community composition shape persistence?"): the guild removals ([`output/cadiz_guild_removal.csv`](output/cadiz_guild_removal.csv)), the removal orders, or both?
- [ ] **Comparison webs.** Candidates on Web of Life with the same data type (Ecopath diet fractions):
  - FW_006, Alvarado lagoon, Gulf of Mexico: 30 groups, 229 links
  - FW_007, St Marks seagrass, Florida: 48, 221
  - FW_016_01, Mondego estuary, Portugal: 37, 242

  Coral-reef gut-content webs (FW_017_01 to _06, 120–217 nodes) are a different data type. Freshwater webs (FW_001–004, 009, 010) could serve as an out-group.

## Fixes for the revised introduction

- [ ] Ref [7]: the DOI 10.1371/journal.pone.0019374 is **Gravel, Canard, Guichard & Mouquet (2011), *PLoS ONE* 6(5): e19374**, not Rooney, McCann & Moore 2012.
- [ ] Ref [8]: Gilbert, *Ecological Indicators* 9:72–80 is dated **2009**.
- [ ] Data availability: add the link to this repository (https://github.com/rbrownartnc-ship-it/gulf-of-cadiz-food-web-biol4200-project).

## Done so far (data and code)

- Dataset downloaded and verified: 44 × 44 matrix, 413 links; group names checked against the Web of Life API.
- Cleaned: `Import` removed → 43 groups, 411 links, 14 cannibalistic self-loops, no isolates, 1 weakly connected component. Every step is in [`output/cadiz_cleaning_log.csv`](output/cadiz_cleaning_log.csv).
- Trophic level, omnivory index, degree, diet diversity and more for every group: [`output/cadiz_node_traits.csv`](output/cadiz_node_traits.csv), or the `node_traits` sheet of [`output/cadiz_foodweb_data.xlsx`](output/cadiz_foodweb_data.xlsx).
- Figures: food web by trophic level, and the diet-matrix heatmap. They are print-ready at 7 in wide, with a PDF for LaTeX and a PNG for Word. See [`figures/README.md`](figures/README.md).
- Network analyses (10/21), in code, tables and figures:
  - Whole-web structure: components, clustering, path length, trophic coherence, against three null models
  - Centralities against trophic level
  - Single and guild removals
  - Removal sequences with secondary extinctions (R50)
  - Giant component under removal

  All verified against independent implementations; see [`code/README.md`](code/README.md). Every table is also in [`output/cadiz_analysis_results.xlsx`](output/cadiz_analysis_results.xlsx).
