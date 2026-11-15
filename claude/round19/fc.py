import json,datetime as dt,numpy as np
S=json.load(open('series.json'))
EOLS={'2022Q1':33.91,'2022Q2':37.16,'2022Q3':33.9,'2022Q4':43.65,'2023Q1':41.72,'2023Q2':49.35,'2023Q3':50.02,'2023Q4':61.0,'2024Q1':59.33,'2024Q2':66.91,'2024Q3':61.09,'2024Q4':78.95,
'2025Q1':68.52,'2025Q2':69.39,'2025Q3':68.97,'2025Q4':90.3,'2026Q1':73.14,'2026Q2':84.1,'2026Q3':78.0}
def qk(d):
  d=dt.date.fromisoformat(d)+dt.timedelta(days=3);return f"{d.year}Q{(d.month-1)//3+1}"
def quarters(dates,v):
  q={}
  for d,x in zip(dates,v): q.setdefault(qk(d),[]).append(x or 0)
  return {k:np.mean(x) for k,x in q.items() if len(x)>=12 or k=='2026Q4'}
def prev(k,n=4):
  y,q=int(k[:4]),int(k[-1]);i=y*4+q-1-n;return f"{i//4}Q{i%4+1}"
def yoy(d,k): p=prev(k);return d[k]/d[p]-1 if p in d and d[p]>0 else None
T=[k for k in EOLS if k>='2023Q1']
R={k:yoy(EOLS,k) for k in T}
train=[k for k in T if k<='2025Q2'];test=[k for k in T if k>'2025Q2']
res=[]
for t,(dates,v) in S.items():
  Q=quarters(dates,v)
  for L in (0,1):
    xs=lambda ks:[yoy(Q,prev(k,L)) if L else yoy(Q,k) for k in ks]
    xtr=xs(train);xte=xs(test)
    if None in xtr+xte: continue
    rtr=[R[k] for k in train];rte=[R[k] for k in test]
    c=np.corrcoef(xtr,rtr)[0,1]
    if np.isnan(c): continue
    b,a=np.polyfit(xtr,rtr,1);pred=[a+b*x for x in xte]
    mae=np.mean([abs(p-r) for p,r in zip(pred,rte)])
    call=np.corrcoef(xtr+xte,rtr+rte)[0,1]
    # direction of change in growth (accelerating vs slowing) on test
    res.append(dict(t=t,L=L,ctrain=round(c,2),call=round(call,2),mae=round(100*mae,1),pred=[round(100*p,1) for p in pred]))
naive=np.mean([abs(R[k]-R[prev(k,1)]) for k in test]);mean_tr=np.mean([R[k] for k in train])
print('test actual',[round(100*R[k],1) for k in test],'naive(last q) MAE %.1f'%(100*naive),'train-mean MAE %.1f'%(100*np.mean([abs(R[k]-mean_tr) for k in test])))
res.sort(key=lambda r:-r['ctrain'])
for r in res[:20]: print(r)
print('--- best on all data')
for r in sorted(res,key=lambda r:-r['call'])[:12]: print(r['t'],r['L'],r['call'],r['ctrain'],r['mae'])
json.dump(res,open('res.json','w'))
