from svgkit import *
from figures import fig

def box(x, y, w, h, fill=CARD, stroke=LINE, r=14, sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def lines(x, y, w, n, gap=16, col=LINE, hl=None):
    o = ""
    for i in range(n):
        ww = w * (0.95 if i % 3 else 0.7)
        o += f'<rect x="{x}" y="{y+i*gap}" width="{ww:.0f}" height="8" rx="4" fill="{(hl if hl and i==0 else col)}"/>'
    return o
def arrow(x1, y1, x2, y2, col=INK, op=.55, w=3):
    import math
    a = math.atan2(y2 - y1, x2 - x1); L = 14
    p1 = (x2 - L * math.cos(a - .45), y2 - L * math.sin(a - .45)); p2 = (x2 - L * math.cos(a + .45), y2 - L * math.sin(a + .45))
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}"/>'
            f'<polygon points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{col}" fill-opacity="{op}"/>')
def chip(x, y, s, fill=TINT, col=BLUE, w=None):
    w = w or (len(s) * 10 + 34)
    return f'<rect x="{x}" y="{y}" width="{w}" height="38" rx="19" fill="{fill}"/>' + t(x + w / 2, y + 25, s, 17, "middle", 700, fill=col)
def phone(x, y, w=230, h=400):
    return box(x, y, w, h, CARD, INK, 30, 3) + f'<rect x="{x+w/2-30}" y="{y+14}" width="60" height="8" rx="4" fill="{LINE}"/>'
SRC = "Illustration: Local AI Registry"

# I1 SEO vs AEO
b = phone(110, 0) + t(225, 60, "SEO", 26, "middle", 800, BLUE, "h")
for i in range(5):
    y = 90 + i * 58; b += f'<rect x="135" y="{y}" width="140" height="10" rx="5" fill="{BLUE}" fill-opacity=".8"/>' + lines(135, y + 20, 180, 2, 12)
b += t(225, 440, "A list of links. You click.", 20, "middle", 700)
b += phone(660, 0) + t(775, 60, "AEO", 26, "middle", 800, BLUE, "h")
b += box(682, 84, 186, 190, TINT, BLUE, 12) + t(698, 112, "AI answer", 16, weight=800, fill=BLUE, cls="h") + lines(698, 128, 160, 7, 17, "#9DB4FF")
b += chip(690, 290, "Sources: 3", DEEP, INK, 120) + lines(690, 344, 160, 3, 14)
b += t(775, 440, "One answer. Most never click.", 20, "middle", 700)
b += arrow(380, 200, 610, 200, BLUE, .8, 4) + t(495, 186, "search is moving", 18, "middle", fill=MUTED)
fig("seo-vs-aeo-explained-illustration", "SEO gets you into the list. AEO gets you into the answer.",
    "Illustration comparing a search results page of blue links (SEO) with an AI answer box that cites a few sources (AEO)",
    "Search engine optimization (SEO) earns a place in a list of links. Answer engine optimization (AEO) earns a place inside the AI-written answer that appears before any links.",
    frame(1000, 470, "SEO gets you into the list. AEO gets you into the answer.", "SEO vs AEO", b, "Explainer", SRC), None, "intro", "illustration")

# I2 how an AI local answer is assembled
b = box(30, 150, 210, 110, TINT, BLUE) + t(135, 195, "“Is Target open", 19, "middle", 700) + t(135, 222, "on Easter?”", 19, "middle", 700)
b += arrow(245, 205, 330, 205, INK)
b += f'<circle cx="420" cy="205" r="80" fill="{BLUE}"/>' + t(420, 200, "Google’s", 20, "middle", 800, "#fff", "h") + t(420, 226, "AI", 22, "middle", 800, "#fff", "h")
srcs = [("News outlets", "67%", BLUE), ("Social posts", "10%", MUTED), ("Portals", "8%", MUTED), ("Store’s own site", "6.5%", CORAL)]
for i, (s, p, c) in enumerate(srcs):
    y = 20 + i * 100
    b += box(560, y, 210, 76, CARD, c, 12, 3) + t(665, y + 32, s, 18, "middle", 700) + t(665, y + 58, p + " of citations", 16, "middle", fill=MUTED)
    b += arrow(560, y + 38, 505, 205 + (i - 1.5) * 18, c, .7)
