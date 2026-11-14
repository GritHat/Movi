#!/usr/bin/env python3
"""Passa nella catena di riferimento tutte le sequenze simulate su disco (o quelle il cui nome contiene un testo).

Uso: <python> -I -B corri_sim.py [--filtro TESTO] [--regex ESPRESSIONE] [--etichetta NOME] [-p nome=valore ...]
Scrive uscite/<etichetta>/<sequenza>/{fotogrammi.jsonl, riassunto.json, griglie.npz, ingressi.json} e
uscite/<etichetta>/ELENCO.json (una riga per sequenza: esito, tempi, tracce, eventi)."""
import argparse
import dataclasses
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune as K                                             # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--filtro", default="")
    p.add_argument("--regex", default="")
    p.add_argument("--etichetta", default="sim")
    p.add_argument("-p", dest="par", action="append", default=[])
    p.add_argument("--senza-griglie", action="store_true")
    a = p.parse_args()
    par = K.Parametri()
    for coppia in a.par:
        nome, _, valore = coppia.partition("=")
        attuale = getattr(par, nome)
        setattr(par, nome, (valore.lower() in ("1", "true")) if isinstance(attuale, bool) else type(attuale)(valore))
    nomi = sorted(n for n in os.listdir(K.SEQ_SIM)
                  if os.path.isdir(os.path.join(K.SEQ_SIM, n)) and a.filtro in n
                  and (not a.regex or re.search(a.regex, n)))
    radice = os.path.join(K.USCITE, a.etichetta)
    os.makedirs(radice, exist_ok=True)
    elenco, t0 = [], time.time()
    for n in nomi:
        sorg = K.SorgenteCartella(os.path.join(K.SEQ_SIM, n))
        r, err, ing = K.corri(sorg, os.path.join(radice, n), dataclasses.replace(par), griglie=not a.senza_griglie)
        elenco.append({"nome": n, "errore": err, "ingressi": len(ing),
                       "fotogrammi": r["fotogrammi"] if r else None,
                       "tempo_ciclo_ms": r["tempo_ciclo_ms"] if r else None,
                       "tracce_confermate": r["tracce_confermate"] if r else None,
                       "eventi": r["eventi"] if r else None,
                       "frazione_per_stato": r["frazione_per_stato"] if r else None})
    with open(os.path.join(radice, "ELENCO.json"), "w", encoding="utf-8") as f:
        json.dump({"parametri": dataclasses.asdict(par), "sequenze": elenco}, f, ensure_ascii=False, indent=1)
    errori = [e for e in elenco if e["errore"]]
    print(f"{len(elenco)} sequenze, {len(errori)} con errore, {time.time() - t0:.1f} s")
    for e in errori:
        print("ERRORE", e["nome"], e["errore"])


if __name__ == "__main__":
    main()
