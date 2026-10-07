# Upper-Bound Proof Roadmap

This file records the proof obligations for the **single-family within-family core** used by `VS-Certify-Delayed`.

The delayed multi-family controller has a different stopping rule. Its extra obligations — maturation timing, family separation, calendar accounting, and source ownership — are tracked separately in [`ALGORITHM_PROOF_MAP.md`](ALGORITHM_PROOF_MAP.md) and [`DELAYED_GADU.md`](DELAYED_GADU.md).

Throughout, let

$$
X=[0,1]^d,
\qquad
g^\star=\max_{x\in X}g(x),
\qquad
\mathrm{gap}(x)=g^\star-g(x),
$$

and

$$
\rho_h=2^{-h-1},
\qquad
a_h=\min\{1,L_g\rho_h\}.
$$

At every active center on depth $h$, the core resolves the center only when

$$
\mathrm{rad}_I\le\frac{a_h}{8}.
$$

## Lemma A — simultaneous empirical-Bernstein confidence

For every possible depth-$h$ dyadic cell $I$ and checkpoint $r$, preassign

$$
\eta_{h,I,r} =
\frac{36\delta}
{\pi^4\,2^{dh}(h+1)^2(r+1)^2}.
$$

There are exactly $2^{dh}$ possible cells at depth $h$. Hence

$$
\sum_{h,I,r}\eta_{h,I,r} =
\frac{36\delta}{\pi^4}
(\sum_{h\ge0}\frac1{(h+1)^2})
(\sum_{r\ge0}\frac1{(r+1)^2}) =
\delta.
$$

For $n\ge2$ Bernoulli observations at a center, use

$$
\mathrm{rad}(n,V,\eta) =
\sqrt{\frac{2V\log(6/\eta)}{n}} +
\frac{7\log(6/\eta)}{3(n-1)}.
$$

After the node/checkpoint allocation and a union bound, there is one event $\mathcal E_{\mathrm{conf}}$ with probability at least $1-\delta$ on which every confidence interval actually used by the adaptive algorithm is valid:

$$
|\widehat g_I-g(c_I)|
\le
\mathrm{rad}_I.
$$

Preallocating risk to **all possible cells and checkpoints** is what makes adaptive activation harmless here.

## Lemma B — every active center resolves in finite checkpoints

Fix a center $c$ at depth $h$, write

$$
\mu=g(c),
\qquad
\lambda=\log(6/\eta).
$$

Using the supporting sample-variance comparison from the frozen concentration audit, a sufficient sample size is

$$
n
\ge
2+
\frac{512\mu\lambda}{a_h^2} +
\frac{70\lambda}{a_h}
$$

for the observable radius to be at most $a_h/8$ on the supporting concentration event.

Because the algorithm samples only at geometric cumulative targets

$$
n_r=2^{r+1},
$$

the first target above this sufficient size overshoots by less than a factor two. Hence the actual designated count at resolution satisfies

$$
N_c(h)
\le
4+
\frac{1024\,g(c)\,\Lambda}{a_h^2} +
\frac{140\Lambda}{a_h}.
$$

Since $g(c)\le1$, the deterministic checkpoint cap $R_h$ in the theorem is sufficient for every center. Thus, in the direct-oracle core with no hard cutoff, the inner checkpoint loop terminates at every finite depth.

The unknown mean $g(c)$ appears only in this **analysis bound**. The learner stops from the observable radius.

## Lemma C — valid cell upper envelope

Let $I$ be a depth-$h$ cell with center $c_I$. For every $x\in I$,

$$
g(x)
\le
g(c_I)+L_g\rho_h.
$$

Because $g\in[0,1]$ and $a_h=\min\{1,L_g\rho_h\}$,

$$
\sup_{x\in I}g(x)
\le
\min\{1,g(c_I)+a_h\}.
$$

On $\mathcal E_{\mathrm{conf}}$,

$$
g(c_I)
\le
\widehat g_I+\mathrm{rad}_I,
$$

so

$$
U_{\mathrm{cell}}(I) =
\min\{1,\widehat g_I+\mathrm{rad}_I+a_h\}
$$

is a valid upper bound on the whole cell. Likewise,

$$
\mathrm{LCB}(I) =
\max\{0,\widehat g_I-\mathrm{rad}_I\}
\le
g(c_I).
$$

