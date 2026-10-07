# VS-Certify-Delayed — Algorithm-to-Proof Map

This file maps the canonical pseudocode in [`ALGORITHM.md`](../ALGORITHM.md) to the mathematical obligation that justifies each nontrivial step.

The purpose is adversarial review: a reviewer should be able to point to one row and return **PASS / FIX / BLOCK** without reconstructing the entire dependency graph.

## Status convention

- **DOCUMENTED** — the logical implication is written explicitly in the current review materials; this is not an independent human verification verdict.
- **DOCUMENTED / CHECK CONCENTRATION** — the algorithmic implication is explicit, while the empirical-Bernstein source theorem/algebra remains a high-value independent check.
- **DOCUMENTED / CHECK GEOMETRY** — the proof chain is explicit, while the packing/integral calculation remains a high-value independent check.
- **INTERFACE-DOCUMENTED** — the composition is written at the declared interface level; this does not mean the historical flagship theorem has been replaced or independently verified.

## Map

| Algorithm block | Mathematical obligation | Current support | Status |
|---|---|---|---|
| Common known $q_w>0$ and valid $L_i>0$ | $g_i=q_wf_i$ preserves family ordering and satisfies $\mathrm{Lip}(g_i)\le q_wL_i$ | `DELAYED_GADU.md` | **DOCUMENTED** |
| Preallocate $\delta_i$ and $\eta_{i,h,I,r}$ | All adaptive cell/checkpoint confidence statements hold on one event with probability at least $1-\delta_{\mathrm{cert}}$ | Upper proof, Lemma A | **DOCUMENTED / CHECK CONCENTRATION** |
| Initialize fresh cell state | A child estimator contains only samples from deployments at its own center | `ALGORITHM.md` | **DOCUMENTED** |
| Top up unresolved center until $m_I=n_r$ | Generated-source count increases on every designated deployment; loop is well-defined | canonical pseudocode | **DOCUMENTED** |
| Geometric targets $n_r=2^{r+1}$ | Every center reaches $\mathrm{rad}\le a_h/8$ after finitely many checkpoints in the no-cutoff core | Upper proof, Lemma B | **DOCUMENTED / CHECK CONCENTRATION** |
| Designated deployment at $c_I$ | Finalized designated observations at one center are Bernoulli with mean $g_i(c_I)$ under the fresh-outcome model | `DELAYED_GADU.md` | **DOCUMENTED** |
| Exactly $w$ legal filler deployments | Every designated source generated before the flush has age at least $w$ at checkpoint update; delay exactly $w$ is observable | `ALGORITHM.md`, `DELAYED_GADU.md` | **DOCUMENTED** |
| Exclude filler feedback | The confidence sequence contains only the designated source-tagged observations analyzed by the theorem | execution contract | **DOCUMENTED** |
| Hard cutoff returns `NOT_CERTIFIED(Acct)` | No unresolved silence is converted to zero; no false certificate is emitted; ownership is preserved | `ALGORITHM.md`, bridge note | **DOCUMENTED** |
| Finalize $B_s^{(w)}$ | $B_s^{(w)}=\mathbf1\{Z_s=1,D_s\le w\}\sim\mathrm{Bernoulli}(q_w f_i(c_I))$ | `DELAYED_GADU.md` | **DOCUMENTED** |
| Empirical mean / variance / radius | On the simultaneous event, $|\widehat g_I-g_i(c_I)|\le\mathrm{rad}_I$ | Upper proof, Lemma A | **DOCUMENTED / CHECK CONCENTRATION** |
| Resolve when $\mathrm{rad}\le a/8$ | Resolution yields the constants needed for safe pruning, $5a/2$ certificate width, and $6a$ sampled-child gap | Upper proof, Lemmas E–G | **DOCUMENTED** |
| $U_{\mathrm{cell}}(I)=\min\{1,\widehat g_I+\mathrm{rad}_I+a_{i,h}\}$ | Upper-bounds $\sup_{x\in I}g_i(x)$ | Upper proof, Lemma C | **DOCUMENTED** |
| $\mathrm{LCB}(I)$ | $\mathrm{LCB}(I)\le g_i(c_I)$ on the same event | Upper proof, Lemma C | **DOCUMENTED** |
| Family envelopes $\underline M_i^g,\overline M_i^g$ | $\underline M_i^g\le g_i^\star\le\overline M_i^g$ | maximizer survival + cell envelopes | **DOCUMENTED** |
| Choose $z_i$ by largest LCB | $g_i^\star-g_i(z_i)\le\xi_i^g:=\overline M_i^g-\underline M_i^g$ | interface extraction; Upper proof, Lemma G | **DOCUMENTED** |
| Family separation | $\underline M_i^g>\max_{j\ne i}\overline M_j^g$ implies a unique best family | best-family proposition / bridge | **DOCUMENTED** |
| Divide certificate by $q_w$ | Returns latent family bounds and deployment error | scaled-to-latent bridge | **INTERFACE-DOCUMENTED** |
| `CERTIFIED` does not auto-commit | Downstream GADU numerical gate remains a separate deterministic comparison | `DELAYED_GADU.md` | **INTERFACE-DOCUMENTED** |
| Prune iff $U_{\mathrm{cell}}(I)<\underline M_i^g$ | A cell containing a maximizer cannot be pruned | Upper proof, Lemma D | **DOCUMENTED** |
| Survivor geometry | Every survivor center has gap at most $5a_h/2$ | Upper proof, Lemma E | **DOCUMENTED** |
| Split survivors into fresh children | Every sampled child has gap at most $6a_h$; no parent/child sample reuse is assumed | Upper proof, Lemma F | **DOCUMENTED** |
| Single-family stop at $a_h\le2\varepsilon/5$ | Returned direct-oracle certificate has width at most $\varepsilon$ | Upper proof, Lemma G | **DOCUMENTED** |
| Center sample bound | $N_c(h)\lesssim g(c)\Lambda/a_h^2+\Lambda/a_h$ | Upper proof, Lemma B | **DOCUMENTED / CHECK CONCENTRATION** |
| Sum over sampled centers | Discrete complexity bound | Upper proof, Lemma H | **DOCUMENTED** |
| Packing-to-volume | Discrete near-optimal centers convert to the local integral | Upper proof, Lemma I | **DOCUMENTED / CHECK GEOMETRY** |
| Dyadic sum | Produces denominators $(\mathrm{gap}+\varepsilon)^{d+2}$ and $(\mathrm{gap}+\varepsilon)^{d+1}$ | Upper proof, Lemma J | **DOCUMENTED / CHECK GEOMETRY** |
| Clipped coarse levels | Coarse contribution is absorbed by the theorem functional | Upper proof, Lemma K | **DOCUMENTED / CHECK GEOMETRY** |
| Calendar identity | On a completed non-truncated path, $T_{\mathrm{cal}}=D+w\sum_h C_h$ | delayed calendar proposition | **DOCUMENTED** |
| Clean fallback | Later arrivals from certification-owned sources are excluded; future source outcomes are conditionally fresh | bridge / source-ownership audit | **INTERFACE-DOCUMENTED** |
| Preflight / commit gate | Entered branch is no worse than the declared fallback certificate on the good event, plus $\delta_{\mathrm{vs}}T$ | GADU-VS composition | **INTERFACE-DOCUMENTED** |

