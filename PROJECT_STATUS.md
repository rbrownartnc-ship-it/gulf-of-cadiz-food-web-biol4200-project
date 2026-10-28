# Project status

Last updated 2026-10-26. Bullet-point notes on every analysis are in [`notes/`](notes/README.md). Canvas dates are authoritative; the syllabus dates differ for several milestones. One person uploads each group milestone to Canvas for all four of us.

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
  - 🟡 Code done:
    - weighted and directed clustering, weighted betweenness, out-strength
    - a weighted extinction rule (dies after losing a set share of its diet)
    - link removal by link strength (strong vs weak) and by directed edge betweenness

    See [`code/README.md`](code/README.md). The methods text is still to write.
- [ ] **Other ecosystems.** Do the conclusions hold for other marine food webs in Web of Life? If they don't, what is the plausible explanation? Also compare global properties (density, centralization) across webs.
  - ⬜ Not started. The analysis code is written so it can be pointed at another web.
- [ ] **Robustness, as a third aim.** Remove a fraction of nodes or links and look at what happens to the system's equilibrium. Suggested model: Kondoh 2003, *Science* 299:1388, https://doi.org/10.1126/science.1079154
  - 🟡 Structural part done:
    - removing groups: knockouts, guild removals, targeted and recalculated attacks (R50), giant component. See [`notes/05_node_removal.md`](notes/05_node_removal.md).
    - cutting links: link knockouts, strong vs weak links, edge-betweenness attacks (L50), bond percolation. See [`notes/06_edge_removal.md`](notes/06_edge_removal.md).
  - ⬜ The **equilibrium (dynamic) model Landry asked for is not done.** The structural rule is bottom-up only, so removing a predator never causes an extinction there. A dynamic model is what can show top-down effects.
- [ ] **Centrality beyond degree.** Betweenness and other measures, each correlated with trophic level. Generalize degree and clustering accordingly.
  - 🟡 Code done: 10 centralities, each correlated with trophic level ([`output/cadiz_centrality_vs_tl.csv`](output/cadiz_centrality_vs_tl.csv), figure `cadiz_centrality_vs_tl`).
- [ ] Reading suggestion: Jennifer Dunne's food-web papers (e.g. Dunne, Williams & Martinez 2004, *MEPS* 273:291, which is already ref [5]).

## Methods draft checklist (from the rubric, 14 pts)

- [ ] 2–3 pages: overall workflow · dataset · preprocessing · network representation · analyses · why each analysis
- [ ] Citations for the methods; equations where needed
- [x] **Explainer figure** with a full caption — built and pushed, [`figures/07_explainer_figure/`](figures/07_explainer_figure/README.md), drawn by `code/explainer_figure.py`. Still to do in the document: insert it and reference it with `\ref{}`.
  - ✅ **n reconciled 2026-10-26.** Panel D now uses the **40 consumers** (ρ = +0.75 prey, −0.65 predators), matching [`output/cadiz_centrality_vs_tl.csv`](output/cadiz_centrality_vs_tl.csv) and paper figures 4–5. It previously used all 43 groups (+0.80, −0.60). Detritus, Discard and Phytoplankton have no prey and sit at trophic level 1 by definition, so they are tied at the bottom of both rankings and rank-concordant by construction — they inflate ρ for number of prey and flip total degree from −0.07 to +0.10 without adding information. **Quote n = 40 everywhere in the paper.**
- [x] Data availability section linking this repo: https://github.com/rbrownartnc-ship-it/gulf-of-cadiz-food-web-biol4200-project — LaTeX drafted 10/26 from Landry's template; cites Torres et al. (2013) and Web of Life, and carries the acknowledgement Web of Life requires. Still to paste into the document.
- [x] This repo public, code in `code/`, every README updated, renamed to lowercase-with-dashes (done 10/20)
- [ ] Course article template; PDF submitted

## Figures for the paper — decided 2026-10-26

