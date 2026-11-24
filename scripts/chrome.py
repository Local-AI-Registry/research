"""Shared header and footer for every page on localairegistry.com/research.

Change them here, then run:  python scripts/build_hub.py  (rebuilds the hub)
and                          python scripts/chrome.py     (updates every study page)
"""
import os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAIM = "https://localairegistry.com/search"
# Google Places API (New) browser key for the map's business search.
# Restrict it in Google Cloud: Application restriction = Websites (localairegistry.com/research/*, proposals.localairegistry.com/*),
# API restriction = Places API (New). Leave empty to fall back to the free OpenStreetMap search.
GOOGLE_PLACES_KEY = ""
CONTACT = "https://localairegistry.com/signup/business/new"
def _studies():
    """Study folders and short names, newest first, from studies.json (so new studies show in the header and footer)."""
    import json
    try: data = json.load(open(os.path.join(ROOT, "studies.json")))["studies"]
    except Exception: return []
    out = [(st["url"].strip("/").split("/")[-1], st.get("short_title") or st["title"].split(":")[0], st.get("date", ""))
           for st in data if st.get("url") and not st["url"].startswith("http") and os.path.exists(os.path.join(ROOT, st["url"].strip("/"), "index.html"))]
    return sorted(out, key=lambda x: x[2], reverse=True)
STUDIES = _studies()
LATEST = STUDIES[0][0] if STUDIES else "local-answer-gap"

SOCIAL = [("LinkedIn", "https://www.linkedin.com/company/local-ai-registry"), ("YouTube", "https://www.youtube.com/@localairegistry"),
          ("X", "https://x.com/LocalAIRegistry"), ("Instagram", "https://www.instagram.com/localairegistry/"),
          ("Facebook", "https://www.facebook.com/profile.php?id=61591432116527"), ("TikTok", "https://www.tiktok.com/@localairegistry"),
          ("Pinterest", "https://pinterest.com/localairegistry"), ("Crunchbase", "https://www.crunchbase.com/organization/local-ai-registry"),
          ("Trustpilot", "https://www.trustpilot.com/review/localairegistry.com")]

MAIN = "https://localairegistry.com"
NAV = [("Platform", "/blueprint"), ("Solutions", "/solutions"), ("Customers", "/results"), ("Research", "/research"), ("Pricing", "/plan")]
MARK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 22 21h-6.2L12 13.6 8.2 21H2z" fill="#1F4FE0"/><path d="M12 2l2.7 5.1H9.3z" fill="#FF5A3C"/></svg>'
ICONS = {
 "LinkedIn": "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.064 2.064 0 1 1 0-4.128 2.064 2.064 0 0 1 0 4.128zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0z",
 "YouTube": "M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z",
 "X": "M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z",
 "Instagram": "M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.4 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2zm0 4.6a5.2 5.2 0 1 0 0 10.4 5.2 5.2 0 0 0 0-10.4zm0 8.6a3.4 3.4 0 1 1 0-6.8 3.4 3.4 0 0 1 0 6.8zm5.4-9.9a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4z",
 "Facebook": "M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z",
 "TikTok": "M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.920-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.150-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z",
 "Pinterest": "M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.162-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.099.12.112.225.085.345-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.401.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.920-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.354-.629-2.758-1.379l-.749 2.848c-.269 1.045-1.004 2.352-1.498 3.146 1.123.345 2.306.535 3.55.535 6.607 0 11.985-5.365 11.985-11.987C23.97 5.39 18.592.026 11.985.026z",
 "Crunchbase": "M21.6 0H2.4A2.41 2.41 0 0 0 0 2.4v19.2A2.41 2.41 0 0 0 2.4 24h19.2a2.41 2.41 0 0 0 2.4-2.4V2.4A2.41 2.41 0 0 0 21.6 0zM7.045 14.465A2.11 2.11 0 0 0 9.84 13.42h1.66a3.69 3.69 0 1 1 0-1.75H9.84a2.11 2.11 0 1 0-2.795 2.795zm11.345.845a3.55 3.55 0 0 1-1.06.63 3.68 3.68 0 0 1-3.39-.38v.38h-1.51V5.37h1.5v4.11a3.74 3.74 0 0 1 1.8-.63H16a3.67 3.67 0 0 1 2.39 6.46zm-.223-2.766a2.104 2.104 0 1 1-4.207 0 2.104 2.104 0 0 1 4.207 0z",
}

