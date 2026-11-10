"""Add each study's YouTube explainer to its study page.

For every study in studies.json that has a "video" block, this script:
  1. puts a click-to-play video (fast: only a thumbnail loads until someone presses play) under the study's short answer,
  2. adds the transcript under the video (AI tools read text, not video),
  3. adds VideoObject structured data and links it to the report,
  4. adds the video to sitemap.xml.
Run: python scripts/video.py   (the GitHub Action runs it automatically)
"""
import json, os, re, html, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = lambda s: html.escape(str(s), quote=True)

def yt_id(u):
    m = re.search(r"(?:youtu\.be/|v=|/shorts/|/embed/|/live/)([A-Za-z0-9_-]{11})", u or "")
    if not m: raise SystemExit(f'video.youtube "{u}" is not a YouTube link')
    return m.group(1)

def iso(d):
    m = re.match(r"^(\d+):([0-5]\d)$", d or "")
    if not m: raise SystemExit(f'video.length "{d}" must look like 1:04')
    mi, se = int(m.group(1)), int(m.group(2))
    return f"PT{mi}M{se}S" if mi else f"PT{se}S"

CSS = """<style>
.vid{margin:28px 0 8px;max-width:760px}.vid-k{font:800 12px var(--f-head,system-ui);letter-spacing:.08em;text-transform:uppercase;color:var(--blue,#1f4fd8);margin:0 0 10px}
.vid-box{position:relative;aspect-ratio:16/9;border-radius:14px;overflow:hidden;background:#111;box-shadow:0 10px 30px rgba(20,24,40,.18)}
.vid-box iframe,.vid-play{position:absolute;inset:0;width:100%;height:100%;border:0}
.vid-play{padding:0;cursor:pointer;background:#111;display:block}.vid-play img{width:100%;height:100%;object-fit:cover;display:block}
.vid-btn{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:76px;height:76px;border-radius:50%;background:var(--blue,#1f4fd8);display:grid;place-items:center;box-shadow:0 6px 24px rgba(0,0,0,.35);transition:transform .15s}
.vid-play:hover .vid-btn,.vid-play:focus-visible .vid-btn{transform:translate(-50%,-50%) scale(1.08)}
.vid-len{position:absolute;right:12px;bottom:12px;background:rgba(0,0,0,.75);color:#fff;font:700 13px system-ui;padding:3px 8px;border-radius:6px}
.vid-cap{font-size:15px;color:var(--muted,#555);margin:10px 0 0}.vid-cap a{font-weight:600}
.vid details{margin-top:10px}.vid summary{cursor:pointer;font-weight:700;color:var(--blue,#1f4fd8)}.vid details p{margin:10px 0 0;line-height:1.6}
</style>"""

JS = """<script>document.querySelectorAll('.vid-play').forEach(function(b){b.addEventListener('click',function(){var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.id+'?autoplay=1&rel=0&modestbranding=1';f.title=b.dataset.title;f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.allowFullscreen=true;b.replaceWith(f);});});</script>"""

def block(v, vid, study):
    title = v.get("title") or study["title"]
    watch = f"https://www.youtube.com/watch?v={vid}"
    thumb = v.get("thumbnail") or f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    tr = v.get("transcript", "").strip()
    paras = "".join(f"<p>{e(p.strip())}</p>" for p in re.split(r"\n\s*\n", tr) if p.strip())
    return (f'<!--video-->{CSS}<section class="vid" id="video" aria-labelledby="vid-h">'
            f'<h2 class="vid-k" id="vid-h">Watch: this study in {e(v["length"])}</h2>'
            f'<div class="vid-box"><button type="button" class="vid-play" data-id="{vid}" data-title="{e(title)}" aria-label="Play video: {e(title)} ({e(v["length"])})">'
            f'<img src="{e(thumb)}" alt="" width="480" height="360" loading="lazy" decoding="async">'
            f'<span class="vid-btn" aria-hidden="true"><svg width="30" height="30" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="#fff"/></svg></span>'
            f'<span class="vid-len">{e(v["length"])}</span></button>'
            f'<noscript><a href="{watch}">Watch on YouTube</a></noscript></div>'
            f'<p class="vid-cap">{e(v.get("description") or "A one-minute, plain-language walkthrough of the findings.")} '
            f'<a href="{watch}" rel="noopener">Watch on&nbsp;YouTube</a></p>'
            + (f'<details><summary>Read the transcript</summary>{paras}</details>' if paras else "")
            + f'</section>{JS}<!--/video-->')

