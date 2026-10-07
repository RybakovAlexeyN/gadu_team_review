# GADU — Variance-Sensitive Delayed Certification

> **Cold-start summary.** This repository is the post–29 September scientific review packet for the current GADU paper. It is designed so that a coauthor or senior reviewer can understand the scientific delta without reconstructing the project history first.

**Baseline manuscript:** *Gap-Adaptive Family Certification for Continuum Bandits with Delayed Positive-Only Feedback*.

**Current reader-first candidate:** variance-sensitive certified continuum optimization  
$\rightarrow$ delayed positive-only execution  
$\rightarrow$ best-family / GADU composition  
$\rightarrow$ controlled evidence.

**Status:** the candidate is mathematically specified and internally adversarially reviewed, but it is **not yet human-approved as the final paper result**. The remaining high-value step is independent coauthor review with **PASS / FIX / BLOCK** verdicts.

---

## 30-second orientation

The paper studies a learner that must choose both

- a discrete family $i\in[K]$; and
- a continuous configuration $x\in X_i$

while successes arrive with delay and failures produce no event.

The practical difficulty is that before the attribution window closes, **silence is ambiguous**: it may mean failure, or a success still in flight.

After the 29 September call, three concrete gaps had to be closed:

1. the manuscript contained an undefined “wait for maturation” step even though the system must deploy something every round;
2. the executed certification backend was not exploiting the local Bernoulli variance structure;
3. synthetic evidence alone was not enough to understand whether the delayed-positive model matches real attribution logs.

The current candidate addresses those three points separately:

| Question | Current answer | Status |
|---|---|---|
| What does the system do while feedback matures? | [VS-Certify-Delayed](ALGORITHM.md) emits one legal deployment every round and never turns unresolved silence into zero. | **Executable specification** |
| What is the main statistical contribution? | A variance-sensitive Bernoulli certified-Lipschitz upper bound, plus a scoped fine-gap lower bound with the same local information structure. | **Theorem candidate — human review pending** |
| Does the mechanism help in sparse-positive regimes? | Controlled component benchmark shows strong instance-dependent sample savings, with explicit counterexamples to uniform dominance. | **Narrow computational evidence** |
| Does a real attribution log satisfy the naive iid row-level model? | No: a Criteo slice falsifies “one positive row = one independent physical success.” | **Model-fit falsification evidence** |
| Is novelty fully closed? | Not yet. Final literature kill-pass and coauthor judgment remain. | **Open** |
| Is there one accepted final manuscript? | Not yet. The integrated reader-first rewrite and full coauthor read remain. | **Open** |

---

## What changed relative to the baseline manuscript?

This is the most important context for a reader who already knows the earlier GADU draft.

### Baseline executed certification route

For a source round $s$ and attribution window $w$, the baseline manuscript uses the inverse-weighted pseudo-reward

$$
Y_s^{(w)}
=
\frac{\mathbf 1\{Z_s=1,\ D_s\le w\}}{q_w},
\qquad
q_w=F(w)>0.
$$

It is unbiased for the latent success probability $f_i(x)$, but takes values in $[0,1/q_w]$. The executed dyadic certification route therefore uses a Hoeffding-style range bound and carries a $q_w^{-2}$ query dependence.

The baseline manuscript already recognizes narrower raw-Bernoulli / $q_w^{-1}$ behavior, so **the factor $q_w^{-1}$ by itself is not the novelty claim**.

### Current candidate

Instead, work directly with the matured Bernoulli indicator

$$
B_s^{(w)}
=
\mathbf 1\{Z_s=1,\ D_s\le w\}
\sim
\mathrm{Bernoulli}\!\left(q_w f_i(x_s)\right).
$$

Define

$$
g_i(x)=q_w f_i(x).
$$

Because $q_w>0$ is common across families,

$$
\operatorname*{arg\,max}_i\sup_{x\in X_i}g_i(x)
=
\operatorname*{arg\,max}_i\sup_{x\in X_i}f_i(x).
$$

The new statistical core combines

$$
\text{empirical-Bernstein confidence}
\longrightarrow
\text{Lipschitz cell envelopes}
\longrightarrow
\text{safe pruning}
\longrightarrow
\text{family certification}.
$$

The local center cost has the variance-sensitive form

$$
\frac{g(c)}{a_h^2}
+
\frac{1}{a_h},
$$

which is the mechanism behind the instance-dependent gain in sparse-positive regimes.

---

## Main theoretical candidate

For a single $L_g$-Lipschitz Bernoulli mean function $g:[0,1]^d\to[0,1]$, define

$$
g^\star=\max_x g(x),
\qquad
\Delta_g(x)=g^\star-g(x).
$$

The current upper theorem has the shape

$$
N
\le
C_d\,\Lambda
\left[
1+
L_g^d
\int
\left(
\frac{g(x)}{(\Delta_g(x)+\varepsilon)^{d+2}}
+
\frac{1}{(\Delta_g(x)+\varepsilon)^{d+1}}
\right)\,dx
\right].
$$

The companion lower bound recovers the same local Bernoulli information structure on a **restricted fine-gap region**, but keeps three limitations explicit:

- strict roughness slack;
- logarithmic layer-selection loss;
- no full minimax claim over all of $X$.

Start here:

- [Upper theorem](theory/UPPER_THEOREM.md)
- [Upper proof roadmap](theory/UPPER_PROOF.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Lower proof outline](theory/LOWER_PROOF.md)

---

## Executable delayed algorithm

The current procedure is [VS-Certify-Delayed](ALGORITHM.md):

