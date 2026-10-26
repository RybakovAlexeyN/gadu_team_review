#!/usr/bin/env python3
"""Independent read-only D234 pilot audit; no simulation is called by this script."""
import math, json, hashlib, itertools, statistics, collections
from pathlib import Path
from fractions import Fraction
from exact_source_preflight import World,preflight,certificate
from d234_pilot import generate_cover,LOCK,DIMS,AMP,T,physical_id
ROOT=Path(__file__).resolve().parent
rows=json.loads((ROOT/'d234_raw.json').read_text())
meta=json.loads((ROOT/'d234_metadata.json').read_text())
assert hashlib.sha256((ROOT/'d234_pilot_lock.json').read_bytes()).hexdigest()==meta['lock_sha256']
assert hashlib.sha256((ROOT/'d234_pilot.py').read_bytes()).hexdigest()==meta['pilot_sha256']
assert hashlib.sha256((ROOT/'exact_source_preflight.py').read_bytes()).hexdigest()==meta['preflight_sha256']
expect={(k,s) for k in LOCK['worlds'] for s in LOCK['seeds']}
assert len(rows)==len(expect)==6
assert {(r['world'],r['seed']) for r in rows}==expect
w=World(DIMS,tuple(LOCK['C']),LOCK['L'],LOCK['q'],LOCK['w'],LOCK['gamma'])
p=preflight(T,w);assert p['entered_search']; a=p['eta_fit'];
assert a['eta']==1 and math.isclose(a['rho_search'],5/12)
for rho in (1,.5,.25,a['rho_search']):
 net,diagnostics=generate_cover(tuple(range(3)),rho)
 assert len(set(net[2].tolist()))==len(net[2])
 for d in diagnostics:
  assert d['radius_witness']<=rho+1e-10
  assert d['count']<=d['envelope']
  # E.g. d=2, rho=0.5: 4 corner-midpoint actions saturate C=1 envelope.
  # Coarse center retention is not possible for that geometry under the locked bound.
  if d['count']<d['envelope']: assert d['coarse_retained']
for i,x in enumerate(LOCK['centers']):
 # f(x)=peak-.09||x-c||^2: ||∇f|| ≤ 2*.09*sqrt(d)/2=.09sqrt(d) <=L
 assert AMP*math.sqrt(len(x))<=LOCK['L']
