"""Small static-SVG chart kit in the Local AI Registry brand. Every chart is plain SVG text: crawlable, no JavaScript."""
import math, html
BLUE = "#1F4FE0"; INK = "#0B1A2E"; PAPER = "#F4F1EA"; DEEP = "#ECE6D6"; CORAL = "#FF5A3C"; CARD = "#FBF9F4"
MUTED = "#4A5A72"; LINE = "#D8D2C3"; GREEN = "#1F8A4C"; TINT = "#E7EDFC"
FOOT = "Local AI Registry · research.localairegistry.com"

def esc(s): return html.escape(str(s), quote=True)

def wrap(text, maxch):
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > maxch and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    # avoid a single orphan word on the last line
    if len(lines) > 1 and len(lines[-1].split()) == 1:
        prev = lines[-2].split(); lines[-1] = prev[-1] + " " + lines[-1]; lines[-2] = " ".join(prev[:-1])
    return lines

def t(x, y, s, size=20, anchor="start", weight=400, fill=INK, cls="", italic=False, extra=""):
    fam = {"h": "'Bricolage Grotesque',Arial,sans-serif", "d": "Cormorant,Georgia,serif"}.get(cls, "'Hanken Grotesk',Arial,sans-serif")
    st = ' font-style="italic"' if italic else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{st} {extra}>{esc(s)}</text>'

def tlines(x, y, lines, size=20, lh=1.25, **kw):
    return "".join(t(x, y + i * size * lh, l, size, **kw) for i, l in enumerate(lines))

def frame(W, H, title, desc, body, kicker="", source="Data: Local AI Registry analysis of the IMC 2026 Google AI Overviews dataset (CC BY 4.0)"):
    tl = wrap(title, int((W - 80) / 15.5))
    top = 40 + (26 if kicker else 0)
    head = (t(40, 46, kicker.upper(), 15, weight=800, fill=BLUE, cls="h", extra='letter-spacing="1.6"') if kicker else "")
    head += tlines(40, top + 24, tl, 30, 1.18, weight=700, cls="h")
    off = top + 24 + (len(tl) - 1) * 35 + 26
    Ht = H + off + 70
    foot = t(40, Ht - 40, source, 15, fill=MUTED) + t(W - 40, Ht - 16, FOOT, 15, anchor="end", weight=700, fill=BLUE)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Ht}" width="{W}" height="{Ht}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
            f'<rect width="{W}" height="{Ht}" fill="{CARD}"/>{head}<g transform="translate(0,{off})">{body}</g>'
            f'<line x1="40" x2="{W-40}" y1="{Ht-66}" y2="{Ht-66}" stroke="{LINE}"/>{foot}</svg>')

def blue_a(v, vmax):  # opacity for sequential blue
    return max(0.07, math.sqrt(min(v, vmax) / vmax)) if v is not None else 0

def hbars(rows, vmax, W=1000, lw=330, rh=46, fmt=lambda v: f"{v:.1f}%", note_w=170):
    """rows: (label, value, highlight[bool|'coral'|'muted'], right_note)"""
    out = []; bw = W - 40 - lw - note_w
    for i, (lab, v, hl, note) in enumerate(rows):
        y = i * rh
        for j, ln in enumerate(wrap(lab, int(lw / 10.5))[:2]):
            out.append(t(lw - 14, y + rh / 2 + 7 - (8 if len(wrap(lab, int(lw / 10.5))) > 1 else 0) + j * 19, ln, 18, "end", 700 if hl is True else 400))
        out.append(f'<rect x="{lw}" y="{y+10}" width="{bw}" height="{rh-20}" fill="{DEEP}" rx="2"/>')
        col = CORAL if hl == "coral" else (MUTED if hl == "muted" else BLUE)
        op = 1 if hl in (True, "coral") else (0.45 if hl == "muted" else 0.75)
        out.append(f'<rect x="{lw}" y="{y+10}" width="{max(bw*v/vmax,2):.1f}" height="{rh-20}" fill="{col}" fill-opacity="{op}" rx="2"/>')
        out.append(t(lw + bw + 12, y + rh / 2 + 7, (fmt(v) + ("  " + note if note else "")), 18, weight=700))
    return "".join(out), len(rows) * rh

