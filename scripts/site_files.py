"""Rebuild the site-wide SEO and AEO files from studies.json, so every new study is listed everywhere automatically.

Writes:
  sitemap.xml    every page, every chart and illustration (image sitemap), last-changed dates
  llms.txt       the short guide AI tools read: each study, its summary, Markdown and CSV links, key findings
  llms-full.txt  the full text of every study (each study's index.md), for AI tools
Video entries are added to sitemap.xml afterwards by video.py.
Run: python scripts/site_files.py   (the GitHub Action runs it automatically)
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://localairegistry.com/research"
x = lambda s: html.escape(html.unescape(str(s)), quote=False)

def strip(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s)).replace(" ", " ")).strip()

def studies():
    out = []
    for st in json.load(open(os.path.join(ROOT, "studies.json")))["studies"]:
        url = st.get("url", "")
        if url.startswith("http"): continue
        slug = url.strip("/").split("/")[-1]
        page = os.path.join(ROOT, slug, "index.html")
        if not os.path.exists(page): continue
        s = open(page, encoding="utf-8").read()
        figs = []
        for m in re.finditer(r'<figure id="([^"]+)" class="fig"><img src="[^"]*?([^"/]+)\.png".*?<figcaption><b>(?:Figure|Illustration) \d+\. (.*?)\.?</b>\s*(.*?)\s*<span class="dl">', s, re.S):
            figs.append(dict(file=m.group(2), title=strip(m.group(3)), caption=strip(m.group(4))))
        kf = re.search(r'id="key-findings".*?<ol[^>]*>(.*?)</ol>', s, re.S)
        findings = [strip(li) for li in re.findall(r"<li>(.*?)</li>", kf.group(1), re.S)] if kf else []
        out.append(dict(st=st, slug=slug, figs=figs, findings=findings,
                        md=os.path.exists(os.path.join(ROOT, slug, "index.md")),
                        lastmod=st.get("updated") or st.get("date", "")))
    return out

def sitemap(S):
    newest = max([s["lastmod"] for s in S] or [""])
    rows = [f"  <url><loc>{SITE}</loc>" + (f"<lastmod>{newest}</lastmod>" if newest else "") + "</url>"]
    for s in S:
        imgs = "".join(f"\n    <image:image><image:loc>{SITE}/{s['slug']}/images/{f['file']}.png</image:loc><image:title>{x(f['title'])}</image:title>"
                       f"<image:caption>{x(f['caption'])}</image:caption></image:image>" for f in s["figs"])
        rows.append(f"  <url><loc>{SITE}/{s['slug']}</loc>" + (f"<lastmod>{s['lastmod']}</lastmod>" if s["lastmod"] else "") + imgs + ("\n  " if imgs else "") + "</url>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n'
        + "\n".join(rows) + "\n</urlset>\n")

HEAD = """# Local AI Registry Research

> Original research from Local AI Registry (localairegistry.com), an answer engine optimization (AEO) company for local businesses, on how AI systems answer questions about local businesses.

Local AI Registry builds verified, owner-confirmed public records of local businesses and pushes those facts to the sources AI reads, through Google Business Profile management, press releases, AEO content, technical AEO (schema, llms.txt) and listing consistency. Headquarters: 9891 Irvine Center Dr, Irvine, CA 92618. Research is published by the Local AI Registry Research Team, led by a former Google Search executive, which builds on research by Aggarwal et al. (Princeton, GEO), Xu, Iqbal and Montgomery (WashU), Kumar and Lakkaraju (Harvard) and Liu, Zhang and Liang (Stanford).
"""
ABOUT = """## About

- [Local AI Registry](https://localairegistry.com): AEO and GEO services for local businesses; free business records and AI visibility audits.
- [Add your business free](https://localairegistry.com/signup/business/new): Create a free Local AI Registry record for a local business.
"""

def llms(S):
    o = [HEAD, "## Research\n", f"- [Research hub]({SITE}): Library of Local AI Registry studies, indexes and datasets on AI search and local businesses."]
    for s in S:
        st = s["st"]; base = f"{SITE}/{s['slug']}"; name = st.get("short_title") or st["title"].split(":")[0]
        o.append(f"- [{name}]({base}): {st['title']}. {st.get('summary', '')}")
        if s["md"]: o.append(f"- [{name}, full text (Markdown)]({base}/index.md): Complete report as plain Markdown.")
        if st.get("data_url"): o.append(f"- [{name}, data (CSV)]({SITE}/{st['data_url'].lstrip('/')}): Aggregated tables behind all charts, CC BY 4.0.")
        if st.get("video"): o.append(f"- [{name}, video explainer]({st['video']['youtube']}): A short plain-language walkthrough of the findings.")
    o.append(f"- [Full site text]({SITE}/llms-full.txt): All research in one file.\n")
    for s in S:
        if s["findings"]:
            o.append(f"## Key findings: {s['st'].get('short_title') or s['st']['title'].split(':')[0]}\n")
            o += [f"- {f}" for f in s["findings"]]
            o.append("")
    o.append(ABOUT)
    open(os.path.join(ROOT, "llms.txt"), "w").write("\n".join(o))
    full = [HEAD]
    for s in S:
        if s["md"]: full.append(open(os.path.join(ROOT, s["slug"], "index.md"), encoding="utf-8").read().strip() + "\n")
    open(os.path.join(ROOT, "llms-full.txt"), "w").write("\n\n---\n\n".join(full))

if __name__ == "__main__":
    S = studies()
    sitemap(S); llms(S)
    print(f"sitemap.xml, llms.txt, llms-full.txt rebuilt for {len(S)} studies, {sum(len(s['figs']) for s in S)} images")
