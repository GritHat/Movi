#!/usr/bin/env python3
"""Legge documentazione/RIFERIMENTI.md e ne estrae le voci (chiave, numero, gruppo, campi).
Uso: leggi_elenco.py <RIFERIMENTI.md> <uscita.json>"""
import json, re, sys

def stato_breve(verifica):
    v = verifica.lower()
    regole = [("dato diverso", "dato diverso"),
              ("in parte", "in parte"),
              ("pagina aperta e dato presente", "verificata"),
              ("aperta dal ruolo", "aperta dal ruolo"),
              ("solo nel riassunto", "solo riassunto"),
              ("non verificata", "non verificata"),
              ("non raggiungibile", "non raggiungibile")]
    testa = v.split("—")[0]
    for chiave, nome in regole:
        if chiave in testa:
            return nome
    return "?" + testa[:40]

def leggi(percorso):
    voci, gruppo, cor = [], None, None
    for riga in open(percorso, encoding="utf-8"):
        riga = riga.rstrip("\n")
        m = re.match(r"^## (\d)\. ", riga)
        if m:
            gruppo = int(m.group(1)); cor = None; continue
        m = re.match(r"^### (\S+) \[(\d+)\]\s*$", riga)
        if m and gruppo and 1 <= gruppo <= 6:
            cor = {"chiave": m.group(1), "numero": int(m.group(2)), "gruppo": gruppo, "usi": [], "campi": {}}
            voci.append(cor); continue
        if cor is None:
            continue
        m = re.match(r"^([A-Z][^:]{2,30}): (.*)$", riga)
        if m:
            nome, val = m.group(1), m.group(2)
            if nome == "Usata per":
                cor["usi"].append(val)
            else:
                cor["campi"][nome] = val
    for v in voci:
        v["stato"] = stato_breve(v["campi"].get("Verifica", ""))
    return voci

if __name__ == "__main__":
    voci = leggi(sys.argv[1])
    json.dump(voci, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(voci), "voci")
    print(Counter(v["stato"] for v in voci))
    print(Counter(v["gruppo"] for v in voci))
