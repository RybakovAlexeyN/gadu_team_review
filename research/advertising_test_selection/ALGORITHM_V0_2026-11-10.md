# Advertising test selection under delayed positive-only feedback — v0.1

**Date:** 2026-11-10  
**Owner:** Alexey Rybakov  
**Status:** executable RESEARCH BASELINE / REQUEST FOR CRITICAL REVIEW. Not a novel published algorithm, not original GADU, not an implementation of Alexander Savelyev's proposed joint likelihood estimator. This note does not claim improved performance or applicability to production advertising without empirical validation.

## 1. Why this problem matters

A DTC team has a finite testing budget and several advertising creatives to test. The objective is to choose the most promising creative at the end of the allocated budget, using conversion events that arrive late. We want to test whether additional *justified* structure between ad hypotheses can improve the efficiency of this process.

Main testable question: **When, if ever, does a graph/metric expressing relationships between advertising hypotheses reduce the cost of identifying a better creative in the presence of delayed conversions?** This is a question, not a claim.

## 2. Narrow model and objective

- Fixed finite creative set `A={1,...,K}`; one decision per round assigns one comparable-cost impression/exposure to one creative. Budget `B` exposures (not arbitrary real currency).
- Unknown fixed conversion rates `p_i in [0,1]` for a common population/context; conditional on chosen arm, `Z_t ~ Bernoulli(p_i)`, independently across exposures.
- If `Z_t=1`, a positive event appears after delay `D_t`; if `Z_t=0`, there is no event. Delays are independent of choice, conversion probability, and other exposures, with **known** common CDF `F`. We observe positive events with attributed exposure IDs; no explicit negative labels.
- Fixed observation window `w` with `q=F(w)>0`. At time `t` only deployments at times `s <= t-w` are included in the estimator. All later events from those deployments are ignored by v0. This eliminates immature non-conversions being treated as negatives.
- Optional side information: a **pre-specified** metric/shortest-path distance `d(i,j)` between creatives, and a **valid** constant `L >=0` satisfying `|p_i-p_j| <= L*d(i,j)` for every pair. This is an assumption, NOT established for semantic or brand-association graphs.
- Primary offline criterion (synthetic known-`p` evaluation): **simple regret** `p_* - p_{recommendation after B}`. Secondary: cumulative pseudo-regret during testing, computation, and sensitivity to misspecification. Real-world counterfactual differences cannot be learned merely from logged historical campaigns without identification assumptions or randomized tests.

## 3. Estimator and simultaneous confidence intervals

For arm i at time t, let `S_i(t)={s<=t-w : a_s=i}`, `n_i=|S_i(t)|`, and

`M_i = sum_{s in S_i(t)} 1{conversion from s arrives by s+w}`.

Then `E[M_i/n_i] = q*p_i`, and for `n_i>0`:

`p_hat_i = M_i/(q*n_i)`.

For fixed `B, K, delta in (0,1)`, define

`beta_i = sqrt(log(2*K*B/delta)/(2*n_i*q^2))`;
`lower_i=max(0,p_hat_i-beta_i)`, `upper_i=min(1,p_hat_i+beta_i)`.

If `n_i=0`, interval is `[0,1]`. The values of `p_hat_i` can exceed 1 before clipping confidence bounds because of the importance scale `1/q`. Under the stated iid and known-q assumptions, pre-sampling independent outcomes for each arm and taking a union bound over all `i,n<=B` yields simultaneous interval coverage at least `1-delta`. This is a conservative Hoeffding construction, not a new theorem.

**Optional graph envelope, only if the Lipschitz assumption is true:**

`U_i = min(1, min_j (upper_j + L*d(i,j)))`

`L_i = max(0, max_j (lower_j - L*d(i,j)))`.

Every true `p_i` lies in `[L_i,U_i]` on the above coverage event. If the metric or L is misspecified, the guarantee fails. Compare to unstructured version `U_i=upper_i, L_i=lower_i`.

## 4. Executable policy: Window–Graph UCB (WG-UCB v0)

Input: creatives, B, w, known q, delta, optional `(d,L)`.

State: `n_i`, `M_i`, deployments per arm, pending fixed-window maturity events. An impression is deployed every round; the policy **never pauses time** to wait for conversions.

