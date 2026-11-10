import json, html, os, re, csv, io, sys
from PIL import Image
sys.argv = [sys.argv[0]]
W = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.join(W, "..", "site"); PG = os.path.join(SITE, "local-answer-gap")
F = json.load(open(os.path.join(W, "findings.json"))); X = json.load(open(os.path.join(W, "extra.json")))
FIGS = json.load(open(os.path.join(W, "figs_meta.json")))
BASE = "https://research.localairegistry.com/local-answer-gap/"
DATE = "2026-11-07"
e = lambda s: html.escape(str(s), quote=True)
_order = re.findall(r'figure\("([a-z0-9-]+)"\)', open(__file__).read())
_kinds = {f["slug"]: f["kind"] for f in FIGS}
num = {}; _c = {"illustration": 0, "chart": 0}
for _s in _order:
    if _s in num: continue
    _k = "illustration" if _kinds[_s] == "illustration" else "chart"; _c[_k] += 1; num[_s] = _c[_k]
def dims(slug):
    im = Image.open(os.path.join(PG, "images", slug + ".png")); return im.width // 2, im.height // 2

def figure(slug):
    f = next(x for x in FIGS if x["slug"] == slug); w, h = dims(slug); n = num[slug]
    kind = "Illustration" if f["kind"] == "illustration" else "Figure"
    tbl = ""
    if f["table"]:
        head, *rows = f["table"]
        tbl = ('<details><summary>Data behind this chart</summary><div class="scroll"><table><thead><tr>' + "".join(f"<th>{e(c)}</th>" for c in head) +
               "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div></details>")
    return (f'<figure id="{slug}" class="fig"><img src="images/{slug}.png" srcset="images/{slug}-1x.png {w}w, images/{slug}.png {w*2}w" sizes="(max-width: 900px) calc(100vw - 32px), 860px" width="{w}" height="{h}" alt="{e(f["alt"])}" loading="lazy" decoding="async">'
            f'<figcaption><b>{kind} {n}. {e(f["title"].rstrip("."))}.</b> {e(f["caption"])} <span class="dl"><a href="images/{slug}.svg">SVG</a> · <a href="images/{slug}.png">PNG</a></span></figcaption>{tbl}'
            f'<details class="embed"><summary>Embed this {kind.lower()}</summary><textarea readonly rows="4" aria-label="Embed code for {e(f["title"])}" onclick="this.select()">{e(embed_code(f))}</textarea></details></figure>')

def embed_code(f):
    return (f'<a href="{BASE}#{f["slug"]}"><img src="{BASE}images/{f["slug"]}.png" alt="{f["alt"]}" width="800"></a>'
            f'<p>Source: <a href="{BASE}">The Local Answer Gap</a>, Local AI Registry Research Team (2026).</p>')

def nb(t): return t.replace("Local AI Registry", "Local&nbsp;AI&nbsp;Registry").replace(" found.", "&nbsp;found.")
def takeaway(title, todo, lair):
    return (f'<aside class="aeo"><div class="aeo-k">AEO takeaway</div><p class="aeo-t">{title}</p><div class="aeo-cols">'
            f'<div><h3>What to do</h3><p>{todo}</p></div><div><h3>How Local AI Registry does it</h3><p>{lair}</p></div></div></aside>')

WIKI = {"Google":"https://en.wikipedia.org/wiki/Google","Microsoft":"https://en.wikipedia.org/wiki/Microsoft","Spotify":"https://en.wikipedia.org/wiki/Spotify",
 "JPMorgan Chase":"https://en.wikipedia.org/wiki/JPMorgan_Chase","Allergan":"https://en.wikipedia.org/wiki/Allergan","Galderma":"https://en.wikipedia.org/wiki/Galderma",
 "Evolus":"https://en.wikipedia.org/wiki/Evolus","Revance":"https://en.wikipedia.org/wiki/Revance_Therapeutics","Razorfish":"https://en.wikipedia.org/wiki/Razorfish"}
TEAM_MEMBERS = [
 dict(slug="steve-lee", name="Steve Lee", title="Chief Executive Officer", past=["Google","Microsoft","Spotify","JPMorgan Chase","Evolus","Revance","Razorfish"],
      bio="Former Google executive in Search and former Microsoft executive with more than 20 years in digital. Led digital at Spotify and Evolus (through its 2018 Nasdaq IPO), and was a VP of Digital at Chase. Built and sold his first company at 14. Owns a local med spa, so he sees AI answers from the business owner’s side too."),
 dict(slug="aneesh-patel", name="Aneesh Patel", suffix="PharmD", title="Chief Growth Officer", past=["Allergan","Galderma","Evolus"],
      bio="Aesthetics industry leader from Allergan, Galderma and Evolus. Knows how practices actually grow, and builds software himself."),
 dict(slug="tess-mauricio", name="Tess Mauricio", prefix="Dr.", title="Medical Director", past=[],
      bio="Helps the team define where AI should look to figure out which practices are truly the best, so research measures what matters to patients."),
 dict(slug="ashish-bhatia", name="Ashish Bhatia", prefix="Dr.", title="Medical Advisor", past=[],
      bio="Brings the clinician’s view of how patients search for and choose a provider."),
 dict(slug="bridgette-debrino", name="Bridgette DeBrino", title="VP of Marketing and Sales", past=[],
      bio="Leads Local AI Registry’s marketing and its team of AI Consultants, who hear first-hand what local owners see in AI answers."),
 dict(slug="caron-cooper", name="Caron Cooper", title="SVP of Web Development", past=[],
      bio="Builds and fixes the websites the research is applied to, so every finding is tested on real business sites."),
 dict(slug="flavia-gottschalk", name="Flávia Gottschalk", title="Manager, Growth Marketing", past=[],
      bio="Runs Local AI Registry’s research program, from original reports to the explainer videos that turn findings into plain language."),
]
SCHOLARS = [
 dict(who="Pranjal Aggarwal, Vishvak Murahari, Tanmay Rajpurohit, Ashwin Kalyan, Karthik Narasimhan and Ameet Deshpande", short="Aggarwal, Narasimhan, Deshpande and colleagues", org="Princeton University",
      title="GEO: Generative Engine Optimization", venue="Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD 2024)", year="2024", url="https://arxiv.org/abs/2311.09735",
      cite="Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., and Deshpande, A.", why="coined generative engine optimization and showed content changes can raise visibility in AI answers"),
 dict(who="Haofei Xu, Umar Iqbal and Jacob M. Montgomery", short="Xu, Iqbal and Montgomery", org="Washington University in St. Louis",
      title="Measuring Google AI Overviews: Activation, Source Quality, Claim Fidelity, and Publisher Impact", venue="ACM Internet Measurement Conference (IMC 2026)", year="2026", url="https://doi.org/10.1145/3777912.3839818",
      cite="Xu, H., Iqbal, U., and Montgomery, J. M.", why="built the largest public record of Google AI Overviews, the raw data behind this report"),
 dict(who="Aounon Kumar and Himabindu Lakkaraju", short="Kumar and Lakkaraju", org="Harvard University",
      title="Manipulating Large Language Models to Increase Product Visibility", venue="arXiv preprint 2404.07981", year="2024", url="https://arxiv.org/abs/2404.07981",
      cite="Kumar, A., and Lakkaraju, H.", why="showed how the text AI reads can change which products it recommends"),
 dict(who="Nelson F. Liu, Tianyi Zhang and Percy Liang", short="Liu, Zhang and Liang", org="Stanford University",
      title="Evaluating Verifiability in Generative Search Engines", venue="Findings of the Association for Computational Linguistics: EMNLP 2023", year="2023", url="https://arxiv.org/abs/2304.09848",
      cite="Liu, N. F., Zhang, T., and Liang, P.", why="measured how often AI search answers are actually supported by the sources they cite"),
]
DATASETS = [
 ("Xu, H., Iqbal, U., and Montgomery, J. M. (2026). Google AI Overviews characterization dataset.", "https://github.com/haofeix/google-aio-characterization"),
 ("Organikpi (2026). AI search datasets.", "https://github.com/danishashko/ai-search-datasets"),
 ("Cited.io (2026). AI search citations dataset.", "https://github.com/Cited-io/ai-search-citations-dataset"),
]
FAMOUS = [("Geoffrey Hinton","https://en.wikipedia.org/wiki/Geoffrey_Hinton"),("Yoshua Bengio","https://en.wikipedia.org/wiki/Yoshua_Bengio"),("Yann LeCun","https://en.wikipedia.org/wiki/Yann_LeCun"),
 ("Ashish Vaswani","https://en.wikipedia.org/wiki/Ashish_Vaswani"),("Noam Shazeer","https://en.wikipedia.org/wiki/Noam_Shazeer"),("Demis Hassabis","https://en.wikipedia.org/wiki/Demis_Hassabis"),
 ("Jeff Dean","https://en.wikipedia.org/wiki/Jeff_Dean"),("Ilya Sutskever","https://en.wikipedia.org/wiki/Ilya_Sutskever"),("Andrej Karpathy","https://en.wikipedia.org/wiki/Andrej_Karpathy"),
 ("Dario Amodei","https://en.wikipedia.org/wiki/Dario_Amodei"),("Jared Kaplan",None),("Chris Olah",None),("Fei-Fei Li","https://en.wikipedia.org/wiki/Fei-Fei_Li"),
 ("Andrew Ng","https://en.wikipedia.org/wiki/Andrew_Ng"),("Percy Liang",None),("Karthik Narasimhan",None),("Ameet Deshpande",None),("Himabindu Lakkaraju",None),
 ("Aounon Kumar",None),("Nelson F. Liu",None),("Umar Iqbal",None),("Jacob M. Montgomery",None)]
