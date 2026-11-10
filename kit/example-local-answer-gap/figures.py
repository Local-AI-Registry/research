import json, math
from svgkit import *
F = json.load(open("findings.json")); X = json.load(open("extra.json"))
CATS = ["Business's own site","Gannett papers","TEGNA TV","Other news","Portals (AOL, Yahoo, MSN)","Social","Everything else"]
CN = {"Business's own site":"Business’s own site","Gannett papers":"Gannett newspapers","TEGNA TV":"TEGNA TV stations","Other news":"Other news","Portals (AOL, Yahoo, MSN)":"AOL, Yahoo, MSN","Social":"Social media","Everything else":"Everything else"}
BN = {"walmart":"Walmart","target":"Target","costco":"Costco","publix":"Publix","trader joe":"Trader Joe’s","starbucks":"Starbucks","dunkin":"Dunkin’","aldi":"Aldi","lowe":"Lowe’s","sam":"Sam’s Club","post office":"Post office","chipotle":"Chipotle","kroger":"Kroger","home depot":"Home Depot","kohl":"Kohl’s","stop and shop":"Stop & Shop","mcdonald":"McDonald’s","food lion":"Food Lion","heb":"H-E-B","wegmans":"Wegmans","cvs":"CVS","no brand named":"No brand named"}
CATN = {"science":"Science","hobbies_leisure":"Hobbies","health":"Health","business_finance":"Business & finance","food_drink":"Food & drink","technology":"Technology","jobs_education":"Jobs & education","entertainment":"Entertainment","shopping":"Shopping","autos_vehicles":"Autos","other":"Other","pets_animals":"Pets","games":"Games","sports":"Sports","law_gov":"Law & government","travel_transport":"Travel","politics":"Politics","climate":"Climate","beauty_fashion":"Beauty & fashion","local":"Local business (our filter)"}
FIGS = []
def fig(slug, title, alt, caption, svg, table, section, kind="chart"):
    FIGS.append(dict(slug=slug, title=title, alt=alt, caption=caption, svg=svg, table=table, section=section, kind=kind))

# 1 census
rows=[("IMC 2026 Google AI Overviews",32608,237),("Organikpi, 13 public datasets",7045,2),("Cited.io, Oct 2026",23,0)]
b,h=heat([r[0] for r in rows]+["All four sources"],["Unique queries","About a physical business","Ask to find a local provider"],
  [[32608,237,0],[7045,2,2],[23,0,0],[39676,239,2]],lambda v:f"{v:,}",1,lw=330,cw=200,colfn=lambda v:(BLUE,0.12 if v>1000 else (0.9 if v<=2 else 0.4)))
fig("public-ai-search-datasets-local-query-census","Only 2 of 39,676 public AI-search research queries ask AI to find a local provider",
 "Table of four public AI search datasets: 39,676 unique queries, 239 about physical businesses, 2 asking for a local provider",
 "Across four public AI-search datasets, 239 of 39,676 unique queries (0.6%) concern a physical business, and only 2 ask an AI to find a local service provider.",
 frame(1000,h,"Only 2 of 39,676 public AI-search research queries ask AI to find a local provider","Census of public AI search datasets",b,"Blind spot",source="Data: IMC 2026, Organikpi and Cited.io public datasets (CC BY 4.0), hand-checked by Local AI Registry"),
 [["Dataset","Unique queries","About a physical business","Ask for a local provider"]]+[[r[0],f"{r[1]:,}",r[2],2 if r[1]==7045 else 0] for r in rows]+[["Total","39,676","239","2"]],"census")

# 2 activation by category
ac=X["act_cat"]
b,h=hbars([(CATN.get(c,c),p,True if c=="local" else False,f"{a:,}/{n:,}") for c,a,n,p in ac],100,W=1000,lw=280,rh=40,note_w=190)
fig("google-ai-overview-activation-by-search-category","Local business searches trigger Google AI Overviews more than any other topic",
 "Bar chart of AI Overview activation by category: local business 76.4%, science 39.9%, all others lower",
 "76.4% of local-business searches showed a Google AI Overview, nearly double the next category (science, 39.9%) and over five times the 13.7% average.",
 frame(1000,h,"Local business searches trigger Google AI Overviews more than any other topic","Activation rate by category",b,"Finding 1"),
 [["Category","AI Overview shown","Searches","Rate"]]+[[CATN.get(c,c),a,n,f"{p}%"] for c,a,n,p in ac],"f1")

