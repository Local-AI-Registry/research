"""Shared header and footer for every page on research.localairegistry.com.

Change them here, then run:  python scripts/build_hub.py  (rebuilds the hub)
and                          python scripts/chrome.py     (updates every study page)
"""
import os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAIM = "https://localairegistry.com/search"
# Google Places API (New) browser key for the map's business search.
# Restrict it in Google Cloud: Application restriction = Websites (research.localairegistry.com/*, proposals.localairegistry.com/*),
# API restriction = Places API (New). Leave empty to fall back to the free OpenStreetMap search.
GOOGLE_PLACES_KEY = ""
CONTACT = "https://localairegistry.com/signup/business/new"
SOCIAL = [("LinkedIn", "https://www.linkedin.com/company/local-ai-registry"), ("YouTube", "https://www.youtube.com/@localairegistry"),
          ("X", "https://x.com/LocalAIRegistry"), ("Instagram", "https://www.instagram.com/localairegistry/"),
          ("Facebook", "https://www.facebook.com/profile.php?id=61591432116527"), ("TikTok", "https://www.tiktok.com/@localairegistry"),
          ("Pinterest", "https://pinterest.com/localairegistry"), ("Crunchbase", "https://www.crunchbase.com/organization/local-ai-registry"),
          ("Trustpilot", "https://www.trustpilot.com/review/localairegistry.com")]

def header(base=""):
    """base = path back to the site root ('' on the hub, '../' on a study page)."""
    home = base or "./"
    return f'''<div class="sitehead" role="banner"><div class="sh-in">
<a class="sh-brand" href="{home}" aria-label="Local AI Registry Research home"><img src="{base}local-answer-gap/images/local-ai-registry-logo.svg" alt="Local AI Registry" width="170" height="21"><span class="sh-tag">Research</span></a>
<nav class="sh-nav" aria-label="Research"><a href="{home}#library">Library</a><a href="{base}local-answer-gap/">Latest study</a><a href="{home}#research-team">Team</a></nav>
<div class="sh-right"><a class="sh-main" href="https://localairegistry.com">localairegistry.com&nbsp;<span aria-hidden="true">↗</span></a><a class="sh-cta" href="{CLAIM}">Claim your free&nbsp;record</a></div>
</div></div>'''

def footer(base=""):
    home = base or "./"
    soc = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in SOCIAL)
    return f'''<div class="sitefoot" role="contentinfo"><div class="sf-in">
<div class="sf-brand"><img src="{base}local-answer-gap/images/local-ai-registry-logo.svg" alt="Local AI Registry" width="170" height="21" loading="lazy">
<p>Local AI Registry helps local businesses get found and described accurately by AI. Its dedicated local AI research team publishes original research here, free to use with&nbsp;credit.</p>
<p class="sf-addr">9891 Irvine Center Dr, Irvine, CA 92618 · <a href="tel:+12139315633">(213)&nbsp;931-5633</a></p></div>
<nav class="sf-col" aria-label="Research"><h2>Research</h2><ul><li><a href="{home}#library">Library</a></li><li><a href="{base}local-answer-gap/">The Local Answer Gap</a></li><li><a href="{home}#research-team">Research team</a></li><li><a href="{base}local-answer-gap/#cite">How to cite</a></li><li><a href="{base}llms.txt">llms.txt</a></li></ul></nav>
<nav class="sf-col" aria-label="Local AI Registry"><h2>Local AI Registry</h2><ul><li><a href="https://localairegistry.com">Home</a></li><li><a href="{CLAIM}">Find and claim your business</a></li><li><a href="https://localairegistry.com/brand">Brand</a></li></ul></nav>
<nav class="sf-col" aria-label="Follow Local AI Registry"><h2>Follow</h2><ul>{soc}</ul></nav>
</div><div class="sf-legal">© 2026 Local AI Registry. Research licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</div></div>'''

