# Paper Story Review

This is the **paper-level decision page**. It asks whether the current scientific delta forms one clear, defensible paper story. It is not a substitute for the mathematical review in [MATH_REVIEW.md](MATH_REVIEW.md).

## Candidate paper in one sentence

> We derive a variance-sensitive certified optimizer for Bernoulli continuum problems, lift it to executable delayed positive-only feedback, and use it for conservative best-family certification inside GADU.

That sentence is the candidate story to attack.

## Why this could be a paper

The baseline executed certification route uses an inverse-weighted Hoeffding-style confidence mechanism. The new candidate works directly with the matured Bernoulli surface

$$
g_i(x)=q_w f_i(x),
$$

so local statistical cost can depend on the Bernoulli mean/variance rather than only on the inflated inverse-weighted range.

The strongest scientific object is the upper/lower theorem pair:

- an instance-dependent upper bound with local term
  $$
  rac{g(x)}{(Delta(x)+arepsilon)^{d+2}}
  +
  rac{1}{(Delta(x)+arepsilon)^{d+1}};
  $$
- a scoped fine-gap lower bound with the same local information structure, but with explicit roughness slack and logarithmic layer-selection loss.

The delayed layer is then an execution/composition result: it turns the statistical certificate into a legal online procedure without interpreting unresolved silence as failure.

## What is evidence, and what is not

| Evidence type | What it supports | What it does **not** support |
|---|---|---|
| Upper/lower theorem files | Mathematical candidate | Human acceptance before review |
| Controlled benchmark | Sparse-positive component efficiency in tested regimes | Uniform dominance or end-to-end regret superiority |
| Criteo audit | Model-fit falsification of naive iid row-level positives | Policy evaluation or validation of the common delay law |
| Delayed/GADU bridge | Executable composition candidate | Automatic improvement of every old GADU theorem |

## The central novelty question

The current novelty target is:

> **local Bernoulli mean/variance-sensitive statistical cost coupled with certified nonparametric Lipschitz continuum geometry, plus a scoped matching local-information lower structure and delayed positive-only execution lift.**

A reviewer should try to kill this by finding a known result that directly gives the same theorem under the same assumptions.

The novelty claim should be rejected or narrowed if the upper theorem is an immediate corollary of an existing certified heteroscedastic/variance-adaptive continuum theorem, or if the lower-bound structure is already standard in exactly this model.

## Three kill conditions

The current paper story should receive **BLOCK** if any of the following is true:

1. **Mathematical kill:** a core theorem or delayed-composition step fails and has no small repair.
2. **Novelty kill:** the main theorem pair is directly subsumed by prior work under the same model and scope.
3. **Story kill:** after correct scoping, the remaining contribution is too fragmented to support one paper-level message.

## What the reviewer should decide

Return short answers to these questions:

1. Does the theorem pair deserve to be the headline contribution?
2. Is the delayed positive-only layer a meaningful specialization/composition rather than a second competing paper story?
3. Is the empirical section appropriately narrow and useful?
4. Is any claim stronger than the evidence?
5. What are the **2–3 mandatory manuscript changes** before full coauthor reading?

## Claims that must remain out of scope

Do not approve wording that implies:

- uniform superiority over Hoeffding;
- novelty of $q_w^{-1}$ by itself;
- first stochastic certified Lipschitz optimization;
- first variance-adaptive bandit method;
- a full minimax characterization;
- automatic improvement of the baseline GADU Theorem 1/8 or scheduler theorem;
- closure of unrelated moving-center regret gaps;
- end-to-end real-data GADU validation;
- any unsupported “first” claim.

## Suggested paper hierarchy

If the scientific review survives, the default reader-first order is

$$
	ext{variance-sensitive certified continuum core}
	o
	ext{delayed positive-only specialization}
	o
	ext{best-family / GADU composition}
	o
	ext{controlled evidence}.
$$

Do not write the final manuscript as a chronology of how the project evolved.

## Review entry points

- [Upper theorem](theory/UPPER_THEOREM.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)
- [Controlled benchmark](experiments/README.md)
- [Criteo model-fit evidence](data/CRITEO_MODEL_FIT.md)
- [Adversarial review request](REVIEW_REQUEST.md)
