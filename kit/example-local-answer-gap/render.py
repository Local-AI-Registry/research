import os, sys, json, asyncio
sys.argv=[sys.argv[0]]
import figures, illus
from figures import FIGS
OUT=sys.path[0]+"/../site/local-answer-gap/images"
os.makedirs(OUT,exist_ok=True)
for f in FIGS: open(f"{OUT}/{f['slug']}.svg","w").write(f["svg"])
json.dump([{k:v for k,v in f.items() if k!="svg"} for f in FIGS],open("figs_meta.json","w"),indent=1)
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(device_scale_factor=2)
        for f in FIGS:
            await pg.set_content(f'<html><body style="margin:0;background:#FBF9F4">{f["svg"]}</body></html>')
            await pg.wait_for_timeout(120)
            el=await pg.query_selector("svg"); await el.screenshot(path=f"{OUT}/{f['slug']}.png")
        await b.close()
asyncio.run(main())
print(len(FIGS),"figures")