def heat(rows, cols, M, fmt, vmax, lw=260, cw=150, ch=52, colfn=None, W=None, colhdr_lines=2):
    out = []; top = 30 * colhdr_lines + 10
    for j, c in enumerate(cols):
        for k, ln in enumerate(wrap(c, int(cw / 10))[:colhdr_lines]):
            out.append(t(lw + j * cw + cw / 2, 22 + k * 22, ln, 17, "middle", 700, cls="h"))
    for i, r in enumerate(rows):
        y = top + i * ch
        out.append(t(lw - 14, y + ch / 2 + 7, r, 18, "end"))
        for j in range(len(cols)):
            v = M[i][j]; x = lw + j * cw
            if v is None:
                out.append(f'<rect x="{x+3}" y="{y+3}" width="{cw-6}" height="{ch-6}" fill="none" stroke="{LINE}" stroke-dasharray="4 4" rx="3"/>')
                out.append(t(x + cw / 2, y + ch / 2 + 6, "n/a", 16, "middle", fill=MUTED)); continue
            fill, a = (colfn(v) if colfn else (BLUE, blue_a(v, vmax)))
            out.append(f'<rect x="{x+3}" y="{y+3}" width="{cw-6}" height="{ch-6}" fill="{DEEP}" rx="3"/>')
            out.append(f'<rect x="{x+3}" y="{y+3}" width="{cw-6}" height="{ch-6}" fill="{fill}" fill-opacity="{a:.2f}" rx="3"/>')
            out.append(t(x + cw / 2, y + ch / 2 + 7, fmt(v), 19, "middle", 700, fill="#FFFFFF" if a > 0.55 else INK))
    return "".join(out), top + len(rows) * ch

