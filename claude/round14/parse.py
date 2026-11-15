import json,glob,collections
W={}; DATES=None; MAPS={}
for f in sorted(glob.glob('raw/*.txt')):
    d=json.load(open(f))
    for it in d['items']:
        if it['type']=='google_trends_graph':
            ks=it['keywords']; rows=[r for r in it['data'] if not r.get('missing_data')]
            dates=[r['date_from'] for r in rows]
            if DATES is None: DATES=dates
            for j,k in enumerate(ks):
                s=[]
                for r in rows:
                    v=r.get('values')
                    if isinstance(v,dict): x=v.get(str(j))
                    elif isinstance(v,list): x=v[j] if j<len(v) else None
                    else: x=None
                    s.append(x)
                W[k]=dict(dates=dates,v=s)
        elif it['type']=='google_trends_map' and len(it['keywords'])==1:
            k=it['keywords'][0]
            MAPS[k]={r['geo_id'][3:]:r['values'][0] for r in it['data'] if r.get('values')}
json.dump({'W':W,'MAPS':MAPS},open('all.json','w'))
print(len(W),'series',len(MAPS),'maps')
for k,s in W.items():
    v=[x for x in s['v'] if x is not None]
    print(f"{k:22s} n={len(s['v'])} max={max(v)} mean={sum(v)/len(v):.1f} first={s['dates'][0]} last={s['dates'][-1]}")
