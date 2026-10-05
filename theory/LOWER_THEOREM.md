# Fine-gap local-information lower bound

Consider two Bernoulli families on `X=[0,1]^d`.

- Family 1 is constant with mean `b`.
- Family 2 has mean `mu(x) < b`.

Define

```text
Delta = b - max_x mu(x) > 0,
G(x) = b - mu(x).
```

Assume

```text
b <= 1/2,
Lip(mu) = L0 <= (1-kappa)L,
kappa in (0,1),
S = L - L0.
```

Use a fixed fine-gap cutoff `c0` compatible with the Bernoulli bump construction (a concrete normalization may take `c0 = 1/6`). Define

```text
A_fine = { x : Delta <= G(x) < c0 }.
```

The target lower bound is

```text
E[tau] >= c_{d,kappa}
  * kl(1-delta, delta) / (1 + log(c0/Delta))
  * S^d
  * integral_{A_fine} {
      mu(x)/G(x)^(d+2)
      + 1/G(x)^(d+1)
    } dx.
```

This is deliberately scoped:

- fine-gap region only;
- strict roughness slack;
- logarithmic loss from layer selection;
- no claim of a full-X minimax characterization.

The atomic one-layer information term is

```text
E[tau] >= c_d * (L/s)^d * kl(1-delta,delta)
             * [ p/s^2 + 1/s ],
```

for a flat Bernoulli layer with baseline `p`, best-family mean `p+s`, and hidden Lipschitz spike alternatives.
