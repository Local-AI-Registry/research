import json, re, collections, itertools, statistics as st, glob
import pandas as pd
from deep import *
NAT=re.compile(r"\ball (?:u\.?s\.? |of its |its |\w+ )?(?:locations|stores|warehouses|restaurants|branches)|\bnationwide\b|\bmost (?:\w+ )?(?:locations|stores|restaurants|branches)|\bmany (?:\w+ )?(?:locations|stores|restaurants)|\bin the united states\b|\bu\.s\. locations", re.I)
CITY=re.compile(r"\b\d{2,5} [A-Z][a-z]+ (?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Dr|Drive|Pkwy|Hwy)\b|\(\d{3}\) ?\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b")
nat=sum(1 for r in L if NAT.search(r["text"] or "")); addr=sum(1 for r in L if CITY.search(r["text"] or ""))
print("national framing",nat,len(L),round(nat/len(L)*100,1),"| specific address/phone",addr)
def uns(rs):
    c=collections.Counter()
    for r in rs:
        for k,v in (r.get("labels") or {}).items(): c[k]+=v
    t=sum(c.values()); return round((c["INCORRECT"]+c["OMITTED"]+c["AMBIGUOUS"])/t*100,2), t, dict(c)
print("unsupported local",uns(L)); print("unsupported control",uns(C)); print("unsupported all",uns(L+C))
# cross-day stability of cited domains for repeated identical keywords
g=collections.defaultdict(list)
for r in L: g[r["kw"].lower()].append(r)
for r in C: g[("C",r["kw"].lower())].append(r) if False else None
def jac(a,b): a,b=set(a),set(b); return len(a&b)/len(a|b) if a|b else 1
def pairs(rs):
    gg=collections.defaultdict(list)
    for r in rs: gg[r["kw"].lower()].append(r)
    js=[jac(x["ref_dom"],y["ref_dom"]) for v in gg.values() if len(v)>1 for x,y in itertools.combinations(v,2)]
    return round(st.mean(js),3) if js else None, len(js)
print("repeat-query domain jaccard local",pairs(L),"control",pairs(C))
# phrasing variants same brand same day: jaccard
bd=collections.defaultdict(list)
for r in L:
    b=brand_of(r["kw"]); 
    if b and "easter" in r["kw"].lower(): bd[(b,r["day"])].append(r)
js=[jac(x["ref_dom"],y["ref_dom"]) for v in bd.values() if len(v)>1 for x,y in itertools.combinations(v,2)]
print("same brand same day different phrasing jaccard",round(st.mean(js),3),len(js))
# failed claims
bad=[(l,c,r["kw"]) for r in L for (l,c) in (r.get("bad_claims") or []) if l in("INCORRECT","OMITTED")]
print("failed local claims",len(bad)); 
for b in bad[:40]: print(" ",b)
# per-day counts
print(sorted(collections.Counter(r["day"] for r in L).items()))
