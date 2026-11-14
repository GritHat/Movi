#!/usr/bin/env python3
"""Costruisce allegato.bib: le voci citabili prese dal file d'origine (senza il campo «note», che là porta lo stato
interno di verifica), più le voci scritte a mano in voci_aggiunte.bib (che prevalgono su quelle d'origine).
Uso: costruisci_bib.py <riferimenti.bib> <citabili.txt> <voci_aggiunte.bib> <allegato.bib>"""
import re, sys

def voci(testo):
    """Restituisce [(tipo, chiave, corpo_intero)] leggendo le graffe carattere per carattere."""
    out, i = [], 0
    while True:
        m = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,").search(testo, i)
        if not m: break
        j, prof = m.end(), 1
        while prof and j < len(testo):
            prof += {"{": 1, "}": -1}.get(testo[j], 0); j += 1
        out.append((m.group(1).lower(), m.group(2), testo[m.start():j])); i = j
    return out

def campi(corpo):
    """Divide il corpo di una voce nei suoi campi 'nome = valore' (valori fra graffe o nudi)."""
    interno = corpo[corpo.index(",") + 1: corpo.rindex("}")]
    res, i = [], 0
    while True:
        m = re.compile(r"\s*([A-Za-z]+)\s*=\s*").match(interno, i)
        if not m: break
        j = m.end()
        if interno[j] == "{":
            prof, k = 1, j + 1
            while prof:
                prof += {"{": 1, "}": -1}.get(interno[k], 0); k += 1
            val = interno[j:k]
        else:
            k = j
            while k < len(interno) and interno[k] not in ",\n": k += 1
            val = interno[j:k].strip()
        res.append((m.group(1).lower(), val)); i = k
        m2 = re.compile(r"\s*,").match(interno, i)
        if m2: i = m2.end()
    return res

CORREZIONI = {  # chiave -> {campo: valore nuovo oppure None per toglierlo}
    "koschi2021": {"url": None},
    "weng2020": {"eprint": None, "archiveprefix": None, "url": None},
    "us-49cfr-236-205": {"author": "{{United States, Federal Railroad Administration}}",
                         "title": "{{49 CFR \\S\\,236.205 -- Signal control circuits; requirements}}",
                         "howpublished": "{Code of Federal Regulations, titolo 49, parte 236; 33 FR 19684 (1968), modificato da 49 FR 3385 (1984)}"},
    "kalman1960": {"journal": "{Journal of Basic Engineering}"},
    "hsieh2023": {"year": "{2023}"},
}

def pulisci(v):
    v = v.replace("—", "--").replace("–", "--").replace("§", "\\S ").replace("×", "$\\times$").replace("°", "$^\\circ$")
    return v

if __name__ == "__main__":
    orig, cit, agg, uscita = sys.argv[1:5]
    chiavi = [k for r in open(cit, encoding="utf-8") if not r.startswith("#") and ":" in r for k in r.split(":")[1].split()]
    v_orig = {k: (t, c) for t, k, c in voci(open(orig, encoding="utf-8").read())}
    testo_agg = open(agg, encoding="utf-8").read()
    v_agg = {k: (t, c) for t, k, c in voci(testo_agg)}
    nuove = [k for k in v_agg if k not in chiavi]
    righe, provenienza = [], {}
    for k in sorted(set(chiavi) | set(nuove)):
        if k in v_agg:
            righe.append(v_agg[k][1]); provenienza[k] = "scritta a mano"; continue
        if k not in v_orig:
            sys.exit("voce senza sorgente: " + k)
        t, c = v_orig[k]
        cc = [(n, pulisci(val)) for n, val in campi(c) if n != "note"]
        for n, nv in CORREZIONI.get(k, {}).items():
            cc = [(a, b) for a, b in cc if a != n]
            if nv is not None: cc.append((n, nv))
        d = dict(cc)
        if "doi" not in d and "eprint" not in d and "url" in d:   # pagina o documento in rete: data di consultazione
            u = d["url"].strip("{}")
            if not any(x in u for x in "%#\\"):
                cc.append(("urldate", "{2026-11-14}"))
                cc.append(("note", "{\\url{" + u + "}, consultato il 14 novembre 2026}"))
        if "eprint" in d and "doi" not in d and t == "misc":
            cc = [(a, b) for a, b in cc if a != "howpublished"]
            cc.append(("howpublished", "{prestampa arXiv:" + d["eprint"].strip("{}") + "}"))
        righe.append("@%s{%s,\n%s\n}" % (t, k, ",\n".join("  %s = %s" % (a, b) for a, b in cc)))
        provenienza[k] = "file d'origine"
    with open(uscita, "w", encoding="utf-8") as f:
        f.write("% Bibliografia dell'allegato tecnico. Generata da programmi/costruisci_bib.py: non modificare a mano.\n\n")
        f.write("\n\n".join(righe) + "\n")
    print(len(righe), "voci scritte;", sum(1 for p in provenienza.values() if p == "scritta a mano"), "scritte a mano;", len(nuove), "nuove:", nuove)
