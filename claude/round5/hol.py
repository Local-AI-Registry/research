import sys,numpy as np,datetime as dt
sys.path.insert(0,'/home/claude/work/charts'); from load import load
tid,d,S=load('weed.json'); D=[dt.date.fromisoformat(x) for x in d]
hol={'420':lambda y:dt.date(y,4,20),'Jul4':lambda y:dt.date(y,7,4),'Xmas':lambda y:dt.date(y,12,25),'NYE':lambda y:dt.date(y,12,31),
 'Thanks':lambda y:[dt.date(y,11,1)+dt.timedelta(days=i) for i in range(30) if (dt.date(y,11,1)+dt.timedelta(days=i)).weekday()==3][3]}
def wk(day):
    for i,s in enumerate(D):
        if s<=day<=s+dt.timedelta(6): return i
for h,f in hol.items():
    out=[]
    for y in range(2022,2027):
        i=wk(f(y))
        if i is None or i<5 or i>len(D)-1: continue
        base=[j for j in range(i-6,i+7) if abs(j-i)>=2 and 0<=j<len(D)]
        r={k:S[k][i]/np.median(S[k][base]) for k in ['dispensary near me','liquor store near me']}
        out.append((y,round(r['dispensary near me'],2),round(r['liquor store near me'],2)))
    print(h,out)
# rank of 4/20 week within its year for dispensary
a=S['dispensary near me']
for y in range(2022,2027):
    idx=[i for i in range(len(D)) if D[i].year==y]
    i=wk(dt.date(y,4,20)); rk=sorted(idx,key=lambda j:-a[j]).index(i)+1
    print('420 rank',y,rk,'of',len(idx))
# Jan vs Dec (excluding holiday weeks): dispensary/liquor
for y in range(2022,2027):
    jan=[i for i in range(len(D)) if D[i].year==y and D[i].month==1 and D[i].day>=8]
    nov=[i for i in range(len(D)) if D[i].year==y-1 and D[i].month in(10,11) and D[i].day<=14]
    if jan and nov: print('Jan/Oct-Nov',y,[round(np.mean(S[k][jan])/np.mean(S[k][nov]),2) for k in ['dispensary near me','liquor store near me']])
