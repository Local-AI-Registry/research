"""Fail loudly if the built site is broken. Run after the build scripts."""
import os, re, json, sys, html
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
        # SEO and AEO: every study carries the same structure as The Local Answer Gap (see PLAYBOOK.md, steps 7 to 9)
        "key findings list (id=\"key-findings\")": 'id="key-findings"',
        "link to the Markdown copy": 'rel="alternate" type="text/markdown"',
        "Open Graph title": '<meta property="og:title"',
        "share image description": '<meta property="og:image:alt"',
        "X (Twitter) card": '<meta name="twitter:card"',
        "published date": '<meta property="article:published_time"',
        "FAQ schema": '"FAQPage"',
        "glossary schema (DefinedTermSet)": '"DefinedTermSet"',
        "dataset schema": '"Dataset"',
        "chart image schema (ImageObject)": '"ImageObject"',
        "breadcrumb schema": '"BreadcrumbList"',
        "speakable summary": '"speakable"',
        "how-to-cite section": 'id="cite"',
    }
    for label, needle in need.items():
        if needle not in s: errors.append(f"{slug}/index.html is missing {label} (copy the structure of local-answer-gap/index.html)")
    if not os.path.exists(os.path.join(ROOT, slug, "index.md")): errors.append(f"{slug}/index.md is missing (the Markdown copy of the page for AI tools)")
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    if t and len(html.unescape(t.group(1))) > 65: errors.append(f"{slug}: page title is {len(html.unescape(t.group(1)))} characters; keep it under 65")
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    if d and len(html.unescape(d.group(1))) > 165: errors.append(f"{slug}: meta description is {len(html.unescape(d.group(1)))} characters; keep it under 165")
    for img in re.findall(r"<img\b[^>]*>", s):
        if " alt=" not in img: errors.append(f"{slug}: an image has no alt text: {img[:90]}")
        elif not (" width=" in img and " height=" in img): errors.append(f"{slug}: an image has no width and height: {img[:90]}")
    og = re.search(r'<meta property="og:image" content="https://localairegistry.com/research/([^"]+)"', s)
    if og and not os.path.exists(os.path.join(ROOT, og.group(1))): errors.append(f"{slug}: the share image {og.group(1)} does not exist")
    if "prefers-color-scheme: dark" in s: errors.append(f"{slug}/index.html has a dark mode; the site is light mode only")
    if "\u2014" in s or "—" in re.sub(r"<script.*?</script>", "", s, flags=re.S): errors.append(f"{slug}/index.html contains an em dash")

if errors:
    print("Problems found:"); [print(" -", e) for e in sorted(set(errors))]; sys.exit(1)
print(f"OK: {len(pages)} pages checked")