CSS = """
.sitehead{width:100%;margin:0;background:var(--paper);border-bottom:1px solid var(--line);position:relative;z-index:30}
.sh-in{max-width:1180px;margin:0 auto;padding:12px 16px;display:flex;align-items:center;gap:20px}
.sh-brand{display:flex;align-items:center;gap:10px;text-decoration:none;flex:none}
.sh-brand img{display:block;width:170px;height:auto}
.sh-tag{font:800 11px/1 var(--f-head,system-ui);letter-spacing:.1em;text-transform:uppercase;color:var(--blue);border-left:1px solid var(--line);padding-left:10px}
.sh-nav{display:flex;gap:18px;font-size:14px;font-weight:600}
.sh-nav a,.sh-main{color:var(--ink);text-decoration:none} .sh-nav a:hover,.sh-main:hover{color:var(--blue)}
.sh-right{margin-left:auto;display:flex;align-items:center;gap:16px;font-size:14px;font-weight:600}
.sh-cta{background:var(--blue);color:#fff;text-decoration:none;padding:9px 14px;border-radius:8px;font-weight:700;white-space:nowrap}
.sh-cta:hover{filter:brightness(1.08)}
@media (max-width:860px){.sh-nav,.sh-main{display:none}}
@media (max-width:420px){.sh-brand img{width:140px}.sh-tag{display:none}.sh-cta{padding:8px 11px;font-size:13px}}
.sitefoot{margin-top:64px;border-top:1px solid var(--line);background:var(--deep)}
.sf-in{max-width:1180px;margin:0 auto;padding:36px 16px 24px;display:grid;grid-template-columns:minmax(0,1.6fr) repeat(3,minmax(0,1fr));gap:28px}
@media (max-width:860px){.sf-in{grid-template-columns:repeat(2,minmax(0,1fr))}.sf-brand{grid-column:1/-1}}
.sf-brand{display:grid;gap:10px;align-content:start} .sf-brand p{margin:0;font-size:14px;color:var(--muted);max-width:420px}
.sf-col h2{font:800 13px/1.2 var(--f-head,system-ui);letter-spacing:.06em;text-transform:uppercase;margin:0 0 10px}
.sf-col ul{list-style:none;margin:0;padding:0;display:grid;gap:7px;font-size:14px} .sf-col a,.sf-legal a,.sf-addr a{color:var(--ink)}
.sf-legal{max-width:1180px;margin:0 auto;padding:14px 16px 28px;font-size:13px;color:var(--muted);border-top:1px solid var(--line)}
"""

def apply_to_studies():
    """Insert the shared header and footer into every study page (folders with index.html, except the hub and simulations)."""
    for path in glob.glob(os.path.join(ROOT, "*", "index.html")):
        folder = os.path.basename(os.path.dirname(path))
        if folder in ("simulations", "scripts", "assets"): continue
        s = open(path).read()
        s = re.sub(r"<!--chrome-css-->.*?<!--/chrome-css-->", "", s, flags=re.S)
        s = s.replace("</style>", "</style><!--chrome-css--><style>" + CSS + "</style><!--/chrome-css-->", 1)
        s = re.sub(r"<!--chrome-head-->.*?<!--/chrome-head-->", "", s, flags=re.S)
        s = re.sub(r"(<body[^>]*>)", r"\1<!--chrome-head-->" + header("../").replace("\\", "\\\\") + "<!--/chrome-head-->", s, count=1)
        s = re.sub(r"<!--chrome-foot-->.*?<!--/chrome-foot-->", "", s, flags=re.S)
        s = re.sub(r"<footer>.*?</footer>", "", s, count=1, flags=re.S)
        s = re.sub(r"(</main>)", r"\1<!--chrome-foot-->" + footer("../").replace("\\", "\\\\") + "<!--/chrome-foot-->", s, count=1)
        s = re.sub(r'<a href="https://localairegistry.com" class="logo-link"[^>]*>.*?</a>\s*', "", s, count=1, flags=re.S)
        open(path, "w").write(s); print("updated", folder)

if __name__ == "__main__":
    apply_to_studies()
