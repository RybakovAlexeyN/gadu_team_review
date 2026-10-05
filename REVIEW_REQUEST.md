# Review request

Please review the current candidate as if you were trying to reject it.

## 1. Upper theorem

Check the full chain:

empirical Bernstein confidence -> valid cell envelopes -> safe pruning -> near-optimal sampled cells -> packing -> packing-to-volume -> dyadic summation -> final sample-complexity integral.

Questions:
- Is the simultaneous confidence event valid under adaptive cell creation/stopping?
- Is every sampled child center provably near-optimal, not only every surviving cell?
- Is the packing-to-volume inequality in the correct direction with the correct scale factor?
- Are coarse levels absorbed without hiding a dependence that changes the theorem?

## 2. Lower theorem

Check:

hard alternatives -> Bernoulli KL -> adaptive change of measure -> disjoint packing -> layer aggregation -> fine-gap integral.

Questions:
- Do all perturbed functions stay in the declared Lipschitz class?
- Does each alternative actually flip the best family?
- Is the KL upper bound valid in the stated Bernoulli range?
- Is the logarithmic layer-selection loss explicit?
- Is the theorem correctly restricted to the fine-gap region?

## 3. Delayed execution and GADU integration

Check:
- one legal deployment is emitted every calendar round;
- unresolved silence is never converted into a zero observation;
- filler feedback is excluded from the designated estimator;
- the calendar identity is correct;
- source ownership is clean at fallback/restart;
- the continuation gate uses latent-scale error, not scaled error.

## 4. Claims and novelty

Please flag any wording that implies more than is proved.

In particular, this packet does not claim:
- first stochastic certified Lipschitz optimizer;
- first variance-adaptive bandit method;
- novelty of `q^-1` itself;
- full minimax matching;
- uniform superiority over Hoeffding;
- end-to-end validation on Criteo.
