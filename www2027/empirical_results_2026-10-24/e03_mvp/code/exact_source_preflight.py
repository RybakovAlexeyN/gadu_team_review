#!/usr/bin/env python3
"""Source-formula faithful finite-T numeric feasibility for WWW/main.tex (ZIP2, 22-Oct-2026).

Outputs necessary/source-prescribed non-random admission into GADU Search.
This is NOT a validation of the expected-regret proof or of numeric acceptance after data.
Specific source equations: gadu-cover-phi, gadu-cover-certificate, gadu-main-explicit-samples,
gadu-main-resolution, gadu-main-explicit-durations, three-stage-deferred.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

KAPPA=3904/3
@dataclass(frozen=True)
class World:
    dims: tuple[int,...] = (1,1)
    covers: tuple[float,...] = (1.0,1.0)
    L:float=.1
    q:float=1.
    w:int=1
    gamma:float=1.
    def __post_init__(self):
        if not (len(self.dims)==len(self.covers)>=2 and all(isinstance(d,int) and d>=0 for d in self.dims) and all(c>=1 for c in self.covers) and self.L>0 and 0<self.q<=1 and self.w>=0 and 0<self.gamma<=1):
            raise ValueError("Invalid World")
    @property
    def K(self):return len(self.dims)


def cover_envelope(w:World, J:tuple[int,...], rho:float)->int:
    return sum(math.ceil(w.covers[i]*rho**(-w.dims[i])) for i in J)


def phi(u:int, rho:float, M:int, w:World)->tuple[float,float]:
    if u<2: raise ValueError("Phi applies to u>=2")
    a=KAPPA*M*math.log(2*u)/w.q
    alpha=min(1.0,math.sqrt(a/u))
    raw=w.L*u*rho + u*alpha + a/alpha + (w.w+7)*M
    return raw,alpha


def certificate(u:int,w:World,J:tuple[int,...], fixed_radius:float|None=None)->dict:
    if u in (0,1):return {"B":float(u),"rho":fixed_radius if fixed_radius is not None else 1.,"M":0 if u==0 else cover_envelope(w,J,1.),"alpha":None,"unclipped":float(u)}
    if u<0:raise ValueError('u>=0')
    if fixed_radius is None:
        stop=math.ceil(math.log2(max(2,w.L*u)))
        radii=(2.0**(-j) for j in range(stop+1))
    else:radii=(fixed_radius,)
    best=None
    for rho in radii:
        M=cover_envelope(w,J,rho)
        raw,alpha=phi(u,rho,M,w)
        # Tie-break larger radius first as earlier enumeration, and retain before clipping.
        if best is None or raw<best['unclipped']-1e-9:
            best={'B':min(float(u),raw),'rho':rho,'M':M,'alpha':alpha,'unclipped':raw}
    return best


def target_budget(T:int,w:World,j:int)->dict:
    eta=2.0**(-j)
    rho=min(1.,eta/(8*w.L))
    M=cover_envelope(w,tuple(range(w.K)),rho)
    ll=math.log(4*M*T**3)
    # Explicit source formula includes integer CEIL for *per-action* m and per-family n.
    m=math.ceil(128*ll/(w.q*w.q*eta*eta))
    n=math.ceil(64*ll/(w.q*w.q*eta*eta))
    tb=M*m+w.K*n+2*w.w
    return {'j':j,'eta':eta,'rho_search':rho,'Mbar':M,'Lambda':ll,'m_search':m,'n_select':n,'T_test_bound':tb}


def preflight(T:int,w:World,max_j:int=64)->dict:
    if T<2:raise ValueError('T>=2')
    if T>2**51:raise ValueError('T too large for robust floats')
    union=certificate(T,w,tuple(range(w.K)))
    singletons=[certificate(T,w,(i,)) for i in range(w.K)]
    cap=math.floor(min(min(s['B'] for s in singletons),w.gamma*union['B']))
    candidate=None
    excluded=[]
    for j in range(max_j+1):
        b=target_budget(T,w,j)
        if b['T_test_bound']<=cap:candidate=b
        else:
            excluded.append({'first_nonfitting_j':j,'eta':b['eta'],'cost':b['T_test_bound']});break
    result={'T':T,'K':w.K,'dims':list(w.dims),'covers':list(w.covers),'L':w.L,'q_w':w.q,'w':w.w,'gamma':w.gamma,'union':union,'singletons':singletons,'T_cap':cap,
            'eta_fit':candidate,'first_nonfit':excluded[0] if excluded else None,
            'entered_search':bool(candidate)}
    if candidate:
        # Conservative evaluated size equals envelope; for real implementation use exact net counts.
        Ts=candidate['Mbar']*candidate['m_search']+w.w
        Tsel=w.K*candidate['n_select']+w.w
        Tinit=Ts+Tsel
        assert Tinit==candidate['T_test_bound']<=cap<=T
        remaining=T-Tinit
        Bprefix=certificate(remaining,w,tuple(range(w.K)),fixed_radius=union['rho'])
        Dt=Tinit+Bprefix['B']
        passed=Dt <=(1+w.gamma)*union['B']+1e-8
        assert passed, "Source claim automatic preflight for eta fit was contradicted"
        result.update({'T_search_conservative':Ts,'T_select':Tsel,'T_init':Tinit,'D_T':Dt,'D_T_over_T':Dt/T,'B_union_over_T':union['B']/T,'preflight_gate':passed})
    return result


def minimum_horizon(w:World,predicate,hi_limit:int=10**13)->tuple[int|None,dict|None]:
    lo,hi=2,2
    while hi<hi_limit and not predicate(preflight(hi,w)):
        hi=min(hi*2,hi_limit)
    if not predicate(preflight(hi,w)):
        return None,None
    while lo<hi:
        mid=(lo+hi)//2
        if predicate(preflight(mid,w)):hi=mid
        else:lo=mid+1
    # Caveat: for scaled finite grids a discrete radius menu can change non-monotonically;
    # binary search is provisional, needs local boundary and increasing grid validation.
    r=preflight(lo,w)
    return lo,r

if __name__=='__main__':
    import argparse,json
    p=argparse.ArgumentParser();p.add_argument('--T',type=int,default=100000);p.add_argument('--K',type=int,default=2);p.add_argument('--d',type=int,default=1);p.add_argument('--C',type=float,default=1.);p.add_argument('--L',type=float,default=.1);p.add_argument('--q',type=float,default=1.);p.add_argument('--w',type=int,default=1);p.add_argument('--gamma',type=float,default=1.);p.add_argument('--thresholds',action='store_true');args=p.parse_args();world=World((args.d,)*args.K,(args.C,)*args.K,args.L,args.q,args.w,args.gamma)
    if args.thresholds:
        for k,pred in [('eta1',lambda r:r['entered_search']),('eta_lt1',lambda r:r['entered_search'] and r['eta_fit']['eta']<1)]:
            t,result=minimum_horizon(world,pred)
            print(json.dumps({'condition':k,'minimum_provisional_T':t,'detail':result},indent=2))
    else:print(json.dumps(preflight(args.T,world),indent=2))
