"""Turn a study's figures into files: SVG, sharp PNG (2x), small PNG (1x) and figs.json.

Usage (from the repo root):
    python kit/render.py <study-folder> <your_figures.py>
Example:
    python kit/render.py how-chatgpt-picks-dentists work/how-chatgpt-picks-dentists/figures.py

<your_figures.py> imports `from svgkit import *` and `from figkit import fig`, and calls fig(...) once per chart or illustration.
Needs: pip install playwright pillow   (and `python -m playwright install chromium` if no browser is installed)
"""
import os, sys, json, runpy
KIT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, KIT)
import figkit

def main(folder, script):
    sys.path.insert(0, os.path.dirname(os.path.abspath(script)))
    runpy.run_path(script, run_name="__figures__")
    out = os.path.join(folder, "images"); os.makedirs(out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    from PIL import Image
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(device_scale_factor=2)
        for f in figkit.FIGS:
            open(os.path.join(out, f["slug"] + ".svg"), "w").write(f["svg"])
            pg.set_content(f'<html><body style="margin:0;background:#FBF9F4">{f["svg"]}</body></html>'); pg.wait_for_timeout(150)
            big = os.path.join(out, f["slug"] + ".png"); pg.query_selector("svg").screenshot(path=big)
            im = Image.open(big); f["width"], f["height"] = im.width // 2, im.height // 2
            im.resize((f["width"], f["height"]), Image.LANCZOS).save(os.path.join(out, f["slug"] + "-1x.png"), optimize=True)
            Image.open(big).save(big, optimize=True)
        b.close()
    meta = [{k: v for k, v in f.items() if k != "svg"} for f in figkit.FIGS]
    json.dump(meta, open(os.path.join(folder, "images", "figs.json"), "w"), indent=1, ensure_ascii=False)
    print(len(meta), "figures written to", out)

if __name__ == "__main__":
    if len(sys.argv) != 3: raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
