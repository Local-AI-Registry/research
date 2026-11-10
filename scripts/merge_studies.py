"""Bring studies in from the `studies` branch, and nothing else.

Flávia (and her Claude) push freely to the `studies` branch. When the site is published,
this script takes ONLY `studies.json` and study folders from that branch. Everything else
(the hub page, header, footer, map, scripts, settings) always comes from `main`, which only
admins can change. So nothing pushed to `studies` can alter the hub or the site design.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANCH = "origin/studies"
PROTECTED = {".github", "scripts", "simulations", "assets", "og", ".git"}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
OK_EXT = {".html", ".md", ".csv", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".pdf", ".json", ".txt"}

def git(*a):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, check=False)

if git("rev-parse", "--verify", BRANCH).returncode != 0:
    print("No studies branch yet; publishing main as is."); sys.exit(0)

files = git("ls-tree", "-r", "--name-only", BRANCH).stdout.decode().splitlines()
taken, skipped = 0, []
for f in files:
    top = f.split("/")[0]
    ext = os.path.splitext(f)[1].lower()
    allowed = f == "studies.json" or ("/" in f and top not in PROTECTED and SLUG.match(top) and ext in OK_EXT)
    if not allowed:
        continue
    data = git("show", f"{BRANCH}:{f}").stdout
    dest = os.path.join(ROOT, f); os.makedirs(os.path.dirname(dest) or ROOT, exist_ok=True)
    open(dest, "wb").write(data); taken += 1
print(f"Took {taken} study files from the studies branch (hub, design and scripts always come from main).")
