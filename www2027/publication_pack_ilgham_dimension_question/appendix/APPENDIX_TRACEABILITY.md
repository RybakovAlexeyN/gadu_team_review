# Figure-to-evidence traceability

| Asset | Underlying source | Displayed quantity | Interpretation |
|---|---|---|---|
| Figure 1 | `data/E20_18cell_summary.csv` row hetero_234/strong/.75 | 4,151.5864 vs 1,605.7827 vs 1,205.8336; 6/6 certs; six-seed paired interval | Full regret of three *different* policies, and retirement ablation |
| Figure 2 | `data/E17_36cell_summary.csv`, all 36 rows | Correct certs `certificates` / 6 per cell (totals strong-q.75=36/36; strong-q.35=9/36; others=0/144) | Selected-world observed certification frequency |
| Figure 3 | `data/E18_E19_report_aggregates.csv` | E18 7,140.2/26.5/33.3 average Stage1 pulls, 0/108 certs; E19 21/108 certs | Independent experiments, not a paired causal effect |
| Figure 4 | Conceptual diagram + Figure 1 exact numbers | Supported mechanism and not-yet-tested author-algorithm boundary | Schematic, not another experiment |
| Table 1 | `data/E20_18cell_summary.csv` | Three source-identical mean values, read-only normalized | Same as Figure 1 |

## Source-chain

Original archived E17/E20/E21 CSV bytes copied identically to this GitHub review branch; verify hashes with `git hash-object`:
- `E17_36cell_summary.csv` -> `cca8fcbec48327e2d39a16dcdf96f5ef7d45725b`
- `E20_18cell_summary.csv` -> `c19ffe65b4822e216da4ba63f83f3126ccc5ab49`
- `E21_108case_certificate_feasibility.csv` -> `ebcf22a90d4c9a172f0049919d8217a68c2d84ce`

The E18/E19 summary is a manually extracted, labeled provenance artifact from frozen internal reports, not the original per-seed data. Figure 3 does NOT test end-to-end author-GADU stages.

**Reproduction:** GitHub Actions validates all numeric inputs against the copied frozen sources, then exports **PNG and PDF** from exactly the committed SVG figure artwork. PDF/PNG are workflow artifacts, while the SVG source files are tracked in Git.
