"""Builds the research hub (index.html) from studies.json.

Flávia: you never need to run this by hand. Edit studies.json on GitHub and save;
the "Build research hub" automation runs this script and publishes the page.
"""
import re, json, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREVIEW = "--preview" in sys.argv
rep = open(os.path.join(ROOT, "local-answer-gap/index.html")).read()
auth = re.search(r'<section id="authors"[^>]*>(.*?)</section>', rep, re.S).group(1)
paras = re.findall(r'<p>.*?</p>', auth, re.S)
SITE = "https://localairegistry.com/research/"; R = SITE + "local-answer-gap/"
SAMEAS = re.search(r'"sameAs": (\[[^\]]*\])', rep).group(1)
IMG = "local-answer-gap/images/who-google-ai-cites-for-local-business-questions-heatmap"
e = lambda s: html.escape(s, quote=True)
FAQ = [
 ("How many people use AI to find local businesses?", "Nearly half of consumers now ask AI tools such as ChatGPT, Gemini and Perplexity for local business recommendations, according to BrightLocal’s 2026 research. ChatGPT has more than 900 million weekly users, Google’s AI Mode passed one billion monthly users in May 2026 with queries more than doubling every quarter, and Local AI Registry found that 76.4% of local business searches show a Google AI answer before any link."),
 ("What is Local AI Registry Research?", "Local AI Registry Research is the research program of Local AI Registry, an answer engine optimization (AEO) company for local businesses. Its dedicated local AI research team studies how ChatGPT, Claude, Gemini, Google AI Overviews, Perplexity and Microsoft Copilot find, read and recommend local businesses, and publishes the findings free at localairegistry.com/research."),
 ("What has Local AI Registry’s research found?", "In The Local Answer Gap, Local AI Registry analyzed 7,583 Google AI Overviews and 98,020 fact-checked claims. News outlets supplied 67.5% of the citations in AI answers about local businesses, businesses’ own websites supplied 6.5%, and 83.6% of answers told people to check with their local store."),
 ("Can I use Local AI Registry’s research and charts?", "Yes. All findings and charts are free to use under a CC BY 4.0 license with credit to Local AI Registry and a link to the study. Every chart has a ready-made embed code, and each study’s data can be downloaded."),
 ("How does Local AI Registry use this research?", "Every finding feeds the AEO playbook Local AI Registry uses for local businesses: verified owner-confirmed business records, Google Business Profile management, press, AEO content, technical AEO and listing consistency."),
]
DESC = "Original AEO research from Local AI Registry on how ChatGPT, Claude, Gemini, Google AI Overviews and Perplexity find and recommend local businesses."

TYPES = ["Study", "Brief", "Index", "Dataset", "Experiment"]
ENGINES = ["ChatGPT", "Claude", "Gemini", "Google AI Overviews", "Google AI Mode", "Perplexity", "Microsoft Copilot", "Meta AI"]
FILTERS_AT = 10   # search and filters appear once there are this many studies

def load_studies():
    data = json.load(open(os.path.join(ROOT, "studies.json")))
    out = []
    for i, x in enumerate(data["studies"]):
        for k in ["id", "title", "url", "date", "type", "summary", "ai_assistants", "topics"]:
            if not x.get(k): raise SystemExit(f'studies.json entry {i+1} is missing "{k}"')
        if x["type"] not in TYPES: raise SystemExit(f'studies.json entry {i+1}: type must be one of {TYPES}')
        bad = [en for en in x["ai_assistants"] if en not in ENGINES]
        if bad: raise SystemExit(f'studies.json entry {i+1}: unknown AI assistant {bad}. Use one of {ENGINES}')
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", x["date"]): raise SystemExit(f'studies.json entry {i+1}: date must look like 2026-11-07')
        y, m, d = x["date"].split("-")
        out.append(dict(id=x["id"], url=x["url"], title=x["title"], date=x["date"],
            dlabel=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][int(m)-1] + f" {int(d)}, {y}",
            type=x["type"], engines=x["ai_assistants"], topics=x["topics"], abstract=x["summary"], data=x.get("data_url") or None, vlen=(x.get("video") or {}).get("length"), real=True))
    return out
