#!/usr/bin/env python3
"""E03 scientific red-team: preregistered-data diagnostics only, no policy reruns.

All calculations are scoped to frozen E03 CSV and source-formula transcription.
Does not establish original-author implementation parity or theorem validity.
"""
import csv, json, math, hashlib
from pathlib import Path
from collections import Counter
from exact_source_preflight import World, preflight, certificate

HERE=Path(__file__).resolve().parent
CSV=HERE.parent/'data'/'e03_seed_runs.csv'
# Also work in the original unzipped user archive which stores CSV at root.
if not CSV.exists(): CSV=HERE/'nested_raw.csv'
with CSV.open(newline='') as fh: rows=list(csv.DictReader(fh))
assert len(rows)==20
T=10_000_000
world=World((1,2),(1.,1.),.3,.75,1,1.)
pf=preflight(T,world)
assert pf['eta_fit']['eta']==.5
assert float(rows[0]['rho_search'])==pf['eta_fit']['rho_search']
Ts=23*pf['eta_fit']['m_search']+1
Ti=Ts+2*pf['eta_fit']['n_select']+1
assert (Ts,Ti)==(1_111_821,1_160_162)
D=Ti+certificate(T-Ti,world,(0,1),fixed_radius=pf['union']['rho'])['B']
assert abs(D-float(rows[0]['D_T_actual']))<1e-6

# Critical falsification: compare is economically guaranteed to accept any
# strict separation in *every* feasible comparison round of this E03 setup.
# This claim is from 48,341 actual integer decision times, not two endpoints.
margins={str(k):[float('inf'),-float('inf')] for k in (0,1)}
for t in range(Ts+1,Ti+1):
    for k in (0,1):
        margin=D-(t+certificate(T-t,world,(k,))['B'])
        margins[str(k)][0]=min(margins[str(k)][0],margin)
        margins[str(k)][1]=max(margins[str(k)][1],margin)
assert all(lo>0 for lo,hi in margins.values())

summary={}
for name in sorted({r['world'] for r in rows}):
    grp=[r for r in rows if r['world']==name]
    floor=[float(r['regret_search'])-float(r['cover_regret']) for r in grp]
    assert all(v>0 for v in floor),name
    total=[float(r['gadu_regret'])-float(r['cover_regret']) for r in grp]
    search=sum(float(r['regret_search']) for r in grp)/len(grp)
    cover=sum(float(r['cover_regret']) for r in grp)/len(grp)
    summary[name]={
        'n':len(grp), 'observed_search_floor_beats_full_cover_n':sum(v>0 for v in floor),
        'mean_search':search,'mean_cover':cover,'search_to_cover_ratio':search/cover,
        'minimum_search_minus_full_cover':min(floor),
        'all_gadu_worse':all(v>0 for v in total),
        'decision_paths':dict(Counter(f"accepted={r['accepted']};winner={r['selected_family']}" for r in grp))}
# Scoped not fully nested: inspect concrete E03 code-set coordinates independently.
# 1D singleton rho=.25 contains .25 and .75; 1D search rho=5/24 does not.
# 2D singleton rho=.25 contains (1/6, 1/6); search rho=5/24 uses
# 4x4 uniform centers and coarse 2x2 only, so does not contain 1/6.
report={
 'study':'E03 independent author-text-informed implementation (post-hoc grid repair)',
 'frozen_csv_sha256':hashlib.sha256(CSV.read_bytes()).hexdigest(),
 'all_rows':len(rows),'author_policy_parity':'BLOCKED',
 'search_floor':summary,
 'economic_gate':{'integer_comparison_rounds_enumerated':Ti-Ts,
                  'valid_times_inclusive':[Ts+1,Ti],
                  'certificate_acceptance_margin_min_max_by_family':margins,
                  'always_accepts_if_strict_separation':True},
 'branch_coverage':{'economic_reject_branch':0,'accepted_1d':8,'accepted_2d':8,'no_separation':4},
 'geometry':{'coarse_grid_retained_in_exercised_transitions':True,
             'fully_nested_all_radius_levels':False,
             'label':'E03 coarse-grid-retaining post-hoc cover correction; not a fully hierarchical nested chain'},
 'interpretation':'In all 20 archived seeds, Search regret alone exceeds observed full-horizon immediate Cover regret. For this fixed source-formula instantiation, economic rejection is unreachable following strict separation during Compare. These facts reduce the informativeness of the current negative comparison; they neither prove universal GADU inferiority nor validate author parity.'}
print(json.dumps(report,indent=2,ensure_ascii=False))
