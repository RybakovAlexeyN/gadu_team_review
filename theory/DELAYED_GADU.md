# Delayed positive-only execution and GADU composition

This note records the execution contract and the minimal composition argument needed for review.

## Raw matured observation

For source round `s`, after age `w` define

```text
B_s^(w) = 1{Z_s = 1 and D_s <= w}.
```

Under the fresh-outcome model,

```text
B_s^(w) ~ Bernoulli(q_w f(x_s)).
```

Define `g_i = q_w f_i`. Common positive scaling preserves family ordering.

## Executable delayed certification

The delayed certifier:

1. maintains active dyadic cells;
2. samples designated cell centers to geometric cumulative targets;
3. after the last designated source of each checkpoint, makes exactly `w` legal filler deployments;
4. excludes filler feedback from the designated certification estimator;
5. finalizes designated Bernoulli outcomes only after the flush;
6. prunes/splits only after finalized confidence intervals are available;
7. returns `NOT_CERTIFIED` if the hard calendar horizon is exhausted.

Unresolved silence is never encoded as zero.

If `D` is the total number of designated source pulls and `C_h` is the number of synchronized checkpoints at level `h`, then before hard-horizon truncation

```text
T_cal = D + w * sum_h C_h.
```

## Certified-optimizer interface

Suppose the scaled optimizer returns

```text
ell_i^g <= g_i(z_i) <= g_i^* <= U_i^g,
0 <= g_i^* - g_i(z_i) <= xi_i^g.
```

For common known `q_w > 0`, define

```text
ell_i = max(0, ell_i^g/q_w)
U_i   = min(1, U_i^g/q_w)
Xi_i  = min(1, xi_i^g/q_w).
```

Then

```text
ell_i <= f_i(z_i) <= f_i^* <= U_i,
0 <= f_i^* - f_i(z_i) <= Xi_i.
```

The continuation gate must use latent-scale error `Xi_i`, not `xi_i^g`.

## Additive preflight composition

Let `I_T` be the immediate full-union certificate and `C_T(u)` the compatible prefix certificate. For a predeclared cutoff `B`, define

```text
V_fb(T,B) = B + C_T(T-B).
```

Enter the VS branch only if

```text
V_fb(T,B) <= (1+gamma) I_T.
```

At a certification checkpoint `s <= B`, commit only if family separation holds and

```text
s + (T-s) Xi_i <= V_fb(T,B).
```

If no certificate is accepted by `B`, restart the frozen full-union fallback on the fresh remaining horizon. Certification-owned source rounds, including filler rounds, are excluded from fresh fallback statistics.

On the simultaneous good event, the entered branch is bounded by `V_fb`. On the failure event, finite-horizon regret is at most `T`, yielding the additive `delta_vs T` term.

## Scope

This composition result does not claim uniform superiority, does not replace the existing scheduler theorem, and does not establish end-to-end regret optimality.
