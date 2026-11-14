#!/usr/bin/env python3
"""Controllo di forma di allegato.bib: campi per voce, anno, autori, DOI/URL, incoerenze."""
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
voci = re.split(r"\n(?=@)", t)
for v in voci:
    m = re.match(r"@(\w+)\{([^,]+),", v)
    if not m: continue
    tipo, k = m.groups()
    c = dict((a.lower(), b.strip()) for a, b in re.findall(r"^\s*(\w+)\s*=\s*[{\"](.*?)[}\"],?\s*$", v, flags=re.M|re.S))
    prob = []
    if "year" not in c: prob.append("SENZA year")
    if "author" not in c and "editor" not in c: prob.append("SENZA author")
    if tipo == "article" and "journal" not in c: prob.append("SENZA journal")
    if tipo == "article" and "pages" not in c and "eprint" not in c and "doi" not in c: prob.append("SENZA pages/doi")
    if tipo == "inproceedings" and "booktitle" not in c: prob.append("SENZA booktitle")
    if tipo == "inproceedings" and "pages" not in c: prob.append("senza pages")
    if tipo == "article" and "volume" not in c: prob.append("senza volume")
    idf = c.get("doi") or c.get("eprint") or c.get("url") or c.get("isbn") or ""
    print(f"{k}\t{tipo}\t{c.get('year','-')}\t{idf[:90]}\t{'; '.join(prob)}\t{sorted(c)}")
