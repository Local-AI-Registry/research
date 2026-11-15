import json,numpy as np
exec(open('fc.py').read().split('res=[]')[0])
out=[]
for t,(dates,v) in S.items():
  Q=quarters(dates,v)
  for L in (0,1):
    g={k:(yoy(Q,prev(k,L)) if L else yoy(Q,k)) for k in T}
    if None in g.values(): continue
    x=[g[k] for k in T];y=[R[k] for k in T]
    dx=np.diff(x);dy=np.diff(y)
    c=np.corrcoef(x,y)[0,1];cd=np.corrcoef(dx,dy)[0,1]
    hit=sum((a>0)==(b>0) for a,b in zip(dx,dy))
    out.append((t,L,round(c,2),round(cd,2),hit))
out.sort(key=lambda r:-abs(r[3]))
for r in out[:25]: print(r)
print('n changes',len(T)-1)
for r in out:
  if r[0] in('equinox','sephora','taylor swift','wingstop','botox near me','planet fitness'): print('SEL',r)
json.dump(out,open('strict.json','w'))