# 3 activation 3 bars
r3=[("Local business searches",F["act_local"],True),("Other question-style searches",F["act_qf"],"muted"),("All searches",F["act_all"],"muted")]
b,h=hbars([(l,v[0]/v[1]*100,hl,f"{v[0]:,}/{v[1]:,}") for l,v,hl in r3],100,lw=310,note_w=210)
fig("local-search-ai-overview-rate-vs-question-searches","Local searches got an AI answer 76% of the time, even more often than other questions",
 "Bar chart: local searches 76.4%, other question searches 64.1%, all searches 13.7% showed an AI Overview",
 "Controlling for phrasing, local searches were still 12 points more likely to get an AI Overview than other question-style searches (76.4% vs 64.1%).",
 frame(1000,h,"Local searches got an AI answer 76% of the time, even more often than other questions","Activation local vs question vs all",b,"Finding 1"),
 [["Group","AI Overview shown","Searches","Rate"]]+[[l,v[0],v[1],f"{v[0]/v[1]*100:.1f}%"] for l,v,_ in r3],"f1")

# 4 source heatmap
M=[[F["mix_local"][c],F["mix_control"][c],F["answers_citing"][c],F["answers_citing_c"][c]] for c in CATS]
b,h=heat([CN[c] for c in CATS],["Local: share of citations","Other: share of citations","Local: answers citing","Other: answers citing"],M,lambda v:f"{v:.1f}%",95,lw=250,cw=170)
fig("who-google-ai-cites-for-local-business-questions-heatmap","Who Google’s AI cites for local business questions vs everything else",
 "Heatmap of cited source types: Gannett newspapers 28.3% of local citations and cited in 90.3% of local answers; business’s own site 6.5%",
 "In local answers, Gannett newspapers supplied 28.3% of citations and appeared in 90.3% of answers. Businesses’ own websites supplied 6.5% of citations.",
 frame(1000,h,"Who Google’s AI cites for local business questions vs everything else","Source mix heatmap",b,"Finding 2"),
 [["Source type","Local share of citations","Other share","Local answers citing","Other answers citing"]]+[[CN[c]]+[f"{v}%" for v in M[i]] for i,c in enumerate(CATS)],"f2")

# 5 lift
L=X["lift"]; lr=sorted([(CN[c],L[c][2]) for c in CATS if L[c][2]],key=lambda x:-x[1])
b,h=hbars([(n,v,True if v>=3 else (False if v>=1 else "muted"),"") for n,v in lr],20,fmt=lambda v:f"{v:.1f}×",lw=260)
fig("local-news-overrepresented-in-ai-local-answers","TEGNA TV stations are 18 times more likely to be cited in local answers than in other answers",
 "Bar chart of how over-represented each source type is in local answers: TEGNA 18x, portals 4.1x, Gannett 3.9x, other news 1.8x, own site 1.3x, social 0.7x",
 "Relative to other topics, local answers lean on TEGNA TV stations 18 times more, AOL/Yahoo/MSN 4.1 times and Gannett 3.9 times. Social media is used less (0.7 times).",
 frame(1000,h,"TEGNA TV stations are 18 times more likely to be cited in local answers than in other answers","Lift by source",b,"Finding 2"),
 [["Source type","Local share","Other share","Lift"]]+[[CN[c],f"{L[c][0]}%",f"{L[c][1]}%",f"{L[c][2]}×"] for c in CATS],"f2")

# 6 top domains
GC={"Gannett papers":BLUE,"TEGNA TV":BLUE,"Business's own site":CORAL}
td=X["top_dom"][:18]; nL=F["n_local"]
rowsd=[(d,n/nL*100,True if g in("Gannett papers","TEGNA TV") else ("coral" if g=="Business's own site" else "muted"),CN[g]) for d,n,g in td]
b,h=hbars(rowsd,70,lw=250,rh=40,note_w=260)
fig("top-domains-cited-in-google-ai-local-answers","The 18 websites Google’s AI cited most for “is it open” questions",
 "Bar chart of the most cited domains in local AI Overview answers led by today.com, usatoday.com and facebook.com",
 f"today.com was cited in {td[0][1]/nL*100:.0f}% of local answers and usatoday.com in {td[1][1]/nL*100:.0f}%. Gannett and TEGNA domains are highlighted; no store’s own site made the top 18.",
 frame(1000,h,"The 18 websites Google’s AI cited most for “is it open” questions","Top domains",b,"Finding 2"),
 [["Domain","Answers citing","Share of local answers","Owner group"]]+[[d,n,f"{n/nL*100:.1f}%",CN[g]] for d,n,g in td],"f2")

