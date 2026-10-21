# WWW 2027 — Preliminary synthetic algorithm evaluation (21 October 2026)

**Shared team review / preliminary evidence only (G4). This branch is PUBLIC.**

The user requested a shareable pointer for the research team rather than a link to a private workspace. This branch contains only a sanitized summary, the scenario configuration and **32 actual paired-seed CSV rows**. It contains **no unpublished Overleaf manuscript, research-source scripts, or private internal audit**. GitHub `main` remains the existing static website.

## Question and tested implementations

Does the independent **search → select → refine** WWW GADU implementation pay less cumulative pseudo-regret than a conventional Cover-UCB baseline? Additional exploratory comparator: independently transcribed **ICLR Bridge v2**, which is *not* an alternate exact implementation of the WWW article.

- Four **synthetic**, stationary Bernoulli Lipschitz-cone reward worlds, two or three families per world; *not real ad logs or user behavior*.
- Eight common seeds `11,17,23,29,41,47,53,59`, `T=4000`, three policy executions per scenario/seed: **32 paired worlds × 3 policies = 96 policy runs**.
- Positive-only delayed feedback: positive arrival window with `q_w=.75` and `w=5` for three worlds, `q_w=1` for strong-gap. Feedback from a previous action at source `s` can be observed before a decision at `s+w`. See `experiment_config.json`.
- Metric: expected/mean **cumulative pseudo-regret relative to true continuum optimum**, not realized conversion count.

### Reported means (smaller is better)

| Scenario | Cover-UCB | WWW three-stage | Bridge v2 |
| --- | ---: | ---: | ---: |
| easy_gap | 255.05 | 726.97 | 718.68 |
| near_tie | 250.33 | 250.09 | 249.86 |
| center_trap | 881.11 | 1062.08 | 1050.91 |
| strong_gap_exploratory | 15.76 | 15.76 | 15.76 |

Raw rows: [`results/source_clock_3way_results.csv`](results/source_clock_3way_results.csv), with one row per (scenario, seed) and separate regret/path/certificate columns per policy. The original simulation's CSV SHA-256 was `8927ccfe5c655696b8843780080b7a6a3f9da22274980b7efab2d73c6b63ca38`; GitHub copy may normalize line endings, so use recorded numerical rows and Git blob identity for this public text copy.

## Most important validity restrictions

1. **No accepted certificates in any run.** First three worlds went through fallback; strong-gap used Cover-UCB by preflight. Therefore certificate validity and post-certificate optimization were **not tested**.
2. The coarse search-net radius `rho=1` effectively produces **one point per family** for all these tested low-dimensional worlds. The experiment is a **smoke test of finite-arm action handling, search cost and fallback**, not convincing validation of continuum-parameter optimization.
3. Particularly in `near_tie` and `center_trap`, regret is dominated by discretization (geometric grid bias). These are deliberately difficult regimes, not a representative performance benchmark.
4. Only eight seeds per world, exploratory selection of worlds; no holdout, power study, real-data evaluation, preregistered confirmatory inference, or independently accepted author-code/algorithm-theorem equivalence.
5. **Not original authors' C.13/C.14 replication.** Do not use these means to assert universal advantage/disadvantage or the published theorem; original supplement not yet obtained.

## Research decision for team

Please confirm (1) which single exact algorithm the WWW submission describes, (2) which author-provided scripts exist, and (3) which **real-world dataset and valid evaluation protocol** should underpin the final results. Real logs require action-selection propensities and observation timestamps for valid offline policy evaluation; without these, a model fit from real observations yields **semi-synthetic** evaluation, not logged-policy counterfactual validation.

**Provenance:** independent local experiment and source-clock reconstruction; full internal reproducible code/archive is held separately and intentionally not copied into this public repository without a deliberate sharing decision. Questions/requests for the full package can be directed to the experiment author.

**This is NOT a release-ready scientific benchmark or a manuscript claim.**