reports=[]
for r in rows:
 peaks=LOCK['worlds'][r['world']]['peaks'];best=max(peaks)
 net,dd=generate_cover(tuple(range(3)),a['rho_search']);f,positions,_=net
 m=a['m_search'];Ts=len(f)*m+LOCK['w'];Tsel=3*a['n_select']+LOCK['w'];Tinit=Ts+Tsel
 assert r['T']==T and r['T_search']==Ts and r['T_init']==Tinit
 assert r['base_rho']==p['union']['rho']==1 and r['base_actions']==3
 assert r['diagnostic_rho']==.5 and r['diagnostic_actions']==30
 assert r['search_actions']==113
 assert r['eta']==a['eta']
 # Derive the deterministic Search cost in exact rational arithmetic; does not use simulated source rewards.
 mu=[]
 for family,x in zip(f,positions):
  d=DIMS[int(family)];cent=LOCK['centers'][int(family)]
  pki=Fraction(str(peaks[int(family)]))
  sq=sum((Fraction(str(float(x[j])))-Fraction(str(cent[j])))**2 for j in range(d))
  raw=pki-Fraction(9,100)*sq
  mu.append(min(Fraction(1),max(Fraction(0),raw)))
 opt=Fraction(str(best))
 prediction=m*sum((opt-x for x in mu),Fraction(0)) + (opt-mu[0])
 assert abs(float(prediction)-r['regret_search'])<1e-4
 assert math.isclose(r['regret_candidate'],r['regret_search']+r['regret_compare']+r['regret_continue'],rel_tol=0,abs_tol=1e-5)
 assert math.isclose(r['delta_vs_source'],r['regret_candidate']-r['regret_source_cover'],rel_tol=0,abs_tol=1e-6)
 assert math.isclose(r['delta_vs_fixed'],r['regret_candidate']-r['regret_fixed_cover'],rel_tol=0,abs_tol=1e-6)
 assert all(val>=-1e-8 for val in (r['regret_search'],r['regret_compare'],r['regret_continue'],r['regret_source_cover'],r['regret_fixed_cover']))
 assert sum(r['source_baseline_family_pulls'])==T
 assert sum(r['fixed_baseline_family_pulls'])==T
 assert sum(r['continue_family_pulls'])==T-r['switch_round']
 assert r['T_search']<=r['switch_round']<=r['T_init'] and 0<r['switch_round']<T
 assert r['winner'] in (-1,0,1,2)
 assert r['search_exceeds_source']==(r['regret_search']>r['regret_source_cover'])
 assert r['search_exceeds_fixed']==(r['regret_search']>r['regret_fixed_cover'])
 if r['accepted']:
  assert r['winner']==0 and r['certificate_correct'] is True
  assert r['switch_round']==r['certification_round']
  assert r['economic_accept_cost']<=r['economic_D']+1e-8
  assert r['continuation_family']==[r['winner']]
 else:
  assert r['winner']==-1 and r['certification_round']==-1
  assert r['switch_round']==Tinit
  assert r['continuation_family']==[0,1,2]
  assert r['economic_accept_cost'] is None
 J=r['continuation_family'];radius=r['continuation_rho'];nc=len(generate_cover(J,radius)[0][0]);assert nc==r['continuation_actions']
 # Exact floor on the physical continuation grid.
 grid,_=generate_cover(J,radius);ids=grid[0];pts=grid[1];gaps=[]
 for family,x in zip(ids,pts):
  d=DIMS[int(family)];c=LOCK['centers'][int(family)]
  reward=min(1,max(0,peaks[int(family)]-AMP*sum((x[j]-c[j])**2 for j in range(d))))
  gaps.append(best-reward)
 floor=(T-r['switch_round'])*min(gaps)
 assert r['regret_continue']+5e-4>=floor,(r['world'],floor,r['regret_continue'])
 # Source baseline no better than best within own sampled net.
 base,_=generate_cover(tuple(range(3)),r['base_rho']);floor_base=T*min(best-(peaks[int(f)]-AMP*sum((p[j]-LOCK['centers'][int(f)][j])**2 for j in range(DIMS[int(f)]))) for f,p in zip(base[0],base[1]))
 assert r['regret_source_cover']+5e-4>=floor_base
 reports.append(dict(world=r['world'],seed=r['seed'],Search_analytic_gap=float(prediction)-r['regret_search'],
    regret_continuation_grid_floor=floor,regret_continuation_excess=r['regret_continue']-floor,
    baseline_grid_floor=floor_base,source_cover_excess=r['regret_source_cover']-floor_base,
    search_cost_exceeds_source=r['search_exceeds_source']))
summary=[]
for world in LOCK['worlds']:
 sub=[x for x in rows if x['world']==world]
 sm=lambda key:statistics.fmean(v[key] for v in sub)
 summary.append({'world':world,'n':len(sub),'candidate_regret':sm('regret_candidate'),
                 'source_cover_regret':sm('regret_source_cover'),'fixed_cover_regret':sm('regret_fixed_cover'),
                 'paired_delta_source':sm('delta_vs_source'),'paired_delta_fixed':sm('delta_vs_fixed'),
                 'mean_search':sm('regret_search'),'mean_compare':sm('regret_compare'),'mean_continue':sm('regret_continue'),
                 'certificate_count':sum(x['winner']>=0 for x in sub),'all_source_delta_positive':all(x['delta_vs_source']>0 for x in sub),
                 'baseline_rho':sub[0]['base_rho'],'baseline_action_count':sub[0]['base_actions']})
result={'audit':'PASS_INTERNAL_CROSSCHECK_NOT_AUTHOR_EQUIVALENCE','n':len(rows),'no_exclusions':True,
        'setup':'K=3; d=(2,3,4); good family=2D; q=.75; T=10m; 3 pilot worlds x 2 seeds',
        'source_baseline_adaptive_radius':1.,'source_baseline_actions':3,
        'fixed_diagnostic_radius':.5,'fixed_diagnostic_actions':30,
        'search_actions':113,'search_decisions':rows[0]['T_search'],
        'positive_candidate_minus_source_count':sum(x['delta_vs_source']>0 for x in rows),
        'search_floor_exceeds_source_count':sum(x['regret_search']>x['regret_source_cover'] for x in rows),
        'summary':summary,'per_run_oracles':reports,
        'limitations':'Author code parity BLOCKED, n=2/cell and pilot-selected functions, K=3 independently generalized, no paper-ready causal/quantitative inference'}
(ROOT/'d234_audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
print(json.dumps({k:v for k,v in result.items() if k not in ('per_run_oracles',)},indent=2,ensure_ascii=False))