# 7 2x2 source groups share vs lift
pts=[]; pos={"Gannett papers":"l","TEGNA TV":"r","Other news":"l","Portals (AOL, Yahoo, MSN)":"r","Business's own site":"r","Social":"b","Everything else":"a"}
for c in CATS:
    pts.append(dict(label=CN[c],x=F["mix_local"][c],y=L[c][2],r=8+math.sqrt(F["mix_local"][c])*3,color=CORAL if c=="Business's own site" else BLUE,pos=pos[c]))
b,h=scatter(pts,(0,36),(0.05,40),"Share of local citations","Over-representation vs other topics",{"tl":"Local specialists","tr":"Local gatekeepers","bl":"Not used for local","br":"Big but generic"},ylog=True,xticks=[0,10,20,30],yticks=[0.1,0.3,1,3,10,30],xfmt=lambda v:f"{v}%",yfmt=lambda v:f"{v}×",xdiv=15,ydiv=1)
fig("ai-local-answer-source-2x2-share-vs-lift","Local gatekeepers: which sources dominate Google AI’s local answers",
 "Two by two chart of source types by share of local citations and over-representation; Gannett and other news are local gatekeepers, TEGNA a local specialist",
 "Gannett newspapers and other news outlets are local gatekeepers: large shares of local citations and over-represented versus other topics. Business sites sit near the bottom left.",
 frame(1000,h,"Local gatekeepers: which sources dominate Google AI’s local answers","2x2 share vs lift",b,"Finding 2"),
 [["Source type","Share of local citations","Lift"]]+[[CN[c],f"{F['mix_local'][c]}%",f"{L[c][2]}×"] for c in CATS],"f2")

# 8 query type heatmap
QT=X["qtype"]; qo=["Brand yes/no (is X open)","Brand hours","Generic (what's open)","Banks and post offices"]
QN={"Brand yes/no (is X open)":"“Is Target open?”","Brand hours":"“Target Easter hours”","Generic (what's open)":"“What’s open today?”","Banks and post offices":"Banks, post offices"}
M=[[QT[q][c] for c in CATS] for q in qo]
SH=["Own site","Gannett","TEGNA","Other news","Portals","Social","Other"]
b,h=heat([f"{QN[q]} ({QT[q]['n']})" for q in qo],SH,M,lambda v:f"{v:.0f}%",55,lw=290,cw=110,ch=56,colhdr_lines=1)
fig("ai-citation-sources-by-local-question-type-heatmap","The vaguer the local question, the less the business gets cited",
 "Heatmap of source types by local question type; business’s own site 10.9% for brand hours questions and 1.0% for generic what’s open questions",
 "Businesses’ own sites made up 8.8 to 10.9% of citations when a brand was named, but only 1.0% for generic “what’s open” questions, which is how people discover new places.",
 frame(1100,h,"The vaguer the local question, the less the business gets cited","Query type x source",b,"Finding 2"),
 [["Question type","Answers"]+[CN[c] for c in CATS]]+[[QN[q],QT[q]["n"]]+[f"{QT[q][c]}%" for c in CATS] for q in qo],"f2")

# 9 brand heatmap
BH=F["brand_heat"]; cols=["Own site cited","Own site share","Gannett","TEGNA","Other news","Portals","Social"]
M=[[b_["own_answers"]]+[b_[c] for c in CATS[:6]] for b_ in BH]
b,h=heat([f"{BN.get(b_['brand'],b_['brand'])} ({b_['n']})" for b_ in BH],cols,M,lambda v:f"{v:.0f}%",100,lw=230,cw=112,ch=46,colhdr_lines=2)
fig("brand-by-source-heatmap-google-ai-overviews-easter-hours","Brand by brand: where Google’s AI got each chain’s hours",
 "Heatmap of brands by citation source; Walmart own site cited in 7% of its answers, Publix, Trader Joe’s and Sam’s Club 100%",
 "Walmart, the most-asked brand, had its own site cited in 7% of its answers. Starbucks and Chipotle were never cited for their own hours; Publix, Trader Joe’s and Sam’s Club were cited every time.",
 frame(1050,h,"Brand by brand: where Google’s AI got each chain’s hours","Brand heatmap",b,"Finding 3"),
 [["Brand (answers)"]+cols]+[[BN.get(b_['brand'],b_['brand']),*[("n/a" if v is None else f"{v:.0f}%") for v in M[i]]] for i,b_ in enumerate(BH)],"f3")

