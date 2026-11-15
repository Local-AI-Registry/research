import json,statistics as st,sys
sys.path.insert(0,'/home/claude/work/aff');import demo
o=json.load(open('mix.json'));W=json.load(open('/home/claude/work/r14/all.json'));M=W['MAPS']
BLUE='#1F4FE0';CORAL='#FF5A3C';INK='#0B1A2E';GR='#B9C0CC'
st_list=[s for s in M['botox near me'] if s not in('WY','DC')]
bt=o['states']['terms']
def z(t):
  v=[M[t].get(s,0) for s in st_list];mu=st.mean(v);sd=st.pstdev(v);return [(x-mu)/sd for x in v]
idx=[st.mean(c) for c in zip(*[z(t) for t in bt])]
pil=[M['pilates'].get(s,0) for s in st_list]
# scatter
w,h,L,R,T,B=640,380,50,20,16,46
x0,x1=min(idx)-.2,max(idx)+.2;y0,y1=0,max(pil)*1.05
X=lambda v:L+(w-L-R)*(v-x0)/(x1-x0);Y=lambda v:T+(h-T-B)*(1-(v-y0)/(y1-y0))
s=[f'<svg viewBox="0 0 {w} {h}" role="img">']
for t in range(0,101,25):
  if t<=y1: s.append(f'<line x1="{L}" x2="{w-R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="rgba(11,26,46,.08)"/><text class="ax" x="{L-8}" y="{Y(t)+4:.1f}" text-anchor="end">{t}</text>')
s.append(f'<text class="ax" x="{(L+w-R)/2}" y="{h-8}" text-anchor="middle">Med spa search index (8 treatment searches combined) →</text><text class="ax" x="{L}" y="{h-26}">lower</text><text class="ax" x="{w-R}" y="{h-26}" text-anchor="end">higher</text>')
top=set(x for x,_ in o['states']['top'][:5]);bot=set(x for x,_ in o['states']['bottom'][-4:])
for st_,a,b in zip(st_list,idx,pil):
  c=CORAL if st_ in top else (INK if st_ in bot else BLUE)
  s.append(f'<circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="6" fill="{c}" fill-opacity=".85" stroke="#fff" stroke-width="2"><title>{st_}: Pilates search {b}</title></circle>')
  OFF={'SD':(-10,-6,'end'),'IA':(10,10,'start'),'VT':(10,4,'start'),'WV':(10,4,'start'),'CO':(-10,4,'end'),'FL':(-10,4,'end'),'AZ':(-10,4,'end'),'CA':(0,-13,'middle'),'UT':(-10,4,'end')}
  if st_ in top|bot:
    dx,dy,an=OFF.get(st_,(10,4,'start'));s.append(f'<text x="{X(a)+dx:.1f}" y="{Y(b)+dy:.1f}" text-anchor="{an}" style="font:700 12px Bricolage Grotesque;fill:{c}">{st_}</text>')
s.append(f'<text class="ax" x="{L+4}" y="{T+12}">Pilates search, by state</text></svg>')
scatter=''.join(s)
def bars(rows,unit,maxv,colfn,ref=None):
  out='<div class="hb">'
  for n,v in rows:
    out+=f'<div class="hr"><span class="hn">{n}</span><span class="ht"><i style="width:{100*v/maxv:.1f}%;background:{colfn(n,v)}"></i><b>{unit.format(v)}</b></span></div>'
  return out+'</div>'
