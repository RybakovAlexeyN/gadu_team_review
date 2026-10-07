# Controlled Component Benchmark

This benchmark compares two confidence mechanisms on the **same Bernoulli stream**:

- inverse-weighted Hoeffding confidence on latent $f$;
- variance-sensitive empirical-Bernstein confidence on the scaled Bernoulli mean $qf$.

It is a **component test**, not an end-to-end GADU policy experiment and not regret evidence.

## Frozen setup

- $q\in\{0.1,0.2,0.5,1.0\}$;
- $f\in\{0.05,0.1,0.3,0.7\}$;
- 400 simulated streams per regime;
- target latent radius $0.05$;
- confidence parameter $0.05$;
- geometric sample checkpoints.

## Sparse-positive regimes

The predeclared sparse regimes are

$$
q\in\{0.1,0.2\},
\qquad
f\in\{0.05,0.1\}.
$$

| $q$ | $f$ | mean $N_{\mathrm{VS}}$ | mean $N_{\mathrm H}$ | $N_{\mathrm{VS}}/N_{\mathrm H}$ |
|---:|---:|---:|---:|---:|
| 0.1 | 0.05 | 16,384.00 | 262,144.00 | 0.062500 |
| 0.1 | 0.10 | 28,794.88 | 262,144.00 | 0.109844 |
| 0.2 | 0.05 | 8,192.00 | 65,536.00 | 0.125000 |
| 0.2 | 0.10 | 12,718.08 | 65,536.00 | 0.194063 |

The mean sparse-regime ratio is

$$
\operatorname{mean}\!\left(\frac{N_{\mathrm{VS}}}{N_{\mathrm H}}\right) =
0.122852.
$$

Observed interval coverage on this simulation grid was $1.000$ for both methods. This is computational sanity evidence, **not a coverage proof**.

## Counterexamples to uniform dominance

The same frozen grid contains regimes where the variance-sensitive implementation is more expensive:

| $q$ | $f$ | mean $N_{\mathrm{VS}}$ | mean $N_{\mathrm H}$ | $N_{\mathrm{VS}}/N_{\mathrm H}$ |
|---:|---:|---:|---:|---:|
| 0.5 | 0.70 | 16,384.00 | 8,192.00 | 2.000000 |
| 1.0 | 0.30 | 4,096.00 | 2,048.00 | 2.000000 |
| 1.0 | 0.70 | 4,096.00 | 2,048.00 | 2.000000 |

Therefore the supported interpretation is:

> **instance-dependent sparse-positive sample efficiency**, not uniform superiority.

## Reproduce

```bash
python3 experiments/benchmark.py synthetic --seeds 400 --radius 0.05 --delta 0.05
python3 experiments/eval.py
```

`numpy` is required for the vectorized benchmark.