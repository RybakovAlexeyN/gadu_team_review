# Criteo Attribution model-fit evidence

This file records the interpretation of a deterministic 1,200-row prefix of the public Criteo Attribution Modeling for Bidding dataset.

Authoritative dataset page:
https://ailab.criteo.com/criteo-attribution-modeling-bidding-dataset/

The raw dataset is **not redistributed in this review packet**.

## Slice summary

- 1,200 impression rows;
- 317 campaign IDs;
- 61 rows with a positive conversion and valid nonnegative impression-to-conversion delay;
- 55 unique `conversion_id` values among those 61 positive rows;
- maximum positive-row multiplicity for one physical conversion: 3.

## Main falsification result

The naive mapping

```text
one positive impression row = one independent Bernoulli success
```

is false on this slice.

Among the 55 unique physical conversion IDs:

- 50 appear on one positive impression row;
- 4 appear on two positive impression rows;
- 1 appears on three positive impression rows.

Therefore the same physical conversion can be linked to multiple source impressions.

## What this evidence supports

The dataset is useful for:

- delayed-positive timing diagnostics;
- impression-to-conversion delay arithmetic;
- attribution/multiplicity stress tests;
- falsifying an invalid iid row-level interpretation.

## What it does not support

This slice is not claimed to be:

- an end-to-end GADU benchmark;
- a policy comparison;
- a population estimate of `q_w`;
- evidence that the common action-independent delay assumption is correct.

The first 1,200 rows span a short chronological prefix, so this artifact can falsify the naive row-level mapping but cannot establish population-level delay-law assumptions.
