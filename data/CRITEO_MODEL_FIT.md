# Criteo Attribution — Model-Fit Evidence

This note records the interpretation of a deterministic 1,200-row prefix of the public Criteo Attribution Modeling for Bidding dataset.

Authoritative dataset page: <https://ailab.criteo.com/criteo-attribution-modeling-bidding-dataset/>

The raw dataset is **not redistributed** in this review packet.

## Observed facts

| Quantity | Observed value |
|---|---:|
| Impression rows | 1,200 |
| Campaign IDs | 317 |
| Positive rows with valid nonnegative impression-to-conversion delay | 61 |
| Unique physical `conversion_id` values among those positive rows | 55 |
| Maximum positive-row multiplicity for one physical conversion | 3 |

Among the 55 unique physical conversion IDs:

- 50 appear on one positive impression row;
- 4 appear on two positive impression rows;
- 1 appears on three positive impression rows.

## Falsified interpretation

The naive mapping

$$
\text{one positive impression row}
\equiv
\text{one independent Bernoulli success}
$$

is false on this slice.

A single physical conversion may be linked to multiple source impressions, so row-level positive indicators cannot automatically be treated as independent Bernoulli successes from distinct physical conversions.

## What this evidence supports

This slice is useful for:

- delayed-positive timing diagnostics;
- impression-to-conversion delay arithmetic;
- attribution and multiplicity stress tests;
- falsifying an invalid iid row-level interpretation.

## What it does **not** support

This slice is not claimed to be:

- an end-to-end GADU benchmark;
- a policy comparison;
- a population estimate of $q_w$;
- evidence that the common action-independent delay assumption is correct.

The first 1,200 rows form a short chronological prefix. This artifact can therefore falsify the naive row-level mapping, but cannot establish population-level delay-law assumptions.