def _soc():
    return '<div class="nx-soc">' + "".join(
        f'<a href="{u}" target="_blank" rel="me noopener" aria-label="Local AI Registry on {n}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONS[n]}"/></svg></a>'
        for n, u in SOCIAL if n in ICONS) + '</div>'

def header(base=""):
    """The main localairegistry.com header and menu, plus a slim Research bar. base = '' on the hub, '../' on a study page."""
    home = base or "./"
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{MAIN}{h}"{cur if n == "Research" else ""}>{n}</a>' for n, h in NAV)
    mnav = f'<a class="nx-g0" href="{MAIN}/">Home</a>' + "".join(f'<a class="nx-g0" href="{MAIN}{h}">{n}</a>' for n, h in NAV)
    return (f'<div class="nx-top" role="banner"><div class="nx-xa"><a href="{MAIN}/guarantee"><b>90 DAYS</b>Named in AI in 90 days, or we keep working for free. See how&nbsp;›</a></div>'
        f'<div class="nx-xh"><div class="nx-in"><a class="nx-brand" href="{MAIN}/">{MARK}Local AI Registry</a>'
        f'<nav class="nx-nav" aria-label="Main">{nav}</nav>'
        f'<div class="nx-r"><a class="nx-agi" href="{MAIN}/agents" title="For AI agents" aria-label="For AI agents">&gt;_</a><a class="nx-li" href="{MAIN}/login">Log in</a><a class="nx-xb nx-b" href="{MAIN}/start">Free AI audit<i>›</i></a></div>'
        f'<button class="nx-menu" type="button" data-nxmenu aria-label="Open menu"><span></span><span></span></button></div>'
        f'<nav class="nx-sub" aria-label="Research"><div class="nx-in"><a class="nx-subh" href="{home}">Research</a><a href="{home}#library">Library</a><a href="{base}{LATEST}/">Latest study</a><a href="{home}#research-team">Team</a><a href="{base}{LATEST}/#cite">How to cite</a></div></nav></div>'
        f'<div class="nx-xm" role="dialog" aria-label="Menu"><div class="nx-x1"><a class="nx-brand" href="{MAIN}/">{MARK}Local AI Registry</a><button type="button" data-nxmenu aria-label="Close menu">×</button></div>'
        f'<nav class="nx-xmn" aria-label="Menu">{mnav}</nav>'
        f'<div class="nx-xmf"><a class="nx-xb nx-b" href="{MAIN}/start">Get my free AI audit<i>›</i></a><div class="nx-xmb">{_soc()}<span><a href="{MAIN}/signup">Sign up</a><a href="{MAIN}/login">Log in&nbsp;→</a></span></div></div></div></div>')

FOOT_JS = """<script>(function(){var m=document.querySelector('.nx-xm');[].forEach.call(document.querySelectorAll('[data-nxmenu]'),function(b){b.addEventListener('click',function(){m.classList.toggle('on');document.documentElement.classList.toggle('nx-lock')})});
if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window))return;document.documentElement.classList.add('nxfx');
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
[].forEach.call(document.querySelectorAll('.nx-eb,.nx-rv'),function(e){io.observe(e)})})()</script>"""