D=demo.D
men=[('Liposuction','liposuction'),('Facelift','facelift'),('Nose job','nose job'),('Teeth whitening','teeth whitening'),('Breast augmentation','breast augmentation'),('Lip filler','lip filler'),('Botox','botox'),('Hair salon','hair salon'),('Nail salon','nail salon'),('Lash extensions','lash extensions'),('Spray tan','spray tan')]
ms=[(n,round(100*D[k][1][1]/sum(D[k][1]))) for n,k in men]
surg={'Liposuction','Facelift','Nose job','Breast augmentation'}
menbars=bars(ms,'{}%',60,lambda n,v:BLUE if n in surg else GR)
lad=[('Brazilian wax','brazilian wax'),('Lip filler','lip filler'),('Chemical peel','chemical peel'),('Laser hair removal','laser hair removal'),('Liposuction','liposuction'),('Nose job','nose job'),('Facelift','facelift'),('Microneedling','microneedling'),('Botox','botox'),('Teeth whitening','teeth whitening'),('Nail salon','nail salon')]
mid=[21,29.5,39.5,49.5,59.5]
def center(ag): s_=sum(ag);return sum(a/s_*b for a,b in zip(ag,mid))
lr=[(n,round(center(D[k][0]))) for n,k in lad]
ladder='<div class="hb">'+''.join(f'<div class="hr"><span class="hn">{n}</span><span class="ht"><i style="width:{100*(v-25)/(50-25):.1f}%;background:{CORAL if v<35 else BLUE}"></i><b>{v}</b></span></div>' for n,v in lr)+'</div>'
spend=bars([('18 to 24*',647),('25 to 34',863),('35 to 44',1202),('45 to 54',1226),('55 to 64',1023)],'${:,}',1300,lambda n,v:CORAL if v<900 else BLUE)
# seasonal grouped bars
sea=[('Q1',102,92),('Q2',101,105),('Q3',97,96),('Q4',101,106)]
w2,h2=640,250;Lb=40;bw=46;gap=150
s=[f'<svg viewBox="0 0 {w2} {h2}" role="img">']
Yb=lambda v:200-(v-80)*5
for t in [80,90,100,110]:
  s.append(f'<line x1="{Lb}" x2="{w2-10}" y1="{Yb(t)}" y2="{Yb(t)}" stroke="{"rgba(11,26,46,.35)" if t==100 else "rgba(11,26,46,.08)"}"/><text class="ax" x="{Lb-6}" y="{Yb(t)+4}" text-anchor="end">{t}</text>')
for i,(q,a,b) in enumerate(sea):
  cx=Lb+40+i*gap
  for j,(v,c) in enumerate([(a,BLUE),(b,CORAL)]):
    x=cx+j*(bw+4);s.append(f'<rect x="{x}" y="{Yb(v)}" width="{bw}" height="{200-Yb(v)}" rx="4" fill="{c}"/><text x="{x+bw/2}" y="{Yb(v)-6}" text-anchor="middle" style="font:700 13px Bricolage Grotesque;fill:#0B1A2E">{v}</text>')
  s.append(f'<text x="{cx+bw+2}" y="{h2-24}" text-anchor="middle" style="font:700 14px Bricolage Grotesque;fill:#0B1A2E">{q}</text>')
