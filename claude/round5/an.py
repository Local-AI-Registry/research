import sys,json,numpy as np
sys.path.insert(0,'/home/claude/work/charts'); from load import load
from scipy.stats import pearsonr
for f in ['weed','shave','hang','sun']:
    tid,d,S=load(f+'.json'); print('\n==',f,tid,len(d),d[0],d[-1])
    ks=list(S)
    for k in ks:
        a=S[k]; i=int(a.argmax()); print(f' {k}: peak {d[i]}; top5', [d[j] for j in np.argsort(-a)[:5]])
    for i in range(len(ks)):
        for j in range(i+1,len(ks)):
            r=pearsonr(S[ks[i]],S[ks[j]])[0]; rd=pearsonr(np.diff(S[ks[i]]),np.diff(S[ks[j]]))[0]
            print(f'  r({ks[i]},{ks[j]})={r:.2f} diff={rd:.2f}')
