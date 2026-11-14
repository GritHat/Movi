#!/usr/bin/env python3
"""Controlla la parte I del fascicolo: parole vietate, sigle interne, percorsi; ogni \\cite ha la sua voce in allegato.bib
e sta fra le citabili. Uso: controlla_parte1.py <fascicolo.md> <allegato.bib> (esce con 1 se trova errori)"""
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
p1 = t[t.index("<!-- INIZIO PARTE I -->"):t.index("<!-- FINE PARTE I -->")]
bib = set(re.findall(r"^@\w+\{([^,]+),", open(sys.argv[2], encoding="utf-8").read(), flags=re.M))
err = []
for w in ["sciame", "agent", "ruol", "fase", "fasi", "arbitr", "verdett", "addendum", "torneo", "corsi", "coordinator",
          "in corso", "in correzione", "da fare", "preliminar", "piano", "versione", "versioni"]:
    for m in re.finditer(r"\b" + w, p1, flags=re.I):
        err.append("parola vietata «%s»: …%s…" % (w, p1[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")))
senza_cite = re.sub(r"\\cite\{[^}]+\}", " ", p1)   # le chiavi sono quelle dell'elenco: non sono sigle
for m in re.finditer(r"\b(?:[HKFVC]-\d+|[MScf]\d{1,2}\b|\.md\b|/home/|\d{1,2}:\d{2}\b)", senza_cite):
    err.append("sigla, percorso o orario: " + m.group(0))
cit = [k.strip() for g in re.findall(r"\\cite\{([^}]+)\}", p1) for k in g.split(",")]
err += ["citazione senza voce: " + k for k in sorted(set(cit)) if k not in bib]
parole = len(re.sub(r"\\cite\{[^}]+\}|\$[^$]*\$", " ", p1).split())
print("parte I: %d parole circa (quattro pagine sono circa 2000-2200); %d citazioni, %d chiavi distinte su %d voci del bib" % (parole, len(cit), len(set(cit)), len(bib)))
print("voci del bib non citate nella parte I:", len(bib - set(cit)))
print("errori:", len(err)); [print("  -", e) for e in err]
sys.exit(1 if err else 0)