def scatter(points, xr, yr, xlabel, ylabel, quads, W=1000, H=600, xlog=False, ylog=False, xticks=None, yticks=None, xfmt=str, yfmt=str, xdiv=None, ydiv=None):
    """points: dict(label,x,y,r,color,pos)"""
    m = dict(l=90, r=40, t=20, b=70); out = []
    def sx(v):
        a, b = (math.log10(xr[0]), math.log10(xr[1])) if xlog else xr; v = math.log10(v) if xlog else v
        return m["l"] + (W - m["l"] - m["r"]) * (v - a) / (b - a)
    def sy(v):
        a, b = (math.log10(yr[0]), math.log10(yr[1])) if ylog else yr; v = math.log10(v) if ylog else v
        return H - m["b"] - (H - m["t"] - m["b"]) * (v - a) / (b - a)
    for v in (xticks or []):
        out.append(f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{m["t"]}" y2="{H-m["b"]}" stroke="{LINE}"/>')
        out.append(t(sx(v), H - m["b"] + 28, xfmt(v), 17, "middle", fill=MUTED))
    for v in (yticks or []):
        out.append(f'<line x1="{m["l"]}" x2="{W-m["r"]}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" stroke="{LINE}"/>')
        out.append(t(m["l"] - 12, sy(v) + 6, yfmt(v), 17, "end", fill=MUTED))
    if xdiv is not None: out.append(f'<line x1="{sx(xdiv):.1f}" x2="{sx(xdiv):.1f}" y1="{m["t"]}" y2="{H-m["b"]}" stroke="{INK}" stroke-opacity=".45" stroke-dasharray="6 6" stroke-width="2"/>')
    if ydiv is not None: out.append(f'<line x1="{m["l"]}" x2="{W-m["r"]}" y1="{sy(ydiv):.1f}" y2="{sy(ydiv):.1f}" stroke="{INK}" stroke-opacity=".45" stroke-dasharray="6 6" stroke-width="2"/>')
    pos = {"tl": (m["l"] + 14, m["t"] + 30, "start"), "tr": (W - m["r"] - 14, m["t"] + 30, "end"),
           "bl": (m["l"] + 14, H - m["b"] - 16, "start"), "br": (W - m["r"] - 14, H - m["b"] - 16, "end")}
    for k, s in quads.items():
        x, y, a = pos[k]; out.append(t(x, y, s, 19, a, 800, fill=BLUE, cls="h"))
    out.append(t((W + m["l"]) / 2, H - 14, xlabel + " →", 18, "middle", fill=MUTED))
    out.append(t(24, (H - m["b"] + m["t"]) / 2, ylabel + " →", 18, "middle", fill=MUTED, extra=f'transform="rotate(-90 24 {(H-m["b"]+m["t"])/2:.0f})"'))
    for p in points:
        cx, cy, r = sx(p["x"]), sy(p["y"]), p.get("r", 9)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{p.get("color", BLUE)}" fill-opacity=".85" stroke="{CARD}" stroke-width="2"/>')
        ps = p.get("pos", "r"); lab = p["label"]
        if ps == "r": out.append(t(cx + r + 8, cy + 6, lab, 17, "start", 700))
        elif ps == "l": out.append(t(cx - r - 8, cy + 6, lab, 17, "end", 700))
        elif ps == "a": out.append(t(cx, cy - r - 8, lab, 17, "middle", 700))
        else: out.append(t(cx, cy + r + 22, lab, 17, "middle", 700))
    return "".join(out), H

def dumbbell(rows, vmax, alab, blab, W=1000, lw=230, rh=48, fmt=lambda v: f"{v:.0f}%"):
    out = []; x0 = lw; x1 = W - 60; X = lambda v: x0 + (x1 - x0) * v / vmax
    out.append(f'<circle cx="{x0+10}" cy="12" r="8" fill="{CARD}" stroke="{INK}" stroke-width="3"/>' + t(x0 + 26, 18, alab, 17, fill=MUTED))
    out.append(f'<circle cx="{x0+330}" cy="12" r="8" fill="{BLUE}"/>' + t(x0 + 346, 18, blab, 17, fill=MUTED))
    top = 44
    for v in range(0, int(vmax) + 1, 25):
        out.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{top}" y2="{top+len(rows)*rh}" stroke="{LINE}"/>' + t(X(v), top + len(rows) * rh + 24, fmt(v), 16, "middle", fill=MUTED))
    for i, (lab, a, b) in enumerate(rows):
        y = top + i * rh + rh / 2
        out.append(t(lw - 16, y + 6, lab, 18, "end"))
        out.append(f'<line x1="{X(a):.1f}" x2="{X(b):.1f}" y1="{y}" y2="{y}" stroke="{MUTED}" stroke-width="3"/>')
        out.append(f'<circle cx="{X(a):.1f}" cy="{y}" r="9" fill="{CARD}" stroke="{INK}" stroke-width="3"/><circle cx="{X(b):.1f}" cy="{y}" r="9" fill="{CORAL if b < a/2 else BLUE}"/>')
    return "".join(out), top + len(rows) * rh + 34

def waffle(n, k, cols=23, size=30, gap=6, on=BLUE, off=DEEP, lab_on="", lab_off="", x0=40):
    out = []; rows = math.ceil(n / cols)
    for i in range(n):
        r, c = divmod(i, cols)
        out.append(f'<rect x="{x0 + c*(size+gap)}" y="{r*(size+gap)}" width="{size}" height="{size}" rx="4" fill="{on if i < k else off}"/>')
    y = rows * (size + gap) + 20
    out.append(f'<rect x="{x0}" y="{y}" width="20" height="20" rx="3" fill="{on}"/>' + t(x0 + 30, y + 16, lab_on, 18, weight=700))
    out.append(f'<rect x="{x0+460}" y="{y}" width="20" height="20" rx="3" fill="{off}"/>' + t(x0 + 490, y + 16, lab_off, 18))
    return "".join(out), y + 30

def vbars(series, labels, vmax, W=1000, H=380, colors=(BLUE, MUTED), names=("", ""), fmt=lambda v: f"{v:.0f}%", every=1):
    m = dict(l=70, r=20, t=40, b=60); out = []; n = len(labels); gw = (W - m["l"] - m["r"]) / n; k = len(series)
    bw = gw * 0.8 / k
    for v in [vmax * f for f in (0, .25, .5, .75, 1)]:
        y = H - m["b"] - (H - m["t"] - m["b"]) * v / vmax
        out.append(f'<line x1="{m["l"]}" x2="{W-m["r"]}" y1="{y:.1f}" y2="{y:.1f}" stroke="{LINE}"/>' + t(m["l"] - 10, y + 6, fmt(v), 16, "end", fill=MUTED))
    for i, lab in enumerate(labels):
        for s in range(k):
            v = series[s][i]; h = (H - m["t"] - m["b"]) * v / vmax
            x = m["l"] + i * gw + gw * 0.1 + s * bw
            out.append(f'<rect x="{x:.1f}" y="{H-m["b"]-h:.1f}" width="{bw-2:.1f}" height="{h:.1f}" fill="{colors[s]}" fill-opacity="{1 if s==0 else .5}" rx="2"/>')
        if i % every == 0: out.append(t(m["l"] + i * gw + gw / 2, H - m["b"] + 26, lab, 16, "middle", fill=MUTED))
    if names[0]:
        for s in range(k):
            out.append(f'<rect x="{m["l"] + s*260}" y="4" width="20" height="20" rx="3" fill="{colors[s]}" fill-opacity="{1 if s==0 else .5}"/>' + t(m["l"] + s * 260 + 30, 20, names[s], 17))
    return "".join(out), H
