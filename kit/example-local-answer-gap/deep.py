import json, re, collections, itertools, statistics as st
from analyze import L, C, recs
BR = {"walmart":"walmart","target":"target","costco":"costco","publix":"publix","kroger":"kroger","aldi":"aldi","trader joe":"traderjoes",
 "starbucks":"starbucks","cvs":"cvs","walgreens":"walgreens","home depot":"homedepot","lowe":"lowes","wegmans":"wegmans","heb":"heb",
 "meijer":"meijer","dunkin":"dunkin","mcdonald":"mcdonalds","chipotle":"chipotle","sam":"samsclub","food lion":"foodlion",
 "harris teeter":"harristeeter","stop and shop":"stopandshop","whole foods":"wholefoods","post office":"usps","usps":"usps","kohl":"kohls",
 "macy":"macys","tj maxx":"tjmaxx","marshalls":"marshalls","ulta":"ulta","best buy":"bestbuy","petsmart":"petsmart","michaels":"michaels",
 "old navy":"oldnavy","panera":"panerabread","olive garden":"olivegarden","cracker barrel":"crackerbarrel","burger king":"bk.com",
 "chili":"chilis","dollar general":"dollargeneral","family dollar":"familydollar","goodwill":"goodwill","giant eagle":"gianteagle",
 "hannaford":"hannaford","homegoods":"homegoods","market basket":"marketbasket","shoprite":"shoprite","winn dixie":"winndixie",
 "burlington":"burlington","stop & shop":"stopandshop","7-eleven":"7eleven","bahama breeze":"bahamabreeze"}
def brand_of(k):
    k=k.lower()
    for t,s in BR.items():
        if re.search(r"\b"+re.escape(t), k):
            if t=="giant" : pass
            return t
    if re.search(r"\bgiant\b",k): return "giant"
    if "bank" in k: return "banks"
    return None
def norm(d): return re.sub(r"[^a-z0-9.]","",d)
BRAND_SLUGS=set(BR.values())|{"giantfood"}
def own_any(d):
    nd=norm(d).replace(".","")
    return any(s.replace(".","") in nd for s in BRAND_SLUGS if len(s)>3) or nd.startswith("heb") or nd.startswith("cvs") or "aldi" in nd
