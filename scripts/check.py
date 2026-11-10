"""Fail loudly if the built site is broken. Run after the build scripts."""
import os, re, json, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []
pages = []
for d, _, fs in os.walk(ROOT):
    rel_d = os.path.relpath(d, ROOT).split(os.sep)[0]
    if "/.git" in d or rel_d in ("kit", "work", "node_modules"): continue
    pages += [os.path.join(d, f) for f in fs if f.endswith(".html")]
for p in pages:
    s = open(p, encoding="utf-8").read(); rel = os.path.relpath(p, ROOT)
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(b)
        except Exception as e: errors.append(f"{rel}: structured data is not valid JSON ({e})")
    for u in re.findall(r'(?:href|src)="(/research(?:/[^"#?]*)?)', s):
        path = os.path.join(ROOT, u[len("/research"):].lstrip("/"))
        if not os.path.splitext(path)[1]: path = os.path.join(path, "index.html")
        if not os.path.exists(path): errors.append(f"{rel}: link to {u} points to a file that does not exist")
for f in ["index.html", "sitemap.xml", "llms.txt", "studies.json", "404.html"]:
    if not os.path.exists(os.path.join(ROOT, f)): errors.append(f"missing {f}")
# Every study must follow the established study template.
data = json.load(open(os.path.join(ROOT, "studies.json")))
for st in data["studies"]:
    url = st.get("url", "")
    if url.startswith("http"): continue
    slug = url.strip("/").split("/")[-1]
    page_path = os.path.join(ROOT, slug, "index.html")
    if not os.path.exists(page_path):
        errors.append(f'{st.get("id")}: no page at {slug}/index.html'); continue
    s = open(page_path, encoding="utf-8").read()
    need = {
        "canonical address": f'<link rel="canonical" href="https://localairegistry.com/research/{slug}">',
        "site header": "<!--chrome-head-->",
        "site footer": "<!--chrome-foot-->",
        "structured data": 'application/ld+json',
        "report schema": '"Report"',
        "the short answer box": 'id="summary"',
        "the closing note that AI evolves every day": "AI is evolving every day",
        "page description": '<meta name="description"',
        "share image": '<meta property="og:image"',
    }
    for label, needle in need.items():
        if needle not in s: errors.append(f"{slug}/index.html is missing {label} (copy the structure of local-answer-gap/index.html)")
    if "prefers-color-scheme: dark" in s: errors.append(f"{slug}/index.html has a dark mode; the site is light mode only")
    if "\u2014" in s or "—" in re.sub(r"<script.*?</script>", "", s, flags=re.S): errors.append(f"{slug}/index.html contains an em dash")

if errors:
    print("Problems found:"); [print(" -", e) for e in sorted(set(errors))]; sys.exit(1)
print(f"OK: {len(pages)} pages checked")