Ten of the 52 figures, listed in order with the reason for each in
[`figures/README.md`](figures/README.md) and marked ★ in every folder README and in
[`notes/`](notes/README.md). The selection lives in `SELECTED` in
[`code/write_docs.py`](code/write_docs.py), so rerunning the pipeline keeps the marks. Each chosen
figure also carries a paragraph under its preview saying what it shows and why it is in; those live
in `EXPLAIN` in the same file.

| # | figure | section it serves |
|---|---|---|
| 1 | `01_web/cadiz_foodweb` | the system |
| 2 | `02_distributions/total_degree_histogram` | degree against the random-web expectation: no hubs |
| 3 | `02_distributions/link_strength_histogram` | most links are weak |
| 4 | `04_centrality/tl_vs_n_prey` | RQ: trophic level vs number of prey (ρ = +0.75) |
| 5 | `04_centrality/tl_vs_n_predators` | the opposing relation (ρ = −0.65) |
| 6 | `05_node_removal/single_group_knockouts` | which single groups matter |
| 7 | `05_node_removal/robustness_all_prey_rule_trophic_position` | targeted vs random, groups |
| 8 | `05_node_removal/r50_summary` | every removal order, both rules |
| 9 | `06_edge_removal/link_robustness_all_prey_rule_strength` | targeted vs random, links |
| 10 | `06_edge_removal/l50_summary` | every cutting order, both rules |

Figures 4 and 5 answer Landry's "centrality beyond degree" note directly, and together they
settle the open "which connectedness?" question below: total degree is flat (ρ = −0.07,
p = 0.67) only because number of prey and number of predators pull in opposite directions.

The methods explainer figure (`07_explainer_figure/`) is separate from these ten: it is a workflow
diagram the rubric requires, not a result. Its panel D already summarises the
centrality-vs-trophic-level correlations that figures 4 and 5 plot in full, and since 10/26 it uses
the same 40 consumers, so the numbers agree. If space is tight, figure 5 is the first one to cut.

Figures 8 and 10 were cut down on 10/26 to only the orders the paper argues from: R50 now shows
random, most connected first, highest betweenness first and most important prey first, and L50 shows
random, highest edge betweenness first and weakest links first. The trophic-level orders came out
because figure 7 is that comparison, strongest-links-first came out because figure 9 is that
comparison, and PageRank and the recalculated attacks came out as sensitivity checks. The choice is a
`SUMMARY_FIGURE_ORDERS` list in `code/node_removal.py` and `code/edge_removal.py`. **No data was
lost** — every order is still in `cadiz_node_robustness_summary.csv` and
`cadiz_link_robustness_summary.csv`.

Deliberately left out of the paper, kept in the repo: `03_structure/` (the null-model
comparison) and the other eight centrality panels. Worth reconsidering for the results draft
on 11/10, since the null models are also an answer to the proposal feedback.

## Open decisions for the group

- [ ] **Edge direction.** The code uses **prey → predator** (energy flow). The proposal's dataset section described predator → prey ("shark → tuna"). Pick one, and state it in the methods.
- [ ] **Which "connectedness"?** Trophic level vs number of prey: ρ = +0.75. Vs number of predators: ρ = −0.65. Vs total degree: ρ = −0.07 ([`output/rq_feasibility.txt`](output/rq_feasibility.txt)). The hypothesis needs to name one.
  - Settled in part on 10/26: all of these are over the **40 consumers**, and that is the n the paper quotes throughout. Paper figures 4 and 5 show the first two; total degree is flat only because they pull in opposite directions.
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
- Added 10/22:
  - histograms of every node and link property
  - recalculated (adaptive) targeted attacks
  - targeted link removal (strongest / weakest, edge betweenness, bottom-up / top-down) with L50 and bond percolation
  - critical single links
  - 52 single-panel figures in six folders, all at print size
  - bullet-point [`notes/`](notes/README.md), generated from the results
  - the verification scripts in [`code/checks/`](code/checks/)

  Everything reruns with `python code/run_all.py`.
