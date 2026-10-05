# Upper-bound proof outline

This file is a reviewable proof roadmap. The goal is to make every nontrivial implication explicit enough for an independent mathematician to attack.

## A. Simultaneous empirical-Bernstein confidence

For each dyadic center stream and each geometric sample checkpoint, allocate a summable failure budget. On the resulting event of probability at least `1-delta`, every center mean lies in its interval at every used checkpoint.

For Bernoulli mean `m`, observable empirical-Bernstein stopping gives sample count of the form

```text
n <= C * lambda * [ m/a^2 + 1/a ]
```

to reach confidence half-width at most a fixed fraction of the geometric uncertainty `a`.

The algorithm does not need to know `m`; `m` appears only in the analysis.

## B. Valid cell upper bounds and safe pruning

At level `h`, let `a_h = L rho_h` for cell radius `rho_h`.

For a cell `I` with center `c`,

```text
U_cell(I) = UCB(c) + a_h
```

upper-bounds `sup_{x in I} g(x)` on the confidence event.

Therefore a cell containing a global maximizer cannot be pruned when pruning is based on comparison with a valid lower bound.

## C. Near-optimality of every sampled child

Controlling only surviving cells is insufficient, because a child may be sampled and then eliminated.

For dyadic refinement, each level-h sampled cell is a child of a level-(h-1) survivor. If the parent-center gap is at most a constant times `a_{h-1}` and `a_{h-1}=2a_h`, then the Lipschitz displacement from parent center to child center adds only `O(a_h)`.

Hence every sampled level-h center satisfies

```text
gap(c) <= C_1 a_h
```

for an absolute constant `C_1`.

## D. Stopping scale

Once every active center is statistically resolved to a small fraction of `a_h`, the family upper envelope and best lower bound differ by `O(a_h)`.

Therefore the algorithm stops once

```text
a_h <= c * epsilon.
```

## E. Weighted packing bound

At a fixed level, sampled centers are separated at scale `a_h/L` and all lie in an `O(a_h)` near-optimal region.

Combining the center-wise empirical-Bernstein cost yields

```text
N <= C * sum_h lambda_h * sum_{c in A_h}
        [ g(c)/a_h^2 + 1/a_h ].
```

## F. Packing-to-volume conversion

Around each sampled center choose a disjoint infinity-norm ball of radius proportional to `a_h/L`.

For `x` in such a ball:

- `g(c) <= g(x) + O(a_h)`;
- `gap(x) <= O(a_h)`.

The ball volume contributes the factor `(a_h/L)^d`, so each discrete center term is bounded by a local integral term multiplied by `L^d`.

Summing the disjoint balls gives a level-wise integral over a constant-scale near-optimal region.

## G. Dyadic summation

A point `x` can appear in the expanded near-optimal region only at levels with

```text
a_h >= c * max{gap(x), epsilon}.
```

Geometric summation over such levels turns powers of `a_h` into powers of `gap(x)+epsilon`, producing

```text
g(x)/(gap(x)+epsilon)^(d+2)
+
1/(gap(x)+epsilon)^(d+1).
```

## H. Coarse levels

The finitely many levels with geometric uncertainty clipped at one contribute at most `O_d(1+L^d)`. For `epsilon <= 1`, this is absorbed by the displayed target functional up to dimension-dependent constants.

## Points the reviewer should try to break

1. simultaneous confidence under adaptive activation;
2. the parent-to-child near-optimality step;
3. disjoint-ball boundary handling on `[0,1]^d`;
4. the direction and scaling of the packing-to-volume inequality;
5. hidden dependence inside `Lambda`;
6. coarse-scale absorption.
