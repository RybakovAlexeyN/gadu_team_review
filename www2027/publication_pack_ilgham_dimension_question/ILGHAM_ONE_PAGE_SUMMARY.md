# Does low-dimensional family retirement reduce regret?

**One-page coauthor brief · 26 October 2026 · exploratory synthetic evidence (NOT an evaluation of the authors' final GADU-Cover)**

## Question

Ilgham proposed heterogeneous reward-function families with dimensions **d=(2,3,4)**, where **d=2** contains the best achievable reward. Can Search / Compare / certification select the low-dimensional winner early enough that avoiding further exploration of weaker 3D/4D families improves **full-horizon cumulative pseudo-regret** over UCB?

## Design

We studied source-informed **independently implemented staged surrogates**, **not** the final authors' GADU-Cover algorithm. We simulated Lipschitz reward families, Bernoulli positive-only delayed feedback with observation-window mass `q`, horizons and randomized reward landscapes. E17 mapped dimensions/gaps/`q`; E18 tested optimistic Stage1; E19 tested certificate-gap allocation; E20 fixed Stage1 while varying retirement and Stage2. Controls included a **matched mandatory Stage1 without retirement** and a **bespoke direct geometry-aware UCB**. Regret counts every decision, including forced Stage1 sampling.

## Three decisive observations

**A. Family retirement can have a large *conditional mechanism* benefit.** In E20 at `d=(2,3,4)`, strong gap, `q=.75`, `T=20,000`, `n=6`, mean regret was **4,151.6** with the same Stage1 and no retirement versus **1,605.8** with correct family retirement (**−61.3%**). The certificate was correct in **6/6** runs.

**B. It did not win the full algorithmic comparison.** Direct geometry-aware UCB achieved **1,205.8**, 399.95 below the staged retirement policy. In E20, all five cells where staged geometric continuation had lower mean regret than direct geo-UCB **had no certificates**, so those are not evidence of gains caused by certification.

**C. Certification is fragile.** E17: with strong gaps, `q=.75`, certificates **36/36** across six dimension layouts, falling to **9/36** at `q=.35`; medium and near-tie regimes had **0** observed certificates. E18 reward-optimistic Stage1 concentrated 7,140 of 7,200 pulls on the leading family and produced **0/108** certificates; E19's certificate-gap allocation gave **21/108** on different seeds (not a paired causal comparison).

## Conclusion for Ilgham

**The proposed mechanism is supported relative to a precisely matched staged baseline, but the published experiments DO NOT identify a winning certified regime against the stronger direct geometry-aware comparator, and they do not test the current author-algorithm.**

E06's source-tuned immediate Cover had only one arm per family (no costly high-dimensional search); E09's positive example had unequal grid geometry. E21 established a fundamental **implementation-parity blocker**: the simulations omit or modify author preflight, physical coarse-cover construction, continuation/fallback certification and clean restart. The paper's theorem is neither confirmed nor contradicted by these surrogate rankings.

## Single action requested

**Please confirm/provide definitive current K=3 GADU-Cover pseudocode or executable for adaptive Stage 1/2, preflight, covers, certificates, gating, fallback, fresh restart and exact tuned immediate all-family Cover baseline.** We can then run one prospectively locked, source-matched comparison addressing the actual hypothesis.

[Figure 1](figures/fig1_main_result_d234_regret.svg) · [Certification map](figures/fig2_certification_map.svg) · [Stage1 diagnostic](figures/fig3_stage1_adaptation.svg) · [methods and source boundaries](appendix/APPENDIX_LIMITATIONS.md).
