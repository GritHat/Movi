#!/usr/bin/env python3
"""Ultime correzioni, parte 4: residui trovati cercando tutte le occorrenze e rileggendo a freddo."""
import pathlib, sys
base = pathlib.Path(__file__).resolve().parent.parent / "capitoli"
E = [
 ("A_parametri.tex", r"i valori marcati «da misurare» vanno rifissati sulla camera usata.", r"i valori marcati «non misurato» vanno fissati sulla camera usata."),
 ("08_limiti.tex", r"\prova{S} 0 passaggi con un vuoto su 23\,402 (6\,000 camminatori distinti: meno di 6,4 su 10\,000), modello ideale del sensore; la premessa manca in 24 passaggi su 23\,402 con l'avviso senza traccia, in 928 senza &",
  r"\prova{S} 0 passaggi con un vuoto dopo l'ingresso su 23\,402 (6\,000 camminatori distinti: meno di 7 su 10\,000), modello ideale del sensore; la premessa manca in 928 passaggi, e con l'avviso senza traccia 24 restano senza avviso &"),
 ("05_occlusione.tex", r"su semi nuovi 0 su 23\,402\\", r"su semi nuovi 0 su 23\,402 (dopo l'ingresso)\\"),
]
for f, old, new in E:
    c = (base / f).read_text(encoding="utf-8").count(old)
    if c != 1: print("ERRORE", f, c, old[:60]); sys.exit(1)
for f, old, new in E:
    p = base / f; p.write_text(p.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
print("parte 4: sostituzioni applicate", len(E))
