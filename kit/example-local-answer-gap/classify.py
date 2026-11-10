import json, re
EXCL = re.compile(r"stock|market open|markets open|market on|the market|nyse|nasdaq|strait|hormuz|lga|airport|opening day|opening ceremony|shooting|earthquake|fire|tornado|amber|explosion|boom|alert|recall|lawsuit|settlement|stock|chapter 11|artemis|rocket|launch|crossfit|season|college|location tracker|jersey|tattoo|vault|demon|happy meal|all american", re.I)
HOURS = re.compile(r"\b(?:is|are|does|do)\b.*\b(?:open|closed|close)\b|\bhours\b|\bopen (?:on|today|tomorrow|now)\b|\bclosed (?:on|today)\b|\bopen easter\b|\bclosed easter\b", re.I)
NEAR = re.compile(r"near me|nearby", re.I)
CLOSE = re.compile(r"(?:closing|closures?|closes|shutdown|shutting)\b.*\b(?:stores?|locations?|restaurants?|mall|dates)|(?:stores?|locations?|restaurants?) (?:closing|closures?)", re.I)
def lclass(k):
    if not k or EXCL.search(k): return None
    if HOURS.search(k): return "Hours & open status"
    if NEAR.search(k): return "Near me"
    if CLOSE.search(k): return "Closures & openings"
    return None
if __name__ == "__main__":
    recs = json.load(open("aio_records.json"))
    import collections
    by = collections.defaultdict(set)
    for r in recs:
        c = lclass(r["kw"])
        if c: by[c].add(r["kw"].lower())
    for c, s in by.items(): print(f"\n== {c} ({len(s)} unique)\n", sorted(s))
