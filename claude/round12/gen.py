import html, json
BLUE="#1F4FE0";INK="#0B1A2E";CORAL="#FF5A3C";PAPER="#F4F1EA";SLATE="#556070";TINT="#C9D4F6"
LOGO="file:///home/claude/work/canvas/logo.svg"
F='/home/claude/research/assets/fonts/'
CSS=f"""@font-face{{font-family:Cormorant;src:url(file://{F}cormorant.woff2);font-weight:300 700}}@font-face{{font-family:'Bricolage Grotesque';src:url(file://{F}bricolage-grotesque.woff2);font-weight:200 800}}@font-face{{font-family:'Hanken Grotesk';src:url(file://{F}hanken-grotesk.woff2);font-weight:100 900}}body{{margin:0}}"""
esc=lambda s:html.escape(s,quote=True)
TR="Source: Google Trends, U.S. search interest, past 12 months (Nov 2025 to Nov 2026), both phrases pulled together. Searches about “him” come mostly from women, but not only."
AD="Source: Google Ads average monthly U.S. searches, Nov 2025 to Oct 2026. Volumes are rounded estimates."
P=[
 dict(h=["“First date outfit” gets","4× the searches of","“first date outfit men.”"],sub="She is planning her look. Plan yours.",a=("first date outfit",4400),b=("first date outfit men",1000),unit="searches a month",src=AD,
  cap="She already knows what she's wearing. “First date outfit” gets about 4,400 searches a month. “First date outfit men” gets about 1,000. Guys: a clean fit and a fresh haircut go a long way. Search data, not science.\n\nWhat's your go-to first date fit?"),
 dict(h=["“Red flags in a man”","gets 4× the searches."],sub="She is checking. Don't be one.",a=("red flags in a man",8100),b=("red flags in a woman",1900),unit="searches a month",src=AD,
  cap="Before the date, she's doing her homework. “Red flags in a man” gets about 8,100 searches a month, more than 4 times “red flags in a woman” (about 1,900). Show up on time, put the phone away, be kind to the server. Search data, not science.\n\nBiggest first date red flag? Go."),
 dict(h=["“How to get him to commit”","beats “her” 26 to 1."],sub="If you're serious, say so.",a=("how to get him to commit",260),b=("how to get her to commit",10),unit="searches a month",src=AD,
  cap="Mixed signals are exhausting. “How to get him to commit” gets about 260 searches a month. “How to get her to commit”? About 10. If you know what you want, saying it out loud is the move. Search data, not science.\n\nTag someone who needs to hear this."),
 dict(h=["“Is he the one?”","outsearches “is she the one?”"],sub="By about 1.5 to 1.",a=("is he the one",66),b=("is she the one",45),unit="avg. search interest",src=TR,
  cap="She's thinking long term. Searches for “is he the one” run about 1.5 times “is she the one” in Google Trends over the past year. Guys: consistency is what answers that question. Search data, not science.\n\nWhen did you know?"),
 dict(h=["“Does he like me?”","beats “does she like me?”"],sub="Just not by as much as you'd think.",a=("does he like me",63),b=("does she like me",47),unit="avg. search interest",src=TR,
  cap="Overthinking is universal. “Does he like me” runs about 1.3 times “does she like me” in Google Trends over the past year. So yes, she's wondering too. Text back. Make the plan. Search data, not science.\n\nDouble text: yes or no?"),
 dict(h=["Plot twist: guys are","more confused."],sub="“How to tell if a girl likes you” wins this one.",a=("how to tell if a girl likes you",42),b=("how to tell if a guy likes you",30),unit="avg. search interest",src="Source: Google Trends, U.S. search interest, past 12 months (Nov 2025 to Nov 2026), both phrases pulled together.",flip=True,
  cap="Guys, you're not alone. “How to tell if a girl likes you” gets about 1.4 times the searches of “how to tell if a guy likes you” in Google Trends over the past year. Easiest way to find out? Ask her out. Search data, not science.\n\nTag the friend who overthinks everything."),
 dict(h=["“Is he cheating?”","barely beats","“is she cheating?”"],sub="The suspicion runs both ways.",a=("is he cheating",75),b=("is she cheating",59),unit="avg. search interest",src=TR,
  cap="Trust issues are not just a her thing. “Is he cheating” runs only about 1.3 times “is she cheating” in Google Trends over the past year. Be the person nobody has to Google about. Search data, not science."),
]
def top(n):return f'<div style="display:flex;justify-content:space-between;align-items:center"><div style="font:700 22px/1 \'Bricolage Grotesque\';letter-spacing:.14em;text-transform:uppercase;color:{BLUE}">Before the Date · No. {n:02d}</div><img src="{LOGO}" style="height:30px"></div>'
def headline(lines,size):return '<h1 style="margin:0;font:600 %dpx/1.04 Cormorant,serif;color:%s">'%(size,INK)+''.join(f'<span style="display:block;white-space:nowrap">{esc(l)}</span>' for l in lines)+'</h1>'
def foot(src):return f'<div style="border-top:1px solid rgba(11,26,46,.14);padding-top:22px;font:400 19px/1.5 \'Hanken Grotesk\';color:{SLATE}">{esc(src)}</div>'
def fmt(v,unit):return f"{v:,}" if unit.startswith("searches") else f"{v}"
def bars(p):
    (la,va),(lb,vb)=p['a'],p['b']; mx=max(va,vb); r=va/vb
    def row(l,v,col,big):
        w=max(8,round(v/mx*820))
        return f'''<div style="display:flex;flex-direction:column;gap:12px"><div style="font:600 30px/1.2 'Hanken Grotesk';color:{INK}">“{esc(l)}”</div>
<div style="display:flex;align-items:center;gap:18px"><div style="width:{w}px;height:72px;background:{col};border-radius:0 10px 10px 0"></div><div style="font:800 40px/1 'Bricolage Grotesque';color:{INK};white-space:nowrap">{fmt(v,p['unit'])}</div></div></div>'''
    ratio=f"{r:.1f}×" if r<10 else f"{round(r)}×"
    return f'''<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px;background:#fff;border-radius:16px;padding:48px">
{row(la,va,BLUE,True)}{row(lb,vb,TINT,False)}
<div style="display:flex;align-items:baseline;gap:20px;border-top:1px solid rgba(11,26,46,.10);padding-top:28px"><div style="font:800 96px/.86 'Bricolage Grotesque';letter-spacing:-.03em;color:{CORAL}">{ratio}</div><div style="font:400 24px/1.4 'Hanken Grotesk';color:{SLATE}">as many searches for the top phrase</div></div></div>'''
def dow():
    d=[("Mon",1.08),("Tue",1.05),("Wed",1.03),("Thu",1.07),("Fri",1.05),("Sat",0.87),("Sun",0.85)]
    cols="".join(f'''<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:12px;height:100%"><div style="font:700 26px/1 'Bricolage Grotesque';color:{INK}">{round(v*100)}</div><div style="width:84px;height:{round((v-0.6)*900)}px;background:{BLUE if v>1 else TINT};border-radius:10px 10px 0 0"></div><div style="font:600 24px/1 'Hanken Grotesk';color:{SLATE}">{n}</div></div>''' for n,v in d)
    return f'''<div style="flex:1;display:flex;flex-direction:column;gap:20px;background:#fff;border-radius:16px;padding:44px 48px">
<div style="font:400 22px/1.4 'Hanken Grotesk';color:{SLATE}">Searches for “does he like me” by day of the week. 100 = the daily average.</div>
<div style="flex:1;display:flex;justify-content:space-between;align-items:flex-end">{cols}</div></div>'''
pages=[]
for i,p in enumerate(P,1):
    size=72 if len(p['h'])<=2 else 64
    inner=top(i)+f'<div style="display:flex;flex-direction:column;gap:14px">{headline(p["h"],size)}<p style="margin:0;font:400 28px/1.35 \'Hanken Grotesk\';color:{SLATE}">{esc(p["sub"])}</p></div>'+bars(p)+foot(p['src'])
    pages.append((p['h'],p['cap'],inner))
