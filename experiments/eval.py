#!/usr/bin/env python3
import json, subprocess, sys

cmd = [sys.executable, "experiments/benchmark.py", "synthetic", "--seeds", "400", "--radius", "0.05", "--delta", "0.05"]
p = subprocess.run(cmd, capture_output=True, text=True, check=True)
regs = json.loads(p.stdout)["regimes"]
sparse = [r for r in regs if r["q"] in (0.1, 0.2) and r["f"] in (0.05, 0.1)]
worst_cov_vs = min(r["coverage_vs"] for r in regs)
worst_cov_h = min(r["coverage_hoeffding"] for r in regs)
worst_sparse_ratio = max(r["mean_ratio_vs_over_hoeffding"] for r in sparse)
mean_sparse_ratio = sum(r["mean_ratio_vs_over_hoeffding"] for r in sparse) / len(sparse)
print(f"worst_coverage_vs: {worst_cov_vs:.6f}")
print(f"worst_coverage_hoeffding: {worst_cov_h:.6f}")
print(f"worst_sparse_ratio: {worst_sparse_ratio:.6f}")
print(f"mean_sparse_ratio: {mean_sparse_ratio:.6f}")
if worst_cov_vs < 0.94:
    sys.exit("VS empirical coverage below 0.94")
if worst_cov_h < 0.94:
    sys.exit("Hoeffding reference coverage below 0.94")
if worst_sparse_ratio >= 1.0:
    sys.exit("No sample reduction in at least one predeclared sparse regime")
print("PASS: component mechanism survived the predeclared test")
