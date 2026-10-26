#!/usr/bin/env python3
"""POST-HOC SYNTHETIC 1D/2D GADU benchmark (not authors' original implementation).

Uses source formulas for default tuning and Bernstein UCB, new independently
implemented heterogeneous deterministic midpoint covers and stable CRN IDs.
Protocol frozen externally in protocol_lock.json BEFORE held-out outcomes.
"""
from __future__ import annotations
import math,os,json,csv,hashlib,platform,argparse
from pathlib import Path
import numpy as np
from numba import njit
from exact_source_preflight import World,preflight,certificate,cover_envelope

ROOT=Path(__file__).resolve().parent
CONFIG=json.loads((ROOT/'protocol_lock.json').read_text()); NEST=json.loads((ROOT/'lock_nested_ablation.json').read_text())
CONFIG['primary_eval_seeds']=NEST['seeds_primary'];CONFIG['secondary_eval_seeds']=NEST['seeds_secondary']
T=CONFIG['T'];Q=CONFIG['q_w'];W=CONFIG['w'];L=CONFIG['L'];DIMS=CONFIG['dims']


def make_cover(families,rho):
    """Nested Euclidean rho-covers. Direct action identities are coordinate-stable."""
    fam=[];xs=[];ys=[];aids=[]
    for i in families:
        d=DIMS[i]
        if d==1:
            if math.isclose(rho,.5,rel_tol=0,abs_tol=1e-8): pts=[(.5,0.)]
            elif math.isclose(rho,.25,rel_tol=0,abs_tol=1e-8): pts=[(.25,0.),(.5,0.),(.75,0.)]
            elif math.isclose(rho,5./24.,rel_tol=0,abs_tol=1e-8): pts=[(1./6.,0.),(.5,0.),(5./6.,0.)]
            else: raise ValueError(f'unlocked 1D cover radius {rho}')
        else:
            if math.isclose(rho,.5,rel_tol=0,abs_tol=1e-8):
                pts=[(x,y) for x in (.25,.75) for y in (.25,.75)]
            elif math.isclose(rho,.25,rel_tol=0,abs_tol=1e-8):
                pts=[(x,y) for x in (1./6.,.5,5./6.) for y in (1./6.,.5,5./6.)]
                pts += [(x,y) for x in (.25,.75) for y in (.25,.75)]
            elif math.isclose(rho,5./24.,rel_tol=0,abs_tol=1e-8):
                pts=[(x,y) for x in (.125,.375,.625,.875) for y in (.125,.375,.625,.875)]
                pts += [(x,y) for x in (.25,.75) for y in (.25,.75)]
            else: raise ValueError(f'unlocked 2D cover radius {rho}')
        # Independent conservative cover witnesses: dense 51x51 grid.
        for x in np.linspace(0.,1.,51):
            for y in (np.linspace(0.,1.,51) if d==2 else [0.]):
                if min(math.hypot(x-px,y-py) for px,py in pts)>rho+1e-9:
                    raise AssertionError(f'not a {rho} cover of family {i}')
        if len(pts)>math.ceil(rho**(-d)):
            raise AssertionError(f'{len(pts)} actions exceed C*rho^-d envelope')
        for x,y in pts:
            fam.append(i);xs.append(x);ys.append(y)
            xid=round(x*1_000_000);yid=round(y*1_000_000)
            aids.append(int(i)*1_000_000_000_000+xid*1_000_000+yid)
    assert len(set(aids))==len(aids)
    return (np.asarray(fam,dtype=np.int64),np.asarray(xs,np.float64),
            np.asarray(ys,np.float64),np.asarray(aids,np.int64))

@njit
def u(seed,t,arm,channel):
    z=(np.uint64(seed)^np.uint64(t)*np.uint64(0x9E3779B97F4A7C15)
        ^np.uint64(arm+1)*np.uint64(0xBF58476D1CE4E5B9)
        ^np.uint64(channel+1)*np.uint64(0x94D049BB133111EB))
    z=(z^(z>>np.uint64(30)))*np.uint64(0xBF58476D1CE4E5B9)
    z=(z^(z>>np.uint64(27)))*np.uint64(0x94D049BB133111EB)
    z=z^(z>>np.uint64(31))
    return float(z>>np.uint64(11))/9007199254740992.

@njit
def reward(fam,x,y,peaks):
    if fam==0:
        raw=peaks[0]-.10*(x-.5)*(x-.5)
    else:
        raw=peaks[1]-.09*((x-.25)*(x-.25)+(y-.75)*(y-.75))
    return min(1.,max(0.,raw))

