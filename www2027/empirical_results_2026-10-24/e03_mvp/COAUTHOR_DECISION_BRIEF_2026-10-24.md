# Coauthor decision brief — WWW 2027 GADU empirical E03 (24 Oct 2026)

**Request to Ilgham:** Please examine the three figures and decide whether these results belong in the draft as a clearly labelled *exploratory finite-horizon cost diagnostic* or should remain supplementary/future work. **Do not treat this bundle as a reproduction of the final author algorithm until parity is checked.** No manuscript changes or submissions have been made here.

## 1. Paper-ready files — use these first

| Priority | Material | Use |
|---|---|---|
| 1 | [Fig. 1 regret trajectories — PDF](figures/fig1_cumulative_regret.pdf) · [PNG preview](figures/fig1_cumulative_regret.png) | Primary comparison, three synthetic worlds |
| 2 | [Fig. 2 Search / Compare / Continue — PDF](figures/fig2_stage_decomposition.pdf) | Explain the finite-horizon loss mechanism |
| 3 | [Fig. 3 test functions — PDF](figures/fig3_reward_functions.pdf) | Show the 1D/2D clipped-quadratic means |
| 4 | [Proposed figure captions + Methods + Results](CAPTIONS_METHODS_RESULTS.md) | Candidate English text; **requires author edits and approval** |
| 5 | [Exact final summary](data/table_e03_final.csv) · [20 paired seeds](data/e03_seed_runs.csv) · [2,080 saved trajectory points](data/e03_per_seed_trajectory_checkpoints.csv) | Numbers and original sampled time histories |
| 6 | [Download self-contained ZIP](E03_COAUTHOR_FIGURES_DATA.zip) · [rebuild & verify](README.md#reproduce-without-rerunning-10m-decisions) | Use without new 10M trials |
| 7 | [Adversarial limitations](REVIEW_GATES.md) | Mandatory scientific qualification |

## 2. Exact experiment and outcome

Independently coded, **author-text-informed** family-certification program against immediate Cover-UCB; **not author-version validated**. Two synthetic families with dimensions (1,2) and clipped quadratic peaks. Three pilot-informed worlds (strong best 1D, strong best 2D, near-tie), peak pairs (0.80,0.18), (0.18,0.80), (0.80,0.78); T=10,000,000, q_w=0.75, window w=1, L=0.3. E03 is a **post-hoc**, coarse-action-retaining correction after E02, not pristine preregistration.

| World | n seeds | Immediate Cover mean R(T) | Independent GADU mean R(T) | Paired mean GADU−Cover |
|---|---:|---:|---:|---:|
| Best 1D | 8 | 2,444.37 | 638,590.92 | **+636,146.55** |
| Best 2D | 8 | 12,267.84 | 126,135.90 | **+113,868.06** |
| Near tie | 4 | 12,397.11 | 57,308.91 | **+44,911.80** |

**What is actually established, conditional on these worlds and this independently written implementation:** all 20 paired GADU final regrets exceed Cover; correct strong-gap family certificates 16/16; no certificate 4/4 near-tie; Search-only regret exceeds the *entire* Cover final regret in all 20 pairs. Thus at T=10M no continuation can reverse the measured result. The economic rejection branch is mathematically unreachable with this E03 setup; the full policy has NOT been stress-tested in all economic branches. Intervals in the public tables are conditional-on-world paired Student-t intervals. Shaded temporal bands on Fig 1 are **pointwise individual-policy**, not simultaneous or paired-difference bands.

**Not established:** original author implementation equivalence, theorems/refutations, universality, crossover horizon, real-world online causal uplift, or a prospective randomized environment study. Criteo delay-calibration results are a separate study.

## 3. Exactly three coauthor decisions required

1. **Policy parity:** Are event maturity, first strict-separation, economic accept/reject, Cover construction and fresh continuation identical to the author-approved algorithm? If no, identify the definitive source/revision; paper may not label this result as an evaluation of the original algorithm.
2. **Editorial slot:** Main paper, appendix, or omit pending a new experiment? Suggested safe framing: *“In selected synthetic finite-horizon cases, the initial search cost of a source-informed independent implementation exceeds the realized regret of immediate Cover-UCB, motivating further horizon- and regime-dependent study.”*
3. **Anonymous reproducibility:** The present link is author-identifiable, so choose a double-blind-compliant supplementary route before placing a repo URL in a reviewer-visible submission.

## 4. Next empirical research task (separate; not a result from this packet)

Verify full policy branch correctness including **strict separation followed by economic rejection and fallback** on short controlled fixtures; obtain exact author parity; then preregister a *discriminating* horizon/world/gap/q/w experiment with horizon-specific retuning and held-out seeds. Do not re-run E03 unchanged, and do not cherry-pick only scenarios favoring certification.

**Release status: READY FOR COAUTHOR CRITICAL REVIEW ONLY. Not approved for insertion into the manuscript.**