b += arrow(500, 205, 520, 205, INK, 0)
b += box(800, 120, 180, 170, CARD, INK, 12, 3) + t(890, 150, "The answer", 17, "middle", 800, cls="h") + lines(818, 166, 145, 4, 18)
b += f'<rect x="812" y="246" width="156" height="32" rx="6" fill="{CORAL}" fill-opacity=".15"/>' + t(890, 268, "“Check your store”", 15, "middle", 700, CORAL)
b += arrow(770, 205, 798, 205, INK)
fig("how-google-ai-builds-a-local-answer-illustration", "How Google’s AI builds an answer about a local business",
    "Diagram: a local question goes to Google’s AI, which pulls mostly from news outlets, then social posts, portals and rarely the store’s own site, and returns an answer that tells you to check your store",
    "For local questions, Google’s AI assembled answers mostly from news coverage (67.5% of citations), rarely from the business itself (6.5%), and usually ended by telling people to check with their local store.",
    frame(1000, 420, "How Google’s AI builds an answer about a local business", "Answer assembly", b, "Explainer", SRC), None, "f2", "illustration")

# I3 ranked vs used
b = box(40, 10, 400, 380, CARD, INK, 16, 3) + t(240, 50, "Google page one", 20, "middle", 800, cls="h")
for i in range(5):
    y = 80 + i * 60; c = CORAL if i == 0 else BLUE
    b += f'<rect x="70" y="{y+6}" width="{220 if i else 250}" height="12" rx="6" fill="{c}"/>' + lines(70, y + 22, 300, 1)
b += t(70, 74, "The store’s own site, ranked first", 16, weight=700, fill=CORAL)
b += box(560, 70, 400, 260, TINT, BLUE, 16, 3) + t(760, 110, "AI answer", 20, "middle", 800, BLUE, "h") + lines(590, 130, 330, 5, 18, "#9DB4FF")
for i, s in enumerate(["usatoday.com", "today.com", "facebook.com"]):
    b += chip(590 + i * 120, 240, s, CARD, INK, 112)
b += arrow(445, 120, 552, 160, CORAL, .8) + t(498, 205, "skipped", 18, "middle", 800, CORAL)
b += f'<line x1="483" y1="125" x2="513" y2="155" stroke="{CORAL}" stroke-width="5"/><line x1="513" y1="125" x2="483" y2="155" stroke="{CORAL}" stroke-width="5"/>'
fig("ranked-vs-used-by-ai-illustration", "Ranked first, still skipped: why SEO alone isn’t AEO",
    "Illustration of a store website ranking at the top of Google page one while the AI answer next to it cites news sites instead",
    "In 147 of 157 brand questions the store’s own site ranked on page one, but the AI cited it in only 70. Ranking and being used by AI are separate outcomes.",
    frame(1000, 400, "Ranked first, still skipped: why SEO alone isn’t AEO", "Ranked vs used", b, "Explainer", SRC), None, "f3", "illustration")

# I4 what AI can read
cards = [("News article", "~500 readable words", BLUE, 12), ("Store locator page", "~100 words, mostly scripts", CORAL, 3), ("Social post", "~8 readable words", CORAL, 1)]
b = ""
for i, (s, n, c, k) in enumerate(cards):
    x = 40 + i * 320
    b += box(x, 10, 280, 330, CARD, c, 16, 3) + t(x + 140, 50, s, 21, "middle", 800, cls="h")
    if i == 1:
        for j in range(6): b += t(x + 30, 100 + j * 30, "</>  {…}  script", 17, fill=MUTED)
    elif i == 2:
        b += f'<rect x="{x+30}" y="80" width="220" height="150" rx="10" fill="{DEEP}"/>' + t(x + 140, 165, "photo", 18, "middle", fill=MUTED) + lines(x + 30, 250, 120, 1)
    else:
        b += lines(x + 30, 80, 220, 12, 17, "#9DB4FF")
    b += t(x + 140, 315, n, 18, "middle", 700, c)