@njit
def source_y(seed,t,arm,mu,q):
    z=u(seed,t,arm,0)<mu
    if not z:return 0.
    return 1./q if u(seed,t,arm,1)<q else 0.

@njit
def cover_policy(seed,start,horizon,fam,x,y,ids,peaks,q,spacing):
    n=len(fam);counts=np.zeros(n,np.int64);sums=np.zeros(n,np.float64)
    prev=-1;prev_y=0.;regret=0.;pulls=np.zeros(2,np.int64)
    nr=0;N=horizon//spacing+2;trace=np.full(N,np.nan,np.float64)
    trace[nr]=0.;nr+=1
    optimal=max(peaks)
    for j in range(1,horizon+1):
        if prev>=0:
            counts[prev]+=1;sums[prev]+=prev_y
        lg=math.log(max(2,j));chosen=0;best=-1e99
        for a in range(n):
            m=counts[a]
            if m<2:score=float('inf')
            else:
                avg=sums[a]/m
                var=max(0.,avg/q-avg*avg)
                score=avg+math.sqrt(16.*var*lg/m)+56.*lg/(3*q*m)
            if score>best:best=score;chosen=a
        k=fam[chosen];m=reward(k,x[chosen],y[chosen],peaks)
        prev=chosen;prev_y=source_y(seed,start+j,ids[chosen],m,q)
        regret+=optimal-m;pulls[k]+=1
        if j%spacing==0:
            trace[nr]=regret;nr+=1
    if horizon%spacing:trace[nr]=regret;nr+=1
    return regret,pulls,trace[:nr]

@njit
def search_phase(seed,fam,x,y,ids,peaks,m,q,w):
    M=len(fam);tmax=M*m+w
    counts=np.zeros(M,np.int64);sums=np.zeros(M,np.float64)
    prev=-1;prev_y=0.;regret=0.;optimal=max(peaks)
    for t in range(1,tmax+1):
        if prev>=0:
            counts[prev]+=1;sums[prev]+=prev_y
        a=(t-1)%M;v=reward(fam[a],x[a],y[a],peaks)
        prev=a;prev_y=source_y(seed,t,ids[a],v,q)
        regret+=optimal-v
    reps=np.zeros(2,np.int64)
    for family in range(2):
        best=-1e10;a_star=-1
        for j in range(M):
            if fam[j]!=family:continue
            val=sums[j]/counts[j]
            if val>best:best=val;a_star=j
        reps[family]=a_star
    return reps,counts,sums,prev,prev_y,regret

@njit
def select_phase(seed,t0,tstop,reps,counts,sums,prev,prev_y,
                 fam,x,y,ids,peaks,q,lam,epsilon):
    regret=0.;optimal=max(peaks)
    winner=-1;separation=-1
    for j in range(1,tstop+1):
        t=t0+j
        if prev>=0:
            counts[prev]+=1;sums[prev]+=prev_y
        a=reps[(j-1)%2];v=reward(fam[a],x[a],y[a],peaks)
        prev=a;prev_y=source_y(seed,t,ids[a],v,q)
        regret+=optimal-v
        bounds_lo=np.zeros(2,np.float64);bounds_hi=np.zeros(2,np.float64)
        for family in range(2):
            a_rep=reps[family];na=counts[a_rep]
            rad=math.sqrt(lam/(2*na))/q;mu=sums[a_rep]/na
            bounds_lo[family]=mu-rad
            bounds_hi[family]=min(1.,mu+rad+epsilon)
        if bounds_lo[0]>bounds_hi[1]:winner=0;separation=t;break
        if bounds_lo[1]>bounds_hi[0]:winner=1;separation=t;break
    return winner,separation,regret

@njit
def remaining_select_pseudoregret(from_t,to_t,search_end,reps,fam,x,y,peaks):
    r=0.;optimal=max(peaks)
    for t in range(from_t+1,to_t+1):
        a=reps[(t-search_end-1)%2]
        r+=optimal-reward(fam[a],x[a],y[a],peaks)
    return r


