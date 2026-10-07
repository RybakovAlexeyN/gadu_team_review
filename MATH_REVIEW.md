# Mathematical Review

This document is for an **independent attempt to break the candidate**. The useful output is not “looks good”; it is a precise **PASS / FIX / BLOCK** verdict tied to an exact theorem step or interface.

After the internal red-team pass, the public theorem files now expose the confidence allocation, empirical-Bernstein radius, lower-bound model, fine-gap cutoff, and delayed execution semantics. That hardening does **not** replace independent coauthor review.

## Verdict format

| Block | Verdict | Exact issue / smallest repair |
|---|---|---|
| Canonical algorithm | PASS / FIX / BLOCK | ... |
| Upper theorem | PASS / FIX / BLOCK | ... |
| Lower theorem | PASS / FIX / BLOCK | ... |
| Delayed / GADU bridge | PASS / FIX / BLOCK | ... |

A **BLOCK** should identify one implication that cannot be proved, ideally with a counterexample or the smallest failed lemma.

## 1. Upper theorem

- [Statement](theory/UPPER_THEOREM.md)
- [Proof roadmap](theory/UPPER_PROOF.md)

The proof chain is

$$
\text{empirical Bernstein confidence}
\Longrightarrow
\text{valid cell envelopes}
\Longrightarrow
\text{safe pruning}
\Longrightarrow
\text{near-optimal sampled children}
$$

$$
\Longrightarrow
\text{weighted packing}
\Longrightarrow
\text{packing-to-volume}
\Longrightarrow
\text{dyadic summation}
\Longrightarrow
\text{final integral bound}.
$$

Highest-value attacks:

1. Is the simultaneous confidence event valid under adaptive cell activation and stopping?
2. Does parent survival really imply that **every sampled child center** is near-optimal?
3. Is the packing-to-volume inequality in the correct direction, with the correct spatial scale and boundary volume?
4. Are the clipped coarse levels absorbed without hiding a dependence that changes the theorem?
5. Are the explicit confidence allocation and $\Lambda$ definition correct?
6. Is the transition between $a_h=1$ and the fine dyadic regime correct?
7. Do the edge cases $L_g=0$, small $L_g$, flat $g$, and $\varepsilon$ near $1$ behave as claimed?

## 2. Lower theorem

- [Statement](theory/LOWER_THEOREM.md)
- [Proof outline](theory/LOWER_PROOF.md)

The intended chain is

$$
\text{hard alternatives}
\Longrightarrow
\text{Bernoulli KL}
\Longrightarrow
\text{adaptive change of measure}
\Longrightarrow
\text{disjoint one-layer packing}
$$

$$
\Longrightarrow
\text{layer aggregation}
\Longrightarrow
\text{fine-gap integral}.
$$

Attack:

1. Do all perturbations remain in the declared $L$-Lipschitz model class?
2. Does each alternative actually flip the best family?
3. Is the Bernoulli KL upper bound valid on the full stated parameter range?
4. Is the logarithmic layer-selection loss explicit and correctly counted?
5. Is the frozen cutoff $c_0=1/6$ compatible with every construction step?
6. Does any line accidentally enlarge the statement from $A_{\mathrm{fine}}$ to all of $X$?
7. Is the model class broad enough to contain every change-of-measure alternative?
8. Are $\delta\in(0,1/2)$, $\delta$-correctness, stopping time, and measurability all stated consistently?

## 3. Canonical procedure

- [VS-Certify-Delayed](ALGORITHM.md)
- [Algorithm → proof obligations](theory/ALGORITHM_PROOF_MAP.md)

Before reviewing theorem complexity, verify that the pseudocode defines **one executable procedure**.

Attack:

1. Are distinct objects given distinct symbols?
2. Are generated designated sources $m_I$ separated from finalized observations $n_I$?
3. Does each inner loop terminate for a fixed checkpoint target in the no-cutoff core?
4. Is a resolved cell's state frozen correctly through the current level?
5. Are parent/child samples kept separate unless a proof explicitly permits reuse?
6. Does `NOT_CERTIFIED` return enough accounting to preserve source ownership?
7. Is statistical family certification separated from the downstream GADU commit decision?
8. Is the within-family core analyzed by the upper theorem the same state update used by the delayed controller?
9. Is an incomplete checkpoint under the hard cutoff accounted for correctly?
10. Is there a legal action for every declared input and every calendar round?

## 4. Delayed / GADU bridge

- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)

Check:

- one legal deployment every calendar round;
- $w=0$ and a delay exactly equal to $w$;
- unresolved feedback is never converted into zero, including at the hard cutoff;
- the active set is frozen during the flush;
- filler feedback is excluded from the designated estimator;
- source ownership remains clean after fallback, including later arrivals;
- scaled certificates are translated back to latent scale correctly;
- the continuation gate uses $\Xi_i$, not $\xi_i^g$.

## What counts as a valuable review result?

The most valuable output is one of:

- a concrete counterexample;
- an exact inequality with the wrong direction or missing factor;
- a concentration statement whose assumptions do not match the algorithm;
- an alternative that leaves the declared model class;
- a delayed-execution step that depends on unavailable information;
- a minimal wording repair that narrows the theorem back to what is actually proved.