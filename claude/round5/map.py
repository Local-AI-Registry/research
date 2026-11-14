import json,numpy as np
from scipy.stats import pearsonr,spearmanr
import sys
sys.path.insert(0,'/home/claude/work/charts'); from load import load
# maps pasted from tool output (solo-scaled)
disp={"NV":100,"NM":89,"MO":85,"MA":84,"VT":73,"AZ":73,"OH":72,"CO":71,"ME":69,"MT":67,"MD":64,"RI":63,"NJ":60,"IL":53,"DE":51,"NH":49,"CT":48,"MI":44,"DC":40,"MN":39,"FL":36,"NY":35,"WV":35,"OK":34,"AR":33,"PA":32,"ND":31,"CA":27,"AK":25,"OR":24,"SD":23,"WY":21,"IN":20,"KS":19,"MS":19,"WA":16,"KY":16,"WI":16,"HI":16,"IA":15,"LA":14,"VA":13,"UT":12,"NE":12,"TN":10,"ID":9,"NC":9,"TX":7,"SC":6,"GA":5,"AL":5}
liq={"DE":100,"MD":61,"DC":58,"GA":55,"TN":52,"NJ":51,"IN":45,"OK":43,"KY":43,"MS":42,"AR":41,"MN":39,"CO":36,"OR":35,"UT":35,"SC":34,"FL":33,"ND":30,"AL":29,"NY":29,"OH":29,"KS":29,"IL":28,"ID":28,"RI":27,"MI":26,"CT":25,"AK":25,"PA":24,"WY":23,"TX":22,"MT":22,"WV":21,"NH":21,"VT":19,"MA":18,"SD":15,"MO":14,"NV":14,"WI":14,"NM":11,"CA":11,"NC":11,"LA":11,"AZ":10,"VA":10,"IA":9,"NE":9,"ME":8,"HI":7,"WA":6}
botox={"WY":100,"FL":40,"NJ":36,"CO":35,"KS":32,"NH":31,"UT":31,"AZ":31,"DC":31,"ID":30,"MA":29,"RI":29,"NY":29,"CA":29,"CT":28,"MS":28,"VA":28,"SC":28,"MI":28,"OH":27,"GA":26,"WV":26,"TN":26,"PA":26,"OR":25,"NC":25,"DE":25,"WA":25,"TX":25,"NM":24,"MD":24,"VT":24,"KY":24,"IL":24,"NV":24,"MN":24,"AL":24,"ND":24,"LA":23,"WI":22,"MO":22,"IN":21,"ME":21,"IA":21,"NE":20,"AR":19,"OK":19,"SD":19,"AK":18,"HI":17,"MT":16}
oz={"WV":100,"WY":99,"KY":85,"MS":77,"LA":77,"OR":76,"CA":75,"AR":73,"KS":72,"TN":72,"CT":71,"AL":71,"WA":70,"PA":70,"OK":69,"FL":69,"NY":68,"HI":68,"AZ":68,"SC":67,"IN":67,"TX":67,"MD":66,"AK":66,"NV":66,"IL":65,"NC":65,"GA":65,"VA":65,"IA":65,"NJ":65,"OH":65,"MI":64,"CO":64,"MO":63,"NM":63,"ID":63,"ND":63,"VT":63,"WI":61,"NH":61,"MN":61,"UT":61,"RI":60,"SD":59,"NE":59,"MT":58,"ME":58,"MA":57,"DE":57,"DC":56}
lip={"WY":100,"AZ":72,"CA":68,"FL":62,"NV":60,"TX":58,"NM":57,"TN":55,"AR":55,"OK":54,"CO":54,"KY":53,"WV":53,"UT":53,"ND":53,"MT":51,"LA":51,"WA":50,"OR":50,"MS":50,"RI":50,"ID":49,"NJ":48,"IL":48,"NY":48,"HI":46,"KS":45,"MA":45,"CT":44,"VA":43,"NE":43,"NH":43,"PA":43,"SC":42,"AK":42,"AL":42,"MI":42,"DC":42,"GA":41,"IA":40,"SD":40,"OH":40,"DE":40,"MO":39,"ME":39,"NC":39,"MN":37,"WI":37,"MD":35,"IN":34,"VT":31}
M={'disp':disp,'liq':liq,'botox':botox,'oz':oz,'lip':lip}
json.dump(M,open('maps.json','w'))
st=[s for s in disp if s not in('WY','DC')]
for a,b in [('disp','botox'),('liq','botox'),('disp','lip'),('liq','lip'),('oz','liq'),('oz','disp'),('oz','lip'),('oz','botox')]:
    x=[M[a][s] for s in st];y=[M[b][s] for s in st]
    print(a,b,'pearson %.2f p=%.3f spearman %.2f'%(pearsonr(x,y)+(spearmanr(x,y)[0],)))
tid,d,S=load('marg.json'); print(tid)
ks=list(S)
for i in range(3):
  for j in range(i+1,3):
    print(ks[i],ks[j],'%.2f'%pearsonr(S[ks[i]],S[ks[j]])[0],'diff %.2f'%pearsonr(np.diff(S[ks[i]]),np.diff(S[ks[j]]))[0])
for k in ks: print(k,'peak',d[int(S[k].argmax())])