# 10 dumbbell rank vs cited
RC=[r for r in X["brand_rank_cite"] if r[1]>=4]
b,h=dumbbell([(f"{BN.get(r[0],r[0])} ({r[1]})",r[2]/r[1]*100,r[3]/r[1]*100) for r in RC],100,"Own site on Google page one","Own site cited by the AI",lw=230)
fig("brand-website-ranked-vs-cited-google-ai-overviews","Ranked on page one, skipped by the AI: brand websites in local answers",
 "Dumbbell chart per brand comparing how often its website ranked on page one versus was cited by the AI Overview",
 f"Brand websites appeared on page one in {F['own_on_serp']} of 157 brand questions but were cited in {F['own_cited']}. Walmart ranked in 11 of 15 answers and was cited once.",
 frame(1000,h,"Ranked on page one, skipped by the AI: brand websites in local answers","Rank vs cite",b,"Finding 3"),
 [["Brand","Answers","Own site on page one","Own site cited"]]+[[BN.get(r[0],r[0]),r[1],r[2],r[3]] for r in RC],"f3")

# 11 2x2 brands
groups={}
for r in RC:
    key=(round(r[2]/r[1]*100),round(r[3]/r[1]*100)); groups.setdefault(key,[]).append(r)
lp={(100,100):"l",(100,0):"l",(100,83):"l",(100,78):"b",(73,7):"r",(67,17):"r",(100,50):"l",(100,25):"l"}
pts=[]
for (x,y),rs in groups.items():
    n=sum(r[1] for r in rs); names=", ".join(BN.get(r[0],r[0]) for r in rs)
    pts.append(dict(label=names,x=x,y=y,r=6+n*0.6,pos=lp.get((x,y),"l"),color=CORAL if y<30 else BLUE))
b,h=scatter(pts,(60,104),(-14,118),"Own site ranks on page one","Own site cited by the AI",{"tl":"Rare: cited without ranking","tr":"Ranked and used","bl":"Invisible","br":"Ranked, ignored"},xticks=[60,70,80,90,100],yticks=[0,25,50,75,100],xfmt=lambda v:f"{v}%",yfmt=lambda v:f"{v}%",xdiv=82,ydiv=50)
fig("brand-rank-vs-ai-citation-2x2","Ranked and used vs ranked and ignored: a 2x2 of brand websites",
 "Two by two of brands by page-one ranking rate and AI citation rate; Walmart, Starbucks and Chipotle are ranked but ignored",
 "Most brands ranked on page one nearly every time. What split them was use: Publix, Trader Joe’s and Sam’s Club were cited every time; Walmart, Starbucks and Chipotle were ranked but ignored.",
 frame(1000,h,"Ranked and used vs ranked and ignored: a 2x2 of brand websites","Brand 2x2",b,"Finding 3"),
 [["Brand","Page-one rate","Cited rate"]]+[[BN.get(r[0],r[0]),f"{r[2]/r[1]*100:.0f}%",f"{r[3]/r[1]*100:.0f}%"] for r in RC],"f3")

# 12 outside page one
O=X["outside"]; orows=sorted([(CN[c],O[c]) for c in CATS],key=lambda x:-x[1])
b,h=hbars([(n,v,"coral" if n=="Business’s own site" else False,"") for n,v in orows],60,lw=260)
fig("ai-citations-from-outside-google-page-one-by-source","The AI goes past page one for news, not for business websites",
 "Bar chart of the share of each source type’s citations that came from outside Google’s first page; business sites 4.1%, portals 48.8%",
 "Only 4.1% of business-site citations came from outside Google’s first page, versus 48.8% for AOL/Yahoo/MSN and 39.8% for TEGNA stations. A business site has to rank to be used.",
 frame(1000,h,"The AI goes past page one for news, not for business websites","Outside page one",b,"Finding 3"),
 [["Source type","Citations from outside page one"]]+[[n,f"{v}%"] for n,v in orows],"f3")