## Lemma D — a maximizer cell survives pruning

Let $I_h^\star$ be an active depth-$h$ cell containing a maximizer $x^\star$. Define

$$
\ell_h =
\max_I\mathrm{LCB}(I).
$$

By Lemma C,

$$
U_{\mathrm{cell}}(I_h^\star)
\ge
g^\star
\ge
\ell_h.
$$

Therefore the rule

$$
\text{remove }I
\quad\Longleftrightarrow\quad
U_{\mathrm{cell}}(I)<\ell_h
$$

cannot remove $I_h^\star$ on $\mathcal E_{\mathrm{conf}}$.

Thus at least one cell containing a global maximizer remains active at every refinement depth.

## Lemma E — every survivor center is $5a_h/2$ near-optimal

At a resolved level,

$$
\mathrm{rad}_I\le\frac{a_h}{8}
$$

for every active cell.

For the maximizer cell $I_h^\star$,

$$
\mathrm{gap}(c_{I_h^\star})\le a_h.
$$

On $\mathcal E_{\mathrm{conf}}$,

$$
\mathrm{LCB}(I_h^\star)
\ge
g(c_{I_h^\star})-2\mathrm{rad}_{I_h^\star}
\ge
g^\star-a_h-\frac{a_h}{4} =
g^\star-\frac{5a_h}{4}.
$$

Therefore

$$
\ell_h\ge g^\star-\frac{5a_h}{4}.
$$

If a cell $I$ survives, then $U_{\mathrm{cell}}(I)\ge\ell_h$. Also,

$$
U_{\mathrm{cell}}(I)
\le
g(c_I)+2\mathrm{rad}_I+a_h
\le
g(c_I)+\frac{5a_h}{4}.
$$

Combining the inequalities yields

$$
\mathrm{gap}(c_I)
\le
\frac{5a_h}{2}.
$$

This is the exact survivor constant used by the parent-to-child argument.

## Lemma F — every sampled child is $6a_h$ near-optimal

A sampled depth-$h$ cell is a child of a surviving depth-$(h-1)$ cell. For the dyadic convention,

$$
\lVert c_{\mathrm{child}}-c_{\mathrm{parent}}\rVert_\infty
\le
\rho_h.
$$

Hence

$$
g(c_{\mathrm{parent}})-g(c_{\mathrm{child}})
\le
a_h.
$$

For all depths,

$$
a_{h-1} =
\min\{1,2L_g\rho_h\}
\le
2a_h.
$$

Lemma E applied to the surviving parent gives

$$
\mathrm{gap}(c_{\mathrm{parent}})
\le
\frac{5a_{h-1}}{2}
\le
5a_h.
$$

Therefore

$$
\mathrm{gap}(c_{\mathrm{child}})
\le
\mathrm{gap}(c_{\mathrm{parent}})+a_h
\le
6a_h.
$$

This also covers the transition out of the clipped regime; the proof uses only $a_{h-1}\le2a_h$, not equality.

## Lemma G — certificate width at a resolved level

At a resolved depth define

$$
\ell^g =
\max_I\mathrm{LCB}(I),
\qquad
U^g =
\max_I U_{\mathrm{cell}}(I).
$$

As above,

$$
\ell^g
\ge
g^\star-\frac{5a_h}{4}.
$$

For every active cell,

$$
U_{\mathrm{cell}}(I)
\le
g(c_I)+2\mathrm{rad}_I+a_h
\le
g^\star+\frac{5a_h}{4}.
$$

Therefore

$$
U^g-\ell^g
\le
\frac{5a_h}{2}.
$$

If $z$ is the center attaining the largest LCB and

$$
\xi=\min\{1,U^g-\ell^g\},
$$

then on $\mathcal E_{\mathrm{conf}}$,

$$
g^\star-g(z)
\le
U^g-\ell^g =
\xi
\le
\frac{5a_h}{2}.
$$

Thus the direct-oracle core may stop at the first resolved depth satisfying

$$
a_h\le\frac{2\varepsilon}{5},
$$

and return a valid $\varepsilon$-certificate.

## Lemma H — discrete designated-sample bound

Let $A_h$ be the set of all centers actually sampled at depth $h$. Combining Lemma B across centers gives