GANNETT=set("usatoday.com delawareonline.com northjersey.com indystar.com elpasotimes.com providencejournal.com democratandchronicle.com lohud.com tcpalm.com cincinnati.com app.com news-journalonline.com courier-journal.com pjstar.com freep.com azcentral.com tennessean.com jsonline.com desmoinesregister.com statesman.com palmbeachpost.com jacksonville.com dispatch.com oklahoman.com burlingtonfreepress.com greenvilleonline.com knoxnews.com commercialappeal.com naplesnews.com news-press.com floridatoday.com sctimes.com detroitnews.com lansingstatejournal.com press-citizen.com hometownlife.com thenewsstar.com theadvertiser.com shreveporttimes.com montgomeryadvertiser.com clarionledger.com ydr.com eveningsun.com lancastereagle.com mansfieldnewsjournal.com coloradoan.com rgj.com redding.com vcstar.com desertsun.com thespectrum.com stargazette.com pressconnects.com poughkeepsiejournal.com post-gazette.com? centralfloridafuture.com caller.com reporternews.com goupstate.com savannahnow.com augustachronicle.com onlineathens.com timesrecordnews.com lubbockonline.com amarillo.com gosanangelo.com wicked local.com patriotledger.com southcoasttoday.com capecodtimes.com telegram.com metrowestdailynews.com enterprisenews.com theledger.com gainesville.com heraldtribune.com theintell.com phillyburbs.com recordonline.com timesherald.com fosters.com seacoastonline.com jconline.com courierpress.com indianagazette.com marionstar.com newarkadvocate.com zanesvilletimesrecorder.com coshoctontribune.com chillicothegazette.com thenorthwestern.com postcrescent.com greenbaypressgazette.com htrnews.com fdlreporter.com wausaudailyherald.com stevenspointjournal.com marshfieldnewsherald.com wisconsinrapidstribune.com sheboyganpress.com packersnews.com beaconjournal.com citizen-times.com guampdn.com the-leader.com mycentraljersey.com dailyrecord.com courierpostonline.com thedailyjournal.com shoreline? starnewsonline.com fayobserver.com gastongazette.com hendersonvillenews.com".split())
TEGNA=set("wcnc.com kare11.com king5.com 13newsnow.com wtsp.com cbs8.com wfaa.com khou.com 11alive.com 9news.com wusa9.com ksdk.com wkyc.com wbir.com wzzm13.com firstcoastnews.com 12news.com kens5.com wgrz.com newscentermaine.com wnep.com whas11.com wtol.com wthr.com kgw.com krem.com kvue.com wwltv.com kiiitv.com ktvb.com wltx.com wcsh6.com abc10.com fox43.com wqad.com wfmynews2.com wvec.com wmaz.com 13wmaz.com localmemphis.com kare11.com wkyc.com fox61.com wnep.com cbs19.tv kcentv.com kagstv.com kbmt12.com 12newsnow.com newswest9.com kwes.com myfoxzone.com wtsp.com kytx.com cbs19.tv ksdk.com wpmt? kvue.com wusa9.com thv11.com wbir.com wjhl? 5newsonline.com kthv.com".split())
SOCIAL={"facebook.com","instagram.com","reddit.com","youtube.com","tiktok.com","x.com","twitter.com","threads.net","quora.com","m.facebook.com","pinterest.com"}
PORTAL={"aol.com","yahoo.com","msn.com","shopping.yahoo.com","news.yahoo.com","finance.yahoo.com","ground.news","newsbreak.com","flipboard.com"}
NEWSPAT=re.compile(r"news|times|post|journal|herald|tribune|gazette|daily|star|register|courier|dispatch|today|cbs|nbc|abc|fox|wral|^k[a-z]{2,3}\d*\.(com|tv)$|^w[a-z]{2,3}\d*\.(com|tv)$|\d+news|mlive|nj\.com|al\.com|silive|pennlive|cleveland|oregonlive|masslive|syracuse|newsweek|thestreet|mensjournal|fastcompany|the-sun|ibtimes|rd\.com|people\.com|parade|bestlife|eatthis|delish|allrecipes|southernliving|thekitchn|foodandwine|nypost|cnn|nbcnews|cbsnews|axios|forbes|businessinsider|huffpost|kiplinger|aarp|thrillist|eater|tasteofhome|newsday|fortune|time\.com|usatoday|mysanantonio|chron|sfgate|kare|wcnc|wkyc|wtsp|king5|wsb|wgal|wpxi|wesh|wlwt|wisn|kcra|kmbc|wbaltv|wmur|wtae|koat|kcci|wyff|wxii|wapt|wvtm|wlky|wdsu|ketv|wpbf|kitv|kout",re.I)
def cat(d,brand=None):
    if d in SOCIAL: return "Social"
    if d in PORTAL: return "Portals (AOL, Yahoo, MSN)"
    if own_any(d) or d.endswith(".gov") or d=="usps.com" or d.endswith("usps.com"): return "Business's own site"
    if d in GANNETT or d.endswith("usatoday.com"): return "Gannett papers"
    if d in TEGNA: return "TEGNA TV"
    if NEWSPAT.search(d): return "Other news"
    return "Everything else"
CATS=["Business's own site","Gannett papers","TEGNA TV","Other news","Portals (AOL, Yahoo, MSN)","Social","Everything else"]
def mix(rs):
    c=collections.Counter(); n=0
    for r in rs:
        for d in r["ref_dom"]: c[cat(d)]+=1; n+=1
    return {k: round(c[k]/n*100,1) for k in CATS}, n
if __name__=="__main__":
    ml,nl=mix(L); mc,nc=mix(C); print("LOCAL mix",nl,ml); print("CONTROL mix",nc,mc)
    oth=collections.Counter(d for r in L for d in r["ref_dom"] if cat(d)=="Everything else"); print("other local:",oth.most_common(40))
    on=collections.Counter(d for r in L for d in r["ref_dom"] if cat(d)=="Other news"); print("othernews local:",on.most_common(30))
    # answers citing at least one
    for k in CATS: print(k, "answers citing:", round(sum(1 for r in L if any(cat(d)==k for d in r["ref_dom"]))/len(L)*100,1))
