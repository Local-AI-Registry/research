import json, re, collections, itertools, statistics as st
from classify import lclass
recs = json.load(open("aio_records.json"))
DROP = re.compile(r"market|school|cori close|valero|protest|no king|power outage|weather", re.I)
def cls(k):
    c = lclass(k)
    if not c or DROP.search(k or ""): return None
    return "local"
for r in recs: r["L"] = cls(r["kw"])
L = [r for r in recs if r["L"]]; C = [r for r in recs if not r["L"]]
print("local AIO executions", len(L), "unique", len({r['kw'].lower() for r in L}), "control", len(C))
# activation
q = json.load(open("../imc_queries.json"))
lq = [x for x in q if x[0] and cls(x[0])]
print("activation local", sum(1 for x in lq if x[2]), "/", len(lq), "| all", sum(1 for x in q if x[2]), "/", len(q))
# labels
def labshare(rs):
    c = collections.Counter()
    for r in rs:
        for k, v in (r.get("labels") or {}).items(): c[k] += v
    t = sum(c.values()); return {k: round(v / t * 100, 2) for k, v in c.items()}, t
print("labels local", labshare(L)); print("labels control", labshare(C))
# question-form control for activation
QF = re.compile(r"^(is|are|what|whats|what's|does|do|how|when|where|will|can|why|who)\b", re.I)
qf = [x for x in q if x[0] and QF.search(x[0]) and not cls(x[0])]
print("activation question-form non-local", sum(1 for x in qf if x[2]), "/", len(qf))
# top domains
cl = collections.Counter(d for r in L for d in set(r["ref_dom"]))
print("top local cited domains (answers citing):", cl.most_common(45))
print("refs per answer local", round(st.mean(len(r["ref_dom"]) for r in L), 2), "control", round(st.mean(len(r["ref_dom"]) for r in C), 2))
