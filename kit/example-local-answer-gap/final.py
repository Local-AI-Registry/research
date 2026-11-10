import json, re, collections, glob, statistics as st, itertools
import pandas as pd
from deep import *
from deep2 import HEDGE, rows as lrows
from deep3 import NAT, CITY
# brand heatmap
bc=collections.defaultdict(list)
for r in L:
    b=brand_of(r["kw"])
    if b and b!="banks": bc[b].append(r)
top=sorted(bc,key=lambda b:-len(bc[b]))[:12]
heat=[]
for b in top:
    c=collections.Counter(cat(d) for r in bc[b] for d in r["ref_dom"]); n=sum(c.values())
    s=BR[b].replace(".","")
    ownr=sum(1 for r in bc[b] if any(s in norm(d).replace(".","") for d in r["ref_dom"]))
    heat.append(dict(brand=b,n=len(bc[b]),cites=n,own_answers=round(ownr/len(bc[b])*100),**{k:round(c[k]/n*100,1) for k in CATS}))
# generic (no brand) local answers
gen=[r for r in L if not brand_of(r["kw"]) or brand_of(r["kw"])=="banks"]
c=collections.Counter(cat(d) for r in gen for d in r["ref_dom"]); n=sum(c.values())
heat.append(dict(brand="no brand named",n=len(gen),cites=n,own_answers=None,**{k:round(c[k]/n*100,1) for k in CATS}))
# blind spot census
LOCALB=re.compile(r"near me|nearby|\b(?:plumber|dentist|med ?spa|salon|lawyer|attorney|contractor|restaurant|clinic|chiropractor|therapist|therapy|vet|mechanic|roofer|electrician|hvac|gym|barber|florist|dispensar\w*|bakery|cafe|coffee shop|hotel)s? (?:in|near) |best (?:\w+ ){0,3}in [A-Z]", re.I)
census=[]
for f in sorted(glob.glob("/home/claude/danishashko/ai-search-datasets/*/*.csv")):
    df=pd.read_csv(f,low_memory=False); col=[c for c in df.columns if c in("query","prompt","user_prompt","keyword")]
    if not col: continue
    q=df[col[0]].dropna().astype(str).str.strip().str.lower().drop_duplicates()
    m=q[q.str.contains(LOCALB)]
    census.append(("Organikpi "+f.split("/")[-2], len(q), int(len(m)), m.tolist()))
cp=pd.read_csv("/home/claude/Cited-io/ai-search-citations-dataset/data/2026-10/prompts.csv"); 
qcol=[c for c in cp.columns if "prompt" in c.lower()][0]; cq=cp[qcol].dropna().astype(str).str.lower().drop_duplicates()
census.append(("Cited.io 2026-10",len(cq),int(cq.str.contains(LOCALB).sum()),cq[cq.str.contains(LOCALB)].tolist()))
imcq=json.load(open("../imc_queries.json")); iq={x[0].lower() for x in imcq if x[0]}
from analyze import cls
census.append(("IMC 2026 Google AIO", len(iq), sum(1 for k in iq if cls(k)), ["chain store hours, closures"]))
# dedupe organikpi duplicates (answers.csv & fanout pairs share queries) -> keep max per folder
agg=collections.OrderedDict()
for name,n,m,ex in census:
    if name not in agg or agg[name][0]<n: agg[name]=(n,m,ex)