REAL = load_studies()
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "Organization", "@id": "https://localairegistry.com/#organization", "name": "Local AI Registry", "alternateName": ["LAIR", "localairegistry.com"], "url": "https://localairegistry.com",
   "logo": R + "images/local-ai-registry-logo.png", "sameAs": json.loads(SAMEAS),
   "address": {"@type": "PostalAddress", "streetAddress": "9891 Irvine Center Dr", "addressLocality": "Irvine", "addressRegion": "CA", "postalCode": "92618", "addressCountry": "US"},
   "telephone": "+1-213-931-5633", "subOrganization": {"@id": SITE + "#research-team"}},
  {"@type": "ResearchOrganization", "@id": SITE + "#research-team", "name": "Local AI Registry Research Team", "url": SITE + "#research-team", "parentOrganization": {"@id": "https://localairegistry.com/#organization"},
   "knowsAbout": ["Answer engine optimization", "Generative engine optimization", "Google AI Overviews", "AI search citations", "Local search"]},
  {"@type": "WebSite", "@id": SITE + "#website", "url": SITE, "name": "Local AI Registry Research", "publisher": {"@id": "https://localairegistry.com/#organization"}, "inLanguage": "en-US"},
  {"@type": "CollectionPage", "@id": SITE + "#page", "url": SITE, "name": "Local AI Registry Research", "description": DESC, "isPartOf": {"@id": SITE + "#website"},
   "about": [{"@type": "Thing", "name": "Answer engine optimization"}, {"@type": "Thing", "name": "Local search"}],
   "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Local AI Registry", "item": "https://localairegistry.com/"}, {"@type": "ListItem", "position": 2, "name": "Research", "item": SITE}]},
   "mainEntity": {"@type": "ItemList", "numberOfItems": len(REAL), "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + x["url"], "name": x["title"]} for i, x in enumerate(REAL)]},
   "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".hero-card h1", ".nums", "#faq"]}},
  {"@type": "FAQPage", "@id": SITE + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
PH = [("How ChatGPT picks a med spa near you","Study",["ChatGPT"],["Med spas"]),
 ("Do Google reviews change which business AI recommends?","Study",["ChatGPT","Gemini","Google AI Overviews"],["Reviews"]),
 ("Plastic surgeons in AI answers: who gets named, and why","Study",["ChatGPT","Claude","Perplexity"],["Plastic surgery"]),
 ("What AI assistants will and won’t say about dispensaries","Brief",["ChatGPT","Claude","Gemini"],["Cannabis"]),
 ("Claude vs ChatGPT vs Gemini on “best near me” questions","Study",["Claude","ChatGPT","Gemini"],["Comparison"]),
 ("Does LocalBusiness schema change AI citations?","Experiment",["Google AI Overviews","Perplexity"],["Technical AEO"]),
 ("How often AI gets business hours wrong","Study",["ChatGPT","Gemini","Microsoft Copilot"],["Accuracy"]),
 ("Press coverage and AI visibility: does it stick?","Study",["ChatGPT","Perplexity"],["Press"]),
 ("Eye surgeons in AI search","Brief",["ChatGPT","Gemini"],["Ophthalmology"]),
 ("AI Visibility Index: Orange County med spas","Index",["ChatGPT","Claude","Gemini","Perplexity"],["Med spas","Index"]),
 ("From AI answer to booked visit: what happens next","Study",["ChatGPT"],["Bookings"]),
 ("Local AI answers by city size","Dataset",["Google AI Overviews"],["Geography"])]
PLACE = [dict(id="LAIR-R-PLACEHOLDER-%02d" % (i+1), url="#", title=t, date="2026-10-%02d" % (28-i), dlabel="Date TBD", type=ty, engines=en, topics=tp,
  abstract="Placeholder study for layout review. Not real research; no findings yet.", data=None, n="", real=False) for i,(t,ty,en,tp) in enumerate(PH)]

def row(x):
    eng = ", ".join(x["engines"]); tops = "".join(f'<li>{e(t)}</li>' for t in x["topics"])
    attrs = f'data-type="{e(x["type"])}" data-engines="{e("|".join(x["engines"]))}" data-topics="{e("|".join(x["topics"]))}" data-date="{x["date"]}" data-text="{e((x["title"]+" "+x["abstract"]+" "+eng+" "+" ".join(x["topics"])).lower())}"'
    badge = "" if x["real"] else '<span class="ph">Placeholder</span>'
    title = f'<a href="{x["url"]}">{e(x["title"])}</a>' if x["real"] else e(x["title"])
    links = (f'<a href="{x["url"]}">Read</a><a href="{x["url"]}#cite">Cite</a>' + (f'<a href="{x["data"]}">Data (CSV)</a>' if x["data"] else "") + (f'<a href="{x["url"]}#video">Video ({e(x["vlen"])})</a>' if x.get("vlen") else "")) if x["real"] else '<span>Read</span><span>Cite</span><span>Data</span>'
    return (f'<li class="st{"" if x["real"] else " is-ph"}" {attrs}><div class="st-meta"><span class="st-type">{e(x["type"])}</span><span>{e(x["dlabel"])}</span><span class="st-id">{e(x["id"])}</span>{badge}</div>'
            f'<h3>{title}</h3><p>{e(x["abstract"])}</p><div class="st-foot"><span class="st-eng">{e(eng)}</span><ul class="tags">{tops}</ul><span class="st-links">{links}</span></div></li>')

def library(items):
    types = sorted({x["type"] for x in items}); engs = sorted({en for x in items for en in x["engines"]}); tops = sorted({t for x in items for t in x["topics"]})
    opt = lambda lst: "".join(f'<option value="{e(v)}">{e(v)}</option>' for v in lst)
    return f'''<section class="lib" id="library" aria-labelledby="libh">
<div class="lib-head"><div><div class="k">Research library</div><h2 id="libh">Studies, indexes and datasets</h2></div>
<p class="lib-count" id="count" aria-live="polite">{len(items)} {"study" if len(items)==1 else "studies"}</p></div>
{'<form class="lib-tools" role="search" onsubmit="return false">' if len(items) >= FILTERS_AT else '<form class="lib-tools" hidden onsubmit="return false">'}
<label class="srch"><span class="sr">Search the research</span><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><input id="q" type="search" placeholder="Search studies, topics or AI assistants" autocomplete="off"></label>
<label><span class="sr">Topic</span><select id="f-topic"><option value="">All topics</option>{opt(tops)}</select></label>
<label><span class="sr">AI assistant</span><select id="f-eng"><option value="">All AI assistants</option>{opt(engs)}</select></label>
<label><span class="sr">Type</span><select id="f-type"><option value="">All types</option>{opt(types)}</select></label>
<label><span class="sr">Sort</span><select id="f-sort"><option value="new">Newest first</option><option value="old">Oldest first</option><option value="az">A to Z</option></select></label>
</form>
<ol class="studies" id="studies">{"".join(row(x) for x in items)}</ol>
<p class="empty" id="empty" hidden>No studies match. Try a different search or clear the filters.</p>
<div class="more"><button type="button" id="more" hidden>Show more</button></div>
</section>'''

JS = r'''<script>
(function(){
  var f=document.getElementById('sim');
  function load(){ if(f && !f.src) f.src=f.getAttribute('data-src'); }
  if(document.readyState==='complete') setTimeout(load,50); else addEventListener('load',function(){setTimeout(load,50);});
  var GKEY=document.getElementById('finder').getAttribute('data-gkey'), CONTACT=document.getElementById('finder').getAttribute('data-contact'), tok=null;
  var gq=document.getElementById('gq'), go=document.getElementById('gopts'), gs=document.getElementById('gstatus'), items=[], act=-1, timer=null, seq=0;
  function kindOf(p){ var k=(p.osm_key||'')+'='+(p.osm_value||''), n=(p.name||'').toLowerCase();
    if(/med ?spa|medspa|aesthetic|botox|injector|laser|skin clinic/.test(n)) return 'medspa';
    if(/plastic surg|cosmetic surg/.test(n)) return 'plastic';
    if(/dentist|dental|orthodont/.test(k+n)) return 'dental';
    if(/cannabis|dispensar/.test(k+n)) return 'dispensary';
    if(/optician|optometr|ophthalm|eye|lasik|vision/.test(k+n)) return 'eyecare';
    if(/restaurant|cafe|fast_food|bar=|pub|bakery|ice_cream/.test(k)) return 'restaurant';
    if(/hairdresser|beauty|nail|salon|barber/.test(k+n)) return /beauty/.test(k)&&/spa/.test(n)?'medspa':'salon';
    return 'other'; }
  function close(){ go.hidden=true; gq.setAttribute('aria-expanded','false'); act=-1; }
  var state='done';
  function show(){ go.innerHTML='';
    if(state==='busy'){ go.innerHTML='<li class="none">Searching\u2026</li>'; }
    else if(state==='down'){ go.innerHTML='<li class="none">Business search is busy right now. Try again in a moment.</li>'; }
    else if(!items.length){ go.innerHTML='<li class="none">No match for that name.</li>'; }
    items.forEach(function(it,i){ var li=document.createElement('li'); li.id='go'+i; li.setAttribute('role','option'); li.setAttribute('aria-selected',i===act?'true':'false');
      var b=document.createElement('b'); b.textContent=it.name; var sp=document.createElement('span'); sp.textContent=it.area; li.appendChild(b); li.appendChild(sp);
      li.addEventListener('mousedown',function(e){e.preventDefault(); pickIt(i);}); go.appendChild(li); });
    if(state!=='busy'){ var cta=document.createElement('li'); cta.className='cta'+(act===items.length?' on':''); cta.setAttribute('role','option'); cta.id='go'+items.length; cta.setAttribute('aria-selected',act===items.length?'true':'false');
      var a=document.createElement('a'); a.href=CONTACT; a.textContent='Don\u2019t see your business? Add it free \u2192'; cta.appendChild(a);
      cta.addEventListener('mousedown',function(e){e.preventDefault(); location.href=CONTACT;}); go.appendChild(cta); }
    if(GKEY&&items.length){ var at=document.createElement('li'); at.className='attr'; at.setAttribute('aria-hidden','true'); at.textContent='Results from Google'; go.appendChild(at); }
    go.hidden=false; gq.setAttribute('aria-expanded','true'); }
  function pickIt(i){ var it=items[i]; if(!it) return; gq.value=it.name; close();
    if(it.gid&&it.lat==null){ gs.textContent='Finding '+it.name+'\u2026'; resolveGoogle(it).then(function(){pickIt2(it);}).catch(function(){gs.textContent='Couldn\u2019t load that business. Try another.';}); return; }
    pickIt2(it); }
  function pickIt2(it){ if(!f.src) load();
    var msg={type:'lair-goto-place',name:it.name,lon:it.lon,lat:it.lat,kind:it.kind,area:it.area,city:it.city};
    var sendIt=function(){ f.contentWindow&&f.contentWindow.postMessage(msg,location.origin); };
    if(f.contentWindow&&f.src) sendIt(); else f.addEventListener('load',function(){setTimeout(sendIt,1500);},{once:true});
    gs.textContent='Showing '+it.name+(it.area?', '+it.area:'')+'. Click the pin to see its Local AI Registry record.'; }
  function newTok(){ tok=(crypto.randomUUID?crypto.randomUUID():String(Date.now())+Math.random()); }
  function gKind(types,name){ var t=(types||[]).join(' '), n=(name||'').toLowerCase();
    if(/med ?spa|medspa|aesthetic|botox|injector|laser|skin/.test(n)||/skin_care_clinic/.test(t)) return 'medspa';
    if(/plastic surg|cosmetic surg/.test(n)) return 'plastic';
    if(/dentist|dental/.test(t+' '+n)) return 'dental';
    if(/cannabis|dispensar|weed/.test(n)) return 'dispensary';
    if(/optometr|optician|eye|lasik|vision/.test(t+' '+n)) return 'eyecare';
    if(/restaurant|cafe|bakery|bar\b|meal_|food/.test(t)) return 'restaurant';
    if(/hair|nail|beauty_salon|barber/.test(t)) return 'salon';
    if(/spa/.test(t)) return 'medspa';
    return 'other'; }
  function searchGoogle(q,my){
    if(!tok) newTok();
    return fetch('https://places.googleapis.com/v1/places:autocomplete',{method:'POST',headers:{'Content-Type':'application/json','X-Goog-Api-Key':GKEY},
      body:JSON.stringify({input:q,sessionToken:tok,includedRegionCodes:['us'],locationBias:{circle:{center:{latitude:33.68,longitude:-117.83},radius:50000}}})})
      .then(function(r){return r.json();}).then(function(j){ if(my!==seq) return;
        items=(j.suggestions||[]).filter(function(x){return x.placePrediction;}).slice(0,6).map(function(x){var p=x.placePrediction, sf=p.structuredFormat||{};
          return {gid:p.placeId,name:(sf.mainText||{}).text||p.text.text,area:(sf.secondaryText||{}).text||'',types:p.types||[]}; });
        state='done'; act=items.length?0:-1; show(); });
  }
  function resolveGoogle(it){
    return fetch('https://places.googleapis.com/v1/places/'+encodeURIComponent(it.gid)+'?sessionToken='+encodeURIComponent(tok||''),
      {headers:{'X-Goog-Api-Key':GKEY,'X-Goog-FieldMask':'id,displayName,location,formattedAddress,primaryType,types,addressComponents'}})
      .then(function(r){return r.json();}).then(function(p){ tok=null;
        var city=''; (p.addressComponents||[]).forEach(function(c){ if((c.types||[]).indexOf('locality')>-1) city=c.longText; });
        it.lon=p.location.longitude; it.lat=p.location.latitude; it.city=city; it.area=p.formattedAddress||it.area;
        it.kind=gKind([p.primaryType].concat(p.types||[]),it.name); return it; });
  }
  function tfetch(url,ms){ var c=('AbortController' in window)?new AbortController():null, t=setTimeout(function(){c&&c.abort();},ms||4000);
    return fetch(url,c?{signal:c.signal}:{}).then(function(r){clearTimeout(t); if(!r.ok) throw new Error('HTTP '+r.status); return r.json();},function(e){clearTimeout(t);throw e;}); }
  function nomKind(x){ return kindOf({osm_key:x.class,osm_value:x.type,name:x.name||((x.namedetails||{}).name)||''}); }
  var lastNom=0;
  function searchNominatim(q,my){
    var wait=Math.max(0,1100-(Date.now()-lastNom));   /* Nominatim allows at most one request per second */
    return new Promise(function(res){setTimeout(res,wait);}).then(function(){ if(my!==seq) return null; lastNom=Date.now();
      return tfetch('https://nominatim.openstreetmap.org/search?format=jsonv2&addressdetails=1&namedetails=1&limit=6&countrycodes=us&q='+encodeURIComponent(q),5000); })
      .then(function(j){ if(!j||my!==seq) return null;
        return j.map(function(x){var a=x.address||{}, city=a.city||a.town||a.village||a.suburb||a.county||'';
          var nm=x.name||[a.house_number,a.road].filter(Boolean).join(' ')||(x.display_name||'').split(',')[0];
          return {name:nm,lon:+x.lon,lat:+x.lat,kind:nomKind(x),city:city,area:[[a.house_number,a.road].filter(Boolean).join(' '),city,a.state].filter(Boolean).join(', ')}; }); });
  }
  function searchOSM(q,my){
    return tfetch('https://photon.komoot.io/api/?limit=8&lang=en&q='+encodeURIComponent(q),4000).then(function(j){
      return (j.features||[]).filter(function(x){var p=x.properties||{};return p.countrycode==='US'&&(p.name||p.street);}).slice(0,6).map(function(x){var p=x.properties; if(!p.name) p.name=[p.housenumber,p.street].filter(Boolean).join(' ');
        var city=p.city||p.town||p.village||p.district||p.county||'';
        return {name:p.name,lon:x.geometry.coordinates[0],lat:x.geometry.coordinates[1],kind:kindOf(p),city:city,
          area:[[p.housenumber,p.street].filter(Boolean).join(' '),city,p.state].filter(Boolean).join(', ')}; }); })
      .catch(function(){ return null; })
      .then(function(list){ if(my!==seq) return; if(list&&list.length) return list;
        return searchNominatim(q,my).catch(function(){ return list===null?'down':[]; }); })
      .then(function(list){ if(my!==seq||list===undefined) return;
        if(list==='down'){ items=[]; state='down'; } else { items=list||[]; state='done'; }
        act=items.length?0:-1; show(); });
  }
  gq.addEventListener('input',function(){ clearTimeout(timer); var q=gq.value.trim(); if(q.length<3){close();return;}
    state='busy'; items=[]; show();
    timer=setTimeout(function(){ var my=++seq; (GKEY?searchGoogle(q,my):searchOSM(q,my)).catch(function(){ if(my===seq){items=[];state='down';show();} }); },250); });
  gq.addEventListener('keydown',function(e){ if(go.hidden) return;
    if(e.key==='ArrowDown'){act=Math.min(act+1,items.length);show();e.preventDefault();}
    else if(e.key==='ArrowUp'){act=Math.max(act-1,0);show();e.preventDefault();}
    else if(e.key==='Enter'){ if(act===items.length){location.href=CONTACT;} else if(act>-1){pickIt(act);} e.preventDefault(); }
    else if(e.key==='Escape'){close();} });
  gq.addEventListener('blur',function(){setTimeout(close,150);});
  var list=document.getElementById('studies'), rows=[].slice.call(list.children), q=document.getElementById('q'),
      ft=document.getElementById('f-topic'), fe=document.getElementById('f-eng'), fy=document.getElementById('f-type'), fs=document.getElementById('f-sort'),
      count=document.getElementById('count'), empty=document.getElementById('empty'), more=document.getElementById('more'), PAGE=20, shown=PAGE;
  function apply(reset){
    if(reset) shown=PAGE;
    var words=q.value.toLowerCase().trim().split(/\s+/).filter(Boolean), t=ft.value, en=fe.value, ty=fy.value;
    var hit=rows.filter(function(r){
      if(t && r.dataset.topics.split('|').indexOf(t)<0) return false;
      if(en && r.dataset.engines.split('|').indexOf(en)<0) return false;
      if(ty && r.dataset.type!==ty) return false;
      return words.every(function(w){return r.dataset.text.indexOf(w)>-1;});
    });
    var s=fs.value; hit.sort(function(a,b){ if(s==='az') return a.querySelector('h3').textContent.localeCompare(b.querySelector('h3').textContent);
      return s==='old' ? a.dataset.date.localeCompare(b.dataset.date) : b.dataset.date.localeCompare(a.dataset.date); });
    rows.forEach(function(r){r.hidden=true;});
    hit.forEach(function(r,i){ list.appendChild(r); r.hidden = i>=shown; });
    count.textContent=hit.length+(hit.length===1?' study':' studies');
    empty.hidden=hit.length>0; more.hidden=hit.length<=shown;
  }
  [q,ft,fe,fy,fs].forEach(function(el){el.addEventListener(el===q?'input':'change',function(){apply(true);});});
  more.addEventListener('click',function(){shown+=PAGE;apply(false);});
  apply(true);
})();
</script>'''

def build(fb, prev=False):
    MAPSRC = "simulations/quiktox-foot-traffic/index.html?embed=1" if prev else "simulations/quiktox-foot-traffic/?embed=1"
    fav = "" if prev else '<link rel="icon" href="/research/favicon.ico" sizes="any"><link rel="icon" href="/research/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/research/apple-touch-icon.png"><link rel="manifest" href="/research/site.webmanifest">'
    return f'''<!doctype html>
<html lang="en-US"><head><meta charset="utf-8"><meta name="color-scheme" content="light"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Local AI Registry Research: Local AEO Studies and Data</title>
<meta name="description" content="{e(DESC)}">
<link rel="canonical" href="{SITE}"><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
{fav}<meta name="theme-color" content="#F4F1EA">
<meta property="og:type" content="website"><meta property="og:locale" content="en_US"><meta property="og:site_name" content="Local AI Registry Research"><meta property="og:title" content="Local AI Registry Research"><meta property="og:description" content="{e(DESC)}"><meta property="og:url" content="{SITE}">
<meta property="og:image" content="{SITE}og/local-ai-registry-research.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:type" content="image/png"><meta property="og:image:alt" content="Local AI Registry Research: How AI sends customers through the door, with a map of a business marked as a verified record"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@LocalAIRegistry"><meta name="twitter:title" content="Local AI Registry Research"><meta name="twitter:description" content="{e(DESC)}"><meta name="twitter:image" content="{SITE}og/local-ai-registry-research.png"><meta name="twitter:image:alt" content="Local AI Registry Research: How AI sends customers through the door">
<link rel="alternate" type="text/plain" href="{SITE}llms.txt" title="llms.txt">
<link rel="preload" href="{fb}hanken-grotesk.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="{fb}cormorant.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face{{font-family:'Hanken Grotesk';src:url({fb}hanken-grotesk.woff2) format('woff2');font-weight:400 700;font-display:swap}}
@font-face{{font-family:'Bricolage Grotesque';src:url({fb}bricolage-grotesque.woff2) format('woff2');font-weight:600 800;font-display:swap}}
@font-face{{font-family:'Cormorant';src:url({fb}cormorant.woff2) format('woff2');font-weight:500 600;font-display:swap}}
:root{{--paper:#F4F1EA;--card:#FBF9F4;--deep:#ECE6D6;--ink:#0B1A2E;--muted:#4A5A72;--blue:#1F4FE0;--line:#D8D2C3;--tint:#E6EBFA;--f-head:"Bricolage Grotesque",system-ui,sans-serif;--f-display:"Cormorant",Georgia,serif}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.6 "Hanken Grotesk",system-ui,sans-serif}}
a{{color:var(--blue)}}p,li{{text-wrap:pretty}}h1,h2,h3{{margin:0;text-wrap:balance}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 16px}}
header.top{{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:20px 0;border-bottom:1px solid var(--line)}}
header.top img{{display:block;width:190px;height:auto}}
header.top nav{{display:flex;gap:18px;font-size:14px;font-weight:600}} header.top nav a{{color:var(--ink);text-decoration:none}}
@media (max-width:600px){{header.top{{flex-wrap:wrap}} header.top img{{width:160px}} header.top nav{{gap:14px;font-size:13px}} header.top nav a:last-child{{display:none}}}}
.k{{font:800 12px var(--f-head);letter-spacing:.1em;text-transform:uppercase;color:var(--blue)}}
.hero-map{{position:relative;width:100vw;margin-left:calc(50% - 50vw);height:max(560px,calc(100svh - 65px));background:#EEDDB8 radial-gradient(ellipse at center,#F3E6C6 0,#E6D2A6 100%);overflow:hidden;border-bottom:1px solid var(--line)}}
.mapbox{{position:absolute;inset:0}} .mapbox iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}
.hero-head{{display:grid;gap:10px}}
.finder{{position:absolute;z-index:6;top:16px;right:16px;width:min(380px,calc(100% - 32px))}}
.btn.big{{font-size:17px;padding:13px 20px;border-radius:10px;box-shadow:0 6px 16px rgba(31,79,224,.28)}}
@media (min-width:641px) and (max-width:1020px){{.hero-card{{top:84px}}}} .finder svg{{position:absolute;left:12px;top:13px;color:var(--muted);pointer-events:none}}
.finder input{{width:100%;font:inherit;font-size:16px;color:#3B2A1A;background:rgba(246,235,208,.88);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);border:1px solid rgba(74,47,27,.32);border-radius:10px;padding:10px 12px 10px 38px;min-height:44px;box-shadow:none}} .finder input::placeholder{{color:#7A6650}} .finder input:focus{{background:#FBF5E6}} .finder svg{{color:#7A6650!important;z-index:2}}
.finder input:focus{{outline:2px solid var(--blue);outline-offset:1px}}
.finder ul{{position:absolute;z-index:20;left:0;right:0;top:calc(100% + 4px);margin:0;padding:4px;list-style:none;background:#fff;border:1px solid var(--line);border-radius:10px;box-shadow:0 12px 28px rgba(11,26,46,.18);max-height:320px;overflow:auto}}
.finder li{{padding:9px 10px;border-radius:6px;cursor:pointer;display:grid;gap:1px}} .finder li[aria-selected=true],.finder li:hover{{background:var(--tint)}}
.finder li b{{font-weight:700;font-size:15px}} .finder li span{{font-size:13px;color:var(--muted)}} .finder li.attr{{cursor:default;font-size:11px;color:var(--muted);text-align:right;padding:4px 10px}} .finder li.none{{cursor:default;color:var(--muted);font-size:14px}} .finder li.cta{{border-top:1px solid var(--line,#e3e6ee);margin-top:4px;padding-top:10px}} .finder li.cta a{{color:var(--blue,#1f4fd8);font-weight:700;font-size:14px;text-decoration:none;white-space:nowrap}} .finder li.cta a:hover,.finder li.cta.on a{{text-decoration:underline}}
.hero-card{{position:absolute;z-index:2;left:max(16px,calc(50vw - 520px));top:20px;max-width:540px;background:rgba(251,249,244,.96);border:1px solid var(--line);border-radius:12px;padding:18px 20px;display:grid;gap:10px;box-shadow:0 10px 30px rgba(11,26,46,.14)}}
.hero-card h1{{font:600 clamp(30px,3.6vw,44px)/1.05 var(--f-display);text-wrap:balance}}
.hero-card p{{margin:0;font-size:15.5px;color:var(--muted)}} .hero-card .fine{{font-size:12px}}
.nojs{{position:absolute;bottom:20px;left:20px}}
@media (max-width:640px){{
 .hero-map{{height:auto;min-height:calc(100svh - 92px);display:flex;flex-direction:column;background:none;overflow:visible;border-bottom:0}}
 .hero-card{{display:contents}}
 .hero-head{{order:1;padding:16px 16px 12px;gap:8px;position:relative;z-index:5}} .hero-head h1{{font-size:30px}} .hero-head p{{display:none}}
 .mapbox{{order:2;position:relative;inset:auto;flex:1 1 auto;min-height:460px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:#EEDDB8}}
 .hero-head .fine{{display:none}} .finder{{top:12px;left:12px;right:12px;width:auto}} .btn.big{{font-size:15px;padding:10px 16px}}}}
.intro{{padding:28px 0 16px;display:grid;gap:8px}}
.intro h1{{font:600 clamp(32px,4.6vw,52px)/1.08 var(--f-display)}}
.mapfig{{margin:0;display:grid;gap:8px}}
.mapframe{{position:relative;height:clamp(420px,calc(100svh - 250px),760px);border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#EEDDB8 radial-gradient(ellipse at center,#F3E6C6 0,#E6D2A6 100%)}}
.mapframe::before{{content:"Loading map";position:absolute;inset:0;display:grid;place-items:center;font:italic 18px var(--f-display);color:#4A2F1B}}
.mapframe iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}
.mapfig figcaption{{font-size:14px;color:var(--muted)}}
.lede{{font-size:19px;color:var(--ink);max-width:780px;margin:24px 0 0}}
.ph{{display:inline-block;font:700 11px/1 var(--f-head);letter-spacing:.06em;text-transform:uppercase;border:1.5px dashed var(--muted);color:var(--muted);border-radius:4px;padding:4px 6px;margin-right:6px;vertical-align:1px}}
.ph.sim{{border-style:solid;border-color:var(--blue);color:var(--blue)}}
.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
.nums{{padding:28px 0 0;display:grid;gap:8px}}
.nums ul{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}}
@media (max-width:760px){{.nums ul{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
.nums li{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 16px;font-size:14px;color:var(--muted)}}
.nums h2{{font:800 clamp(22px,2.6vw,26px)/1.2 var(--f-head)}}
.nums li{{display:flex;flex-direction:column;gap:2px}} .nums .src{{margin-top:auto;padding-top:6px;font-size:12px;color:var(--muted)}}
.nums b{{display:block;font:800 clamp(26px,3.4vw,36px)/1.1 var(--f-head);color:var(--blue);font-variant-numeric:tabular-nums}}
.qa{{border-top:1px solid var(--line);padding-top:12px;display:grid;gap:4px;max-width:780px}} .qa h3{{font:800 17px/1.35 var(--f-head)}} .qa p{{margin:0;color:var(--muted)}}
.lib{{padding:40px 0 0;display:grid;gap:16px}}
.lib-head{{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap}} .lib-head h2{{font:800 clamp(24px,3vw,30px)/1.2 var(--f-head)}}
.lib-count{{margin:0;font-size:14px;color:var(--muted)}}
.lib-tools{{display:grid;grid-template-columns:minmax(0,2.2fr) repeat(4,minmax(0,1fr));gap:8px}}
@media (max-width:900px){{.lib-tools{{grid-template-columns:repeat(2,minmax(0,1fr))}} .lib-tools .srch{{grid-column:1/-1}}}}
.lib-tools select,.lib-tools input{{width:100%;font:inherit;font-size:15px;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;min-height:44px}}
.srch{{position:relative;display:block}} .srch svg{{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:var(--muted)}} .srch input{{padding-left:38px}}
.studies{{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}}
.st{{padding:16px 0;border-bottom:1px solid var(--line);display:grid;gap:6px}}
.st-meta{{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:12.5px;color:var(--muted);align-items:center}}
.st-type{{font:800 11px var(--f-head);letter-spacing:.08em;text-transform:uppercase;color:var(--blue)}} .st-id{{font-variant-numeric:tabular-nums}}
.st h3{{font:800 19px/1.3 var(--f-head)}} .st h3 a{{color:var(--ink);text-decoration:none}} .st h3 a:hover{{text-decoration:underline}}
.st p{{margin:0;font-size:15.5px;color:var(--muted);max-width:820px}}
.st-foot{{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;font-size:13px}}
.st-eng{{color:var(--ink);font-weight:600}}
.tags{{display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0;list-style:none}} .tags li{{background:var(--deep);border-radius:999px;padding:2px 9px;font-size:12px}}
.st-links{{display:flex;gap:12px;margin-left:auto;font-weight:600}}
.is-ph h3,.is-ph p,.is-ph .st-eng{{color:#8A93A3}} .is-ph .st-links span{{color:#A9AFBA}} .is-ph{{background:repeating-linear-gradient(135deg,transparent 0 10px,rgba(216,210,195,.25) 10px 20px)}}
.empty{{color:var(--muted)}} .more{{text-align:center}} .more button{{font:inherit;font-weight:700;padding:10px 18px;border-radius:6px;border:1px solid var(--line);background:var(--card);cursor:pointer}}
.hero{{padding:56px 0 40px;display:grid;gap:16px;max-width:820px}}
.hero h1{{font:600 clamp(40px,7vw,68px)/1.05 var(--f-display)}}
.hero p{{font-size:19px;color:var(--muted);max-width:700px;margin:0}}
.feature{{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:28px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:24px;align-items:center}}
@media (max-width:820px){{.feature{{grid-template-columns:minmax(0,1fr)}}}}
.feature img{{width:100%;height:auto;border-radius:6px;border:1px solid var(--line);display:block}}
.feature h2{{font:800 clamp(23px,3vw,30px)/1.2 var(--f-head);letter-spacing:-.01em}} .feature h2 a{{color:var(--ink);text-decoration:none}}
.feature .body{{display:grid;gap:14px}} .feature p{{margin:0;color:var(--muted)}}
.stats{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:0;padding:0;list-style:none}}
.stats li{{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:10px 12px;font-size:13.5px;line-height:1.35;color:var(--muted)}}
.stats b{{display:block;font:800 26px/1.1 var(--f-head);color:var(--blue);margin-bottom:2px}}
.cta{{display:flex;flex-wrap:wrap;gap:10px}} .btn{{display:inline-block;padding:10px 16px;border-radius:6px;font-weight:700;font-size:15px;text-decoration:none}}
.btn.p{{background:var(--blue);color:#fff}} .btn.s{{border:1px solid var(--line);color:var(--ink);background:var(--card)}}
section.blk{{padding:48px 0 0;display:grid;gap:14px}} section.blk h2{{font:800 clamp(24px,3vw,30px)/1.2 var(--f-head)}}
.grid4{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:14px;margin:0;padding:0;list-style:none}}
.grid4 li{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:16px}} .grid4 h3{{font:800 17px/1.3 var(--f-head);margin-bottom:6px}} .grid4 p{{margin:0;font-size:15px;color:var(--muted)}}
.team p{{max-width:780px;margin:0}} .fine{{font-size:13px;color:var(--muted)}}
.note{{margin-top:48px;background:var(--tint);border-left:3px solid var(--blue);border-radius:4px;padding:18px 20px;display:grid;gap:8px;max-width:820px}}
.note p{{margin:0}} .note .t{{font:600 23px/1.25 var(--f-display)}}
{chrome.CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>
<body>{chrome.header("")}<div class="wrap">
<main>
<section class="hero-map" aria-labelledby="h1">
<div class="mapbox"><iframe id="sim" title="Interactive map: people asking AI assistants and walking to Quiktox, a med spa on Newport Boulevard in Costa Mesa" data-src="{MAPSRC}" allow="fullscreen"></iframe>
<noscript><p class="nojs"><a href="{MAPSRC}">Open the interactive map</a></p></noscript>
<div class="finder" id="finder" data-gkey="{chrome.GOOGLE_PLACES_KEY}" data-contact="{chrome.CONTACT}"><label class="sr" for="gq">Find any business on the map</label>
<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
<input id="gq" type="search" placeholder="Search a business or address" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="gopts" maxlength="120">
<ul id="gopts" role="listbox" hidden></ul></div></div>
<div class="hero-card"><div class="hero-head">
<h1 id="h1">How AI sends customers through the&nbsp;door</h1>
<p>Every day people ask ChatGPT, Claude, Gemini and Google where to go. We study how those answers are made, and which local businesses they&nbsp;name.</p>
<div class="cta"><a class="btn p big" href="#library">Explore the research <span aria-hidden="true">↓</span></a></div>
<p class="fine" id="gstatus" aria-live="polite">Click the pin to see the business on Local AI Registry. Real streets; foot traffic is&nbsp;illustrative.</p></div>
</div>
</section>

<section class="nums" aria-labelledby="numh"><h2 id="numh">Local discovery has moved to&nbsp;AI</h2><ul>
<li><b>45%</b>of consumers ask AI for local business recommendations<a class="src" href="https://www.brightlocal.com/research/lcrs-ai-trust/">BrightLocal, 2026</a></li>
<li><b>900M+</b>people use ChatGPT every&nbsp;week<a class="src" href="https://searchengineland.com/chatgpt-900-million-weekly-active-users-470492">OpenAI, 2026</a></li>
<li><b>1B+</b>monthly users of Google AI Mode, with queries doubling every&nbsp;quarter<a class="src" href="https://blog.google/products-and-platforms/products/search/search-io-2026/">Google, May 2026</a></li>
<li><b>76.4%</b>of local business searches show an AI answer before any&nbsp;link<a class="src" href="local-answer-gap/">Local AI Registry, 2026</a></li></ul></section>

{library(REAL + (PLACE if prev else []))}

<section class="blk" aria-labelledby="study"><h2 id="study">What we study</h2>
<ul class="grid4">
<li><h3>Where AI gets local facts</h3><p>Which sources AI assistants cite when they answer questions about local&nbsp;businesses.</p></li>
<li><h3>What AI can read</h3><p>Which pages, listings and formats AI can actually read and verify.</p></li>
<li><h3>How answers change</h3><p>How wording, timing and the assistant used change who gets&nbsp;recommended.</p></li>
<li><h3>What owners can do</h3><p>Turning every finding into steps a local business can take, tested on real&nbsp;businesses.</p></li></ul></section>

<section class="blk team" id="research-team" aria-labelledby="t"><h2 id="t">About the Local AI Registry Research Team</h2>
{chr(10).join(paras).replace('href="https://localairegistry.com/research/local-answer-gap/#references"','href="local-answer-gap/#references"').replace('href="#references"','href="local-answer-gap/#references"')}
<p>The team also turns its findings into plain-language explainers on the <a href="https://www.youtube.com/@localairegistry">Local AI Registry YouTube channel</a>.</p></section>

<section class="blk" aria-labelledby="use"><h2 id="use">Use our research</h2>
<p style="margin:0;max-width:780px">All charts and findings are free to use with credit under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Every chart has a ready-made embed code, and the data behind each study is downloadable. Please credit “Local AI Registry” and link to the study.</p></section>

<section class="blk" id="faq" aria-labelledby="faqh"><h2 id="faqh">Questions about our research</h2>
{"".join(f'<div class="qa"><h3>{e(q)}</h3><p>{e(a).replace(" free at research.", " free at&nbsp;research.")}</p></div>' for q, a in FAQ)}</section>

<aside class="note"><div class="k">One last thing</div><p class="t">AI is evolving every day. So is our&nbsp;research.</p>
<p>The engines change how they find, read and cite local businesses constantly. Local AI Registry’s dedicated local AI research team keeps testing what works, so the businesses we serve always get the current best&nbsp;approach.</p></aside>
</main>
</div>{chrome.footer("")}<div>
</div>
{JS}
</body></html>'''
out = build("/research/assets/fonts/")
assert "\u2014" not in out and "\u2013" not in out
open(os.path.join(ROOT, "index.html"), "w").write(out)
if PREVIEW:
    open(os.path.join(ROOT, "hub-preview.html"), "w").write(build("assets/fonts/", prev=True))
print(f"Built index.html with {len(REAL)} stud{'y' if len(REAL)==1 else 'ies'}")
