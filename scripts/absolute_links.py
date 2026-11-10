"""Make every internal link absolute (/research/...) and drop trailing slashes.

The site is shown at localairegistry.com/research by the main site (Next.js), which
redirects any URL ending in a slash to the same URL without it. So every link,
canonical, sitemap entry and structured-data address here is written without the
trailing slash, to match the address people and crawlers actually end up on.
Run after the other build scripts: python scripts/absolute_links.py
"""
import os, re, posixpath

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "/research/"
FULL = re.compile(r"(https://localairegistry\.com/research(?:/[A-Za-z0-9._-]+)*)/(?=[\"'#?<\s,)\]])")
LOCAL = re.compile(r"(?<=[\"' ,])(/research(?:/[A-Za-z0-9._-]+)*)/(?=[\"'#?\s,])")

def no_slash(s):
    return LOCAL.sub(r"\1", FULL.sub(r"\1", s))

SKIP = re.compile(r"(https?:|//|/|#|mailto:|tel:|data:|javascript:|\{|\$)")

def fix(u, base):
    if not u or SKIP.match(u): return u
    frag = ""
    if "#" in u: u, frag = u.split("#", 1); frag = "#" + frag
    q = ""
    if "?" in u: u, q = u.split("?", 1); q = "?" + q
    full = posixpath.normpath(posixpath.join(base, u)) if u else base.rstrip("/")
    return full.rstrip("/") + q + frag

def page(path):
    rel = os.path.relpath(os.path.dirname(path), ROOT)
    base = BASE if rel == "." else BASE + rel.replace(os.sep, "/") + "/"
    s = open(path, encoding="utf-8").read()
    for q in ('"', "'"):
        s = re.sub(r'(?<![\w-])(href|src|poster)=' + q + '([^' + q + '<>]*)' + q, lambda m: f'{m.group(1)}={q}{fix(m.group(2), base)}{q}', s)
        s = re.sub(r'(?<![\w-])srcset=' + q + '([^' + q + '<>]*)' + q, lambda m: "srcset=" + q + ", ".join(
            " ".join([fix(p.strip().split(" ")[0], base)] + p.strip().split(" ")[1:]) for p in m.group(1).split(",") if p.strip()) + q, s)
    open(path, "w", encoding="utf-8").write(no_slash(s))

def text_file(path):
    s = open(path, encoding="utf-8").read()
    open(path, "w", encoding="utf-8").write(no_slash(s))

if __name__ == "__main__":
    for d, _, fs in os.walk(ROOT):
        if ".git" in d or "simulations" in d: continue
        for f in fs:
            if f.endswith(".html"): page(os.path.join(d, f))
            elif f.endswith((".xml", ".txt", ".md", ".webmanifest")): text_file(os.path.join(d, f))
    print("links made absolute")
