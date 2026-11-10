import json, re, collections, statistics as st
from deep import *
from analyze import cls
out={}
# activation by category
q=json.load(open("../imc_queries.json"))
c=collections.defaultdict(lambda:[0,0])
for kw,cat_,aio,_ in q:
    k="local" if (kw and cls(kw)) else cat_
    c[k][1]+=1; c[k][0]+=1 if aio else 0
out["act_cat"]=sorted([[k,v[0],v[1],round(v[0]/v[1]*100,1)] for k,v in c.items()],key=lambda x:-x[3])
# per-brand rank vs cited
pb=collections.defaultdict(lambda:[0,0,0])
for r in L:
    b=brand_of(r["kw"]); s=BR.get(b) if b else None
    if not s or b=="banks": continue
    s=s.replace(".","")
    pb[b][0]+=1; pb[b][1]+=any(s in norm(d).replace(".","") for d in r["serp_dom"]); pb[b][2]+=any(s in norm(d).replace(".","") for d in r["ref_dom"])
out["brand_rank_cite"]=sorted([[b,v[0],v[1],v[2]] for b,v in pb.items() if v[0]>=3],key=lambda x:-x[1])
# query type x source
def qtype(k):
    k=k.lower(); b=brand_of(k)
    if b in("banks","post office","usps") or re.search(r"bank|post office|usps",k): return "Banks and post offices"
    if not b: return "Generic (what's open)"
    if re.search(r"\bhours\b|what time",k): return "Brand hours"
    return "Brand yes/no (is X open)"
qt=collections.defaultdict(list)
for r in L: qt[qtype(r["kw"])].append(r)
out["qtype"]={k:dict(n=len(v),**mix(v)[0]) for k,v in qt.items()}
# lift
ml,_=mix(L); mc,_=mix(C)
out["lift"]={k:[ml[k],mc[k],round(ml[k]/mc[k],1) if mc[k] else None] for k in CATS}
# refs per answer histogram
def hist(rs):
    h=collections.Counter(min(len(r["ref_dom"]),15) for r in rs); n=len(rs); return {i:round(h[i]/n*100,1) for i in range(0,16)}
out["refs_hist"]={"local":hist(L),"control":hist(C)}
# outside page one by source group
def outside(rs):
    a=collections.Counter(); t=collections.Counter()
    for r in rs:
        s=set(r["serp_dom"])
        for d in r["ref_dom"]:
            k=cat(d); t[k]+=1; a[k]+= d not in s
    return {k:round(a[k]/t[k]*100,1) for k in CATS if t[k]}
out["outside"]=outside(L)
# timeline
q2=collections.Counter(x[3].split("/")[1][:28] if False else None for x in q)
days=collections.Counter()
for kw,cat_,aio,root in q:
    if kw and cls(kw):
        m=re.search(r"2026-\d\d-\d\d",root); days[m.group(0)]+=1
out["days_exec"]=sorted(days.items())
# top domains with group
out["top_dom"]=[[d,n,cat(d)] for d,n in collections.Counter(d for r in L for d in set(r["ref_dom"])).most_common(20)]
# Gannett distinct domains count in local
out["gannett_domains"]=len({d for r in L for d in r["ref_dom"] if cat(d)=="Gannett papers"})
out["tegna_domains"]=len({d for r in L for d in r["ref_dom"] if cat(d)=="TEGNA TV"})
json.dump(out,open("extra.json","w"),indent=1)
for k,v in out.items(): print(k, json.dumps(v)[:700])
