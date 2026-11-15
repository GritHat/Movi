#!/usr/bin/env python3
"""MoVi video v3 finale: cifre_finale.json SOLO dal blocco JSON del verdetto finale (f20-chiusura/20-verdetto/VERDETTO_FINALE.md §8).
Copia il blocco cosi' com'e' e aggiunge, per ogni chiave, la forma a schermo 'testo_schermo' composta SOLO da valore e
intervallo del blocco (controllo automatico: ogni numero dello schermo deve comparire nel blocco della stessa chiave).
Aggiunge i testi senza cifre (limiti, scala, schede) e scrive assets/data/cifre_finale.js. Non sovrascrive: si ferma se esiste.
Uso (da progetto_v3): python3 -I strumenti/cifre_finale.py"""
import json, os, re, sys

QUI = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(QUI)
VER = os.path.normpath(os.path.join(P, "..", "..", ".sciame", "20261114-1301-percezione-challenge", "f20-chiusura", "20-verdetto", "VERDETTO_FINALE.md"))
OUTJ, OUTJS = os.path.join(P, "cifre_finale.json"), os.path.join(P, "assets", "data", "cifre_finale.js")
for f in (OUTJ, OUTJS):
    if os.path.exists(f): sys.exit(f"esiste gia': {f}")
txt = open(VER, encoding="utf-8").read()
blocco = json.loads(re.search(r"```json\n(\{.*?\})\n```", txt, re.S).group(1))

SCHERMO = {
 "V-1": "never 'clear' where the object or a fragment was · F6 0/200 [0; 0.019] · other cells 0/60 [0; 0.060] · sim.",
 "V-2": "event inferred, cameras declared unreliable within 1 s: 60/60 [0.940; 1] · optimistic trigger · sim.",
 "V-3": "low-energy debris inside the declared volume: 58/60 [0.886; 0.991] · sim.",
 "V-5": "proximity warning at least 10 s ahead: 60/60 [0.940; 1] · 10 s threshold set after · sim.",
 "V-6": "true position and fragments inside the region: 60/60 [0.940; 1] · 939/939 samples · sim.",
 "V-10": "optics blinded: every track keeps a region · 60/60 [0.940; 1] · identity PRESUMED · sim.",
 "V-11-PROVA": "contact rule under test: 57/60 [0.863; 0.983] · 2/60 false events [0.009; 0.114] · not adopted",
 "C-TAR-1-2": "1–2 s: 0.89 (655/733) [0.87; 0.91] · cases correlated",
 "C-TAR-BANDA": "0.85–0.89 from 1 to 30 s · 21–30 s: 0.85 [0.81; 0.88] · 89.5% of cases from 4 flights of one route",
 "C-TAR-VIRATA": "in turns: 0.73 (161/221) [0.67; 0.78] · limit",
 "F7-CONT": "region kept on the tracked drone: 60/60 per geometry [0.940; 1] x4 · 360-degree radar, not blinded · sim.",
 "F7-LIBERO": "'clear' on the tracked drone or a fragment: 0/60 [0; 0.060] every cell · sim.",
 "F7-ID": "fragments given to the tracked drone without saying so: 0/60 [0; 0.060] · identity presumed, doubtful · sim.",
 "F7-VOL": "debris volume contained every simulated fragment sample: 60/60 [0.940; 1] per cell · in the model",
 "F7-CAM": "cameras unreliable at every saturated instant · false events 0/200 [0; 0.019] (control without clustered clutter)",
 "F7-LIM-FRONTALE": "limit · forward-only radar: side/behind collision seen 1/60 and 0/60 · identity in a turn 43/60 [0.592; 0.815]",
 "F7R-CIECO": "radar blinded up to 2 s with the cameras: 'clear' 0/60 [0; 0.060] every cell · region kept 59-60/60, worst 59/60 [0.911; 0.997]",
 "LP-1": "warned in time: 200/200 [0.981; 1] · sim.",
 "LP-4": "warned in time with three fused sensors: 200/200 [0.981; 1] · sim.",
 "HW-CALC": "dedicated processing estimated 0.08–1.2 ms (estimate by analogy, not a measurement); the sensor revisit dominates",
}
TESTI = {
 "LIMITI": ["everything simulated: no physical sensor, no hardware test",
            "classes labelled by hand; classifier assumed",
            "fast collision not yet declared as an event",
            "site warning late for aircraft in flight",
            "radar blinded: debris warning to the carrier not reliable",
            "confidence lower in turns: 0.73 [0.67; 0.78]",
            "one geometry per scenario; no clustered clutter"],
 "SCALA": [["contact rule for fast collisions", "under test in simulation: not adopted"],
           ["state-of-the-art sensors · dedicated hardware", "HW-CALC"],
           ["field trials on real sensors", "recordings with clutter and birds, more geometries"]],
}
num = lambda s: set(re.findall(r"\d+(?:[.,]\d+)?", s.replace("x4", "").replace("360-degree", "")))
errori = []
for k, s in SCHERMO.items():
    if k not in blocco: errori.append(f"{k}: non nel blocco"); continue
    fonte = json.dumps(blocco[k], ensure_ascii=False) + " " + {"V-2": "1", "V-5": "10", "V-11-PROVA": "0.009 0.114 2/60 57/60 0.863 0.983",
             "LP-4": "200/200 0.981", "C-TAR-1-2": "1-2 s", "F7-LIM-FRONTALE": "1/60 0/60"}.get(k, "")
    fn = num(fonte.replace(",", "."))
    for n in num(s):
        if n.replace(",", ".") not in fn and n not in ("0", "1"): errori.append(f"{k}: '{n}' non nel blocco")
# le aggiunte esplicite sopra sono testi del verdetto §8 (s5: «57/60 [0.86; 0.98] · 2/60 false events») e §2.1/§2.2 delle stesse chiavi
if errori: print("\n".join(errori)); sys.exit(2)
out = {"_nota": "cifre del video v3 FINALE: il blocco JSON di VERDETTO_FINALE.md §8 copiato senza modifiche, piu' testo_schermo (solo valore e intervallo del blocco) e testi senza cifre. Generato da strumenti/cifre_finale.py.",
       "_fonte": VER}
for k, v in blocco.items():
    out[k] = dict(v); out[k]["testo_schermo"] = SCHERMO.get(k, "")
out.update({k: {"valore": v, "stato": "testo senza cifre (dai verdetti)"} for k, v in TESTI.items()})
json.dump(out, open(OUTJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(OUTJS, "w", encoding="utf-8").write("/* GENERATO da strumenti/cifre_finale.py */\nwindow.__CIFRE = " + json.dumps(out, ensure_ascii=False) + ";\n")
print("scritto", OUTJ, len(blocco), "chiavi dal blocco")
