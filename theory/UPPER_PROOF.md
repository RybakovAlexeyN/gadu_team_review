# Upper-bound proof roadmap

This file records the proof obligations for the **single-family within-family core** used by `VS-Certify-Delayed`.

The delayed multi-family controller has a different stopping rule. Its extra obligations — maturation timing, family separation, calendar accounting, and source ownership — are tracked separately in [`ALGORITHM_PROOF_MAP.md`](ALGORITHM_PROOF_MAP.md) and [`DELAYED_GADU.md`](DELAYED_GADU.md).

Throughout this file, let

```text
X = [0,1]^d,
g* = max_x g(x),
gap(x) = g* - g(x),
rho_h = 2^(-h-1),
a_h = min{1, L_g rho_h}.
```

At every active center on depth `h`, the core resolves the center only when

```text
rad_I <= a_h / 8.
```

## Lemma A — simultaneous empirical-Bernstein confidence

For every possible depth-`h` dyadic cell `I` and checkpoint `r`, preassign

```text
eta_{h,I,r}
=
36 delta /
[pi^4 * 2^(d h) * (h+1)^2 * (r+1)^2].
```

There are exactly `2^(d h)` possible cells at depth `h`. Hence

```text
sum_{h,I,r} eta_{h,I,r}
=
(36 delta / pi^4)
* sum_h 1/(h+1)^2
* sum_r 1/(r+1)^2
=
delta.
```

For `n>=2` Bernoulli observations at a center use

```text
rad(n,V,eta)
=
sqrt(2 V log(6/eta)/n)
+
7 log(6/eta)/(3(n-1)).
```

Therefore, after the per-node/per-checkpoint allocation and a union bound, there is one event `E_conf` with probability at least `1-delta` on which every confidence interval actually used by the adaptive algorithm is valid:

```text
|hat g_I - g(c_I)| <= rad_I.
```

Preallocation over **all possible cells and checkpoints** is what makes adaptive activation harmless here.

## Lemma B — every active center resolves in finite checkpoints

Fix a center `c` at depth `h`, write `mu=g(c)`, and let

```text
lambda = log(6/eta).
```

Using the supporting sample-variance comparison from the frozen concentration audit, a sufficient sample size is

```text
n
>=
2
+ 512 mu lambda / a_h^2
+ 70 lambda / a_h
```

for the observable radius to be at most `a_h/8` on the supporting concentration event.

Because the algorithm samples only at geometric cumulative targets

```text
n_r = 2^(r+1),
```

the first target above this sufficient sample size overshoots by less than a factor two. Thus the actual designated count at resolution is bounded by

```text
N_c(h)
<=
4
+ 1024 g(c) Lambda / a_h^2
+ 140 Lambda / a_h.
```

Since `g(c)<=1`, the deterministic checkpoint cap `R_h` in the theorem is sufficient for every center:

```text
n_{R_h}
>=
4
+ 1024 lambda_{h,R_h}/a_h^2
+ 140 lambda_{h,R_h}/a_h.
```

Hence, in the direct-oracle core with no hard cutoff, the inner checkpoint loop terminates at every finite depth.

The unknown mean `g(c)` is used only in this **analysis bound**. The learner stops from the observable radius.

## Lemma C — valid cell upper envelope

Let `I` be a depth-`h` cell with center `c_I`.

For every `x in I`,

```text
g(x) <= g(c_I) + L_g rho_h.
```

Because `g in [0,1]` and

```text
a_h = min{1, L_g rho_h},
```

we may write

```text
sup_{x in I} g(x) <= min{1, g(c_I) + a_h}.
```

On `E_conf`,

```text
g(c_I) <= hat g_I + rad_I,
```

so the algorithmic quantity

```text
U_cell(I)
=
min{1, hat g_I + rad_I + a_h}
```

is a valid upper bound on the whole cell.

Likewise

```text
LCB(I) = max{0, hat g_I - rad_I}
<= g(c_I).
```

## Lemma D — maximizer cell survives pruning

Let `I_h^*` be an active depth-`h` cell containing a maximizer `x^*`.

Define

```text
ell_h = max_I LCB(I).
```

By Lemma C,

```text
U_cell(I_h^*) >= g* >= ell_h.
```

Therefore the pruning rule

```text
remove I iff U_cell(I) < ell_h
```

cannot remove `I_h^*` on `E_conf`.

Thus at least one cell containing a global maximizer remains active at every refinement depth.

## Lemma E — every survivor center is 5 a_h / 2 near-optimal

At a resolved level, `rad_I<=a_h/8` for every active cell.

For the maximizer cell `I_h^*`,

```text
gap(c_{I_h^*}) <= a_h.
```

On `E_conf`,

```text
LCB(I_h^*)
>=
g(c_{I_h^*}) - 2 rad_{I_h^*}
>=
g* - a_h - a_h/4
=
g* - 5 a_h/4.
```

Hence

```text
ell_h >= g* - 5 a_h/4.
```

If a cell `I` survives, then `U_cell(I)>=ell_h`. Also

```text
U_cell(I)
<=
g(c_I) + 2 rad_I + a_h
<=
g(c_I) + 5 a_h/4.
```

Combining these inequalities gives

```text
gap(c_I) <= 5 a_h / 2.
```

This is the exact survivor constant used by the parent-to-child argument.

## Lemma F — every sampled child is 6 a_h near-optimal

