#!/usr/bin/env python3
"""Independent, exploratory K=3, d=(2,3,4) variant of previous source-informed E03 policy.

NOT the authors' original implementation. This pilot prioritizes auditable dynamics and honest
fair-baseline comparisons. Full T decisions include all Search/Compare/Continue rounds.
"""
from __future__ import annotations
import math, json, hashlib, sys, platform, time
from pathlib import Path
from itertools import product
import numpy as np
from numba import njit
from exact_source_preflight import World, preflight, certificate
HERE=Path(__file__).resolve().parent
LOCK=json.loads((HERE/'d234_pilot_lock.json').read_text())
DIMS=tuple(LOCK['dims']); K=len(DIMS); AMP=LOCK['reward_amplitude']; T=LOCK['T']
CENTERS=np.zeros((K,4),dtype=np.float64)
for i,v in enumerate(LOCK['centers']):CENTERS[i,:len(v)]=v


def physical_id(i,p):
    """Stable keyed by physical (family, coordinates) independent of local net index."""
    msg=f'{i}:'+','.join(str(round(float(c)*1_000_000)) for c in p)
    return int.from_bytes(hashlib.blake2b(msg.encode(),digest_size=8,person=b'GADU2026').digest(),'big') & ((1<<62)-1)


def generate_cover(families,rho):
    fam=[];pts=[];ids=[];diag=[]
    for i in families:
        d=DIMS[i]
        n=max(1,math.ceil(math.sqrt(d)/(2*rho)-1e-12))
        base=[tuple((j+.5)/n for j in ix) for ix in product(range(n),repeat=d)]
        pts_i=base[:]
        limit=math.ceil(LOCK['C'][i]*rho**(-d)-1e-12)
        if len(pts_i)>limit:raise ValueError(('C too small for valid Euclidean cover',i,rho,len(pts_i),limit))
        coarse=tuple(.5 for _ in range(d))
        if coarse not in pts_i and len(pts_i)<limit:pts_i.append(coarse)
        assert len(pts_i)==len(set(pts_i))
        assert math.sqrt(d)/(2*n)<=rho+1e-12
        for p in pts_i:
            fam.append(i);pts.append(p+(0.,)*(4-d));ids.append(physical_id(i,p))
        diag.append({'family':i,'dim':d,'rho':rho,'axis':n,'base_count':len(base),'count':len(pts_i),'envelope':limit,'radius_witness':math.sqrt(d)/(2*n),'coarse_retained':coarse in pts_i})
    assert len(set(ids))==len(ids)
    return (np.array(fam,dtype=np.int64),np.array(pts,dtype=np.float64),np.array(ids,dtype=np.int64)),diag

@njit
def urn(seed,t,arm,channel):
    v=(np.uint64(seed)^np.uint64(t)*np.uint64(0x9E3779B97F4A7C15)
       ^np.uint64(arm+1)*np.uint64(0xBF58476D1CE4E5B9)
       ^np.uint64(channel+1)*np.uint64(0x94D049BB133111EB))
    v=(v^(v>>np.uint64(30)))*np.uint64(0xBF58476D1CE4E5B9)
    v=(v^(v>>np.uint64(27)))*np.uint64(0x94D049BB133111EB)
    v=v^(v>>np.uint64(31))
    return float(v>>np.uint64(11))/9007199254740992.

@njit
def latent(k,p,peaks,centers,dims,amp):
    sq=0.
    for j in range(dims[k]):
        z=p[j]-centers[k,j];sq+=z*z
    return min(1.,max(0.,peaks[k]-amp*sq))

@njit
def ysource(seed,t,arm,mu,q):
    if urn(seed,t,arm,0)>=mu:return 0.
    return 1./q if urn(seed,t,arm,1)<q else 0.

@njit
def immediate_cover(seed,start,horizon,fam,points,ids,peaks,centers,dims,amp,q):
    M=len(fam);counts=np.zeros(M,np.int64);sums=np.zeros(M,np.float64)
    pulls=np.zeros(len(peaks),np.int64)
    previous=-1;prev_y=0.;regret=0.;opt=np.max(peaks)
    for j in range(1,horizon+1):
        if previous>=0:
            counts[previous]+=1;sums[previous]+=prev_y
        tt=math.log(max(2,j));arg=0;maxv=-1e100
        for a in range(M):
            n=counts[a]
            if n<2: score=float('inf')
            else:
                mean=sums[a]/n;variance=max(0.,mean/q-mean*mean)
                score=mean+math.sqrt(16.*variance*tt/n)+56.*tt/(3*q*n)
            if score>maxv:maxv=score;arg=a
        f=fam[arg];mu=latent(f,points[arg],peaks,centers,dims,amp)
        previous=arg;prev_y=ysource(seed,start+j,ids[arg],mu,q)
        regret+=opt-mu;pulls[f]+=1
    return regret,pulls

