# E06 — Ilgham's d=2 vs d=3,4 proposal: view the real trajectories

**Exploratory only: 3 synthetic scenarios × 2 seeds, T=10M. Independent manuscript-informed K=3 adaptation, NOT approved original-author GADU. No manuscript conclusions without coauthor signoff.**

## Figure 1 — archived cumulative regret

![E06 actual 51-checkpoint-per-seed R(t) trajectories](d234_cumulative_regret.png)

[Direct-download PDF for LaTeX](https://raw.githubusercontent.com/RybakovAlexeyN/gadu_team_review/ebc663743491a90568408eb965b64a4382d7dae5/www2027/empirical_results_2026-10-24/e06_dim234_exploratory/d234_cumulative_regret.pdf) · [PNG](d234_cumulative_regret.png)

## Figure 2 — Search/Compare/Continue decomposition

![E06 stage decomposition](d234_stage_decomposition.png)

[Direct-download PDF for LaTeX](https://raw.githubusercontent.com/RybakovAlexeyN/gadu_team_review/ebc663743491a90568408eb965b64a4382d7dae5/www2027/empirical_results_2026-10-24/e06_dim234_exploratory/d234_stage_decomposition.pdf) · [PNG](d234_stage_decomposition.png)

## Entire self-contained package

**[Download ZIP with source, immutable seed results, audits and both figures](https://raw.githubusercontent.com/RybakovAlexeyN/gadu_team_review/ebc663743491a90568408eb965b64a4382d7dae5/www2027/empirical_results_2026-10-24/e06_dim234_exploratory/E06_D234_ILGHAM_EXPLORATORY_REVIEW.zip)** · [Read full protocol/results](README.md) · [Critical referee note](E06_RESEARCH_REVIEW_2026-10-24.md)

**Result:** GADU-inspired implementation has larger final pseudo-regret than immediate Cover in all 6 paired 10M rounds. Strong-gap family choice certified 2/2, moderate/near-tie 0/4. Importantly, **source-tuned Cover uses rho=1 and only 3 physical arms, one per family**; hence it does **not** spend its time exhaustively exploring the 3D and 4D domains at this T. The 30-arm fixed rho=0.5 Cover diagnostic also does better. Exact replay and scoped numerical checks pass; final author-code parity and statistical inference remain blocked.

GitHub's embedded PDF viewer may show a spurious “Invalid PDF”; use these `raw.githubusercontent.com` direct downloads. Both PDFs opened and rasterized in independent PDF engines locally.
