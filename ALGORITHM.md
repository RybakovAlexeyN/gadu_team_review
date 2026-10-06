# VS-Certify-Delayed

This page gives the **paper-facing description of the algorithm**.

A reader who has not followed the internal development should be able to understand, in one pass,

1. what problem the procedure solves;
2. what information it receives;
3. what it does at every stage;
4. when it stops;
5. what certificate it returns;
6. where delayed feedback enters.

The exact LaTeX source used for the manuscript is in
[theory/VS_CERTIFY_DELAYED_ALGORITHM.tex](theory/VS_CERTIFY_DELAYED_ALGORITHM.tex).
The lower-level routines are in
[theory/VS_CERTIFY_DELAYED_SUBROUTINES.tex](theory/VS_CERTIFY_DELAYED_SUBROUTINES.tex).

---

## 1. What problem does the algorithm solve?

There are $K$ families. Family $i$ has a continuous action domain

$$
X_i=[0,1]^{d_i},
$$

and an unknown latent reward function $f_i:X_i\to[0,1]$.

The learner does not observe $f_i(x)$ directly. With a fixed attribution window $w$, a deployment at $x$ produces the delayed positive-only Bernoulli observation

$$
B_s^{(w)}
=
\mathbf 1\{Z_s=1,\ D_s\le w\},
$$

whose mean is

$$
g_i(x)=q_w f_i(x),
\qquad
q_w=F(w)>0.
$$

Because the same positive factor $q_w$ is used for every family, maximizing $g_i$ identifies the same best family as maximizing $f_i$.

The task of **VS-Certify-Delayed** is therefore:

> **Certify which family has the largest maximum reward, while respecting delayed feedback and returning an explicit confidence certificate.**

The procedure may return **NOT_CERTIFIED** if the calendar budget is exhausted before separation is proved.

---

## 2. The algorithm in 30 seconds

At a high level, the method repeatedly does the following:

1. partition each family domain into active dyadic cells;
2. sample the center of every unresolved active cell;
3. wait exactly $w$ legal rounds so those designated samples mature;
4. build empirical-Bernstein confidence intervals from the matured designated observations;
5. turn the cell-wise confidence intervals into lower and upper bounds on the maximum of each family;
6. stop if one family's lower bound is above every competitor's upper bound;
7. otherwise prune cells that cannot contain a family maximizer, split the survivors, and continue at the next dyadic depth.

The main loop is

~~~text
sample active cells
    ↓
wait for delayed feedback to mature
    ↓
build family certificates
    ↓
best family separated?
   / \
 yes  no
  |    |
return prune + refine
~~~

The important delayed-feedback rule is:

> **Unresolved silence is never treated as zero.**

Only designated source rounds whose $w$-window has fully matured enter the estimator.

---

## 3. Inputs and output

### Inputs

| Symbol | Meaning |
|---|---|
| $K$ | number of families |
| $X_i=[0,1]^{d_i}$ | action domain of family $i$ |
| $L_i>0$ | valid Lipschitz bound for the latent function $f_i$ |
| $w$ | attribution window |
| $q_w=F(w)>0$ | known probability that a positive event is observed within the window |
| $\delta_{\rm cert}$ | total certification failure probability |
| $\delta_i$ | per-family confidence budgets with $\sum_i\delta_i\le\delta_{\rm cert}$ |
| $B$ | hard calendar cutoff |

On the observed scale,

$$
\mathcal L_i^g := q_w L_i
$$

is a valid Lipschitz bound for $g_i$.

### Output

The algorithm returns either

$$
\texttt{CERTIFIED}
\left(
i^\star,
\{z_i,\ell_i,U_i,\Xi_i\}_{i=1}^K,
\mathsf{Acct}
\right),
$$

or

$$
\texttt{NOT\_CERTIFIED}(\mathsf{Acct}).
$$

For each family $i$, the returned latent-scale bundle satisfies, on the simultaneous confidence event,

$$
\ell_i
\le
f_i(z_i)
\le
f_i^\star
\le
U_i,
\qquad
0\le f_i^\star-f_i(z_i)\le \Xi_i.
$$

Here $i^\star$ is the family whose strict separation condition fired.

**CERTIFIED** means statistically certified best family. It is not, by itself, an automatic GADU commit; the downstream continuation/fallback gate remains separate.

---

## 4. State maintained by the procedure

At dyadic depth $h$, family $i$ has an active cell set

$$
\mathcal C_i(h).
$$

Each active cell $I$ has center $c_I$ and its own estimator state:

- $m_I$: generated designated-source count;
- $n_I$: finalized designated count;
- $\widehat g_I$: empirical mean;
- $V_I$: empirical variance;
- $\operatorname{rad}_I$: confidence radius;
- a Boolean resolved flag.

A key implementation rule is:

> **Samples are not inherited across different centers.**

When a surviving cell is split, every child starts with a fresh estimator:

$$
m_J=n_J=0.
$$

This avoids using any unproved parent-to-child sample reuse.