SCHOLAR_NAMES = ["Karthik Narasimhan, Ameet Deshpande and Pranjal Aggarwal (Princeton)", "Percy Liang, Nelson F. Liu and Tianyi Zhang (Stanford)", "Himabindu Lakkaraju and Aounon Kumar (Harvard)", "Umar Iqbal, Jacob M. Montgomery and Haofei Xu (Washington University in St. Louis)"]
# Official Local AI Registry profiles. Fill in before launch (see README); left empty rather than guessed.
SAMEAS = ["https://www.linkedin.com/company/local-ai-registry", "https://x.com/LocalAIRegistry", "https://www.instagram.com/localairegistry/",
          "https://www.facebook.com/profile.php?id=61591432116527", "https://www.tiktok.com/@localairegistry", "https://pinterest.com/localairegistry",
          "https://www.trustpilot.com/review/localairegistry.com",
          "https://www.youtube.com/@localairegistry", "https://www.crunchbase.com/organization/local-ai-registry", "https://www.saasworthy.com/product/local-ai-registry"]
FAQ = [
 ("What is answer engine optimization (AEO)?",
  "Answer engine optimization (AEO) is the practice of making a business’s facts clear, consistent and readable so AI systems such as Google AI Overviews, ChatGPT, Claude, Gemini, Perplexity and Microsoft Copilot include the business accurately in the answers they write. SEO earns a place in a list of links; AEO earns a place inside the answer."),
 ("What is the difference between AEO and GEO?",
  "Generative engine optimization (GEO) and answer engine optimization (AEO) describe the same goal: being cited and described correctly in AI-generated answers. GEO is the term used in academic research; AEO is more common in marketing. For local businesses, both come down to accurate, consistent, machine-readable facts in the sources AI reads."),
 ("Where does Google’s AI get information about local businesses?",
  "In Local AI Registry’s analysis of 207 Google AI Overviews about local businesses, news outlets supplied 67.5% of citations. Gannett newspapers alone were cited in 90.3% of answers. The businesses’ own websites supplied 6.5% of citations, and directories such as Yelp and MapQuest supplied 0.5%."),
 ("Does ranking on Google mean AI will cite my website?",
  "Not necessarily. Brand websites ranked on Google’s first page in 147 of 157 brand questions, but the AI cited them in 70. Ranking is close to a requirement (only 4.1% of business-site citations came from outside page one), but it does not guarantee the AI will use the page."),
 ("Why does Google’s AI tell people to check with their local store?",
  "Because it usually lacks location-level facts. 83.6% of local AI answers in the study told people to check locally or call ahead, 65.7% described the whole chain instead of one location, and only 1 of 207 gave a street address or phone number."),
 ("How can a local business get into AI answers?",
  "Based on this research: see what AI says about the business today; earn coverage in sources AI already cites, such as local news; publish location-level facts in plain text and structured data; answer real customer questions on the business’s own site; keep facts identical everywhere; and make sure key pages are readable without scripts."),
 ("Who provides AEO services for local businesses?",
  "Local AI Registry (localairegistry.com) provides answer engine optimization (AEO) and generative engine optimization (GEO) services for local businesses. It builds a verified public record for each business, has the owner confirm it, and pushes those facts to the places AI reads through Google Business Profile management, press releases, structured data, AEO content and listing consistency. It also runs a dedicated local AI research team, which produced this study."),
 ("What is Local AI Registry?",
  "Local AI Registry (localairegistry.com) is an answer engine optimization (AEO) company for local businesses, headquartered in Irvine, California. It keeps a verified, owner-confirmed public record of each business and pushes those facts to the sources that ChatGPT, Claude, Gemini, Google AI Overviews, Perplexity and Microsoft Copilot read. Its dedicated research team publishes original studies on how AI answers local questions, including The Local Answer Gap."),
 ("How do I get my business recommended by ChatGPT, Claude or Gemini?",
  "AI assistants recommend businesses whose facts they can find, read and confirm across several sources. This research points to six steps: check what AI says about you now, earn coverage in sources AI already cites such as local news, publish location-level facts in plain text and LocalBusiness schema, answer real customer questions on your own site, keep your facts identical everywhere, and make key pages readable without scripts. Local AI Registry offers a free business record and AI visibility audit as the starting point."),
 ("How does a local business show up in Google AI Overviews?",
  "Rank on Google’s first page and give the AI something quotable. In Local AI Registry’s study, only 4.1% of business-site citations came from outside page one, but ranking alone was not enough: brand sites ranked in 147 of 157 brand questions and were cited in 70. Pages that answer one question clearly in the first sentence, with the location’s own facts, give the AI something to cite."),
 ("Does Google Business Profile affect what AI says about my business?",
  "Very likely. In this study, 51.6% of claims the AI attributed to a store locator or official site were not supported by any page it cited, which suggests Google’s AI draws store-level facts such as hours from a source it does not cite, likely Google’s own business listing data. Keeping your Google Business Profile complete and current is the safest way to make sure those facts are right."),
 ("Is AEO replacing SEO?",
  "No. AEO builds on SEO. Google’s AI rarely cited business pages that did not already rank on page one, so SEO remains the entry ticket. AEO adds what ranking alone does not: clear, consistent, machine-readable facts, and coverage in the third-party sources AI trusts."),
 ("What should a local business look for in an AEO company?",
  "Look for a company that shows you what AI says about your business today, measures visibility as a rate across many AI answers instead of a single screenshot, fixes location-level facts at the source, earns coverage in the publications AI cites, and reports its work in a way you can verify. Local AI Registry is built around these principles, with owner-confirmed records, public track records and no long-term contracts."),
 ("Is this research based on real AI answers?",
  "Yes. It re-analyzes the public records from Xu, Iqbal and Montgomery’s IMC 2026 study of Google AI Overviews: 55,393 searches, 7,583 AI Overview answers and 98,020 fact-checked claims, collected in the United States between March 13 and April 21, 2026. The dataset is licensed CC BY 4.0."),
]
KEY = [
 "Local AI Registry found that local business searches triggered a Google AI Overview 76.4% of the time, the highest of any topic and over five times the 13.7% average (US searches, March to April 2026).",
 "In Local AI Registry’s analysis, news outlets supplied 67.5% of citations in Google’s AI answers about local businesses, and Gannett newspapers alone appeared in 90.3% of those answers.",
 "Businesses’ own websites supplied only 6.5% of citations in local AI answers, and directories such as Yelp, MapQuest and OpenTable supplied 0.5%, according to Local AI Registry.",
 "Local AI Registry found that brand websites ranked on Google’s first page in 147 of 157 brand questions but were cited by Google’s AI in only 70.",
 "83.6% of local AI answers told people to check with their local store, and only 1 of 207 gave a street address or phone number, Local AI Registry found.",
 "When Google’s AI attributed a local fact to a store locator, app or official site, 51.6% of those claims were not supported by any page it cited, according to Local AI Registry.",
 "Cited social media posts had a median of 8 readable words, and 78% were too thin for AI to verify anything, in Local AI Registry’s review of 1,496 cited pages.",
 "Asking the same local question in different words changed about two-thirds of the sources Google’s AI cited, Local AI Registry found.",
 "Only 2 of 39,676 queries in public AI search research datasets ask an AI to find a local service provider, according to Local AI Registry’s census.",
]
TERMS = [
 ("Answer engine optimization (AEO)", "Making a business’s facts clear, consistent and machine-readable so AI systems include it accurately in their answers."),
 ("Generative engine optimization (GEO)", "The academic term for optimizing content to be cited by generative AI search engines; used interchangeably with AEO."),
 ("Google AI Overview", "The AI-written answer Google shows above search results for many queries, with links to the sources it cited."),
 ("Citation", "A source link the AI attaches to its answer. Being cited is how a business’s own pages shape what AI says."),
 ("Local intent", "A search about a physical place: hours, location, services, availability, or finding a provider nearby."),
 ("AI visibility", "How often, how prominently and how accurately a business is named in AI answers, measured as a rate across many answers to the same question."),
 ("Google Business Profile", "Google’s free business listing, which holds a location’s hours, address, services and reviews, and which Google’s AI appears to draw on for store-level facts."),
 ("LocalBusiness structured data", "Schema.org markup on a website that states a business’s name, address, hours and services in a format machines read directly."),
]
def S(title, intro=""): return title