def run_cell(world_name,seed):
    peaks=np.array(CONFIG['world_parameters'][world_name]['peaks'],dtype=np.float64)
    world=World((1,2),(1.,1.),L,Q,W,1.)
    pf=preflight(T,world)
    assert pf['entered_search'] and pf['eta_fit']['eta']==.5
    # The conservative upper-size envelope is used ONLY to select eta,
    # actual M is required for the actual testing duration and D_T.
    coarse=make_cover((0,1),pf['eta_fit']['rho_search'])
    M=len(coarse[0]);assert M<=pf['eta_fit']['Mbar']
    m=pf['eta_fit']['m_search'];n=pf['eta_fit']['n_select']
    Ts=M*m+W;Tsel=2*n+W;Tinit=Ts+Tsel
    fixedrho=pf['union']['rho']
    # Paper preflight's D_T must reflect actual discrete cover length.
    D=Tinit+certificate(T-Tinit,world,(0,1),fixed_radius=fixedrho)['B']
    assert D<=(1+world.gamma)*pf['union']['B']+1e-9
    cover=make_cover((0,1),fixedrho)
    rc,cp,ctr=cover_policy(seed,0,T,*cover,peaks,Q,200_000)
    reps,counts,sums,prev,prev_y,rs=search_phase(seed,*coarse,peaks,m,Q,W)
    assert counts.min()==m and counts.max()==m,(counts,m)
    eps=L*pf['eta_fit']['rho_search']+2*math.sqrt(pf['eta_fit']['Lambda']/(2*m))/Q
    winner,sep,rpart=select_phase(seed,Ts,Tsel,reps,counts.copy(),sums.copy(),
                                    prev,prev_y,*coarse,peaks,Q,pf['eta_fit']['Lambda'],eps)
    accepted=False;accept_cost=None
    if winner>=0:
        accept_cost=sep+certificate(T-sep,world,(winner,))['B']
        accepted=accept_cost<=D+1e-9
    switch=sep if accepted else Tinit
    if accepted: sel=rpart
    else:
        stop=sep if sep>=0 else Tinit
        sel=rpart+remaining_select_pseudoregret(stop,Tinit,Ts,reps,*coarse[:3],peaks)
    J=(winner,) if accepted else (0,1)
    rho=certificate(T-switch,world,J)['rho'] if accepted else fixedrho
    gcover=make_cover(J,rho)
    cont,gp,_=cover_policy(seed,switch,T-switch,*gcover,peaks,Q,200_000)
    rg=rs+sel+cont
    return {"world":world_name,"seed":seed,"T":T,"q":Q,"dims":"1,2","L":L,
      "union_rho":fixedrho,"eta":pf['eta_fit']['eta'],"rho_search":pf['eta_fit']['rho_search'],
      "M_actual":M,"M_envelope":pf['eta_fit']['Mbar'],"m_search":m,"n_select":n,
      "T_search":Ts,"T_init_actual":Tinit,"T_init_envelope":pf['T_init'],
      "D_T_actual":D,"B_union":pf['union']['B'],"B_family1":pf['singletons'][0]['B'],
      "B_family2":pf['singletons'][1]['B'],"cover_regret":rc,"gadu_regret":rg,
      "paired_difference":rg-rc,"regret_search":rs,"regret_select":sel,
      "regret_continue":cont,"accepted":accepted,"selected_family":winner,
      "certificate_correct":winner==int(np.argmax(peaks)) if winner>=0 else None,
      "certification_round":sep,"switch_round":switch,"accepted_rho":rho,
      "cover_family_pulls":cp.tolist(),"gadu_continue_pulls":gp.tolist(),
      "cover_trace_every_200k":ctr.tolist()}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--smoke',action='store_true')
    args=ap.parse_args()
    # one smoke first on seed outside heldout blocks
    if args.smoke:
        runs=[('best_1d_strong',123123)]
    else:
        runs=[(w,s) for w in CONFIG['primary_worlds'] for s in CONFIG['primary_eval_seeds']]
        runs.extend((w,s) for w in CONFIG['secondary_worlds'] for s in CONFIG['secondary_eval_seeds'])
    rows=[];out=ROOT/('smoke_nested_output.json' if args.smoke else 'nested_raw.json')
    for i,(world,seed) in enumerate(runs,1):
        r=run_cell(world,seed);rows.append(r)
        out.write_text(json.dumps(rows,indent=2))
        print(f'{i}/{len(runs)} {world} {seed} Cover={r["cover_regret"]:.2f} GADU={r["gadu_regret"]:.2f} diff={r["paired_difference"]:.2f} accepted={r["accepted"]} correct={r["certificate_correct"]}',flush=True)
    if not args.smoke:
        with (ROOT/'nested_raw.csv').open('w',newline='') as fp:
            fields=[k for k in rows[0] if k not in ('cover_trace_every_200k','cover_family_pulls','gadu_continue_pulls')]
            outcsv=csv.DictWriter(fp,fieldnames=fields);outcsv.writeheader()
            for r in rows:outcsv.writerow({k:r[k] for k in fields})

if __name__=='__main__':main()
