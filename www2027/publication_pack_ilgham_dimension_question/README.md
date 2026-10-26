# Does retiring inferior high-dimensional families reduce regret?

> **RESEARCH STATUS UPDATE — 26 October 2026: No paper submission in the current cycle.** Ilgham decided the manuscript needs substantial revision and requested a team planning call to define the next work stage and assign responsibilities; Alexey agrees. This pack is retained solely as an exploratory coauthor research archive, **not a submitted or submission-approved WWW 2027 artifact**. No follow-up meeting date or owner assignments have been confirmed. See the [canonical decision record](https://github.com/RybakovAlexeyN/gadu_ai_research_lab/blob/main/context/TEAM_DECISION_2026-10-26_NO_SUBMISSION_AND_NEXT_STAGE.md) (private R&D repository; access required).

**Publication-oriented coauthor pack · 26 October 2026 · exploratory synthetic evidence**

> **Ilgham's question.** The best reward-function family has **dimension d=2**, whereas weaker families have **d=3 and d=4**. Can Search → Compare → certificate → optimize-the-winner repay its sampling cost by avoiding wasteful exploration in inferior high-dimensional families?

## The answer in 30 seconds

**Yes, family retirement can save substantial regret over the same staged algorithm without retirement. No, we have not shown that the full staged procedure beats a strong direct geometric UCB; nor have we evaluated the authors' definitive GADU-Cover implementation.**

**Most informative test:** `d=(2,3,4)`, strong family gap, `q=0.75`, `T=20,000`, six paired synthetic seeds. Mean latent cumulative pseudo-regret (lower is better):

| Policy | Mean regret |
|---|---:|
| Same Stage 1 + geometric Stage 2, **no retirement** | **4,151.6** |
| Same Stage 1 + correct family retirement + geometric Stage 2 | **1,605.8** |
| Direct bespoke geometry-aware UCB | **1,205.8** |

Retirement saves **61.3%** versus *matched Stage 1 without retirement*, but the full staged procedure still loses by **+399.95** regret to direct geo-UCB. This is a benefit **of exclusion within the two-stage design**, **not** a demonstrated victory over the original author's tuned Cover-UCB.

## Publication figures

### Figure 1 — main result: retirement vs full cost
![Figure 1: E20 source-grounded final cumulative regret](figures/fig1_main_result_d234_regret.svg)

[Open Figure 1 (SVG)](figures/fig1_main_result_d234_regret.svg) · [Main number table](tables/table1_main_numbers.md)

### Figure 2 — when does certification occur?
![Figure 2: observed family certificates for E17 36 cells](figures/fig2_certification_map.svg)

[Open Figure 2 (SVG)](figures/fig2_certification_map.svg) · [Source: 36 E17 cells](data/E17_36cell_summary.csv)

### Figure 3 — why naive Stage 1 adaptation failed
![Figure 3: Stage 1 allocation and separate E18/E19 certification diagnostic](figures/fig3_stage1_adaptation.svg)

[Open Figure 3 (SVG)](figures/fig3_stage1_adaptation.svg) · [Source: traced E18/E19 report aggregates](data/E18_E19_report_aggregates.csv)

**Important:** E18/E19 are **independent exploratory draws**, *not a paired A/B test*. This diagnostic does not establish a causal superiority of E19 over E18.

### Figure 4 — what did we actually test?
![Figure 4: research scope and inference boundary](figures/fig4_research_logic_diagram.svg)

[Open Figure 4 (SVG)](figures/fig4_research_logic_diagram.svg) · conceptual diagram, not empirical trajectory data.

## Choose what you need

- **[One-page research brief](ILGHAM_ONE_PAGE_SUMMARY.md)** — research question, result, scientific limitation and one specific action for Ilgham.
- **[Figure Guide: suggested article captions, precise source and prohibited overclaims](FIGURE_GUIDE.md)** — all four figure captions in English, ready for coauthor editing.
- **[Table 1](tables/table1_main_numbers.md)** — canonical three-policy contrast and methods footnotes.
- **[Methods](appendix/APPENDIX_METHODS.md)** · **[limitations](appendix/APPENDIX_LIMITATIONS.md)** · **[traceability](appendix/APPENDIX_TRACEABILITY.md)** · **[source manifest](data/FIGURE_SOURCE_MANIFEST.md)**.

## Download journal-format files (vector PDF / high-resolution PNG)

The four **editable/viewable SVGs are committed here**. A [GitHub Actions workflow](../../.github/workflows/ilgham_publication_figures.yml) verifies the three original data Git blobs, checks the published numbers and produces **four vector PDFs and four 3600px-wide PNGs** as a workflow artifact. Open the most recent *successful* [publication-figure workflow](https://github.com/RybakovAlexeyN/gadu_team_review/actions/workflows/ilgham_publication_figures.yml), then download the artifact named **`ilgham-publication-4figures-pdf-png`**. Workflow artifacts expire according to their retention schedule; the canonical SVG source persists in Git.

Local reproducibility: `python verify_and_export.py` (stdlib verification) and `pip install cairosvg && python verify_and_export.py --export` (binary export).

## One outstanding request for Ilgham

**Please confirm the definitive current K=3 GADU-Cover pseudocode/source, especially the new adaptive Stage 1/2 and the physical-cover/preflight/certificate/fallback/restart rules.** Until source-to-code parity and a source-matched immediate full-union Cover-UCB comparator are established, these exploratory results must not be presented as an evaluation or falsification of the actual GADU-Cover theorem.

**This is not a real-traffic causal regret result.** For the full chronological E01–E21 record, see the [archive-oriented handoff](../empirical_results_2026-10-26/ilgham_heterodimensional_followup/E01_E21_EVIDENCE_INDEX.md). Older E03/E06 figure packs in PR #5 remain unmodified.