~~~text
active dyadic cells
→ designated sampling
→ synchronized checkpoint
→ w legal filler deployments
→ finalize matured designated outcomes
→ empirical-Bernstein confidence
→ Lipschitz envelopes
→ prune / split
→ family certificate
~~~

The key invariant is:

> **Unresolved silence is never converted into zero.**

At every synchronized checkpoint, the active set is frozen, designated pulls are generated, exactly $w$ legal filler deployments are issued, and only then are the designated outcomes finalized for the estimator.

On a completed non-truncated execution,

$$
T_{\mathrm{cal}}
=
D+w\sum_h C_h.
$$

A statistical family certificate is then translated from the observed scale $g_i=q_wf_i$ back to the latent scale before entering the existing GADU continuation/fallback interface.

The new backend is **additive**. It does not automatically rewrite or improve every theorem in the baseline manuscript.

- [Algorithm](ALGORITHM.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)
- [Algorithm-to-proof map](theory/ALGORITHM_PROOF_MAP.md)

---

## Evidence

### Controlled component benchmark

The benchmark compares the current inverse-weighted Hoeffding confidence route with the variance-sensitive empirical-Bernstein mechanism on the same Bernoulli stream.

For the predeclared sparse-positive regimes

$$
q\in\{0.1,0.2\},
\qquad
f\in\{0.05,0.1\},
$$

the mean designated-sample ratio is

$$
\operatorname{mean}\!\left(
\frac{N_{\mathrm{VS}}}{N_{\mathrm H}}
\right)
=
0.122852.
$$

But the same frozen grid contains regimes with

$$
\frac{N_{\mathrm{VS}}}{N_{\mathrm H}}
=
2.
$$

So the supported statement is:

> **instance-dependent sparse-positive sample efficiency**, not uniform superiority.

[Controlled benchmark →](experiments/README.md)

### Real-data model-fit check

A deterministic 1,200-row Criteo Attribution prefix contains:

| Quantity | Observed value |
|---|---:|
| Impression rows | 1,200 |
| Positive impression rows with valid delay | 61 |
| Unique physical conversions | 55 |
| Maximum positive-row multiplicity for one conversion | 3 |

Therefore

$$
\text{one positive impression row}
\not\equiv
\text{one independent physical Bernoulli success}.
$$

This is **model-fit / attribution falsification evidence only**. It is not end-to-end GADU evaluation, policy comparison, population estimation of $q_w$, or validation of the common delay-law assumption.

[Criteo model-fit evidence →](data/CRITEO_MODEL_FIT.md)

---

## What is actually still open?

A cold reader should distinguish **specified**, **supported**, and **accepted**.

| Object | Current state | What would close it? |
|---|---|---|
| Executable algorithm | Fully specified in the review packet | Independent round-by-round audit |
| Upper theorem | Structured proof candidate | Human check of concentration, packing-to-volume, dyadic summation, coarse levels |
| Lower theorem | Structured scoped candidate | Human check of bumps, Bernoulli KL, change of measure, layer aggregation |
| Delayed/GADU bridge | Explicit composition candidate | Human source-ownership / clean-restart audit |
| Component benchmark | Reproducible narrow experiment | No broader claim should be inferred |
| Criteo evidence | Reproducible model-fit falsifier | No policy claim should be inferred |
| Novelty framing | Conservative but not closed | Final literature kill-pass |
| Final manuscript | Not frozen | One reader-first integrated draft + full coauthor read |

The main scientific decision is therefore not “does the code run?” but:

> **Does any substantive mathematical or novelty BLOCK remain, and is this theorem pair strong enough to be the paper’s primary story?**

---

## Read this repository by available time

### 5 minutes

Read this README only. You should leave knowing:

- the problem;
- what changed after 29 September;
- the proposed contribution;
- what is evidence versus theorem;
- what is still unverified.

### 15 minutes

Read:

1. [ALGORITHM.md](ALGORITHM.md)
2. [UPPER_THEOREM.md](theory/UPPER_THEOREM.md)
3. [DELAYED_GADU.md](theory/DELAYED_GADU.md)

Then answer: **Is the new scientific object coherent enough to deserve full proof review?**

### 45–60 minutes

Read:

1. [MATH_REVIEW.md](MATH_REVIEW.md)
2. [UPPER_PROOF.md](theory/UPPER_PROOF.md)
3. [LOWER_THEOREM.md](theory/LOWER_THEOREM.md)
4. [LOWER_PROOF.md](theory/LOWER_PROOF.md)
5. [REVIEW_REQUEST.md](REVIEW_REQUEST.md)

Return **PASS / FIX / BLOCK** for each mathematical block.

### Paper-story review

Read:

- [PAPER_REVIEW.md](PAPER_REVIEW.md)
- [Post-call task pool](TASK_POOL.md)

Then decide whether the reader-first hierarchy

$$
\text{variance-sensitive continuum certification}
\to
\text{delayed positive-only specialization}
\to
\text{GADU composition}
\to
\text{controlled evidence}
$$

is the right paper story.

---

## What this repository does not claim

It does **not** claim:

- that the new method is always better than Hoeffding;
- that $q_w^{-1}$ scaling is new by itself;
- first stochastic certified Lipschitz optimization;
- first variance-adaptive bandit method;
- a full minimax characterization;
- automatic improvement of the baseline GADU Theorem 1/8 or scheduler theorem;
- end-to-end GADU validation on Criteo;
- any unsupported “first” claim.

For the exact adversarial checklist, use [REVIEW_REQUEST.md](REVIEW_REQUEST.md).
