"""Independent pure-Python time-indexed Cover policy reference for short runs.

Uses model's immutable source oracle only; independently computes UCB policy,
feedback maturity and regret on heterogeneous 1D+2D grids. Not author parity.
"""
import math
import numpy as np
import experiment_nested as sim


def reference(seed,worldname,horizon):
    peak=np.array(sim.CONFIG['world_parameters'][worldname]['peaks'])
    fam,x,y,ids=sim.make_cover((0,1),.5)
    n=len(fam);count=[0]*n;obs=[0.]*n;pending=None;R=0.;pulls=[0,0]
    for t in range(1,horizon+1):
        # Window w=1: v=t-1 source available before decision t.
        if pending is not None:
            a,yy=pending;count[a]+=1;obs[a]+=yy
        scores=[]
        for a in range(n):
            if count[a]<2:scores.append(float('inf'))
            else:
                mean=obs[a]/count[a]
                variance=max(0.,mean/sim.Q-mean*mean)
                scores.append(mean+math.sqrt(16*variance*math.log(max(2,t))/count[a])+56*math.log(max(2,t))/(3*sim.Q*count[a]))
        choice=max(range(n),key=lambda a:scores[a])
        k=int(fam[choice]);p=sim.reward(k,float(x[choice]),float(y[choice]),peak)
        z=sim.u(seed,t,int(ids[choice]),0)<p
        ontime=z and sim.u(seed,t,int(ids[choice]),1)<sim.Q
        pending=(choice,(1/sim.Q if ontime else 0.))
        R+=max(peak)-p;pulls[k]+=1
    return R,pulls


def run():
    tested=0
    for world in ('best_1d_strong','best_2d_strong','best_1d_near_tie'):
        for seed in (222,444,888):
            for horizon in (17,101,1201):
                peak=np.asarray(sim.CONFIG['world_parameters'][world]['peaks'],float)
                grid=sim.make_cover((0,1),.5)
                R,Ps=reference(seed,world,horizon)
                fast,pulls,_=sim.cover_policy(seed,0,horizon,*grid,peak,sim.Q,200)
                assert abs(R-fast)<1e-7,(world,seed,horizon,R,fast)
                assert Ps==pulls.tolist(),(world,seed,horizon,Ps,pulls)
                tested+=1
    print(f'PASS {tested}/{tested} pure-Python Cover policy/source-clock checks, including q<1, 1D+2D, distinct horizons')

if __name__=='__main__':run()
