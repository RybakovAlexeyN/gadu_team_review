# Lower-Bound Proof Outline

The theorem is evaluated at a base instance where family 1 is constant and family 2 is suboptimal, while $\delta$-correctness is required uniformly over the larger Lipschitz model class containing the bump alternatives. This enlargement is necessary for the adaptive change-of-measure argument because some alternatives make family 2 optimal.

## A. Function-class closure

The base suboptimal function has Lipschitz constant $L_0$. Perturbation tents use slope at most

$$
S=L-L_0.
$$

Therefore every perturbed alternative remains in the declared $L$-Lipschitz class.

Uniform constants are obtained under

$$
L_0\le(1-\kappa)L.
$$

## B. Fine-gap layer alternatives

For a dyadic layer

$$
A_s =
\{x:s\le G(x)<2s\},
$$

choose a maximal packing at spatial scale proportional to $s/S$.

At each packed center construct a compact tent perturbation with

$$
\text{slope}\le S,
\qquad
\text{peak}=3s,
\qquad
\text{support radius}=\frac{3s}{S}.
$$

A convenient packing separation is $8s/S$, which makes supports within one layer disjoint.

The perturbation raises family 2 above the constant family 1 at the selected center, so every alternative flips the best family while remaining inside the declared $L$-Lipschitz model class.

## C. Bernoulli validity and KL

Use the frozen fine-gap convention

$$
c_0=\frac16,
$$

with dyadic layers satisfying

$$
s\le\frac1{12},
\qquad
b\le\frac12.
$$

This keeps the perturbed Bernoulli means valid and bounded away from one.

Inside one perturbation support, use a Bernoulli KL upper bound of the form

$$
\mathrm{kl}(p,p+a)
\le
C\frac{a^2}{p+a}.
$$

At a packed center $c$, write $p_0=\mu(c)$ for the base Bernoulli mean. After comparison with that packed-center baseline, this yields

$$
\frac{1}{\mathrm{KL}_{\mathrm{per\ informative\ pull}}}
\ge
c(
\frac{p_0}{s^2} +
\frac1s
).
$$

## D. Adaptive change of measure

Only pulls of family 2 inside the selected perturbation support distinguish the base instance from that alternative.

For $\delta\in(0,1/2)$ and an algorithm that is $\delta$-correct uniformly over the full model class, data processing gives the binary relative-entropy lower bound

$$
\mathrm{kl}(1-\delta,\delta)
$$

between the output distributions under the base instance and each alternative.

Hence expected pulls inside each support must be at least the confidence term divided by the per-pull KL.

## E. One-layer packing

Because supports are disjoint within a layer, summing over alternatives gives

$$
\mathbb E[\tau]
\ge
c\,\mathrm{kl}(1-\delta,\delta)\,H_s,
$$

where $H_s$ is the weighted packing sum carrying, at each packed center $c$, the local factor $\frac{\mu(c)}{s^2}+\frac1s$.

## F. Multiple layers

Across gap layers the supports need not be disjoint. Apply the one-layer lower bound separately to each layer and select the largest layer.

With the frozen dyadic convention this costs the explicit factor

$$
\frac{1}
{1+\lceil\log_2(c_0/\Delta)\rceil}.
$$

The logarithmic loss is part of the theorem and must not be hidden.

## G. Packing-to-integral

Maximality of the packing gives a cover of each fine layer. Lipschitz control compares the packed-center weight with nearby values of $\mu(x)$ and $G(x)$.

This yields

$$
H_s
\ge
c_{d,\kappa}S^d
\int_{A_s}
[
\frac{\mu(x)}{G(x)^{d+2}} +
\frac{1}{G(x)^{d+1}}
]dx.
$$

Summing the fine layers gives the theorem.

## Highest-value attacks

A reviewer should try to break, in order:

1. whether every perturbation really flips the best family;
2. whether all perturbed means remain valid Bernoulli parameters;
3. the local KL inequality and its dependence on the baseline mean;
4. change of measure under adaptive sampling and stopping;
5. disjointness within a layer;
6. the logarithmic layer-selection step;
7. the packing-to-integral direction;
8. any accidental extension from $A_{\mathrm{fine}}$ to all of $X$.