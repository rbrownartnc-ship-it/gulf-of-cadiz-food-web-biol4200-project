# Project status

Last updated 2026-11-11. Bullet-point notes on every analysis are in [`notes/`](notes/README.md). Canvas dates are authoritative; the syllabus dates differ for several milestones. One person uploads each group milestone to Canvas for all four of us.

## Milestones

| Milestone | Due (Eastern) | Status |
|---|---|---|
| Project proposal | Thu 10/1 | ✅ submitted 9/30 · [`manuscript/`](manuscript/) |
| First draft: introduction | Tue 10/13 | ✅ 13/14 completion · 6.5/8 quality · graded 11/2 |
| **First draft: methods** + public repo + data availability | Tue 10/27 | ✅ 13/14 completion · 6/8 quality · graded 11/8 |
| **First draft: results** | **Thu 11/12, 11:59 PM** (Canvas; the table said 11/10) | ⬜ |
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
- [x] **Other ecosystems.** Do the conclusions hold for other marine food webs in Web of Life? If they don't, what is the plausible explanation? Also compare global properties (density, centralization) across webs.
  - ✅ **Done 2026-11-11**, [`code/compare_webs.py`](code/compare_webs.py) → [`notes/07_cross_ecosystem.md`](notes/07_cross_ecosystem.md), five figures in [`figures/08_comparison/`](figures/08_comparison/README.md). Four other Ecopath webs: Angolan shelf (FW_003), Alvarado lagoon (FW_006), St Marks seagrass (FW_007), Mondego estuary (FW_016_01).
  - **The conclusions hold.** Number of prey and diet diversity rise with trophic level in all five webs (ρ +0.52 to +0.82, all p < 0.05); number of predators falls in all five (−0.36 to −0.65); total degree is flat in four of five because the two cancel. Top-down removal causes no secondary extinctions anywhere; bottom-up and most-important-prey-first are the most damaging everywhere; cutting the strongest links first is devastating under the half-diet rule (L50 0.01–0.10) while cutting the weakest barely matters (0.62–0.94).
  - **One exception, and it is explainable.** The Mondego estuary web is species-level benthic invertebrates with **no top predators at all** (max trophic level 3.04, no fish or birds). There total degree rises with trophic level (+0.70) and clustering falls (−0.49), unlike the four functional-group webs.
  - **Where Cadiz sits:** highest connectance (0.222 vs 0.096–0.254) and link density (9.56 vs 4.54–7.63) of the five; clustering 0.571, the highest; trophic coherence q 0.786, second to Alvarado's 0.895; degree centralization 0.403, mid-range.
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
- [x] **Comparison webs.** Settled 2026-11-11: FW_003 Angolan shelf (28 groups, 127 links), FW_006 Alvarado lagoon (30, 229), FW_007 St Marks seagrass (48, 221), FW_016_01 Mondego estuary (36, 240) — all Ecopath diet fractions, all run through [`code/compare_webs.py`](code/compare_webs.py).
  - FW_008 (Caribbean, Bascompte et al. 2005, 249 species) was considered and rejected: its diet columns sum to between 0.05 and 1.83, so the weights are not comparable.
  - Coral-reef gut-content webs (FW_017_01 to _06, 120–217 nodes) are still a different data type. Freshwater webs (FW_001–004, 009, 010) remain available as an out-group if one is wanted.
- [ ] **How much of the comparison goes in the paper.** Decided on the 11/11 call: the comparison is for the **final draft**, not the 11/12 results draft. One figure (`compare_centrality_vs_tl`, full width) plus the global-structure table would carry it.

## Instructor feedback on the methods draft (11/8): 13/14 completion, 6/8 quality

> "Overall, this is starting to come together nicely! I enjoyed reading this. You should be commended for the quality of your corresponding repository. My main comments are to tighten up the language and make it more precise and some organizational suggestions. Also, take another look at your proposal comments."

- [x] **"Apply your methods [to] at least one other ecosystem to compare and contrast."** Done — see the cross-ecosystem item above.
- [ ] **Section II.B was the one rubric row that scored 0.** "I had a hard time reading II.B. I think that this should be framed solely in terms of network terminology. After reading this section, I still was unclear what functional groups were, and how you were changing the network representation so that nodes are no longer species but functional groups. I would reiterate the point about the 'import' row/column in the main text."
- [ ] **Visualization is not structure.** "Instead of 'arrows' I would say 'directed edges, represented with arrows in Fig. 1'. Same thing with node size, thickness, color, etc."
- [ ] **Reorganize each methods subsection: why first, then the method.** "I would reorganize the contents of the methods subsections so you start with the WHY? and then follow with the method that will help you answer the question, rather than the other way around."
- [ ] **Add a summary paragraph before the Data subsection** laying out what we will do and why.
- [ ] **Define total degree.** "What is 'total degree'? Is it different than just 'degree'? Are you including the weights in the degree calculation?" (It is in-degree + out-degree, unweighted, self-loops excluded — `n_prey + n_predators` in `output/cadiz_node_traits.csv`.)
- [ ] **Explainer figure: one caption, the LaTeX one.** "Can you combine the captions? It looks weird to have two separate captions. Use the LaTeX caption, not the embedded version."
- [ ] **Consider a scatterplot with a regression line** to complement the rank-based (Spearman) approach.

