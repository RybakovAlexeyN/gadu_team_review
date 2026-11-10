"""Window–Graph UCB v0: synthetic delayed positive-only creative selection.
Research baseline, NOT a demonstrated novel method or real-world performance claim.
Usage: python window_graph_ucb_v0.py
"""
import math
from collections import defaultdict
import numpy as np


class WindowGraphUCB:
    def __init__(self, k, budget, maturity_window, q, delta=0.05, distances=None, L=None):
        if not (0 < q <= 1 and 0 < delta < 1 and budget > 0 and maturity_window >= 1):
            raise ValueError("Invalid budget/window/q/delta")
        self.k, self.budget, self.w, self.q, self.delta = k, budget, maturity_window, q, delta
        self.d = None if distances is None else np.asarray(distances, dtype=float)
        self.L = L
        if (self.d is None) != (self.L is None):
            raise ValueError("Provide both distances and L, or neither")
        if self.d is not None and (self.d.shape != (k, k) or L < 0):
            raise ValueError("Invalid graph distances/L")
        self.matured = np.zeros(k, dtype=int)
        self.positives = np.zeros(k, dtype=int)
        self.deployed = np.zeros(k, dtype=int)
        self.pending = defaultdict(list)

    def mature(self, time):
        for arm, conversion_within_window in self.pending.pop(time, []):
            self.matured[arm] += 1
            self.positives[arm] += int(conversion_within_window)

    def intervals(self):
        lo = np.zeros(self.k)
        hi = np.ones(self.k)
        for arm, n in enumerate(self.matured):
            if n:
                estimate = self.positives[arm] / (self.q * n)
                beta = math.sqrt(math.log(2 * self.k * self.budget / self.delta) / (2 * n * self.q**2))
                lo[arm] = max(0, estimate - beta)
                hi[arm] = min(1, estimate + beta)
        if self.d is not None:
            # Valid only when |p_i-p_j| <= L d(i,j) for all i,j.
            lo = np.maximum(0, np.max(lo[None, :] - self.L * self.d, axis=1))
            hi = np.minimum(1, np.min(hi[None, :] + self.L * self.d, axis=1))
        return lo, hi

    def select(self):
        _, hi = self.intervals()
        candidates = np.flatnonzero(np.isclose(hi, np.max(hi), rtol=0, atol=1e-12))
        # During feedback delay, spread deployments instead of repeatedly selecting a tied arm.
        min_deployed = np.min(self.deployed[candidates])
        return int(candidates[self.deployed[candidates] == min_deployed][0])

    def record(self, time, arm, success, delay):
        self.deployed[arm] += 1
        within_window = bool(success and delay <= self.w)
        # All deployments mature at their fixed window boundary. Early successes aren't used.
        self.pending[time + self.w].append((arm, within_window))

    def recommend(self):
        lo, _ = self.intervals()
        return int(np.argmax(lo))


def simulate(seed=0, structure=True, budget=1500, q_delay=0.4, w=4):
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 1, 6)
    rates = 0.05 + 0.16 * np.exp(-((x - 0.7) / 0.25) ** 2)
    distance = np.abs(x[:, None] - x[None, :]) if structure else None
    # L=0.5 exceeds the maximal slope of the chosen ground-truth p(x).
    q = 1 - (1 - q_delay) ** w
    policy = WindowGraphUCB(len(rates), budget, w, q, distances=distance, L=0.5 if structure else None)
    for t in range(budget):
        policy.mature(t)
        arm = policy.select()
        success = bool(rng.random() < rates[arm])
        delay = int(rng.geometric(q_delay)) if success else math.inf
        policy.record(t, arm, success, delay)
    policy.mature(budget)
    choice = policy.recommend()
    return {"seed": seed, "structure": structure, "best_rate": float(max(rates)),
            "chosen_rate": float(rates[choice]), "simple_regret": float(max(rates) - rates[choice]),
            "n_matured": int(sum(policy.matured)), "budget": budget}


if __name__ == "__main__":
    for structured in (False, True):
        rows = [simulate(seed=s, structure=structured) for s in range(20)]
        print({"variant": "Graph-Window-UCB" if structured else "Window-UCB",
               "mean_simple_regret": round(float(np.mean([r['simple_regret'] for r in rows])), 6),
               "n_runs": len(rows), "matured_0": rows[0]['n_matured']})
