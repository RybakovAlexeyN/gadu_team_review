# GADU — Variance-Sensitive Delayed Certification

This repository is the **team-facing scientific review packet** for the current GADU candidate. The central question is whether we can certify the globally best family over a continuous control space when positive outcomes are rare, delayed, and only become attributable after a fixed window.

The current candidate combines a variance-sensitive certified Lipschitz optimizer, an executable delayed positive-only realization, a scoped fine-gap lower bound, and conservative integration with the existing GADU certified-optimizer interface.

> **Review status.** The candidate is not yet accepted as a final paper result. Independent coauthor review is still required; reviewers should return **PASS / FIX / BLOCK** for the mathematical and paper-level objects linked below.

## The problem

There are $K$ families. Family $i$ has a continuous domain

$$
X_i=[0,1]^{d_i},
$$

and an unknown latent reward function

$$
f_i:X_i\to[0,1].
$$

A deployment at source round $s$ may generate a positive event $Z_s=1$ after delay $D_s$. For a fixed attribution window $w$, the matured positive-only observation is

$$
B_s^{(w)} =
\mathbf 1\{Z_s=1,\ D_s\le w\}.
$$

Under the current fresh-outcome model,

$$
B_s^{(w)}\sim\mathrm{Bernoulli}\!\left(q_w f_i(x_s)\right),
\qquad
q_w=F(w)>0.
$$

Define the observed-scale surface

$$
g_i(x)=q_w f_i(x).
$$

Because the same positive factor $q_w$ multiplies every family,

$$
\operatorname*{arg\,max}_i\sup_{x\in X_i}g_i(x) =
\operatorname*{arg\,max}_i\sup_{x\in X_i}f_i(x).
$$

The task is therefore to **certify the best family**, not merely estimate one point, while never interpreting unresolved delayed silence as an observed failure.

## Main idea

The executable procedure is [`VS-Certify-Delayed`](ALGORITHM.md):

```text
active dyadic cells
→ designated sampling
→ synchronized checkpoint
→ w legal filler rounds
→ finalize matured designated outcomes
→ empirical-Bernstein confidence
→ Lipschitz envelopes
→ prune / split
→ family certification
```

The statistical core works directly with the Bernoulli surface $g_i$. The delayed layer determines **when** an observation is legally finalized; the geometric layer determines **where** the optimizer refines.

The most important execution invariant is:

> **Unresolved silence is never converted into zero.**

## Main upper bound

For a single family, let $g:X\to[0,1]$ be $L_g$-Lipschitz, let

$$
g^\star=\max_{x\in X}g(x),
\qquad
\operatorname{gap}(x)=g^\star-g(x),
$$

and let $\varepsilon$ be the target certificate error. The current upper theorem has the form

$$
N
\le
C_d\,\Lambda(\varepsilon,\delta,L_g,d)
\left[
1+
L_g^d
\int_X
\left(
\frac{g(x)}{(\operatorname{gap}(x)+\varepsilon)^{d+2}} +
\frac{1}{(\operatorname{gap}(x)+\varepsilon)^{d+1}}
\right)\,dx
\right].
$$

The two local terms come from the empirical-Bernstein sample cost at a center:

$$
\frac{g(c)}{a_h^2} +
\frac{1}{a_h}.
$$

The first term is variance/mean-sensitive for Bernoulli observations; the second is the linear empirical-Bernstein correction. The theorem is **instance-dependent** and does not claim optimal constants or uniform improvement over Hoeffding.

- [Upper theorem](theory/UPPER_THEOREM.md)
- [Upper proof roadmap](theory/UPPER_PROOF.md)

## Fine-gap lower bound

The lower-bound construction recovers the same local Bernoulli information structure on a restricted fine-gap region. In the two-family base instance, with gap function $G(x)$, the target functional is

$$
S^d
\int_{A_{\mathrm{fine}}}
\left(
\frac{\mu(x)}{G(x)^{d+2}} +
\frac{1}{G(x)^{d+1}}
\right)\,dx,
$$

up to dimension-dependent constants, the confidence term, and an explicit dyadic layer-selection logarithmic loss.

The result is deliberately scoped:

- **fine-gap region only**;
- **strict roughness slack** $S=L-L_0>0$;
- **logarithmic layer-selection loss**;
- **no full-$X$ minimax characterization**.