## Exact upper-proof constants

The current proof roadmap exposes the central geometric constants:

$$
\mathrm{gap}(\text{survivor center})
\le
\frac52a_h,
$$

$$
\mathrm{gap}(\text{sampled child})
\le
6a_h,
$$

and

$$
U^g-\ell^g
\le
\frac52a_h.
$$

Hence

$$
a_h\le\frac{2\varepsilon}{5}
\quad\Longrightarrow\quad
\xi\le\varepsilon.
$$

The parent-to-child argument uses

$$
a_{h-1}\le2a_h,
$$

which remains valid at the clipped/fine transition and does not require equality there.

## What remains worth attacking independently

1. **Empirical-Bernstein source theorem and constants.** Re-derive the two-sided computable radius and sufficient sample-size constants used in Lemmas A–B.
2. **Packing-to-volume direction.** Check the exact ball radius, boundary volume, and conversion of the $g(c)/a_h^2$ term.
3. **Dyadic summation.** Check pointwise level membership and the replacement of $\max\{\mathrm{gap},\varepsilon\}$ by $\mathrm{gap}+\varepsilon$.
4. **Coarse absorption.** Check the claimed $O_d(1+L_g^d)$ contribution uniformly over the allowed parameter range.
5. **Source-exact GADU composition.** Confirm that no historical Theorem 1/8 or Theorem 9 numerical quantity is silently reused by the VS branch.

A BLOCK should name the exact row above, the failed implication, and the smallest repair.