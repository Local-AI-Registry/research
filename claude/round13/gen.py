import sys,json,html,datetime as dt
sys.path.insert(0,'/home/claude/work/r13'); from weekly import W
import numpy as np
BLUE="#1F4FE0";INK="#0B1A2E";CORAL="#FF5A3C";PAPER="#F4F1EA";SLATE="#556070"
LOGO="file:///home/claude/work/canvas/logo.svg";F='/home/claude/research/assets/fonts/'
CSS=f"""@font-face{{font-family:Cormorant;src:url(file://{F}cormorant.woff2);font-weight:300 700}}@font-face{{font-family:'Bricolage Grotesque';src:url(file://{F}bricolage-grotesque.woff2);font-weight:200 800}}@font-face{{font-family:'Hanken Grotesk';src:url(file://{F}hanken-grotesk.woff2);font-weight:100 900}}body{{margin:0}}"""
esc=lambda s:html.escape(s,quote=True)
D0=dt.date(2025,11,9); dates=[D0+dt.timedelta(weeks=i) for i in range(53)]
SRC="Source: Google Trends weekly U.S. search interest, Nov 2025 to Nov 2026. Each line is scaled from its own low to its own high. Correlation, not causation. Obviously."
P=[
 dict(a="brazilian",b="icecream",la="“Brazilian wax”",lb="“ice cream near me”",h=["Brazilian wax and ice cream","search the same way."],sub="Treat yourself, apparently.",
  cap="Science has spoken (it hasn't). Searches for “Brazilian wax” and “ice cream near me” rise and fall together all year, a 0.93 match week by week. Both peak in summer, which is the boring real reason. The fun reason is yours to decide. Correlation, not causation. Obviously.\n\nTag your post-wax ice cream buddy."),
 dict(a="laser",b="kayak",la="“laser hair removal”",lb="“kayak”",h=["Laser hair removal and kayaks:","basically the same chart."],sub="Smooth on land. Smooth on water.",
  cap="These two lines are almost the same (a 0.96 weekly match). “Laser hair removal” and “kayak” both climb in spring, peak in summer and fade by fall. Does laser hair removal make you want to paddle? No. But it's fun to pretend. Correlation, not causation. Obviously."),
 dict(a="brazilian",b="kayak",la="“Brazilian wax”",lb="“kayak”",h=["Brazilian wax season","is kayak season."],sub="Paddle responsibly.",
  cap="Another summer twin. “Brazilian wax” and “kayak” searches move together week by week (a 0.92 match). The real reason is summer. The funny reason is up to you. Correlation, not causation. Obviously.\n\nWho's going kayaking this summer?"),
 dict(a="botox",b="pickleball",la="“Botox near me”",lb="“pickleball”",h=["Botox people are","pickleball people."],sub="Twins by season and by state.",
  cap="Botox and pickleball keep showing up together. Their weekly searches line up (a 0.71 match), and in our earlier state map, the states that search Botox the most also search pickleball the most. Frozen forehead, fast hands. Correlation, not causation. Obviously.\n\nTag your pickleball partner."),
 dict(a="botox",b="pizza",la="“Botox near me”",lb="“pizza near me”",h=["Botox and pizza peaked","the exact same week."],sub="June 14 to 20, 2026. Coincidence? Yes.",peak=True,
  cap="Searches for “Botox near me” and “pizza near me” both hit their highest week of the year at the same time: June 14 to 20, 2026. Both roughly doubled from last November. Does a fresh Botox appointment mean pizza night? Science says no. We say maybe. Correlation, not causation. Obviously."),
]
def r(a,b): return float(np.corrcoef(W[a],W[b])[0,1])
def chart(p):
    cw,ch=952,600;L,R,T,B=24,24,40,62
    def path(k):
        v=np.array(W[k],float); v=(v-v.min())/(v.max()-v.min())*100
        pts=[(L+i/52*(cw-L-R), T+(1-y/100)*(ch-T-B)) for i,y in enumerate(v)]
        return "M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts), pts
    pa,ptA=path(p['a']); pb,ptB=path(p['b'])
    g=[f'<rect x="0" y="0" width="{cw}" height="{ch}" rx="16" fill="#fff"/>']
    for gy in (0,50,100):
        y=T+(1-gy/100)*(ch-T-B); g.append(f'<line x1="{L}" x2="{cw-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="rgba(11,26,46,.08)" stroke-width="1.5"/>')
    for i,d in enumerate(dates):
        if d.day<=7 and d.month in (1,3,5,7,9,11):
            x=L+i/52*(cw-L-R); g.append(f'<text x="{x:.1f}" y="{ch-18}" text-anchor="middle" font-family="Hanken Grotesk" font-size="22" fill="{SLATE}">{d.strftime("%b")}</text>')
    g.append(f'<path d="{pb}" fill="none" stroke="{CORAL}" stroke-width="5" stroke-linejoin="round"/>')
    g.append(f'<path d="{pa}" fill="none" stroke="{BLUE}" stroke-width="5" stroke-linejoin="round"/>')
    if p.get('peak'):
        i=int(np.argmax(W[p['a']])); x=ptA[i][0]
        g.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{T}" y2="{ch-B}" stroke="{INK}" stroke-width="2" stroke-dasharray="6 6"/>')
        g.append(f'<text x="{x-14:.1f}" y="{ch-B-16}" text-anchor="end" font-family="Hanken Grotesk" font-weight="600" font-size="22" fill="{INK}">Same peak week: June 14 to 20</text>')
    return f'<svg width="{cw}" height="{ch}" viewBox="0 0 {cw} {ch}">{"".join(g)}</svg>'
