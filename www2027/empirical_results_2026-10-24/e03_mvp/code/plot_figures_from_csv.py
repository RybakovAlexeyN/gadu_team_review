#!/usr/bin/env python3
"""Independent public-CSV regenerater of E03 figures; no bandit reruns.
Usage: python code/plot_figures_from_csv.py  (numpy, scipy, matplotlib)
Output: regenerated/fig1...pdf/svg/png etc. Same scientific content and
archived seed-level checkpoints; numerical rendering can differ by library versions.
"""
from pathlib import Path
import csv, math
from collections import defaultdict
import numpy as np
from scipy.stats import t as tdist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'regenerated';OUT.mkdir(exist_ok=True)
with (ROOT/'data/e03_per_seed_trajectory_checkpoints.csv').open(newline='') as f: pts=list(csv.DictReader(f))
with (ROOT/'data/e03_seed_runs.csv').open(newline='') as f: raw=list(csv.DictReader(f))
with (ROOT/'data/table_e03_final.csv').open(newline='') as f: summ={r['scenario']:r for r in csv.DictReader(f)}
assert len(pts)==2080 and len(raw)==20
W=['best_1d_strong','best_2d_strong','best_1d_near_tie']
COL={'GADU':'#c46239','Cover-UCB':'#285b83'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
for w in W:
 n=sum(r['world']==w for r in raw)
 assert n in (4,8)

# Ensure every archived seed-level endpoint matches frozen CSV.
groups=defaultdict(list)
for r in pts:groups[(r['scenario'],r['policy'],r['seed'])].append((int(r['t']),float(r['pseudo_regret'])))
for r in raw:
 for p,col in [('GADU','gadu_regret'),('Cover-UCB','cover_regret')]:
  zz=sorted(groups[(r['world'],p,r['seed'])]);assert zz[0]==(0,0.) and zz[-1][0]==10000000
  assert all(b[0]>a[0] and b[1]>=a[1]-1e-6 for a,b in zip(zz,zz[1:]))
  assert abs(zz[-1][1]-float(r[col]))<2e-5
 assert abs(sum(float(r[x]) for x in ('regret_search','regret_select','regret_continue'))-float(r['gadu_regret']))<1e-5

def save(fig,name):
 for fmt in ('pdf','svg','png'): fig.savefig(OUT/(name+'.'+fmt),dpi=230,bbox_inches='tight')
 plt.close(fig)
fig,axs=plt.subplots(3,1,figsize=(7.15,7.4),sharex=True,layout='constrained')
for ax,w,lab in zip(axs,W,['A  Best 1D, gap 0.62','B  Best 2D, gap 0.62','C  Near tie, gap 0.02']):
 seedset=sorted(r['seed'] for r in raw if r['world']==w);n=len(seedset)
 for pol in ('Cover-UCB','GADU'):
  z=[sorted(groups[(w,pol,s)]) for s in seedset]
  xx=np.array([t for t,_ in z[0]],float)
  assert all(np.array_equal(xx,[t for t,_ in a]) for a in z)
  yy=np.array([[v for t,v in a] for a in z]);mu=yy.mean(axis=0)
  half=tdist.ppf(.975,n-1)*yy.std(axis=0,ddof=1)/math.sqrt(n)
  ax.plot(xx/1e6,mu,color=COL[pol],lw=1.9,label=pol)
  ax.fill_between(xx/1e6,np.maximum(0,mu-half),mu+half,color=COL[pol],alpha=.19,lw=0)
  expected=float(summ[w]['gadu_regret' if pol=='GADU' else 'cover_regret'])
  assert abs(mu[-1]-expected)<1e-5
 ax.axvline(1.160162 if w=='best_1d_near_tie' else 1.111822,color='#667085',lw=.8,ls='--',alpha=.7)
 ax.set_title(f'{lab}   (n={n})',loc='left',weight='bold',pad=6)
 ax.set_ylabel('Cumulative pseudo-regret')
 ax.yaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x/1000:,.0f}k' if abs(x)>=1000 else f'{x:g}'))
 ax.grid(axis='y',alpha=.16);ax.set_xlim(0,10.1)
axs[-1].set_xlabel('Decision round t (millions)')
axs[0].legend(frameon=False,ncol=2,loc='center right',bbox_to_anchor=(.98,.83))
fig.suptitle('E03 | finite-horizon performance of independent source-informed GADU',fontsize=11,weight='bold')
save(fig,'fig1_cumulative_regret')
fig,ax=plt.subplots(figsize=(7.15,3.9),layout='constrained')
loc=np.arange(3);width=.33;base=np.zeros(3)
for key,title,color in [('regret_search','Search','#596f9a'),('regret_select','Compare','#dab16f'),('regret_continue','Continue','#52958f')]:
 val=np.array([float(summ[w][key]) for w in W])/1000.
 ax.bar(loc-width/1.8,val,bottom=base,width=width,color=color,label=title);base+=val
ax.bar(loc+width/1.8,[float(summ[w]['cover_regret'])/1000 for w in W],width=width,color=COL['Cover-UCB'],label='Immediate Cover')
ax.set_xticks(loc,['Best 1D','Best 2D','Near tie']);ax.set_ylabel('Mean final pseudo-regret (thousands)')
ax.set_title('E03 | search cost dominates GADU regret on these worlds',weight='bold',loc='left')
ax.set_ylim(0,700);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
for j,w in enumerate(W):
 ax.annotate(f"{float(summ[w]['search_share'])*100:.1f}% Search",(loc[j]-width/1.8,base[j]),xytext=(0,4),textcoords='offset points',ha='center',fontsize=7.5)
ax.legend(frameon=False,ncol=4,loc='upper right');save(fig,'fig2_stage_decomposition')
fig=plt.figure(figsize=(7.15,3.45),layout='constrained')
ax=fig.add_subplot(1,2,1);x=np.linspace(0,1,240)
ax.plot(x,.8-.1*(x-.5)**2,label='$p_1=0.8$',color='#c46239')
ax.plot(x,.18-.1*(x-.5)**2,label='$p_1=0.18$',color='#285b83')
ax.set(xlabel='x',ylabel='$f_1(x)$',title='1D family | peak at 0.5');ax.grid(alpha=.15);ax.legend(frameon=False,fontsize=8)
ax=fig.add_subplot(1,2,2)
xv,yv=np.meshgrid(np.linspace(0,1,100),np.linspace(0,1,100));z=.8-.09*((xv-.25)**2+(yv-.75)**2)
im=ax.imshow(z,origin='lower',extent=(0,1,0,1),cmap='viridis',vmin=.66,vmax=.81,aspect='equal')
ax.plot([.25],[.75],'+',color='white',ms=11,mew=2)
ax.set(title='2D family | peak at (0.25,0.75)',xlabel='x',ylabel='y');fig.colorbar(im,ax=ax,shrink=.72).set_label('$f_2(x,y)$, $p_2=0.8$')
save(fig,'fig3_reward_functions')
print(f'PASS {len(raw)} original seed records, {len(pts)} archived checkpoints; 3 three-format figures regenerated without any new policy simulation')