A sampled depth-`h` cell is a child of a surviving depth-`h-1` cell.

For the dyadic convention,

```text
||c_child - c_parent||_infty <= rho_h.
```

Therefore

```text
g(c_parent) - g(c_child) <= a_h.
```

Also, for all depths,

```text
a_{h-1}
=
min{1, 2 L_g rho_h}
<=
2 a_h.
```

Lemma E applied to the surviving parent yields

```text
gap(c_parent) <= 5 a_{h-1}/2 <= 5 a_h.
```

Hence every sampled child satisfies

```text
gap(c_child)
<=
gap(c_parent) + a_h
<=
6 a_h.
```

This argument also covers the transition out of the clipped regime; it needs only `a_{h-1}<=2a_h`, not equality.

## Lemma G — the resolved family certificate has width at most 5 a_h / 2

At a resolved depth define

```text
ell^g = max_I LCB(I),
U^g   = max_I U_cell(I).
```

As above,

```text
ell^g >= g* - 5 a_h/4.
```

For every active cell,

```text
U_cell(I)
<=
g(c_I) + 2 rad_I + a_h
<=
g* + 5 a_h/4.
```

Therefore

```text
U^g - ell^g <= 5 a_h / 2.
```

If the recommendation `z` is the center attaining the largest LCB and

```text
xi = min{1, U^g - ell^g},
```

then, on `E_conf`,

```text
g* - g(z)
<=
U^g - ell^g
=
xi
<=
5 a_h/2.
```

Thus the direct-oracle core may stop at the first resolved depth satisfying

```text
a_h <= 2 epsilon / 5,
```

and then returns a valid `epsilon`-certificate.

## Lemma H — discrete designated-sample bound

Let `A_h` be all centers actually sampled at depth `h`.

Combining Lemma B across sampled centers gives

```text
N
<=
C
* sum_h
  sum_{c in A_h}
  lambda_{h,r(c)}
  [ g(c)/a_h^2 + 1/a_h ],
```

up to the fixed initialization/overshoot constant.

By Lemma F, every fine-scale sampled center satisfies

```text
gap(c) <= 6 a_h.
```

This is the strongest discrete form that feeds the geometric part of the proof.

## Lemma I — packing-to-volume conversion

At a fixed fine depth, distinct dyadic centers are separated in infinity norm at scale

```text
2^(-h) = 2 a_h / L_g.
```

Choose disjoint infinity-norm balls around sampled centers with radius a fixed fraction of `a_h/L_g`.

Even at the boundary of `[0,1]^d`,

```text
vol(B_infty(c,r) intersect X) >= r^d.
```

For `x` in the ball around `c`,

- `g(c) <= g(x) + C a_h`;
- `gap(x) <= gap(c) + C a_h <= C' a_h`.

Multiplying a center cost by the reciprocal ball volume yields

```text
g(c)/a_h^2 + 1/a_h
<=
C_d L_g^d
* integral_{ball(c)} [
    g(x)/a_h^(d+2)
    + 1/a_h^(d+1)
  ] dx.
```

Summing over disjoint balls converts the level-wise discrete sum to a level-wise integral.

## Lemma J — dyadic summation

If a point `x` contributes at depth `h`, Lemmas F and I imply

```text
gap(x) <= C a_h.
```

The refinement stops once `a_h` reaches the target scale `Theta(epsilon)`.

Therefore the contributing dyadic scales satisfy, up to fixed constants,

```text
a_h >= c * max{gap(x), epsilon}.
```

Geometric summation gives

```text
sum_h 1/a_h^(d+2)
<=
C / (gap(x)+epsilon)^(d+2),

sum_h 1/a_h^(d+1)
<=
C / (gap(x)+epsilon)^(d+1).
```

Substituting into Lemma I yields

```text
N
<=
C_d Lambda
* [
    1
    + L_g^d integral_X {
        g(x)/(gap(x)+epsilon)^(d+2)
        + 1/(gap(x)+epsilon)^(d+1)
      } dx
  ].
```

## Lemma K — clipped coarse levels and flat case

The packing conversion above is used only in the fine regime where the dyadic spatial scale is represented by `a_h/L_g`.

The finitely many clipped levels `a_h=1` are bounded separately and contribute at most a fixed

```text
O_d(1 + L_g^d)
```

term, absorbed into the theorem functional for `epsilon<=1`.

If `L_g=0`, the function is constant and the optimizer returns any point with certificate zero without querying.

## Proof chain

The theorem is the composition

```text
A  simultaneous confidence
-> B  finite resolution and center cost
-> C  valid cell envelopes
-> D  maximizer survival
-> E  survivor near-optimality
-> F  sampled-child near-optimality
-> G  epsilon certificate
-> H  discrete sample bound
-> I  packing-to-volume
-> J  dyadic summation
-> K  coarse/flat cleanup.
```

## Remaining independent-review targets

The proof roadmap above makes the intended constants and dependencies explicit, but it is still a review artifact rather than a substitute for independent proof checking.

The highest-value attacks are:

1. verify the empirical-Bernstein concentration statement and the sufficient sample-size algebra in Lemmas A–B;
2. verify the packing-to-volume inequality in Lemma I, including boundary cells;
3. verify the pointwise dyadic summation in Lemma J;
4. verify that no hidden sample reuse is needed when child estimators start fresh;
5. check the coarse-level absorption in Lemma K for all allowed `L_g` and `epsilon`.
