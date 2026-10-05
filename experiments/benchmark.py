#!/usr/bin/env python3
import argparse, json, math


def stitched_eta(delta, r):
    return delta * 6.0 / (math.pi ** 2 * (r + 1) ** 2)


def hoeffding_radius_f(n, q, eta):
    return math.sqrt(math.log(2.0 / eta) / (2.0 * n)) / q


def vectorized_regime(f, q, target_radius_f, delta, seed_count):
    import numpy as np
    p = q * f
    regime_seed = int(round(q * 100000)) * 1000 + int(round(f * 100000)) + seed_count
    rng = np.random.default_rng(regime_seed)
    counts = np.zeros(seed_count, dtype=np.int64)
    done_vs = np.zeros(seed_count, dtype=bool)
    done_h = np.zeros(seed_count, dtype=bool)
    n_vs = np.zeros(seed_count, dtype=np.int64)
    n_h = np.zeros(seed_count, dtype=np.int64)
    cov_vs = np.zeros(seed_count, dtype=bool)
    cov_h = np.zeros(seed_count, dtype=bool)
    n_prev = 0
    for r in range(23):
        n = 2 ** (r + 1)
        inc = n - n_prev
        counts += rng.binomial(inc, p, size=seed_count)
        n_prev = n
        eta = stitched_eta(delta, r)
        mean_g = counts / n
        var = (n / (n - 1.0)) * mean_g * (1.0 - mean_g)
        lam = math.log(6.0 / eta)
        eb = np.sqrt(2.0 * var * lam / n) + 7.0 * lam / (3.0 * (n - 1))
        h_f = hoeffding_radius_f(n, q, eta)

        hit_vs = (~done_vs) & (eb <= q * target_radius_f)
        if hit_vs.any():
            n_vs[hit_vs] = n
            cov_vs[hit_vs] = np.abs(mean_g[hit_vs] - p) <= eb[hit_vs]
            done_vs[hit_vs] = True

        if h_f <= target_radius_f:
            hit_h = ~done_h
            if hit_h.any():
                n_h[hit_h] = n
                mean_f = mean_g[hit_h] / q
                cov_h[hit_h] = np.abs(mean_f - f) <= h_f
                done_h[hit_h] = True

        if done_vs.all() and done_h.all():
            break

    if not done_vs.all() or not done_h.all():
        raise RuntimeError("checkpoint cap too small")

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
        "coverage_vs": float(cov_vs.mean()),
        "coverage_hoeffding": float(cov_h.mean()),
    }


def synthetic_suite(seed_count=400, target_radius_f=0.05, delta=0.05):
    out = []
    for q in (0.1, 0.2, 0.5, 1.0):
        for f in (0.05, 0.1, 0.3, 0.7):
            out.append(vectorized_regime(f, q, target_radius_f, delta, seed_count))
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("synthetic")
    s.add_argument("--seeds", type=int, default=400)
    s.add_argument("--radius", type=float, default=0.05)
    s.add_argument("--delta", type=float, default=0.05)
    args = ap.parse_args()
    print(json.dumps({"mode": "synthetic_component_benchmark", "regimes": synthetic_suite(args.seeds, args.radius, args.delta)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
