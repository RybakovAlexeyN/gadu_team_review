# Variance-sensitive Bernoulli certified-continuum upper bound

Let `X=[0,1]^d` and let `g:X->[0,1]` be `L_g`-Lipschitz in the infinity norm, with known valid `L_g>=0`. A query at `x` returns an independent Bernoulli observation with mean `g(x)`.

Define

```text
g* = max_x g(x),
gap(x) = g* - g(x).
```

If `L_g=0`, every point is optimal and no query is needed. Assume below that `L_g>0`.

## Explicit dyadic/confidence convention

At depth `h` use

```text
rho_h = 2^(-h-1),
a_h   = min{1, L_g rho_h}.
```

Stop refining no later than the first level satisfying

```text
a_h <= 2 epsilon / 5.
```

For every possible depth-`h` cell `I` and geometric checkpoint `r`, preassign

```text
eta_{h,I,r}
=
36 delta /
[pi^4 * 2^(d h) * (h+1)^2 * (r+1)^2].
```

The total budget over all cells, depths and checkpoints is at most `delta`.

Write

```text
lambda_{h,r} = log(6 / eta_{h,I,r}),
n_r = 2^(r+1).
```

A concrete deterministic checkpoint cap can be taken as the first `R_h` for which

```text
n_r >=
4
+ 1024 lambda_{h,r}/a_h^2
+ 140  lambda_{h,r}/a_h.
```

Define the explicit confidence factor

```text
Lambda(epsilon,delta,L_g,d)
=
max lambda_{h,r}
```

over `0<=h<=h_epsilon` and `0<=r<=R_h`.

## Observable empirical-Bernstein radius

For `n>=2` finalized Bernoulli samples,

```text
V_n = (1/(n-1)) * sum_j (Y_j - mean(Y))^2
```

and use

```text
r_n
=
sqrt(2 V_n log(6/eta) / n)
+
7 log(6/eta) / (3(n-1)).
```

The learner stops a center from this observable radius; the unknown mean appears only in the performance analysis.

## Upper bound

For every target accuracy `epsilon in (0,1]` and confidence `delta in (0,1)`, there exists an executable dyadic certified optimizer that returns `(x_hat, xi)` such that, with probability at least `1-delta`,

```text
g* - g(x_hat) <= xi <= epsilon.
```

Its number of Bernoulli observations satisfies

```text
N <= C_d * Lambda(epsilon,delta,L_g,d)
     * [ 1
         + L_g^d * integral_X {
             g(x) / (gap(x)+epsilon)^(d+2)
             + 1 / (gap(x)+epsilon)^(d+1)
           } dx ].
```

`C_d` depends only on dimension and the fixed infinity-norm/dyadic convention. No optimal-constant claim is made.

The strongest discrete intermediate form is

```text
N <= C * sum_h sum_{c in A_h}
        lambda_{h,r(c)}
        [ g(c)/a_h^2 + 1/a_h ],
```

where `A_h` is the set of all centers sampled at level `h`.

Every sampled center in the fine dyadic regime satisfies

```text
gap(c) <= 6 a_h.
```

The clipped coarse levels `a_h=1` are bounded separately and absorbed into the same target functional for `epsilon<=1`.

A center-wise explicit designated-sample bound is

```text
N_c(h)
<=
4
+ 1024 g(c) Lambda / a_h^2
+ 140 Lambda / a_h.
```

## Delayed positive-only specialization

For a fixed attribution window `w`, let

```text
g_i(x) = q_w f_i(x),    q_w = F(w) > 0.
```

If `q_w` is common across families and known in the main model, then `Lip(g_i)<=q_w L_i`. For simultaneous family certification, preassign per-family risks `delta_i>0` with

```text
sum_i delta_i <= delta_cert.
```

Set

```text
Lambda_i = Lambda(q_w epsilon, delta_i, q_w L_i, d_i).
```

Then the latent-scale specialization is

```text
N_i(epsilon) <= C * Lambda_i * [ 1
  + (L_i^d / q_w) * integral {
      f_i(x)/(Delta_i(x)+epsilon)^(d+2)
      + 1/(Delta_i(x)+epsilon)^(d+1)
    } dx ].
```

The factor `q_w^-1` is not claimed as novel by itself.

→ [Proof outline](UPPER_PROOF.md)  
→ [Algorithm](../ALGORITHM.md)
