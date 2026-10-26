# Table 1. Primary descriptive comparison

E20 strong-gap setting with optimal `d=2` family among weaker `d=3,4`, `q=F(w)=0.75`, `T=20,000`. Six matched simulator seeds; mean latent cumulative pseudo-regret (lower is better).

| Policy | Mean pseudo-regret | Comparison |
|---|---:|---|
| Same mandatory Stage 1 → geometric Stage 2, **no** family retirement | 4,151.6 | Matched two-stage control |
| Same mandatory Stage 1 → **retire** certified inferior families → geometric Stage 2 | **1,605.8** | −2,545.8 (−61.3%) vs control |
| Direct bespoke geometry-aware UCB from round one | **1,205.8** | Staged with retirement is +399.95 worse |

**Analysis:** The retirement benefit is identified *relative to the same-initialization staged control*. This does **not** imply superiority to direct geometry UCB, and the latter is **not** a source-exact immediate Cover-UCB implementation. In this selected cell 6/6 certificates chose the correct best family. Mean Stage1 regret was 583.72 across 1,430.83 rounds. For staged-with-retirement minus direct geo-UCB, conditional six-seed descriptive paired 95% CI = **[250.18, 549.72]**; no correction for multiple tested cells, no across-landscape CI. End-point means do not supply full regret trajectories.

Raw numerical input is [E20 frozen CSV](../data/E20_18cell_summary.csv) row `hetero_234,strong,0.75`, also extracted as machine-readable [Table 1 CSV](table1_main_numbers.csv).
