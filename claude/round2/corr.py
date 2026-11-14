from states import *
from scipy import stats
sets=dict(hinge=hinge,tinder=tinder,pizza=pizza)
for drop in ([],['WY']):
  st=[s for s in hinge if s not in drop]
  for a in ('hinge','tinder','pizza'):
    for b,bd in (('lip',lip),('botox',botox)):
      x=[sets[a][s] for s in st]; y=[bd[s] for s in st]
      r,p=stats.pearsonr(x,y); rs,ps=stats.spearmanr(x,y)
      print(f"drop={drop} {a} vs {b}: n={len(st)} pearson r={r:.2f} p={p:.3f} spearman={rs:.2f} p={ps:.3f}")