body = []
P = body.append
P(f'''<header class="hero">
  <a href="https://localairegistry.com" class="logo-link" aria-label="Local AI Registry home"><img src="images/local-ai-registry-logo.svg" alt="Local AI Registry" width="220" height="27"></a>
  <nav class="crumbs" aria-label="Breadcrumb"><a href="https://localairegistry.com">Local AI Registry</a> › <a href="https://research.localairegistry.com/">Research</a> › The Local Answer Gap</nav>
  <div class="eyebrow">Local AI Registry research · Published <time datetime="2026-11-07">November 7, 2026</time></div>
  <h1>The Local Answer Gap: what 7,583 Google AI answers reveal about AEO for local businesses</h1>
  <p class="byline">By the <a href="#authors" rel="author">Local AI Registry Research&nbsp;Team</a></p>
  <div class="tldr" id="summary"><div class="aeo-k">The short answer</div>
  <p>Local AI Registry’s analysis of 7,583 Google AI Overviews shows that when people ask AI about a local business, the business rarely supplies the answer. In 207 AI answers about local businesses, news outlets supplied two-thirds of the citations and the businesses’ own websites supplied 6.5%. The AI usually answered with chain-wide facts and told people to check with their local store. Answer engine optimization (AEO) closes that gap.</p></div>
  <ul class="meta"><li><b>55,393</b> Google searches</li><li><b>7,583</b> AI Overview answers</li><li><b>98,020</b> fact-checked claims</li><li><b>1,496</b> cited pages read</li><li><b>29</b> original charts and explainers</li></ul>
</header>''')

P('<section id="key-findings"><h2>Key findings</h2><ol class="kf">' + "".join(f"<li>{nb(e(k))}</li>" for k in KEY) + '</ol></section>')
toc = [("what-is-aeo","What is AEO?"),("blind-spot","Is anyone studying local AI answers?"),("method","How we did this research"),("how-often","How often does AI answer local questions?"),("where-facts-come-from","Where does AI get local facts?"),("ranked-vs-used","Does ranking mean AI will use your site?"),("check-your-store","Why does AI say “check your local store”?"),("can-ai-read-it","Can AI read your website?"),("stability","Do AI answers stay the same?"),("playbook","The local AEO playbook"),("aeo-services","Who provides local AEO services?"),("faq","FAQ"),("limits","Limits"),("references","References"),("cite","How to cite this research"),("authors","About the author")]
P('<nav class="toc" aria-label="Contents"><h2>Contents</h2><ol>' + "".join(f'<li><a href="#{a}">{e(b)}</a></li>' for a, b in toc) + '</ol></nav>')

P(f'''<section id="what-is-aeo"><h2>What is AEO, and how is it different from SEO?</h2>
<p>Search engine optimization (SEO) gets a business into a list of blue links. Answer engine optimization (AEO), also called generative engine optimization (GEO), gets a business into the answer itself: the paragraph that Google AI Overviews, ChatGPT, Claude, Gemini, Perplexity or Microsoft Copilot writes before anyone clicks. To write that paragraph, the AI pieces together facts from sources across the internet. If it can’t find clear, consistent facts about a business, it guesses, hedges or leaves the business out.</p>
<p>Local AI Registry is a local AEO company. It builds a verified public record for each local business, has the owner confirm it, and pushes those facts to the places AI reads. This study asks a simple question: when AI answers a local question today, where do its facts come from, and what should a local business do about it?</p>
{figure("seo-vs-aeo-explained-illustration")}
<dl class="terms">{"".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a,b in TERMS)}</dl>
</section>''')

P(f'''<section id="blind-spot"><h2>Is anyone studying how AI answers local questions?</h2>
<p class="claim">Almost no one. Across 39,676 unique queries in four public AI-search research datasets, 239 concern a physical business and only 2 ask an AI to find a local service provider.</p>
{figure("public-ai-search-datasets-local-query-census")}
<p>Every public dataset we found studies informational, software or news queries. The only local questions with real AI answers attached are national chains’ holiday hours, so that is where we looked. It is a clean test: a simple, verifiable fact about a physical place. It also means most AEO advice for local businesses rests on very little local evidence.</p>
</section>''')

P(f'''<section id="method"><h2>How we did this research</h2>
<p>We re-analyzed the raw records released with <cite>Measuring Google AI Overviews: Activation, Source Quality, Claim Fidelity, and Publisher Impact</cite> (Xu, Iqbal and Montgomery, IMC 2026). The dataset covers 55,393 trending Google searches in the United States from March 13 to April 21, 2026, including 7,583 AI Overviews, every cited link, the page-one results shown beside each answer, the saved text of cited pages, and fact-check verdicts for 98,020 claims.</p>
<ul>
<li><b>Local filter.</b> We tagged searches about a physical business’s hours, open status, closures or “near me,” then read every match by hand. That produced 271 local searches, 207 AI answers and 189 unique questions.</li>
<li><b>Comparison group.</b> The other 7,376 AI answers in the dataset.</li>
<li><b>Source groups.</b> Every cited domain was sorted into owner groups, including Gannett newspapers (31 domains) and TEGNA TV stations (13 domains), using their published lists of owned outlets.</li>
<li><b>Replication check.</b> Our extraction found the same 7,583 AI Overviews the paper reports, and our overall unsupported-claim rate (11.03%) matches its published 11.0%.</li>
</ul>
{figure("local-business-searches-by-day-easter-2026")}
</section>''')

