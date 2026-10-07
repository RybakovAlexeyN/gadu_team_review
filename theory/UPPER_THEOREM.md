# Variance-Sensitive Bernoulli Certified-Continuum Upper Bound

This note states the current **single-family** upper theorem used by the variance-sensitive certification backend.

## Setting

Let

$$
X=[0,1]^d,
$$

and let

$$
g:X\to[0,1]
$$

be $L_g$-Lipschitz in the $\ell_\infty$ norm, with a known valid bound $L_g\ge0$. A query at $x$ returns an independent Bernoulli observation with mean $g(x)$.

Define

$$
g^\star=\max_{x\in X}g(x),
\qquad
\mathrm{gap}(x)=g^\star-g(x).
$$

If $L_g=0$, then every point is optimal and no query is needed. Assume below that $L_g>0$.

## Dyadic and confidence convention

At depth $h$ use

$$
\rho_h=2^{-h-1},
\qquad
 a_h=\min\{1,L_g\rho_h\}.
$$

Refinement stops no later than the first level satisfying

$$
a_h\le\frac{2\varepsilon}{5}.
$$

For every possible depth-$h$ cell $I$ and geometric checkpoint $r$, preassign

$$
\eta_{h,I,r} =
\frac{36\delta}
{\pi^4\,2^{dh}(h+1)^2(r+1)^2}.
$$

The total confidence budget over all cells, depths, and checkpoints is at most $\delta$.

Define

$$
\lambda_{h,r}=\log\frac{6}{\eta_{h,I,r}},
\qquad
n_r=2^{r+1}.
$$

A deterministic checkpoint cap may be taken as the first $R_h$ for which

$$
n_r
\ge
4+
\frac{1024\lambda_{h,r}}{a_h^2} +
\frac{140\lambda_{h,r}}{a_h}.
$$

Define the explicit confidence factor

$$
\Lambda(\varepsilon,\delta,L_g,d) =
\max_{0\le h\le h_\varepsilon,\ 0\le r\le R_h}
\lambda_{h,r}.
$$

## Observable empirical-Bernstein radius

For $n\ge2$ finalized Bernoulli observations $Y_1,\dots,Y_n$, let

$$
V_n =
\frac{1}{n-1}
\sum_{j=1}^n
\left(Y_j-\overline Y_n\right)^2.
$$

The learner uses the computable radius

$$
\mathrm{rad}(n,V_n,\eta) =
\sqrt{\frac{2V_n\log(6/\eta)}{n}} +
\frac{7\log(6/\eta)}{3(n-1)}.
$$

The stopping rule depends only on this observable radius; the unknown mean appears only in the analysis.

## Procedure analyzed

The theorem analyzes the **single-family within-family core** used by [`VS-Certify-Delayed`](../ALGORITHM.md), not the multi-family delayed stopping rule itself.

Run the same dyadic resolution and pruning rule in the direct Bernoulli-oracle model until the first resolved depth satisfying

$$
a_h\le\frac{2\varepsilon}{5}.
$$

At that depth choose the sampled center $z$ attaining the largest lower confidence bound, and define

$$
\ell^g=\max_I \mathrm{LCB}(I),
\qquad
U^g=\max_I U_{\mathrm{cell}}(I),
$$

and

$$
\xi=\min\{1,U^g-\ell^g\}.
$$

On the simultaneous confidence event,

$$
g^\star-g(z)\le\xi\le\varepsilon.
$$

The multi-family delayed controller uses the same per-family state update, but may stop earlier when strict family separation is already available. Calendar delay is handled separately by the delayed execution proposition.

## Theorem — upper bound

For every target accuracy $\varepsilon\in(0,1]$ and confidence $\delta\in(0,1)$, the single-family core returns $(\widehat x,\xi)$ such that, with probability at least $1-\delta$,

$$
g^\star-g(\widehat x)\le\xi\le\varepsilon.
$$

Its number of Bernoulli observations satisfies

$$
N
\le
C_d\,\Lambda(\varepsilon,\delta,L_g,d)
\left[
1+
L_g^d
\int_X
\left(
\frac{g(x)}{(\mathrm{gap}(x)+\varepsilon)^{d+2}} +
\frac{1}{(\mathrm{gap}(x)+\varepsilon)^{d+1}}
\right)\,dx
\right],
$$

where $C_d$ depends only on the dimension and the fixed $\ell_\infty$/dyadic convention. No optimal-constant claim is made.


The strongest discrete intermediate form is

$$
N
\le
C
\sum_h
\sum_{c\in A_h}
\lambda_{h,r(c)}
\left[
\frac{g(c)}{a_h^2} +
\frac{1}{a_h}
\right],
$$

where $A_h$ is the set of all centers sampled at level $h$.

Every sampled center in the fine dyadic regime satisfies

$$
\mathrm{gap}(c)\le 6a_h.
$$

The clipped coarse levels $a_h=1$ are bounded separately and absorbed into the same target functional for $\varepsilon\le1$.

A center-wise designated-sample bound is

$$
N_c(h)
\le
4+
\frac{1024\,g(c)\,\Lambda}{a_h^2} +
\frac{140\,\Lambda}{a_h}.
$$

## Delayed positive-only specialization

For a fixed attribution window $w$, let

$$
g_i(x)=q_w f_i(x),
\qquad
q_w=F(w)>0.
$$

If $q_w$ is common across families and known in the main model, then

$$
\mathcal L_i^g=q_wL_i
$$

is a valid Lipschitz bound for $g_i$. For simultaneous family certification, preassign per-family risks $\delta_i>0$ with

$$
\sum_i\delta_i\le\delta_{\mathrm{cert}}.
$$

Define

$$
\Lambda_i =
\Lambda(q_w\varepsilon,\delta_i,q_wL_i,d_i).
$$

Then the latent-scale specialization is

$$
N_i(\varepsilon)
\le
C\,\Lambda_i
\left[
1+
\frac{L_i^{d_i}}{q_w}
\int_{X_i}
\left(
\frac{f_i(x)}{(\Delta_i(x)+\varepsilon)^{d_i+2}} +
\frac{1}{(\Delta_i(x)+\varepsilon)^{d_i+1}}
\right)\,dx
\right].
$$

The factor $q_w^{-1}$ is **not** claimed as novel by itself.

## Scope

This theorem does not claim:

- optimal constants;
- uniform superiority over Hoeffding;
- a full minimax characterization;
- novelty of the $q_w^{-1}$ scaling by itself;
- that the multi-family delayed controller has the same stopping rule as the single-family core.

[Proof roadmap →](UPPER_PROOF.md)  
[Algorithm →](../ALGORITHM.md)