# DOW post
inner=top(8)+f'<div style="display:flex;flex-direction:column;gap:14px">{headline(["“Does he like me?”","is a weekday worry."],72)}<p style="margin:0;font:400 28px/1.35 \'Hanken Grotesk\';color:{SLATE}">Searches drop about 15% on weekends. Busy, or on a date?</p></div>'+dow()+foot("Source: Google Trends daily U.S. search interest, Aug 15 to Nov 14, 2026, averaged by day of the week.")
pages.append((["“Does he like me?” is a weekday worry."],"Overthinking runs Monday to Friday. Searches for “does he like me” sit about 5% to 8% above average on weekdays and drop about 15% below on Saturdays and Sundays. Maybe that's when the dates happen. Guys: a midweek text goes further than you think. Search data, not science.\n\nWhat day do you overthink the most?",inner))
items=[]
for i,(h,cap,inner) in enumerate(pages,1):
    page=f'<html><head><style>{CSS}</style></head><body><div style="width:1080px;height:1350px;box-sizing:border-box;padding:64px;background:{PAPER};display:flex;flex-direction:column;gap:34px;overflow:hidden">{inner}</div></body></html>'
    fn=f"btd-{i:02d}"
    open(f"{fn}.html","w").write(page)
    items.append({"n":i,"file":f"posts/{fn}.png","title":" ".join(h),"cap":cap})
json.dump(items,open('items.json','w'),ensure_ascii=False)
print(len(items))