s.append('</svg>');season=''.join(s)
g=o['groups'];order=['Drinks','Fitness & active','Dating & weddings','Fast food & treats','Screens & pop culture','Astrology & tarot','Big-ticket buys','Weight-loss drugs']
wal={'Drinks':'Dining out is the #1 thing clients would cut (54%)','Fitness & active':'Fitness is near the bottom of the cut list (27%)','Dating & weddings':'Big-day spending, short window','Fast food & treats':'Dining out is the #1 thing clients would cut (54%)'}
rows=''.join(f'<tr><td><b>{k}</b><small>best: {g[k]["botox"]["best"]}</small></td><td>{g[k]["botox"]["place"]:.2f}</td><td>{round(100*g[k]["botox"]["people"])}%</td><td>{g[k]["botox"]["passes"]:.1f}</td><td>{wal.get(k,"")}</td></tr>' for k in order)
html=f'''
<section id="mix"><div class="eyebrow">Everything combined</div><h2>Six things the data says when you mix it</h2>
<p>We put every dataset from this project side by side: five years of search, state maps, the age and gender of searchers, company sales, government spending data and client surveys. These are the patterns that show up in more than one source.</p>
<div class="cards">

<div class="card"><div class="ch"><h3>1. The med spa map is the Pilates map</h3><span class="badge b3">0.81 match</span></div>
<p class="take">We combined eight treatment searches into one score per state. The state ranking that matches it best is Pilates (0.81), then Tesla, Rolex, Love Island and Uber Eats (0.74 to 0.75). The opposite map belongs to fishing licenses and crockpots (−0.66).</p>
{scatter}
<p class="take" style="margin-top:10px">Top states: Florida, Arizona, Colorado, Utah and California. Bottom: Vermont, South Dakota, Iowa and West Virginia. Much of this is the map of city life and money, so treat it as a wallet signal, not proof that one causes the other.</p></div>

<div class="card"><div class="ch"><h3>2. Men search for surgery, not upkeep</h3><span class="badge">46% vs 22%</span></div>
<p class="take">Men make up about 46% of searches for liposuction, facelifts and nose jobs. That's close to their share of everyday searches (44%). For upkeep like Botox, nails, lashes and spray tans, their share drops to 22% to 33%.</p>
{menbars}
<p class="take" style="margin-top:10px">Men's share of searches, from DataForSEO's search panel, past 12 months. Blue is surgery. We can't tell whether a man is searching for himself or for a partner.</p></div>

<div class="card"><div class="ch"><h3>3. The youngest searchers have the thinnest wallets</h3><span class="badge b3">Age 33 vs 41</span></div>
<p class="take">The typical lip filler, laser hair removal or Brazilian wax searcher is about 33. The typical Botox searcher is about 41. Households under 35 spend $647 to $863 a year on personal care. Households 35 to 54 spend about $1,200.</p>
<div class="two"><div><div class="mini">Typical age of the searcher</div>{ladder}</div><div><div class="mini">Personal care spend per household, 2024</div>{spend}</div></div>
<p class="take" style="margin-top:10px">Younger clients also stretch more to pay. In a 2026 Zenoti survey, 26% of Gen Z had delayed medical or dental care to pay for beauty, against 11% of boomers. Memberships and payment plans matter most for the youngest treatments. *BLS groups everyone under 25.</p></div>

<div class="card"><div class="ch"><h3>4. Q1 is research season</h3><span class="badge">Searches 102, sales 92</span></div>
<p class="take">Botox searches run at their normal level in January to March. Botox sales to clinics run 8% below average in Q1, then jump in Q2. Each bar is that quarter against the year's average, 2023 to 2025.</p>
<div class="lg"><span><i style="background:{BLUE}"></i>Search for “botox”</span><span><i style="background:{CORAL}"></i>Botox Cosmetic sales</span></div>{season}
<p class="take" style="margin-top:10px">These are AbbVie's sales to practices, not what patients pay, so clinics stocking up in Q4 explains part of it. For a clinic, the takeaway holds: people are still searching in Q1. That is the time to keep marketing, not to cut.</p></div>

<div class="card"><div class="ch"><h3>5. Brand search moves first</h3><span class="badge b3">Club Pilates −17%</span></div>
<p class="take">Searches for a brand's own name track its sales direction (Jeuveau matched 10 of 11 quarters). A generic word like “botox” tracks the category instead: it rose in 2025 while Botox brand sales fell. Club Pilates brand searches stalled in mid-2025, before Xponential's same-store sales turned negative, while plain “pilates” kept growing.</p>
<p class="take">For any local business, the number to watch is searches for your own name next to searches for your category. When the first falls and the second doesn't, a competitor is taking share. <a href="#sales">See the charts</a>.</p></div>

<div class="card"><div class="ch"><h3>6. Who to partner with, ranked</h3><span class="badge">Botox searchers</span></div>
<p class="take">For “botox near me”, we averaged each type of everyday search: do the same states search it, is it the same age mix, and how many of our three tests it passes. Then we checked it against what clients say they spend on.</p>
<div class="tbl"><table style="min-width:760px"><thead><tr><th>Category</th><th>Same states</th><th>Same age mix</th><th>Tests passed (of 3)</th><th>Wallet</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="take" style="margin-top:12px">Wine bars, Pilates studios and bridal shops come out on top. Weight-loss drugs share the age mix but not the states. Fast food looks like a fit on age, but it's spread everywhere, and dining out is the first thing clients cut.</p></div>
</div></section>
'''
open('mix.html','w').write(html)
