import json,html,numpy as np
S=json.load(open('monthly.json'))
BLUE="#1F4FE0";ORANGE="#C2410C";INK="#0B1A2E";CORAL="#FF5A3C";PAPER="#F4F1EA";SLATE="#556070";TINT="#C9D4F6"
LOGO="file:///home/claude/work/canvas/logo.svg";F='/home/claude/research/assets/fonts/'
CSS=f"""@font-face{{font-family:Cormorant;src:url(file://{F}cormorant.woff2);font-weight:300 700}}@font-face{{font-family:'Bricolage Grotesque';src:url(file://{F}bricolage-grotesque.woff2);font-weight:200 800}}@font-face{{font-family:'Hanken Grotesk';src:url(file://{F}hanken-grotesk.woff2);font-weight:100 900}}body{{margin:0}}"""
esc=lambda s:html.escape(s,quote=True)
ADM=["2025-11","2025-12","2026-01","2026-02","2026-03","2026-04","2026-05","2026-06","2026-07","2026-08","2026-09","2026-10"]
ADS={"first date outfit":[4400,3600,4400,4400,4400,4400,4400,4400,4400,4400,4400,4400],
"first date outfit men":[1000,880,1000,1000,1000,1300,1000,1000,880,1000,880,880],
"red flags in a man":[8100,8100,8100,8100,8100,8100,6600,6600,8100,6600,6600,8100],
"red flags in a woman":[2400,2400,2400,1900,2400,1900,2400,1900,1900,1900,1900,2400],
"how to get him to commit":[260,260,320,260,320,320,260,260,320,320,320,390],
"how to get her to commit":[10,10,10,10,10,0,0,10,10,10,10,0]}
TR="Monthly average of weekly Google search interest, U.S., Dec 2021 to Oct 2026. Both phrases pulled together, on the same scale. Google does not say who searched."
AD="Google Ads monthly U.S. searches, Nov 2025 to Oct 2026. Rounded estimates."
P=[
 dict(src="ads",a="first date outfit",b="first date outfit men",la="First date outfit",lb="…men",h=["“First date outfit” gets","4× the searches of","“first date outfit men.”"],sub="She is planning her look. Plan yours.",stat=("4.4×","as many searches for the women's version"),
  cap="She already knows what she's wearing. “First date outfit” gets about 4,400 searches a month. “First date outfit men” gets about 1,000. Guys: a clean fit and a fresh haircut go a long way.\n\nWhat's your go-to first date fit?"),
 dict(src="ads",a="red flags in a man",b="red flags in a woman",la="Red flags in a man",lb="…in a woman",h=["“Red flags in a man”","gets 4× the searches."],sub="She is checking. Don't be one.",stat=("4.3×","as many searches as “red flags in a woman”"),
  cap="Before the date, she's doing her homework. “Red flags in a man” gets about 8,100 searches a month, more than 4 times “red flags in a woman” (about 1,900). Show up on time, put the phone away, be kind to the server.\n\nBiggest first date red flag? Go."),
 dict(src="ads",a="how to get him to commit",b="how to get her to commit",la="…him to commit",lb="…her to commit",h=["“How to get him to commit”","beats “her” 26 to 1."],sub="If you're serious, say so.",stat=("26×","as many searches as the “her” version"),
  cap="Mixed signals are exhausting. “How to get him to commit” gets about 260 searches a month. “How to get her to commit”? About 10. If you know what you want, saying it out loud is the move.\n\nTag someone who needs to hear this."),
 dict(src="tr",a="is he the one",b="is she the one",la="Is he the one",lb="Is she the one",h=["“Is he the one?”","outsearches “is she the one?”"],sub="Every single year.",
  cap="She's thinking long term. Over the past five years, “is he the one” has been searched about 1.4 times as often as “is she the one,” and it wins every year. Guys: consistency is what answers that question.\n\nWhen did you know?"),
 dict(src="tr",a="does he like me",b="does she like me",la="Does he like me",lb="Does she like me",h=["“Does he like me?”","beats “does she like me?”"],sub="By 1.5 to 1 over five years.",
  cap="Overthinking is universal, but she does more of it. “Does he like me” has run about 1.5 times “does she like me” over the past five years. So yes, she's wondering. Text back. Make the plan.\n\nDouble text: yes or no?"),
 dict(src="tr",a="does he love me",b="does she love me",la="Does he love me",lb="Does she love me",h=["“Does he love me?”","wins by 1.6 to 1."],sub="Say it back, guys.",
  cap="The biggest gap of the bunch. “Does he love me” has been searched about 1.6 times as often as “does she love me” over the past five years. If you feel it, say it. She's literally Googling it.\n\nWho said “I love you” first?"),
 dict(src="tr",a="how to tell if a girl likes you",b="how to tell if a guy likes you",la="…a girl likes you",lb="…a guy likes you",h=["Plot twist: guys are","more confused."],sub="“How to tell if a girl likes you” wins this one.",
  cap="Guys, you're not alone. “How to tell if a girl likes you” outsearches “how to tell if a guy likes you,” about 1.2 to 1 over five years and 1.4 to 1 this past year. Easiest way to find out? Ask her out.\n\nTag the friend who overthinks everything."),
 dict(src="tr",a="is he cheating",b="is she cheating",la="Is he cheating",lb="Is she cheating",h=["“Is he cheating?”","beats “is she cheating?”"],sub="The suspicion runs both ways.",
  cap="Trust issues are not just a her thing. “Is he cheating” runs about 1.4 times “is she cheating” over five years, so plenty of guys are asking too. Be the person nobody has to Google about."),
]
def lines_chart(xs,A,B,la,lb,ymax,yticks,yfmt,xlab):
    cw,ch=952,560;L,R,T,B_=70,190,26,52;n=len(xs)
    X=lambda i:L+i*(cw-L-R)/(n-1); Y=lambda v:T+(ymax-v)*(ch-T-B_)/ymax
    g=[f'<rect width="{cw}" height="{ch}" rx="16" fill="#fff"/>']
    for v in yticks:
        g.append(f'<line x1="{L}" x2="{cw-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{"rgba(11,26,46,.25)" if v==0 else "rgba(11,26,46,.08)"}" stroke-width="1.5"/>')
        g.append(f'<text x="{L-10}" y="{Y(v)+7:.1f}" text-anchor="end" font-family="Hanken Grotesk" font-size="20" fill="{SLATE}">{yfmt(v)}</text>')
    for i,t in xlab: g.append(f'<text x="{X(i):.1f}" y="{ch-16}" text-anchor="middle" font-family="Hanken Grotesk" font-size="21" fill="{SLATE}">{t}</text>')
    ends=[]
    for v,lab,col in ((A,la,BLUE),(B,lb,ORANGE)):
        d="M"+" L".join(f"{X(i):.1f},{Y(y):.1f}" for i,y in enumerate(v))
        g.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')
        ends.append([Y(v[-1]),lab,col])
    ends.sort()
    if ends[1][0]-ends[0][0]<30: ends[1][0]=ends[0][0]+30
    for y,lab,col in ends: g.append(f'<text x="{cw-R+12}" y="{y+7:.1f}" font-family="Hanken Grotesk" font-weight="600" font-size="22" fill="{col}">{esc(lab)}</text>')
    return f'<svg width="{cw}" height="{ch}" viewBox="0 0 {cw} {ch}">{"".join(g)}</svg>'
