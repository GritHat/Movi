#!/usr/bin/env python3
"""Passa una sequenza nel formato comune dentro la catena di riferimento.

Uso:
    <ambiente>/venv/bin/python -I -B esegui.py <sequenza> <cartella_uscita> [opzioni]

  --ogni N            elabora un fotogramma ogni N (30 fps → 15 Hz con N = 2)
  --primo I, --ultimo J   solo i fotogrammi dalla posizione I alla J (comprese)
  --posa H,T          altezza in metri e inclinazione in gradi verso il basso (scavalca meta.json)
  -p NOME=VALORE      cambia un parametro di parametri.Parametri (ripetibile), per esempio -p q=0.5 -p portata_m=4
  --salva-griglie     scrive anche griglie.npz (stato di ogni cella e possibile presenza, per fotogramma)

Scrive in <cartella_uscita>: fotogrammi.jsonl (una riga JSON per fotogramma) e riassunto.json; stampa il riassunto.
Se meta.json non ha la posa e manca --posa, il piano del suolo è STIMATO dai primi 5 fotogrammi (lo dice il riassunto).
Un solo filo di calcolo, per misurare il costo in modo ripetibile. Codici d'uscita: 0 fatto; 2 uso sbagliato;
3 un invariante del nucleo è stato violato (difetto della catena)."""
import argparse
import dataclasses
import json
import math
import os
import sys

for _nome in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_nome, "1")
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # con -I la cartella dello script non è nel percorso

from catena import esegui                                           # noqa: E402
from geometria import posa_da_normale                               # noqa: E402
from mappa import InvarianteViolato                                 # noqa: E402
from parametri import Parametri                                     # noqa: E402
from sorgente import SorgenteCartella                               # noqa: E402


def leggi_parametri(coppie):
    par = Parametri()
    nomi = {c.name for c in dataclasses.fields(Parametri)}
    for coppia in coppie:
        nome, _, valore = coppia.partition("=")
        if nome not in nomi:
            raise ValueError(f"parametro sconosciuto: {nome} (vedi parametri.py)")
        attuale = getattr(par, nome)
        if isinstance(attuale, bool):
            valore = valore.lower() in ("1", "true", "vero", "si", "sì")
        else:
            valore = type(attuale)(valore)
        setattr(par, nome, valore)
    return par


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("sequenza")
    p.add_argument("uscita")
    p.add_argument("--ogni", type=int, default=1)
    p.add_argument("--primo", type=int, default=0)
    p.add_argument("--ultimo", type=int, default=None)
    p.add_argument("--posa", default=None)
    p.add_argument("-p", dest="parametri", action="append", default=[])
    p.add_argument("--salva-griglie", action="store_true")
    a = p.parse_args(argv)
    try:
        par = leggi_parametri(a.parametri)
    except ValueError as e:
        p.error(str(e))                                             # esce con 2
    posa = None
    if a.posa:
        h, t = (float(v) for v in a.posa.split(","))
        t = math.radians(t)
        posa = posa_da_normale(h, [0.0, -math.cos(t), -math.sin(t)], nota="dalla riga di comando")
    sorgente = SorgenteCartella(a.sequenza, ogni=a.ogni, primo=a.primo, ultimo=a.ultimo)
    try:
        riassunto = esegui(sorgente, a.uscita, par, posa, a.salva_griglie)
    except InvarianteViolato as e:
        print(f"INVARIANTE VIOLATO: {e}", file=sys.stderr)
        return 3
    json.dump(riassunto, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
