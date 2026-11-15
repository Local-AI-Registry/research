import json,numpy as np
from scipy.stats import spearmanr
from demo import D
R=json.load(open('/home/claude/work/r14/all.json')); MAPS=R['MAPS']
Mo=json.load(open('/home/claude/work/r14/monthly.json'));M={k:np.array(v) for k,v in Mo['M'].items()}
DN={"botox near me":"botox","pizza near me":"pizza","ice cream near me":"ice cream","sushi near me":"sushi","nail salon near me":"nail salon","hair salon near me":"hair salon","boba near me":"boba"}
dn=lambda k:DN.get(k,k)
MID=np.array([21,29.5,39.5,49.5,59.5])
def prof(k):
    a,(f,m)=D[dn(k)]; a=np.array(a,float); return a/a.sum(), f/(f+m)
def detr(x):
    ma=np.convolve(x,np.ones(12)/12,mode='same'); ma[:6]=ma[6]; ma[-6:]=ma[-7]; return x/ma
def r(x,y): return float(np.corrcoef(x,y)[0,1])
def state(a,b):
    S=[s for s in MAPS[a] if s in MAPS[b] and s not in('WY','DC')]
    if len(S)<40: return None,None
    rr,p=spearmanr([MAPS[a][s] for s in S],[MAPS[b][s] for s in S]); return float(rr),float(p)
beauty=["botox near me","lip filler","microneedling","nail salon near me","brazilian wax","liposuction","facelift","tummy tuck","laser hair removal","lash extensions","hair salon near me","nose job","breast augmentation","eyebrow threading","spray tan","teeth whitening","chemical peel"]
ctrl=["mattress","costco"]
cands=[k for k in M if k not in beauty and k not in ctrl and dn(k) in D]
out=[]
for t in beauty:
    if t not in M or dn(t) not in D: continue
    cr=max(r(M[t],M[c]) for c in ctrl); cd=max(r(detr(M[t]),detr(M[c])) for c in ctrl)
    ta,tf=prof(t)
    for c in cands:
        raw=r(M[t],M[c]); de=r(detr(M[t]),detr(M[c])); sr,sp=state(t,c); ca,cf=prof(c)
        time_ok= raw>=0.5 and de>=0.4 and raw>cr and de>cd
        place_ok= sr is not None and sr>=0.35 and sp<0.01
        ov=1-0.5*float(np.abs(ta-ca).sum()); people_ok= ov>=0.85 and abs(tf-cf)<=0.10
        out.append(dict(t=t,c=c,raw=round(raw,2),det=round(de,2),state=None if sr is None else round(sr,2),sp=sp,dage=round(ov,2),dfem=round(cf-tf,2),time=time_ok,place=place_ok,people=people_ok,n=int(time_ok)+int(place_ok)+int(people_ok)))
json.dump(out,open('aff.json','w'))
print('pairs',len(out),'targets',len(set(x['t'] for x in out)))
for n in (3,2):
    xs=[x for x in out if x['n']==n]; print(f'--- pass {n}: {len(xs)}')
    for x in sorted(xs,key=lambda x:-(x['raw']+(x['state'] or 0)))[:40]:
        print(f"{x['t']:20s} ~ {x['c']:18s} time {x['raw']:.2f}/{x['det']:.2f} {'Y' if x['time'] else '-'} | state {x['state']} {'Y' if x['place'] else '-'} | age overlap {x['dage']} fem {x['dfem']:+} {'Y' if x['people'] else '-'}")
print('--- the 14 viral posts')
for t,c in [("lip filler","pilates"),("microneedling","monster energy"),("nail salon near me","boba near me"),("hair salon near me","pizza near me"),("microneedling","engagement ring"),("brazilian wax","ice cream near me"),("breast augmentation","wedding dress"),("brazilian wax","white claw"),("liposuction","boba near me"),("botox near me","astrology"),("tummy tuck","sushi near me"),("eyebrow threading","chick fil a"),("liposuction","bumble"),("nose job","tarot")]:
    x=[o for o in out if o['t']==t and o['c']==c][0]
    print(f"{t} ~ {c}: time {'Y' if x['time'] else '-'} place {'Y' if x['place'] else '-'} ({x['state']}) people {'Y' if x['people'] else '-'} (age overlap {x['dage']}, fem {x['dfem']:+}) => {x['n']}/3")
