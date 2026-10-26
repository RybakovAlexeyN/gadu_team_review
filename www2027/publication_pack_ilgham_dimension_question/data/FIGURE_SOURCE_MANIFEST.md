# Frozen sources and provenance

## Same-byte public copies (verified by Git blobs)
- E17 36-cell summary: `data/E17_36cell_summary.csv`, Git SHA `cca8fcbec48327e2d39a16dcdf96f5ef7d45725b`. Original frozen from `gadu_ai_research_lab` branch `agent/ilgham-e17-dimension-phase-diagram-20261025`.
- E20 18-cell summary: `data/E20_18cell_summary.csv`, Git SHA `c19ffe65b4822e216da4ba63f83f3126ccc5ab49`. Original `agent/ilgham-e20-stage2-matched-20261025`.
- E21 108-cell central feasibility: `data/E21_108case_certificate_feasibility.csv`, Git SHA `ebcf22a90d4c9a172f0049919d8217a68c2d84ce`. Original `agent/g5-e21-gadu-strict-audit-20261025`.

## New provenance-only extracted records
- E18/E19: `data/E18_E19_report_aggregates.csv`; **NOT original seed-level raw data**, explicitly extracted from independently frozen internal `RESEARCH_REPORT.md`:
  - `agent/ilgham-e18-adaptive-stage1-20261025/sprints/www2027/2026-10-25/e18_adaptive_stage1/RESEARCH_REPORT.md` (commit `0031127f7d0809306684b53b0fa4679f0cad42a1` or later source-approved content).
  - `agent/ilgham-e19-certificate-gap-20261025/sprints/www2027/2026-10-25/e19_certificate_gap/RESEARCH_REPORT.md` (commit `5ea35c7b14aef4b92c5f87f50db1113e120c0c82`).
  - E18 Stage1 allocation d=(2,3,4), strong gap q=.75: 7140.2 / 26.5 / 33.3 of 7200.
  - Total observed new-policy certificates E18 0/108 vs E19 21/108, separate landscape samples; **never present as paired improvement/causal estimate**.
  - Strong gap q=.75 new-policy certificates E18 0/18 vs E19 18/18 on different seeds/landscapes.

## What figures can support
1. Figure 1 E20: **cell-level mean** differences, E20 Stage1 matched within the two staged variants; direct Geometry-UCB comparator is bespoke, not source-tuned full-union Cover-UCB.
2. Figure 2 E17: **descriptive** observed certificate counts / 6 seeds, 36 cells; data from a selected synthetic world family, not probabilistic coverage guarantees.
3. Figure 3 E18/E19: **illustrative independent** experimental summaries, never paired causal improvement.
4. Figure 4: **conceptual schematic**, no numerical empirical assertion.

## Statistical/claim boundaries
Intervals at Figure 1, where displayed, are E20's **six-seed paired, conditional, unadjusted descriptive 95% interval**; cannot use across-landscape or post-selection inference. No unseen point-by-point cumulative curves are inferred from aggregate endpoints. Historical E03/E06 trajectories, archived in the parent PR, have a different experiment and are not mixed into this E20 plot.

The definitive author's GADU-Cover with source preflight / coarse physical cover / economic gating / fallback / fresh restart, and the updated adaptive stages, was **NOT IMPLEMENTED**. Our synthetic GADU-inspired surrogates and custom geo-UCB do not establish the author's theorem or live online causal regret improvement.
