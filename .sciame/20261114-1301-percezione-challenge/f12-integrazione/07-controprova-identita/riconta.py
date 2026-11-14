#!/usr/bin/env python3
"""Riconto indipendente (programma mio, sola libreria standard) delle cifre di 06-identita dai .jsonl grezzi,
e confronto con il rifacimento (risultati/*_rifatto.jsonl).  Uso: python3 riconta.py"""
import json
import math
import os
import re

QUI = os.path.dirname(os.path.abspath(__file__))
AUT = os.path.join(QUI, "..", "06-identita", "risultati")
MIE = os.path.join(QUI, "risultati")


def wilson(k, n, z=1.96):
    if n == 0:
        return "[–]"
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return f"[{100 * max(0, c - h):.0f}–{100 * min(1, c + h):.0f}]"


def leggi(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(r) for r in f if r.strip()]


def caso(r):
    m = re.search(r"pannello_(a12z21|a12|a05|b|c|d)(?:_scuro|_nero|_alta185)?__s", r["nome"])
    if not m:
        return None
    pl = re.match(r"(d435i|d455|g335)_(nom|lim)__", r["nome"])
    var = re.search(r"pannello_a12(_scuro|_nero|_alta185)__", r["nome"])
    return f"{pl.group(1)}/{pl.group(2)}/{m.group(1)}{var.group(1) if var else ''}"


def conta(righe, conf):
    out = {}
    lib = omb = fant = scat_v = scat_n = fuori = nasc = acc = npass = errori = 0
    for r in righe:
        if r["conf"] != conf:
            continue
        if r.get("errore"):
            errori += 1
            continue
        lib += r["libero_in_ombra"]
        omb += r["celle_ombra_fot"]
        c = caso(r)
        if c:
            k, n = out.get(c, (0, 0))
            out[c] = (k + (r.get("continuita_pulita") is True), n + 1)
            if not c.endswith("/d") and "/lim/" not in c and r.get("cella_centro_nascosto"):
                cc = r["cella_centro_nascosto"]
                nasc += sum(cc.values())
                fuori += sum(v for k_, v in cc.items() if k_ != "possibile_presenza")
            if not c.endswith("/d"):
                acc += bool(r.get("avviso_acceso_alla_fine"))
                npass += 1
        if "pavimento_vuoto" in r["nome"] and "_nom__" in r["nome"]:
            fant += r["tracce_confermate"]
        for o in r.get("ostacoli") or []:
            if "scatola" in r["nome"] and r["nome"].startswith("d435i_nom__"):
                scat_v += o["fotogrammi_visto_entro_15cm"]
                scat_n += o["fotogrammi"]
    return out, dict(libero_in_ombra=lib, celle_ombra_fot=omb, tracce_pavimento_nominale=fant, scatola=f"{scat_v}/{scat_n}",
                     nascosta_fuori_avviso=f"{fuori}/{nasc}", avviso_acceso_alla_fine=f"{acc}/{npass}", errori=errori)


def stampa(titolo, righe, confs):
    print(f"\n## {titolo} ({len(righe)} righe)")
    for conf in confs:
        per_caso, tot = conta(righe, conf)
        if not per_caso and not tot["celle_ombra_fot"]:
            continue
        print(f"- **{conf}**: " + "; ".join(f"{c} {k}/{n} {wilson(k, n)}" for c, (k, n) in sorted(per_caso.items())))
        print(f"  somma nominale d435i a12+a05+b+c: {sum(k for c, (k, n) in per_caso.items() if c.startswith('d435i/nom') and not c.endswith('/d'))}"
              f"/{sum(n for c, (k, n) in per_caso.items() if c.startswith('d435i/nom') and not c.endswith('/d'))}; {tot}")
    return {conf: conta(righe, conf) for conf in confs}


def main():
    confs = ("prima", "tutte", "tutte_p")
    a424 = stampa("AUTORE nuovi424", leggi(os.path.join(AUT, "nuovi424.jsonl")), confs)
    a848 = stampa("AUTORE nuovi848", leggi(os.path.join(AUT, "nuovi848.jsonl")), confs)
    stampa("AUTORE disco (taratura)", leggi(os.path.join(AUT, "disco.jsonl")), confs)
    stampa("AUTORE z21_424", leggi(os.path.join(AUT, "z21_424.jsonl")), confs)
    stampa("AUTORE z21_848", leggi(os.path.join(AUT, "z21_848.jsonl")), confs)
    m424 = stampa("RIFATTO nuovi424", leggi(os.path.join(MIE, "nuovi424_rifatto.jsonl")), confs)
    m848 = stampa("RIFATTO nuovi848", leggi(os.path.join(MIE, "nuovi848_rifatto.jsonl")), ("tutte_p",))
    stampa("REPLICA semi k = 200… a 424 (mai usati)", leggi(os.path.join(MIE, "ultimi424_replica.jsonl")), ("tutte_p",))
    stampa("REPLICA semi k = 200… a 848 (mai usati)", leggi(os.path.join(MIE, "ultimi848_replica.jsonl")), ("tutte_p",))
    print("\n## Confronto riga per riga autore/rifatto (campi deterministici)")
    campi = ("continuita_pulita", "esito_identita", "libero_in_ombra", "tracce_confermate", "cella_centro_nascosto", "ostacoli")
    for nome in ("nuovi424", "nuovi848"):
        A = {(r["nome"], r["conf"]): r for r in leggi(os.path.join(AUT, nome + ".jsonl"))}
        M = {(r["nome"], r["conf"]): r for r in leggi(os.path.join(MIE, nome + "_rifatto.jsonl"))}
        diversi = [k for k in M if k in A and any(A[k].get(c) != M[k].get(c) for c in campi)]
        print(f"- {nome}: {len(M)} righe rifatte, {len([k for k in M if k in A])} confrontate, {len(diversi)} diverse {diversi[:3]}")
    # i casi esclusi: passaggi senza esito di continuità (mai nascosto, non ricompare…)
    print("\n## Esiti dell'identità per tutte_p (i casi che non sono né «stessa» né «diversa»)")
    for nome in ("nuovi424", "nuovi848"):
        es = {}
        for r in leggi(os.path.join(AUT, nome + ".jsonl")):
            if r["conf"] == "tutte_p" and caso(r):
                es.setdefault(caso(r), {}).setdefault(str(r.get("esito_identita")), 0)
                es[caso(r)][str(r.get("esito_identita"))] += 1
        print(f"- {nome}: {json.dumps(es, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
