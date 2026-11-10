import json, re, collections, itertools, statistics as st
from deep import *
HEDGE=re.compile(r"var(y|ies) by (location|store|region|market|state)|check (with )?(your )?local|call (ahead|your local)|store locator|individual (store|location)|local store|confirm (with|hours|before)|may (vary|differ)|hours may|it is (best|recommended)|recommended to (check|call|verify)|before (heading|visiting|going)", re.I)
def verdict(r):
    t=(r["text"] or "").strip().lower()
    first=re.split(r"(?<=[.!?])\s",t)[0] if t else ""
    k=r["kw"].lower()
    if not re.match(r"(is|are|does|will|\w+ (open|closed) on)", k): return None
    op= bool(re.search(r"\b(is|are|will be|remain|stay) (?:\w+ ){0,3}open\b|\bopen (on|for|regular|normal|limited|reduced|easter)|\byes\b", first))
    cl= bool(re.search(r"\bclosed\b|\bwill close\b|\bnot open\b|\bno,", first))
    mx= bool(re.search(r"\bmost\b|\bsome\b|\bmany\b|\bselect\b|\bvar(y|ies)\b|\blimited\b|\breduced\b|\bdepend", first))
    if op and cl: return "mixed"
    if cl: return "closed"
    if op: return "open (limited)" if mx else "open"
    return "unclear"
rows=[]
for r in L:
    b=brand_of(r["kw"]); slug=BR.get(b) if b else None
    own_this = bool(slug) and any(slug.replace(".","") in norm(d).replace(".","") for d in r["ref_dom"])
    serp=set(r["serp_dom"]); notin=[d for d in r["ref_dom"] if d not in serp]
    rows.append(dict(kw=r["kw"],day=r["day"],brand=b,own=own_this,hedge=bool(HEDGE.search(r["text"] or "")),verdict=verdict(r),
        notin=len(notin),nref=len(r["ref_dom"]),fid=r.get("fid"),labels=r.get("labels"),bad=r.get("bad_claims"),first=(r["text"] or "")[:220]))
json.dump(rows,open("local_rows.json","w"))
br=[x for x in rows if x["brand"] and x["brand"] not in ("banks",)]
print("brand-specific answers",len(br),"citing that brand's own site",sum(x["own"] for x in br), round(sum(x["own"] for x in br)/len(br)*100,1))
print("hedge rate local",round(sum(x["hedge"] for x in rows)/len(rows)*100,1),"| control",round(sum(1 for r in C if HEDGE.search(r["text"] or ""))/len(C)*100,1))
def notin_rate(rs): 
    a=sum(1 for r in rs for d in r["ref_dom"] if d not in set(r["serp_dom"])); b=sum(len(r["ref_dom"]) for r in rs); return round(a/b*100,1)
print("cited domains not on page-1 SERP: local",notin_rate(L),"control",notin_rate(C))
# own site in serp but not cited?
own_in_serp=0;own_cited=0;n=0
for r in L:
    b=brand_of(r["kw"]); slug=BR.get(b) if b else None
    if not slug or b=="banks": continue
    n+=1; s=slug.replace(".","")
    ins=any(s in norm(d).replace(".","") for d in r["serp_dom"]); c=any(s in norm(d).replace(".","") for d in r["ref_dom"])
    own_in_serp+=ins; own_cited+=c
print("brand answers",n,"own site on SERP page",own_in_serp,"cited",own_cited)
# verdicts per brand
vb=collections.defaultdict(list)
for x in br:
    if x["verdict"] and "easter" in x["kw"].lower(): vb[x["brand"]].append((x["verdict"],x["kw"],x["day"]))
conf={b:v for b,v in vb.items() if len({a for a,_,_ in v if a not in("unclear",)})>1}
print("brands with Easter verdicts",len(vb),"with conflicting verdicts",len(conf))
for b,v in sorted(vb.items(), key=lambda kv:-len(kv[1])): print(" ",b,collections.Counter(a for a,_,_ in v))
print(json.dumps({b:v for b,v in list(conf.items())[:6]},indent=0)[:3000])
