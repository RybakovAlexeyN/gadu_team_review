# Lower-bound proof outline

The theorem is evaluated at a base instance where family 1 is constant and family 2 is suboptimal, but `delta`-correctness is required uniformly over the larger Lipschitz model class containing the bump alternatives. This is necessary for the change-of-measure argument, because some alternatives make family 2 optimal.

## A. Function-class closure

The base suboptimal function has Lipschitz constant `L0`. Perturbation tents use slope at most

```text
S = L - L0.
```

Therefore every perturbed alternative remains in the declared `L`-Lipschitz class.

Uniform constants are obtained by assuming `L0 <= (1-kappa)L`.

## B. Fine-gap layer alternatives

For a dyadic layer

```text
A_s = { x : s <= G(x) < 2s },
```

choose a maximal packing at spatial scale proportional to `s/S`.

At each packed center construct a compact tent perturbation with slope at most `S`, peak `3s`, and support radius `3s/S`. A convenient packing separation is `8s/S`, so supports within one layer are disjoint.

The perturbation raises family 2 above the constant family 1 at the selected center, so every alternative flips the best family while remaining inside the declared `L`-Lipschitz model class.

## C. Bernoulli validity and KL

Use the frozen fine-gap convention `c0=1/6`, with dyadic layers satisfying `s<=1/12` and `b<=1/2`, so all perturbed Bernoulli means remain valid and bounded away from one.

Inside one perturbation support, the Bernoulli KL satisfies an upper bound of the form

```text
kl(p, p+a) <= C * a^2/(p+a).
```

After comparison with the packed-center baseline, this yields

```text
1 / KL_per_informative_pull
>= c * [ p0/s^2 + 1/s ].
```

## D. Adaptive change of measure

Only pulls of family 2 inside the selected perturbation support distinguish the base instance from that alternative.

For `delta in (0,1/2)` and an algorithm that is `delta`-correct uniformly over the full model class, data processing gives the binary relative-entropy lower bound `kl(1-delta,delta)` between the output distributions under the base instance and each alternative.

Thus expected pulls inside each support must be at least the confidence term divided by the per-pull KL.

## E. One-layer packing

Because supports are disjoint within a layer, summing over alternatives gives

```text
E[tau] >= c * kl(1-delta,delta) * H_s,
```

where `H_s` is the weighted packing sum carrying the local factor `p/s^2 + 1/s`.

## F. Multiple layers

Across gap layers the supports need not be disjoint. Apply the one-layer lower bound separately to each layer and select the largest layer.

With the frozen dyadic convention this costs the explicit factor

```text
1 / [1 + ceil(log_2(c0/Delta))].
```

The logarithmic loss is part of the theorem and should not be hidden.

## G. Packing-to-integral

Maximality of the packing gives a cover of each fine layer. Lipschitz control compares the packed-center weight with nearby values of `mu(x)` and `G(x)`.

This yields

```text
H_s >= c_{d,kappa} * S^d * integral_{A_s} [
  mu(x)/G(x)^(d+2) + 1/G(x)^(d+1)
] dx.
```

Summing the fine layers gives the theorem.

## Points the reviewer should try to break

1. whether every perturbation really flips the best family;
2. whether all perturbed means remain valid Bernoulli parameters;
3. the local KL inequality and its dependence on the baseline mean;
4. change-of-measure under adaptive sampling/stopping;
5. disjointness within a layer;
6. the logarithmic layer-selection step;
7. the packing-to-integral direction;
8. any accidental extension from `A_fine` to all of `X`.
