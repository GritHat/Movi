"""conta_liberi.py - un passaggio A1 'alta' (indice 0) con v2 e mappa dichiarata completa: quante celle 'libere'
hanno le griglie alla fine (per sapere se il pilota 'cert' mette alla prova il 'libero' o lo esclude per costruzione)."""
import os, sys, types
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__)); F15 = os.path.dirname(os.path.dirname(QUI))
sys.path[:0] = [QUI, os.path.join(F15, "10-simulatore")]
import numpy as np
import movi_lp_v2 as m2
m2.MAPPA_CERTIFICATA_PREDEFINITA = True
G = []
class Gr(m2.GrigliaPolare):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); G.append(self)
m2.GrigliaPolare = Gr
sys.modules["movi_lp_import"] = types.SimpleNamespace(nucleo=m2)
import prove_lp as P
P.REG = m2.carica_regole(os.path.join(QUI, "regole_lunga_portata_v2.json"))
R = P.passaggio("A1", "alta", 0, chiamante="interfaccia")
cls = [P.REG["classi"][c] for c in P.REG["scenari"]["aeroporto_e_droni"]["classi_ammesse"]]
for g in G:
    t = max(tp for tp, _ in g.passate)
    st = g.stati(t, cls)
    print(g.s.nome, "doppler" if g.doppler else "", "celle", st.size, "libere", int((st == m2.LIBERO).sum()),
          "dist max libera", float(g.dist[st == m2.LIBERO].max()) if (st == m2.LIBERO).any() else None)
