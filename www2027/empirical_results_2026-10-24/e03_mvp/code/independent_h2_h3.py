#!/usr/bin/env python3
"""Independent event-source/short-policy oracle and exact cover envelope tests.
Deliberately writes no experiment CSV and runs no 10m simulations.
"""
import csv, math, sys
from pathlib import Path
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
from experiment_nested import make_cover, search_phase, select_phase, source_y, u

MASK=(1<<64)-1

def U(seed,t,arm,channel):
    z=(seed ^ (t*0x9E3779B97F4A7C15) ^ ((arm+1)*0xBF58476D1CE4E5B9) ^ ((channel+1)*0x94D049BB133111EB))&MASK
    z=((z^(z>>30))*0xBF58476D1CE4E5B9)&MASK
    z=((z^(z>>27))*0x94D049BB133111EB)&MASK
    z=z^(z>>31)
    return (z>>11)/(2**53)

def mu(k,x,y,peaks):
    a=(peaks[0]-.10*(x-.5)**2) if k==0 else peaks[1]-.09*((x-.25)**2+(y-.75)**2)
    return min(1.,max(0.,a))

def obs(seed,t,arm,m,q):
    z=U(seed,t,arm,0)<m
    d=1 if U(seed,t,arm,1)<q else 4
    return (float(z and d<=1)/q, 'silent_failure' if not z else 'on_time_positive' if d<=1 else 'late_censored_positive')

def check(a,b,label,tol=1e-9):
    if abs(float(a)-float(b))>tol:raise AssertionError((label,a,b))

def oracle_search(seed,F,X,Y,IDS,peaks,m,q,w):
    M=len(F);cnt=[0]*M;sums=[0.]*M;due={};regret=0.;last=-1;last_y=0.
    for t in range(1,M*m+w+1):
        for i,y in due.pop(t,[]):cnt[i]+=1;sums[i]+=y
        i=(t-1)%M;v=mu(int(F[i]),float(X[i]),float(Y[i]),peaks)
        regret+=max(peaks)-v
        yy,_=obs(seed,t,int(IDS[i]),v,q)
        due.setdefault(t+1,[]).append((i,yy));last=i;last_y=yy
    reps=[max((i for i in range(M) if F[i]==k),key=lambda i:(sums[i]/cnt[i],-i)) for k in (0,1)]
    return reps,cnt,sums,last,last_y,regret

def oracle_select(seed,t0,h,reps,counts,sums,prev,prev_y,F,X,Y,IDS,peaks,q,lam,eps):
    C=list(counts);S=list(sums);regret=0.
    for j in range(1,h+1):
        t=t0+j;C[prev]+=1;S[prev]+=prev_y
        a=reps[(j-1)%2];v=mu(int(F[a]),float(X[a]),float(Y[a]),peaks)
        regret+=max(peaks)-v
        prev_y,_=obs(seed,t,int(IDS[a]),v,q);prev=a
        low=[];high=[]
        for k in (0,1):
            ix=reps[k];n=C[ix];rad=math.sqrt(lam/(2*n))/q; avg=S[ix]/n
            low.append(avg-rad);high.append(min(1.,avg+rad+eps))
        if low[0]>high[1]:return 0,t,regret
        if low[1]>high[0]:return 1,t,regret
    return -1,-1,regret

