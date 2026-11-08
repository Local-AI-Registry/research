"""Make every internal link and image path absolute (/research/...).

The site is shown at localairegistry.com/research through the main site's forwarding rule.
Absolute paths keep links working whether or not a URL ends in a slash.
Run after the other build scripts: python scripts/absolute_links.py
"""
import os, re, posixpath

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "/research/"
SKIP = re.compile(r"(https?:|//|/|#|mailto:|tel:|data:|javascript:|\{|\$)")

def fix(u, base):
    if not u or SKIP.match(u): return u
    frag = ""
    if "#" in u: u, frag = u.split("#", 1); frag = "#" + frag
    q = ""
    if "?" in u: u, q = u.split("?", 1); q = "?" + q
    full = posixpath.normpath(posixpath.join(base, u)) if u else base.rstrip("/")
    if u.endswith("/") or u in (".", "./", ""): full = full.rstrip("/") + "/"
    return full + q + frag

def page(path):
    rel = os.path.relpath(os.path.dirname(path), ROOT)
    base = BASE if rel == "." else BASE + rel.replace(os.sep, "/") + "/"
    s = open(path, encoding="utf-8").read()
    s = re.sub(r'\b(href|src|poster)=(["\'])([^"\']*)\2', lambda m: f'{m.group(1)}={m.group(2)}{fix(m.group(3), base)}{m.group(2)}', s)
    s = re.sub(r'\bsrcset=(["\'])([^"\']*)\1', lambda m: "srcset=" + m.group(1) + ", ".join(
        " ".join([fix(p.strip().split(" ")[0], base)] + p.strip().split(" ")[1:]) for p in m.group(2).split(",") if p.strip()) + m.group(1), s)
    open(path, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    for d, _, fs in os.walk(ROOT):
        if ".git" in d or "simulations" in d: continue
        for f in fs:
            if f.endswith(".html"): page(os.path.join(d, f))
    print("links made absolute")
