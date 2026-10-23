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

## Scientific interpretation

The curves show cumulative *latent pseudo-regret*, not realized random regret or upper bound. At T=3m, strong-gap GADU has mean regret 91,957.05 compared with 24,392.09 for optimized immediate Cover-UCB. The GADU search stage accounts for about 69,914.70 regret by t=197,465.

These are pilot-informed tent-shaped synthetic environments, q_w=1 without nontrivial positive censoring, and independent source-informed GADU code. No real advertisement policy regret was measured; no universal algorithm ordering or theorem falsification follows. A separate small q_w<1 study measured only final regret and is reported in the main PR.
