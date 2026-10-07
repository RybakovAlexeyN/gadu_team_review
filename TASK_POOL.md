# Post-Call Task Pool — 29 September

This page answers one question:

> **What did the team ask for on 29 September, what exists now, and what is still blocking the paper?**

It is a coordination summary, not an additional theorem.

## Call-to-current status

| 29 September ask | Current artifact | Status | Residual gap |
|---|---|---|---|
| Turn the idea into a testable algorithm | [VS-Certify-Delayed](ALGORITHM.md) | **Specified** | Independent human round-by-round audit |
| Remove undefined “wait for maturation” semantics | [Delayed execution](theory/DELAYED_GADU.md) | **Specified** | Verify source ownership / clean restart |
| Run experiments once the algorithm is testable | [Controlled benchmark](experiments/README.md) | **Component test complete** | No end-to-end real-data policy claim |
| Find a real dataset and test model fit | [Criteo audit](data/CRITEO_MODEL_FIT.md) | **Falsification check complete** | Common delay law and policy validity remain unvalidated |
| Strengthen the paper beyond the old executed backend | [Upper theorem](theory/UPPER_THEOREM.md) + [lower theorem](theory/LOWER_THEOREM.md) | **Scientific candidate** | Human mathematical review + final novelty kill-pass |
| Read one coherent paper as a team | Reader-first hierarchy now documented in [README](README.md) and [PAPER_REVIEW](PAPER_REVIEW.md) | **Open** | One integrated manuscript + full coauthor read |

## What was actually unresolved on the call

The central execution objection was simple: the manuscript said “wait for maturation,” but a deployed system cannot have a calendar round with no action.

The current candidate resolves that by requiring:

- one legal deployment every calendar round;
- designated source pulls separated from filler deployments;
- exactly $w$ filler deployments after a synchronized checkpoint;
- unresolved silence never treated as zero;
- pruning/splitting only after designated outcomes are finalized;
- explicit calendar accounting;
- a hard cutoff returning NOT_CERTIFIED.

The second scientific opportunity was to avoid paying only for the inverse-weighted range. The current candidate works directly with

$$
B_s^{(w)}
\sim
\mathrm{Bernoulli}\!\left(q_wf_i(x_s)\right)
$$

and uses empirical-Bernstein confidence in the continuum certification geometry.

The third question was empirical: synthetic-only evidence was judged insufficient for understanding real attribution semantics. The Criteo audit now gives a **negative but useful** answer: one physical conversion may map to multiple positive impression rows, so the naive iid row-level mapping is invalid.

## What remains on the critical path

### 1. Human mathematical red-team

Highest-value objects:

- empirical-Bernstein confidence statement and constants;
- packing-to-volume conversion;
- dyadic summation;
- coarse-scale absorption;
- fine-gap lower-bound construction;
- delayed/GADU clean-restart composition.

Preferred output for every block:

- **PASS**
- **FIX**
- **BLOCK**

A BLOCK should name the exact failed step and the smallest repair.

[Mathematical review packet →](MATH_REVIEW.md)

### 2. Novelty and paper-story decision

The candidate should survive a final literature kill-pass around:

- heteroscedastic / variance-adaptive certified continuum optimization;
- stochastic Lipschitz fixed-confidence certification;
- Bernoulli local-variance continuum identification.

The paper-level question is whether the hierarchy

$$
\text{variance-sensitive continuum certification}
\to
\text{delayed positive-only specialization}
\to
\text{GADU composition}
\to
\text{controlled evidence}
$$

is the right primary story.

[Paper review →](PAPER_REVIEW.md)

### 3. One integrated manuscript

The review repository contains the scientific delta, not a frozen final manuscript.

Before submission:

- freeze the theorem statements and Algorithm 1;
- integrate one reader-first draft;
- ensure limitations sit next to the corresponding claims;
- complete the full coauthor read;
- run final PDF / numbering / bibliography / figure QA;
- freeze one submission SHA/version.

## Requested coauthor decision

The next team decision should answer exactly:

1. **Is there a mathematical BLOCK?**
2. **Is the variance-sensitive theorem pair strong enough to be the headline contribution?**
3. **Does the delayed/GADU bridge preserve the intended semantics without overclaiming?**
4. **What exact edits are mandatory before the integrated manuscript is frozen?**
