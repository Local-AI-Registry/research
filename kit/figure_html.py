"""Print the page HTML for every figure (image, caption, data table, embed code) and the ImageObject structured data.

Usage: python kit/figure_html.py <study-folder> "<Study title>"
Writes <study-folder>/images/figures.html (paste each <figure> where it belongs) and images/figures-ld.json
(add these nodes to the page's @graph and list their @ids in the Report's "image")."""
import json, html, os, sys
e = lambda s: html.escape(str(s), quote=True)
SITE = "https://localairegistry.com/research/"

def main(folder, study_title):
    base = SITE + folder.strip("/")
    F = json.load(open(os.path.join(folder, "images", "figs.json")))
    out, ld, n = [], [], {"chart": 0, "illustration": 0}
    for f in F:
        n[f["kind"]] += 1; kind = "Illustration" if f["kind"] == "illustration" else "Figure"; w, h = f["width"], f["height"]
        tbl = ""
        if f.get("table"):
            head, *rows = f["table"]
            tbl = ('<details><summary>Data behind this chart</summary><div class="scroll"><table><thead><tr>' + "".join(f"<th>{e(c)}</th>" for c in head)
                   + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div></details>")
        embed = (f'<a href="{base}#{f["slug"]}"><img src="{base}/images/{f["slug"]}.png" alt="{f["alt"]}" width="800"></a>'
                 f'<p>Source: <a href="{base}">{study_title}</a>, Local AI Registry Research Team.</p>')
        out.append(f'<figure id="{f["slug"]}" class="fig"><img src="images/{f["slug"]}.png" srcset="images/{f["slug"]}-1x.png {w}w, images/{f["slug"]}.png {w*2}w" '
                   f'sizes="(max-width: 900px) calc(100vw - 32px), 860px" width="{w}" height="{h}" alt="{e(f["alt"])}" loading="lazy" decoding="async">'
                   f'<figcaption><b>{kind} {n[f["kind"]]}. {e(f["title"].rstrip("."))}.</b> {e(f["caption"])} <span class="dl"><a href="images/{f["slug"]}.svg">SVG</a> · <a href="images/{f["slug"]}.png">PNG</a></span></figcaption>{tbl}'
                   f'<details class="embed"><summary>Embed this {kind.lower()}</summary><textarea readonly rows="4" aria-label="Embed code for {e(f["title"])}" onclick="this.select()">{e(embed)}</textarea></details></figure>')
        ld.append({"@type": "ImageObject", "@id": f"{base}#{f['slug']}", "contentUrl": f"{base}/images/{f['slug']}.png", "url": f"{base}/images/{f['slug']}.png",
                   "name": f["title"], "caption": f["caption"], "description": f["alt"], "width": w * 2, "height": h * 2,
                   "creator": {"@id": "https://localairegistry.com/research#research-team"}, "copyrightHolder": {"@id": "https://localairegistry.com/#organization"},
                   "creditText": "Local AI Registry", "license": "https://creativecommons.org/licenses/by/4.0/", "acquireLicensePage": base + "#cite"})
    open(os.path.join(folder, "images", "figures.html"), "w").write("\n\n".join(out))
    json.dump(ld, open(os.path.join(folder, "images", "figures-ld.json"), "w"), indent=1, ensure_ascii=False)
    print(len(F), "figures ->", folder + "/images/figures.html and figures-ld.json")

if __name__ == "__main__":
    if len(sys.argv) != 3: raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
