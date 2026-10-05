#!/usr/bin/env python3
"""Controlled component benchmark for the variance-sensitive radius."""

import argparse
import json
import math

import numpy as np

MAX_CHECKPOINTS = 23
DEFAULT_SEEDS = 400
DEFAULT_RADIUS = 0.05
DEFAULT_DELTA = 0.05

Q_GRID = (0.1, 0.2, 0.5, 1.0)
F_GRID = (0.05, 0.1, 0.3, 0.7)


def stitched_eta(delta, checkpoint):
    """Allocate failure probability across geometric checkpoints."""
    return delta * 6.0 / (math.pi**2 * (checkpoint + 1) ** 2)


def hoeffding_radius_f(sample_count, q, eta):
    """Hoeffding radius on the latent f-scale."""
    return math.sqrt(math.log(2.0 / eta) / (2.0 * sample_count)) / q


def empirical_bernstein_radius(sample_var, sample_count, eta):
    """Observable empirical-Bernstein radius on the scaled g=q*f scale."""
    log_term = math.log(6.0 / eta)
    variance_term = np.sqrt(
        2.0 * sample_var * log_term / sample_count
    )
    linear_term = 7.0 * log_term / (3.0 * (sample_count - 1))
    return variance_term + linear_term


def deterministic_seed(q, f, seed_count):
    """Stable seed so every regime is reproducible."""
    q_code = int(round(q * 100000))
    f_code = int(round(f * 100000))
    return q_code * 1000 + f_code + seed_count


def vectorized_regime(f, q, target_radius_f, delta, seed_count):
    """Run one (q, f) regime over many independent Bernoulli streams."""
    p = q * f
    rng = np.random.default_rng(
        deterministic_seed(q, f, seed_count)
    )

    successes = np.zeros(seed_count, dtype=np.int64)

    done_vs = np.zeros(seed_count, dtype=bool)
    done_h = np.zeros(seed_count, dtype=bool)

    n_vs = np.zeros(seed_count, dtype=np.int64)
    n_h = np.zeros(seed_count, dtype=np.int64)

    coverage_vs = np.zeros(seed_count, dtype=bool)
    coverage_h = np.zeros(seed_count, dtype=bool)

    previous_n = 0

    for checkpoint in range(MAX_CHECKPOINTS):
        n = 2 ** (checkpoint + 1)
        increment = n - previous_n

        successes += rng.binomial(
            increment,
            p,
            size=seed_count,
        )
        previous_n = n

        eta = stitched_eta(delta, checkpoint)
        mean_g = successes / n
        sample_var = (n / (n - 1.0)) * mean_g * (1.0 - mean_g)

        radius_vs = empirical_bernstein_radius(
            sample_var,
            n,
            eta,
        )
        radius_h = hoeffding_radius_f(n, q, eta)

        newly_done_vs = (~done_vs) & (
            radius_vs <= q * target_radius_f
        )
        if newly_done_vs.any():
            n_vs[newly_done_vs] = n
            coverage_vs[newly_done_vs] = (
                np.abs(mean_g[newly_done_vs] - p)
                <= radius_vs[newly_done_vs]
            )
            done_vs[newly_done_vs] = True

        if radius_h <= target_radius_f:
            newly_done_h = ~done_h
            if newly_done_h.any():
                n_h[newly_done_h] = n
                mean_f = mean_g[newly_done_h] / q
                coverage_h[newly_done_h] = (
                    np.abs(mean_f - f) <= radius_h
                )
                done_h[newly_done_h] = True

        if done_vs.all() and done_h.all():
            break

    if not done_vs.all() or not done_h.all():
        raise RuntimeError(
            "Checkpoint cap is too small for at least one stream."
        )

    ratios = n_vs / n_h

    return {
        "f": f,
        "q": q,
        "target_radius_f": target_radius_f,
        "delta": delta,
        "seeds": seed_count,
        "mean_n_vs": float(n_vs.mean()),
        "mean_n_hoeffding": float(n_h.mean()),
        "mean_ratio_vs_over_hoeffding": float(ratios.mean()),
        "coverage_vs": float(coverage_vs.mean()),
        "coverage_hoeffding": float(coverage_h.mean()),
    }


def synthetic_suite(
    seed_count=DEFAULT_SEEDS,
    target_radius_f=DEFAULT_RADIUS,
    delta=DEFAULT_DELTA,
):
    """Run the frozen grid used in the component benchmark."""
    regimes = []

    for q in Q_GRID:
        for f in F_GRID:
            regimes.append(
                vectorized_regime(
                    f=f,
                    q=q,
                    target_radius_f=target_radius_f,
                    delta=delta,
                    seed_count=seed_count,
                )
            )

    return regimes


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the controlled confidence benchmark."
    )
    subparsers = parser.add_subparsers(
        dest="mode",
        required=True,
    )

    synthetic = subparsers.add_parser(
        "synthetic",
        help="Run the frozen synthetic grid.",
    )
    synthetic.add_argument(
        "--seeds",
        type=int,
        default=DEFAULT_SEEDS,
    )
    synthetic.add_argument(
        "--radius",
        type=float,
        default=DEFAULT_RADIUS,
    )
    synthetic.add_argument(
        "--delta",
        type=float,
        default=DEFAULT_DELTA,
    )

    return parser.parse_args()


def main():
    args = parse_args()

    payload = {
        "mode": "synthetic_component_benchmark",
        "regimes": synthetic_suite(
            seed_count=args.seeds,
            target_radius_f=args.radius,
            delta=args.delta,
        ),
    }

    print(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
