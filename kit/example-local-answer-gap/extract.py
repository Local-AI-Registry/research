import os, json, re, sys
from urllib.parse import urlparse
R = sys.argv[1]
def dom(u):
    try:
        h = urlparse(u).netloc.lower()
        return h[4:] if h.startswith("www.") else h
    except Exception: return ""
out = []
for root, dirs, files in os.walk(os.path.join(R, "aio_results")):
    if "result.json" not in files: continue
    try: d = json.load(open(os.path.join(root, "result.json")))
    except Exception: continue
    if not d.get("aioExists"): continue
    parts = root.split(os.sep)
    i = parts.index("aio_results")
    day = re.search(r"2026-\d\d-\d\d", parts[i+1]).group(0)
    cat = re.search(r"trending_US_1d_([a-z_]+)_2026", parts[i+2]).group(1)
    ao = d.get("aiOverview") or {}
    refs = ao.get("references") or []
    serp = d.get("serpLinksDedup") or []
    serp_urls = [s if isinstance(s, str) else (s.get("url") or s.get("link") or "") for s in serp]
    rec = {"kw": d.get("keyword"), "cat": cat, "day": day, "path": os.path.relpath(root, R),
           "text": (ao.get("content") or "")[:4000],
           "ref_urls": [r.get("url", "") for r in refs], "ref_dom": [dom(r.get("url", "")) for r in refs],
           "serp_dom": [dom(u) for u in serp_urls if u]}
    vf = [f for f in files if f.startswith("verification_result")]
    if vf:
        try:
            v = json.load(open(os.path.join(root, vf[0])))
            rec["labels"] = v.get("label_counts"); rec["fid"] = v.get("fidelity_rate"); rec["n_claims"] = v.get("n_claims")
            rec["bad_claims"] = [(x.get("label"), x.get("claim")) for x in v.get("verifications", []) if x.get("label") in ("INCORRECT", "OMITTED", "AMBIGUOUS")][:6]
        except Exception: pass
    out.append(rec)
json.dump(out, open("aio_records.json", "w"))
print(len(out), "AIO records;", sum(1 for r in out if r.get("labels")), "with verification")
