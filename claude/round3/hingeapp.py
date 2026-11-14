from states import botox, lip, hinge
from scipy import stats
happ=dict(WY=100,DC=42,UT=30,CA=30,WA=29,CO=28,NV=28,RI=28,KS=28,NJ=28,MA=28,OR=27,MD=27,NY=26,CT=26,DE=25,AZ=25,LA=24,NH=24,GA=24,HI=24,FL=24,VA=24,IL=24,AK=24,PA=23,MN=22,MI=22,ID=21,AL=21,TN=21,NC=20,SC=20,OH=20,OK=19,IA=19,TX=19,WI=19,ND=19,IN=19,MT=19,ME=18,NM=17,KY=17,MS=17,WV=17,MO=16,AR=16,NE=15,VT=14,SD=11)
st=[s for s in happ if s!='WY']
for name,d in (('botox',botox),('lip',lip),('hinge(raw)',hinge)):
  x=[happ[s] for s in st]; y=[d[s] for s in st]
  print(name, stats.pearsonr(x,y), stats.spearmanr(x,y))
st2=[s for s in st if s!='DC']
x=[happ[s] for s in st2]; y=[botox[s] for s in st2]; print('noDC botox',stats.pearsonr(x,y))