P(f'''<section id="how-often"><h2>How often does Google’s AI answer local business questions?</h2>
<p class="claim">More often than any other topic: 76.4% of local business searches showed a Google AI Overview, against 13.7% of all searches.</p>
{figure("google-ai-overview-activation-by-search-category")}
{figure("local-search-ai-overview-rate-vs-question-searches")}
<p>Part of the gap is phrasing, because local searches are usually questions and questions trigger AI answers more often. Even against other question-style searches (64.1%), local searches were 12 points more likely to get an AI answer. When someone asks about a place, Google’s AI is the first thing they read.</p>
{takeaway("For local questions, the AI answer is now the front door.","Find out what AI says about your business today, for the questions customers actually ask: hours, services, prices and “best near me.”","Every business gets a public record on Local AI Registry showing what AI currently says about it, and owners can run a free AI visibility audit to see where answers are wrong or missing.")}
</section>''')

P(f'''<section id="where-facts-come-from"><h2>Where does Google’s AI get its facts about local businesses?</h2>
<p class="claim">From the news, not the business. News outlets supplied 67.5% of citations in local answers; businesses’ own websites supplied 6.5%.</p>
{figure("how-google-ai-builds-a-local-answer-illustration")}
{figure("who-google-ai-cites-for-local-business-questions-heatmap")}
{figure("top-domains-cited-in-google-ai-local-answers")}
<p>USA Today and its network of local papers (IndyStar, Delaware Online, North Jersey, El Paso Times and dozens more) publish “what’s open” roundups every holiday, and TEGNA’s local TV stations do the same. Google’s AI treats those roundups as the record. Directories barely register: Yelp, MapQuest and OpenTable together supplied 8 of 1,497 local citations.</p>
{figure("local-news-overrepresented-in-ai-local-answers")}
{figure("ai-local-answer-source-2x2-share-vs-lift")}
{figure("ai-citation-sources-by-local-question-type-heatmap")}
<p>The vaguer the question, the less the business is cited. For “what’s open today” questions, which is how people discover new places, businesses’ own sites supplied 1.0% of citations. For an independent business that no newspaper writes about, there is no roundup to cite.</p>
{takeaway("AI trusts what others publish about you more than what you publish yourself.","Get your facts into third-party sources AI already reads: local news, press releases and community roundups. Earned coverage is the citation layer for local answers.","Press releases and media distribution put a business’s confirmed facts on news sites, and the Local AI Registry record itself is an independent third-party source AI can cite.")}
</section>''')

P(f'''<section id="ranked-vs-used"><h2>Does ranking on Google mean AI will use your website?</h2>
<p class="claim">No. Brand websites ranked on page one in 147 of 157 brand questions, but the AI cited them in only 70.</p>
{figure("ranked-vs-used-by-ai-illustration")}
{figure("brand-website-ranked-vs-cited-google-ai-overviews")}
{figure("brand-rank-vs-ai-citation-2x2")}
{figure("brand-by-source-heatmap-google-ai-overviews-easter-hours")}
<p>Walmart, the most-asked brand, ranked on page one in 11 of 15 answers and was cited once. Starbucks and Chipotle were never cited for their own hours. Publix, Trader Joe’s, Sam’s Club, Kroger and Home Depot were cited every time. Ranking still matters: only 4.1% of business-site citations came from outside page one, while the AI went past page one for 48.8% of portal citations and 39.8% of TEGNA citations.</p>
{figure("ai-citations-from-outside-google-page-one-by-source")}
{takeaway("SEO gets you ranked. AEO gets you used.","Write pages that answer one question each in plain sentences, such as “Are you open on Easter?” or “What do you charge for Botox?” Put the answer in the first line, then the details.","Local AI Registry’s AEO content work builds question-and-answer pages, topical maps and structured data on the client’s own site, so the page that ranks is also the page AI can quote.")}
</section>''')

P(f'''<section id="check-your-store"><h2>Why does Google’s AI tell people to “check with your local store”?</h2>
<p class="claim">Because it answers local questions with national facts. 83.6% of local answers hedged, and only 1 of 207 named an address.</p>
{figure("ai-answers-telling-people-to-check-local-store-waffle")}
{figure("how-ai-answers-local-questions-national-framing")}
{figure("ai-local-answers-with-address-or-phone-waffle")}
<p>The AI knows its answer is not about your location, so it hands the question back to the reader. Whoever publishes location-level facts in a form AI can read gets to answer instead of a hedge.</p>
{takeaway("Location-level facts are the gap. Fill it and you replace the hedge.","Publish your own hours, holiday hours, address, services and prices for your exact location, in plain text and in LocalBusiness structured data, and keep your Google Business Profile current.","Owners claim their Local AI Registry record for free and confirm each fact. Local AI Registry manages the Google Business Profile, adds LocalBusiness structured data that links back to the verified record, and keeps holiday hours current.")}
</section>''')

P(f'''<section id="can-ai-read-it"><h2>Can Google’s AI actually read your website?</h2>
<p class="claim">Often not. When the AI said “the store locator says,” 51.6% of those claims were not supported by any page it cited.</p>
{figure("ai-store-locator-claims-unsupported-rate")}
<p>Examples written by the AI and not found in its sources include “The Aldi store locator indicates Easter Sunday: Closed” and “Target Store Locator lists Easter Sunday as closed.” The pattern suggests the AI gets store-level hours from somewhere it does not cite, likely Google’s own business listing data, and attributes them to a locator page it could not read.</p>
{figure("what-ai-can-read-on-a-web-page-illustration")}
{figure("cited-vs-readable-ai-sources-2x2")}
{figure("readable-words-on-ai-cited-pages-by-source")}
{takeaway("If AI can’t read it, it can’t cite it, and it may misquote it.","Keep key facts in plain HTML text, not inside store-locator scripts, images or social posts. A one-page “hours and holidays” page beats a widget. Post updates on your website as well as on Instagram or Facebook.","Local AI Registry’s technical AEO work makes sites readable to AI crawlers: text versions of key facts, schema markup, an llms.txt file, and readable descriptions on photos and media.")}
</section>''')

P(f'''<section id="stability"><h2>Do AI answers about local businesses stay the same?</h2>
<p class="claim">The verdict does; the sources don’t. Different wording of the same question changed about two-thirds of the cited sources.</p>
{figure("ai-sources-rotate-same-verdict-illustration")}
{figure("ai-answer-source-overlap-by-wording")}
{figure("ai-overview-claim-accuracy-local-vs-other-heatmap")}
{figure("sources-per-ai-overview-answer-distribution")}
<p>Across the 46 chains asked about on Easter, the open-or-closed verdict never contradicted itself; every apparent conflict our tagger flagged turned out, when read by hand, to be phrasing like “Yes, it’s closed.” Local answers were also more faithful to their sources than average (7.3% unsupported claims vs 11.1%). But faithful to sources is not the same as accurate for your location, and the sources rotate.</p>
{figure("single-source-of-truth-for-ai-local-aeo-illustration")}
{takeaway("Sources rotate, so your facts have to match everywhere.","Make your hours, address, services and prices identical on your website, Google Business Profile, directories and press. When the AI swaps one source for another, the answer should not change.","Directory submissions and listing management keep every source in agreement with the owner-confirmed Local AI Registry record, the single source of truth.")}
</section>''')