def apply():
    data = json.load(open(os.path.join(ROOT, "studies.json")))
    sm_path = os.path.join(ROOT, "sitemap.xml"); sm = open(sm_path).read()
    for st in data["studies"]:
        page = os.path.join(ROOT, st["url"].strip("/"), "index.html")
        if not os.path.exists(page): continue
        s = open(page).read()
        s = re.sub(r"<!--video-->.*?<!--/video-->", "", s, flags=re.S)
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', s).group(1)
        m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
        ld = json.loads(m.group(2)); g = ld["@graph"]
        g[:] = [n for n in g if n.get("@id") != canon + "#video"]
        for n in g:
            if n.get("@id") == canon + "#report": n.pop("video", None)
        v = st.get("video")
        sm = re.sub(r"(<loc>" + re.escape(canon) + r"</loc>(?:(?!</url>).)*?)\s*<video:video>.*?</video:video>", r"\1", sm, flags=re.S)
        if v:
            for k in ("youtube", "length", "uploaded"):
                if not v.get(k): raise SystemExit(f'{st["id"]}: video is missing "{k}"')
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", v["uploaded"]): raise SystemExit(f'{st["id"]}: video.uploaded must look like 2026-11-12')
            vid = yt_id(v["youtube"]); title = v.get("title") or st["title"]
            desc = v.get("description") or st["summary"]
            thumb = v.get("thumbnail") or f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
            node = {"@type": "VideoObject", "@id": canon + "#video", "name": title, "description": desc,
                    "thumbnailUrl": [thumb], "uploadDate": v["uploaded"], "duration": iso(v["length"]),
                    "contentUrl": f"https://www.youtube.com/watch?v={vid}", "embedUrl": f"https://www.youtube.com/embed/{vid}",
                    "url": canon + "#video", "inLanguage": "en-US", "isFamilyFriendly": True,
                    "publisher": {"@id": "https://localairegistry.com/#organization"},
                    "creator": {"@id": "https://localairegistry.com/research#research-team"},
                    "about": {"@id": canon + "#report"}}
            if v.get("transcript"): node["transcript"] = v["transcript"].strip()
            g.append(node)
            for n in g:
                if n.get("@id") == canon + "#report": n["video"] = {"@id": canon + "#video"}
            # place the video under the short answer + stats, at the end of the article header
            i = s.find('id="summary"'); j = s.find("</header>", i)
            s = s[:j] + block(v, vid, st) + s[j:]
            vx = (f"\n    <video:video><video:thumbnail_loc>{e(thumb)}</video:thumbnail_loc><video:title>{e(title)}</video:title>"
                  f"<video:description>{e(desc)}</video:description><video:player_loc>https://www.youtube.com/embed/{vid}</video:player_loc>"
                  f"<video:duration>{int(v['length'].split(':')[0])*60+int(v['length'].split(':')[1])}</video:duration>"
                  f"<video:publication_date>{v['uploaded']}</video:publication_date></video:video>")
            sm = re.sub(r"(<loc>" + re.escape(canon) + r"</loc>)", r"\1" + vx.replace("\\", "\\\\"), sm, count=1)
            print("video added:", st["id"])
        m2 = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
        s = s[:m2.start(2)] + json.dumps(ld, indent=1, ensure_ascii=False) + s[m2.end(2):]
        open(page, "w").write(s)
    if "xmlns:video=" not in sm:
        sm = sm.replace('<urlset ', '<urlset xmlns:video="http://www.google.com/schemas/sitemap-video/1.1" ', 1)
    open(sm_path, "w").write(sm)

if __name__ == "__main__":
    apply()