## Cross-ecosystem comparison: where the webs come from, and what is still missing

### Same source as the Gulf of Cadiz — the whole catalogue, checked 2026-11-12

Yes. All of them are Web of Life networks, from the same collection FW_005 came from
(<https://www.web-of-life.es/map.php?type=7>, "Food Webs"). The site serves them as CSV matrices;
the API (`get_networks.php`) serves the same values as an edge list. The two agree: the Gulf of
Cadiz web rebuilt from the API reproduces `output/cadiz_diet_matrix_culled.csv` exactly, which is
the control `code/compare_webs.py` runs before it reports anything.

**Web of Life holds 330 networks, 39 of them food webs.** Only some can be compared with ours:

| Networks | Cell value | Usable with our methods? |
|---|---|---|
| FW_001–FW_010, FW_016_01 | relative frequency of prey in each predator's diet (Ecopath) | ✅ yes — identical quantity to FW_005 |
| FW_011, FW_012_0*, FW_013_0*, FW_014_0*, FW_015_0* (15 webs) | — (`is_weighted = 0`) | ❌ binary presence/absence only. Every weighted method we use (diet-share weights, the half-diet extinction rule, strong-vs-weak link removal, weighted betweenness) is undefined on them. |
| FW_017, FW_017_01–_06 | standardized frequency of prey in gut content | ❌ different measurement (coral-reef gut content, Pozas-Schacre 2021), not a diet-composition matrix |
| FW_012, FW_013, FW_014, FW_016, FW_017 | — | ❌ umbrella entries, not networks. `get_networks.php?network_name=FW_016` returns an empty set; FW_016_01 is the only Mondego network. |

**The four we use, and why they and not the others:**

| Network | Site | Groups | Links | Why |
|---|---|---|---|---|
| FW_003 | Angolan shelf | 28 | 127 | marine, Ecopath, different ocean basin |
| FW_006 | Alvarado lagoon, Gulf of Mexico | 30 | 229 | marine/estuarine lagoon, closest in size to Cadiz |
| FW_007 | St Marks seagrass, Florida | 48 | 221 | marine seagrass, larger than Cadiz and much sparser |
| FW_016_01 | Mondego estuary, Portugal | 36 | 240 | estuarine, and species-level rather than functional groups |

**Rejected, with reasons:** FW_008 (Caribbean, Bascompte et al. 2005, 249 species) — diet columns
sum to between 0.05 and 1.83, so the weights are not comparable. FW_001 (Paraná floodplain, 40),
FW_002 (Cerrado river, 14), FW_004 (Itaipu reservoir, 32), FW_009 and FW_010 (Pantanal oxbow
lakes, 40 and 39) — all **freshwater**, so they are an out-group rather than a like-for-like
comparison. All five are clean (diets sum to 1, `Import` handled by the existing rule, no short
diets) and would drop into the pipeline unchanged if the group wants an out-group.

### Processing each web needs

Everything below is already implemented in `code/compare_webs.py`; this is the list of what the
data actually required, not a to-do list.

| Step | Cadiz | Angola | Alvarado | St Marks | Mondego |
|---|---|---|---|---|---|
| drop the Ecopath boundary row after checking it eats nothing | `Import` | none | none | none | `Imports` |
| rescale percent → fraction | no | no | no | **÷ 100** | no |
| rescale short diets to sum to 1 | 2 (Import removed) | none | none | **9 diets, as low as 0.065** | 2 (Imports removed) |
| keep detritus / discards as nodes | Detritus, Discard | Detritus | Detritus | Detritus | Detritus |
| keep cannibalism and weak links | yes | yes | yes | yes | yes |

Two things do **not** transfer and are worth saying out loud in the paper:

- **The taxonomic categories are Cadiz-only.** `build_network.py` hand-codes every group as
  fishes / invertebrates & plankton / mammals-birds-turtles / non-living. The other webs have no
  such column, so any guild comparison has to use **trophic-level bands and the basal/top roles**,
  which are computed from the data and do transfer.
- **Node resolution differs, and Web of Life says so itself.** Its `taxonomic resolution` field:
  Alvarado 30/30 "Group", St Marks 47/48 "Group", Angola 15 Group + 6 Genus + 5 Family + 2
  Species, **Mondego 28 Species + 2 Genus + 1 Subclass + 6 Group**. That is independent
  confirmation that Mondego is the odd one out — and it is the one web where our conclusions
  break, which is the explanation Landry asked for.

### Which analyses the comparison still lacks

`compare_webs.py` currently runs: cleaning, node traits, **the full descriptive layer
(`distributions.py`'s table of every node and link property, plus the named extremes)**,
whole-web structure, degree centralization, ten centralities vs trophic level, R50 for seven
removal orders under two rules, and L50 for three link orders under two rules. The Cadiz pipeline
does more than that. The gap, most useful first:

- [ ] **1. Null models per web (ER, degree-preserving, niche).** The biggest one. Right now the
  table says Cadiz clustering 0.571 vs St Marks 0.284 — but clustering depends on size and
  connectance, so that difference may be nothing but St Marks being sparser. Without a null we
  cannot say any web is *more clustered than it should be*. `network_structure.py` already does
  this for Cadiz (1000 ER, 300 rewired, 1000 niche) in 33 s; the other four are smaller, so about
  +90 s.
- [x] **2. Guild removals per web, using trophic-level bands.** ✅ **done 2026-11-12** — and the
  claim holds everywhere. See below.
- [x] **3. Single-group knockouts per web.** ✅ **done 2026-11-12**. See below.
- [ ] **4. Extinction-rule sensitivity (θ = 3/4 and 1/4).** Cadiz reports four thresholds; the
  comparison reports two. Cheap, and it is the honest answer to "does the conclusion depend on the
  rule?" +60 s.
- [ ] **5. Recalculated (adaptive) attacks.** Cadiz has most-connected and highest-betweenness
  re-ranked after every removal (Holme et al. 2002), and recalculated edge betweenness for links.
  The comparison uses static orders only. +60 s.
- [x] **6. Giant component / fragmentation per web.** ✅ **done 2026-11-12**. See below.
- [ ] **7. Scatterplots with regression lines.** Landry's suggestion on the methods draft, and it
  applies to the comparison figure too, not just to Cadiz.
- [x] ~~per-web degree distributions against the random expectation~~ — **done 2026-11-12**, see
  the descriptive layer below.
- [ ] **8. Lower priority:** single-link knockouts, critical links and bond percolation per web;
  the two extra link orders (links from lowest-TL prey, links into highest-TL predators); an
  igraph cross-check of the comparison webs (the Cadiz control covers the shared code, but not
  the per-web numbers).

### The descriptive layer — added 2026-11-12

`output/compare_webs_distributions.csv` and `compare_webs_extremes.csv`, five new figures, and two
new sections in `notes/07_cross_ecosystem.md`. Verified: 110 distribution statistics for the Gulf
of Cadiz agree with `distributions.py`'s own table to 2.8e-4 (not exactly, because that script
reads node traits back from a CSV rounded to 3–4 dp).

What it shows, beyond the correlations:

- **Diet concentration separates the webs cleanly.** Median share of a consumer's diet carried by
  its single largest prey: Cadiz 0.39, Angola 0.31, Alvarado 0.39 — but **St Marks 0.58 and
  Mondego 0.68**. The webs where our trophic-level correlations are weakest are the webs where a
  typical consumer eats mostly one thing.
- **Degrees are far more uneven than random in every web.** Variance/mean for number of prey runs
  1.58 (Angola) to 11.13 (Mondego), against 0.75–0.90 for a random web of the same size and
  density. Cadiz is 4.98. This is the one distributional statement that is safe to make without a
  null-model ensemble, because the random expectation is analytic.
- **A trophic-level ladder:** mean trophic level Cadiz 3.14 > Angola 2.90 > Alvarado 2.62 >
  St Marks 2.47 > Mondego 2.04; maxima 4.84 / 4.32 / 3.62 / 4.32 / 3.04.
- **Detritus is the single most important prey in four of the five webs** (summed diet share:
  Cadiz 5.13, Angola 5.50, St Marks 5.43, **Mondego 18.05** — eaten by 30 of its 36 groups).
  Alvarado is the exception: Wigeongrass, 5.73.
- **Cadiz has the most diverse diets** (mean effective prey 5.26, max 13.30 for Sharks) and the
  weakest typical link (median 0.037, against 0.175 in Angola) — many weak links rather than a few
  strong ones.
- **Top predators:** St Marks 9, Cadiz 6, Angola 4, Alvarado 1, **Mondego 0**. Basal groups:
  St Marks 6, Mondego 5, Cadiz 3, Alvarado 3, Angola 2.

### Basic network structure + removal analyses — added 2026-11-12

`output/compare_webs_knockouts.csv`, `compare_webs_guild_removal.csv`, fragmentation columns in
`compare_webs_robustness.csv`, three new figures, four new sections in the note. Verified against
the Cadiz outputs: all 43 single knockouts, 4 guild removals and 21 fragmentation points agree
exactly.

**⚠️ The high clustering is mostly density, and this corrects an earlier reading.** These webs are
dense, so a random graph of the same density already clusters heavily. Observed vs that baseline:

| | Cadiz | Angola | Alvarado | St Marks | Mondego |
|---|---|---|---|---|---|
| clustering | 0.571 | 0.357 | 0.539 | 0.284 | 0.562 |
| random web, same density | 0.425 | 0.328 | 0.485 | 0.193 | 0.354 |
| ratio | ×1.34 | ×1.09 | ×1.11 | ×1.47 | ×1.59 |
| small-world σ | 1.10 | 0.93 | 0.94 | 1.23 | 1.35 |

So "Cadiz is the most clustered of the five" is true of the raw number but nearly all of the gap to
St Marks is density. **None of the five is strongly small-world** (σ ≈ 1). Note this analytic
baseline (clustering = density) gives 0.425 for Cadiz while the simulated ER ensemble in
`cadiz_structure_vs_null.csv` gives 0.39, because the two count directed and undirected edges
differently — the simulated ensemble is the better test, so gap #1 still stands.

**Other basic structure:** every web is a single connected component. **Angola and St Marks have no
feeding loops at all** (reciprocity 0, largest loop 1), against Cadiz 23, Alvarado 14, Mondego 9.
Mean undirected degree Cadiz 17.9 > Alvarado 14.1 > Mondego 12.4 > St Marks 9.1 > Angola 8.9.
Diameter 3 everywhere except St Marks (4). All disassortative except St Marks (+0.11); Mondego
strongly so (−0.38).

**Single knockouts: the same two groups everywhere.** Under the all-prey rule almost nothing
matters (0–3 groups per web; Alvarado: none at all). Under the half-diet rule it is Detritus or
Phytoplankton in every web — Cadiz Detritus 33, Mondego Detritus 25, Angola Phytoplankton 19,
Alvarado Phytoplankton 14, St Marks Phytoplankton 11. St Marks has the most groups that matter
(14 of 48) but each does less damage, which fits its many basal resources.

**Guild removals: the bottom-up result is universal.** Removing **upper consumers (TL ≥ 3.5) or top
predators causes exactly 0 secondary extinctions in all five webs, under both rules.** Removing
primary consumers under the half-diet rule is devastating everywhere: Cadiz 34 secondary
extinctions leaving 1 living group, Angola 19 leaving 1, St Marks 20 leaving 5, Alvarado 14 leaving
6. Removing Alvarado's 2 basal groups leaves **nothing alive at all**. This is the direct answer to
research question 1, and it is the same answer in every web.

**Fragmentation follows Albert et al. (2000) everywhere.** Share of groups removed before the web
splits, no secondary extinctions: most-connected-first always splits it earliest (Cadiz 0.39,
Angola 0.33, Alvarado 0.52, **St Marks 0.13**, Mondego 0.63) while random order tolerates far more
(0.48–0.86) and least-connected-first never splits four of the five. St Marks is by far the most
fragile to a targeted attack.

Closing 1–6 takes the comparison script from 22 s to roughly 5 min and the whole pipeline to about
7 min, which is still fine.

**Still missing everywhere, Cadiz included:** the dynamic/equilibrium model (Kondoh 2003). That is
why top-down removal shows nothing in any of the five webs — the structural rule is bottom-up by
construction, so it *cannot* show a top-down effect. Worth saying explicitly in the results rather
than leaving it to be read as a finding.

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
- Added 11/11:
  - the cross-ecosystem comparison, [`code/compare_webs.py`](code/compare_webs.py): four other Ecopath food webs measured the same way, with the Gulf of Cadiz rebuilt from the raw API data as a control. The script refuses to report anything unless that control reproduces the published outputs exactly (culled matrix, 43 node traits, 11 whole-web measures, 14 R50 values, 14 correlations).
  - [`notes/07_cross_ecosystem.md`](notes/07_cross_ecosystem.md) and five figures in [`figures/08_comparison/`](figures/08_comparison/README.md)
  - raw downloads in [`data/web-of-life_2026-11-11_comparison/`](data/README.md), untouched as served
  - one small defect found by the control: `network_structure.py` reads out-strength back from the rounded CSV, which moves ρ for importance-as-prey from −0.675 to −0.666. Immaterial to any conclusion, left as is, recorded in the note.

  Everything reruns with `python code/run_all.py`.
