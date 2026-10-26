# Complete E-series record — source and scope

**Record-based index, not a claim of every series having complete public raw data.** E01 and the E11/E12 full archives are not part of this PR, and E16/E21 are reviews/control work rather than newly completed full research grids.

| Study | Purpose | Executed evidence / status | Directly tests d=(2,3,4) mechanism? |
|---|---|---|---|
| E01 | Early one-dimensional pilot | Separate canonical E01 raw not available in this public packet | No |
| E02 | Heterogeneous d=(1,2) midpoint covers | 20 paired T=10M paths | Partial |
| E03 | Post-hoc retained/nested-grid correction of E02 | 20 paired T=10M paths, no winning pair, large compulsory Search cost | Partial |
| E04 | Horizon/budget discontinuity and branch smoke | 12 paired T=3M/4M cases; GADU-inspired higher regret | Diagnostics |
| E05 | Fixed-net approximation oracle | Deterministic calculation, no new policy rollouts | Diagnostics |
| E06 | Direct d=(2,3,4) with source-tuned Cover | 6 paired T=10M; staged policy loses; Cover uses 3 arms | **Yes, mechanism not activated** |
| E07 | d=100/1000 admissible-cover feasibility | Mathematical no-go for tiny full-cube covers, no new large-d runs | Geometry gate |
| E08 | d=(2,3,4), T=225M geometry/cost | Real synthetic Cover-only path + deterministic Search regret lower bound | Partial |
| E09 | Shifted optimum geometry confound | One full staged synthetic path and Cover deterministic lower bound; positive *confounded* comparison | Control |
| E10 | High ambient/low intrinsic dimension toy | 72 T=12k toy trajectories: cert beats flat, loses geometry-aware | Indirect, different problem |
| E11 | Family certification vs flat/geo heuristic | Exploratory earlier synthetic study; raw not published in this packet | Indirect |
| E12 | Multi-modal functions and delayed feedback | Frozen E12 simulator underlies later experiments; original full archive not published here | Indirect |
| E13 | Heterogeneous vs equal dimensions, 2 peak and quadratic, gap/horizon | **1152** complete paths, 138.24M decisions; cert helps versus identical Stage1 no-retire, loses geo in certified strong-gap worlds | **Yes, surrogate** |
| E14 | Vary Stage1 budget/early certificate | **960** complete paths, 57.6M decisions; budget tradeoff / failed medium-gap cert | **Yes, surrogate** |
| E15 | Futility bailout from forced certification | **256** complete paths, 15.36M decisions; no verified win in certified cells | **Yes, surrogate** |
| E16 | Six-hour review, verification and incomplete plan | **0** new full trials; E15 audit accepted; other planned work incomplete | Review |
| E17 | Dimension × gap × q phase diagram | **864** complete paths, 25.92M decisions; 36/36 big-gap q=.75 correct certificates | **Yes, surrogate** |
| E18 | Optimistic adaptive Stage1 sampling | **540** paths, 10.8M decisions; adaptive 0/108 certificates | **Yes, surrogate** |
| E19 | Certificate-gap bottleneck sampling | **540** paths, 10.8M decisions; 21/108 certificates; certified cells lose direct geo | **Yes, surrogate** |
| E20 | Matched geometric Stage2, controlled no-retirement | **540** paths, 10.8M decisions; 26/108 certificates; d234 large q=.75 cert 1605.8 / no-retire 4151.6 / direct geo 1205.8 | **Yes, surrogate** |
| E21 | Strict algorithm/source/statistics review | **0** new broad grids; rechecked E20 540 original trajectories and 162 post-hoc label permutations; source-parity blocker | Audit |

**Correct total for E13–E20:** 1152+960+256+0+864+540+540+540 = **4852** independently recorded policy trajectories, 269.52 million simulated decision rounds. E02/E03/E06/E09/E10 are different protocols and not merged into this count. None is a full source-parity test of final author GADU-Cover.

## Public pre-existing sources in this PR

[E03](../../empirical_results_2026-10-24/e03_mvp/README.md) · [E06 d=(2,3,4)](../../empirical_results_2026-10-24/e06_dim234_exploratory/README.md). Their frozen sources, figures and seed-level trajectories remain unchanged.

## Internal independently preserved evidence (not all exposed publicly)

The E13–E21 full reports and code sit in research branches `agent/ilgham-yuriy-e13-20261024`, `agent/ilgham-yuriy-e14-stage1-budget-20261025`, `agent/ilgham-yuriy-e15-futility-bailout-20261025`, `agent/ilgham-e17-dimension-phase-diagram-20261025`, `agent/ilgham-e18-adaptive-stage1-20261025`, `agent/ilgham-e19-certificate-gap-20261025`, `agent/ilgham-e20-stage2-matched-20261025`, and `agent/g5-e21-gadu-strict-audit-20261025` in `RybakovAlexeyN/gadu_ai_research_lab`. Coauthors who require full seed-level reproduction should obtain access or a specific shareable, audited archive. Private links must **not** be mistaken for published public raw data.
