#!/usr/bin/env python3
"""MoVi video v3c: cifre_v3c.json = cifre_finale.json (blocco del verdetto finale, che resta) + correzione giurato 12 sulla riga
V-11 + le chiavi F7R-C1-* SOLO dai rapporti c1 (f20-chiusura/05-scorta/correzione_f7r/CORREZIONE.md e verifica/VERIFICA.md).
Controllo: ogni numero di testo_schermo deve comparire in valore+intervallo della stessa chiave. Non sovrascrive.
Uso (da progetto_v3): python3 -I strumenti/cifre_v3c.py"""
import json, os, re, sys
OUTJ, OUTJS = "cifre_v3c.json", "assets/data/cifre_v3c.js"
for f in (OUTJ, OUTJS):
    if os.path.exists(f): sys.exit(f"esiste gia': {f}")
cf = json.load(open("cifre_finale.json", encoding="utf-8"))
FC1 = "f20/05-scorta/correzione_f7r/CORREZIONE.md; verifica/VERIFICA.md (confronto appaiato, costo.txt, attacco F7c)"
# giurato 12: in quale prova sono i 2/60 falsi eventi (CONTATTO.md §2: F5, quasi incrocio a 39 m con gli ottici ciechi)
cf["V-11-PROVA"]["testo_schermo"] = "contact rule under test: 57/60 [0.863; 0.983] · false events in a 39 m near miss (F5) 2/60 [0.009; 0.114] · not adopted"
cf["V-11-PROVA"]["intervallo"] += " (F5: near miss at 39 m, optics blinded; CONTATTO.md §2)"
nuove = {
 "F7R-C1-AVVISO": {"valore": "fix c1 (under test): warning to the carrier before the first fragment, radar and cameras blinded together (total cell): 59/59 with c1, 0/59 without, same seeds",
   "intervallo": "59/59 [0.939; 1]; without 0/59 [0; 0.061]; paired, McNemar exact p = 3.5e-18",
   "stato": "simulato; sostenuto dai dati; strada promettente, non adottata come risultato definitivo", "fonte": FC1,
   "testo_schermo": "fix under test · carrier warned before the first fragment, radar and cameras blinded: 59/59 [0.939; 1] · without 0/59 [0; 0.061] · same seeds · sim."},
 "F7R-C1-LIBERO": {"valore": "with c1: 'clear' on the tracked drone or a fragment 0 in every cell; region kept 60/60 every cell",
   "intervallo": "0/60 [0; 0.060]; continuity 60/60 [0.940; 1]", "stato": "simulato", "fonte": FC1,
   "testo_schermo": "with the fix: 'clear' on the tracked drone or a fragment 0/60 [0; 0.060] · region kept 60/60 [0.940; 1] · sim."},
 "F7R-C1-LOC": {"valore": "warning not localised: conservative sphere around the carrier, up to 565 m, on for a median of 8 s",
   "intervallo": "radius 565 m at 8 s (median); active 3-8 s, median 8 s; 240 runs with event", "stato": "simulato; limite", "fonte": FC1,
   "testo_schermo": "limit · warning not localised: conservative sphere up to 565 m, median 8 s"},
 "F7R-C1-RIACQ": {"valore": "radar reacquisition within 2 s still below the 51/60 threshold: ahead 49/60, in a turn 40/60",
   "intervallo": "49/60 [0.701; 0.894]; 40/60 [0.541; 0.773]", "stato": "simulato; P2 smentita (limite)", "fonte": FC1,
   "testo_schermo": "limit · reacquisition within 2 s below the 51/60 threshold: ahead 49/60 [0.701; 0.894] · in a turn 40/60 [0.541; 0.773]"},
 "F7R-C1-FALSI": {"valore": "false warnings if the radar saturates for another cause: 11/200",
   "intervallo": "11/200 [0.031; 0.096] (F7c, radar saturated 1 s by another cause, natural glare)", "stato": "simulato; robustezza smentita sotto interferenza", "fonte": FC1,
   "testo_schermo": "limit · false warnings if the radar saturates for another cause: 11/200 [0.031; 0.096] · sim."},
 "F7R-C1-ID": {"valore": "undeclared spurious identities 1 -> 0 (not significant); reacquired identity declared presumed, doubtful",
   "intervallo": "1/60 [0.003; 0.089] -> 0/60 [0; 0.060]", "stato": "simulato; non significativo", "fonte": FC1,
   "testo_schermo": "spurious identities 1/60 → 0/60 [0; 0.060], not significant · reacquired identity: presumed, doubtful"},
}
num = lambda s: set(re.findall(r"\d+(?:\.\d+)?(?:e-\d+)?", s))
bad = 0
for k, v in list(cf.items()) + list(nuove.items()):
    if not isinstance(v, dict) or "testo_schermo" not in v: continue
    extra = num(v["testo_schermo"]) - num(v.get("valore", "") + " " + v.get("intervallo", "")) - {"0", "1", "2", "5", "7"} - num(v.get("_ammessi", ""))
    if k.startswith("F7R-C1") or k == "V-11-PROVA":
        if extra: print("NUMERO A SCHERMO NON NEL BLOCCO", k, extra); bad += 1
cf.update(nuove)
cf["_nota_v3c"] = "v3c: cifre_finale.json + V-11 (giurato 12) + F7R-C1-* dai rapporti c1. Generato da strumenti/cifre_v3c.py."
if bad: sys.exit(5)
json.dump(cf, open(OUTJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(OUTJS, "w", encoding="utf-8").write("/* GENERATO da strumenti/cifre_v3c.py */\nwindow.__CIFRE = " + json.dumps(cf, ensure_ascii=False) + ";\n")
print("scritti", OUTJ, OUTJS)
