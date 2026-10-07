# Fine-Gap Local-Information Lower Bound

This note states the current **scoped** Bernoulli lower-bound candidate. It is intentionally narrower than a full minimax characterization.

## Setting

Consider two Bernoulli families on

$$
X=[0,1]^d.
$$

The base instance is:

- family 1 is constant with mean $b$;
- family 2 has mean $\mu(x)<b$.

Define

$$
\Delta=b-\max_x\mu(x)>0,
\qquad
G(x)=b-\mu(x).
$$

Assume

$$
b\le\frac12,
\qquad
L_0=\operatorname{Lip}(\mu)\le(1-\kappa)L,
\qquad
\kappa\in(0,1),
$$

and define the roughness slack

$$
S=L-L_0>0.
$$

Fix

$$
c_0=\frac16,
\qquad
0<\Delta<c_0,
$$

and define the fine-gap region

$$
A_{\mathrm{fine}}
=
\{x:\Delta\le G(x)<c_0\}.
$$

## Correctness model

Let $\mathcal M_L$ be the two-family Bernoulli model class in which both family mean functions

- are $L$-Lipschitz on $X$;
- take values in $[0,1]$;
- have a unique best family.

The base instance is the point at which the lower bound is evaluated. The local bump alternatives used in the proof must also remain inside $\mathcal M_L$; under some alternatives, family 2 becomes optimal.

Fix $\delta\in(0,1/2)$. An algorithm is $\delta$-correct on $\mathcal M_L$ if, for every instance $\nu\in\mathcal M_L$,

- it has an almost surely finite stopping time $\tau$ with respect to the natural adaptive-sampling filtration;
- it returns an $\mathcal F_\tau$-measurable family label;
- it identifies the unique optimal family with probability at least $1-\delta$.

## Theorem — lower bound

Every algorithm that is $\delta$-correct on $\mathcal M_L$ satisfies, at the displayed base instance,

$$
\mathbb E[\tau]
\ge
c_{d,\kappa}
\frac{\operatorname{kl}(1-\delta,\delta)}
{1+\left\lceil\log_2(c_0/\Delta)\right\rceil}
\,S^d
\int_{A_{\mathrm{fine}}}
\left(
\frac{\mu(x)}{G(x)^{d+2}}
+
\frac{1}{G(x)^{d+1}}
\right)\,dx,
$$

up to fixed dimension/$\ell_\infty$ packing constants.

## One-layer mechanism

For a dyadic fine layer

$$
A_s=\{x:s\le G(x)<2s\},
\qquad
s\le\frac1{12},
$$

use a maximal packing with separation proportional to $s/S$.

The perturbation tents have

$$
\text{peak}=3s,
\qquad
\text{slope}\le S,
\qquad
\text{support radius}=\frac{3s}{S}.
$$

Since

$$
\operatorname{Lip}(\mu+\text{tent})
\le
L_0+S
=
L,
$$

the alternatives remain in the declared Lipschitz class and flip the best family at the selected center.

The local Bernoulli information scale is

$$
\frac{p}{s^2}+\frac1s.
$$

Consequently the one-layer lower bound has the form

$$
\mathbb E[\tau]
\ge
c_{d,\kappa}
\left(\frac{S}{s}\right)^d
\operatorname{kl}(1-\delta,\delta)
\left(
\frac{p}{s^2}+\frac1s
\right),
$$

up to fixed packing constants.

Selecting the largest dyadic layer produces the explicit logarithmic factor in the theorem.

## Scope

The result is deliberately restricted to:

- the **fine-gap region** $A_{\mathrm{fine}}$;
- strict roughness slack $S>0$;
- an explicit logarithmic layer-selection loss;
- the declared fixed-confidence model class.

It does **not** claim:

- a full-$X$ lower bound;
- a full minimax characterization;
- exact matching without the logarithmic loss;
- a broader model class than the one stated above.

[Proof outline →](LOWER_PROOF.md)  
[Mathematical review checklist →](../MATH_REVIEW.md)