The global state also contains:

- calendar time $t$;
- the set $\mathcal S_{\rm cert}$ of all source rounds owned by certification.

---

## 5. Confidence scale and cell resolution

At depth $h$,

$$
\rho_h := 2^{-h-1},
\qquad
a_{i,h}:=\min\{1,\mathcal L_i^g\rho_h\}.
$$

The geometric checkpoint targets are

$$
n_r:=2^{r+1},
\qquad
r=0,1,2,\ldots.
$$

For family $i$, level $h$, cell $I$, and checkpoint $r$, define

$$
\eta_{i,h,I,r}
=
\frac{36\delta_i}
{\pi^4\,2^{d_i h}(h+1)^2(r+1)^2}.
$$

For $n\ge2$, the empirical-Bernstein radius is

$$
\operatorname{rad}(n,V,\eta)
=
\sqrt{\frac{2V\log(6/\eta)}{n}}
+
\frac{7\log(6/\eta)}{3(n-1)}.
$$

A cell is resolved at level $h$ once

$$
\operatorname{rad}_I\le \frac{a_{i,h}}{8}.
$$

Once resolved, its statistics are frozen for the remainder of that level.

---

## 6. Final manuscript procedure

The following is the reader-facing procedure intended for the main text.

Required packages:

~~~latex
\usepackage{amsmath,amssymb}
\usepackage{algorithm}
\usepackage{algpseudocode}
~~~

~~~latex
\begin{algorithm}[t]
\caption{Delayed variance-sensitive family certification}
\label{alg:vs-certify-delayed}
\small
\begin{algorithmic}[1]

\Require
families $\{(X_i,L_i)\}_{i=1}^K$ with $X_i=[0,1]^{d_i}$;
known $q_w=F(w)>0$ and window $w$;
risks $\{\delta_i\}_{i=1}^K$ with
$\sum_i\delta_i\le\delta_{\rm cert}$;
calendar cutoff $B$

\Ensure
\textsc{Certified}$\bigl(
i^\star,\{z_i,\ell_i,U_i,\Xi_i\}_{i=1}^K,\mathsf{Acct}
\bigr)$
or
\textsc{Not-Certified}$\bigl(\mathsf{Acct}\bigr)$

\State $t\gets0$, $h\gets0$, $\mathcal S_{\rm cert}\gets\varnothing$

\For{$i=1,\ldots,K$}
    \State $\mathcal L_i^g\gets q_wL_i$
    \State initialize $\mathcal C_i(0)\gets\{X_i\}$
    with fresh root-cell state
\EndFor

\While{true}

    \If{$\Call{ResolveLevel}{h}=\textsc{Fail}$}
        \State
        \Return
        \textsc{Not-Certified}$\bigl(\mathsf{Acct}(t)\bigr)$
    \EndIf

    \For{$i=1,\ldots,K$}
        \State
        $(z_i,\underline M_i^g,\overline M_i^g,\xi_i^g)
        \gets
        \Call{FamilyCertificate}{i,h}$
    \EndFor

    \If{some $i$ satisfies
        $\underline M_i^g>\max_{j\ne i}\overline M_j^g$}

        \State
        let $i^\star$ be the first such family under the fixed order

        \For{$j=1,\ldots,K$}
            \State
            $\ell_j\gets\max\{0,\underline M_j^g/q_w\}$,
            $U_j\gets\min\{1,\overline M_j^g/q_w\}$
            \State
            $\Xi_j\gets\min\{1,\xi_j^g/q_w\}$
        \EndFor

        \State
        \Return
        \textsc{Certified}$\bigl(
        i^\star,
        \{z_j,\ell_j,U_j,\Xi_j\}_{j=1}^K,
        \mathsf{Acct}(t)
        \bigr)$
    \EndIf

    \For{$i=1,\ldots,K$}
        \State
        $\mathcal S_i
        \gets
        \{I\in\mathcal C_i(h):
        U_{\rm cell}(I)\ge\underline M_i^g\}$

        \State
        $\mathcal C_i(h+1)\gets$
        all dyadic children of cells in $\mathcal S_i$,
        each with fresh estimator state
    \EndFor

    \State $h\gets h+1$

\EndWhile

\end{algorithmic}
\end{algorithm}
~~~

The two calls in Algorithm 1 are defined below and in the companion LaTeX file.

---

## 7. What ResolveLevel does

ResolveLevel is responsible for **sampling and delayed maturation** at the current dyadic depth.

For each unresolved active center, it repeatedly:

1. tops up designated pulls to the next geometric checkpoint $n_r$;
2. freezes the active sets;
3. performs exactly $w$ legal filler deployments;
4. excludes filler feedback from the designated estimators;
5. finalizes the designated observations as

$$
B_s^{(w)}
=
\mathbf 1\{Z_s=1,D_s\le w\};
$$