def footer(base=""):
    home = base or "./"
    M = lambda pth: MAIN + pth
    col = lambda title, links: f'<div><b>{title}</b>' + "".join(f'<a href="{h}">{n}</a>' for n, h in links) + '</div>'
    research = ([("Library", f"{home}#library")] + [(nm, f"{base}{sl}/") for sl, nm, _ in STUDIES[:4]]
                + [("Research team", f"{home}#research-team"), ("How to cite", f"{base}{LATEST}/#cite"), ("llms.txt", f"{base}llms.txt")])
    cols = "".join([
        col("Research", research),
        col("Platform", [("The Blueprint", M("/blueprint")), ("AI monitoring", M("/blueprint/ai-monitoring")), ("Google profile", M("/blueprint/google-profile")), ("Reviews", M("/blueprint/reputation")), ("Directory listings", M("/blueprint/directory-listings")), ("Press releases", M("/blueprint/pr")), ("SEO", M("/blueprint/seo")), ("Website", M("/blueprint/web-management"))]),
        col("Solutions", [("Local business owners", M("/solutions/owners")), ("Multi-location groups", M("/solutions/multi-location")), ("Teams and agencies", M("/solutions/teams")), ("By industry", M("/industries")), ("Free AI audit", M("/start")), ("Pricing", M("/plan")), ("The 90-day guarantee", M("/guarantee"))]),
        col("Resources", [("Customers", M("/results")), ("Free tools", M("/tools")), ("Compare", M("/compare")), ("News", M("/news")), ("Changelog", M("/changelog"))]),
        col("Company", [("About", M("/about")), ("Team", M("/about#team")), ("Careers", M("/about#careers")), ("Contact", M("/contact")), ("Log in", M("/login")), ("Sign up", M("/signup"))]),
    ])
    return (f'<div class="nx-foot" role="contentinfo">'
        f'<section class="nx-close"><div class="nx-in"><span class="nx-eb">The 90-day guarantee</span><h2 class="nx-h2">Put the research to work<br>for your&nbsp;business.</h2>'
        f'<p class="nx-subp">Named in AI in 90 days. If not, we keep working for free until&nbsp;it&nbsp;happens.</p>'
        f'<div class="nx-xbs"><a class="nx-xb nx-w" href="{M("/start")}">Get my free AI audit<i>›</i></a><a class="nx-xb nx-o" href="{M("/guarantee")}">How the guarantee works</a></div></div></section>'
        f'<footer class="nx-ft2"><div class="nx-in"><div class="nx-fcols">{cols}</div>'
        f'<div class="nx-fsoc">{_soc()}<a class="nx-agt" href="{M("/agents")}">/agents · for AI agents</a></div>'
        f'<div class="nx-fb"><span>© 2026 Local AI Registry. 9891 Irvine Center Dr, Irvine, CA 92618. <a href="tel:+12139315633">(213)&nbsp;931-5633</a>. Research licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC&nbsp;BY&nbsp;4.0</a>.</span>'
        f'<span><a href="{M("/legal/privacy")}">Privacy</a> &nbsp; <a href="{M("/legal/terms")}">Terms</a></span></div></div></footer></div>' + FOOT_JS)

