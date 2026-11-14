#!/usr/bin/env python3
"""Diagnosi di due attacchi: (1) B4, celle d'avviso fotogramma per fotogramma dopo la rimozione del pannello;
(2) B3b, quale identità ha la persona ferma sul bordo. Uso: <python> -I -B diag.py rimozione|bordo [k]"""
import sys, os, json, dataclasses
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # con -I la cartella dello script non è nel percorso
sys.argv, ARG = sys.argv[:1], sys.argv[1:]
import attacco as A
import numpy as np
K, C = A.K, A.C
cosa, k = ARG[0], int(ARG[1]) if len(ARG) > 1 else 300
if cosa == "rimozione":
    l = dict(profilo="d435i", livello="nominale", larghezza=424, tipo="passa", gruppo="B4_rimozione", k=k, rimozione=True)
else:
    l = dict(profilo="d435i", livello="nominale", larghezza=424, tipo="passa", gruppo="B3b_bordo_campo_stretto", k=k,
             caso="bordo2", pannello=dict(x0=0.5, x1=1.5))
A.imposta(l)
spec = A.spec_di(l)
meta, tempi, quadri, ver = A.genera(spec, 424)
n1 = len(quadri)
if cosa == "rimozione":
    sp2 = C._spec(l["gruppo"], "d435i", "nominale", "pavimento", f"B4_rimozione_vuoto__s{k:02d}", n=30)
    q2 = A.genera(sp2, 424)[2]
    quadri = quadri + q2
    tempi = tempi + [tempi[-1] + (i + 1) / 15 for i in range(len(q2))]
usc = os.path.join(A.QUI, "tmp_diag", spec["nome"])
par = dataclasses.replace(K.Parametri(), **A.CONFIG["tutte_p"])
r, err, _ = K.corri(K.SorgenteMemoria(meta, tempi, quadri), usc, par)
g = K.leggi_griglie(usc); rr = K.leggi_righe(usc)
pres, stati = g["possibile_presenza"], g["stati"]
if cosa == "rimozione":
    for kk in range(n1 - 3, len(rr)):
        m = pres[kk]
        st = np.bincount(stati[kk][m], minlength=4) if m.any() else [0, 0, 0, 0]
        ir = np.nonzero(m)[1]
        print(kk - n1, "celle d'avviso", int(m.sum()), "stati [non_oss, libero, occupato, ombra]", list(map(int, st)),
              "anelli", (int(ir.min()), int(ir.max())) if m.any() else None,
              [(e["tipo"], e.get("id"), e.get("motivo")) for e in rr[kk]["eventi"]][:4],
              [(t["id"], t["stato"]) for t in rr[kk]["tracce"]])
else:
    sog = [f["soggetti"][0] for f in ver["fotogrammi"]]
    for kk in range(0, len(rr), 3):
        s = sog[kk]
        print(kk, f"x={s['x']:.2f} fraz={s['frazione_visibile']:.2f}",
              [(t["id"], t["stato"], round(t["ultima_misura"][0], 2), round(t["ultima_misura"][1], 2), t.get("misura_tagliata")) for t in rr[kk]["tracce"]],
              [(e["tipo"], e.get("id"), e.get("motivo")) for e in rr[kk]["eventi"]][:3])
import shutil; shutil.rmtree(os.path.join(A.QUI, "tmp_diag"), ignore_errors=True)
