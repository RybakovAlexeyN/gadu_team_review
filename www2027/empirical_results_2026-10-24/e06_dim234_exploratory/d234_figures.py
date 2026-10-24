#!/usr/bin/env python3
"""Generate Figure 1 and Figure 2 exclusively from audited archived E06 source trajectories."""
from pathlib import Path
import json, statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter,MultipleLocator
ROOT=Path(__file__).resolve().parent
rows=json.loads((ROOT/'d234_raw.json').read_text())
traces=json.loads((ROOT/'d234_trajectories.json').read_text())
worlds=[('strong_gap','Strong gap: 0.80 vs 0.28/0.26'),('moderate_gap','Moderate gap: 0.80 vs 0.55/0.53'),('near_tie','Near tie: 0.80 vs 0.785/0.780')]
colors={'gadu':'#cf6426','source_cover':'#24618e','fixed_cover':'#389783'}
fig,axs=plt.subplots(3,1,figsize=(10.4,10.6),sharex=True,constrained_layout=True)
for ax,(world,label) in zip(axs,worlds):
 subset=[x for x in traces if x['world']==world]
 t=np.array([p['t']/1e6 for p in subset[0]['points']]);assert len(t)==51
 for key,name in [('gadu','GADU-inspired (independent)'),('source_cover','Immediate Cover (source tuned)'),('fixed_cover','Immediate Cover (fixed radius 0.5)')]:
  ys=np.array([[p[key] for p in one['points']] for one in subset]);mu=ys.mean(axis=0)
  for y in ys:ax.plot(t,y,color=colors[key],alpha=.19,lw=.8)
  ax.plot(t,mu,color=colors[key],lw=2.2,label=name)
 for trace in subset:ax.axvline(trace['switch']/1e6,color='gray',alpha=.15,lw=1,ls='--')
 ax.set_title(label,loc='left',fontsize=11,weight='bold')
 ax.yaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x/1e3:,.0f}k'))
 ax.grid(axis='y',alpha=.15)
 ax.set_ylabel('Cumulative regret')
 ax.spines[['top','right']].set_visible(False)
axs[0].legend(fontsize=8.7,loc='upper left',frameon=False)
axs[-1].set_xlabel('Decision round (millions)')
axs[-1].xaxis.set_major_locator(MultipleLocator(2))
fig.suptitle('d = 2 vs d = 3, 4   |   T = 10M, q = 0.75   |   n = 2 seeds per world',fontsize=12.5,weight='bold')
for ext in ('png','pdf'):
 fig.savefig(ROOT/f'd234_cumulative_regret.{ext}',dpi=190,bbox_inches='tight')
plt.close(fig)
fig,ax=plt.subplots(figsize=(10.4,5.4),constrained_layout=True)
xx=np.arange(3);width=.27
from collections import defaultdict
by={world:[r for r in rows if r['world']==world] for world,_ in worlds}
for i,k in enumerate(['regret_search','regret_compare','regret_continue']):
 vals=np.array([statistics.fmean(r[k] for r in by[w]) for w,_ in worlds])
 bottom=np.zeros(3)
 for prev in ['regret_search','regret_compare','regret_continue'][:i]:
  bottom+=np.array([statistics.fmean(r[prev] for r in by[w]) for w,_ in worlds])
 ax.bar(xx-width,vals,width,bottom=bottom,label=['GADU: Search','GADU: Compare','GADU: Continue'][i],alpha=.92)
for key,name,shift,hatch in [('regret_source_cover','Source-tuned Cover',0,''),('regret_fixed_cover','Fixed-radius Cover',width,'//')]:
 vals=[statistics.fmean(r[key] for r in by[w]) for w,_ in worlds]
 ax.bar(xx+shift,vals,width,label=name,hatch=hatch,alpha=.7)
ax.set_xticks(xx,['Strong gap','Moderate gap','Near tie'])
ax.set_ylabel('Final cumulative latent pseudo-regret')
ax.set_title('Where the 10M decisions were spent (mean of 2 seeds)',fontsize=12,weight='bold')
ax.yaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x/1e3:,.0f}k'))
ax.grid(axis='y',alpha=.15)
ax.set_axisbelow(True)
ax.legend(ncol=2,fontsize=8.5,loc='upper right',frameon=False)
ax.spines[['top','right']].set_visible(False)
for ext in ('png','pdf'):
 fig.savefig(ROOT/f'd234_stage_decomposition.{ext}',dpi=190,bbox_inches='tight')
plt.close(fig)
print('FIGURES GENERATED, no endpoint-interpolated curves')
