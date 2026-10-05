# Fine-gap local-information lower bound

Consider two Bernoulli families on `X=[0,1]^d`.

The base instance is:

- family 1 is constant with mean `b`;
- family 2 has mean `mu(x)<b`.

Define

```text
Delta = b - max_x mu(x) > 0,
G(x)  = b - mu(x).
```

Assume

```text
b <= 1/2,
L0 = Lip(mu) <= (1-kappa)L,
kappa in (0,1),
S = L - L0 > 0.
```

Fix

```text
c0 = 1/6,
0 < Delta < c0,
A_fine = {x : Delta <= G(x) < c0}.
```

## Correctness model

Let `M_L` be the two-family Bernoulli model class in which both family mean functions:

- are `L`-Lipschitz on `X`;
- take values in `[0,1]`;
- have a unique best family.

The base instance above is the point at which the lower bound is evaluated. The local bump alternatives used in the proof are also required to remain inside `M_L`; under some of them family 2 becomes optimal.

Fix `delta in (0,1/2)`.

An algorithm is `delta`-correct on `M_L` if, for every instance `nu in M_L`:

- it has an almost surely finite stopping time `tau` with respect to the natural adaptive-sampling filtration;
- it returns an `F_tau`-measurable family label;
- it identifies the unique optimal family with probability at least `1-delta`.

## Lower bound

Every algorithm that is `delta`-correct on `M_L` satisfies, at the displayed base instance,

```text
E[tau] >= c_{d,kappa}
  * kl(1-delta,delta)
    / [1 + ceil(log_2(c0/Delta))]
  * S^d
  * integral_{A_fine} {
      mu(x)/G(x)^(d+2)
      + 1/G(x)^(d+1)
    } dx,
```

up to fixed dimension/infinity-norm packing constants.

This is deliberately scoped:

- fine-gap region only;
- strict roughness slack;
- logarithmic loss from layer selection;
- no claim of a full-X minimax characterization.

## Verified one-layer mechanism

For a dyadic fine layer

```text
A_s = {x : s <= G(x) < 2s},
s <= 1/12,
```

use a maximal packing with separation proportional to `s/S`.

The perturbation tents have:

```text
peak = 3s,
slope <= S,
support radius = 3s/S.
```

Since

```text
Lip(mu + tent) <= L0 + S = L,
```

the alternatives remain in the declared class and flip the best family at the selected center.

The local Bernoulli information scale is

```text
p/s^2 + 1/s.
```

Consequently the one-layer lower bound has the form

```text
E[tau] >= c_{d,kappa}
  * (S/s)^d
  * kl(1-delta,delta)
  * [p/s^2 + 1/s],
```

up to fixed packing constants.

Selecting the largest dyadic layer produces the explicit logarithmic factor in the theorem.

→ [Proof outline](LOWER_PROOF.md)  
→ [Mathematical review checklist](../MATH_REVIEW.md)
