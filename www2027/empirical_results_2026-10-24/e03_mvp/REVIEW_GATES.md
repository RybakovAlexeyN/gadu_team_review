# Scientific release and adversarial audit — E03 (24 October 2026)

## Confirmed within scoped protocol

- Frozen E03 post-hoc repaired covering, 20 original paired trials (8 strong-1D + 8 strong-2D + 4 near-tie) without exclusions, T=10M, q=.75 and w=1.
- 20/20 paired final GADU−Cover regret strictly positive; separately sampled source trajectories from actual stored runs, NOT interpolated from endpoints.
- The original frozen 32-member experiment archive has an internal file manifest with 31 SHA256 entries that previously passed integrity checks. This public folder contains the selected figure/data subset, not the complete private archive or author manuscript.
- Archived seed-level telemetry gives 2,080 exact checkpoints; 40/40 series endpoints reconcile with the same-seed frozen E03 CSV, monotonic time/regret and stage sums.
- Local source-informed short-policy oracle: 96 Search traces, 288 Compare branches, three positive-only statuses; admissible covers and E03 budgets checked. These tests are scoped to this independently authored program and do not validate exact original author policy.

## Two primary falsifications, not merely caveats

1. **Deterministic Search cost floor:** per-seed regret_search > full-horizon Cover regret for all 20/20 E03 pairs. Later stages cannot reverse that realized ranking because pseudo-regret is nonnegative. Mean ratios 255.45×, 9.37×, 3.58×; do not misconstrue tiny within-world confidence intervals as robust generalization.
2. **Economic rejection structurally unreachable:** for every one of 48,341 Compare decision clocks t and either candidate winner, D_t − [t + B_singleton(T−t)] > 0 in the independent source-formula implementation. No strict statistical separator can be economically rejected in these fixed E03 settings. New seeds would not cover that branch. An independent end-to-end rejection/fallback fixture remains necessary.

## Known limitations and MUST NOT claims

- Implementation is independent and manuscript-informed, **NOT proven equivalent to original coauthors' code**. H1 source-author policy parity BLOCKED.
- Current paper snapshot states *GADU is not evaluated* and has different baseline-only 3-family HOO/Zooming studies. Do not substitute E03 without author editorial approval: H7 BLOCKED.
- Post-hoc E03 after nonnested E02 geometry issue; correction retained original coarse actions in exercised transitions but **not** all-radius hierarchy. E02/E03 have different seed blocks and Search lengths: no one-factor causal geometry ablation.
- Only 3 selected synthetic worlds, n=8/8/4, q=.75, one delay distribution, no randomized real-world online test, no credible claims of uniform superiority/inferiority or approximate crossover horizon.
- Observed regret **is not** theoretical upper regret certificate; neither contradicts the other's mathematics. Existing Criteo attribution-delay observation is a separate study, NOT evidence of counterfactual policy improvement.
- Pointwise individual-policy t intervals are not simultaneous confidence bands, not paired time-wise differences, and not across-world inference. Publication double-blind requires anonymized access if included as reviewer supplement; this public repo is directly attributable to an account.

## Gates

| Gate | Outcome | Details |
|---|---|---|
| H2/H3 | PASS scoped internally (local) | independent event-clock and physical cover checks; author parity unknown |
| H4/H5 | PASS scoped | 20+20 paired CSV accounting, original clean CI Cover and arithmetic |
| H6 | PASS scoped | original archive per-seed 40 trajectories, 2,080 points, PDF/SVG/PNG |
| H1/H7 | BLOCKED | original author program and paper inclusion not approved |

**Release policy:** this public folder is a PRELIMINARY COAUTHOR REVIEW PACK. Use figures only after coauthor's explicit author-source and editorial signoff. New experiments, horizon sweeps or algorithm optimization are a separate phase and were **not** performed here.
