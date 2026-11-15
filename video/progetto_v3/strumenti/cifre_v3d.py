#!/usr/bin/env python3
"""MoVi video v3d (finale; cifre_v3c.json resta): cifre_v3d.json = cifre_v3c.json con
- LIMITI: la riga di prima di c1 («debris warning to the carrier not reliable») sostituita con le righe c1
  (QA_V3C D1-D2, REVISIONE_V3C C1); l'unica cifra (11/200) e' copiata con intervallo e stato da F7R-C1-FALSI;
- V-11-PROVA: tolta la sigla «(F5)» dal testo a schermo (REVISIONE_V3C C4); numeri invariati.
Controllo: ogni numero delle righe nuove deve stare in valore+intervallo di F7R-C1-FALSI. Non sovrascrive.
Uso (da progetto_v3): python3 -I strumenti/cifre_v3d.py"""
import json, os, re, sys
OUTJ, OUTJS = "cifre_v3d.json", "assets/data/cifre_v3d.js"
for f in (OUTJ, OUTJS):
    if os.path.exists(f): sys.exit(f"esiste gia': {f}")
cf = json.load(open("cifre_v3c.json", encoding="utf-8"))
L = cf["LIMITI"]["valore"]
vecchia = "radar blinded: debris warning to the carrier not reliable"
assert vecchia in L
k = L.index(vecchia)
nuove = ["radar blinded: carrier warned only with a fix under test (sim.)",
         "that fix: warning not localised; reacquisition still partial",
         "that fix: false warnings 11/200 [0.031; 0.096] (sim.)"]
num = lambda s: set(re.findall(r"\d+(?:\.\d+)?", s))
fonte = cf["F7R-C1-FALSI"]["valore"] + " " + cf["F7R-C1-FALSI"]["intervallo"]
extra = set().union(*[num(x) for x in nuove]) - num(fonte)
if extra: sys.exit(f"numeri non nel blocco F7R-C1-FALSI: {extra}")
cf["LIMITI"]["valore"] = L[:k] + nuove + L[k + 1:]
cf["LIMITI"]["stato"] = ("testo dai verdetti; righe radar da c1 (CORREZIONE.md, VERIFICA.md): 11/200 [0.031; 0.096] = F7R-C1-FALSI, "
                         "simulato; correzione in prova, non adottata")
v = cf["V-11-PROVA"]["testo_schermo"]
assert " (F5)" in v
cf["V-11-PROVA"]["testo_schermo"] = v.replace(" (F5)", " with optics blinded")
cf["_nota_v3d"] = "v3d: cifre_v3c.json + LIMITI con c1 (QA_V3C D1) + V-11 senza sigla. Generato da strumenti/cifre_v3d.py."
json.dump(cf, open(OUTJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(OUTJS, "w", encoding="utf-8").write("/* GENERATO da strumenti/cifre_v3d.py */\nwindow.__CIFRE = " + json.dumps(cf, ensure_ascii=False) + ";\n")
print("scritti", OUTJ, OUTJS)
