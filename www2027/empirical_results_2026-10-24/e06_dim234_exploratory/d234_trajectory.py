#!/usr/bin/env python3
"""Recompute ACTUAL seed-level policy trajectories; no endpoint interpolation.
The cumulative Search and Compare regret can be evaluated exactly from policy's
round-robin choice sequence (deterministic conditional on chosen reps); the
Cover/Bernstein continuation is rerun at identical seed and calendar ticks.
Outputs are secondary; verify against immutable d234_raw.json endpoints.
"""
import json, math
from pathlib import Path
import numpy as np
from numba import njit
from d234_pilot import LOCK,DIMS,CENTERS,AMP,T,generate_cover,search,compare,urn,ysource,latent
from exact_source_preflight import World,preflight

ROOT=Path(__file__).resolve().parent
SPACING=200_000

@njit
def cover_time_trace(seed,start,horizon,fam,points,ids,peaks,centers,dims,amp,q,spacing):
    M=len(fam);n=len(peaks);counts=np.zeros(M,np.int64);sums=np.zeros(M,np.float64)
    best=np.max(peaks);prev=-1;py=0.;regret=0.
    ticks=np.zeros(horizon//spacing+4,np.int64)
    val=np.zeros(horizon//spacing+4,np.float64)
    nr=0
    for j in range(1,horizon+1):
        if prev>=0:counts[prev]+=1;sums[prev]+=py
        lg=math.log(max(2,j));vmax=-1e100;arg=0
        for k in range(M):
            nk=counts[k]
            if nk<2:score=float('inf')
            else:
                avg=sums[k]/nk;var=max(0.,avg/q-avg*avg)
                score=avg+math.sqrt(16.*var*lg/nk)+56.*lg/(3*q*nk)
            if score>vmax:vmax=score;arg=k
        f=fam[arg];mu=latent(f,points[arg],peaks,centers,dims,amp)
        prev=arg;py=ysource(seed,start+j,ids[arg],mu,q)
        regret+=best-mu
        if (start+j)%spacing==0 or j==horizon:
            ticks[nr]=start+j;val[nr]=regret;nr+=1
    return ticks[:nr],val[:nr]


def prefix_rr_regret(t,gaps):
    n=len(gaps);turns=t//n;left=t%n
    return turns*sum(gaps)+sum(gaps[:left])


def rebuild_one(r):
    peaks=np.array(LOCK['worlds'][r['world']]['peaks'],float)
    w=World(DIMS,tuple(LOCK['C']),LOCK['L'],LOCK['q'],LOCK['w'],LOCK['gamma'])
    pre=preflight(T,w);tune=pre['eta_fit'];q=LOCK['q'];dims=np.array(DIMS)
    sc,_=generate_cover((0,1,2),tune['rho_search']);nc=len(sc[0]);m=tune['m_search'];Ts=nc*m+LOCK['w']
    reps,counts,sums,prev,py,rs=search(r['seed'],*sc,peaks,CENTERS,dims,AMP,m,q,w.w)
    assert abs(rs-r['regret_search'])<1e-5
    raw=ROOT/'d234_raw.json'
    # Use archived certificate/choice/switch; compare policy's input representative schedule is reproduced.
    gaps=[];best=max(peaks)
    for fam,p in zip(sc[0],sc[1]):
        d=DIMS[fam];mu=max(0.,min(1.,peaks[fam]-AMP*sum((p[k]-CENTERS[fam,k])**2 for k in range(d))))
        gaps.append(best-mu)
    cmp_gaps=[gaps[i] for i in reps]
    sw=r['switch_round'];cmp_steps=sw-Ts
    assert cmp_steps>0
    assert abs(prefix_rr_regret(cmp_steps,cmp_gaps)-r['regret_compare'])<1e-5
    bc,_=generate_cover((0,1,2),r['base_rho'])
    fc,_=generate_cover((0,1,2),r['diagnostic_rho'])
    chosen=tuple(r['continuation_family']);cc,_=generate_cover(chosen,r['continuation_rho'])
    bt,bv=cover_time_trace(r['seed'],0,T,*bc,peaks,CENTERS,dims,AMP,q,SPACING)
    ft,fv=cover_time_trace(r['seed'],0,T,*fc,peaks,CENTERS,dims,AMP,q,SPACING)
    ct,cv=cover_time_trace(r['seed'],sw,T-sw,*cc,peaks,CENTERS,dims,AMP,q,SPACING)
    assert bt[-1]==ft[-1]==ct[-1]==T
    for key,got in [('regret_source_cover',bv[-1]),('regret_fixed_cover',fv[-1]),('regret_continue',cv[-1])]:
        assert abs(got-r[key])<1e-4,(r['world'],key,got,r[key])
    bmap={int(t):float(v) for t,v in zip(bt,bv)}
    fmap={int(t):float(v) for t,v in zip(ft,fv)}
    cmap={int(t):float(v) for t,v in zip(ct,cv)}
    grid_times=[int(t) for t in range(0,T+1,SPACING)]
    out=[]
    for t in grid_times:
        if t==0:out.append({'t':t,'gadu':0.,'source_cover':0.,'fixed_cover':0.});continue
        if t<=Ts:
            value=prefix_rr_regret(t,gaps)
        elif t<=sw:
            value=float(rs)+prefix_rr_regret(t-Ts,cmp_gaps)
        else:
            value=float(rs)+prefix_rr_regret(sw-Ts,cmp_gaps)+cmap[t]
        out.append({'t':t,'gadu':value,'source_cover':bmap[t],'fixed_cover':fmap[t]})
    assert abs(out[-1]['gadu']-r['regret_candidate'])<1e-4,(r['world'],out[-1]['gadu'],r['regret_candidate'])
    return {'world':r['world'],'seed':r['seed'],'switch':sw,'T_search':Ts,'points':out,
        'provenance':'Actual Bernstein UCB trajectories recomputed from frozen seed/absolute clock; Search/Compare exact round-robin actions; no endpoint interpolation.'}


def main():
    rows=json.loads((ROOT/'d234_raw.json').read_text())
    all_=[]
    for r in rows:
        print('replay',r['world'],r['seed'],flush=True)
        result=rebuild_one(r);all_.append(result)
        (ROOT/'d234_trajectories.json').write_text(json.dumps(all_,indent=2))
        print('check t=',result['points'][-1]['t'],'candidate=',round(result['points'][-1]['gadu'],2),flush=True)
    assert len(all_)==6
if __name__=='__main__':main()