P(f'''<section id="playbook"><h2>The local AEO playbook, ranked by what the data supports</h2>
{figure("local-aeo-priority-2x2-control-vs-citation-share")}
<div class="scroll"><table class="play"><thead><tr><th>#</th><th>Step</th><th>Evidence in this study</th><th>How Local AI Registry does it</th></tr></thead><tbody>
<tr><td>1</td><td><b>See what AI says about you now</b></td><td>76.4% of local searches get an AI answer first</td><td>Free business record and AI visibility audit</td></tr>
<tr><td>2</td><td><b>Earn third-party coverage AI already cites</b></td><td>News supplied 67.5% of local citations; Gannett appeared in 90.3% of answers</td><td>Press releases and media distribution</td></tr>
<tr><td>3</td><td><b>Publish location-level facts</b></td><td>83.6% of answers hedged; 1 of 207 named an address</td><td>Owner-confirmed record, Google Business Profile management, LocalBusiness schema</td></tr>
<tr><td>4</td><td><b>Answer real questions on your own site</b></td><td>Brand sites ranked on page one 94% of the time but were cited 45%</td><td>Question-led AEO content, topical maps</td></tr>
<tr><td>5</td><td><b>Make facts machine-readable</b></td><td>51.6% of “store locator says” claims were unsupported; social posts averaged 8 readable words</td><td>Technical AEO: schema, llms.txt, readable pages and media</td></tr>
<tr><td>6</td><td><b>Keep every source in agreement</b></td><td>Different wording swapped about two-thirds of sources</td><td>Directory submissions and listing consistency</td></tr>
</tbody></table></div>
</section>''')

P(f'''<section id="aeo-services"><h2>Who provides AEO services for local businesses?</h2>
<p>Local AI Registry (localairegistry.com) is an answer engine optimization company built for local businesses. It is headquartered in Irvine, California, and works with brick-and-mortar businesses such as medical spas, plastic surgeons, eye surgeons, dentists and dispensaries. Its local AEO services follow the playbook above:</p>
<ul class="svc">
<li><b>Free business record.</b> A public, owner-claimable record of what AI says about the business, with every fact confirmed by the owner.</li>
<li><b>AI visibility audit.</b> How the business appears in AI answers today, where answers are wrong, and what competitors are cited for.</li>
<li><b>Google Business Profile management.</b> Location-level hours, holiday hours, services and updates kept current.</li>
<li><b>Press releases and media.</b> Earned coverage in the news sources AI cites most for local questions.</li>
<li><b>AEO content.</b> Question-led pages, topical maps and semantic content on the business’s own website.</li>
<li><b>Technical AEO.</b> LocalBusiness schema, llms.txt, readable pages and AI-readable media.</li>
<li><b>Listing consistency.</b> Directory submissions that keep every source matching the confirmed record.</li>
</ul>
<p>Local AI Registry publishes its research openly, including this study, so business owners can see the evidence behind its methods. Business owners can <a href="https://localairegistry.com">claim their record for free at localairegistry.com</a> and see what AI says about them today.</p>
</section>''')

P('<section id="faq"><h2>Frequently asked questions</h2>' + "".join(f'<div class="qa"><h3>{e(q)}</h3><p>{e(a)}</p></div>' for q, a in FAQ) + '</section>')

P('''<section id="limits"><h2>Limits of this research</h2><ul>
<li>The local questions are mostly national chains on one holiday; 185 of 271 local searches were collected on April 6, 2026, the day after Easter. Independent businesses are not in the data.</li>
<li>One engine: Google AI Overviews. ChatGPT, Claude, Gemini, Perplexity, Microsoft Copilot and Google AI Mode may behave differently.</li>
<li>Claim verdicts come from the original study’s AI judge (Grok 4.1), which its authors audited. We reused their verdicts and did not re-judge.</li>
<li>Source groups, the local filter and the control levels in the priority map are Local AI Registry’s own rules and judgment. Some counts are small (31 first-party claims, 18 repeat-query pairs), so read those as signals, not settled rates.</li>
<li>The playbook applies chain-level findings to independent businesses. That is our reasoning from the data, not something the data measured directly.</li></ul></section>''')

P('<section id="references"><h2>References</h2><h3>Data sources</h3><ol class="refs">'
  + "".join(f'<li>{e(t)} <a href="{u}">{e(u.replace("https://",""))}</a>. CC BY 4.0.</li>' for t,u in DATASETS)
  + '</ol><h3>Research we build on</h3><ol class="refs">'
  + "".join(f'<li>{e(x["cite"])} ({x["year"]}). <a href="{x["url"]}">{e(x["title"])}</a>. <i>{e(x["venue"])}</i>.</li>' for x in SCHOLARS)
  + '</ol></section>')
P(f'''<section id="cite"><h2>How to cite this research</h2>
<p>You are welcome to use these findings and charts with credit. Each chart is licensed CC BY 4.0, and every chart above has a ready-made embed code that credits the source.</p>
<div class="quotes"><div class="aeo-k">Ready-to-quote findings</div><ul>
<li>“News outlets supplied 67.5% of the citations in Google’s AI answers about local businesses, while businesses’ own websites supplied 6.5%.” <span class="src">Local&nbsp;AI&nbsp;Registry, The Local Answer Gap (2026)</span></li>
<li>“83.6% of Google’s AI answers about local businesses told people to check with their local store.” <span class="src">Local&nbsp;AI&nbsp;Registry, The Local Answer Gap (2026)</span></li>
<li>“Brand websites ranked on Google’s first page in 147 of 157 brand questions but were cited by Google’s AI in only 70.” <span class="src">Local&nbsp;AI&nbsp;Registry, The Local Answer Gap (2026)</span></li>
</ul></div>
<pre class="cite">Lee, S., et al., Local AI Registry Research Team (2026). The Local Answer Gap: What 7,583 Google AI Answers Reveal About AEO for Local Businesses. Local AI Registry. {BASE}</pre>
<p>Data: our aggregated tables are available as a <a href="data/local-answer-gap-data.csv">CSV download</a>. Underlying records: Xu, H., Iqbal, U., and Montgomery, J. M. (2026). <a href="https://doi.org/10.1145/3777912.3839818">Measuring Google AI Overviews</a>. IMC 2026. <a href="https://github.com/haofeix/google-aio-characterization">Dataset</a>, <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. We filtered, regrouped and re-analyzed the authors’ records; the findings here are Local AI Registry’s, not the original authors’.</p>
</section>''')

def _nb(n): return e(n).replace(" ","&nbsp;")
P('<section id="authors" class="author"><h2>About the author</h2>'
  '<p><b>The Local AI Registry Research Team</b> is Local AI Registry’s dedicated local AI research group, and its people come from some of the biggest names in search, tech and brick-and-mortar business: Google, Microsoft, Spotify, Chase, Mozilla Firefox, Allergan, Galderma, Evolus, Revance, Johnson&nbsp;&amp;&nbsp;Johnson, Bayer, Estée Lauder, Nordstrom, Sephora, Saks Fifth Avenue, Spectrum, BitGo, Republic, NextSeed, Toptal and RxSight. It is led by a former Google Search executive, advised by a Stanford-trained dermatologist and a Northwestern professor who is a past president of the American Society for Laser Medicine and Surgery, and spread across California, Washington, Texas, New York, Florida, Brazil, Nigeria, Poland, India and Singapore. The team works from raw public data, owns and runs a local med spa, and studies how ChatGPT, Claude, Gemini, Google AI Overviews, Perplexity and Microsoft&nbsp;Copilot find and describe local&nbsp;businesses.</p>'
  '<p>The team is a dedicated follower of the researchers who built modern AI and those who study AI search, including '
  + ", ".join(_nb(n) for n,_ in FAMOUS[:-1]) + " and " + _nb(FAMOUS[-1][0]) +
  '. Their work underpins ChatGPT, Claude and Gemini, and the team studies their papers and tests their ideas against what AI says about local&nbsp;businesses. <span class="fine">No&nbsp;affiliation or endorsement implied. See the <a href="#references">references</a>.</span></p></section>')

