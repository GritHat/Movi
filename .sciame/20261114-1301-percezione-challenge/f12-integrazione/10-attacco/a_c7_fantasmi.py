# a_c7_fantasmi.py — P11: quanti avvisi accenderebbe c7 sui fantasmi di F-403. Legge SOLO le uscite gia' su disco di
# f10-dati/20-validazione/uscite/sim (catena f10, parametri del nucleo, profondita' simulata da scheda): json e npz, nessun codice altrui.
# Una traccia «finisce senza entrare in ombra» = il suo id c'e' nel fotogramma k e non nel k+1, e nel k non era «previsto» ne' «perso».
import sys, os, json, glob, re
import numpy as np
B = sys.argv[1]
sys.path.insert(0, os.path.join(B, "..", "..", "..", "10-catena"))
from parametri import IN_OMBRA
tot = []
for d in sorted(glob.glob(os.path.join(B, "*_nom__pannello_a12__s[0-9][0-9]"))):
    L = [json.loads(l) for l in open(os.path.join(d, "fotogrammi.jsonl"))]
    g = np.load(os.path.join(d, "griglie.npz"))
    st, az, rr = g["stati"], np.radians(g["azimut_gradi"]), g["distanza_m"]
    cx, cz = np.outer(np.sin(az), rr), np.outer(np.cos(az), rr)
    n_fine = n_c7 = n_conf_c7 = 0
    for k in range(len(L) - 1):
        dopo = {t["id"] for t in L[k + 1]["tracce"]}
        omb = st[k] == IN_OMBRA
        for t in L[k]["tracce"]:
            if t["id"] in dopo or t["stato"] in ("previsto", "perso"):
                continue
            n_fine += 1
            x, z = t["ultima_misura"][0], t["ultima_misura"][1]
            if omb.any() and np.hypot(cx[omb] - x, cz[omb] - z).min() <= 0.75:
                n_c7 += 1
    pend = len(L[-1]["possibili_presenze"])
    stati = sorted({t["stato"] for f in L for t in f["tracce"]})
    tot.append((os.path.basename(d), len(L), n_fine, n_c7, pend))
    print("%-36s fotogrammi %3d | tracce finite senza entrare in ombra %3d | di cui entro 0,75 m da un'ombra (c7 accenderebbe) %3d | strati pendenti all'ultimo fotogramma %3d" % tot[-1])
a = np.array([t[3] for t in tot]); f = np.array([t[2] for t in tot]); p = np.array([t[4] for t in tot])
print("SEQUENZE %d | c7 accenderebbe: mediana %.1f, min %d, max %d, sequenze con almeno uno %d | finite: mediana %.1f | pendenti alla fine: mediana %.1f, min %d, max %d | stati visti: %s"
      % (len(tot), np.median(a), a.min(), a.max(), int((a > 0).sum()), np.median(f), np.median(p), p.min(), p.max(), stati))
