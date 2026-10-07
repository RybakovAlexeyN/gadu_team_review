# Paper Story Review

The central review question is:

> **Does the current candidate form one clear, defensible paper?**

This is a story/claims review, not a substitute for the mathematical review in [`MATH_REVIEW.md`](MATH_REVIEW.md).

## Scientific story in one paragraph

We study certified optimization and family selection when positive outcomes may be rare and feedback arrives after a delay. The current Hoeffding-style route pays a globally conservative statistical price. The new variance-sensitive backend exploits local Bernoulli information and can require substantially fewer designated observations in sparse-positive regimes, while not being uniformly better. The statistical core is coupled to an executable delayed procedure in which every calendar round has a legal deployment, unresolved silence is never interpreted as failure, and family certificates are passed conservatively through the existing GADU certified-optimizer interface.

## Scientific objects under review

### Theory

- [Variance-sensitive upper theorem](theory/UPPER_THEOREM.md)
- [Fine-gap lower theorem](theory/LOWER_THEOREM.md)
- [Delayed execution and GADU composition](theory/DELAYED_GADU.md)

### Controlled evidence

The controlled component benchmark compares the variance-sensitive confidence mechanism against the current Hoeffding-style mechanism on the same Bernoulli stream.

In the predeclared sparse-positive regimes,

$$
\operatorname{mean}\!\left(\frac{N_{\mathrm{VS}}}{N_{\mathrm H}}\right)
\approx 0.123.
$$

But the frozen grid also contains regimes with

$$
\frac{N_{\mathrm{VS}}}{N_{\mathrm H}}=2.
$$

The supported claim is therefore **instance-dependent sparse-positive sample efficiency**, not uniform superiority.

[Controlled benchmark →](experiments/README.md)

### Real-data model-fit evidence

On the 1,200-row Criteo slice, one physical conversion may be attached to multiple positive impression rows. Therefore

$$
\text{one positive row}
\not\equiv
\text{one independent Bernoulli success}.
$$

Criteo is useful here as attribution/model-fit falsification evidence, not as an end-to-end GADU policy benchmark.

[Criteo model-fit evidence →](data/CRITEO_MODEL_FIT.md)

## What the reviewer should decide

1. **Yes / no:** does this form one coherent paper story?
2. Is the main contribution clearly distinguishable from the historical GADU-Cover result?
3. Is novelty stated narrowly enough to survive comparison with adjacent certified-continuum, variance-dependent identification, and delayed-bandit work?
4. Should the upper/lower theorem pair be the main theoretical result in the body?
5. Does the experiment section support the theorem rather than promise more?
6. Are the three evidence types kept distinct?
   - theorem/proof;
   - controlled component evidence;
   - real-data model-fit/falsification evidence.
7. What are the 2–3 mandatory changes to the abstract, contribution bullets, or section order before a full coauthor read?

## Claims that must remain out of scope

Do not approve wording that implies:

- uniform superiority over Hoeffding;
- a novel $q_w^{-1}$ law by itself;
- a full minimax characterization;
- automatic improvement of the existing GADU Theorem 1/8 or Theorem 9;
- closure of unrelated moving-center regret gaps;
- end-to-end real-data GADU validation;
- an unsupported “first” claim.

If the mathematics receives PASS, the next writing step is to build the manuscript around the story that survives this review rather than around the chronology of the project.