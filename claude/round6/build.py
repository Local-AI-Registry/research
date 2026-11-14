import json,numpy as np
from scipy.stats import spearmanr
M=json.load(open('statemaps.json'))
def card(p,b,key,xn,yn,xl,yl,xmax=None,extra=()):
    st=sorted([s for s in M['pop'][p] if s in M['beauty'][b] and s not in('WY','DC')],key=lambda s:-M['pop'][p][s])
    pts=[[s,M['pop'][p][s],M['beauty'][b][s]] for s in st]
    rho=spearmanr([q[1] for q in pts],[q[2] for q in pts])[0]
    top=pts[:5];bot=pts[-5:]
    ty=np.mean([q[2] for q in top]);by=np.mean([q[2] for q in bot])
    lab=[q[0] for q in top[:3]]+[q[0] for q in bot[-2:]]+list(extra)
    print(key,p,b,'rho %.2f'%rho,'top5',[(q[0],q[2]) for q in top],round(ty,1),'bot5',[(q[0],q[2]) for q in bot],round(by,1),'ratio %.2f'%(ty/by))
    c={'t':'s','p':pts,'xn':xn,'yn':yn,'xl':xl,'yl':yl,'lab':lab}
    if xmax:c['xmax']=xmax
    return key,c
out=dict([card('love island','botox near me','c11','Love Island','botox near me','Love Island search interest by state →','↑ \"botox near me\" search interest'),
 card('real housewives','botox near me','c12','Real Housewives','botox near me','Real Housewives search interest by state →','↑ \"botox near me\" search interest',xmax=40),
 card('pickleball','botox near me','c13','pickleball','botox near me','Pickleball search interest by state →','↑ \"botox near me\" search interest'),
 card('hallmark movies','med spa near me','c14','Hallmark movies','med spa near me','Hallmark movies search interest by state →','↑ \"med spa near me\" search interest',extra=('NH',))])
json.dump(out,open('scatter.json','w'),separators=(',',':'),ensure_ascii=False)
