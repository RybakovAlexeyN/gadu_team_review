# GADU Team Review

Public review packet for the current GADU variance-sensitive research candidate.

This repository is intentionally small. It contains only the material needed to review the scientific result: theorem statements, proof outlines, delayed-execution logic, controlled benchmark evidence, and the real-data model-fit summary.

## What reviewers should decide

For each area, please return one of:

- **PASS**
- **WORDING / SCOPE CHANGE**
- **BLOCK**

A BLOCK should identify the exact claim, proof step, or interface that fails and, if possible, the smallest repair that would clear it.

## Main scientific candidate

1. A variance-sensitive certified Lipschitz continuum upper bound for Bernoulli observations.
2. A fine-gap lower bound with the same local Bernoulli information structure.
3. An executable delayed positive-only realization.
4. A GADU composition rule through a certified-optimizer interface.

We do **not** claim uniform superiority, a new `q^-1` law by itself, a full minimax characterization, or end-to-end real-world GADU validation.

## Suggested reading order

1. [`REVIEW_REQUEST.md`](REVIEW_REQUEST.md)
2. [`theory/UPPER_THEOREM.md`](theory/UPPER_THEOREM.md)
3. [`theory/UPPER_PROOF.md`](theory/UPPER_PROOF.md)
4. [`theory/LOWER_THEOREM.md`](theory/LOWER_THEOREM.md)
5. [`theory/LOWER_PROOF.md`](theory/LOWER_PROOF.md)
6. [`theory/DELAYED_GADU.md`](theory/DELAYED_GADU.md)
7. [`experiments/README.md`](experiments/README.md)
8. [`data/CRITEO_MODEL_FIT.md`](data/CRITEO_MODEL_FIT.md)

The main review question is simple: **is there a substantive mathematical or integration BLOCK?**
