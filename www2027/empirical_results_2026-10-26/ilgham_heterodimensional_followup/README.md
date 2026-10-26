# Heterogeneous family dimensions — coauthor research handoff (26 October 2026)

> ### Впервые открываете этот PR? / First time here?
>
> **[НАЧАТЬ ЗДЕСЬ: что именно мы сделали по вопросу Ильгама о d=2/3/4?](START_HERE_ILGHAM.md)** — постановка, ответ за 30 секунд, главный график, что доказано / не доказано и единственный ключевой вопрос к автору.
>
> **One-line answer:** retirement of inferior 3D/4D families lowers regret against a same-Stage-1 no-retirement control (E20: 4151.6 → 1605.8), but does not beat direct geometry-aware UCB (1205.8), and the authors' latest GADU-Cover has **not** been evaluated.
>
**For Ilgham / Yuriy — scientific review, not manuscript-ready empirical evidence.**

**Short verdict:** We investigated the *mechanism* suggested on 24 October: the optimal family has smaller parameter-space dimension (`d=(2,3,4)` with best `d=2`), and explicit family certification might prevent continued sampling of inferior higher-dimensional families. **Retirement helps strongly relative to the *same Stage-1* algorithm without retirement; nevertheless our independently implemented staged surrogates do not beat a bespoke geometry-aware UCB in any of the studied certified strong-gap cells. We have NOT evaluated the authors' final GADU-Cover policy.**

## Start here

- **Figure:** [E20 paired-condition comparison](figures/e20_certification_vs_geometry.svg) (SVG; actual archived mean regrets, `T=20,000`, six seeds/cell).
- **Scientific findings & decision gates:** [METHODS_FINDINGS_AND_LIMITATIONS.md](METHODS_FINDINGS_AND_LIMITATIONS.md).
- **Exactly what needs Ilgham's decision:** [COAUTHOR_DECISIONS.md](COAUTHOR_DECISIONS.md).
- **Complete E-series audit table:** [E01_E21_EVIDENCE_INDEX.md](E01_E21_EVIDENCE_INDEX.md).
- **Machine-readable frozen aggregates:** [E17 36 cells](data/E17_36cell_summary.csv) · [E20 18 cells](data/E20_18cell_summary.csv) · [E21 108 certificate-feasibility cases](data/E21_108case_certificate_feasibility.csv).
- **Read-only standard-library verification:** [verify_public_summary.py](verify_public_summary.py), runnable from this folder: `python verify_public_summary.py`.

These three published CSVs were transferred **byte-for-byte** from the independently archived internal experiment branches; their Git blob IDs are listed below. The E18 and E19 outcomes in this note are taken from frozen reports, but their full original seed-level logs/executables **are not part of this public handoff**. The CSVs are cell/case-level aggregates, not all 4,852 complete per-policy paths; the original raw archives remain in the internal research repository.

## The scientific question

Given `K=3` Lipschitz reward families with respective continuous action domains of dimensions `(2,3,4)`, and the best family in `d=2`, under delayed positive-only feedback with known window-arrival probability `q=F(w)`:

> Does the cumulative reward lost during Search / Compare / certification repay itself by eliminating inferior 3D/4D families early, relative to a **properly tuned** immediate all-family competitor under the same geometry, oracle and horizon?

Our primary reported quantity is **latent cumulative pseudo-regret** (smaller is better):

```math
R_T(\pi) = \sum_{t=1}^T \Big( \sup_{i,x\in\mathcal X_i} f_i(x) - f_{i_t}(x_t) \Big).
```

This is a controlled synthetic decision metric, **not** click-through improvement, true logged-policy regret, or the paper's computable *upper regret certificate*.

## Key evidence

### (A) Source-informed d=(2,3,4) attempt — E06, 24 Oct

At `T=10,000,000`, `q=.75`, peaks `(.80,.28,.26)`, `(.80,.55,.53)`, `(.80,.785,.780)`, the K=3 GADU-inspired experiment **lost all six seed-paired comparisons** to immediate source-tuned Cover, although the good family was correctly certified in 2/2 strong-gap seeds.

| E06 world | staged surrogate | source-tuned immediate Cover | fixed-radius Cover (diagnostic) |
|---|---:|---:|---:|
| Strong gap | 764,552 | **113,893** | 29,789 |
| Moderate gap | 492,619 | **114,581** | 37,379 |
| Near tie | 169,754 | **126,167** | 95,232 |

**Crucial experimental mismatch:** the *source-tuned* union Cover selected radius 1 with only **three physical arms** (one/family). The hypothesized “Cover wastes time on detailed d=3/4 search” mechanism was **not actually active** in this test. [Previously published E06 source, six-run raw data and figures](../../empirical_results_2026-10-24/e06_dim234_exploratory/README.md).

### (B) E09 — a numerically positive but **confounded** example

In a deliberately shifted d=2 maximizer position at `T=225M`, measured GADU-inspired regret was `961,405`, while baseline Cover had an analytic lower bound `2,531,250`. **Not a valid family-certification win:** the GADU continuation grid was finer and contained the optimum, while the immediate Cover grid did not. This post-hoc geometry example was explicitly rejected as evidence for the proposed mechanism.

### (C) E13–E20 — broader surrogate mechanism studies, 25 Oct

Across E13–E20, **4,852 archived policy rollouts and 269.52 million simulated decisions** (E16 added zero new rollouts). These are exploratory across previously designed landscape families, not thousands of independent function distributions.

