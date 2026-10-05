#!/usr/bin/env python3
"""Sanity checks for the frozen component benchmark."""

import json
import subprocess
import sys
from pathlib import Path

BENCHMARK = Path(__file__).with_name("benchmark.py")

SEEDS = 400
TARGET_RADIUS = 0.05
DELTA = 0.05
MIN_COVERAGE = 0.94

SPARSE_Q = {0.1, 0.2}
SPARSE_F = {0.05, 0.1}


def run_benchmark():
    """Execute the benchmark with the frozen evaluation settings."""
    command = [
        sys.executable,
        str(BENCHMARK),
        "synthetic",
        "--seeds",
        str(SEEDS),
        "--radius",
        str(TARGET_RADIUS),
        "--delta",
        str(DELTA),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)["regimes"]


def sparse_regimes(regimes):
    """Select the predeclared sparse-positive regimes."""
    return [
        regime
        for regime in regimes
        if regime["q"] in SPARSE_Q
        and regime["f"] in SPARSE_F
    ]


def summarize(regimes):
    """Compute the small set of evaluation statistics we gate on."""
    sparse = sparse_regimes(regimes)

    return {
        "worst_coverage_vs": min(
            regime["coverage_vs"]
            for regime in regimes
        ),
        "worst_coverage_hoeffding": min(
            regime["coverage_hoeffding"]
            for regime in regimes
        ),
        "worst_sparse_ratio": max(
            regime["mean_ratio_vs_over_hoeffding"]
            for regime in sparse
        ),
        "mean_sparse_ratio": (
            sum(
                regime["mean_ratio_vs_over_hoeffding"]
                for regime in sparse
            )
            / len(sparse)
        ),
    }


def print_summary(metrics):
    """Print stable, human-readable evaluation output."""
    print(
        f"worst_coverage_vs: "
        f"{metrics['worst_coverage_vs']:.6f}"
    )
    print(
        f"worst_coverage_hoeffding: "
        f"{metrics['worst_coverage_hoeffding']:.6f}"
    )
    print(
        f"worst_sparse_ratio: "
        f"{metrics['worst_sparse_ratio']:.6f}"
    )
    print(
        f"mean_sparse_ratio: "
        f"{metrics['mean_sparse_ratio']:.6f}"
    )


def validate(metrics):
    """Fail loudly if the frozen component test no longer passes."""
    if metrics["worst_coverage_vs"] < MIN_COVERAGE:
        raise SystemExit(
            f"VS empirical coverage fell below {MIN_COVERAGE:.2f}."
        )

    if metrics["worst_coverage_hoeffding"] < MIN_COVERAGE:
        raise SystemExit(
            f"Hoeffding reference coverage fell below {MIN_COVERAGE:.2f}."
        )

    if metrics["worst_sparse_ratio"] >= 1.0:
        raise SystemExit(
            "At least one predeclared sparse regime "
            "no longer shows a sample reduction."
        )


def main():
    regimes = run_benchmark()
    metrics = summarize(regimes)

    print_summary(metrics)
    validate(metrics)

    print(
        "PASS: component mechanism survived "
        "the predeclared test"
    )


if __name__ == "__main__":
    main()
