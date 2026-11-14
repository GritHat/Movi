#!/usr/bin/env python3
"""Confronta le voci di allegato.bib con le risposte grezze di Crossref (per DOI). Solo lettura dei dati scaricati."""
import re, sys, json, pathlib, unicodedata
bib = open(sys.argv[1], encoding="utf-8").read()
def norm(s):
    s = unicodedata.normalize("NFKD", s or ""); s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", re.sub(r"\\[a-zA-Z]+|[{}$'`\"^~\\]", "", s).lower()).strip()
voci = {}
for v in re.split(r"\n(?=@)", bib):
    m = re.match(r"@(\w+)\{([^,]+),", v)
    if not m: continue
    c = {}
    for a, b in re.findall(r"^\s*(\w+)\s*=\s*\{(.*)\},?\s*$", v, flags=re.M): c[a.lower()] = b
    c["_tipo"] = m.group(1); voci[m.group(2)] = c
per_doi = {norm(c.get("doi","")): k for k, c in voci.items() if c.get("doi")}
visti = set()
for d in sys.argv[2:]:
    for f in sorted(pathlib.Path(d).glob("*.json")):
        try: j = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        except Exception: continue
        w = j.get("message") if isinstance(j, dict) else None
        if not isinstance(w, dict) or "DOI" not in w: continue
        k = per_doi.get(norm(w["DOI"]))
        if not k or k in visti: continue
        visti.add(k); c = voci[k]; diff = []
        t = (w.get("title") or [""])[0]
        if norm(t) not in norm(c.get("title","")) and norm(c.get("title","")) not in norm(t): diff.append(f"TITOLO bib=«{c.get('title','')[:70]}» registro=«{t[:70]}»")
        anni = {str(w.get(x,{}).get("date-parts",[[None]])[0][0]) for x in ("published-print","published-online","issued","published") if w.get(x)}
        if c.get("year") not in anni: diff.append(f"ANNO bib={c.get('year')} registro={sorted(anni)}")
        if w.get("volume") and c.get("volume") and w["volume"] != c["volume"]: diff.append(f"VOLUME bib={c['volume']} registro={w['volume']}")
        if w.get("volume") and not c.get("volume") and c["_tipo"]=="article": diff.append(f"VOLUME mancante (registro {w['volume']})")
        pg = (w.get("page") or "").replace("-", "--")
        if pg and c.get("pages") and norm(pg) != norm(c["pages"]): diff.append(f"PAGINE bib={c['pages']} registro={w['page']}")
        if pg and not c.get("pages"): diff.append(f"PAGINE mancanti (registro {w['page']})")
        au = w.get("author") or []
        if au:
            fam = norm(au[0].get("family",""))
            if fam and fam not in norm(c.get("author","")): diff.append(f"PRIMO AUTORE registro={au[0].get('family')} bib=«{c.get('author','')[:50]}»")
            nb = len(re.split(r"\s+and\s+", c.get("author","")))
            if nb != len(au) and "others" not in c.get("author",""): diff.append(f"N. AUTORI bib={nb} registro={len(au)}")
        ct = (w.get("container-title") or [""])[0]
        sede = c.get("journal") or c.get("booktitle") or ""
        if ct and sede and not (set(norm(ct).split()) & set(norm(sede).split()) - {"of","the","on","and","in","for","international","conference","ieee","journal"}): diff.append(f"SEDE bib=«{sede[:60]}» registro=«{ct[:60]}»")
        print(f"{k}\t{'coincide' if not diff else ' | '.join(diff)}")
print("confrontate:", len(visti), file=sys.stderr)
