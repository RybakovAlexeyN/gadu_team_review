# Technical decisions requested from Ilgham and Yuriy

**Short reply is sufficient; the empirical results in this package are exploratory.** No manuscript edit is proposed without author approval.

## D1. What exactly is the definitive 3-family policy?

Please provide a frozen executable or complete pseudocode for the **current** K=3 GADU-Cover, including:
- Stage-1 coarse-cover construction and admissible geometry (metric, `C_i`, Lipschitz constant, net radii/cardinalities);
- Stage-1 / Stage-2 sample allocation and the proposed improved *adaptive* rules mentioned on 24 October;
- source attribution, delayed positive-only observation maturation, q=F(w), window and absolute clock;
- family separation/accuracy certificate, economic preflight, branch dispatch, no-certification fallback, and the exact fresh-reset/continuation policy;
- whether the theorem protects a computable Cover *upper certificate* or aims to show realized advantage against a concrete on-policy learner.

Our E13–E20 variants **are not source-identical to that policy**. This is the decisive implementation-parity blocker.

## D2. Which baseline should the paper claim concern?

For a fair primary comparison we propose the manuscript's tuned **immediate full-union Cover-UCB**, under identical action domains, horizon, observation model and valid geometric covers. As independent *additional diagnostics*: (a) equal-initialization no-retirement, (b) resolution-matched Cover, (c) geometry-aware adaptive heuristic/HOO/Zooming when source-verified, (d) oracle-known-family regret floor.

The E06 original-tuned Cover uses only three arms at T=10M and therefore cannot test the proposed over-exploration of higher dimensions at that horizon. E09's one favorable example is confounded by unequal grids.

**Please confirm whether this comparator and primary estimand match the desired claim.**

## D3. Which dimension regime is scientifically intended?

A genuine full \([0,1]^d\) with Euclidean metric and d=100 or 1000 cannot be represented by the tiny covers used for d=2,3,4. Radius-one unit-cube covering-volume lower bounds are ~4.2e39 and ~3.25e885, respectively. We must distinguish:
1. *ambient* d=100/1000 with known low *intrinsic* dimension;
2. genuine high covering dimension with feasible geometry/horizon;
3. a finite set of high-dimensional parameter vectors (a different finite-arm problem).

**Which is the intended theoretical family?** A numerical experiment should not quietly switch between them.

## D4. Which result is useful for the manuscript?

On controlled synthetic surrogate studies:
- verified family-retirement benefit against *matched Stage-1/no-retirement* (e.g. E20 d=(2,3,4), 4151.6 → 1605.8 regret);
- **no verified certified regime** beating bespoke geometry-aware UCB;
- E18's naive optimistic Stage1 failed certificate acquisition; E19's bottleneck sampling improved it; E20's Stage2 replacement was insufficient.

Do you want these **negative/diagnostic** empirical findings as a separate appendix, the motivation for a modified algorithm, or held out from the current paper? The current handoff does not provide positive evidence for the author-original GADU theorem.

## Proposed review-and-run gate

After D1–D3 are resolved: source-to-code parity tests for every branch and the feedback clock → locked function distribution with randomly permuted winning-family label → source-tuned full-union baseline plus matched-initialization no-retirement and matched-resolution controls → independent offline reconstruction of all regret curves and certificates → only then consider a paper claim.

No online-causal GADU regret result is asserted from Criteo or iPinYou in this synthetic experiment packet.
