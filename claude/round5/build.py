import json,sys,datetime as dt,numpy as np
sys.path.insert(0,'/home/claude/work/charts'); from load import load
def days(a,b):
    d0=dt.date.fromisoformat(a);n=(dt.date.fromisoformat(b)-d0).days+1
    return [(d0+dt.timedelta(i)).isoformat() for i in range(n)]
out={}
# c7 Friday 13 (task 11142135-...f6130b869df7)
x=days('2026-10-16','2026-11-13')
tat=[37,50,39,27,28,28,30,35,48,38,31,31,28,31,32,44,34,25,26,23,30,34,47,41,35,36,42,41,100]
pie=[27,35,33,22,21,22,23,27,32,30,24,21,22,22,23,27,24,20,20,18,23,24,37,34,24,25,26,24,41]
bot=[8,7,5,8,8,7,7,8,7,9,9,8,9,8,8,7,9,8,7,7,8,8,8,7,8,11,9,8,7]
assert len(tat)==len(x)==len(pie)==len(bot)
out['c7']={'x':x,'s':[{'n':'tattoo near me','v':tat},{'n':'piercing near me','v':pie},{'n':'botox near me','v':bot}],'t':'d','mark':[['2026-11-13','Fri 13th']]}
# c8 liquor/dispensary daily (task 11142133-...09dbbe869df6)
x=days('2025-11-15','2026-04-30')
disp=[20,20,14,14,14,16,17,20,20,15,15,21,37,27,21,18,13,12,13,15,15,19,18,13,12,15,14,17,20,19,14,14,14,16,17,22,20,16,19,29,37,26,21,20,18,18,21,23,18,20,17,17,13,14,15,16,18,16,14,13,13,14,16,20,19,16,13,13,14,17,19,17,15,13,13,14,15,19,17,17,12,13,15,15,19,17,12,13,15,14,17,22,20,16,12,14,15,15,20,18,15,16,14,15,17,22,20,14,13,15,15,17,21,22,16,16,14,16,18,22,21,16,14,17,15,19,21,21,15,14,14,18,19,20,22,14,13,16,16,30,22,24,18,14,14,15,18,21,20,15,13,14,18,22,21,21,26,15,52,14,17,19,19,13,13,29,16]
liq=[23,22,9,7,9,9,13,23,25,13,11,24,100,31,21,20,10,8,8,9,11,22,21,11,8,9,9,12,23,22,11,9,10,13,15,24,27,17,21,53,78,23,19,22,15,14,41,48,15,16,16,9,7,8,8,10,16,19,9,7,7,8,11,18,20,14,7,7,7,11,20,25,13,8,7,8,10,18,18,9,7,7,8,11,18,23,8,6,7,8,12,22,22,12,7,8,8,11,18,20,12,8,8,9,12,19,21,9,7,7,9,12,20,22,12,8,8,9,13,23,24,11,9,9,9,13,22,23,10,8,9,9,13,21,24,10,8,8,10,15,23,34,12,8,8,9,13,22,22,11,7,8,9,13,22,23,12,8,8,9,13,22,22,10,8,8,10]
print(len(x),len(disp),len(liq))
assert len(disp)==len(x)==len(liq)
out['c8']={'x':x,'s':[{'n':'liquor store near me','v':liq},{'n':'dispensary near me','v':disp}],'t':'d','mark':[['2025-11-27','Thanksgiving'],['2025-12-25','Christmas'],['2026-04-20','4/20']]}
# c9 dry january weekly from weed.json, own-peak scaled
tid,d,S=load('weed.json'); i0=d.index('2025-09-07'); i1=d.index('2026-03-29')+1
out['c9']={'x':d[i0:i1],'s':[{'n':'liquor store near me','v':[int(round(v)) for v in S['liquor store near me'][i0:i1]]},{'n':'dispensary near me','v':[int(round(v)) for v in S['dispensary near me'][i0:i1]]}],'t':'w','mark':[['2025-12-28','New Year']]}
# c10 munchies (task 11142134-...c0dc8ee00637)
x=days('2026-04-06','2026-05-03')
dd=[20,16,16,16,19,23,22,17,15,15,19,24,23,24,29,16,59,15,18,21,21,14,15,32,17,20,25,23]
pz=[52,53,57,69,74,86,68,45,48,51,48,62,95,88,53,48,44,53,68,84,72,48,47,50,55,77,100,92]
ic=[15,14,15,17,20,29,29,16,18,16,16,19,29,28,16,14,14,16,17,27,30,17,14,13,16,16,28,31]
assert len(x)==len(dd)==len(pz)==len(ic)
out['c10']={'x':x,'s':[{'n':'pizza near me','v':pz},{'n':'dispensary near me','v':dd},{'n':'ice cream near me','v':ic}],'t':'d','mark':[['2026-04-20','4/20']]}
json.dump(out,open('new.json','w'),separators=(',',':'))
# stats
print('liq Thanksgiving/NYE',100/41, 'weekday median', np.median([v for v,dd_ in zip(liq,x) if True][:12]))
f13=[('2024-09-13',100,[31,31]),('2024-12-13',50,[20,24]),('2025-06-13',100,[32,33]),('2026-02-13',100,[42,47]),('2026-03-13',89,[38,37]),('2026-11-13',100,[34,32])]
for d_,v,b in f13: print(d_, round(v/np.mean(b),2))
# dry jan detail
dd_=[dt.date.fromisoformat(z) for z in d]
for y in range(2022,2027):
  jan=[i for i in range(len(d)) if dd_[i].year==y and dd_[i].month==1 and dd_[i].day>=8]
  fall=[i for i in range(len(d)) if dd_[i].year==y-1 and (dd_[i].month==10 or (dd_[i].month==11 and dd_[i].day<=14))]
  if jan and fall: print(y,[round(np.mean(S[k][jan])/np.mean(S[k][fall]),2) for k in ['dispensary near me','liquor store near me']])
