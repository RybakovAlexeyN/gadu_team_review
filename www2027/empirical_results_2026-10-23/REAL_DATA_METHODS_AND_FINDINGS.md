# Criteo Attribution — full-dataset observational delay/correction benchmark

**23 October 2026 | Status: executed and technically reproducible; NOT manuscript-accepted scientific evidence.**
**This is not a GADU online-policy regret study, not randomized off-policy evaluation, and not a reproduction of author code.**

## Source and exact execution

- Dataset: [Criteo Attribution](https://huggingface.co/datasets/criteo/criteo-attribution-dataset), Hugging Face pinned revision 904188a63cbad78bee43cd26ff5ee4ac77903986, original dataset license CC BY-NC-SA 4.0.
- [Executable, Python 3 stdlib](code/criteo_full_stream_delay_audit.py), streaming full publisher data without publishing raw ad rows.
- [Machine-readable final results](data/criteo_full_realdata_summary.json).
- [Successful full-dataset GitHub Actions execution](https://github.com/RybakovAlexeyN/gadu_ai_research_lab/actions/runs/39954486600), which may require access to the independent research repository.
- Dataset read: **16,468,027 impressions**, **806,196 positive linked rows**.
- Raw conversion IDs: **435,810**; composite distinct (uid, conversion_id, conversion_timestamp) groups: **438,730**. **2,910 raw IDs recur under different users and/or conversion timestamps**, so deduplication by conversion_id alone is incorrect.

**Unresolved publisher-semantic blocker:** the publisher overview reportedly cites about 45,000 conversions, materially fewer than these composite groups. Event definitions or release-version differences have not been reconciled. The groups are therefore not established to be unique original advertiser purchases.

Associated exposure selected per group: latest linked attributed=1 row if present, else latest row. A latest-row-only sensitivity has similar reported results. These observational exposure links are not randomized treatment assignments.

## A. Real conditional delay-calibration evaluation

Operational target is the conditional probability of impression-to-conversion delay D up to w **given a linked conversion within seven days**, NOT the unconditional probability of reporting positive feedback used in the paper. H = 7 days, w in {1h, 24h, 72h}. Historical train events fully mature before test starts and test exposures end seven days before the last available log impression. Train: **108,004** matured positive event groups; test: **72,948**.

Compare pooled historical probability with campaign-specific historical shrinkage (fixed prior weight 50). Metric = event-level held-out Brier, smaller is better. The 300-resample campaign-cluster bootstrap intervals are descriptive, not causal.

| Window | Pooled Brier | Campaign shrinkage Brier | Relative improvement |
|---|---:|---:|---:|
| 1 hour | 0.24920826 | 0.19388576 | **22.2%** |
| 24 hours | 0.20546872 | 0.18464951 | **10.1%** |
| 72 hours | 0.12296320 | 0.11822207 | **3.9%** |

These are legitimate out-of-time *conditional delay prediction* comparisons for the described selected event population, not per-impression purchase forecasting and not GADU policy regret.

## B. Inverse-window event-count reconstruction

Estimate the number of seven-day linked conversion events from the early-window observed event count divided by historical delay probability, either globally or by campaign.

**Chronology:** train impression/source times in days [0,10), test days [17,23), separated by seven days for mature follow-up. The 293 included campaigns were selected using minimum 20 training seven-day events, **minimum 20 test seven-day events**, and 1,000 test impressions. The test-event eligibility requirement is **outcome-dependent test-set selection**: no generalization to all campaigns follows from the panel.

The selected group has **2,631,942** actual test impressions and **59,926** linked seven-day event groups. Loss = sum across campaigns of absolute difference between estimated and actual seven-day event counts, divided by total test impressions. The result is an **event-count error rate**, not a causal treatment effect or bandit regret.

| Window | Pooled error | Campaign shrinkage error | Error reduction |
|---|---:|---:|---:|
| 1h | 0.00978708 | 0.00260433 | **73.4%** |
| 24h | 0.00458387 | 0.00151116 | **67.0%** |
| 72h | 0.00193299 | 0.00086717 | **55.1%** |

For one-hour observations, the *pooled* estimator has lower **signed aggregate bias** (-0.58%) than the campaign estimator (-2.48%), even though the campaign estimator wins on per-campaign absolute error. Therefore never state that campaign modeling is superior under every metric.

## Research interpretation and what is still blocked

**Supported:** The conditional timing of source-linked conversions is heterogeneous across historical campaigns. Using campaign identity predicts the short-window timing of seven-day linked conversion events better than a single pooled probability on this held-out source history. For a selected supported-campaign set, campaign-based inverse-window weighting has smaller per-campaign absolute conversion-count error.

**Not supported:** Real-data GADU online pseudo-regret, superiority to Cover-UCB on real campaigns, improved CPA/ROAS, exact calibration of the theoretical feedback-arrival process, causal policy value, prospective performance across all campaigns.

**Critical next checks:** independently resolve event IDs versus publisher conversion counts, rerun the event-count correction on campaigns selected using **training-only support**, test sensitivity to attribution choice and to the definition of event-reporting delay versus purchase occurrence. These are scientific acceptance requirements, not mere presentation work.

## Reproduction

From the current public results directory, on a network-enabled Python 3 host:

~~~bash
python3 code/criteo_full_stream_delay_audit.py --output criteo_full_realdata_output.json
~~~

The code streams the publisher data from a pinned revision and writes JSON. This public package contains no original raw ad dataset, user IDs, author manuscript TeX or private experiment code.
