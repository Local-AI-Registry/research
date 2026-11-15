import json,glob
W=json.load(open('/home/claude/work/r14/all.json'))['W']
S={k:(v['dates'],v['v']) for k,v in W.items()}
new=[]
for f in glob.glob('/tmp/claude-tool-results/224b16ac-3afb-5c52-a482-4571800d37ac/*.json'):
  try:
    raw=json.load(open(f));raw=json.loads(raw[0]['text']) if isinstance(raw,list) else raw
  except Exception: continue
  for it in (raw.get('items') or []):
    if it.get('type')=='google_trends_graph' and len(it['keywords'])==1:
      kw=it['keywords'][0]; d=it['data']
      if d[0]['date_from']=='2021-11-14' and kw not in S:
        S[kw]=([x['date_from'] for x in d],[x['values'][0] if x['values'][0] is not None else 0 for x in d]);new.append(kw)
json.dump(S,open('series.json','w'))
print(len(S),new)
