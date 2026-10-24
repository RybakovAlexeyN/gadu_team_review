# 23 Oct independent reproducibility gate — FINAL HANDOFF STATUS

**Status: NUMERIC REPRODUCIBILITY PASSED; MANUSCRIPT SCIENCE APPROVAL BLOCKED.**

This is a rigorous review of independently transcribed GADU and optimized Cover-UCB code, **not** the authors' original GADU simulator. Figures must not be described as theorem proof, advertising-policy evaluation or evidence of GADU outperforming immediate Cover.

## What was checked against unmodified original files

- Manuscript source `WWW/main.tex` SHA256: `9a196140a7b600d578f69240a0a1a7638299da651728e376a46c4caa10a35b81`. Author must confirm this is the submission source.
- Original q=1 simulator `benchmark.py` SHA256: `0d2452dbaac48a43e5eadbcf613d7487a018547c822d2af1477fc304d13a687c`. Frozen original raw-80 scientific CSV SHA256: `a6b49fbaa252c3d92a64ba5f9d4fd2c39d2a904a590ab85c18709480b2638963`.
- q<1 source raw-16 CSV SHA256: `6a0273fb0784128f6854e80cd6474b466f462dbb2c0970294aea1b43591b932e`.
- Both original research ZIP manifests: all **24 q=1** listed members and all **23 q<1** listed members verified.
- 80/80 q=1 and 16/16 q<1 raw row differences and stage-regret decomposition rechecked **without importing any bandit policy**.
- Search regret calculated independently by closed-form summation of known `p_i-s_i|x-c_i|` over the frozen cyclic action schedule. **96/96 exact agreements**.
- Full telemetry: **80 trajectories ×104 checkpoints = 8,320** q=1 rows; **16×107=1,712** positive-only q<1 rows. Origin, monotone cumulative regret, difference identity and exact R(T) agreement against frozen raw endpoints passed for **all 96 trajectories**. These are reexecutions, **not endpoint interpolations**.
- **Six** selected full original-policy paths rerun (three q=1, three q<1) with exact regret, stages and switch rounds.
- q=1 source original tests **8/9** initially ran: historical `raw_96_policy_runs.json` absent from its original package. Reconstructed a **clearly labelled compatibility fixture** solely from the separately preserved old 32-row CSV. With this repair, **9/9** source tests passed. The original archive was not rewritten.
- Extra feedback tests: **8/8 q=1** and **10/10 q<1**; q<1 **4 independent source-event schedule replays** and **9/9 independent pure-Python short-horizon Cover-UCB reference cases** passed.

## Main measured results

q=1, w=1, T=3,000,000, 16 seeds per selected world:
- Strong gap Δ=.62: Cover **24,392.09** vs GADU **91,957.05**; Search alone **69,914.70** pseudo-regret at t=197,465.
- Moderate Δ=.35: Cover **24,682.17** vs GADU **65,299.41**.
- Near tie Δ=.02: Cover **26,849.22** vs GADU **36,434.57**.
- Equal peaks: Cover **4,880.86** vs GADU **13,768.75**.
- Offcenter Δ=.62: Cover **139,798.63** vs GADU **205,080.43**.
All 80 matched pairs had higher realized latent pseudo-regret for independently transcribed GADU.

q=.75 / .5, w=1, T=3m, four seeds per cell: mean GADU-Cover differences **+10,412.79** (.75 strong), **+1,772.98** (.75 near), **+243,294.01** (.5 strong), **+3,672.19** (.5 near). The q-dependent grid and testing budget differ; no causal q-only interpretation.

[Regret-over-round figures and exact functions](regret_figures_20261023/README.md). Original numeric summaries and Criteo observational diagnostics in [parent README](README.md).

## Scientific release conditions — OPEN

1. **Author-code parity**: no independently authored, end-to-end GADU reference interpreter or author-original executable was verified; Ilgham/team must confirm exact `WWW/main.tex` version, stage-2 observation clock, first strict comparison, numerical gate, and fresh continuation.
2. **Different paper experiments**: the paper's current §Experiments uses clipped-quadratic environments for delayed UCB, HOO and delayed Zooming, and *explicitly states GADU is not evaluated*. The new tent functions are a distinct exploratory protocol.
3. **Limited external validity**: only two one-dimensional equal-dimension families; pilot-informed worlds; q<1 only four seeds per cell and one binary delay law; off-center grid geometry may confound an attribution to certification.
4. **Theorem object differs**: current theorem is an *expected-regret upper bound against a computable Cover certificate*; observed realized pseudo-regret cannot falsify that theorem nor establish positive GADU performance.
5. **Real-data**: Criteo test is a delayed-event calibration diagnostic, not counterfactual real-policy GADU regret; source conversion IDs versus official description remain under audit.
6. **Public reproducer incomplete**: this PR has SVG preview curves, aggregate results and Criteo source. Original raw 80+16 paths and policy sources are in a separate tested **coauthor-only** full MVP ZIP, not yet committed as public bytes. No full-public-reproduction claim.

**Recommendation:** For an Oct 25 submission, consider a figure-plus-table **only as an explicitly negative search-cost diagnostic**, and only after the authors sign off on algorithm parity and supplementary evidence access. Otherwise do not insert these plots into the manuscript and keep existing theorem claims clearly separated from experimental evidence.