def legend(p):
    item=lambda c,l:f'<div style="display:flex;align-items:center;gap:12px"><div style="width:36px;height:6px;border-radius:3px;background:{c}"></div><div style="font:600 26px/1.2 \'Hanken Grotesk\';color:{INK}">{esc(l)}</div></div>'
    return f'<div style="display:flex;gap:36px;flex-wrap:wrap">{item(BLUE,p["la"])}{item(CORAL,p["lb"])}</div>'
items=[]
for i,p in enumerate(P,1):
    rv=r(p['a'],p['b'])
    stat=(f'<div style="display:flex;align-items:center;gap:28px"><div style="font:800 104px/.86 \'Bricolage Grotesque\';letter-spacing:-.03em;color:{CORAL}">{rv:.2f}</div><div style="font:400 23px/1.45 \'Hanken Grotesk\';color:{SLATE}"><span style="display:block;white-space:nowrap"><b style="color:{INK};font-weight:600">Weekly match score.</b> 1.00 means the</span><span style="display:block;white-space:nowrap">two lines move exactly together.</span></div></div>')
    if p.get('peak'):
        stat=(f'<div style="display:flex;align-items:center;gap:28px"><div style="font:800 104px/.86 \'Bricolage Grotesque\';letter-spacing:-.03em;color:{CORAL}">2×</div><div style="font:400 23px/1.45 \'Hanken Grotesk\';color:{SLATE}"><span style="display:block;white-space:nowrap"><b style="color:{INK};font-weight:600">Both roughly doubled</b> from November</span><span style="display:block;white-space:nowrap">to their June peak.</span></div></div>')
    size=68 if max(len(l) for l in p['h'])>26 else 74
    inner=(f'<div style="display:flex;justify-content:space-between;align-items:center"><div style="font:700 22px/1 \'Bricolage Grotesque\';letter-spacing:.14em;text-transform:uppercase;color:{BLUE}">Correlation, Not Causation · No. {i:02d}</div><img src="{LOGO}" style="height:30px"></div>'
      f'<div style="display:flex;flex-direction:column;gap:12px"><h1 style="margin:0;font:600 {size}px/1.04 Cormorant,serif;color:{INK}">'+''.join(f'<span style="display:block;white-space:nowrap">{esc(l)}</span>' for l in p['h'])+f'</h1><p style="margin:0;font:400 28px/1.35 \'Hanken Grotesk\';color:{SLATE}">{esc(p["sub"])}</p></div>'
      +legend(p)+f'<div style="flex:1;display:flex;align-items:center">{chart(p)}</div>'+stat
      +f'<div style="border-top:1px solid rgba(11,26,46,.14);padding-top:20px;font:400 19px/1.5 \'Hanken Grotesk\';color:{SLATE}">{esc(SRC)}</div>')
    open(f"cnc-{i:02d}.html","w").write(f'<html><head><style>{CSS}</style></head><body><div style="width:1080px;height:1350px;box-sizing:border-box;padding:60px 64px;background:{PAPER};display:flex;flex-direction:column;gap:26px;overflow:hidden">{inner}</div></body></html>')
    items.append({"n":i,"file":f"posts/cnc-{i:02d}.png","title":" ".join(p['h']),"cap":p['cap'],"r":round(rv,2)})
json.dump(items,open('items.json','w'),ensure_ascii=False); print([(x['n'],x['r']) for x in items])
# check peak weeks
for k in ['botox','pizza']: i=int(np.argmax(W[k])); print(k,dates[i],W[k][i],W[k][0])
