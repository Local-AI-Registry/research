import datetime as dt, statistics as st
from scipy import stats
start=dt.date(2026,9,1)
CO=[42,53,62,55,56,67,50,40,100,50,64,64,48,38,44,41,57,71,60,38,None,41,60,55,62,65,60,46,47,42,45,55,59,73,43,45,51,45,49,67,60,50,44,39,48,60,63,63,38,42,50,51,44,63,43,43,36,49,53,50,57,50,42,41,34,46,50,58,49,40,39,49,43]
MI=[35,49,56,56,61,56,61,32,100,42,49,47,42,42,38,43,45,67,45,68,55,39,32,39,57,52,41,45,35,36,36,57,52,73,41,34,37,43,52,55,42,49,35,41,39,50,50,43,34,28,34,38,45,49,48,38,29,38,36,46,57,42,39,33,30,37,45,49,40,37,32,35,33]
IL=[59,61,65,74,100,90,86,57,87,59,77,79,70,65,61,64,61,83,97,79,60,65,70,69,76,92,81,55,48,59,73,76,88,77,57,58,60,65,78,90,72,67,58,62,66,74,83,73,52,54,61,62,81,84,77,54,57,64,64,81,74,71,59,52,52,66,75,84,72,60,56,62,67]
MA=[73,69,65,83,95,95,78,55,100,64,75,78,88,65,61,68,53,70,69,99,85,65,65,70,77,71,63,54,57,57,58,69,80,77,55,53,52,75,72,81,73,62,61,62,65,69,75,59,52,49,63,64,68,80,70,53,47,66,61,69,75,68,51,53,52,61,74,74,67,58,53,66,57]
series=dict(CO=CO,MI=MI,IL=IL,MA=MA)
for k,v in series.items(): assert len(v)==73,(k,len(v))
def d(m,dd): return dt.date(2026,m,dd)
# (state, game date, won)
games=[
("CO",d(9,14),0),("CO",d(9,20),1),("CO",d(9,27),1),("CO",d(10,4),0),("CO",d(10,11),1),("CO",d(10,15),1),("CO",d(10,25),1),("CO",d(11,1),1),("CO",d(11,8),1),
("MI",d(9,13),1),("MI",d(9,17),0),("MI",d(9,27),1),("MI",d(10,4),0),("MI",d(10,11),1),("MI",d(10,25),1),("MI",d(11,1),1),("MI",d(11,8),1),
("IL",d(9,13),1),("IL",d(9,20),0),("IL",d(9,28),1),("IL",d(10,4),1),("IL",d(10,11),0),("IL",d(10,18),1),("IL",d(10,22),1),("IL",d(11,2),1),("IL",d(11,8),1),
("MA",d(9,9),0),("MA",d(9,20),1),("MA",d(9,27),0),("MA",d(10,4),1),("MA",d(10,11),1),("MA",d(10,18),1),("MA",d(10,22),0),("MA",d(11,1),1),("MA",d(11,8),0),
]
def val(s,date):
  i=(date-start).days
  return series[s][i] if 0<=i<73 else None
def wd_mean(s,date):
  vals=[val(s,start+dt.timedelta(i)) for i in range(73) if (start+dt.timedelta(i)).weekday()==date.weekday() and start+dt.timedelta(i)!=d(9,9)]
  vals=[x for x in vals if x is not None]; return st.mean(vals)
W=[];L=[]
for s,g,won in games:
  nd=g+dt.timedelta(1)
  v=val(s,nd)
  if v is None: continue
  r=v/wd_mean(s,nd)
  (W if won else L).append(r)
print("wins",len(W),round(st.mean(W),3),"losses",len(L),round(st.mean(L),3))
print(stats.mannwhitneyu(L,W,alternative='two-sided'))
print(stats.ttest_ind(L,W,equal_var=False))
