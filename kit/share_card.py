"""Make a study's link-preview image (1200x630), the picture people see when the link is shared.

Usage (from the repo root):
  python kit/share_card.py <study-folder> "<Short title>" "<One-line subtitle>" "<Big number 1>" "<what it means>" "<Big number 2>" "<what it means>"
Example:
  python kit/share_card.py local-answer-gap "The Local Answer Gap" "What 7,583 Google AI answers reveal about AEO for local businesses." \
      "67.5%" "of citations in local AI answers came from news sites" "6.5%" "came from the businesses' own websites"
Writes <study-folder>/images/share.png. Use it for og:image and twitter:image:
  https://localairegistry.com/research/<study-folder>/images/share.png
"""
import os, sys, html, tempfile
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = lambda s: html.escape(s)

def nbsp_last(s):  # keep the last two words together (no lonely last word)
    w = e(s).rsplit(" ", 1); return "&nbsp;".join(w) if len(w) == 2 else w[0]

def main(folder, title, sub, n1, t1, n2, t2):
    F = "file://" + os.path.join(ROOT, "assets", "fonts")
    logo = "file://" + os.path.join(ROOT, "kit", "local-ai-registry-logo.svg")
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:H;src:url({F}/hanken-grotesk.woff2);font-weight:400 700}}
@font-face{{font-family:B;src:url({F}/bricolage-grotesque.woff2);font-weight:600 800}}
@font-face{{font-family:C;src:url({F}/cormorant.woff2);font-weight:500 600}}
*{{box-sizing:border-box;margin:0}}body{{width:1200px;height:630px;overflow:hidden;background:#F4F1EA;color:#0B1A2E;font-family:H}}
.wrap{{position:absolute;inset:0;display:grid;grid-template-columns:660px 1fr}}
.l{{padding:64px 0 56px 72px;display:flex;flex-direction:column}}
.brand{{display:flex;align-items:center;gap:14px}}.brand img{{width:230px}}.tag{{font:800 15px B;letter-spacing:.12em;color:#1F4FE0;border-left:2px solid #D8D2C3;padding-left:14px}}
h1{{font:600 72px/1.02 C;margin-top:auto;text-wrap:balance}}p{{font-size:23px;line-height:1.35;color:#4A5568;margin-top:22px}}
.foot{{margin-top:28px;font:700 17px B;color:#1F4FE0;letter-spacing:.02em}}
.r{{background:#0B1A2E;color:#fff;padding:70px 56px;display:flex;flex-direction:column;justify-content:center;gap:34px}}
.n{{font:800 92px/1 B;letter-spacing:-.02em}}.n.b{{color:#7FA0FF}}.n.c{{color:#FF7A61}}.t{{font-size:22px;line-height:1.3;color:#C9D3E3;margin-top:8px}}
</style></head><body><div class="wrap"><div class="l"><div class="brand"><img src="{logo}"><span class="tag">RESEARCH</span></div>
<h1>{nbsp_last(title)}</h1><p>{nbsp_last(sub)}</p><div class="foot">localairegistry.com/research</div></div>
<div class="r"><div><div class="n b">{e(n1)}</div><div class="t">{nbsp_last(t1)}</div></div><div><div class="n c">{e(n2)}</div><div class="t">{nbsp_last(t2)}</div></div></div></div></body></html>"""
    tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False); tmp.write(page); tmp.close()
    out = os.path.join(ROOT, folder, "images", "share.png"); os.makedirs(os.path.dirname(out), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
        pg.goto("file://" + tmp.name); pg.wait_for_timeout(500); pg.screenshot(path=out); b.close()
    Image.open(out).convert("RGB").quantize(256).save(out, optimize=True)
    print("share image:", out)

if __name__ == "__main__":
    if len(sys.argv) != 8: raise SystemExit(__doc__)
    main(*sys.argv[1:])
