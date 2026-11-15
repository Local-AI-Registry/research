import datetime as dt, json
from data import *
from scipy.stats import pearsonr, spearmanr
for n,a in [('b',BOTOX),('c',CLUBP),('j',JEUV)]: print(n,len(a))
start=dt.date(2022,12,25)
def quarters(a):
  q={}
  for i,v in enumerate(a):
    d=start+dt.timedelta(days=7*i+3); k=f"{d.year}Q{(d.month-1)//3+1}"; q.setdefault(k,[]).append(v)
  return {k:sum(v)/len(v) for k,v in q.items()}
QB,QC,QJ=quarters(BOTOX),quarters(CLUBP),quarters(JEUV)
ks=sorted(ABBV)
def yoy(d,k):
  y,q=k.split('Q'); p=f"{int(y)-1}Q{q}"; return d[k]/d[p]-1 if p in d else None
out={}
for name,S,R in [('botox',QB,ABBV),('jeuveau',QJ,EOLS)]:
  x=[S[k] for k in ks]; y=[R[k] for k in ks]
  r,p=pearsonr(x,y)
  yk=[k for k in ks if yoy(R,k) is not None]
  gx=[yoy(S,k) for k in yk]; gy=[yoy(R,k) for k in yk]
  r2,p2=pearsonr(gx,gy)
  same=sum((a>0)==(b>0) for a,b in zip(gx,gy))
  print(name,'level r=%.2f p=%.3f'%(r,p),'yoy r=%.2f p=%.3f'%(r2,p2),'direction match %d/%d'%(same,len(yk)))
  for k in ks: print(' ',k,round(S[k],1),R[k], '' if yoy(R,k) is None else '%+.1f%% / %+.1f%%'%(100*yoy(S,k),100*yoy(R,k)))
  out[name]={'q':ks,'search':[round(S[k],1) for k in ks],'rev':[R[k] for k in ks],'r_level':round(r,2),'p_level':round(p,3),'r_yoy':round(r2,2),'p_yoy':round(p2,3),'dir':[same,len(yk)],
    'yoy':{k:[round(100*yoy(S,k),1),round(100*yoy(R,k),1)] for k in yk}}
print('clubp', {k:round(QC[k],1) for k in ks}, 'Q3 yoy %+.1f%%'%(100*yoy(QC,'2026Q3')), 'Q2 yoy %+.1f%%'%(100*yoy(QC,'2026Q2')))
out['clubp']={k:round(QC[k],2) for k in ks}
json.dump(out,open('r17.json','w'),indent=1)
