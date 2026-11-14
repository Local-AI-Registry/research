from scipy import stats
picks = {
 "Miami":["LUX MedSpa Brickell","Charette Cosmetics Medical Spa","4Ever Young Med Spa Midtown","No Filter Medical Spa","Azala Skin Clinic","KC Medical Aesthetics","MDW Aesthetics Miami","Monaco MedSpa","Zia Medical Aesthetics","Miami Surgical MedSpa"],
 "Los Angeles":["SkinSpirit at Lasky","Cienega Medical","Skin by Lovely","Your Laser Skin Care","Double J Medical Aesthetics and Hair Clinic"],
 "New York":["Dr. Lanna Aesthetics","SkinSpirit New York - UES","JECT","Tribeca Medspa","BeRejuved Medical Spa & Wellness Studio - NYC"],
 "Chicago":["SpaDerma","Dvida Med Spa","New Image Works","Lapiel Laser Center"],
 "Houston":["PurA Medical Aesthetics","Dream Aesthetics Medspa","Rose Milk Aesthetics","Glow Medical Aesthetics","Juvan MD"],
 "Dallas":["Omni Sculpt MD","Sanjiva Medical Spa","SkinSpirit Preston Royal","Mara's Med Spa","ZO Skin Centre"],
 "Atlanta":["MetroDerm & Center for Plastic Surgery","4Ever Young Med Spa & Wellness Center - Atlanta Midtown","Radiance Medspa Atlanta","ELLEMES Medical Spa"],
 "Denver":["The Luxe Room - South Denver","Denver Botox: GATTONI Medical Aesthetics","Rejuvenate MedSpa","PREVA Aesthetics","Gleam Medical Spa"],
 "Seattle":["Blue Haven Medical Spa","Lux Aesthetics","Skin Synthesis Clinic & Spa","Seattle Beauty","Glow Medispa"],
}
def b(n):
  c=n[0].upper()
  if 'A'<=c<='C': return 'A-C'
  if 'D'<=c<='L': return 'D-L'
  if 'M'<=c<='R': return 'M-R'
  if 'S'<=c<='Z': return 'S-Z'
  return 'other'
names=[n for v in picks.values() for n in v]
print("AI picks:",len(names))
base={'A-C':11140,'D-L':15415,'M-R':11472,'S-Z':12312}; tot=50711; base['other']=tot-sum(base.values())
cnt={k:0 for k in base}
for n in names: cnt[b(n)]+=1
for k in base: print(k, cnt[k], f"{cnt[k]/len(names):.1%}", "baseline", f"{base[k]/tot:.1%}")
obs=[cnt[k] for k in base]; exp=[base[k]/tot*len(names) for k in base]
print(stats.chisquare(obs,exp))
# A-C specifically
print("A-C binomial", stats.binomtest(cnt['A-C'],len(names),base['A-C']/tot))
print("S-Z binomial", stats.binomtest(cnt['S-Z'],len(names),base['S-Z']/tot))
lux=[n for n in names if 'lux' in n.lower()]; skin=[n for n in names if n.lower().startswith('skin')]
print("lux",len(lux),lux); print("skin*",len(skin),skin)
