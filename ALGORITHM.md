# VS-Certify-Delayed

This page gives the **paper-facing description of the executable certification algorithm**. A reader should be able to understand, in one pass,

1. what problem the procedure solves;
2. what information it receives;
3. what it does at every stage;
4. when it stops;
5. what certificate it returns;
6. where delayed feedback enters.

The exact LaTeX source intended for the manuscript is in [`theory/VS_CERTIFY_DELAYED_ALGORITHM.tex`](theory/VS_CERTIFY_DELAYED_ALGORITHM.tex). Detailed helper routines are in [`theory/VS_CERTIFY_DELAYED_SUBROUTINES.tex`](theory/VS_CERTIFY_DELAYED_SUBROUTINES.tex).

## Algorithm at a glance

```text
active cells
→ designated pulls
→ synchronized checkpoint
→ w legal filler rounds
→ finalize matured designated outcomes
→ empirical-Bernstein confidence
→ prune / split
→ family certification
→ CERTIFIED / continue / NOT_CERTIFIED
```

Three distinctions are essential:

- **designated pulls** are the observations used by the certification estimator;
- **filler rounds** are legal deployments used while designated observations mature and are excluded from that estimator;
- **CERTIFIED** means a statistical family certificate, not an automatic downstream GADU commit.

> **Delayed-feedback invariant:** unresolved silence is never treated as zero.

## 1. Problem solved

There are $K$ families. Family $i$ has continuous action domain

$$
X_i=[0,1]^{d_i},
$$

and an unknown latent reward function

$$
f_i:X_i\to[0,1].
$$

With a fixed attribution window $w$, a deployment at $x$ produces the matured positive-only Bernoulli observation

$$
B_s^{(w)}
=
\mathbf 1\{Z_s=1,\ D_s\le w\},
$$

with mean

$$
g_i(x)=q_w f_i(x),
\qquad
q_w=F(w)>0.
$$

Because the same positive factor $q_w$ is used for every family, maximizing $g_i$ identifies the same best family as maximizing $f_i$.

The goal of **VS-Certify-Delayed** is therefore:

> **Certify which family has the largest maximum reward while respecting delayed feedback and returning an explicit confidence certificate.**

The procedure may return `NOT_CERTIFIED` if the calendar budget is exhausted before separation is proved.

## 2. Main loop

At a high level the method repeatedly:

1. partitions each family domain into active dyadic cells;
2. samples the center of every unresolved active cell;
3. waits for those **designated** sources to mature by emitting exactly $w$ legal filler deployments;
4. builds empirical-Bernstein confidence intervals from the matured designated observations;
5. converts cell-wise confidence intervals into lower and upper bounds on each family maximum;
6. stops if one family's lower bound exceeds every competitor's upper bound;
7. otherwise prunes cells that cannot contain a family maximizer, splits the survivors, and continues at the next dyadic depth.

```text
sample active cells
        ↓
flush w legal rounds
        ↓
finalize designated outcomes
        ↓
build family certificates
        ↓
best family separated?
      /   \
    yes    no
     |      |
 CERTIFIED  prune + refine
```

## 3. Inputs and output

### Inputs

| Symbol | Meaning |
|---|---|
| $K$ | number of families |
| $X_i=[0,1]^{d_i}$ | action domain of family $i$ |
| $L_i>0$ | valid Lipschitz bound for latent $f_i$ |
| $w$ | attribution window |
| $q_w=F(w)>0$ | known probability that a positive event is observed within $w$ |
| $\delta_{\mathrm{cert}}$ | total certification failure probability |
| $\delta_i$ | per-family risk budgets with $\sum_i\delta_i\le\delta_{\mathrm{cert}}$ |
| $B$ | hard calendar cutoff |

On the observed scale,

$$
\mathcal L_i^g=q_wL_i
$$

is a valid Lipschitz bound for $g_i$.

### Output

The algorithm returns either

$$
\mathrm{CERTIFIED}
\left(
i^\star,
\{z_i,\ell_i,U_i,\Xi_i\}_{i=1}^K,
\mathsf{Acct}
\right),
$$

or

$$
\mathrm{NOT\_CERTIFIED}(\mathsf{Acct}).
$$

For each family $i$, on the simultaneous confidence event,

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

## 4. State

At dyadic depth $h$, family $i$ has active cells

$$
\mathcal C_i(h).
$$

Each active cell $I$ has center $c_I$ and estimator state:

- $m_I$: generated designated-source count;
- $n_I$: finalized designated count;
- $\widehat g_I$: empirical mean;
- $V_I$: empirical variance;
- $\operatorname{rad}_I$: confidence radius;
- a Boolean resolved flag.

A key implementation rule is:

> **Samples are not inherited across different centers.**

When a surviving cell is split, every child starts with fresh estimator state:

$$
m_J=n_J=0.
$$

This avoids any unproved parent-to-child sample reuse.

The global state also contains calendar time $t$ and the set $\mathcal S_{\mathrm{cert}}$ of all source rounds owned by certification.

## 5. Confidence scale and resolution

At depth $h$,

$$
\rho_h=2^{-h-1},
\qquad
 a_{i,h}=\min\{1,\mathcal L_i^g\rho_h\}.
$$

The geometric checkpoint targets are

$$
n_r=2^{r+1},
\qquad
r=0,1,2,\ldots
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
\operatorname{rad}_I\le\frac{a_{i,h}}{8}.
$$

Once resolved, its statistics are frozen for the remainder of that level.

## 6. Reader-facing control flow

