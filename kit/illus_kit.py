"""Shapes for flat illustrations in the Local AI Registry style (same palette as svgkit).
Use them inside svgkit.frame(...) just like a chart body. See example-local-answer-gap/illus.py."""
import math
from svgkit import t, CARD, LINE, INK, BLUE, TINT

def box(x, y, w, h, fill=CARD, stroke=LINE, r=14, sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def lines(x, y, w, n, gap=16, col=LINE, hl=None):
    """Grey 'text lines' that stand in for writing on a page or screen."""
    o = ""
    for i in range(n):
        ww = w * (0.95 if i % 3 else 0.7)
        o += f'<rect x="{x}" y="{y+i*gap}" width="{ww:.0f}" height="8" rx="4" fill="{(hl if hl and i==0 else col)}"/>'
    return o

def arrow(x1, y1, x2, y2, col=INK, op=.55, w=3):
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