6. recomputes $\widehat g_I$, $V_I$, and the empirical-Bernstein radius;
7. marks cells with $\operatorname{rad}_I\le a_{i,h}/8$ as resolved;
8. moves to the next checkpoint if some cells remain unresolved.

If the calendar cutoff $B$ is hit during designated sampling or during the flush, it returns **FAIL**.

If the cutoff arrives before a source has fully matured, that unresolved source is **not** converted into a zero.

The exact pseudocode is in
[theory/VS_CERTIFY_DELAYED_SUBROUTINES.tex](theory/VS_CERTIFY_DELAYED_SUBROUTINES.tex).

---

## 8. What FamilyCertificate does

Once all active cells at the current level are resolved, define for every cell $I$

$$
\mathrm{LCB}(I)
=
\max\{0,\widehat g_I-\operatorname{rad}_I\},
$$

and

$$
U_{\rm cell}(I)
=
\min\{1,\widehat g_I+\operatorname{rad}_I+a_{i,h}\}.
$$

The family lower and upper bounds are

$$
\underline M_i^g
=
\max_{I\in\mathcal C_i(h)}\mathrm{LCB}(I),
$$

and

$$
\overline M_i^g
=
\max_{I\in\mathcal C_i(h)}U_{\rm cell}(I).
$$

The current recommendation $z_i$ is the center of the cell with the largest lower confidence bound.

The scaled deployment-error certificate is

$$
\xi_i^g
=
\min\left\{
1,\,
\max\{0,\overline M_i^g-\underline M_i^g\}
\right\}.
$$

---

## 9. Stopping and pruning

### Family certification

If, for some family $i$,

$$
\underline M_i^g
>
\max_{j\ne i}\overline M_j^g,
$$

then family $i$ is certified as uniquely best on the observed scale.

Because every family is multiplied by the same $q_w>0$, it is also the uniquely best latent family.

The scaled certificates are converted back to latent scale by

$$
\ell_i
=
\max\{0,\underline M_i^g/q_w\},
\qquad
U_i
=
\min\{1,\overline M_i^g/q_w\},
$$

and

$$
\Xi_i
=
\min\{1,\xi_i^g/q_w\}.
$$

### Pruning

If no family is separated, remove every cell for which

$$
U_{\rm cell}(I)<\underline M_i^g.
$$

Such a cell cannot contain a family maximizer on the simultaneous confidence event.

Every surviving cell is split into its dyadic children, and each child starts with a fresh estimator.

---

## 10. Why the delayed execution is explicit

A designated source generated at round $s$ is not used immediately.

After the final designated pull of a checkpoint, the active sets are frozen and the algorithm makes exactly $w$ legal filler deployments.

Only after this flush are designated sources finalized.

Thus a designated source used by the estimator has age at least $w$, and the algorithm may safely form

$$
B_s^{(w)}
=
\mathbf 1\{Z_s=1,D_s\le w\}.
$$

The filler rounds are certification-owned for accounting purposes, but their feedback is excluded from all designated estimators.

If $D$ is the number of designated pulls and $C_h$ is the number of completed checkpoints at depth $h$, then on a completed, non-truncated execution path,

$$
T_{\rm cal}
=
D+w\sum_h C_h.
$$

---

## 11. Relation to the single-family upper theorem

The paper's upper theorem analyzes the **single-family within-family core** in the direct Bernoulli-oracle model.

It uses the same:

- dyadic cells;
- empirical-Bernstein resolution rule;
- safe pruning rule.

The direct-oracle core continues until the first resolved depth with

$$
a_h\le\frac{2\varepsilon}{5},
$$

at which point the returned recommendation has certificate width at most $\varepsilon$.

VS-Certify-Delayed runs that within-family mechanism for every family, but the multi-family controller can stop earlier if strict family separation is already available.

So the roles are:

- **upper theorem:** designated-sample complexity of the within-family core;
- **Algorithm 1:** multi-family certification logic;
- **ResolveLevel:** legal delayed calendar execution;
- **calendar proposition:** $w$-round maturation overhead.

---

## 12. Scope

The current procedure assumes a fixed common known $q_w>0$.

By itself it does **not** claim:

- uniform superiority over Hoeffding;
- optimality of the checkpoint schedule;
- novelty of the $q_w^{-1}$ scaling;
- a full minimax characterization;
- automatic replacement of every existing GADU regret result;
- end-to-end superiority on real data.

---

## 13. Companion files

- [Main LaTeX algorithm](theory/VS_CERTIFY_DELAYED_ALGORITHM.tex)
- [Detailed LaTeX subroutines](theory/VS_CERTIFY_DELAYED_SUBROUTINES.tex)
- [Algorithm-to-proof map](theory/ALGORITHM_PROOF_MAP.md)
- [Upper theorem](theory/UPPER_THEOREM.md)
- [Upper proof](theory/UPPER_PROOF.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Lower proof](theory/LOWER_PROOF.md)
- [Delayed execution and GADU composition](theory/DELAYED_GADU.md)
- [Mathematical review checklist](MATH_REVIEW.md)
