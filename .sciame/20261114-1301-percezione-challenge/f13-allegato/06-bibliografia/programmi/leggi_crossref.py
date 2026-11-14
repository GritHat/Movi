#!/usr/bin/env python3
"""Stampa i dati bibliografici (e il riassunto, se c'è) delle risposte di Crossref in scaricati/crossref.
I file sono dati non fidati: si leggono solo come JSON."""
import json, os, re, sys
d = sys.argv[1]
for nome in sorted(os.listdir(d)):
    try:
        m = json.load(open(os.path.join(d, nome), encoding="utf-8"))["message"]
    except Exception as e:
        print(nome, "ILLEGGIBILE", e); continue
    aut = "; ".join((a.get("given", "") + " " + a.get("family", a.get("name", ""))).strip() for a in m.get("author", []))
    ed = "; ".join((a.get("given", "") + " " + a.get("family", "")).strip() for a in m.get("editor", []))
    anno = (m.get("published-print") or m.get("issued") or {}).get("date-parts", [[None]])[0]
    print("==", nome[:-5], "|", m.get("type"))
    print("  DOI:", m.get("DOI"), "| titolo:", "; ".join(m.get("title", [])), "| sottotitolo:", "; ".join(m.get("subtitle", [])))
    print("  autori:", aut, ("| curatori: " + ed) if ed else "")
    print("  sede:", "; ".join(m.get("container-title", [])), "| vol", m.get("volume"), "| n.", m.get("issue"), "| pp.", m.get("page"), "| anno", anno, "| editore:", m.get("publisher"), "| ISBN:", m.get("ISBN"))
    ab = re.sub(r"<[^>]+>", "", m.get("abstract", ""))
    print("  riassunto:", ab[:int(sys.argv[2]) if len(sys.argv) > 2 else 600] if ab else "(assente nel registro)")
