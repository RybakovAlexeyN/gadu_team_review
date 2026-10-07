# Delayed Positive-Only Execution and GADU Composition

This note records the execution contract and the minimal composition argument needed for review.

For the reader-facing procedure, start with [`VS-Certify-Delayed`](../ALGORITHM.md).

## Two clocks

The delayed problem has two distinct clocks:

1. **deployment clock** — the system must emit a legal action every calendar round;
2. **maturation / information clock** — evidence from an earlier source round becomes usable only after the observation rule resolves it.

The current algorithm makes both clocks explicit. It does not contain an unspecified “wait for feedback” action.

## Matured observation

For source round $s$, after age $w$, define

$$
B_s^{(w)} =
\mathbf 1\{Z_s=1,\ D_s\le w\}.
$$

Under the fresh-outcome model,

$$
B_s^{(w)}
\sim
\mathrm{Bernoulli}\!\left(q_w f(x_s)\right).
$$

Define

$$
g_i=q_w f_i.
$$

Because $q_w>0$ is common across families, this positive scaling preserves family ordering.

## Executable delayed certification

Take $w$ to be a nonnegative integer number of calendar rounds. If $w=0$, the flush is empty.

The delayed certifier:

1. maintains active dyadic cells;
2. samples designated cell centers to geometric cumulative targets $n_r=2^{r+1}$;
3. uses observable empirical-Bernstein confidence on finalized designated Bernoulli samples;
4. after the last designated source of a checkpoint, **freezes the active set** and performs exactly $w$ legal filler deployments;
5. excludes filler feedback from the designated certification estimator;
6. finalizes designated Bernoulli outcomes only after the flush;
7. recomputes confidence intervals and Lipschitz cell bounds;
8. prunes impossible cells and splits survivors;
9. checks learner-computable family separation;
10. returns `NOT_CERTIFIED(accounting)` if the predeclared hard calendar cutoff is exhausted before an accepted certificate.

> **Invariant:** unresolved silence is never encoded as zero, including at the hard cutoff.

If $D$ is the total number of designated source pulls and $C_h$ is the number of synchronized checkpoints at depth $h$, then on a completed, non-truncated path,

$$
T_{\mathrm{cal}} =
D+w\sum_h C_h.
$$

## Certified-optimizer interface

A `CERTIFIED` output is a statistical family certificate, not an automatic GADU commit.

Suppose the scaled optimizer returns

$$
\ell_i^g
\le
g_i(z_i)
\le
g_i^\star
\le
U_i^g,
$$

and

$$
0\le g_i^\star-g_i(z_i)\le\xi_i^g.
$$

For common known $q_w>0$, define

$$
\ell_i=\max\{0,\ell_i^g/q_w\},
\qquad
U_i=\min\{1,U_i^g/q_w\},
$$

and

$$
\Xi_i=\min\{1,\xi_i^g/q_w\}.
$$

Then

$$
\ell_i
\le
f_i(z_i)
\le
f_i^\star
\le
U_i,
$$

and

$$
0\le f_i^\star-f_i(z_i)\le\Xi_i.
$$

The continuation gate must use the **latent-scale** error $\Xi_i$, not the scaled error $\xi_i^g$.

## Additive preflight composition

Let $I_T$ be the immediate full-union certificate and let $C_T(u)$ be the compatible prefix certificate. For a predeclared cutoff $B$, define

$$
V_{\mathrm{fb}}(T,B) =
B+C_T(T-B).
$$

Enter the VS branch only if

$$
V_{\mathrm{fb}}(T,B)
\le
(1+\gamma)I_T.
$$

At a certification checkpoint $s\le B$, commit only if family separation holds and

$$
s+(T-s)\Xi_i
\le
V_{\mathrm{fb}}(T,B).
$$

The conservative continuation underlying this certificate is repeated deployment of the returned point $z_i$. Any different continuation requires a separately proved certificate no larger than this one.

If no certificate is accepted by $B$, or if the primitive returns `NOT_CERTIFIED(accounting)`, restart the frozen full-union fallback on the fresh remaining horizon.

All certification-owned source rounds — including filler rounds and later arrivals tagged to those sources — are excluded from fresh fallback statistics. Under the fresh-outcome model, future source outcomes after the clean restart are fresh conditional on the pre-cutoff history.

On the simultaneous good event, the entered branch is bounded by $V_{\mathrm{fb}}$. On the failure event, finite-horizon regret is at most $T$, yielding the additive $\delta_{\mathrm{vs}}T$ term.

## Scope

This composition result does not claim:

- uniform superiority over the existing backend;
- replacement of the current scheduler theorem;
- end-to-end regret optimality;
- that old Theorem 1/8 or Theorem 9 is automatically improved;
- that filler observations may be reused without a separate proof.