$$
N
\le
C
\sum_h
\sum_{c\in A_h}
\lambda_{h,r(c)}
[
\frac{g(c)}{a_h^2} +
\frac{1}{a_h}
],
$$

up to the fixed initialization and geometric-overshoot constant.

By Lemma F, every fine-scale sampled center satisfies

$$
\mathrm{gap}(c)\le6a_h.
$$

This is the strongest discrete form feeding the geometric part of the proof.

## Lemma I — packing-to-volume conversion

At a fixed fine depth, distinct dyadic centers are separated in $\ell_\infty$ norm at scale

$$
2^{-h} =
\frac{2a_h}{L_g}.
$$

Choose disjoint $\ell_\infty$ balls around sampled centers with radius a fixed fraction of $a_h/L_g$.

Even at the boundary of $[0,1]^d$,

$$
\mathrm{vol}(B_\infty(c,r)\cap X)
\ge
r^d.
$$

For $x$ in the ball around $c$,

$$
g(c)\le g(x)+C a_h,
$$

and

$$
\mathrm{gap}(x)
\le
\mathrm{gap}(c)+C a_h
\le
C'a_h.
$$

Multiplying a center cost by the reciprocal ball volume yields

$$
\frac{g(c)}{a_h^2} +
\frac1{a_h}
\le
C_dL_g^d
\int_{B(c)}
[
\frac{g(x)}{a_h^{d+2}} +
\frac1{a_h^{d+1}}
]dx.
$$

Summing over disjoint balls converts the level-wise discrete sum to a level-wise integral.

## Lemma J — dyadic summation

If a point $x$ contributes at depth $h$, Lemmas F and I imply

$$
\mathrm{gap}(x)\le C a_h.
$$

Refinement stops when $a_h$ reaches the target scale $\Theta(\varepsilon)$. Thus the contributing dyadic scales satisfy, up to fixed constants,

$$
a_h
\ge
c\max\{\mathrm{gap}(x),\varepsilon\}.
$$

Geometric summation gives

$$
\sum_h\frac1{a_h^{d+2}}
\le
\frac{C}{(\mathrm{gap}(x)+\varepsilon)^{d+2}},
$$

and

$$
\sum_h\frac1{a_h^{d+1}}
\le
\frac{C}{(\mathrm{gap}(x)+\varepsilon)^{d+1}}.
$$

Substituting into Lemma I yields

$$
N
\le
C_d\Lambda
[
1+
L_g^d
\int_X
(
\frac{g(x)}{(\mathrm{gap}(x)+\varepsilon)^{d+2}} +
\frac1{(\mathrm{gap}(x)+\varepsilon)^{d+1}}
)dx
].
$$

## Lemma K — clipped coarse levels and flat case

The packing conversion is used only in the fine regime where the dyadic spatial scale is represented by $a_h/L_g$.

The finitely many clipped levels with $a_h=1$ are bounded separately and contribute at most

$$
O_d(1+L_g^d),
$$

which is absorbed into the theorem functional for $\varepsilon\le1$.

If $L_g=0$, the function is constant and the optimizer may return any point with certificate zero without querying.

## Proof chain

$$
\text{A: simultaneous confidence}
\to
\text{B: finite resolution and center cost}
\to
\text{C: valid cell envelopes}
\to
\text{D: maximizer survival}
$$

$$
\to
\text{E: survivor near-optimality}
\to
\text{F: sampled-child near-optimality}
\to
\text{G: }\varepsilon\text{-certificate}
\to
\text{H: discrete sample bound}
$$

$$
\to
\text{I: packing-to-volume}
\to
\text{J: dyadic summation}
\to
\text{K: coarse/flat cleanup}.
$$

## Remaining independent-review targets

The roadmap makes the intended constants and dependencies explicit, but it remains a review artifact rather than a substitute for independent proof checking.

Highest-value attacks:

1. re-derive the empirical-Bernstein concentration statement and the sample-size algebra in Lemmas A–B;
2. verify the packing-to-volume inequality in Lemma I, including boundary cells;
3. verify the pointwise dyadic summation in Lemma J;
4. verify that no hidden sample reuse is needed when child estimators start fresh;
5. check the coarse-level absorption in Lemma K for all allowed $L_g$ and $\varepsilon$.