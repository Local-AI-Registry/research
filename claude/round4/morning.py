import json, datetime as dt, numpy as np
def load(f):
    d=json.loads(json.load(open(f))[0]['text']); it=d['items'][0]
    rows=[r for r in it['data'] if r.get('values') and not r.get('missing_data')]
    return d['id'], it['keywords'], [dt.date.fromisoformat(r['date_from']) for r in rows], rows
def series(rows,i): return [ (r['values'][i] if i<len(r['values']) else None) for r in rows]
def ratio(dates,vals,day):
    idx=[k for k,d in enumerate(dates) if d<=day<d+dt.timedelta(7)]
    if not idx: return None
    k=idx[0]; base=[vals[j] for j in list(range(k-4,k-1))+list(range(k+2,k+5)) if 0<=j<len(vals) and vals[j] is not None]
    if len(base)<4 or not vals[k]: return None
    return round(vals[k]/np.mean(base),2), vals[k], round(np.mean(base),1)
D=dt.date
events={
 'St Patrick morning (Mar 18)':[D(y,3,18) for y in (2022,2023,2024,2025,2026)],
 'New Year morning (Jan 1)':[D(y,1,1) for y in (2022,2023,2024,2025,2026)],
 'Super Bowl Monday':[D(2022,2,14),D(2023,2,13),D(2024,2,12),D(2025,2,10),D(2026,2,9)],
 'Day after Halloween (Nov 1)':[D(y,11,1) for y in (2022,2023,2024,2025)],
 'Thanksgiving week':[D(2021,11,25),D(2022,11,24),D(2023,11,23),D(2024,11,28),D(2025,11,27)],
 'July 5':[D(y,7,5) for y in (2022,2023,2024,2025,2026)],
 'Second week of January':[D(y,1,8) for y in (2022,2023,2024,2025,2026)],
}
plan=[('iv.json',0,['St Patrick morning (Mar 18)','New Year morning (Jan 1)','Super Bowl Monday','Day after Halloween (Nov 1)','Thanksgiving week']),
      ('iv.json',1,['St Patrick morning (Mar 18)','New Year morning (Jan 1)','Super Bowl Monday']),
      ('dent.json',0,['Day after Halloween (Nov 1)','Thanksgiving week']),
      ('dent.json',2,['Day after Halloween (Nov 1)']),
      ('plumb.json',0,['Thanksgiving week','New Year morning (Jan 1)']),
      ('plumb.json',1,['Thanksgiving week']),
      ('urgent.json',0,['July 5','New Year morning (Jan 1)']),
      ('urgent.json',1,['July 5']),
      ('divorce.json',0,['Second week of January']),
      ('divorce.json',1,['Second week of January']),
      ('divorce.json',2,['Second week of January'])]
for f,i,evs in plan:
    tid,kw,dates,rows=load(f); vals=series(rows,i)
    print(f"{kw[i]}  [{tid}]")
    for e in evs:
        rs=[ratio(dates,vals,d) for d in events[e]]
        print(f"   {e}: "+"  ".join(f"{d.year}:{r[0]}x" if r else f"{d.year}:na" for d,r in zip(events[e],rs)))
