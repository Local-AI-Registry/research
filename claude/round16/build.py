import json,numpy as np,re
from demo import D
A=json.load(open('aff.json')); R=json.load(open('/home/claude/work/r14/all.json')); MAPS=R['MAPS']
Mo=json.load(open('/home/claude/work/r14/monthly.json'))
DN={"botox near me":"botox","pizza near me":"pizza","ice cream near me":"ice cream","sushi near me":"sushi","nail salon near me":"nail salon","hair salon near me":"hair salon","boba near me":"boba"}
dn=lambda k:DN.get(k,k)
LBL={"botox near me":"Botox","pizza near me":"Pizza","ice cream near me":"Ice cream","sushi near me":"Sushi","nail salon near me":"Nail salon","hair salon near me":"Hair salon","boba near me":"Boba","chick fil a":"Chick-fil-A","monster energy":"Monster Energy","white claw":"White Claw","love island":"Love Island","tesla":"Tesla","pilates":"Pilates","bumble":"Bumble","astrology":"Astrology","tarot":"Tarot","margarita":"Margaritas","engagement ring":"Engagement rings","wedding dress":"Wedding dresses"}
lab=lambda k:LBL.get(k,k[:1].upper()+k[1:])
get=lambda t,c:[o for o in A if o['t']==t and o['c']==c][0]
def age_share(k): a=np.array(D[dn(k)][0],float); return [round(x,3) for x in a/a.sum()]
def fem(k): f,m=D[dn(k)][1]; return round(f/(f+m),2)
def series(k): v=np.array(Mo['M'][k]); return [round(x,1) for x in v/v.max()*100]
def states(t,c): return [[s,MAPS[t][s],MAPS[c][s]] for s in sorted(x for x in MAPS[t] if x in MAPS[c] and x not in('WY','DC'))]
VIRAL=[("lip filler","pilates","Lip filler girls do Pilates"),("microneedling","monster energy","Microneedling girls run on Monster Energy"),("nail salon near me","boba near me","Nail girls are boba girls"),("hair salon near me","pizza near me","Fresh blowout? Pizza night"),("microneedling","engagement ring","She's getting microneedling. He's ring shopping"),("brazilian wax","ice cream near me","Brazilian wax girls earn the ice cream"),("breast augmentation","wedding dress","Boob job, then the dress"),("brazilian wax","white claw","Brazilian wax girls drink White Claw"),("liposuction","boba near me","Lipo girls love boba"),("botox near me","astrology","Botox girls check their horoscope"),("tummy tuck","sushi near me","Tummy tuck people eat sushi"),("eyebrow threading","chick fil a","Brow girls love Chick-fil-A"),("liposuction","bumble","Lipo first. Then Bumble"),("nose job","tarot","Nose job girls read tarot")]
deep=[("nose job","tarot"),("botox near me","wedding dress"),("botox near me","pilates"),("microneedling","pilates"),("botox near me","engagement ring"),("facelift","tesla"),("nose job","sushi near me"),("laser hair removal","love island"),("liposuction","boba near me"),("hair salon near me","pizza near me"),("microneedling","engagement ring")]
out={"months":Mo['MON'],"viral":[],"deep":[]}
for t,c,h in VIRAL:
    o=get(t,c); out["viral"].append(dict(h=h,t=lab(t),c=lab(c),raw=o['raw'],state=o['state'],ov=o['dage'],dfem=o['dfem'],time=o['time'],place=o['place'],people=o['people'],n=o['n']))
for t,c in deep:
    o=get(t,c); out["deep"].append(dict(t=lab(t),c=lab(c),raw=o['raw'],state=o['state'],ov=o['dage'],time=o['time'],place=o['place'],people=o['people'],n=o['n'],st=series(t),sc=series(c),states=states(t,c),at=age_share(t),ac=age_share(c),ft=fem(t),fc=fem(c)))
out["counts"]={n:sum(1 for o in A if o['n']==n) for n in range(4)}; out["total"]=len(A)
print(out['counts'],[(d['t'],d['c'],d['n']) for d in out['deep']], sum(v['n']==3 for v in out['viral']),sum(v['n']==2 for v in out['viral']))
p=open('site/index.html').read()
p=re.sub(r'const DATA=.*?;\nconst BLUE',lambda m:'const DATA='+json.dumps(out)+';\nconst BLUE',p,flags=re.S)
p=p.replace("The pair passes if the average searcher age is within 4 years and the female share is within 10 points.","The pair passes if the age mix of the two searches overlaps by at least 85% and the female share is within 10 points.")
p=p.replace("chip(v.people,`Age ${sgn(v.dage)} yrs, female share ${sgn(Math.round(v.dfem*100))} pts`)","chip(v.people,`Age mix overlap ${Math.round(v.ov*100)}%, female share ${sgn(Math.round(v.dfem*100))} pts`)")
p=p.replace("<p>The two triple matches, plus the strongest pairs that pass two of the three.","<p>The two pairs that pass all three tests, plus the strongest pairs that pass two.")
p=p.replace("const t1=el('text',{x:W/2,y:H-5,'text-anchor':'middle',class:'ax'},s);t1.textContent='first search →'}","const t1=el('text',{x:W/2,y:H-5,'text-anchor':'middle',class:'ax'},s);t1.textContent=xl+' by state →'}")
p=p.replace("function scatter(p,pts){","function scatter(p,pts,xl){")
p=p.replace("scatter(card.querySelector('.p2'),d.states)","scatter(card.querySelector('.p2'),d.states,d.t)")
p=p.replace("<div class=\"panel p2\"><div class=\"pt\"><span>Place</span>","<div class=\"panel p2\"><div class=\"pt\"><span>Place (up = ${d.c})</span>")
p=p.replace("<span>${d.people?'Pass':'No'} · ${Math.round(d.ft*100)}% vs ${Math.round(d.fc*100)}% female</span>","<span>${d.people?'Pass':'No'} · ${Math.round(d.ov*100)}% age overlap</span>")
p=p.replace("if(d.people)parts.push(`the same age and gender searches both`);","if(d.people)parts.push(`the same age and gender mix searches both (${Math.round(d.ft*100)}% vs ${Math.round(d.fc*100)}% female)`);")
p=p.replace("A med spa and a Pilates studio, for example, sell to the same age group, the same gender mix and the same states, so a joint offer reaches people who already want both.","Botox and Pilates are an example: the same states, the same age mix and nearly the same share of women search both, so a med spa and a Pilates studio running a joint offer would be talking to people who already want both.")
p=p.replace("Every one of these passed the time test. That is how they got picked. Most fall apart on place or people.","Every one of these passed the time test. That is how they got picked. Nine fall apart on place and people. One passes all three.")
open('site/index.html','w').write(p)
