import json, numpy as np, datetime as dt
from scipy import stats
def load(f):
    d=json.loads(json.load(open(f))[0]['text'])['items'][0]
    rows=[r for r in d['data'] if not r.get('missing_data')]
    dates=[dt.date.fromisoformat(r['date_from']) for r in rows]
    return d['keywords'], dates, np.array([r['values'] for r in rows],float)
def xcorr(name,a,b,dates,excl_vday=True):
    da,db=np.diff(a),np.diff(b); dd=dates[1:]
    keep=np.array([not(excl_vday and ((d.month==2 and d.day<=24) or (d.month==1 and d.day>=25))) for d in dd])
    out=[]
    for k in range(-4,5):
        if k>=0: x,y,m=da[:len(da)-k],db[k:],keep[k:]&keep[:len(keep)-k]
        else: x,y,m=da[-k:],db[:len(db)+k],keep[-k:]&keep[:len(keep)+k]
        r,p=stats.pearsonr(x[m],y[m]); out.append((k,round(r,3),round(p,4)))
    print(name,"(lag k: app change at week t vs restaurant change at week t+k)")
    for o in out: print("  ",o)
kw,dates,v=load('trio.json'); print(kw, len(dates), dates[0], dates[-1])
print("levels r hinge vs datenight", stats.pearsonr(v[:,0],v[:,1])[0], "hinge vs romantic", stats.pearsonr(v[:,0],v[:,2])[0])
xcorr("hinge app -> date night restaurant",v[:,0],v[:,1],dates)
xcorr("hinge app -> romantic restaurant",v[:,0],v[:,2],dates)
xcorr("hinge app -> date night (incl Valentine)",v[:,0],v[:,1],dates,False)
kw2,d2,v2=load('quad.json'); print(kw2)
xcorr("tinder -> date night",v2[:,1],v2[:,3],d2)
# yearly pattern: average by month, hinge app and date night
import collections
for i,n in ((0,'hinge app'),(1,'date night rest'),(2,'romantic rest')):
    m=collections.defaultdict(list)
    for d,x in zip(dates,v[:,i]):
        if d.year in (2022,2023,2024): m[d.month].append(x)
    print(n,{k:round(np.mean(m[k]),1) for k in sorted(m)})
