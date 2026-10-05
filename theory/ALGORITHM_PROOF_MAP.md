# VS-Certify-Delayed — algorithm-to-proof map

This file maps the canonical pseudocode in [`ALGORITHM.md`](../ALGORITHM.md) to the exact mathematical obligation that justifies each nontrivial step.

The purpose is adversarial review: a reviewer should be able to point to one row and say **PASS / FIX / BLOCK** without reconstructing dependencies from the whole paper.

## Status convention

- **CLOSED** — the logical implication is written explicitly in the current review materials.
- **CLOSED / EXTERNAL CONCENTRATION CHECK** — the algorithmic implication is explicit, but the underlying empirical-Bernstein concentration/algebra is still a high-value independent check.
- **CLOSED / GEOMETRIC CHECK** — the proof chain is explicit, but the packing/integral calculation remains a high-value independent check.
- **INTERFACE-CLOSED** — the composition is proved at the declared interface level; this does not mean the old flagship theorem was replaced.

## Map

| Algorithm block | Mathematical obligation | Current support | Status |
|---|---|---|---|
| Inputs: common known \(q_w>0\), valid \(L_i>0\) | Scaled surface \(g_i=q_wf_i\) preserves family ordering and satisfies \(\operatorname{Lip}(g_i)\le q_wL_i\) | `DELAYED_GADU.md`; manuscript VS insert | CLOSED |
| Preallocate \(\delta_i\), \(\eta_{i,h,I,r}\) | All adaptive cell/checkpoint confidence statements hold on one simultaneous event with probability at least \(1-\delta_{\rm cert}\) | Upper proof Lemma A | CLOSED / EXTERNAL CONCENTRATION CHECK |
| Initialize fresh cell state | A child estimator contains samples only from deployments at its own center | `ALGORITHM.md` state contract | CLOSED |
| Top up unresolved center until \(m_I=n_r\) | The loop is well-defined; generated-source count increases every designated deployment | canonical pseudocode | CLOSED |
| Geometric targets \(n_r=2^{r+1}\) | Every center reaches `rad <= a_h/8` after finitely many checkpoints in the no-cutoff core | Upper proof Lemma B | CLOSED / EXTERNAL CONCENTRATION CHECK |
| Designated deployment at \(c_I\) | Finalized designated observations at a fixed center are Bernoulli with mean \(g_i(c_I)\) under the fresh-outcome model | `DELAYED_GADU.md`; source-exact model audit | CLOSED |
| Exactly \(w\) legal filler deployments | At the checkpoint update every designated source generated before the flush has age at least \(w\); delay exactly \(w\) is observable | `ALGORITHM.md` chronology; `DELAYED_GADU.md` | CLOSED |
| Exclude filler feedback from designated estimator | Designated confidence sequence contains only the source-tagged samples analyzed by the theorem | execution contract | CLOSED |
| Hard cutoff returns `NOT_CERTIFIED(Acct)` | No unresolved silence is converted to zero; no false family certificate is emitted; source ownership is preserved | `ALGORITHM.md`; substitution lemma | CLOSED |
| Finalize \(B_s^{(w)}\) | \(B_s^{(w)}=\mathbf1\{Z_s=1,D_s\le w\}\sim\mathrm{Bernoulli}(q_w f_i(c_I))\) | `DELAYED_GADU.md`; manuscript raw-Bernoulli representation | CLOSED |
| Empirical mean / variance / radius | On the simultaneous good event, \(|\widehat g_I-g_i(c_I)|\le\operatorname{rad}_I\) | Upper proof Lemma A | CLOSED / EXTERNAL CONCENTRATION CHECK |
| Mark resolved when `rad <= a/8` | Resolution yields the constants needed for safe pruning, \(5a/2\) certificate width, and \(6a\) sampled-child gap | Upper proof Lemmas E–G | CLOSED |
| \(U_{\rm cell}(I)=\min\{1,\widehat g_I+\operatorname{rad}_I+a_{i,h}\}\) | This upper-bounds \(\sup_{x\in I}g_i(x)\) | Upper proof Lemma C | CLOSED |
| `LCB(I)` | `LCB(I) <= g_i(c_I)` on the same event | Upper proof Lemma C | CLOSED |
| Family envelopes \(\underline M_i^g,\overline M_i^g\) | \(\underline M_i^g\le g_i^\star\le\overline M_i^g\) | maximizer survival + cell envelope; interface extraction proposition | CLOSED |
| Choose \(z_i\) by largest LCB | \(g_i^\star-g_i(z_i)\le \xi_i^g:=\overline M_i^g-\underline M_i^g\) | interface extraction proposition; Upper proof Lemma G | CLOSED |
| Family separation | \(\underline M_i^g>\max_{j\ne i}\overline M_j^g\) implies unique best family | best-family proposition / substitution lemma | CLOSED |
| Divide certificate by \(q_w\) | Returns Proposition-11-style latent bounds and deployment error for every family | scaled-to-latent bridge proposition | INTERFACE-CLOSED |
| `CERTIFIED` does not auto-commit | Downstream GADU numerical gate remains a separate deterministic comparison | `DELAYED_GADU.md`; `gadu_vs_preflight_corollary.tex` | INTERFACE-CLOSED |
| Prune iff \(U_{\rm cell}(I)<\underline M_i^g\) | A cell containing a maximizer cannot be pruned | Upper proof Lemma D | CLOSED |
| Survivor geometry | Every survivor center has gap at most \(5a_h/2\) | Upper proof Lemma E | CLOSED |
| Split survivors into fresh children | Every sampled child has gap at most \(6a_h\); no parent/child sample reuse is assumed | Upper proof Lemma F | CLOSED |
| Single-family stop at \(a_h\le2\varepsilon/5\) | Returned direct-oracle certificate has width at most \(\varepsilon\) | Upper proof Lemma G | CLOSED |
| Center sample bound | \(N_c(h)\lesssim g(c)\Lambda/a_h^2+\Lambda/a_h\) | Upper proof Lemma B | CLOSED / EXTERNAL CONCENTRATION CHECK |
| Sum over sampled centers | Discrete complexity bound | Upper proof Lemma H | CLOSED |
| Packing-to-volume | Discrete near-optimal centers convert to local integral | Upper proof Lemma I | CLOSED / GEOMETRIC CHECK |
| Dyadic sum | Produces denominators \((\mathrm{gap}+\varepsilon)^{d+2}\) and \((\mathrm{gap}+\varepsilon)^{d+1}\) | Upper proof Lemma J | CLOSED / GEOMETRIC CHECK |
| Clipped coarse levels | Coarse contribution is absorbed by the theorem functional | Upper proof Lemma K | CLOSED / GEOMETRIC CHECK |
| Calendar identity | On a completed, nontruncated path \(T_{\rm cal}=D+w\sum_hC_h\) | calendar proposition | CLOSED |
| Clean fallback after failure/rejection | Later arrivals from certification-owned sources are excluded; future source outcomes are fresh conditionally on history | substitution lemma; source-exact audit | INTERFACE-CLOSED |
| Preflight / commit gate | Entered branch is no worse than declared fallback certificate on the good event, plus \(\delta_{\rm vs}T\) | `gadu_vs_preflight_corollary.tex` | INTERFACE-CLOSED |

