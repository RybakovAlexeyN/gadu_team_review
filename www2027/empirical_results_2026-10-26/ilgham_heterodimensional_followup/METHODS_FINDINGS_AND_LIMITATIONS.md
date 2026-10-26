# Methods, quantitative findings, and inference boundaries

## Study units and estimand

The E13–E20 suite compares independently authored GADU-**inspired** family-certification/retirement policies to controls on synthetic Lipschitz reward functions with delayed positive-only feedback. All policies within a matched experimental cell use the same horizons and indexed source-potential-outcome randomization (different policies selecting different actions do **not** thereby receive identical realized Bernoulli outcomes). The target is *latent cumulative pseudo-regret* against the true continuous supremum; delayed/censored observations enter policy decisions, not the evaluator's true reward means.

E13–E20 totals: 1152 + 960 + 256 + 0 + 864 + 540 + 540 + 540 = **4852 full rollouts**, with horizons T=60k/180k, T=30k, T=20k as specified in each individual preregistration; **269.52M** decision rounds total. E16 checked prior evidence and created no new rollouts. These are *per-policy simulations*, not 4852 independent random worlds or 4852 paired contrasts.

E17: 6 dimension layouts × 3 gap types × 2 q values × 6 seeds × 4 policies = **864** paths (36 cells). E18/E19/E20: each 3 dimensions × 3 gap types × 2 q values × 6 seeds × 5 policies = **540** (18 cells, 108 matched five-policy sets). The E18/E19/E20 reward landscapes and seed sets are distinct and do not justify naive pointwise paired subtraction across experiment IDs.

## Reproducible subset, copied directly from frozen Git blobs

| File | Rows | Meaning | Original Git blob SHA |
|---|---:|---|---|
| `data/E17_36cell_summary.csv` | 36 | Four-policy mean regrets, six seeds/cell, 36 combinations | `cca8fcbec48327e2d39a16dcdf96f5ef7d45725b` |
| `data/E20_18cell_summary.csv` | 18 | Five-policy mean regrets, stages, six seeds/cell, intervals | `c19ffe65b4822e216da4ba63f83f3126ccc5ab49` |
| `data/E21_108case_certificate_feasibility.csv` | 108 | Independent population central-certificate margins | `ebcf22a90d4c9a172f0049919d8217a68c2d84ce` |

The only computations required to reproduce the **published comparisons** are CSV reads; `verify_public_summary.py` asserts row uniqueness, counts and the key E20/E21 facts. **It is not a full stochastic policy rerun.** Per-seed raw JSONL, full executable code and frozen source-hash manifests live in the original archived internal packages. No unrelated proprietary manuscript is redistributed here.

## Representative contrasts

- E17, `d=(2,3,4)`, large-gap, q=.75, T=30k: **cert+retire 2658.58**, **identical initial Stage1/no-retire 6883.20**, **bespoke geo-UCB 1885.34**, flat full grid 6059.08; 6/6 certificates.
- E18, `d=(2,3,4)`, large-gap q=.75 T=20k: optimism-guided Stage1 **4769.3**, uniform Stage1 **1938.4**, geo-UCB **1349.4**; **zero** optimistic Stage1 certificates anywhere in 108 matched experimental cases.
- E19, *fresh different seeds*, same dimension/gap/q labels: bottleneck-guided adaptive Stage1 **2058.5**, uniform Stage1 **2205.0**, geo-UCB **1365.4**; 18/18 strong-gap q=.75 certificates and 21/108 overall.
- E20, `d=(2,3,4)`, large-gap q=.75 T=20k: staged policy with geometric Stage2 **1605.7826622** vs **4151.5864104** if identical Stage1 is followed by geometric Stage2 *without explicit retirement*. Direct geometry UCB, **1205.8335991**. Within-cell paired staged minus direct geo: **+399.9490631**, descriptive conditional paired 95% [250.1801, 549.7181]; certificate 6/6. Stage1 alone contributes **583.7169047** average regret and lasts 1430.833 rounds. Fixing Stage2 does not reverse total ranking.

**E20 source note:** At equal `d=(2,2,2)`, the published frozen E20 results show *equal* staged and no-retirement geometric Stage2 regret in the strong-gap q=.75 cell (1452.4232), despite six certificates. That is plausible when the geometric policy naturally concentrates on the best family without being forcibly constrained. This differs from the **fine-grid** no-retirement policy in the same CSV (2138.58), which is a different post-Stage1 continuation. Never compare those two different Stage2 implementations as if only retirement changed.

## E21 statistical/geometric interpretation

The *one-center* certificate has the following sufficient condition under valid uniform confidence intervals:
```math
\bar Y_k-r_k > \max_{j\ne k} (\bar Y_j+r_j+L\sqrt{d_j}/2).
```
The right-hand geometric radius is specific to a center in a full Euclidean hypercube. E21 confirmed the corresponding population feasibility on exact synthetic functions: among **36 strong, 36 moderate, 36 near-tie** cases, the counts theoretically feasible with exact center means were **36, 36, 0**, while observed certificates were **26, 0, 0**. This is **not a theorem about full-cover GADU**, only about the one-center surrogate. For moderate cases, the largest population certificate margin was ~0.1317, while the minimum two-arm q=.75 statistical confidence-radius sum under a 7200-pull cap was ~0.14458, so exact-population-means + this fixed width cannot certify the moderate cases under this cap. A favorable noisy path can still cross a threshold, and would need to be logged correctly.

E21 repeated the E20 deterministic arithmetic consistency: 540/540 paths and 5940/5940 regret checkpoints, and explored 162 order permutations in seen worlds. The original code also asserted that any returned certificate winner must be `-1` or `0`; a wrong-family certificate could crash instead of being counted. Future evaluators **must log incorrect certificates as outcomes**, never silently censor such runs.

## High-dimensional feasibility

E07 performed geometry preflight, not d=100 or 1000 actual policy simulations: in full unit Euclidean cubes `[0,1]^d` the volume lower bound on a radius-one cover explodes at large d. A low-intrinsic-dimensional embedded manifold or finite candidate library is a different action class; both algorithms must receive the same admissible geometric information. This is a study-design gate, not negative regret evidence.

## Threats to validity (must accompany any coauthor presentation)

1. **P0 source parity:** E13–E20 do not execute the paper's definitive GADU-Cover (preflight/coarse covers/economic gate/fresh restart differ). We do not know the final unpublished adaptive Stage1/Stage2 semantics.
2. **P0 comparator parity:** E17–E20's direct `geo_ucb` is a bespoke initialization/bonus/expansion heuristic, not original source-tuned full-union Cover-UCB and not a validated HOO/Zooming implementation.
3. **Selection and independence:** worlds/gaps were chosen after earlier exploratory evidence; winner family has label zero, reused across q/gap grids; seed-level intervals are *conditional on selected fixed environments*, no multiple-testing adjustment.
4. **Finite geometry and horizon:** the `3^d` action grid incurs a true-continuum approximation floor; positions of maximizers relative to cover can determine observed ranking (E09 shows this directly).
5. **Feedback:** q known and one simplified matured-pseudo-reward clock; not evidence of the theorem under estimated q, nonstationary/adversarial delays, or heterogeneous real-world sources.
6. **No deployment causal evidence:** actual Criteo/iPinYou logs elsewhere are observational and do not identify GADU vs Cover regret without additional randomization/policy support and assumptions.

**Coauthor verdict:** Suitable as negative/diagnostic mechanism evidence for review, *not* an author-approved algorithm comparison or positive publication claim.