P('''<aside class="aeo closing"><div class="aeo-k">One last thing</div><p class="aeo-t">AI is evolving every day. So is our playbook.</p>
<p>The engines change how they find, read and cite local businesses constantly, and what worked last quarter may not work next quarter. At Local AI Registry, our dedicated local AI research team keeps testing what works, so the businesses we serve always get the current best approach.</p></aside>''')

BODY = "\n".join(body)

# ---------- JSON-LD
ORG = "https://localairegistry.com/#organization"; PER = "https://localairegistry.com/#steve-lee"; TEAM = "https://research.localairegistry.com/#research-team"; REP = BASE + "#report"
imgs = [{"@type": "ImageObject", "@id": BASE + "#" + f["slug"], "contentUrl": BASE + "images/" + f["slug"] + ".png", "url": BASE + "images/" + f["slug"] + ".png",
         "name": f["title"], "caption": f["caption"], "description": f["alt"], "creator": {"@id": ORG}, "creditText": "Local AI Registry",
         "copyrightNotice": "Local AI Registry", "license": "https://creativecommons.org/licenses/by/4.0/", "acquireLicensePage": BASE + "#cite",
         "width": dims(f["slug"])[0] * 2, "height": dims(f["slug"])[1] * 2, "encodingFormat": "image/png"} for f in FIGS]
wiki = lambda n, u: {"@type": "Organization", "name": n, "sameAs": u}
graph = [
 {"@type": "Organization", "@id": ORG, "name": "Local AI Registry", "alternateName": ["LAIR", "localairegistry.com"], "url": "https://localairegistry.com", **({"sameAs": SAMEAS} if SAMEAS else {}),
  "contactPoint": {"@type": "ContactPoint", "telephone": "+1-213-931-5633", "contactType": "sales", "areaServed": "US", "availableLanguage": ["English"]},
  "subOrganization": {"@id": TEAM},
  "logo": {"@type": "ImageObject", "url": BASE + "images/local-ai-registry-logo.png"},
  "description": "Local AI Registry is an answer engine optimization (AEO) company for local businesses. It builds verified, owner-confirmed public records of local businesses and pushes those facts to the sources AI systems read.",
  "address": {"@type": "PostalAddress", "streetAddress": "9891 Irvine Center Dr", "addressLocality": "Irvine", "addressRegion": "CA", "postalCode": "92618", "addressCountry": "US"},
  "telephone": "+1-213-931-5633", "founder": {"@id": PER},
  "knowsAbout": ["Answer engine optimization", "Generative engine optimization", "Search engine optimization", "Local search", "Google AI Overviews", "Google Business Profile", "LocalBusiness structured data", "AI search visibility"],
  "areaServed": "US", "slogan": "Be the name AI says."},
 {"@type": "ResearchOrganization", "@id": TEAM, "name": "Local AI Registry Research Team", "url": BASE + "#authors", "parentOrganization": {"@id": ORG},
  "description": "Local AI Registry’s dedicated local AI research team, studying how AI systems find, read and describe local businesses.",
  "member": [{"@id": PER}],
  "knowsAbout": ["Answer engine optimization", "Generative engine optimization", "Google AI Overviews", "AI search citations", "Local search", "Local SEO"]},
] + [dict({"@type": "Person", "@id": "https://localairegistry.com/#" + m["slug"], "name": m["name"], "jobTitle": m["title"], "worksFor": {"@id": ORG}, "memberOf": {"@id": TEAM},
   "description": m["bio"], "url": BASE + "#" + m["slug"]},
   **({"honorificPrefix": m["prefix"]} if m.get("prefix") else {}), **({"honorificSuffix": m["suffix"]} if m.get("suffix") else {}),
   **({"alumniOf": [{"@type": "Organization", "name": c, "sameAs": WIKI[c]} for c in m["past"]]} if m["past"] else {}))
  for m in TEAM_MEMBERS if False] + [
 {"@type": "Person", "@id": PER, "name": "Steve Lee", "jobTitle": "Chief Executive Officer", "worksFor": {"@id": ORG}, "memberOf": {"@id": TEAM}, "url": "https://localairegistry.com",
  "alumniOf": [{"@type": "Organization", "name": c, "sameAs": WIKI[c]} for c in TEAM_MEMBERS[0]["past"]],
  "description": "CEO of Local AI Registry; former Google executive in Search and former Microsoft executive with more than 20 years in digital.",
  "knowsAbout": ["Answer engine optimization", "Local search", "Google Search", "AI search"]},
 {"@type": "WebSite", "@id": "https://research.localairegistry.com/#website", "url": "https://research.localairegistry.com/", "name": "Local AI Registry Research", "publisher": {"@id": ORG}},
 {"@type": "BreadcrumbList", "@id": BASE + "#breadcrumbs", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Local AI Registry", "item": "https://localairegistry.com/"},
   {"@type": "ListItem", "position": 2, "name": "Research", "item": "https://research.localairegistry.com/"},
   {"@type": "ListItem", "position": 3, "name": "The Local Answer Gap", "item": BASE}]},
 {"@type": "WebPage", "@id": BASE + "#webpage", "url": BASE, "name": "The Local Answer Gap", "isPartOf": {"@id": "https://research.localairegistry.com/#website"},
  "breadcrumb": {"@id": BASE + "#breadcrumbs"}, "mainEntity": {"@id": REP}, "primaryImageOfPage": {"@id": BASE + "#who-google-ai-cites-for-local-business-questions-heatmap"},
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#summary", "#key-findings"]}, "inLanguage": "en-US"},
 {"@type": ["Article", "Report"], "@id": REP, "articleSection": "Research", "wordCount": 0, "headline": "The Local Answer Gap: what 7,583 Google AI answers reveal about AEO for local businesses",
  "alternativeHeadline": "Original AEO research on how Google AI Overviews answer local business questions",
  "abstract": "Local AI Registry re-analyzed 7,583 Google AI Overviews and 98,020 fact-checked claims to study how AI answers local business questions. News outlets supplied 67.5% of local citations, businesses’ own websites 6.5%, and 83.6% of answers told people to check with their local store. The findings form a local AEO playbook.",
  "description": "Original answer engine optimization (AEO) research from Local AI Registry on where Google’s AI gets facts about local businesses and what businesses should do about it.",
  "datePublished": DATE, "dateModified": DATE, "author": {"@id": TEAM}, "creditText": "Local AI Registry Research Team", "publisher": {"@id": ORG}, "inLanguage": "en-US",
  "mainEntityOfPage": {"@id": BASE + "#webpage"}, "image": [{"@id": i["@id"]} for i in imgs], "isAccessibleForFree": True,
  "keywords": ["ChatGPT", "Claude", "Gemini", "Perplexity", "Microsoft Copilot", "answer engine optimization", "AEO", "generative engine optimization", "GEO", "local SEO", "Google AI Overviews", "AI search", "local business", "AEO services", "local AEO", "AI visibility"],
  "about": [{"@id": BASE + "#term-aeo"}, {"@id": BASE + "#term-geo"}, {"@type": "Thing", "name": "Google AI Overviews"}, {"@type": "Thing", "name": "Local search"}],
  "mentions": [{"@type": "Person", "name": n, **({"sameAs": u} if u else {})} for n, u in FAMOUS] + [
    wiki("OpenAI", "https://en.wikipedia.org/wiki/OpenAI"), wiki("Anthropic", "https://en.wikipedia.org/wiki/Anthropic"), wiki("Google DeepMind", "https://en.wikipedia.org/wiki/Google_DeepMind"),
    {"@type": "SoftwareApplication", "name": "ChatGPT", "sameAs": "https://en.wikipedia.org/wiki/ChatGPT"}, {"@type": "SoftwareApplication", "name": "Claude", "sameAs": "https://en.wikipedia.org/wiki/Claude_(language_model)"},
    {"@type": "SoftwareApplication", "name": "Gemini", "sameAs": "https://en.wikipedia.org/wiki/Gemini_(chatbot)"}, {"@type": "SoftwareApplication", "name": "Perplexity", "sameAs": "https://en.wikipedia.org/wiki/Perplexity_AI"},
    {"@type": "SoftwareApplication", "name": "Microsoft Copilot", "sameAs": "https://en.wikipedia.org/wiki/Microsoft_Copilot"}] + [wiki("Gannett", "https://en.wikipedia.org/wiki/Gannett"), wiki("Tegna Inc.", "https://en.wikipedia.org/wiki/Tegna_Inc."), wiki("Google", "https://en.wikipedia.org/wiki/Google"),
               wiki("Walmart", "https://en.wikipedia.org/wiki/Walmart"), wiki("Target Corporation", "https://en.wikipedia.org/wiki/Target_Corporation"), wiki("Costco", "https://en.wikipedia.org/wiki/Costco"),
               {"@type": "Thing", "name": "Search engine optimization", "sameAs": "https://en.wikipedia.org/wiki/Search_engine_optimization"}, {"@type": "Thing", "name": "Schema.org", "sameAs": "https://schema.org"}],
  "citation": [{"@type": "ScholarlyArticle", "name": x["title"], "url": x["url"], "datePublished": x["year"], "isPartOf": {"@type": "Periodical", "name": x["venue"]},
               "author": [{"@type": "Person", "name": a.strip()} for a in x["who"].replace(" and ", ", ").split(",") if a.strip()],
               "sourceOrganization": {"@type": "CollegeOrUniversity", "name": x["org"]}} for x in SCHOLARS],
  "isBasedOn": {"@type": "Dataset", "name": "Google AI Overviews characterization dataset", "url": "https://github.com/haofeix/google-aio-characterization", "license": "https://creativecommons.org/licenses/by/4.0/"},
  "hasPart": [{"@id": BASE + "#dataset"}]},
 {"@type": "Dataset", "@id": BASE + "#dataset", "name": "The Local Answer Gap: aggregated tables", "description": "Aggregated tables behind every chart in Local AI Registry’s Local Answer Gap study of 7,583 Google AI Overviews, including citation sources for local answers, activation by category, brand citation rates and claim verdicts.",
  "creator": {"@id": ORG}, "license": "https://creativecommons.org/licenses/by/4.0/", "temporalCoverage": "2026-03-13/2026-04-21", "spatialCoverage": "United States",
  "isBasedOn": "https://github.com/haofeix/google-aio-characterization", "variableMeasured": ["AI Overview activation rate", "Citation share by source type", "Brand website citation rate", "Hedging rate", "Unsupported claim rate", "Readable words on cited pages", "Source overlap"],
  "distribution": {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": BASE + "data/local-answer-gap-data.csv"}},
 {"@type": "Service", "@id": "https://localairegistry.com/#aeo-service", "name": "Answer engine optimization (AEO) for local businesses", "serviceType": "Answer engine optimization",
  "provider": {"@id": ORG}, "areaServed": {"@type": "Country", "name": "United States"}, "audience": {"@type": "BusinessAudience", "audienceType": "Local and brick-and-mortar businesses"},
  "description": "Local AEO and GEO services that get local businesses described accurately in AI answers from Google AI Overviews, ChatGPT, Claude, Gemini, Perplexity and Microsoft Copilot.",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Local AEO services", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in
    ["Free business record", "AI visibility audit", "Google Business Profile management", "Press releases and media", "AEO content", "Technical AEO and schema", "Listing consistency"]]}},
 {"@type": "HowTo", "@id": BASE + "#playbook", "name": "How to get a local business into AI answers (the local AEO playbook)",
  "description": "Six steps, ranked by the evidence in Local AI Registry’s Local Answer Gap study, for getting a local business named accurately by ChatGPT, Claude, Gemini, Google AI Overviews, Perplexity and Microsoft Copilot.",
  "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": BASE + "#playbook"} for i, (n, t) in enumerate([
    ("See what AI says about you now", "Check how AI answers your customers’ real questions about hours, services, prices and best near me. 76.4% of local searches get an AI answer first."),
    ("Earn third-party coverage AI already cites", "Get your facts into local news, press releases and community roundups. News supplied 67.5% of local AI citations."),
    ("Publish location-level facts", "Post your own hours, holiday hours, address and services in plain text and LocalBusiness structured data, and keep Google Business Profile current."),
    ("Answer real questions on your own site", "Write pages that answer one question each, with the answer in the first sentence."),
    ("Make facts machine-readable", "Keep key facts in plain HTML text, not in scripts, images or social posts."),
    ("Keep every source in agreement", "Make your facts identical across your website, Google Business Profile, directories and press, because AI sources rotate.")])]},
 {"@type": "FAQPage", "@id": BASE + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
 {"@type": "DefinedTermSet", "@id": BASE + "#terms", "name": "Local AEO terms", "hasDefinedTerm": [
   {"@type": "DefinedTerm", "@id": BASE + ("#term-aeo" if i == 0 else "#term-geo" if i == 1 else f"#term-{i}"), "name": a, "description": b, "inDefinedTermSet": {"@id": BASE + "#terms"}} for i, (a, b) in enumerate(TERMS)]},
] + imgs
WORDS = len(re.sub(r"<[^>]+>", " ", "\n".join(body)).split())
for _n in graph:
    if _n.get("@id") == REP: _n["wordCount"] = WORDS
