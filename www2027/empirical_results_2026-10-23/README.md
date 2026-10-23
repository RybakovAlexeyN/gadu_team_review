# WWW 2027 / GADU — empirical results for team review (23 October 2026)

**Status: PUBLIC PRELIMINARY EMPIRICAL HANDOFF — not accepted manuscript evidence.**

**Update 23 Oct:** Removed test-outcome-dependent campaign eligibility from the inverse-window experiment, added regression test, reran full Criteo on pinned revision. This is a **post-hoc methodological repair**, not a fresh independent holdout. All corrected metrics below supersede the original 293-campaign values.
  
**Дата:** 23.10.2026 | **Scope:** source-informed independent GADU implementations, strong Cover-UCB baselines, public Criteo Attribution observational data.

> **TL;DR (RU):** В исследованных синтетических сценариях GADU не показывает меньший фактический pseudo-regret, чем корректно настроенный Cover-UCB: предварительная сертификация семейств оказывается дорогой. На 16,47 млн реальных показов Criteo обнаружена неоднородность времён конверсии между кампаниями, которая заметно влияет на оценку windowed positive-only correction. **Реальный regret политики GADU не измерен.**

## 1. Scientific questions

- **Synthetic:** Does the independently transcribed WWW GADU policy pay less **realized cumulative latent pseudo-regret** than **source-optimized immediate Cover-UCB** under explicitly fixed finite-horizon Lipschitz/Bernoulli worlds? Which testing phases contribute to regret?
- **Real, observational:** Is a shared conversion delay probability adequate across campaigns? How accurately does inverse-window weighting recover **7-day conversion-event counts** from shorter windows on genuine Criteo histories?
- **Not tested:** Counterfactual online GADU policy regret on real advertising traffic; original-author exact experimental code; actual reporting/notification delay as distinct from impression-to-conversion latency; any causal ROI effect.

## 2. Synthetic results

### 2.1. 80 paired holdout seed–world rows, three policies per row

Independent source-informed WWW GADU versus optimized Bernstein Cover-UCB versus simple fixed-net diagnostic. Five pilot-informed worlds, **16 new pre-locked seeds each**, T = 3,000,000, K = 2, q_w = 1, w = 1, gamma = 0.25. Lower regret is better.

| World | Mean Cover regret | Mean GADU regret | Paired GADU − Cover [95% t interval] | GADU worse |
|---|---:|---:|---:|---:|
| Strong family gap 0.62 | 24,392 | 91,957 | +67,565 [67,498, 67,632] | 16/16 |
| Moderate gap 0.35 | 24,682 | 65,299 | +40,617 [40,573, 40,662] | 16/16 |
| Near tie 0.02 | 26,849 | 36,435 | +9,585 [9,417, 9,754] | 16/16 |
| Exact tie | 4,881 | 13,769 | +8,888 [8,742, 9,033] | 16/16 |
| Off-center strong gap | 139,799 | 205,080 | +65,282 [65,234, 65,330] | 16/16 |

**Interpretation:** GADU loses on these **selected** worlds; these intervals only quantify seed-level Monte Carlo variation conditional on world/configuration, not general-population significance. In strong-gap, GADU's pre-certification Search already accumulates about **69,915** pseudo-regret out of its ~91,957 final regret. GADU correctly certifies the best family for all 16 strong-gap seeds, but this benefit does not recover the Search cost. **q_w = 1 does not exercise positive censoring**.

[Machine-readable aggregate table](data/synthetic_q1_heldout_80_aggregate.csv). The 80-row original raw archive and executable bundle were preserved in a separate private research conversation artifact; **they are not silently claimed to be part of this public repository**.

### 2.2. 16 paired runs with nontrivial positive-only censoring

Independent author-text-informed policy, same T = 3,000,000 and w = 1; q_w in {0.75, 0.5}; strong gap 0.62 vs near tie 0.02; **4 locked seeds per cell**.