# 13 waffle hedge
k=round(F["hedge_local"]/100*F["n_local"])
b,h=waffle(F["n_local"],k,cols=23,size=34,gap=6,lab_on=f"Told people to check locally ({k})",lab_off=f"Did not ({F['n_local']-k})")
fig("ai-answers-telling-people-to-check-local-store-waffle","173 of 207 local AI answers told people to check with their local store",
 "Waffle chart of 207 squares, 173 highlighted for answers that hedged with check locally or call ahead",
 "83.6% of local AI answers sent the reader back to the store (“check your local store,” “call ahead,” “hours may vary”), against 2.6% of other answers.",
 frame(1000,h,"173 of 207 local AI answers told people to check with their local store","Hedge waffle",b,"Finding 4"),
 [["Group","Hedged"],["Local answers",f"{F['hedge_local']}%"],["Other answers",f"{F['hedge_control']}%"]],"f4")

# 14 waffle address
b,h=waffle(F["n_local"],F["address_n"],cols=23,size=34,gap=6,on=CORAL,lab_on="Gave a street address or phone (1)",lab_off=f"Did not ({F['n_local']-1})")
fig("ai-local-answers-with-address-or-phone-waffle","1 of 207 local AI answers named a street address or phone number",
 "Waffle chart of 207 squares with a single highlighted square for the one answer that gave an address or phone number",
 "Only 1 of 207 local AI answers gave a street address or phone number. The AI answered about chains, not places.",
 frame(1000,h,"1 of 207 local AI answers named a street address or phone number","Address waffle",b,"Finding 4"),
 [["Answers","With address or phone"],["207","1"]],"f4")

# 15 local vs other behavior bars (grouped)
b,h=vbars([[F["hedge_local"],F["national"],F["address_n"]/F["n_local"]*100],[F["hedge_control"],X["national_control"],X["address_control"]]],["Tells you to check locally","Answers at chain level","Gives address or phone"],100,W=1000,H=420,names=("Local answers","Other answers"),colors=(BLUE,MUTED))
fig("how-ai-answers-local-questions-national-framing","AI answers local questions with national facts",
 "Grouped bar chart: 83.6% of local answers hedge, 65.7% frame the answer at chain level, 0.5% give an address",
 "65.7% of local answers spoke about “all locations” or “most stores” (vs 2.3% of other answers), and 83.6% hedged (vs 2.6%). National facts are the AI’s default for local questions.",
 frame(1000,h,"AI answers local questions with national facts","Framing bars",b,"Finding 4",),
 [["Measure","Local answers","Other answers"],["Tells you to check locally",f"{F['hedge_local']}%",f"{F['hedge_control']}%"],["Answers at chain level",f"{F['national']}%",f"{X['national_control']}%"],["Gives address or phone","0.5%",f"{X['address_control']}%"]],"f4")

# 16 first-party bars
fp=F["fp"]
r16=[("Local claims quoting a store locator, app or official site",fp["fp_local"][1]/fp["fp_local"][0]*100,"coral",f"{fp['fp_local'][1]}/{fp['fp_local'][0]}"),
     ("All other local claims",fp["nonfp_local"][1]/fp["nonfp_local"][0]*100,False,f"{fp['nonfp_local'][1]}/{fp['nonfp_local'][0]:,}"),
     ("Non-local claims quoting an official source",fp["fp_control"][1]/fp["fp_control"][0]*100,"muted",f"{fp['fp_control'][1]}/{fp['fp_control'][0]}")]
b,h=hbars(r16,60,lw=360,rh=56,note_w=170)
fig("ai-store-locator-claims-unsupported-rate","When Google’s AI says “the store locator says,” half the time it can’t show it",
 "Bar chart: 51.6% of local claims quoting a store locator or app were unsupported, vs 6.7% of other local claims",
 "16 of 31 local claims that cited a store locator, app or official site (51.6%) were not supported by any page the AI cited, against 6.7% of other local claims.",
 frame(1000,h,"When Google’s AI says “the store locator says,” half the time it can’t show it","First-party claims",b,"Finding 5"),
 [["Claim type","Unsupported","Total","Rate"]]+[[r[0],r[3].split("/")[0],r[3].split("/")[1],f"{r[1]:.1f}%"] for r in r16],"f5")

