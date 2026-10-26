# Scientific limitations and what is NOT demonstrated

1. **P0 algorithm parity unresolved.** The actual current authors' GADU-Cover for K=3 with its new Stage 1/2 was not tested. E17–E20 execute independent *surrogates*. Preflight, physical coarse covers, family certificates, economic acceptance/fallback and clean-restart semantics differ.
2. **Comparator mismatch.** Direct geometry-aware UCB is bespoke and not the authors' source-tuned immediate Cover-UCB. E06 did compare against tuned Cover, but its radius-1 net had only one arm per family, so the claimed over-exploration mechanism was absent.
3. **Search/retirement benefit ≠ end-to-end advantage.** Matched staged controls permit isolating *family restriction after the same Stage1*; full advantage requires amortizing *all* Stage1 expenditure against an equally strong competitor. E20 did not establish this.
4. **Confounding by geometry.** E09's positive example arose from different spatial grids, not demonstrated elimination efficiency.
5. **Statistical scope.** All figures summarize a finite group of selected synthetic landscapes. Intervals are descriptive conditional paired six-seed CIs; no across-world conclusion, familywise multiple-test correction or unbiased publication selection claimed.
6. **Certification feasibility.** E21 center-only margin can be intrinsically negative in near-tie conditions and positive but unaffordable in medium-gap fixed budgets. This is **not** a fundamental impossibility for full-cover GADU.
7. **Index-bias and implementation issues.** Best family held index 0 in many studies, wrong certificates could cause assertions rather than being logged, and bespoke UCB initialization differs from standard optimistic untried-arm policies. Follow-up must randomize labels and record every error.
8. **Real-data/online scope.** None of these figures establishes causal real advertising-regret improvement; iPinYou/Criteo are separate observational source audits. Do not describe this pack as real-data GADU performance.

**Release gate before paper:** Ilgham reviews the algorithm mapping + comparator + figure captions; an independent source-to-action verification and fresh preregistered seed/world holdout must precede publication-level superiority claims.
