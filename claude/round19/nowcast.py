import json,numpy as np,datetime as dt
exec(open('fc.py').read().split('res=[]')[0])
d,v=S['sephora'];Q=quarters(d,v)
x=np.array([yoy(Q,k) for k in T]);y=np.array([R[k] for k in T])
b,a=np.polyfit(x,y,1);resid=y-(a+b*x);sd=resid.std(ddof=2)
print('fit a %.3f b %.3f r %.2f sd %.3f'%(a,b,np.corrcoef(x,y)[0,1],sd))
# Q4 partial: same weeks
wk={dd:val for dd,val in zip(d,v)}
cur=[dd for dd in d if '2026-10-04'<=dd<'2026-11-15'];prv=[(dt.date.fromisoformat(dd)-dt.timedelta(days=364)).isoformat() for dd in cur]
print(cur,prv)
g=np.mean([wk[c] for c in cur])/np.mean([wk[p] for p in prv])-1
f=a+b*g;q4=90.3*(1+f)
print('sephora Q4-to-date yoy %.1f%%, forecast evolus yoy %.1f%% -> $%.1fM (range %.1f-%.1f)'%(100*g,100*f,q4,90.3*(1+f-sd),90.3*(1+f+sd)))
print('guidance implied Q4: %.1f-%.1f'%(330-235.24,337-235.24))
# in-sample fitted vs actual table
for k,xx,yy in zip(T,x,y): print(k,round(100*xx,1),round(100*yy,1),round(100*(a+b*xx),1))
# leave-one-out errors
loo=[]
for i in range(len(T)):
  m=np.ones(len(T),bool);m[i]=False;bb,aa=np.polyfit(x[m],y[m],1);loo.append(abs(aa+bb*x[i]-y[i]))
print('LOO MAE %.1f pts'%(100*np.mean(loo)), 'vs avg-growth MAE %.1f'%(100*np.mean(abs(y-y.mean()))))
json.dump(dict(T=T,x=list(map(float,x)),y=list(map(float,y)),fit=[float(a),float(b)],sd=float(sd),g4=float(g),f4=float(f),q4=float(q4),lo=float(90.3*(1+f-sd)),hi=float(90.3*(1+f+sd)),weeks=[cur[0],cur[-1]],loo=float(np.mean(loo)),avgmae=float(np.mean(abs(y-y.mean())))),open('nowcast.json','w'))