- **E17:** 864 runs, `d=(2,2,2),(1,2,3),(2,3,4),(1,3,5),(2,4,5),(3,4,5)`; three reward-gap regimes; `q=.35/.75`. In large-gap `q=.75`, **36/36** correct certificates across layouts; in large-gap `q=.35`, **9/36**; no medium/near-tie certification. Retiring families reduced regret against the *identically initialized* no-retirement control, but the staged method lost to the bespoke geometry-aware UCB in every certified large-gap cell. [Exact 36-cell CSV](data/E17_36cell_summary.csv).
- **E18:** 540 new-seed runs; optimistic Stage-1 allocation spent ~`7140/7200` sampling rounds on the apparently best family at `d=(2,3,4)`; **0/108** adaptive certificates. Reward-optimism is not a certificate-information acquisition rule.
- **E19:** 540 new-seed runs; allocate Stage-1 pulls to the prospective winner or its strongest UCB challenger according to the confidence-width bottleneck. **21/108** correct certificates, including **18/18** in large-gap `q=.75`; lower mean regret than frozen uniform Stage-1 in these three strong-gap dimension layouts, but worse than direct geometry UCB.
- **E20:** 540 new-seed runs; hold Stage 1 identical, replace downstream fine-net UCB with the same geometry-based Stage 2 used by the bespoke direct comparator. **26/108** observed certificates, all for the true best family. Among 18 cells, **five** staged geometric variants were lower-regret than direct geo-UCB, **but every such cell had zero certificates**. No reported cell attributes mean superiority over direct geo-UCB to a successful certificate.

### E20: most informative controlled comparison

Large reward gap, `q=.75`, `T=20,000`, six independent random seeds **per listed cell**:

| `(d_1,d_2,d_3)` | staged with retirement + geometric Stage 2 | **same Stage 1**, no retirement + geometric Stage 2 | direct geometry-aware UCB | certificates |
|---|---:|---:|---:|---:|
| (2,2,2) | 1,452.4 | 1,452.4* | **1,171.3** | 6/6 |
| **(2,3,4)** | **1,605.8** | **4,151.6** | **1,205.8** | 6/6 |
| (2,4,5) | 1,658.9 | 10,741.0 | **1,284.3** | 6/6 |

* **Equal-dimension control:** The frozen E20 summary reports equal regret for retirement and no-retirement **with geometric Stage 2** in this cell. That can occur when a geometric policy naturally concentrates on the best family without forced exclusion. Do not confuse this with the separately reported **fine-grid Stage 2 without retirement** (2,138.6), which is a different continuation policy. See the methods note.

For `d=(2,3,4)`, family retirement reduces regret **by 2,545.8 (61.3%)** relative to the *same Stage-1* no-retirement control. But paying Stage-1 overhead still leaves the staged method **+399.95** regret worse than direct geometry UCB, with a **descriptive, within-cell six-seed paired 95% interval [250.18, 549.72]** (not multiplicity corrected, nor a population-world interval). [E20 complete 18-cell summary](data/E20_18cell_summary.csv).

### (D) E21 — hostile specification / arithmetic audit, 25 Oct

Independently reconstructed all **540/540** E20 original synthetic trajectories at the count-based-regret level and **5,940/5,940** checkpoints. Tested **162** order-permutation follow-up trajectories on previously seen synthetic worlds, not fresh scientific confirmation.

In the simpler one-center-per-family certificate architecture, the *population* certificate using exact central means is feasible in **72/108** cases but observed in only **26/108**. **Near tie: 0/36 population-feasible** (a geometric obstruction); **moderate: 36/36 population-feasible, 0/36 observed** under the fixed 7,200-pull cap (insufficient confidence precision in the central-mean plug-in test). These results do **not** imply impossibility for full-cover GADU. [108-row feasibility CSV](data/E21_108case_certificate_feasibility.csv).

**P0: source / algorithm parity is unresolved.** Unlike the reported author's GADU-Cover (preflight, physical coarse covers/seed envelope, gated continuation/fallback, fresh restart), E13–E20 use independently written central-anchor and warm-start implementations plus a bespoke geometry-aware UCB. Their negative ranking **cannot refute** the manuscript's regret-certificate theorem and is **not** a test of the new author adaptive Stage 1/2.

## Coauthor release decision

**Share as exploratory mechanism evidence and reproducibility handoff; do not paste a claimed GADU win/loss or the nominal confidence intervals into WWW 2027 without author algorithm-parity and baseline review.**

The actionable scientific gap is no longer “more seeds” but **the exact authoritative K=3 algorithm and fair comparator**. Please see [decision questions](COAUTHOR_DECISIONS.md).

## Source integrity / public-scope ledger

- `E17_36cell_summary.csv`: exact frozen source Git blob `cca8fcbec48327e2d39a16dcdf96f5ef7d45725b` (36 rows).
- `E20_18cell_summary.csv`: exact frozen source Git blob `c19ffe65b4822e216da4ba63f83f3126ccc5ab49` (18 rows).
- `E21_108case_certificate_feasibility.csv`: exact frozen source Git blob `ebcf22a90d4c9a172f0049919d8217a68c2d84ce` (108 rows).
- Separate frozen private archives contain per-seed trajectories, code, and source hashes; **not** published here. No author-unpublished manuscript, unlicensed advertising observations or private user event IDs are included.
- This is a review branch of a **public, identifiable** GitHub repository; any eventual anonymous conference supplement needs author confirmation.