## Exact upper-proof constants now exposed

The current proof roadmap no longer hides the central geometry behind \(O(a_h)\):

\[
\text{survivor center gap}\le \frac52 a_h,
\]

\[
\text{sampled child gap}\le 6a_h,
\]

and at a resolved level

\[
U^g-\ell^g\le\frac52 a_h.
\]

Therefore

\[
a_h\le\frac{2\varepsilon}{5}
\quad\Longrightarrow\quad
\xi\le\varepsilon.
\]

The parent-to-child argument uses the inequality

\[
a_{h-1}\le2a_h,
\]

which remains valid at the clipped/fine transition. It does **not** require equality there.

## What is still worth attacking independently

After this mapping, the remaining highest-value mathematical attacks are narrow rather than architectural:

1. **Empirical-Bernstein source theorem and constants.** Re-derive the two-sided computable radius and the sufficient sample-size constants used in Lemmas A–B.
2. **Packing-to-volume direction.** Check the exact ball radius, boundary volume, and the conversion of the \(g(c)/a_h^2\) term.
3. **Dyadic summation.** Check pointwise level membership and the replacement of \(\max\{\mathrm{gap},\varepsilon\}\) by \(\mathrm{gap}+\varepsilon\).
4. **Coarse absorption.** Check the claimed \(O_d(1+L_g^d)\) contribution uniformly over the allowed parameter range.
5. **Source-exact GADU composition.** Confirm that no old Theorem 1/8 or Theorem 9 numerical quantity is silently reused by the VS branch.

A BLOCK should identify one row above, the exact failed implication, and the smallest repair.
