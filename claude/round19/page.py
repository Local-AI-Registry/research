import json,numpy as np
exec(open('fc.py').read().split('res=[]')[0])
d,v=S['sephora'];Q=quarters(d,v);nc=json.load(open('nowcast.json'))
T2=T[1:]
X=np.array([[1,yoy(Q,k),R[prev(k,1)]] for k in T2]);y=np.array([R[k] for k in T2])
fit=lambda X,y:np.linalg.lstsq(X,y,rcond=None)[0]
loo=[]
for i in range(len(T2)):
  m=np.ones(len(T2),bool);m[i]=False;loo.append(float(X[i]@fit(X[m],y[m])))
mae=np.mean(abs(np.array(loo)-y))
c=fit(X,y);f4=float(c@[1,nc['g4'],R['2026Q3']]);q4=90.3*(1+f4);lo=90.3*(1+f4-mae);hi=90.3*(1+f4+mae)
pred_rev={k:EOLS[prev(k)]*(1+p) for k,p in zip(T2,loo)}
hits=sum(abs(pred_rev[k]-EOLS[k])/EOLS[k]<0.07 for k in T2)
print('q4 %.1f range %.1f-%.1f mae %.1f'%(q4,lo,hi,100*mae),'within7%',hits,len(T2))
print({k:round(pred_rev[k],1) for k in T2})
BLUE='#1F4FE0';CORAL='#FF5A3C';INK='#0B1A2E'
lab=lambda k:"Q"+k[-1]+" ’"+k[2:4]
def line(series,ks,ymin,ymax,step,fmt,extra='',w=640,h=320,L=54,R_=26,T_=16,B=40,n=None):
  n=n or len(ks);X_=lambda i:L+(w-L-R_)*i/(n-1);Y=lambda v:T_+(h-T_-B)*(1-(v-ymin)/(ymax-ymin))
  s=[f'<svg viewBox="0 0 {w} {h}" role="img">']
  t=ymin
  while t<=ymax+1e-9:
    s.append(f'<line x1="{L}" x2="{w-R_}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="{"rgba(11,26,46,.35)" if t==0 else "rgba(11,26,46,.08)"}"/><text class="ax" x="{L-8}" y="{Y(t)+4:.1f}" text-anchor="end">{fmt(t)}</text>');t+=step
  for i,k in enumerate(ks):
    if k.endswith('Q1'): s.append(f'<text class="ax" x="{X_(i):.1f}" y="{h-14}" text-anchor="middle">{k[:4]}</text>')
  s.append(extra.format(X=X_,Y=Y) if False else '')
  for name,vals,col,dash in series:
    pts=[(X_(i),Y(v)) for i,v in enumerate(vals) if v is not None]
    s.append(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)}" fill="none" stroke="{col}" stroke-width="2.5" {"stroke-dasharray=\"6 5\"" if dash else ""}/>')
    for (a,b),(i,vv) in zip(pts,[(i,v) for i,v in enumerate(vals) if v is not None]): s.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="4" fill="{col}" stroke="#fff" stroke-width="2"><title>{name} {lab(ks[i])}: {fmt(vv)}</title></circle>')
  return s,X_,Y
# chart 1: growth lines
s,X_,Y=line([('Sephora searches vs. a year before',[100*yoy(Q,k) for k in T],INK,0),('Evolus revenue vs. a year before',[100*R[k] for k in T],CORAL,0)],T,-20,50,10,lambda t:f'{t:+.0f}%' if t else '0%')
s.append('</svg>');c1=''.join(s)
# chart 2: actual vs predicted + forecast
ks=T+['2026Q4']
act=[EOLS[k] for k in T]+[None];prd=[None]+[pred_rev[k] for k in T2]+[q4]
s,X_,Y=line([('Actual Evolus revenue',act,CORAL,0),('Our search-based estimate',prd,BLUE,1)],ks,30,120,15,lambda t:f'${t:.0f}M')
i=len(ks)-1;x=X_(i)
s.insert(1,f'<rect x="{x-14:.1f}" y="{Y(101.76):.1f}" width="28" height="{Y(94.76)-Y(101.76):.1f}" fill="rgba(11,26,46,.12)" rx="4"/><line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(hi):.1f}" y2="{Y(lo):.1f}" stroke="{BLUE}" stroke-width="2"/>')
s.append(f'<text x="{x-20:.1f}" y="{Y(q4)-2:.1f}" text-anchor="end" style="font:700 13px Bricolage Grotesque;fill:{BLUE}">Q4 ’26 est. ${q4:.0f}M</text><text x="{x-20:.1f}" y="{Y(94.76)+16:.1f}" text-anchor="end" style="font:600 12px Hanken Grotesk;fill:#556070">Evolus guidance range</text></svg>')
c2=''.join(s)
json.dump(dict(q4=q4,lo=lo,hi=hi,mae=100*mae,hits=int(hits),n=len(T2),g4=100*nc['g4'],f4=100*f4),open('final.json','w'))
open('c1.svg','w').write(c1);open('c2.svg','w').write(c2)