@njit
def search(seed,fam,points,ids,peaks,centers,dims,amp,m,q,w):
    M=len(fam);last=M*m+w;counts=np.zeros(M,np.int64);sums=np.zeros(M,np.float64)
    opt=np.max(peaks);regret=0.;prev=-1;py=0.
    for t in range(1,last+1):
        if prev>=0: counts[prev]+=1;sums[prev]+=py
        a=(t-1)%M;mu=latent(fam[a],points[a],peaks,centers,dims,amp)
        prev=a;py=ysource(seed,t,ids[a],mu,q)
        regret+=opt-mu
    reps=np.zeros(len(peaks),np.int64)
    for k in range(len(peaks)):
        best=-1e100;ix=-1
        for a in range(M):
            if fam[a]!=k:continue
            val=sums[a]/counts[a]
            if val>best:best=val;ix=a
        reps[k]=ix
    return reps,counts,sums,prev,py,regret

@njit
def compare(seed,t0,compare_budget,reps,counts,sums,prev,py,
            fam,points,ids,peaks,centers,dims,amp,q,lam,epsilon):
    K=len(reps);regret=0.;opt=np.max(peaks)
    for j in range(1,compare_budget+1):
        t=t0+j
        if prev>=0:counts[prev]+=1;sums[prev]+=py
        a=reps[(j-1)%K];mu=latent(fam[a],points[a],peaks,centers,dims,amp)
        prev=a;py=ysource(seed,t,ids[a],mu,q)
        regret+=opt-mu
        # Certification requires one candidate's lower interval above every competitor's upper.
        for winner in range(K):
            idx=reps[winner];cnt=counts[idx];mean=sums[idx]/cnt
            lo=mean-math.sqrt(lam/(2*cnt))/q
            safe=True
            for other in range(K):
                if other==winner:continue
                x=reps[other];nc=counts[x];avg=sums[x]/nc
                hi=min(1.,avg+math.sqrt(lam/(2*nc))/q+epsilon)
                if lo<=hi:safe=False;break
            if safe:return winner,t,regret
    return -1,-1,regret


def expected_tail_regret(reps,stop,tend,search_end,fam,points,peaks):
    # Compare if no economically valid certification: finish committed Compare budget.
    N=len(reps);v=0.;optimal=max(peaks)
    for t in range(stop+1,tend+1):
        ix=reps[(t-search_end-1)%N];k=fam[ix]
        x=points[ix];d=DIMS[k];mu=min(1.,max(0.,peaks[k]-AMP*np.sum((x[:d]-CENTERS[k,:d])**2)))
        v+=optimal-mu
    return v


