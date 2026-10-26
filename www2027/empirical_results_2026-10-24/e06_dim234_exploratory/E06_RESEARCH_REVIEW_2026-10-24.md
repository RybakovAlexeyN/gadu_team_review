# E06 / Dimensional heterogeneity — hostile reviewer decision (24 Oct)

**Request from Ilgham:** best mean reward family has dimension 2; other candidate families have dimensions 3, 4; investigate whether Cover-UCB wastes actions exploring high-dimension, worse families while GADU certifies the 2D family and exploits it.

## Experiment and honest evidence

- 3 families, dimensions (2,3,4), clipped-quadratic means with peak locations explicitly specified in pre-run lock; 3 worlds varying gap (.52/.54; .25/.27; .015/.02), T=10m, q=.75, w=1, L=.3, gamma=1, C=(1,2,3).
- Source-informed 3-family independent implementation; **not** author code; first complete 6 paired seeds and all requested branches under available simulator.
- Source tune selects eta=1, search rho=5/12, physical search net 113 arms (d2=5, d3=27, d4=81), initial Search takes 1,405,043 actions. Compare takes 18,652 reserved actions; early accept at Search end + 1 in strong world. All world/seed results archived unchanged and no exclusions.
- **Direct source-tuned Cover baseline rho=1: only one action per family** (three arms total). This falsifies the experimental *mechanism assumption* in the user-proposed 10m finite-horizon setup: it is not exploring rich 3D/4D parameter grids. Additional *fixed-rho=.5* diagnostic baseline has 30 physical actions, still not worse than GADU.
- Mean final latent pseudo-regret: GADU vs source-cover = 764,552 vs 113,893 (strong); 492,619 vs 114,581 (moderate); 169,754 vs 126,167 (near-tie). All 6 paired differences positive; the diagnostic 30-arm Cover also better all 6.
- Actual 51-checkpoint-per-seed R(t) trajectories regenerated with exact source-timing and CRN physical keys, all six replay endpoints agree with archived runs. Two PDF/PNG figures produced and independently rasterized from PDF.
- Independent exact-rational Search pseudo-regret oracle and all-action time accounting PASS for six seed/world runs. Pure Python vs Numba RNG/status/Compare on K=3 320/24/72 tests PASS, both strict separation and no-separation branches exercised. Euclidean covering radius/cardinality/Lipschitz witnesses PASS at all tested radii. Pseudocode-author equivalence still unapproved.

## Reviewers' objections and required fixes

1. **Theory/algorithm:** need Ilgham's exact K=3 policy and certificate to claim original GADU, not merely extending our own E03 K=2. C cover-envelope must be validated for the entire admissible radius menu, not only four evaluated radii; the current proof-valid C value is author-blocked.
2. **Experiment design:** the main source-optimized baseline at T=10m has three actions; no high-dimensional-search contrast exists. To test proposed mechanism, seek source-optimal rho<1 at larger T or other source-approved parameters. Do not secretly replace baseline tuning with rho=.5.
3. **Statistics:** two seeds per world and three hand-designed worlds do not justify CIs or generalization. Negative results remain valid descriptive outcomes for *these* runs.
4. **Outcome fairness:** equal T decisions and same source-clock/noise hashing; cover policy and continuation use same Bernstein index but different arms. The diagnostic fixed grid is an alternate baseline, not a clean ablation isolating Search.
5. **Geometry:** good 2D optimum at (.25,.75) lies off the source rho1 midpoint, making positive linear approximation regret inevitable for baseline. Need stratified peak-location shifts on held-out worlds in future design.
6. **Web relevance:** synthetic continuum decision environment only; no real ad policy uplift evidence and no source-equivalent author GADU statement. Do not insert into WWW article without signoff.

**Decision:** R&D pilot technically completed; empirical hypothesis did not succeed under the selected source tuning, and its anticipated mechanism is absent. Handoff as *exploratory counterexample to an intuition*, not as a universal impossibility. STOP additional same-cell seeds; first redesign with a feasible opportunity for high-dimensional Cover exploration. Maintain E03/E04 datasets immutable.
