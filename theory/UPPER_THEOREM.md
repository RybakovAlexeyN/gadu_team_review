# Variance-sensitive Bernoulli certified-continuum upper bound

Let `X = [0,1]^d` and let `g : X -> [0,1]` be `L`-Lipschitz in the infinity norm. A query at `x` returns an independent Bernoulli observation with mean `g(x)`.

Define

- `g* = max_x g(x)`;
- `gap(x) = g* - g(x)`.

For target accuracy `epsilon in (0,1]` and confidence `delta in (0,1)`, consider a dyadic optimizer that:

1. maintains active dyadic cells;
2. samples cell centers;
3. uses empirical-Bernstein confidence intervals;
4. forms Lipschitz cell upper bounds;
5. prunes cells whose upper bound is below the current best lower bound;
6. refines surviving cells;
7. stops when the family-level certificate width is at most `epsilon`.

The target bound is

```text
N <= C_d * Lambda(epsilon, delta, L, d)
     * [ 1
         + L^d * integral_X {
             g(x) / (gap(x)+epsilon)^(d+2)
             + 1 / (gap(x)+epsilon)^(d+1)
           } dx ]
```

with probability at least `1-delta`, where `Lambda` is polylogarithmic and arises from simultaneous confidence allocation over dyadic cells/checkpoints.

The strongest discrete intermediate form is

```text
N <= C * sum_h lambda_h * sum_{c in A_h}
        [ g(c)/a_h^2 + 1/a_h ],
```

where `a_h` is the geometric uncertainty at level `h` and `A_h` is the set of centers actually sampled at that level.

## Delayed positive-only specialization

For a fixed attribution window `w`, let

```text
g_i(x) = q_w f_i(x),    q_w = F(w) > 0.
```

If `q_w` is common across families and known for the main model, then `Lip(g_i) <= q_w L_i`, and the latent-scale sample-complexity specialization becomes

```text
N_i(epsilon) <= C * Lambda_i * [ 1
  + (L_i^d / q_w) * integral {
      f_i(x)/(Delta_i(x)+epsilon)^(d+2)
      + 1/(Delta_i(x)+epsilon)^(d+1)
    } dx ].
```

The factor `q_w^-1` is not claimed as novel by itself.