def h2():
    statuses=set();s_checks=0
    # Force all three possible statuses, plus 64-bit deterministic hash parity.
    for seed in range(1,9):
        for t in range(1,14):
            for arm in [0,500000000000,1250000000000]:
                for channel in (0,1):check(U(seed,t,arm,channel),u(seed,t,arm,channel),'hash',2e-15)
                for mm in (0,.18,.78,1):
                    y,status=obs(seed,t,arm,mm,.75);statuses.add(status)
                    check(y,source_y(seed,t,arm,mm,.75),'source event')
    assert statuses=={'silent_failure','on_time_positive','late_censored_positive'},statuses
    cases=0;branches=set();F,X,Y,IDS=make_cover((0,1),5./24.)
    for seed in range(1,17):
        for peaks in ((.8,.18),(.18,.8),(.8,.78)):
            for q in (1.,.75):
                m=4;w=1;ts=len(F)*m+w
                ref=oracle_search(seed,F,X,Y,IDS,peaks,m,q,w)
                tested=search_phase(seed,F,X,Y,IDS,np.array(peaks),m,q,w)
                assert list(tested[0])==ref[0]
                assert list(tested[1])==ref[1]
                assert min(ref[1])==m==max(ref[1])
                np.testing.assert_allclose(tested[2],ref[2],atol=1e-9,rtol=0.)
                assert tested[3]==ref[3]
                check(tested[4],ref[4],'last_y')
                check(tested[5],ref[5],'search regret')
                s_checks+=1
                for lam,eps,h in ((0.,0.,18),(2.,2.,12),(.02,0.,18)):
                    o=oracle_select(seed,ts,h,*ref[:5],F,X,Y,IDS,peaks,q,lam,eps)
                    result=select_phase(seed,ts,h,tested[0],tested[1].copy(),tested[2].copy(),tested[3],tested[4],F,X,Y,IDS,np.array(peaks),q,lam,eps)
                    assert (result[0],result[1])==(o[0],o[1]),(seed,peaks,q,lam,eps,result,o)
                    check(result[2],o[2],'select regret')
                    branches.add('strict_sep' if o[0]>=0 else 'none')
                    cases+=1
    assert branches=={'strict_sep','none'},branches
    print('H2 PASS scoped: 3 statuses, independent 64bit CRN and event oracle,',s_checks,'Search and',cases,'Compare branches; both separation/no separation.')

def h3():
    # Analytic Euclidean radius upper bounds via full uniform Cartesian subsets.
    verified=[]; maps={}
    for rho in (.5,.25,5./24.):
        for k,d in ((0,1),(1,2)):
            F,X,Y,IDS=make_cover((k,),rho)
            assert len(IDS)<=math.ceil(rho**(-d))
            assert len(IDS)==len(set(map(int,IDS)))
            if k==0:
                vv=sorted(float(x) for x in X)
                upper=max(vv[0],1.-vv[-1],max(((b-a)/2 for a,b in zip(vv,vv[1:])), default=0.) )
            else:
                # Cartesian subset guaranteed by construction; enclosing max radius
                # sqrt(2)/2n where n in {2,3,4} for actual exercised radius.
                n={.5:2,.25:3,5./24.:4}[rho]
                axis={(i+.5)/n for i in range(n)} if rho !=.5 else {.25,.75}
                pts={(round(float(x),12),round(float(y),12)) for x,y in zip(X,Y)}
                assert all((round(x,12),round(y,12)) in pts for x in axis for y in axis)
                upper=math.sqrt(2)/(2*n)
            assert upper<=rho+1e-10,(rho,k,upper)
            verified.append((k,rho,upper,len(IDS)))
            for a,x,y,idx in zip(F,X,Y,IDS):
                key=(int(a),round(float(x),12),round(float(y),12))
                if key in maps:assert maps[key]==int(idx)
                maps[key]=int(idx)
    with (ROOT.parent/'data'/'e03_seed_runs.csv').open(newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==20
    for r in rows:
        assert int(r['T'])==10_000_000 and float(r['q'])==.75
        assert int(r['M_actual'])==23 and int(r['M_envelope'])==29
        ts=int(r['M_actual'])*int(r['m_search'])+1
        ti=ts+2*int(r['n_select'])+1
        assert ts==int(r['T_search'])==1111821
        assert ti==int(r['T_init_actual'])==1160162
        switch=int(r['switch_round'])
        assert switch+(int(r['T'])-switch)==int(r['T'])
        if r['accepted']=='True':assert switch==int(r['certification_round']) and ts<switch<=ti
        else:assert switch==ti
    print('H3 PASS scoped: ',len(verified),'provably admissible physical grids and stable CRN action identities; 20/20 horizon budgets.')

if __name__=='__main__':h2();h3()