b += t(500, 395, "AI quotes text. If the facts aren’t in readable text, it guesses or borrows them.", 20, "middle", 700)
fig("what-ai-can-read-on-a-web-page-illustration", "What Google’s AI can actually read on a page",
    "Illustration of three page types: a news article full of readable text, a store locator page made mostly of scripts, and a social post with a photo and a few words",
    "News pages the AI cited had about 500 readable words. Store locator pages were mostly scripts, and the median cited social post had 8 readable words.",
    frame(1000, 410, "What Google’s AI can actually read on a page", "Readability", b, "Explainer", SRC), None, "f5", "illustration")

# I5 single source of truth (LAIR)
b = box(370, 140, 260, 130, BLUE, BLUE, 16) + t(500, 185, "Owner-confirmed", 21, "middle", 800, "#fff", "h") + t(500, 213, "record", 21, "middle", 800, "#fff", "h") + t(500, 245, "Local AI Registry", 16, "middle", 700, "#fff")
outs = [("Your website", 60, 20), ("Google Business Profile", 60, 330), ("Directories", 740, 20), ("Press and news", 740, 330)]
for s, x, y in outs:
    b += box(x, y, 200, 70, CARD, INK, 12, 2) + t(x + 100, y + 42, s, 17, "middle", 700)
    b += arrow(500 + (-130 if x < 500 else 130), 205 + (-50 if y < 200 else 50), x + (200 if x < 500 else 0), y + 35, BLUE, .7)
b += f'<circle cx="500" cy="380" r="0"/>'
b += box(395, 330, 210, 70, TINT, BLUE, 12, 3) + t(500, 362, "AI answers", 19, "middle", 800, BLUE, "h") + t(500, 386, "match everywhere", 15, "middle", fill=BLUE)
b += arrow(500, 272, 500, 326, BLUE, .9, 4)
fig("single-source-of-truth-for-ai-local-aeo-illustration", "One confirmed record, pushed everywhere AI looks",
    "Diagram of an owner-confirmed Local AI Registry record feeding the business website, Google Business Profile, directories and press, so AI answers match",
    "Because AI rotates between sources, a business’s facts need to match on its website, Google Business Profile, directories and press. Local AI Registry starts from one owner-confirmed record.",
    frame(1000, 410, "One confirmed record, pushed everywhere AI looks", "Single source of truth", b, "Explainer", SRC), None, "f6", "illustration")

# I6 sources rotate
qs = ["“Is Target open on Easter?”", "“Target Easter hours”", "“Target closed on Easter”"]
pools = [["kare11.com", "13newsnow.com", "mercurynews.com"], ["today.com", "facebook.com", "reolink.com"], ["msn.com", "usatoday.com", "the-sun.com"]]
b = ""
for i, q in enumerate(qs):
    y = 10 + i * 120
    b += box(30, y, 300, 70, TINT, BLUE, 12) + t(180, y + 43, q, 18, "middle", 700)
    b += arrow(335, y + 35, 400, y + 35, INK)
    for j, s in enumerate(pools[i]): b += chip(410 + j * 140, y + 16, s, CARD, INK, 132)
    b += arrow(830, y + 35, 870, 185, INK, .35)
b += box(870, 140, 110, 90, BLUE, BLUE, 12) + t(925, 180, "Closed", 20, "middle", 800, "#fff", "h") + t(925, 205, "same verdict", 13, "middle", fill="#fff")
fig("ai-sources-rotate-same-verdict-illustration", "Different wording, different sources, same answer",
    "Illustration of three phrasings of the same Target question, each citing a different mix of websites, all producing the same closed verdict",
    "Three ways of asking about Target on Easter returned the same verdict but shared only about a third of their sources. No single publisher owns a local answer.",
    frame(1000, 370, "Different wording, different sources, same answer", "Rotation", b, "Explainer", SRC + ". Sources shown are real citations from these answers."), None, "f6", "illustration")
