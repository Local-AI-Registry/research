import json,numpy as np,collections
A=json.load(open('all.json'));W=A['W']
def monthly(k):
    s=W[k];acc=collections.OrderedDict()
    for d,v in zip(s['dates'],s['v']):
        if v is None: continue
        acc.setdefault(d[:7],[]).append(v)
    ks=[m for m in acc if '2021-12'<=m<='2026-10']
    return ks,np.array([np.mean(acc[m]) for m in ks])
M={};MON=None
for k in W:
    v=[x for x in W[k]['v'] if x is not None]
    if max(v)<15 and k not in('botox near me',): continue
    MON,M[k]=monthly(k)
beauty=["botox near me","lip filler","laser hair removal","spray tan","lash extensions","brazilian wax","microneedling","teeth whitening","facelift","liposuction","tummy tuck","nose job","breast augmentation","chemical peel","nail salon near me","hair salon near me","eyebrow threading"]
beauty=[b for b in beauty if b in M]
ctrl=["mattress","costco"]
other=[k for k in M if k not in beauty and k not in ctrl]
def detr(x):
    ma=np.convolve(x,np.ones(12)/12,mode='same'); ma[:6]=ma[6]; ma[-6:]=ma[-7]
    return x/ma
def r(x,y): return float(np.corrcoef(x,y)[0,1])
res=[]
for b in beauty:
    cr=max(r(M[b],M[c]) for c in ctrl); cd=max(r(detr(M[b]),detr(M[c])) for c in ctrl)
    for o in other:
        res.append(dict(b=b,o=o,raw=r(M[b],M[o]),det=r(detr(M[b]),detr(M[o])),craw=cr,cdet=cd))
for x in res: x['score']=min(x['raw'],x['det']+0.15)
res.sort(key=lambda x:-x['score'])
print(len(M),'usable series',len(res),'pairs; months',MON[0],MON[-1],len(MON))
for x in res[:45]:
    flag='' if (x['raw']>x['craw'] and x['det']>x['cdet']) else ' (ctrl)'
    print(f"raw {x['raw']:.2f} det {x['det']:.2f} | ctrl {x['craw']:.2f}/{x['cdet']:.2f} {x['b']} ~ {x['o']}{flag}")
json.dump({'MON':MON,'M':{k:v.tolist() for k,v in M.items()}},open('monthly.json','w'))
json.dump(res,open('pairs.json','w'))