- [Lower theorem](theory/LOWER_THEOREM.md)
- [Lower proof outline](theory/LOWER_PROOF.md)

## Delayed execution and GADU composition

The delayed certifier emits one legal deployment every calendar round. At each synchronized checkpoint it generates designated pulls, freezes the active set, performs exactly $w$ legal filler deployments, then finalizes the designated outcomes whose attribution windows have matured.

On a completed non-truncated path,

$$
T_{\mathrm{cal}} =
D+w\sum_h C_h,
$$

where $D$ is the number of designated source pulls and $C_h$ is the number of completed synchronized checkpoints at depth $h$.

A scaled family certificate

$$
\ell_i^g
\le
g_i(z_i)
\le
g_i^\star
\le
U_i^g,
\qquad
0\le g_i^\star-g_i(z_i)\le\xi_i^g
$$

is translated back to latent scale by

$$
\ell_i=\max\{0,\ell_i^g/q_w\},
\qquad
U_i=\min\{1,U_i^g/q_w\},
\qquad
\Xi_i=\min\{1,\xi_i^g/q_w\}.
$$

The downstream continuation gate must use the **latent-scale** error $\Xi_i$. The VS backend is an additional certified backend; it does not silently replace the current GADU Theorem 1/8 or Theorem 9.

- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)
- [Algorithm-to-proof map](theory/ALGORITHM_PROOF_MAP.md)

## Controlled evidence

The controlled component benchmark compares inverse-weighted Hoeffding confidence with the variance-sensitive empirical-Bernstein mechanism on the **same Bernoulli stream**.

For the predeclared sparse-positive regimes $q\in\{0.1,0.2\}$ and $f\in\{0.05,0.1\}$,

$$
\operatorname{mean}\!\left(\frac{N_{\mathrm{VS}}}{N_{\mathrm H}}\right) =
0.122852.
$$

The worst sparse-case ratio in that set is approximately $0.194$.

The same grid also contains counterexamples to uniform dominance: some regimes have

$$
\frac{N_{\mathrm{VS}}}{N_{\mathrm H}}=2.
$$

Therefore the supported empirical interpretation is:

> **instance-dependent sparse-positive sample efficiency**, not uniform superiority.

[Controlled benchmark →](experiments/README.md)

## Real-data model-fit evidence

A deterministic 1,200-row prefix of the public Criteo Attribution dataset contains:

| Quantity | Observed value |
|---|---:|
| Impression rows | 1,200 |
| Positive impression rows with valid delay | 61 |
| Unique physical conversions | 55 |
| Maximum positive-row multiplicity for one conversion | 3 |

Thus the naive mapping

$$
\text{one positive impression row}
\equiv
\text{one independent Bernoulli success}
$$

is false on this slice.

Criteo is used here as **model-fit / attribution falsification evidence**, not as an end-to-end GADU policy benchmark, policy comparison, population estimate of $q_w$, or validation of a common action-independent delay law.

[Criteo model-fit evidence →](data/CRITEO_MODEL_FIT.md)

## Review status

The highest-value remaining task is independent adversarial review of the exact candidate:

| Review object | What to attack | Entry point |
|---|---|---|
| Canonical algorithm | Executability, delayed semantics, source ownership | [ALGORITHM.md](ALGORITHM.md) |
| Upper theorem | Confidence, packing, dyadic sum, coarse levels | [MATH_REVIEW.md](MATH_REVIEW.md) |
| Lower theorem | Bumps, KL, change of measure, scope | [MATH_REVIEW.md](MATH_REVIEW.md) |
| Paper story | Novelty, claims, contribution hierarchy | [PAPER_REVIEW.md](PAPER_REVIEW.md) |
| Full adversarial checklist | Try to reject the candidate | [REVIEW_REQUEST.md](REVIEW_REQUEST.md) |

### What this repository does **not** claim

It does not claim:

- that the new method is always better than Hoeffding;
- that the $q_w^{-1}$ scaling is new by itself;
- a full minimax characterization;
- end-to-end GADU validation on Criteo;
- automatic replacement of the current GADU flagship guarantees;
- any unsupported “first” claim.

The key remaining question is:

> **Is there any substantive BLOCK that prevents this candidate from entering the final manuscript?**