def head(n,h,sub,size):
    return (f'<div style="display:flex;justify-content:space-between;align-items:center"><div style="font:700 22px/1 \'Bricolage Grotesque\';letter-spacing:.14em;text-transform:uppercase;color:{BLUE}">Before the Date · No. {n:02d}</div><img src="{LOGO}" style="height:30px"></div>'
      f'<div style="display:flex;flex-direction:column;gap:12px"><h1 style="margin:0;font:600 {size}px/1.04 Cormorant,serif;color:{INK}">'+''.join(f'<span style="display:block;white-space:nowrap">{esc(l)}</span>' for l in h)+f'</h1><p style="margin:0;font:400 28px/1.35 \'Hanken Grotesk\';color:{SLATE}">{esc(sub)}</p></div>')
def statblock(big,t1,t2):
    return f'<div style="display:flex;align-items:center;gap:28px"><div style="font:800 104px/.86 \'Bricolage Grotesque\';letter-spacing:-.03em;color:{CORAL}">{big}</div><div style="font:400 23px/1.45 \'Hanken Grotesk\';color:{SLATE}"><span style="display:block;white-space:nowrap">{t1}</span><span style="display:block;white-space:nowrap">{t2}</span></div></div>'
def foot(s): return f'<div style="border-top:1px solid rgba(11,26,46,.14);padding-top:20px;font:400 19px/1.5 \'Hanken Grotesk\';color:{SLATE}">{esc(s)}</div>'
pages=[]
for p in P:
    if p['src']=='ads':
        A=ADS[p['a']];B=ADS[p['b']];top=max(A+B)
        step={4400:1000,8100:2000,390:100}[top]; ymax=(top//step+1)*step
        ticks=list(range(0,ymax+1,step*(2 if ymax/step>5 else 1)))
        xlab=[(i,m) for i,m in enumerate(["Nov","","","Feb","","","May","","","Aug","","Oct"]) if m]
        ch=lines_chart(ADM,A,B,p['la'],p['lb'],ymax,ticks,lambda v:f"{v:,}",xlab)
        big,t1=p['stat']; st=statblock(big,f'<b style="color:{INK};font-weight:600">{esc(t1.split(" ",3)[0]+" "+t1.split(" ",3)[1]+" "+t1.split(" ",3)[2])}</b>',esc(t1.split(" ",3)[3]))
        src=AD+" Google does not say who searched."
    else:
        ms=[m for m in S[p['a']]]; A=np.array([S[p['a']][m] for m in ms]); B=np.array([S[p['b']][m] for m in ms])
        k=100/max(A.max(),B.max()); A=A*k; B=B*k
        xlab=[(i,m[:4]) for i,m in enumerate(ms) if m.endswith('-01')]
        ch=lines_chart(ms,A,B,p['la'],p['lb'],100,[0,50,100],lambda v:str(v),xlab)
        rr=A.mean()/B.mean()
        st=statblock(f"{rr:.1f}×",f'<b style="color:{INK};font-weight:600">More searches over five years</b>',f'for “{esc(p["a"])}.”')
        src=TR
    size=72 if len(p['h'])<=2 and max(len(x) for x in p['h'])<=24 else 64
    pages.append((p['h'],p['cap'],head(len(pages)+1,p['h'],p['sub'],size)+f'<div style="flex:1;display:flex;align-items:center">{ch}</div>'+st+foot(src)))
# DOW bar post kept as a chart
d=[("Mon",1.08),("Tue",1.05),("Wed",1.03),("Thu",1.07),("Fri",1.05),("Sat",0.87),("Sun",0.85)]
cols="".join(f'''<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:12px;height:100%"><div style="font:700 26px/1 'Bricolage Grotesque';color:{INK}">{round(v*100)}</div><div style="width:84px;height:{round((v-0.6)*900)}px;background:{BLUE if v>1 else TINT};border-radius:10px 10px 0 0"></div><div style="font:600 24px/1 'Hanken Grotesk';color:{SLATE}">{n}</div></div>''' for n,v in d)
dow=f'<div style="flex:1;display:flex;flex-direction:column;gap:20px;background:#fff;border-radius:16px;padding:40px 48px"><div style="font:400 22px/1.4 \'Hanken Grotesk\';color:{SLATE}">Searches for “does he like me” by day of the week. 100 = the daily average.</div><div style="flex:1;display:flex;justify-content:space-between;align-items:flex-end">{cols}</div></div>'
pages.append((["“Does he like me?”","is a weekday worry."],"Overthinking runs Monday to Friday. Searches for “does he like me” sit about 5% to 8% above average on weekdays and drop about 15% on Saturdays and Sundays. Maybe that's when the dates happen. Guys: a midweek text goes further than you think.\n\nWhat day do you overthink the most?",
  head(len(pages)+1,["“Does he like me?”","is a weekday worry."],"Searches drop about 15% on weekends. Busy, or on a date?",72)+dow+statblock("−15%",f'<b style="color:{INK};font-weight:600">Weekend dip</b> vs. the daily average','on Saturdays and Sundays.')+foot("Google Trends daily U.S. search interest, Aug 15 to Nov 14, 2026, averaged by day of the week.")))
items=[]
for i,(h,cap,inner) in enumerate(pages,1):
    open(f"btd-{i:02d}.html","w").write(f'<html><head><style>{CSS}</style></head><body><div style="width:1080px;height:1350px;box-sizing:border-box;padding:60px 64px;background:{PAPER};display:flex;flex-direction:column;gap:28px;overflow:hidden">{inner}</div></body></html>')
    items.append({"n":i,"file":f"posts/btd-{i:02d}.png","title":" ".join(h),"cap":cap})
json.dump(items,open('items.json','w'),ensure_ascii=False);print(len(items))
