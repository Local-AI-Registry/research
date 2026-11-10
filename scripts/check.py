"""Fail loudly if the built site is broken. Run after the build scripts."""
import os, re, json, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []
pages = []
for d, _, fs in os.walk(ROOT):
    if "/.git" in d: continue
    pages += [os.path.join(d, f) for f in fs if f.endswith(".html")]
for p in pages:
    s = open(p, encoding="utf-8").read(); rel = os.path.relpath(p, ROOT)
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(b)
        except Exception as e: errors.append(f"{rel}: structured data is not valid JSON ({e})")
    for u in re.findall(r'(?:href|src)="(/research/[^"#?]*)', s):
        path = os.path.join(ROOT, u[len("/research/"):])
        if u.endswith("/"): path = os.path.join(path, "index.html")
        if not os.path.exists(path): errors.append(f"{rel}: link to {u} points to a file that does not exist")
for f in ["index.html", "sitemap.xml", "llms.txt", "studies.json", "404.html"]:
    if not os.path.exists(os.path.join(ROOT, f)): errors.append(f"missing {f}")
if errors:
    print("Problems found:"); [print(" -", e) for e in sorted(set(errors))]; sys.exit(1)
print(f"OK: {len(pages)} pages checked")
