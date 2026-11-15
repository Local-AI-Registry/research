import json,sys,statistics as st
sys.path.insert(0,'/home/claude/work/aff');import demo
D=demo.D
mid=[21,29.5,39.5,49.5,59.5]; SPEND=[647,863,1202,1226,1023]  # BLS 2024 personal care per household
beauty=['botox','lip filler','facelift','liposuction','tummy tuck','nose job','breast augmentation','microneedling','chemical peel','laser hair removal','lash extensions','brazilian wax','eyebrow threading','spray tan','teeth whitening','hair salon','nail salon']
every=[k for k in D if k not in beauty]
def share(ag): s=sum(ag); return [x/s for x in ag]
def center(ag): sh=share(ag); return sum(a*b for a,b in zip(sh,mid))
def sw(ag): sh=share(ag); return sum(a*b for a,b in zip(sh,SPEND))
base_c=st.mean(center(D[k][0]) for k in every); base_sw=st.mean(sw(D[k][0]) for k in every)
print('baseline center %.1f spendw %.0f'%(base_c,base_sw))
rows=[]
for k in beauty:
  ag,(f,m)=D[k]; rows.append((k,round(center(ag),1),round(sw(ag)),round(100*m/(f+m))))
for r in sorted(rows,key=lambda r:r[1]): print(r)
print('everyday male share median', st.median(100*D[k][1][1]/sum(D[k][1]) for k in every))
out={'ladder':sorted(rows,key=lambda r:r[1]),'base_center':round(base_c,1),'base_sw':round(base_sw)}
# co-promo groups
a=json.load(open('/home/claude/work/aff/aff.json'))
G={'Fast food & treats':['pizza near me','taco bell','chick fil a','wingstop','hot dog','ice cream near me','boba near me','starbucks','sushi near me'],
 'Drinks':['wine','tequila','margarita','white claw','beer','aperol spritz','espresso martini'],
 'Fitness & active':['pilates','pickleball','golf','lululemon','kayak'],
 'Dating & weddings':['tinder','bumble','engagement ring','wedding dress'],
 'Astrology & tarot':['tarot','astrology','horoscope','crystals'],
 'Big-ticket buys':['tesla','hot tub'],
 'Screens & pop culture':['tiktok','taylor swift','love island','wordle','fantasy football'],
 'Weight-loss drugs':['ozempic']}
res={}
for g,cs in G.items():
  for scope,ts in [('botox',['botox near me']),('all',None)]:
    sel=[x for x in a if x['c'] in cs and (ts is None or x['t'] in ts)]
    res.setdefault(g,{})[scope]=dict(place=round(st.mean(x['state'] for x in sel),2),people=round(st.mean(x['dage'] for x in sel),2),passes=round(st.mean(x['n'] for x in sel),2),
      best=max(sel,key=lambda x:(x['n'],x['state']+x['dage']))['c'])
for g in sorted(res,key=lambda g:-(res[g]['all']['place']+res[g]['all']['people'])): print(f'{g:22s}',res[g])
out['groups']=res
# states
W=json.load(open('/home/claude/work/r14/all.json'));M=W['MAPS']
st_list=[s for s in M['botox near me'] if s not in('WY','DC')]
from scipy.stats import rankdata,spearmanr
bt=['botox near me','lip filler','microneedling','hydrafacial','med spa near me','laser hair removal','chemical peel','dermaplaning']
bt=[t for t in bt if t in M]
def z(t):
  v=[M[t].get(s,0) for s in st_list];mu=st.mean(v);sd=st.pstdev(v);return [(x-mu)/sd for x in v]
idx=[st.mean(col) for col in zip(*[z(t) for t in bt])]
order=sorted(zip(st_list,idx),key=lambda x:-x[1]);print('med spa index terms',bt);print('top',order[:10]);print('bottom',order[-8:])
cors=[]
for t in M:
  if t in bt: continue
  v=[M[t].get(s,0) for s in st_list]; r,p=spearmanr(idx,v); cors.append((t,round(r,2),p))
cors.sort(key=lambda x:-x[1]);print('top geo matches',cors[:12]);print('least',cors[-8:])
out['states']={'terms':bt,'top':[(s,round(v,2)) for s,v in order[:10]],'bottom':[(s,round(v,2)) for s,v in order[-5:]],'geo':[(t,r) for t,r,p in cors[:10]],'geo_low':[(t,r) for t,r,p in cors[-6:]]}
json.dump(out,open('mix.json','w'),indent=1)