# 17 verdict heatmap
labs=["CLEAR","VAGUE","AMBIGUOUS","INCORRECT","OMITTED"]; ln=["Supported","Vague","Ambiguous","Incorrect","Not in sources"]
M=[[F["labels_local"][l] for l in labs],[F["labels_control"][l] for l in labs]]
b,h=heat(["Local answers","Everything else"],ln,M,lambda v:f"{v:.1f}%",10,lw=220,cw=148,colfn=lambda v:(BLUE,0.85) if v>50 else (CORAL,max(.1,min(1,v/9))))
fig("ai-overview-claim-accuracy-local-vs-other-heatmap","Local AI answers were more faithful to their sources than average",
 "Heatmap of claim verdicts: 87.8% of local claims supported vs 84.5% of other claims",
 "87.8% of 2,253 local claims were supported by the cited pages, versus 84.5% of 95,767 other claims. Faithful to sources is not the same as accurate for your location.",
 frame(1000,h,"Local AI answers were more faithful to their sources than average","Verdict heatmap",b,"Finding 6",source="Data: IMC 2026 claim verdicts (CC BY 4.0), regrouped by Local AI Registry"),
 [["Group"]+ln]+[[g]+[f"{v}%" for v in M[i]] for i,g in enumerate(["Local answers","Everything else"])],"f6")

# 18 readable 2x2
P=F["pages"]; A=F["answers_citing"]
pp={"Gannett papers":"l","Other news":"l","TEGNA TV":"b","Portals (AOL, Yahoo, MSN)":"r","Everything else":"l","Business's own site":"b","Social":"r"}
pts=[dict(label=CN[c],x=A[c],y=100-P[c]["thin_or_error"],r=6+math.sqrt(P[c]["n"])*0.8,color=CORAL if c in("Business's own site","Social") else BLUE,pos=pp[c]) for c in CATS]
b,h=scatter(pts,(20,100),(-8,122),"Share of local answers citing it","Cited pages with readable text",{"tr":"The record","tl":"Readable, rarely used","bl":"Thin and rarely used","br":"Cited, nothing to read"},xticks=[20,40,60,80,100],yticks=[0,25,50,75,100],xfmt=lambda v:f"{v}%",yfmt=lambda v:f"{v}%",xdiv=60,ydiv=50)
fig("cited-vs-readable-ai-sources-2x2","Cited vs readable: what Google’s AI could actually read",
 "Two by two of source types by how often they were cited and how often their pages had readable text; social is cited but 78% unreadable",
 "News pages were both cited and readable. Social posts were cited in 48% of local answers but 78% were thin (median 8 words). 11% of businesses’ own pages were thin.",
 frame(1000,h,"Cited vs readable: what Google’s AI could actually read","Readability 2x2",b,"Finding 5",source="Data: 1,496 cited pages saved by the IMC 2026 study (CC BY 4.0). Thin = under 150 words or load error."),
 [["Source type","Answers citing","Pages","Median words","Thin or error"]]+[[CN[c],f"{A[c]}%",P[c]["n"],P[c]["median_words"],f"{P[c]['thin_or_error']}%"] for c in CATS],"f5")

# 19 median words
wr=sorted([(CN[c],P[c]["median_words"]) for c in CATS],key=lambda x:-x[1])
b,h=hbars([(n,v,"coral" if n in("Social media","Business’s own site") else False,"") for n,v in wr],700,fmt=lambda v:f"{v:,.0f} words",lw=260,note_w=180)
fig("readable-words-on-ai-cited-pages-by-source","Social posts the AI cited had a median of 8 readable words",
 "Bar chart of median readable words on cited pages: portals 639, news about 500, business sites 350, social media 8",
 "The median cited social post had 8 readable words. Store locator pages were also thin: Trader Joe’s store search had 97 words and Cracker Barrel’s Easter page 18.",
 frame(1000,h,"Social posts the AI cited had a median of 8 readable words","Median words",b,"Finding 5"),
 [["Source type","Median readable words"]]+[[n,v] for n,v in wr],"f5")

# 20 jaccard
r20=[("Same local query, another day",F["jac_repeat_local"][0]*100,False,f"{F['jac_repeat_local'][1]} pairs"),("Same brand, same day, different wording",F["jac_phrasing"][0]*100,True,f"{F['jac_phrasing'][1]} pairs"),("Other topics, same query repeated",F["jac_repeat_control"][0]*100,"muted",f"{F['jac_repeat_control'][1]:,} pairs")]
b,h=hbars(r20,100,lw=360,rh=52,fmt=lambda v:f"{v:.0f}% shared",note_w=230)
fig("ai-answer-source-overlap-by-wording","Ask the same thing in different words and two-thirds of the sources change",
 "Bar chart of source overlap: 35% shared for the same brand asked in different words on the same day",
 "“Is Target open on Easter” and “Target Easter hours,” asked the same day, shared about 35% of cited sources on average. The verdict stayed the same; the sources rotated.",
 frame(1000,h,"Ask the same thing in different words and two-thirds of the sources change","Jaccard",b,"Finding 6"),
 [["Comparison","Average shared sources","Pairs"]]+[[r[0],f"{r[1]:.0f}%",r[3]] for r in r20],"f6")

