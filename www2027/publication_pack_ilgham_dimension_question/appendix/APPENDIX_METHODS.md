# Methods (condensed, review appendix)

**Status:** Exploratory synthetic GADU-inspired experiments (E06, E13–E21). Author GADU-Cover implementation parity not established.

## Setting

`K=3` continuous Lipschitz reward families `f_i: X_i -> [0,1]` with heterogeneous dimension vectors including `d=(2,3,4)`. Synthetic Bernoulli success is observed through positive-only delayed feedback; `q=F(w)` denotes the fraction of successful events arriving within a fixed attribution window. Action-level latent pseudo-regret sums `f* - f_{i_t}(x_t)` over each *actual* time step (including Stage1). It is not the paper's computable high-probability regret certificate.

For E17: full Cartesian physical grid `{1/6,1/2,5/6}^d`; 6 layouts × 3 reward gaps × 2 q × 6 seeds × 4 policies at T=30,000. For E18/E19/E20: 3 layouts × 3 gaps × 2 q × 6 seeds × 5 policies at T=20,000, with different seed allocations between experiments. Most relevant E20 strong-gap q=.75 d=(2,3,4) cell comprises six paired seeds and five policy variants. We use one direct bespoke geometry-aware UCB and two staged variants with *identical Stage1* and geometric Stage2 but with/without family retirement.

## Primary identified within-cell contrast

`Delta_retire = R_staged_cert_geo - R_staged_no_retire_geo = 1605.7826622 - 4151.5864104 = -2545.8037482`. This isolates the effect of the **retirement restriction given the same Stage1** within this simulator, not the effect of mandatory Stage1 vs no Stage1. Percent relative reduction: `61.321%`.

`Delta_direct = R_staged_cert_geo - R_direct_geo = 1605.7826622 - 1205.8335991 = +399.9490631` (unadjusted descriptive six-seed 95% paired CI [250.1801, 549.7181]). Positive is worse.

## Observations from other experiments

E17 certificates in strong gap q=.75: 36/36, strong q=.35: 9/36; none moderate/near-tie in selected worlds. E18 optimistic allocation: 0/108, excessive use of best-looking family, certificate-information scarcity. E19 independent certificate-gap allocation: 21/108; E20: 26/108, all correct in archived paths. E21 exact-center feasibility: 36/36 strong, 36/36 moderate, 0/36 near tie; not a no-go for full-cover certification.

## Design caveats

- E13–E20 are independent GADU-inspired surrogates with central anchors, differing preflight/fallback and reused statistics; definitive author GADU-Cover not executed.
- Direct geometric comparator is independently engineered, not source-exact Cover-UCB, HOO or Zooming.
- Some results arise from comparisons of fixed grids; E09 showed optimum-grid alignment can dominate apparent regret improvement.
- Cells share previously selected landscape generators; six-seed conditional intervals do not account for across-landscape, multiple-comparison or post-selection uncertainty.
- Original author algorithm needs cover validity, feedback clock and proper physical search geometry, preflight and economic certification/fallback checks before any paper claim.
- Publication pack includes complete *cell-level CSVs* for E17/E20/E21 but not original full per-seed source archives.

For complete evidence catalogue and exact internal-archive lineage, see [older review evidence index](../../empirical_results_2026-10-26/ilgham_heterodimensional_followup/E01_E21_EVIDENCE_INDEX.md).