At each round `t=0,...,B-1`:

1. Mature all deployments with original time `s=t-w`. For each, increment `n_i`; increment `M_i` if and only if its conversion occurred within w.
2. Compute per-arm confidence intervals; optionally propagate them through the graph metric, producing `(L_i,U_i)`.
3. Choose `a_t = argmax_i U_i`; resolve ties first by the fewest TOTAL deployments (not just matured deployments), then by fixed arm index. This keeps the decision defined even when no feedback has matured.
4. Deploy one exposure to `a_t`; store its exposure ID and timestamp. When its observation window closes, it will become one matured sample. Do not access latent outcomes at choice time.

After budget B, recommend `argmax_i L_i`. **This is a concrete conservative recommendation rule, not proven optimal for simple regret.** Optionally certify arm i if `L_i > max_{j != i} U_j`, valid only under the assumptions and confidence event. In the first version, no early stopping or budget reallocation is used.

The code contains a synthetic simulator and a smoke comparison against a no-graph Window-UCB using the same observation rule.

## 5. Minimal executed smoke test, not evidence for an improvement

Command: `python window_graph_ucb_v0.py` (NumPy dependency). On 2026-11-10, the script executed for one deliberately simple smooth six-creative synthetic world, B=1500, w=4, 20 RNG seeds per method. Both variants achieved measured mean simple regret `0.0` in this **easy** setup; matured count for seed 0 was `1497`. This test proves only that the code runs on the toy world and is not a nontrivial performance comparison, let alone real advertising evidence. No source-exact GADU comparison was performed.

## 6. What is / is not the contribution

- **Currently available:** mathematically specified, executable, reproducible baseline + a falsifiable hypothesis about useful relationships among creatives.
- **NOT claimed:** mathematical novelty, empirical superiority, positive business uplift, robustness to nonstationarity, unequal costs, changing audiences, unknown F, graph misspecification, or original GADU parity.
- Existing delayed conversion bandits were studied by Vernade, Cappé, Perchet (UAI 2017); delayed linear bandits with positive-only observations by Vernade et al. (ICML 2020). Our v0 is a baseline, not a claim to supersede them.
- The proposed **joint Lipschitz-constrained likelihood** approach discussed with Alexander Savelyev is **different** from this confidence-envelope method and remains open.

## 7. Alexander Savelyev's proposal (29 October 2026): joint Lipschitz-constrained likelihood

**Provenance / status.** This is an attributed **research proposal**, discussed by Alexander Savelyev, Alexey Rybakov, and Ilgham Latypov on 29 October 2026. The meeting notes and noisy ASR transcript are in [the call summary](../../context/team_call_2026-10-29.md) and [the full call transcript](../../context/team_call_2026-10-29_full_transcript.md). The equations below formalize the *substance of the discussion*; in particular the delayed-feedback log-likelihood is **a mathematical reconstruction in the meeting notes, not a verbatim transcription of Alexander's board or an author-approved final model**.

### 7.1. Motivation: avoid treating related points as unrelated

In a continuum/structured action space, discretizing first and independently estimating conversion probabilities at the resulting grid points can throw away information. If true success probabilities obey a Lipschitz relation, observations at nearby actions jointly constrain their plausible values.

For sampled/available actions x_1,...,x_n, introduce unknown positive-outcome probabilities p_i = p(x_i). With a preselected distance d(x_i,x_j) (or norm of the difference) and a valid constant L:

```text
0 <= p_i <= 1                              for i=1,...,n
|p_i - p_j| <= L * d(x_i, x_j)             for all i,j
```

Alexander first discussed local/pairwise likelihood bounds; the group identified their dependence on a reference point and inconsistency across 3+ points. The more coherent proposal was to maximize **one joint likelihood over the whole vector** p=(p_1,...,p_n), subject to **all** Lipschitz constraints, and update the estimate when new observations arrive.

### 7.2. Joint estimation (no delays: conceptual starting point)

If at action i we observed s_i successes and f_i **genuinely observed** failures without delay, a simple joint likelihood would be

```text
maximize over p_1,...,p_n:
    sum_i [ s_i * log(p_i) + f_i * log(1 - p_i) ]
subject to:
    0 <= p_i <= 1,
    |p_i - p_j| <= L * d(x_i, x_j) for all i,j.
```

