# Ready-to-review article inserts (NOT author approved)

## Figure 1 — suggested caption

*Finite-horizon cumulative **latent pseudo-regret** for a separately implemented, source-informed family-certification policy versus original-horizon tuned immediate Cover-UCB on three pilot-informed synthetic two-family environments (T=10^7 decisions, q_w=0.75, w=1, dimensions 1 and 2). The 1D and 2D reward surfaces have clipped-quadratic means, with strong-gap peak differences 0.62 or near-tie difference 0.02. Curves are from archived per-seed trajectories, n=8,8,4, with **pointwise**, world-conditional 95% t intervals for individual-policy means (not simultaneous coverage or paired time-difference intervals). Vertical dashed lines mark the certified handover or fallback switch. E03 is a post-hoc coarse-grid-retaining cover repair, not an independently preregistered replication or original-author executable.*

## Figure 2 — suggested caption

*Mean cumulative latent pseudo-regret accumulated during Search, Compare and Continue of the independently coded GADU-inspired policy, versus the full-horizon realized pseudo-regret of immediate Cover-UCB. Source Search alone exceeds full Cover-UCB regret on every archived E03 seed pair; at this selected T and these functions a subsequent zero-regret continuation could not reverse the observed result. This diagnostic does not identify general future crossover horizons or refute regret upper certificates.*

## Figure 3 — suggested caption

*Two clipped-quadratic reward families on [0,1] and [0,1]^2, respectively. Family 1 peaks at x=0.5, while Family 2 peaks at (0.25,0.75). The illustration shows representative p1=0.8,0.18 and p2=0.8; all three actual world parameters, including p2=0.78 near-tie, are reported in the experiment setup and data files.*

## Methods — author-review wording

We considered a stylized Web-decision motivation with two continuum model families of dimensions d=(1,2). The latent Bernoulli rewards are functions f1(x)=clip(p1−0.10(x−0.5)^2,0,1) and f2(x,y)=clip(p2−0.09[(x−0.25)^2+(y−0.75)^2],0,1). Three selected settings take (p1,p2) equal to (.80,.18), (.18,.80), and (.80,.78). Successful outcomes have conditional delay D=1 with probability q_w=.75 or D=4 otherwise, with attribution window w=1; failures remain silent. A source-normalized window estimator is used only after observations mature. T=10^7 rounds; L=.3; gamma=1. We use an independently written, manuscript-informed three-stage certification policy and compare it to immediate Bernstein Cover-UCB, each making one decision per round; exploration durations and grids are allowed to differ as specified by their respective algorithms. The post-hoc E03 cover correction preserves the relevant coarse-grid action points but is not an all-radii nested cover hierarchy. Paired seeds of sizes 8,8,4 are used within each fixed environment. The primary outcome is cumulative latent pseudo-regret at T, not realized event count or theoretical certificate width.

## Results — CONDITIONAL; author must approve policy parity

In all 16 strong-gap runs the independent procedure selected the optimal family, whereas no certificate was issued in the four near-tie runs. For every one of the 20 paired seed experiments, the policy incurred higher final pseudo-regret than immediate Cover-UCB. The mean paired increases were 636,146.55, 113,868.06 and 44,911.80 for best-1D, best-2D and near-tie worlds, respectively (see summary table for conditional paired t intervals). Search accounts for 97.8%, 91.1% and 77.4% of mean final policy regret. In all 20 runs, cumulative regret accrued during Search alone exceeded the comparator's entire final pseudo-regret. This is a finite-horizon certification-cost diagnostic, not evidence of universal algorithm ranking or evaluation of online performance with real advertisements. An economic-rejection branch is unreachable for this frozen protocol given a strict statistical separation, so branch-complete effectiveness is not established.

## Questions for Ilgham and coauthors

1. Is the inspected WWW/main.tex file SHA256 9a196140a7b600d578f69240a0a1a7638299da651728e376a46c4caa10a35b81 the actual final submission source?
2. Is event arrival/maturity and the one-shot economic rejection/acceptance rule transcribed correctly, and is the fresh continuation after Compare correct?
3. Is the paper's original baseline-only experiment (which says GADU not evaluated) still separate, and should E03 be held for supplement/future work?
4. Which claim may go into the main paper without implying author-code parity, broad generalization, or empirical theorem proof?
5. How should reproducibility material be served under WWW double-blind constraints? The present public GitHub page is identifiable.
