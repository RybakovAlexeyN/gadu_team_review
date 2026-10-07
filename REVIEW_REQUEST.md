# Adversarial Review Request

Please review the current candidate **as if you were trying to reject it**.

Return one of **PASS / FIX / BLOCK** for each block below. A BLOCK should identify the exact failed theorem step, claim, or interface and the smallest repair that would clear it.

## 1. Upper theorem

Review the full chain:

$$
\text{empirical Bernstein confidence}
\to
\text{valid cell envelopes}
\to
\text{safe pruning}
\to
\text{near-optimal sampled cells}
$$

$$
\to
\text{packing}
\to
\text{packing-to-volume}
\to
\text{dyadic summation}
\to
\text{sample-complexity integral}.
$$

Questions:

- Is the simultaneous confidence event valid under adaptive cell creation and stopping?
- Is every sampled child center provably near-optimal, not only every surviving parent cell?
- Is the packing-to-volume inequality in the correct direction and at the correct scale?
- Are coarse levels absorbed without hiding a dependence that changes the theorem?

## 2. Lower theorem

Review:

$$
\text{hard alternatives}
\to
\text{Bernoulli KL}
\to
\text{adaptive change of measure}
\to
\text{disjoint packing}
\to
\text{layer aggregation}
\to
\text{fine-gap integral}.
$$

Questions:

- Do all perturbed functions remain in the declared Lipschitz class?
- Does each alternative actually flip the best family?
- Is the KL upper bound valid in the stated Bernoulli range?
- Is the logarithmic layer-selection loss explicit?
- Is the theorem correctly restricted to the fine-gap region?

## 3. Delayed execution and GADU integration

Check:

- one legal deployment is emitted every calendar round;
- unresolved silence is never converted into a zero observation;
- filler feedback is excluded from the designated estimator;
- the calendar identity
  $$
  T_{\mathrm{cal}}=D+w\sum_h C_h
  $$
  is correct on the stated completed paths;
- source ownership is clean at fallback/restart;
- the continuation gate uses latent-scale error $\Xi_i$, not scaled error $\xi_i^g$.

## 4. Claims and novelty

Flag any wording that implies more than is proved.

This packet does **not** claim:

- first stochastic certified Lipschitz optimizer;
- first variance-adaptive bandit method;
- novelty of $q_w^{-1}$ itself;
- full minimax matching;
- uniform superiority over Hoeffding;
- end-to-end validation on Criteo.

## Requested output

| Block | Verdict | Exact issue / smallest repair |
|---|---|---|
| Canonical algorithm | PASS / FIX / BLOCK | ... |
| Upper theorem | PASS / FIX / BLOCK | ... |
| Lower theorem | PASS / FIX / BLOCK | ... |
| Delayed / GADU bridge | PASS / FIX / BLOCK | ... |
| Claims / novelty | PASS / FIX / BLOCK | ... |