# 21 refs histogram
RH=X["refs_hist"]; ks=[str(i) for i in range(2,16)]
b,h=vbars([[RH["local"][k] for k in ks],[RH["control"][k] for k in ks]],[k if k!="15" else "15+" for k in ks],20,names=("Local answers","Other answers"),H=400)
fig("sources-per-ai-overview-answer-distribution","Local AI answers cite fewer sources: 7.2 per answer vs 8.1",
 "Histogram of sources cited per answer for local and other AI Overviews",
 f"Local AI Overviews cited {F['refs_local']} sources on average versus {F['refs_control']} for other topics, clustered at 5 to 8 sources.",
 frame(1000,h,"Local AI answers cite fewer sources: 7.2 per answer vs 8.1","Sources per answer",b,"Finding 6"),
 [["Sources per answer","Local answers","Other answers"]]+[[k,f"{RH['local'][k]}%",f"{RH['control'][k]}%"] for k in ks],"f6")

# 22 timeline
DE=X["days_exec"]; labs22=[d[5:] for d,_ in DE]
b,h=vbars([[n for _,n in DE]],labs22,200,H=400,fmt=lambda v:f"{v:.0f}",every=1)
fig("local-business-searches-by-day-easter-2026","Local “is it open” searches spiked the day after Easter",
 "Bar chart of local business searches by collection day in March and April 2026, peaking at 185 on April 6",
 "185 of 271 local searches in the dataset were collected on April 6, 2026, the day after Easter, which is why most local answers in this study are about holiday hours.",
 frame(1000,h,"Local “is it open” searches spiked the day after Easter","Timeline",b,"Method",source="Data: IMC 2026 trending-query collection days (CC BY 4.0)"),
 [["Day","Local searches"]]+[[d,n] for d,n in DE],"method")

# 23 control x share playbook 2x2
ctrl={"Business's own site":4,"Social":3,"Everything else":2.4,"Portals (AOL, Yahoo, MSN)":1.3,"Gannett papers":1.6,"TEGNA TV":1.9,"Other news":1.15}
pc={"Business's own site":"l","Social":"r","Everything else":"b","Portals (AOL, Yahoo, MSN)":"b","Gannett papers":"r","TEGNA TV":"a","Other news":"r"}
pts=[dict(label=CN[c],x=ctrl[c],y=F["mix_local"][c],r=8+math.sqrt(F["mix_local"][c])*3,color=CORAL if c=="Business's own site" else BLUE,pos=pc[c]) for c in CATS]
b,h=scatter(pts,(0.6,4.6),(0,40),"How much a business controls it","Share of local AI citations",{"tl":"Earn it: press and coverage","tr":"Own it and grow it","bl":"Low priority","br":"Control it, fix readability"},xticks=[1,2,3,4],yticks=[0,10,20,30,40],xfmt=lambda v:{1:"None",2:"Influence",3:"Partial",4:"Full"}[v],yfmt=lambda v:f"{v}%",xdiv=2.5,ydiv=15)
fig("local-aeo-priority-2x2-control-vs-citation-share","Local AEO priority map: what AI cites vs what you control",
 "Two by two of source types by business control and share of local AI citations; news is high citation low control, own site is full control low citation",
 "The sources AI cites most for local answers (news) are the ones businesses control least, and the source they fully control (their site) is cited least. AEO closes that gap from both sides.",
 frame(1000,h,"Local AEO priority map: what AI cites vs what you control","Priority 2x2",b,"Playbook",source="Data: Local AI Registry analysis of IMC 2026 (CC BY 4.0). Control levels are Local AI Registry’s judgment."),
 [["Source type","Business control (our judgment)","Share of local citations"]]+[[CN[c],["","None","Influence","Partial","Full"][round(ctrl[c])],f"{F['mix_local'][c]}%"] for c in CATS],"playbook")