CSS = """
.nx-top,.nx-foot{--nx-ink:#0B1A2E;--nx-ink2:#5A647A;--nx-soft:#8C94A3;--nx-line:#E6E3DC;--nx-blue:#1F4FE0;--nx-paper:#F4F1EA;font:400 16px/1.6 "Hanken Grotesk",system-ui,sans-serif;color:var(--nx-ink);-webkit-font-smoothing:antialiased;text-align:left}
.nx-top *,.nx-foot *{box-sizing:border-box}
.nx-top{position:sticky;top:-40px;z-index:40}
.nx-in{max-width:1200px;margin:0 auto;padding:0 24px}
.nx-xa{background:var(--nx-ink);color:#fff;text-align:center;font-size:14px;line-height:20px;padding:10px 16px}
.nx-xa a{color:#fff;text-decoration:none}
.nx-xa b{display:inline-block;background:var(--nx-blue);font:600 10.5px/1 "Bricolage Grotesque",sans-serif;letter-spacing:.12em;padding:5px 8px;border-radius:5px;margin-right:10px;vertical-align:1px}
.nx-xh{background:rgba(255,255,255,.88);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-bottom:1px solid var(--nx-line)}
.nx-xh>.nx-in{display:flex;align-items:center;height:64px;gap:32px}
.nx-brand{display:flex;align-items:center;gap:9px;text-decoration:none;font:700 18px/1 "Bricolage Grotesque",sans-serif;color:var(--nx-ink)!important;letter-spacing:-.01em;white-space:nowrap}
.nx-brand svg{width:24px;height:24px;flex:0 0 auto}
.nx-nav{display:flex;align-items:center;gap:26px;margin:0 auto}
.nx-nav a{font-size:14.5px;text-decoration:none;color:var(--nx-ink2)!important}
.nx-nav a[aria-current]{color:var(--nx-ink)!important;font-weight:500}.nx-nav a:hover{color:var(--nx-ink)!important}
.nx-r{display:flex;align-items:center;gap:18px}
.nx-li{font-size:14.5px;text-decoration:none;color:var(--nx-ink)!important;white-space:nowrap}
.nx-agi{font:600 12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--nx-soft)!important;text-decoration:none;border:1px solid var(--nx-line);border-radius:6px;padding:5px 6px;letter-spacing:-.02em}
.nx-agi:hover{color:var(--nx-ink)!important;border-color:var(--nx-ink)}
.nx-xb{display:inline-flex;align-items:center;gap:10px;height:44px;padding:0 6px 0 20px;border-radius:999px;font:500 15px/1 "Hanken Grotesk",sans-serif;text-decoration:none!important;white-space:nowrap;transition:background .2s,transform .2s;border:0;cursor:pointer}
.nx-xb i{width:32px;height:32px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:15px}
.nx-xb:active{transform:scale(.985)}
.nx-b{background:var(--nx-blue,#1F4FE0);color:#fff!important}.nx-b i{background:rgba(255,255,255,.18)}.nx-b:hover{background:#1A43C2}
.nx-k{background:var(--nx-ink,#0B1A2E);color:#fff!important;padding:0 20px}.nx-k:hover{background:#22324A}
.nx-w{background:#fff;color:var(--nx-ink)!important}.nx-w i{background:var(--nx-paper)}
.nx-o{background:transparent;color:#fff!important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.35);padding:0 20px}
.nx-xh .nx-xb{height:38px;font-size:14px}.nx-xh .nx-xb i{width:28px;height:28px}
.nx-menu{display:none;background:none;border:0;width:40px;height:40px;margin-left:auto;cursor:pointer}
.nx-menu span{display:block;width:18px;height:1.5px;background:var(--nx-ink);margin:4px auto}
.nx-sub{border-top:1px solid var(--nx-line)}
.nx-sub .nx-in{display:flex;align-items:center;gap:22px;height:42px;overflow-x:auto;scrollbar-width:none}
.nx-sub a{font-size:13.5px;color:var(--nx-ink2)!important;text-decoration:none;white-space:nowrap}.nx-sub a:hover{color:var(--nx-ink)!important}
.nx-sub .nx-subh{font:600 11px/1 "Bricolage Grotesque",sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--nx-blue)!important}
.nx-xm{display:none;position:fixed;inset:0;z-index:60;background:#fff;padding:16px 24px 24px;flex-direction:column;overflow-y:auto}
.nx-xm.on{display:flex}.nx-lock body{overflow:hidden}
.nx-x1{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
.nx-x1 button{background:none;border:0;font-size:30px;line-height:1;color:var(--nx-ink);cursor:pointer;padding:6px 2px}
.nx-xmn{display:flex;flex-direction:column;gap:2px}
.nx-g0{font:400 clamp(30px,8.5vw,40px)/1.15 "Hanken Grotesk",sans-serif;letter-spacing:-.025em;color:#5B6170!important;text-decoration:none;padding:8px 0}
.nx-g0:first-child{color:var(--nx-ink)!important}
.nx-xmf{margin-top:auto;padding-top:28px}.nx-xmf .nx-xb{display:flex;justify-content:center;min-height:54px}
.nx-xmb{display:flex;justify-content:space-between;align-items:center;margin-top:22px;padding-top:20px;border-top:1px solid var(--nx-line);gap:12px;flex-wrap:wrap}
.nx-xmb span{display:flex;gap:18px;align-items:center}.nx-xmb span a{color:var(--nx-ink)!important;text-decoration:none}
.nx-soc{display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.nx-soc a{display:grid;place-items:center;width:22px;height:22px;color:var(--nx-ink)}
.nx-soc svg{width:20px;height:20px;fill:currentColor}
@media (max-width:1180px){.nx-xh>.nx-in{gap:20px}.nx-nav{gap:16px}.nx-r{gap:12px}.nx-nav a{font-size:14px}}
@media (max-width:980px){.nx-nav,.nx-r{display:none}.nx-menu{display:block}}
@media (max-width:560px){.nx-xa{font-size:13px}}
.nx-foot{margin-top:clamp(64px,8vw,110px)}
.nx-close{background:var(--nx-ink);color:#fff;text-align:center;position:relative;overflow:hidden;padding:clamp(110px,12vw,170px) 0}
.nx-close::before{content:"";position:absolute;inset:0;background:radial-gradient(60% 70% at 50% 0%,rgba(31,79,224,.55),transparent 70%);opacity:.9}
.nx-close::after{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1px,transparent 1px);background-size:5px 5px;-webkit-mask:linear-gradient(#000,transparent 75%);mask:linear-gradient(#000,transparent 75%)}
.nx-close .nx-in{position:relative;z-index:1;text-align:center}
.nx-h2{font:400 clamp(32px,3.5vw,48px)/1.18 "Hanken Grotesk",sans-serif;letter-spacing:-.025em;color:#fff;margin:0;text-wrap:balance}
.nx-subp{margin:18px auto 0;max-width:30em;font-size:clamp(17px,1.4vw,20px);line-height:1.5;color:rgba(255,255,255,.7)}
.nx-xbs{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:center;margin-top:30px}
.nx-eb{font:600 11.5px/1 "Bricolage Grotesque",sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#8C94A3;margin:0 0 18px;display:block}
.nx-close .nx-eb{color:rgba(255,255,255,.6);margin-left:auto;margin-right:auto;width:fit-content}
.nx-ft2{background:var(--nx-ink);color:rgba(255,255,255,.7);font-size:14px;padding:30px 0 40px;border-top:1px solid rgba(255,255,255,.08)}
.nx-fcols{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:24px;padding:40px 0;border-bottom:1px solid rgba(255,255,255,.08)}
.nx-fcols b{display:block;color:#fff;font-weight:500;margin-bottom:14px;font-size:14px}
.nx-fcols a{display:block;text-decoration:none;color:rgba(255,255,255,.62)!important;padding:4px 0;font-size:13.5px}
.nx-fcols a:hover{color:#fff!important}
.nx-fsoc{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:22px 0;border-bottom:1px solid rgba(255,255,255,.08);flex-wrap:wrap}
.nx-ft2 .nx-soc a{color:rgba(255,255,255,.7)}.nx-ft2 .nx-soc a:hover{color:#fff}
.nx-agt{font:12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;color:rgba(255,255,255,.55)!important;text-decoration:none;letter-spacing:.02em}
.nx-fb{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-top:22px;font-size:12.5px;color:rgba(255,255,255,.5)}
.nx-fb a{color:inherit!important}
@media (max-width:980px){.nx-fcols{grid-template-columns:1fr 1fr}}
.nxfx .nx-eb{position:relative;width:fit-content;color:transparent}
.nxfx .nx-eb::after{content:"";position:absolute;inset:-4px -6px;background:#1F4FE0;border-radius:3px;clip-path:inset(0 100% 0 0)}
.nxfx .nx-eb.on{animation:nxebt .9s steps(1) forwards}.nxfx .nx-close .nx-eb.on{animation-name:nxebt2}
.nxfx .nx-eb.on::after{animation:nxebw .9s cubic-bezier(.7,0,.3,1) forwards}
@keyframes nxebw{0%{clip-path:inset(0 100% 0 0)}45%{clip-path:inset(0)}100%{clip-path:inset(0 0 0 100%)}}
@keyframes nxebt{0%,44%{color:transparent}45%,100%{color:#8C94A3}}
@keyframes nxebt2{0%,44%{color:transparent}45%,100%{color:rgba(255,255,255,.6)}}
.nxfx .nx-rv{opacity:0;filter:blur(12px);transform:translateY(28px);transition:opacity 1s cubic-bezier(.2,.7,.2,1),filter 1s cubic-bezier(.2,.7,.2,1),transform 1s cubic-bezier(.2,.7,.2,1);transition-delay:var(--d,0s)}
.nxfx .nx-rv.on{opacity:1;filter:none;transform:none}
@media (prefers-reduced-motion:reduce){.nx-rv{opacity:1!important;filter:none!important;transform:none!important}}
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
