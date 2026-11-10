import json, re, collections, statistics as st, os
from deep import *
R="/home/claude/haofeix/google-aio-characterization/raw"
FP=re.compile(r"store locator|the \w+(?:'s)? app\b|official (?:website|site|holiday schedule)|website (?:indicates|lists|states|shows)|according to (?:\w+(?:'s)? )?(?:official|website|corporate)|corporate (?:website|site)|\.com (?:indicates|lists|states)", re.I)
def allclaims(rs):
    out=[]
    for r in rs:
        root=os.path.join(R,r["path"]); vf=[f for f in os.listdir(root) if f.startswith("verification_result")]
        if not vf: continue
        v=json.load(open(os.path.join(root,vf[0])))
        for x in v.get("verifications",[]): out.append((x.get("label"),x.get("claim") or "",r))
    return out
cl=allclaims(L); cc=allclaims(C)
def fp_stats(cs):
    f=[c for c in cs if FP.search(c[1])]; bad=[c for c in f if c[0] in("INCORRECT","OMITTED","AMBIGUOUS")]
    return len(f), len(bad), round(len(bad)/len(f)*100,1) if f else None
print("first-party attributed claims local (n, unsupported, %)", fp_stats(cl)); print("control", fp_stats(cc))
other=[c for c in cl if not FP.search(c[1])]; ob=[c for c in other if c[0] in("INCORRECT","OMITTED","AMBIGUOUS")]
print("non-attributed local claims", len(other), len(ob), round(len(ob)/len(other)*100,1))
for c in [c for c in cl if FP.search(c[1]) and c[0] in("INCORRECT","OMITTED")][:25]: print("  ",c[0],"|",c[1][:120],"|",c[2]["kw"])
# own-site cited vs not -> unsupported rate (brand-specific answers)
def uns_r(rs):
    c=collections.Counter()
    for r in rs:
        for k,v in (r.get("labels") or {}).items(): c[k]+=v
    t=sum(c.values()); return round((c["INCORRECT"]+c["OMITTED"]+c["AMBIGUOUS"])/t*100,2) if t else None, len(rs), t
ow=[];no=[]
for r in L:
    b=brand_of(r["kw"]); s=BR.get(b) if b else None
    if not s or b=="banks": continue
    (ow if any(s.replace(".","") in norm(d).replace(".","") for d in r["ref_dom"]) else no).append(r)
print("unsupported when own site cited",uns_r(ow),"not cited",uns_r(no))
json.dump({"fp_local":fp_stats(cl),"fp_control":fp_stats(cc),"nonfp_local":[len(other),len(ob)],"own":uns_r(ow),"noown":uns_r(no)},open("fp.json","w"))
