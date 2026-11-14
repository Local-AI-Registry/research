import sys,numpy as np,datetime as dt
sys.path.insert(0,'/home/claude/work/charts'); from load import load
from scipy.stats import pearsonr
for f in ['notebook','gilmore','loveisland','bridgerton']:
    tid,d,S=load(f+'.json'); ks=list(S); print('\n==',f,tid)
    for k in ks: a=S[k]; print(f' {k}: peak {d[int(a.argmax())]} top', [d[j] for j in np.argsort(-a)[:4]])
    for i in range(3):
        for j in range(i+1,3):
            a,b=S[ks[i]],S[ks[j]]
            r=pearsonr(a,b)[0]; rd=pearsonr(np.diff(a),np.diff(b))[0]
            lag=[round(pearsonr(np.diff(a)[:-L or None],np.diff(b)[L:])[0],2) for L in range(0,5)]
            print(f'  {ks[i]} ~ {ks[j]}: r={r:.2f} diff={rd:.2f} lag0-4(a leads)={lag}')
