# Post-Call Task Pool — 29 September

This page records the concrete tasks that followed the 29 September team discussion and their current status. It is a coordination summary, not an additional scientific claim.

## 1. Make the candidate algorithm executable

**Status: closed at the current scientific-candidate level.**

The main requirement was to turn the proposed mechanism into a procedure that can actually be executed and reviewed round by round.

The current procedure is **VS-Certify-Delayed**. It now specifies:

- dyadic active cells;
- designated sampling;
- empirical-Bernstein confidence;
- synchronized checkpoints;
- a delayed flush of exactly $w$ legal filler rounds;
- finalization of matured designated feedback;
- pruning and refinement;
- family certification;
- a hard calendar cutoff returning `NOT_CERTIFIED`.

Entry points:

- [Algorithm: VS-Certify-Delayed](ALGORITHM.md)
- [Upper theorem](theory/UPPER_THEOREM.md)
- [Lower theorem](theory/LOWER_THEOREM.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)

## 2. Run a controlled experiment

**Status: component-level test completed.**

The variance-sensitive confidence mechanism was compared with the current Hoeffding route on the same Bernoulli stream.

For the predeclared sparse-positive regimes,

$$
\operatorname{mean}\!\left(
\frac{N_{\mathrm{VS}}}{N_{\mathrm H}}
\right)
=0.122852.
$$

The same grid contains regimes with

$$
\frac{N_{\mathrm{VS}}}{N_{\mathrm H}}=2,
$$

so the supported conclusion is **instance-dependent sparse-positive sample efficiency**, not uniform superiority.

[Controlled benchmark →](experiments/README.md)

## 3. Find and audit real data

**Status: dataset/model-fit task completed within the stated scope.**

Criteo Attribution is used to test delayed-positive and attribution semantics.

The key falsification result is that one physical conversion may be linked to multiple positive impression rows. Therefore the naive mapping

$$
\text{one positive impression row}
\equiv
\text{one independent Bernoulli success}
$$

is invalid on the audited slice.

This evidence is used for **model-fit / attribution falsification**, not end-to-end GADU policy evaluation.

[Criteo model-fit evidence →](data/CRITEO_MODEL_FIT.md)

## 4. Remove the undefined “wait for maturation” step

**Status: resolved for the new backend and made explicit in the executable algorithm.**

The current delayed execution rule now guarantees:

- one legal deployment every calendar round;
- unresolved silence is never encoded as zero;
- confidence updates occur at synchronized checkpoints;
- exactly $w$ legal filler deployments follow designated sampling at a checkpoint;
- the active set is frozen during the flush;
- designated and filler rounds are accounted for separately;
- pruning/splitting occurs only after designated feedback is finalized;
- a hard cutoff returns `NOT_CERTIFIED`;
- calendar delay cost is explicit.

Entry points:

- [Algorithm: VS-Certify-Delayed](ALGORITHM.md)
- [Delayed execution + GADU composition](theory/DELAYED_GADU.md)

## 5. Assemble one manuscript and run a full coauthor read

**Status: still open.**

Before calling the paper submission-ready, the following tasks remain.

### A. Independent mathematical review

Each major mathematical object should receive one verdict:

- **PASS**
- **FIX**
- **BLOCK**

The review should cover the upper theorem, lower theorem, and delayed/GADU bridge.

[Mathematical review checklist →](MATH_REVIEW.md)

### B. Novelty and claim-scope review

Confirm that:

- the closest literature does not directly subsume the stated contribution;
- manuscript wording is no stronger than the proved scope;
- unsupported claims such as “first”, “optimal”, “minimax”, or “uniformly better” do not appear.

### C. Reader-first manuscript reconstruction

The integrated manuscript still needs a single agreed hierarchy for:

- title;
- abstract;
- contribution bullets;
- related work;
- theorem-pair ordering;
- delayed integration;
- experimental story;
- limitations.

[Paper-level review →](PAPER_REVIEW.md)

### D. Full coauthor reading

After mathematical and scientific-story freeze, all coauthors should review the same integrated manuscript version rather than separate intermediate drafts.

### E. Final assembly

Once no substantive **BLOCK** remains:

- remove residual TODOs;
- check proof references and numbering;
- check figures, tables, and bibliography;
- compile and visually inspect the final PDF;
- freeze one submission version.

## Decisions for the next team call

1. Is there any mathematical **BLOCK**?
2. Is the variance-sensitive theorem pair the primary scientific story?
3. Which manuscript changes are mandatory before submission?
4. Who owns each remaining task and deadline?
