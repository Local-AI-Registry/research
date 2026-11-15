import json,html,numpy as np
D=json.load(open('/home/claude/work/r14/monthly.json'));MON=D['MON'];M=D['M']
BLUE="#1F4FE0";ORANGE="#C2410C";INK="#0B1A2E";CORAL="#FF5A3C";PAPER="#F4F1EA";SLATE="#556070"
LOGO="file:///home/claude/work/canvas/logo.svg";F='/home/claude/research/assets/fonts/'
CSS=f"""@font-face{{font-family:Cormorant;src:url(file://{F}cormorant.woff2);font-weight:300 700}}@font-face{{font-family:'Bricolage Grotesque';src:url(file://{F}bricolage-grotesque.woff2);font-weight:200 800}}@font-face{{font-family:'Hanken Grotesk';src:url(file://{F}hanken-grotesk.woff2);font-weight:100 900}}body{{margin:0}}"""
esc=lambda s:html.escape(s,quote=True)
SRC="Monthly average of weekly Google search interest, U.S., Dec 2021 to Oct 2026. Each line is scaled to its own five-year peak. Correlation, not causation."
P=[
 ("lip filler","pilates","Lip filler","Pilates",["Lip filler girls","do Pilates."],"Plump lips, strong core. Science.",
  "The lip filler girlies are on the reformer. Searches for lip filler and Pilates have moved together for five straight years (0.94 match). Is that a lifestyle or a coincidence? Yes. Correlation, not causation.\n\nTag your Pilates bestie."),
 ("microneedling","monster energy","Microneedling","Monster Energy",["Microneedling girls","run on Monster Energy."],"Tiny needles. Big caffeine.",
  "Turns out the glow comes with a can. Microneedling searches and Monster Energy searches have tracked each other for five years (0.92 match). We are not doctors. Correlation, not causation.\n\nWhat's your go-to energy drink?"),
 ("nail salon near me","boba near me","Nail salon near me","Boba near me",["Nail girls are","boba girls."],"Fresh set, brown sugar boba. Every time.",
  "You know the move. Nails done, boba in hand. “Nail salon near me” and “boba near me” have been nearly the same chart for five years (0.90 match). Correlation, not causation, but come on.\n\nWhat's your boba order?"),
 ("hair salon near me","pizza near me","Hair salon near me","Pizza near me",["Fresh blowout?","Pizza night."],"The hair is done. The diet is not.",
  "A new haircut deserves a slice. “Hair salon near me” and “pizza near me” searches have moved together for five years (0.85 match). Correlation, not causation. Pizza is still the right call.\n\nPizza topping that ends friendships?"),
 ("microneedling","engagement ring","Microneedling","Engagement ring",["She's getting","microneedling.","He's ring shopping."],"Glow up before the proposal.",
  "Somebody's getting ready for photos. Microneedling searches and engagement ring searches have tracked each other for five years (0.83 match). Coincidence? Probably. Cute? Definitely. Correlation, not causation.\n\nTag someone who should be ring shopping."),
 ("brazilian wax","ice cream near me","Brazilian wax","Ice cream near me",["Brazilian wax girls","earn the ice cream."],"Pain first, then a waffle cone.",
  "Brave girls get dessert. “Brazilian wax” and “ice cream near me” rise and fall together year after year (0.81 match). Mostly because of summer. Mostly. Correlation, not causation.\n\nTag your post-wax ice cream buddy."),
 ("breast augmentation","wedding dress","Breast augmentation","Wedding dress",["Boob job,","then the dress."],"Wedding season plans ahead.",
  "The dress has to fit somehow. Breast augmentation searches and wedding dress searches have moved together for five years (0.76 match). We are not saying brides do this. We are saying the chart does. Correlation, not causation."),
 ("brazilian wax","white claw","Brazilian wax","White Claw",["Brazilian wax girls","drink White Claw."],"Smooth, then seltzer.",
  "Summer starter pack, apparently. “Brazilian wax” and White Claw searches have tracked each other for five years (0.76 match). There are no laws when you're drinking Claws. Correlation, not causation.\n\nFavorite White Claw flavor?"),
 ("liposuction","boba near me","Liposuction","Boba near me",["Lipo girls","love boba."],"Let's not overthink this one.",
  "We have questions too. Liposuction searches and “boba near me” searches have moved together for five years (0.75 match). The math says yes. Your nutritionist says no. Correlation, not causation."),
 ("botox near me","astrology","Botox near me","Astrology",["Botox girls","check their horoscope."],"Mercury is in retrograde. So is the forehead.",
  "It's written in the stars. “Botox near me” and astrology searches have tracked each other for five years (0.71 match). Booking Botox around your moon sign? We support it. Correlation, not causation.\n\nDrop your sign."),
 ("tummy tuck","sushi near me","Tummy tuck","Sushi near me",["Tummy tuck people","eat sushi."],"Light lunch. Big plans.",
  "Tummy tuck searches and “sushi near me” searches have moved together for five years (0.70 match). Clean eating before the big day? Or just a spicy tuna roll? Correlation, not causation.\n\nSushi order go."),
 ("eyebrow threading","chick fil a","Eyebrow threading","Chick-fil-A",["Brow girls","love Chick-fil-A."],"Clean arches. Waffle fries.",
  "Threaded brows, then the drive-thru. Eyebrow threading and Chick-fil-A searches have tracked each other for five years (0.69 match). My pleasure. Correlation, not causation.\n\nChick-fil-A sauce or Polynesian?"),
 ("liposuction","bumble","Liposuction","Bumble",["Lipo first.","Then Bumble."],"New profile pic incoming.",
  "Updating the profile, inside and out. Liposuction and Bumble searches have moved together for five years (0.64 match). Swipe right on the glow up. Correlation, not causation.\n\nWorst dating app opener you've gotten?"),
 ("nose job","tarot","Nose job","Tarot",["Nose job girls","read tarot."],"The cards said do it.",
  "The cards have spoken. Nose job searches and tarot searches have tracked each other for five years (0.60 match). Pull the Star card, book the consult. Correlation, not causation.\n\nWhat card would you pull today?"),
]
def r(a,b): return float(np.corrcoef(M[a],M[b])[0,1])
def chart(a,b,la,lb):
    cw,ch=952,560;L,R,T,B=46,186,26,52;n=len(MON)
    X=lambda i:L+i*(cw-L-R)/(n-1); Y=lambda v:T+(100-v)*(ch-T-B)/100
    g=[f'<rect width="{cw}" height="{ch}" rx="16" fill="#fff"/>']
    for v in (0,50,100):
        g.append(f'<line x1="{L}" x2="{cw-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{"rgba(11,26,46,.25)" if v==0 else "rgba(11,26,46,.08)"}" stroke-width="1.5"/>')
        g.append(f'<text x="{L-10}" y="{Y(v)+7:.1f}" text-anchor="end" font-family="Hanken Grotesk" font-size="20" fill="{SLATE}">{v}</text>')
    for i,m in enumerate(MON):
        if m.endswith('-01'): g.append(f'<text x="{X(i):.1f}" y="{ch-16}" text-anchor="middle" font-family="Hanken Grotesk" font-size="21" fill="{SLATE}">{m[:4]}</text>')
    ends=[]
    for k,(key,lab,col) in enumerate(((a,la,BLUE),(b,lb,ORANGE))):
        v=np.array(M[key]);v=v/v.max()*100
        d="M"+" L".join(f"{X(i):.1f},{Y(y):.1f}" for i,y in enumerate(v))
        g.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')
        ends.append([Y(v[-1]),lab,col])
    def split(lab):
        words=lab.split(); return [lab] if len(lab)<=14 else [" ".join(words[:len(words)//2+len(words)%2])," ".join(words[len(words)//2+len(words)%2:])]
    ends.sort()
    need=24*len(split(ends[0][1]))+8
    if ends[1][0]-ends[0][0]<need: ends[1][0]=ends[0][0]+need
    for y,lab,col in ends:
        lines=split(lab)
        for j,t in enumerate(lines):
            g.append(f'<text x="{cw-R+12}" y="{y+7+j*24:.1f}" font-family="Hanken Grotesk" font-weight="600" font-size="22" fill="{col}">{esc(t)}</text>')
    return f'<svg width="{cw}" height="{ch}" viewBox="0 0 {cw} {ch}">{"".join(g)}</svg>'
items=[]
for i,(a,b,la,lb,h,sub,cap) in enumerate(P,1):
    rv=r(a,b)
    size=74 if len(h)<=2 and max(len(x) for x in h)<=22 else 64
    inner=(f'<div style="display:flex;justify-content:space-between;align-items:center"><div style="font:700 22px/1 \'Bricolage Grotesque\';letter-spacing:.14em;text-transform:uppercase;color:{BLUE}">Correlation, Not Causation · No. {i:02d}</div><img src="{LOGO}" style="height:30px"></div>'
      f'<div style="display:flex;flex-direction:column;gap:12px"><h1 style="margin:0;font:600 {size}px/1.04 Cormorant,serif;color:{INK}">'+''.join(f'<span style="display:block;white-space:nowrap">{esc(l)}</span>' for l in h)+f'</h1><p style="margin:0;font:400 28px/1.35 \'Hanken Grotesk\';color:{SLATE}">{esc(sub)}</p></div>'
      f'<div style="flex:1;display:flex;align-items:center">{chart(a,b,la,lb)}</div>'
      f'<div style="display:flex;align-items:center;gap:28px"><div style="font:800 104px/.86 \'Bricolage Grotesque\';letter-spacing:-.03em;color:{CORAL}">{rv:.2f}</div><div style="font:400 23px/1.45 \'Hanken Grotesk\';color:{SLATE}"><span style="display:block;white-space:nowrap"><b style="color:{INK};font-weight:600">Five-year match score.</b> 1.00 means</span><span style="display:block;white-space:nowrap">the two lines move exactly together.</span></div></div>'
      f'<div style="border-top:1px solid rgba(11,26,46,.14);padding-top:20px;font:400 19px/1.5 \'Hanken Grotesk\';color:{SLATE}">{esc(SRC)}</div>')
    open(f"cnc-{i:02d}.html","w").write(f'<html><head><style>{CSS}</style></head><body><div style="width:1080px;height:1350px;box-sizing:border-box;padding:60px 64px;background:{PAPER};display:flex;flex-direction:column;gap:28px;overflow:hidden">{inner}</div></body></html>')
    items.append({"n":i,"file":f"posts/cnc-{i:02d}.png","title":" ".join(h),"cap":cap,"r":round(rv,2)})
json.dump(items,open('items.json','w'),ensure_ascii=False)
print([(x['n'],x['r']) for x in items])