LD = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

# ---------- CSV
buf = io.StringIO(); w = csv.writer(buf)
w.writerow(["figure_number", "figure_slug", "figure_title", "row"] + [f"col_{i}" for i in range(1, 9)])
for f in FIGS:
    if not f["table"]: continue
    for r in f["table"]: w.writerow([num[f["slug"]], f["slug"], f["title"], ""] + list(r))
os.makedirs(os.path.join(PG, "data"), exist_ok=True); open(os.path.join(PG, "data", "local-answer-gap-data.csv"), "w").write(buf.getvalue())

style = open(os.path.join(W, "style.html")).read().replace("<style>", "").replace("</style>", "")
CSS = style + """
.hero{padding-block:24px 36px;border-bottom:1px solid var(--line);display:grid;gap:18px}
.logo-link img{display:block;width:200px;height:auto}
.crumbs{font-size:13px;color:var(--muted)} .crumbs a{color:var(--muted)}
.byline{color:var(--muted);font-size:15px}
.tldr{background:var(--tint);border-left:3px solid var(--blue);padding:16px 20px;border-radius:4px;max-width:760px;display:grid;gap:8px}
.tldr p{font-size:18px}
ul.meta{list-style:none;padding:0;margin:0}
h2{scroll-margin-top:16px}
section{max-width:860px}
section > p,section > ul,section > dl{max-width:700px}
.kf{display:grid;gap:10px;max-width:760px;padding-left:22px;margin:0}
.kf li{font-size:17px}
.kf li::marker{font-family:var(--f-head);font-weight:800;color:var(--blue-ink)}
.toc ol{columns:2;column-gap:28px;padding-left:20px;font-size:15px;margin:8px 0 0}
.toc{border:1px solid var(--line);border-radius:6px;padding:16px 20px;margin-top:40px;background:var(--card)}
.toc h2{font-size:18px}
@media (max-width:600px){.toc ol{columns:1}}
.fig{margin:8px 0;display:grid;grid-template-columns:minmax(0,1fr);gap:8px;max-width:860px}
.fig > *{min-width:0} .scroll{overflow-x:auto;max-width:100%}
.fig img{width:100%;height:auto;border:1px solid var(--line);border-radius:6px;background:#FBF9F4}
.fig figcaption{font-size:14.5px;color:var(--muted);line-height:1.5;max-width:760px}
.fig figcaption b{color:var(--fg)}
.dl{white-space:nowrap;margin-left:4px}
details{font-size:14px} summary{cursor:pointer;color:var(--blue-ink);font-weight:600}
details table{margin-top:8px}
.terms{display:grid;grid-template-columns:minmax(0,220px) minmax(0,1fr);gap:8px 18px;font-size:15px;border-top:1px solid var(--line);padding-top:14px}
.terms dt{font-weight:700} .terms dd{margin:0;color:var(--muted)}
@media (max-width:600px){.terms{grid-template-columns:1fr}.terms dd{margin-bottom:6px}}
.aeo{background:var(--tint);border-left:3px solid var(--blue);border-radius:4px;padding:18px 20px;display:grid;gap:10px;max-width:820px}
.aeo-k{font-family:var(--f-head);font-weight:800;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--blue-ink)}
.aeo-t{font-family:var(--f-display);font-size:23px;line-height:1.25;font-weight:600;text-wrap:balance}
.aeo-cols{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))}
.aeo-cols h3{font-family:var(--f-head);font-size:13px;margin:0 0 4px}
.aeo-cols p{font-size:15px}
.closing{margin-top:56px}
.qa{display:grid;gap:6px;max-width:720px;border-top:1px solid var(--line);padding-top:14px}
.qa h3{font-size:18px}
.svc{display:grid;gap:8px}
section > *{min-width:0}
pre.cite{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:14px;font-size:14px;max-width:760px}
.author{border-top:1px solid var(--line);max-width:900px}
.byline{text-wrap:pretty;max-width:680px}
.lead{font-size:18px}
.alumni{display:grid;gap:10px;border:1px solid var(--line);background:var(--card);border-radius:6px;padding:16px 18px}
.alumni ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px 22px}
.alumni li{font-family:var(--f-head);font-weight:800;font-size:clamp(17px,2.4vw,22px);letter-spacing:-.01em;color:var(--fg)}
.diff{display:grid;gap:10px;max-width:760px}
.team{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(min(100%,240px),1fr))}
.member{border:1px solid var(--line);border-radius:6px;padding:14px 16px;background:var(--card);display:grid;gap:4px;align-content:start}
#steve-lee{grid-column:1/-1}
#steve-lee p{max-width:680px}
.m-n{font-family:var(--f-head);font-weight:800;font-size:18px}
.m-t{font-size:13px;color:var(--blue-ink);font-weight:600}
.member p{font-size:14.5px;color:var(--muted);margin-top:4px}
.scholars{display:grid;gap:8px;font-size:15px;max-width:760px}
.refs{display:grid;gap:8px;font-size:15px;max-width:760px;overflow-wrap:anywhere}
.fine{font-size:13px;color:var(--muted)}
details.embed summary{font-size:13px;color:var(--muted);font-weight:500}
details.embed textarea{width:100%;font:12px/1.4 ui-monospace,monospace;margin-top:6px;border:1px solid var(--line);border-radius:4px;padding:8px;background:var(--card);color:var(--fg);resize:vertical}
.quotes{border:1px solid var(--line);background:var(--card);border-radius:6px;padding:16px 18px;display:grid;gap:8px;max-width:760px}
.quotes .src{display:block;font-size:13px;color:var(--muted);margin-top:2px}
p,li,figcaption,dd,.aeo-t{text-wrap:pretty}
td,th{text-wrap:balance}
.quotes ul{margin:0;padding-left:18px;display:grid;gap:8px;font-size:15px}
table.play td{font-size:14px}
"""
def fonts(base):
    return (f'<link rel="preload" href="{base}hanken-grotesk.woff2" as="font" type="font/woff2" crossorigin>'
            f'<link rel="preload" href="{base}cormorant.woff2" as="font" type="font/woff2" crossorigin>'
            "<style>"
            f"@font-face{{font-family:'Hanken Grotesk';src:url({base}hanken-grotesk.woff2) format('woff2');font-weight:400 700;font-style:normal;font-display:swap}}"
            f"@font-face{{font-family:'Bricolage Grotesque';src:url({base}bricolage-grotesque.woff2) format('woff2');font-weight:600 800;font-style:normal;font-display:swap}}"
            f"@font-face{{font-family:'Cormorant';src:url({base}cormorant.woff2) format('woff2');font-weight:500 600;font-style:normal;font-display:swap}}"
            f"@font-face{{font-family:'Cormorant';src:url({base}cormorant-italic.woff2) format('woff2');font-weight:500 600;font-style:italic;font-display:swap}}"
            "</style>")
