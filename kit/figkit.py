"""Collects a study's figures. Call fig(...) once per chart or illustration; render.py does the rest."""
FIGS = []
def fig(slug, title, alt, caption, svg, table=None, section="", kind="chart"):
    """slug: file name and anchor, written as the question people search (e.g. "dentists-chatgpt-recommends-by-city-heatmap").
    title: the finding as a full sentence with the number in it. alt: what the image shows, with the key numbers.
    caption: one or two sentences, the finding plus the comparison. svg: svgkit.frame(...). table: rows (first row = headers) for
    the "Data behind this chart" table and the CSV, or None for illustrations. kind: "chart" or "illustration"."""
    if any(f["slug"] == slug for f in FIGS): raise SystemExit("duplicate figure slug: " + slug)
    FIGS.append(dict(slug=slug, title=title, alt=alt, caption=caption, svg=svg, table=table, section=section, kind=kind))