```text
initialize t = 0, h = 0
initialize one root cell for every family

repeat:
    ResolveLevel(h)
    if hard cutoff is hit:
        return NOT_CERTIFIED(accounting)

    build one FamilyCertificate(i,h) for each family i

    if some family i has
       lower_family_bound(i) > all competing upper_family_bounds:
        translate the full certificate bundle back to latent scale
        return CERTIFIED(i, bundle, accounting)

    for every family:
        prune cells whose cell upper bound is below the family lower bound
        split every surviving cell
        initialize every child with fresh estimator state

    h ← h + 1
```

The exact paper pseudocode is in [`theory/VS_CERTIFY_DELAYED_ALGORITHM.tex`](theory/VS_CERTIFY_DELAYED_ALGORITHM.tex).

## 7. `ResolveLevel`

`ResolveLevel` handles **sampling and delayed maturation** at the current depth.

For every unresolved active center it repeatedly:

1. tops up designated pulls to the next geometric checkpoint $n_r$;
2. freezes the active sets;
3. performs exactly $w$ legal filler deployments;
4. excludes filler feedback from the designated estimators;
5. after maturation, finalizes designated outcomes as
   $$
   B_s^{(w)}=\mathbf 1\{Z_s=1,D_s\le w\};
   $$
6. recomputes $\widehat g_I$, $V_I$, and $\operatorname{rad}_I$;
7. marks cells with
   $$
   \operatorname{rad}_I\le\frac{a_{i,h}}8
   $$
   as resolved;
8. advances to the next checkpoint if some cells remain unresolved.

If the hard calendar cutoff $B$ is reached during designated sampling or during the flush, the routine returns `FAIL`.

If the cutoff arrives before a source has fully matured, that source is **not** converted into a zero.

## 8. `FamilyCertificate`

Once all active cells at the current level are resolved, define

$$
\operatorname{LCB}(I)
=
\max\{0,\widehat g_I-\operatorname{rad}_I\},
$$

and

$$
U_{\mathrm{cell}}(I)
=
\min\{1,\widehat g_I+\operatorname{rad}_I+a_{i,h}\}.
$$

The family lower and upper envelopes are

$$
\underline M_i^g
=
\max_{I\in\mathcal C_i(h)}\operatorname{LCB}(I),
$$

and

$$
\overline M_i^g
=
\max_{I\in\mathcal C_i(h)}U_{\mathrm{cell}}(I).
$$

The current recommendation $z_i$ is the center of the cell with the largest lower confidence bound.

The scaled deployment-error certificate is

$$
\xi_i^g
=
\min\left\{
1,
\max\{0,\overline M_i^g-\underline M_i^g\}
\right\}.
$$

## 9. Family certification and pruning

### Family separation

If, for some family $i$,

$$
\underline M_i^g
>
\max_{j\ne i}\overline M_j^g,
$$

then family $i$ is certified as uniquely best on the observed scale. Because all families share the same $q_w>0$, it is also uniquely best on the latent scale.

Translate the certificate by

$$
\ell_i=\max\{0,\underline M_i^g/q_w\},
\qquad
U_i=\min\{1,\overline M_i^g/q_w\},
$$

and

$$
\Xi_i=\min\{1,\xi_i^g/q_w\}.
$$

### Within-family pruning

If no family is separated, retain exactly the cells satisfying

$$
U_{\mathrm{cell}}(I)
\ge
\underline M_i^g.
$$

A cell containing a family maximizer cannot be pruned on the simultaneous confidence event. Every surviving cell is split into dyadic children, each with fresh estimator state.

## 10. Delayed calendar accounting

A designated source generated at round $s$ is not used immediately. After the last designated pull of a checkpoint, the active sets are frozen and the algorithm emits exactly $w$ legal filler deployments.

Only after this flush are the designated source outcomes finalized. Thus every designated source used by the estimator has age at least $w$.

If $D$ is the number of designated pulls and $C_h$ is the number of completed checkpoints at depth $h$, then on a completed, non-truncated execution path,

$$
T_{\mathrm{cal}}
=
D+w\sum_h C_h.
$$

## 11. Relation to the single-family upper theorem

The paper's [upper theorem](theory/UPPER_THEOREM.md) analyzes the **single-family within-family core** in the direct Bernoulli-oracle model. It uses the same

- dyadic cells;
- empirical-Bernstein resolution rule;
- safe pruning rule.

The direct-oracle core refines until the first resolved depth satisfying

$$
a_h\le\frac{2\varepsilon}{5},
$$

at which point the returned recommendation has certificate width at most $\varepsilon$.

VS-Certify-Delayed runs that within-family mechanism for every family, but the multi-family controller may stop earlier when strict family separation is already available.

The division of responsibility is:

| Object | Role |
|---|---|
| Upper theorem | designated-sample complexity of the within-family core |
| Algorithm | multi-family certification logic |
| `ResolveLevel` | legal delayed calendar execution |
| Calendar proposition | $w$-round maturation overhead |

## 12. Scope

The current procedure assumes a fixed common known $q_w>0$.

It does **not** claim:

- uniform superiority over Hoeffding;
- optimality of the checkpoint schedule;
- novelty of the $q_w^{-1}$ scaling;
- a full minimax characterization;
- automatic replacement of every existing GADU regret result;
- end-to-end superiority on real data.

## Companion files

- [Main LaTeX algorithm](theory/VS_CERTIFY_DELAYED_ALGORITHM.tex)
- [Detailed LaTeX subroutines](theory/VS_CERTIFY_DELAYED_SUBROUTINES.tex)
- [Algorithm-to-proof map](theory/ALGORITHM_PROOF_MAP.md)
- [Upper theorem](theory/UPPER_THEOREM.md)
- [Upper proof](theory/UPPER_PROOF.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Lower proof](theory/LOWER_PROOF.md)
- [Delayed execution and GADU composition](theory/DELAYED_GADU.md)
- [Mathematical review checklist](MATH_REVIEW.md)