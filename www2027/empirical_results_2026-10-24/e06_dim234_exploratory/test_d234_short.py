#!/usr/bin/env python3
"""Pure-Python independent toy oracle for K=3 Search/Compare source-clock semantics.
This is not author-source equivalence nor a full long-horizon independent simulation.
"""
import math
import numpy as np
from d234_pilot import LOCK,urn,ysource,search,compare,generate_cover,latent,AMP,CENTERS,DIMS
MASK=(1<<64)-1

def ref_random(seed,t,arm,channel):
    x=(seed ^ ((t*0x9E3779B97F4A7C15)&MASK)
       ^ (((arm+1)*0xBF58476D1CE4E5B9)&MASK)
       ^ (((channel+1)*0x94D049BB133111EB)&MASK))
    x=((x^(x>>30))*0xBF58476D1CE4E5B9)&MASK
    x=((x^(x>>27))*0x94D049BB133111EB)&MASK
    x=x^(x>>31)
    return (x>>11)/9007199254740992.

def ref_reward(f,p,peaks):
    d=DIMS[f]
    return max(0.,min(1.,peaks[f]-AMP*sum((p[j]-CENTERS[f,j])**2 for j in range(d))))

def ref_event(seed,t,aid,mu,q):
    if ref_random(seed,t,aid,0)>=mu:return 0.
    return 1./q if ref_random(seed,t,aid,1)<q else 0.

def ref_search(seed,f,p,ids,peaks,m,q):
    M=len(f);counts=[0]*M;sums=[0.]*M;prev=None;prev_y=0.;regret=0.
    for t in range(1,M*m+2):
        if prev is not None:counts[prev]+=1;sums[prev]+=prev_y
        a=(t-1)%M;mu=ref_reward(int(f[a]),p[a],peaks)
        prev=a;prev_y=ref_event(seed,t,int(ids[a]),mu,q)
        regret+=max(peaks)-mu
    rep=[]
    for i in range(len(peaks)):
        rep.append(max((j for j in range(M) if f[j]==i),key=lambda j:(sums[j]/counts[j],-j)))
    return rep,counts,sums,prev,prev_y,regret

def ref_compare(seed,t0,steps,reps,counts,sums,prev,prev_y,f,p,ids,peaks,q,lam,eps):
    counts=list(counts);sums=list(sums);regret=0.
    for j in range(1,steps+1):
        t=t0+j;counts[prev]+=1;sums[prev]+=prev_y
        a=reps[(j-1)%len(reps)];mu=ref_reward(int(f[a]),p[a],peaks)
        prev=a;prev_y=ref_event(seed,t,int(ids[a]),mu,q)
        regret+=max(peaks)-mu
        for wi in range(len(reps)):
            ix=reps[wi];lo=sums[ix]/counts[ix]-math.sqrt(lam/(2*counts[ix]))/q
            others=[min(1.,sums[reps[other]]/counts[reps[other]]+math.sqrt(lam/(2*counts[reps[other]]))/q+eps)
                    for other in range(len(reps)) if other!=wi]
            if all(lo>hi for hi in others):return wi,t,regret
    return -1,-1,regret


def main():
    cover,diag=generate_cover((0,1,2),5/12)
    f,p,ids=cover
    counts={'rng':0,'search':0,'compare':0,'strict_separation':0,'no_separation':0}
    for seed in (11,37,101,202610246401):
        for t in (1,2,3,5,100):
            for arm in ids[::max(1,len(ids)//7)]:
                for channel in (0,1):
                    a=ref_random(seed,t,int(arm),channel);b=urn(seed,t,int(arm),channel)
                    assert a==b,(seed,t,arm,channel,a,b)
                    counts['rng']+=1
        for world in LOCK['worlds']:
            peaks=np.array(LOCK['worlds'][world]['peaks'],float)
            for q in (1.,.75):
                m=3
                source=search(seed,f,p,ids,peaks,CENTERS,np.array(DIMS),AMP,m,q,1)
                oracle=ref_search(seed,f,p,ids,peaks,m,q)
                assert np.array_equal(source[0],oracle[0])
                assert np.array_equal(source[1],oracle[1])
                np.testing.assert_allclose(source[2],oracle[2],rtol=0,atol=1e-10)
                assert source[3]==oracle[3] and abs(source[4]-oracle[4])<1e-12 and abs(source[5]-oracle[5])<1e-8
                assert np.min(source[1])==m
                counts['search']+=1
                for lam,eps in ((0.,0.),(2.,2.),(.1,.05)):
                    steps=15;fargs=(f,p,ids,peaks,CENTERS,np.array(DIMS),AMP,q,lam,eps)
                    c=compare(seed,len(f)*m+1,steps,source[0],source[1].copy(),source[2].copy(),source[3],source[4],*fargs)
                    d=ref_compare(seed,len(f)*m+1,steps,*oracle[:5],f,p,ids,peaks,q,lam,eps)
                    assert c[0]==d[0] and c[1]==d[1] and abs(c[2]-d[2])<1e-8,(c,d)
                    counts['compare']+=1
                    counts['strict_separation' if c[0]>=0 else 'no_separation']+=1
    assert counts['strict_separation']>0 and counts['no_separation']>0,counts
    import json
    with open('d234_short_test_report.json','w') as v:json.dump({'result':'PASS_SCOPED','tests':counts},v,indent=2)
    print(counts)
if __name__=='__main__':main()
