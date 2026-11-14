#!/usr/bin/env python3
"""Estrae ogni \\cite dai capitoli con la frase che la contiene; confronta con allegato.bib."""
import re, sys, pathlib, json
base = pathlib.Path(sys.argv[1])
bib = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[3])
chiavi_bib = re.findall(r"^@\w+\{([^,\s]+),", bib, flags=re.M)
files = [base/"allegato_tecnico.tex"] + sorted((base/"capitoli").glob("*.tex"))
righe = []; usate = {}
for f in files:
    testo = f.read_text(encoding="utf-8")
    # toglie i commenti
    testo_nc = re.sub(r"(?<!\\)%.*", "", testo)
    for m in re.finditer(r"\\cite[a-zA-Z]*(?:\[[^\]]*\])*\{([^}]*)\}", testo_nc):
        ks = [k.strip() for k in m.group(1).split(",")]
        a = max(testo_nc.rfind(". ", 0, m.start()), testo_nc.rfind("\n\n", 0, m.start()), testo_nc.rfind(".\n", 0, m.start()))
        b = testo_nc.find(".", m.end())
        fr = " ".join(testo_nc[a+1:(b+1 if b>0 else m.end()+200)].split())
        riga = testo_nc.count("\n", 0, m.start()) + 1
        for k in ks:
            usate.setdefault(k, []).append((f.name, riga))
            righe.append((f.name, riga, k, fr))
with open(out/"cite_estratte.tsv", "w", encoding="utf-8") as g:
    for r in righe: g.write("\t".join(map(str, r)) + "\n")
mancanti = sorted(set(usate) - set(chiavi_bib))
mai = sorted(set(chiavi_bib) - set(usate))
with open(out/"conteggi.txt", "w", encoding="utf-8") as g:
    g.write(f"voci nel .bib: {len(chiavi_bib)}\ncomandi cite (occorrenze di chiave): {len(righe)}\nchiavi distinte citate: {len(usate)}\n")
    g.write(f"chiavi citate non nel .bib ({len(mancanti)}): {mancanti}\n")
    g.write(f"voci del .bib mai citate ({len(mai)}): {mai}\n")
    for k in sorted(usate): g.write(f"{k}\t{len(usate[k])}\t{usate[k]}\n")
print(open(out/"conteggi.txt").read())
