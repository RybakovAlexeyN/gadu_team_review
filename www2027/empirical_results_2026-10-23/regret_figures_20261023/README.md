# GADU synthetic benchmark: regret trajectories and reward functions

23 October 2026. Exploratory synthetic experiments, not original-author implementation or a real-data policy test.

Functions: f_i(x) = p_i - s_i |x - c_i|, x in [0,1], Bernoulli success probability f_i(x). L=0.2, K=2, T=3,000,000, q_w=1, w=1. 16 fixed seeds per world.

| World | p1,p2 | c1,c2 | s1,s2 |
| --- | --- | --- | --- |
| strong_gap | .8,.18 | .8,.25 | .15,.12 |
| medium_gap | .8,.45 | .8,.25 | .15,.12 |
| near_tie | .8,.78 | .8,.25 | .15,.12 |
| exact_tie | .8,.8 | .8,.25 | .15,.12 |
| offcenter_geometry | .8,.18 | .02,.88 | .20,.12 |

The cumulative pseudo-regret R(t) curves were obtained by instrumenting a complete replay of the frozen implementation, not by interpolating final values. All 80 of 80 final seed results match previously frozen 3-million-round results at absolute tolerance 1e-4. The public SVGs show 16-seed mean traces sampled every 150k rounds, with search-boundary points. Original telemetry captured 104 checkpoints; the complete raw trajectory archive and instrumentation script are in a separate ZIP delivered to the experiment author, not yet this public repo.

## Figures

- [Strong gap regret](figures/Rt_strong_gap.svg) and [functions](figures/functions_strong_gap.svg)
- [Moderate gap regret](figures/Rt_medium_gap.svg) and [functions](figures/functions_medium_gap.svg)
- [Near tie regret](figures/Rt_near_tie.svg) and [functions](figures/functions_near_tie.svg)
- [Exact tie regret](figures/Rt_exact_tie.svg) and [functions](figures/functions_exact_tie.svg)
- [Off-center regret](figures/Rt_offcenter_geometry.svg) and [functions](figures/functions_offcenter_geometry.svg)

[Mean regret checkpoints CSV](data/mean_regret_150k_from_validated_trace.csv) | [Reward function parameters CSV](data/tent_functions.csv).

## Additional R(t) curves for censored positive-only feedback (q_w < 1)

The separate archived Stage III executable was also instrumented and replayed, **with source-correct window maturity and the original policy decisions unchanged**. All **16/16** frozen full-horizon regrets agree with the telemetry replay at tolerance 1e-4. Four seeds per world/q cell, T=3,000,000, w=1, q_w in {0.5,0.75}. The stochastic law assigns an early success delay of 1 with probability q_w and delay w+3 otherwise; late positives are excluded from the windowed pseudo-reward. These are *genuinely censored synthetic* rewards, not Criteo data.

- [q=0.5, strong gap](figures/Rt_q0p5_strong_gap.svg)
- [q=0.75, strong gap](figures/Rt_q0p75_strong_gap.svg)
- [q=0.5, near tie](figures/Rt_q0p5_near_tie.svg)
- [q=0.75, near tie](figures/Rt_q0p75_near_tie.svg)
- [Machine-readable 4-seed means](data/mean_regret_q_lt1_4cells_150k.csv)

The complete 107-checkpoint seed-level q<1 records and the telemetry script are in the companion archive for the experiment author, not fully committed to this public PR. **Only four seeds per condition** and one synthetic delay law; the q=0.5 strong-gap GADU cumulative path is effectively deterministic under its locked geometry. Differences across q cannot be attributed to censoring alone because tuning parameters and budgets also change.

## Scientific interpretation

The curves show cumulative *latent pseudo-regret*, not realized random regret or upper bound. At T=3m, strong-gap GADU has mean regret 91,957.05 compared with 24,392.09 for optimized immediate Cover-UCB. The GADU search stage accounts for about 69,914.70 regret by t=197,465.

These are pilot-informed tent-shaped synthetic environments, q_w=1 without nontrivial positive censoring, and independent source-informed GADU code. No real advertisement policy regret was measured; no universal algorithm ordering or theorem falsification follows. The separate q_w<1 study now also has telemetry-replayed R(t) curves, with four seeds per cell and one synthetic censoring law; it remains exploratory.