| q_w | Gap | Cover regret mean | GADU regret mean | GADU − Cover mean |
|---:|---:|---:|---:|---:|
| 0.75 | 0.62 | 135,540 | 145,952 | **+10,413** |
| 0.75 | 0.02 | 138,795 | 140,568 | **+1,773** |
| 0.50 | 0.62 | 135,818 | 379,112 | **+243,294** |
| 0.50 | 0.02 | 139,848 | 143,521 | **+3,672** |

This is a genuine **synthetic** Bernoulli/positive-only event-channel study. When q changes, the policy's chosen grid and planned testing budget change too; therefore **the q=0.5 vs q=0.75 contrast cannot be attributed solely to censoring**. In the q=0.5/strong-gap cell, GADU regret is actually deterministic under the selected geometry; the paired SD measures Cover variation, not stochastic GADU variation. Four seeds per cell are not enough for broad statistical generalization.

[Machine-readable aggregate table](data/synthetic_q_lt1_16_aggregate.csv).

### 2.3. Other public raw data and important control

- [32 raw matched rows](data/synthetic_T3m_oct22_raw32.csv), two worlds × 16 seeds at q=1, w=1, T=3m, three policies; an earlier independently run end-to-end diagnostic **with different configurations from the 80-row holdout**.
- [448 raw policy executions](data/synthetic_certification_fairness_raw448.csv), seven worlds × 16 seeds × four policies at T=5,000. Includes source Cover versus fixed-net one-stage comparators; *candidate/certificate acceptance* is distinct from actual realized regret and time budget. Fixed-net controls do not establish the original WWW theorem.
- [Earlier public 32-seed/96-policy engineering smoke](../synthetic_evaluation_2026-10-21/README.md) from October 21. Its nets degenerated to one point per family and cannot validate continuum tuning.

**Strongest permitted negative claim:** these independent implementations have higher realized cumulative pseudo-regret than optimized Cover-UCB in the tested synthetic worlds. **Not permitted:** GADU is universally worse; the theorem is false; this is original-author C.13/C.14 reproduction; or the paper claims real-policy performance.

## 3. Real-data experiment — complete Criteo Attribution

**Completed and successfully reproduced** via GitHub Actions on full authentic **16,468,027 impression rows**. Full methods, code, and numeric summaries are in this public review packet:

- [Real-data scientific methods and restrictions](REAL_DATA_METHODS_AND_FINDINGS.md).
- [Python 3 stdlib executable](code/criteo_full_stream_delay_audit.py) and [zero-positive-campaign regression test](code/test_outcome_independent_selection.py): streams the full public gzip from a pinned publisher mirror revision, does not require raw-data redistribution.
- [Real-data machine-readable summary](data/criteo_full_realdata_summary.json).
- [Original successful full-dataset job and log](https://github.com/RybakovAlexeyN/gadu_ai_research_lab/actions/runs/39974114339) (may require access to the research workspace).
- [Published Criteo dataset](https://huggingface.co/datasets/criteo/criteo-attribution-dataset) — publisher's raw dataset, not rehosted here; CC BY-NC-SA 4.0. We **do not publish original impression rows, user IDs, or licensed source data**.

### A. Conditional delay calibration, 7-day observation horizon

Among linked conversion events matured by seven days, prediction of conversion by **w** using campaign-shrunk historical probabilities improves the held-out event-level Brier score over a single pooled q:

| Early window w | Pooled q Brier ↓ | Campaign q Brier ↓ | Relative reduction |
|---|---:|---:|---:|
| 1h | 0.249208 | 0.193886 | **22.2%** |
| 24h | 0.205469 | 0.184650 | **10.1%** |
| 72h | 0.122963 | 0.118222 | **3.9%** |

There are **108,004** eligible matured positive training events and **72,948** eligible matured positive test events. This is **conditional-on-event positive delay prediction**, *not conversion-probability modeling over all impressions* and not online regret.

### B. Inverse-window event-count correction on real served impressions

For **367 campaigns selected without using test conversion counts**, **2,832,326 actual held-out impressions** and **60,936 observed linked conversion-event groups within H = 7d**, use an empirical q from training and estimate event counts from the early window as N_early/q. Compare the sum of per-campaign absolute count errors divided by test impressions:

| w | Pooled q error ↓ | Campaign q error ↓ | Relative reduction |
|---|---:|---:|---:|
| 1h | 0.009225 | 0.002538 | **72.5%** |
| 24h | 0.004328 | 0.001470 | **66.0%** |
| 72h | 0.001836 | 0.000845 | **54.0%** |

**POST-HOC COHORT REPAIR:** The original 293-campaign panel selected campaigns using **test-period positive outcome counts** and could not support generalization to a prospective evaluation population. The corrected panel qualifies campaigns from **train 7-day positive count >=20** and **test exposure count >=1000**, without using held-out outcomes. Campaigns are enumerated from test impressions; a unit test verifies that a train-supported campaign with *zero held-out conversions* is retained. The real-data sample of 367 eligible campaigns happens to contain no such zeros. Because the data had been previously explored, this correction is **not a new blinded holdout**, and it remains a support-based subset. Importantly, the global q has smaller **aggregate signed bias** at 1h despite a higher sum of per-campaign absolute errors.

### Mandatory source-data limitation

The observed Criteo table contains **806,196 positive impression–event links**, **435,810 raw distinct conversion_id** and **438,730 composite (uid, conversion_id, conversion_timestamp) event groups**. **2,910 raw IDs occur across different users/timestamps**, requiring composite deduplication. The publisher's overview reportedly describes ~45,000 conversions, which does **not match these counts**. The correct publisher-level conversion unit must be reconciled **before manuscript publication claims**.

Also, impression-to-conversion time is not necessarily conversion-to-reporting delay. The conditional probability q^(7d) is **not automatically** the unconditional common-delay CDF required by the theoretical GADU reward model.

**We did not execute GADU as a randomized online policy on these Criteo logs, and have NOT measured empirical real-data regret.** Logging propensities and supported counterfactual learner actions are not in this dataset.

## 4. Quality audit and decision gate

What has actually passed:
- Locked seeds/configurations, repeatable aggregate/result accounting, synthetic event-clock tests, independent review of a 16-run specialized policy implementation.
- Complete 16.47-million-row data read on a pinned Hugging Face dataset revision, repeat full execution with matching final Brier scores and source counts.
- Quantitative negative and positive results presented with precise metrics and population restrictions.

What has **not** passed:
- An independent end-to-end **author-original** exact-policy replay; the paper's experimental supplement was not available.
- Fully matched-grid, grid-cost-controlled, multiple delay-law test of continuum GADU; 4 q<1 seeds per cell remain exploratory.
- Full-public-package raw 80-row and 16-row trajectories + identical runnable GADU policy code; the public packet contains **summaries** of those, and raw CSV from separate prior studies.
- Independent publisher-semantics signoff for Criteo conversion IDs and external review of the post-hoc corrected cohort definition.
- Real causal counterfactual GADU regret or manuscript G5/G6 acceptance.

**Team review request:** examine whether the paper's actual claim is a bound relative to a Cover upper certificate or a claim of lower **realized** Cover regret. The current data address the latter in synthetic scenarios, but they do not falsify an upper-certificate theorem. Treat the real-data observation study as exploratory model diagnostics pending the corrections above.

## 5. Reproduce the public real-data study

Python 3.10+ and ordinary network access:

~~~bash
python3 code/criteo_full_stream_delay_audit.py --output criteo_realdata_delay_v1.json
~~~

The code downloads/streams the dataset from a **pinned Hugging Face revision**; the data remain with the publisher. Outputs include the cohort splits, shrinkage model, public summary statistics and per-window results in JSON. Raw original advertising records are not redistributed.

**No manuscript, private research notes, original author TeX or unpublished team source code were copied into this public packet.** Changes are proposed in a standalone review branch, without altering the team's existing public website on main.