def run_case(world,seed,T,quiet=True):
    peaks=np.asarray(LOCK['worlds'][world]['peaks'],dtype=np.float64)
    source=World(DIMS,tuple(LOCK['C']),LOCK['L'],LOCK['q'],LOCK['w'],LOCK['gamma'])
    pf=preflight(T,source)
    assert pf['entered_search']
    tune=pf['eta_fit'];q=source.q
    searchcover,sd=generate_cover(tuple(range(K)),tune['rho_search']);M=len(searchcover[0])
    assert M<=tune['Mbar']
    m=tune['m_search'];nc=tune['n_select']
    Ts=M*m+source.w;Tsel=K*nc+source.w;Tinit=Ts+Tsel
    unionr=pf['union']['rho'];basecover,bd=generate_cover(tuple(range(K)),unionr)
    cover_regret,coverpulls=immediate_cover(seed,0,T,*basecover,peaks,CENTERS,np.asarray(DIMS,dtype=np.int64),AMP,q)
    # Secondary DIAGNOSTIC, not source-optimized baseline.
    fixedcover,fd=generate_cover(tuple(range(K)),.5)
    fixed_regret,fixedpulls=immediate_cover(seed,0,T,*fixedcover,peaks,CENTERS,np.asarray(DIMS,dtype=np.int64),AMP,q)
    reps,counts,sums,prev,py,rsearch=search(seed,*searchcover,peaks,CENTERS,np.asarray(DIMS,dtype=np.int64),AMP,m,q,source.w)
    assert np.min(counts)==m==np.max(counts)
    eps=source.L*tune['rho_search']+2*math.sqrt(tune['Lambda']/(2*m))/q
    winner,sep,cmp=compare(seed,Ts,Tsel,reps,counts.copy(),sums.copy(),prev,py,
       *searchcover,peaks,CENTERS,np.asarray(DIMS,dtype=np.int64),AMP,q,tune['Lambda'],eps)
    D=Tinit+certificate(T-Tinit,source,tuple(range(K)),fixed_radius=unionr)['B']
    accepted=False;cost=None
    if winner>=0:
        cost=sep+certificate(T-sep,source,(winner,))['B']; accepted=cost<=D+1e-9
    switch=sep if accepted else Tinit
    if accepted: rcompare=cmp;J=(winner,)
    else:
        stop=sep if sep>=0 else Tinit
        rcompare=cmp+expected_tail_regret(reps,stop,Tinit,Ts,searchcover[0],searchcover[1],peaks)
        J=tuple(range(K))
    next_rho=certificate(T-switch,source,J)['rho'] if accepted else unionr
    contcover,cd=generate_cover(J,next_rho)
    rcontinue,continuepulls=immediate_cover(seed,switch,T-switch,*contcover,peaks,CENTERS,np.asarray(DIMS,dtype=np.int64),AMP,q)
    rgadu=rsearch+rcompare+rcontinue
    return {'world':world,'seed':seed,'T':T,'dims':list(DIMS),'peak_parameters':peaks.tolist(),
      'eta':tune['eta'],'rho_search':tune['rho_search'],'search_envelope':tune['Mbar'],
      'search_actions':M,'search_by_family':sd,'search_m':m,'compare_n':nc,'T_search':Ts,'T_init':Tinit,
      'epsilon':eps,'base_rho':unionr,'base_actions':len(basecover[0]),'base_by_family':bd,
      'diagnostic_rho':.5,'diagnostic_actions':len(fixedcover[0]),'diagnostic_by_family':fd,
      'winner':winner,'certificate_correct':bool(winner==int(np.argmax(peaks))) if winner>=0 else None,
      'accepted':bool(accepted),'certification_round':sep,'switch_round':switch,
      'economic_D':D,'economic_accept_cost':cost,'continuation_family':list(J),
      'continuation_rho':next_rho,'continuation_actions':len(contcover[0]),'continuation_by_family':cd,
      'regret_search':float(rsearch),'regret_compare':float(rcompare),'regret_continue':float(rcontinue),
      'regret_candidate':float(rgadu),'regret_source_cover':float(cover_regret),
      'regret_fixed_cover':float(fixed_regret),
      'delta_vs_source':float(rgadu-cover_regret),'delta_vs_fixed':float(rgadu-fixed_regret),
      'source_baseline_family_pulls':coverpulls.tolist(),
      'fixed_baseline_family_pulls':fixedpulls.tolist(),
      'continue_family_pulls':continuepulls.tolist(),
      'search_exceeds_source':bool(rsearch>cover_regret),
      'search_exceeds_fixed':bool(rsearch>fixed_regret)}


def main():
    p=json.loads((HERE/'d234_pilot_lock.json').read_text());out=HERE/'d234_raw.json'
    meta={'lock_sha256':hashlib.sha256((HERE/'d234_pilot_lock.json').read_bytes()).hexdigest(),
          'pilot_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'preflight_sha256':hashlib.sha256((HERE/'exact_source_preflight.py').read_bytes()).hexdigest(),
          'python':platform.python_version(),'numpy':np.__version__,'numba':'active'}
    (HERE/'d234_metadata.json').write_text(json.dumps(meta,indent=2))
    rows=[];cells=[(world,seed) for world in p['worlds'] for seed in p['seeds']]
    for i,(world,seed) in enumerate(cells,1):
        start=time.monotonic();r=run_case(world,seed,p['T']);r['elapsed_seconds']=time.monotonic()-start
        rows.append(r);out.write_text(json.dumps(rows,indent=2))
        print(f'{i}/{len(cells)} {world} seed={seed} sourceCover={r["regret_source_cover"]:.1f} '
              f'fixedCover={r["regret_fixed_cover"]:.1f} candidate={r["regret_candidate"]:.1f} '
              f'cert={r["winner"]} accepted={r["accepted"]} source_delta={r["delta_vs_source"]:+.1f}',flush=True)
    assert len(rows)==len(cells)
if __name__=='__main__':main()