Here the coupling is through the **constraints**, not an assumed independence of the unknown parameters. This differs from taking independent per-action MLEs and *afterwards* tightening confidence intervals by a Lipschitz envelope (the implemented WG-UCB v0).

### 7.3. Delayed positive-only feedback: provisional reconstruction

For each exposure k assigned to action i(k), suppose a latent Bernoulli success occurs with probability p_{i(k)}. Conditional on success, its report arrives after a random delay with **known** common CDF F, independent across exposures and of the action. At one clearly defined analysis time T, let a_k=T-s_k be the exposure's age, and let y_k=1 iff its positive report has arrived by T (otherwise y_k=0, which **does not mean a confirmed failure**).

Under *these extra assumptions*:

```text
P(y_k = 1 | p, a_k) = p_{i(k)} * F(a_k)
P(y_k = 0 | p, a_k) = 1 - p_{i(k)} * F(a_k)

maximize over p_1,...,p_n:
    sum_k [ y_k * log(p_{i(k)} * F(a_k))
          + (1-y_k) * log(1 - p_{i(k)} * F(a_k)) ]
subject to:
    0 <= p_i <= 1,
    |p_i - p_j| <= L * d(x_i, x_j) for all i,j.
```

**Critical data rule:** each exposure contributes **one** current observation at the chosen analysis time, not an independent term for each minute/day that it remains pending. Repeated snapshots of the *same* exposure are dependent. If exact conversion arrival times, changing observation windows, late reports, unknown F, context changes, or other censoring mechanisms are present, this likelihood must be re-derived from the actual observation process. Boundary cases such as F(a)=0 must be handled explicitly in numerical code. No claim of correctness for an unspecified ad platform observation model is made.

### 7.4. What remains open (not yet an executable policy)

1. **Action semantics:** is x an ad creative, message/angle, persona–angle–hook tuple, continuous embedding, or another testable object? What is held constant across tests?
2. **Validity of structure:** what observed evidence would support or reject a Lipschitz relation between ad hypotheses? No guarantee follows from an arbitrary text embedding or assumed similarity graph.
3. **Selection policy:** a constrained MLE returns estimates, **not** the next action x_t. We still need uncertainty quantification, exploration/exploitation, budget constraints, stopping/switching rules, and an explicit objective such as simple regret or business value of the next test.
4. **Theory and computation:** analyze concentration/identifiability/optimization with pairwise constraints (up to O(n²) explicit comparisons), and possible comparison with Gaussian-process alternatives under their different assumptions.
5. **Minimal falsifiable experiment:** first solve a 2–3-action synthetic example with delayed observations; compare constrained joint estimation against independent estimation, then attach and evaluate a decision policy under matched assumptions.

**Important:** the executable Python file in this directory implements **Window–Graph UCB**, not Alexander's constrained joint MLE. This section is a separately attributed candidate direction awaiting mathematical and empirical review; neither novelty nor a regret guarantee was established in the meeting.

## 8. Exact review questions (Alexander / Ilgham)

1. Does the fixed-window, known-q observation model map to a meaningful version of DTC creative testing, or is another definition of action/reward essential?
2. Is simple regret after budget B the right primary objective, or should we explicitly minimize cumulative regret / cost of identification? What decision would the client actually make?
3. Is the metric/Lipschitz premise meaningful for real creatives? What *empirical* test would reject it? Should we first use product/category/audience structure rather than brand-association graphs?
4. Could a joint constrained likelihood estimator use *immature* survival observations more efficiently than the fixed-window correction? What confidence sets and decision rule would be needed?
5. Which closest prior art already covers the meaningful part, and what new scientific statement remains to be investigated?

## 9. Smallest next research step

Lock 3 paired worlds: (A) true graph smoothness with helpful structure, (B) valid but weak/uninformative structure, (C) deliberately misspecified graph. For each, sweep budgets and delay laws; report simple regret, cumulative pseudo-regret, uncertainty intervals across seeds, and ablations for graph/no graph. Compare with a stronger delayed bandit baseline from the literature where implementable. Avoid interpreting this as a causal test of brand advertising.

Sources: https://proceedings.mlr.press/r15/vernade17a.html ; https://proceedings.mlr.press/v119/vernade20a.html .