tot=sum(v[0] for v in agg.values()); loc=sum(v[1] for v in agg.values())
print("census", {k:(v[0],v[1],v[2][:4]) for k,v in agg.items()}); print("TOTAL unique",tot,"local",loc)
# figures
lq=[x for x in imcq if x[0] and cls(x[0])]; QF=re.compile(r"^(is|are|what|whats|what's|does|do|how|when|where|will|can|why|who)\b", re.I)
qf=[x for x in imcq if x[0] and QF.search(x[0]) and not cls(x[0])]
labs=lambda rs: (lambda c: {k: round(c[k]/sum(c.values())*100,2) for k in ["CLEAR","VAGUE","AMBIGUOUS","INCORRECT","OMITTED"]})(sum((collections.Counter(r.get("labels") or {}) for r in rs), collections.Counter()))
ml,nl=mix(L); mc,nc=mix(C)
answers_citing={k: round(sum(1 for r in L if any(cat(d)==k for d in r["ref_dom"]))/len(L)*100,1) for k in CATS}
answers_citing_c={k: round(sum(1 for r in C if any(cat(d)==k for d in r["ref_dom"]))/len(C)*100,1) for k in CATS}
pages=json.load(open("pages.json")); fp=json.load(open("fp.json"))
def jac(a,b): a,b=set(a),set(b); return len(a&b)/len(a|b) if a|b else 1
bd=collections.defaultdict(list)
for r in L:
    b=brand_of(r["kw"])
    if b and "easter" in r["kw"].lower(): bd[(b,r["day"])].append(r)
js=[jac(x["ref_dom"],y["ref_dom"]) for v in bd.values() if len(v)>1 for x,y in itertools.combinations(v,2)]
g=collections.defaultdict(list)
for r in L: g[r["kw"].lower()].append(r)
jr=[jac(x["ref_dom"],y["ref_dom"]) for v in g.values() if len(v)>1 for x,y in itertools.combinations(v,2)]
gc=collections.defaultdict(list)
for r in C: gc[r["kw"].lower()].append(r)
jc=[jac(x["ref_dom"],y["ref_dom"]) for v in gc.values() if len(v)>1 for x,y in itertools.combinations(v,2)]
brand_ans=[x for x in lrows if x["brand"] and x["brand"]!="banks"]
own_serp=0
for r in L:
    b=brand_of(r["kw"]); s=BR.get(b) if b else None
    if s and b!="banks" and any(s.replace(".","") in norm(d).replace(".","") for d in r["serp_dom"]): own_serp+=1
out=dict(
 n_local=len(L), n_local_unique=len({r['kw'].lower() for r in L}), n_control=len(C), n_all=len(L)+len(C),
 n_exec=len(imcq), act_local=[sum(1 for x in lq if x[2]),len(lq)], act_all=[sum(1 for x in imcq if x[2]),len(imcq)], act_qf=[sum(1 for x in qf if x[2]),len(qf)],
 labels_local=labs(L), labels_control=labs(C), mix_local=ml, mix_control=mc, ncite_local=nl, ncite_control=nc,
 answers_citing=answers_citing, answers_citing_c=answers_citing_c, brand_heat=heat, pages=pages, fp=fp,
 brand_answers=len(brand_ans), own_cited=sum(x["own"] for x in brand_ans), own_on_serp=own_serp,
 hedge_local=round(sum(x["hedge"] for x in lrows)/len(lrows)*100,1), hedge_control=round(sum(1 for r in C if HEDGE.search(r["text"] or ""))/len(C)*100,1),
 national=round(sum(1 for r in L if NAT.search(r["text"] or ""))/len(L)*100,1), national_n=sum(1 for r in L if NAT.search(r["text"] or "")), address_n=sum(1 for r in L if CITY.search(r["text"] or "")),
 jac_phrasing=[round(st.mean(js),3),len(js)], jac_repeat_local=[round(st.mean(jr),3),len(jr)], jac_repeat_control=[round(st.mean(jc),3),len(jc)],
 days=sorted(collections.Counter(r["day"] for r in L).items()),
 census=[[k,v[0],v[1],v[2][:6]] for k,v in agg.items()], census_total=[tot,loc],
 refs_local=round(st.mean(len(r["ref_dom"]) for r in L),2), refs_control=round(st.mean(len(r["ref_dom"]) for r in C),2),
 top_domains=collections.Counter(d for r in L for d in set(r["ref_dom"])).most_common(15))
json.dump(out,open("findings.json","w"),indent=1)
print(json.dumps({k:v for k,v in out.items() if k not in("brand_heat","census","days","top_domains")},indent=0)[:3000])
for h in heat: print(h)