def page(title_tag, head_extra, fontbase="/assets/fonts/"):
    return f'''{title_tag}
<meta name="claude:viewport-fit-sides" content="cover">
{head_extra}
{fonts(fontbase)}
<style>{CSS}</style>
<script type="application/ld+json">{LD}</script>
<main class="wrap"><article>
{BODY}
</article>
<footer><div>Local AI Registry · 9891 Irvine Center Dr, Irvine, CA 92618 · <a href="https://localairegistry.com">localairegistry.com</a></div>
<div>Charts and text © 2026 Local AI Registry, licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Underlying data: Xu, Iqbal and Montgomery, IMC 2026 (CC BY 4.0), adapted.</div></footer>
</main>'''
DESC = "Local AI Registry’s AEO study of 7,583 Google AI answers: news supplied 67.5% of local citations, business sites 6.5%. Charts, data and an AEO playbook."
SEO_HEAD = f'''<meta name="description" content="{e(DESC)}">
<link rel="canonical" href="{BASE}">
<link rel="alternate" type="text/markdown" href="{BASE}index.md" title="Markdown version">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="Local AI Registry Research Team">
<meta property="og:type" content="article"><meta property="og:locale" content="en_US">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#F4F1EA"><meta property="og:site_name" content="Local AI Registry Research">
<meta property="og:title" content="The Local Answer Gap: AEO research on 7,583 Google AI answers">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:url" content="{BASE}">
<meta property="og:image" content="{BASE}images/who-google-ai-cites-for-local-business-questions-heatmap.png">
<meta property="og:image:width" content="2000"><meta property="og:image:height" content="1310"><meta property="og:image:type" content="image/png">
<meta property="og:image:alt" content="Heatmap of who Google’s AI cites for local business questions">
<meta property="article:published_time" content="{DATE}"><meta property="article:author" content="Local AI Registry Research Team">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@LocalAIRegistry"><meta name="twitter:title" content="The Local Answer Gap: AEO research on 7,583 Google AI answers">
<meta name="twitter:description" content="{e(DESC)}"><meta name="twitter:image" content="{BASE}images/who-google-ai-cites-for-local-business-questions-heatmap.png">'''
deploy = "<!doctype html>\n<html lang=\"en-US\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n" + page("<title>The Local Answer Gap: Local AEO Research | Local AI Registry</title>", SEO_HEAD).replace("<main", "</head><body><main", 1) + "</body></html>"
preview = page("<title>The Local Answer Gap</title>", f'<meta name="description" content="{e(DESC)}">', fontbase="assets/fonts/")
_glue = lambda h: re.sub(r' ([^\s<>]{1,14}(?:</(?:a|b|i|span)>)?</(?:p|li|dd|td|th|figcaption|div)>)', r'&nbsp;\1', h)
deploy = _glue(deploy); preview = _glue(preview)
for s_ in (deploy, preview):
    assert "—" not in s_ and "–" not in s_
open(os.path.join(PG, "index.html"), "w").write(deploy)
open(os.path.join(PG, "preview.html"), "w").write(preview)
print("deploy", len(deploy), "preview", len(preview), "figs", len(FIGS), "jsonld nodes", len(graph))
