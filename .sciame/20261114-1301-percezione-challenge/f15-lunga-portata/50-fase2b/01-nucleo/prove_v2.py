"""prove_v2.py - prove unitarie di movi_lp_v2.py (f15/50-fase2b/01-nucleo). Solo conto e simulazione costruita.

Uso: <venv>/bin/python -I -B prove_v2.py [--compat]
Ogni prova confronta v2 con v1 (movi_lp.py di 04-moto, importato senza scrivere nella sua cartella) sul caso che
rompeva v1 (attacchi X1, X3, X4, X5, X6 di f15/20-attacco; validazione-1 e 2 di 11-prove). Un caso costruito per
prova: niente frequenze. --compat: un passaggio A1 di prove_lp con v2 al posto del nucleo (piu' lento).
"""
import copy
import json
import math
import os
import sys
import time
import types

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
F15 = os.path.dirname(os.path.dirname(QUI))
sys.path.insert(0, QUI)
import numpy as np  # noqa: E402
import movi_lp_v2 as m2  # noqa: E402

sys.path.insert(0, os.path.join(F15, "04-moto"))
import movi_lp as m1  # noqa: E402

R1 = m1.carica_regole(os.path.join(F15, "04-moto", "regole_lunga_portata.json"))
R2 = m2.carica_regole(os.path.join(QUI, "regole_lunga_portata_v2.json"))
ESITI = []


def esito(nome, v1_rotto, v2_ok, dettagli):
    ESITI.append({"prova": nome, "v1_rompeva": bool(v1_rotto), "v2_regge": bool(v2_ok), "dettagli": dettagli})
    print("%-34s v1 rompeva: %-5s  v2 regge: %-5s  %s" % (nome, bool(v1_rotto), bool(v2_ok), json.dumps(dettagli, default=float)[:160]))


def traccia(p, v, sp=2.0, sv=0.3, t=0.0):
    return types.SimpleNamespace(t_vista=t, p_ultima=np.asarray(p, float), v_ultima=np.asarray(v, float), sigp_ultima=sp, sigv_ultima=sv)


def moto(v0, a, vmax, tau):
    ta = max(0.0, (vmax - v0) / a)
    return v0 * tau + 0.5 * a * tau ** 2 if tau <= ta else v0 * ta + 0.5 * a * ta ** 2 + vmax * (tau - ta)


RADAR = R1["sensori_segnaposto"]["radar_sorveglianza"]


def prova_X1():
    fuori1, fuori2 = [], []
    for a in (20.0, 25.0):
        for tau in (0.5, 1, 2, 3, 5, 8, 10, 15, 30):
            d = moto(0.0, a, 45.0, tau)
            tr = traccia([0, 0, 50], [0, 0, 0])
            if d > m1.insieme_presenza(tr, tau, R1, R1["scenari"]["aeroporto_e_droni"]["classi_ammesse"])["raggio"]:
                fuori1.append((a, tau))
            for sc in ("aeroporto_e_droni", "sito_droni_rullaggio", "ferrovia"):
                if d > m2.insieme_presenza(tr, tau, R2, R2["scenari"][sc]["classi_ammesse"])["raggio"]:
                    fuori2.append((sc, a, tau))
    # X2: aereo in decollo a 205 m/s
    tr = traccia([0, 0, 300], [205.0, 0, 0], sp=7.5, sv=2.0)
    f2 = [tau for tau in (1, 2, 5, 10, 30) if 205.0 * tau > m2.insieme_presenza(tr, tau, R2, R2["scenari"]["aeroporto_e_droni"]["classi_ammesse"])["raggio"]]
    esito("X1 scatto da fermo (e X2 205 m/s)", fuori1, not fuori2 and not f2, {"v1_fuori(a,tau)": fuori1, "v2_fuori": fuori2, "v2_X2_fuori_tau": f2})


def prova_X3():
    aer = m2.tempestivita(R2, "aeroporto_e_droni")["operatore_di_sito"]
    sito = m2.tempestivita(R2, "sito_droni_rullaggio")["operatore_di_sito"]
    v1_d = m1.distanza_avviso(R1, R1["scenari"]["aeroporto_e_droni"]["classi_ammesse"], "operatore_di_sito")
    v1_port = m1.Sensore("r", [0, 0, 10], RADAR).portata(0.01, 0.99, 5)
    ins = m2.Inseguitore(R2, "aeroporto_e_droni", [])
    esito("X3 tempestivita' dichiarata", v1_port >= v1_d, (not aer["tempestivo"]) and sito["tempestivo"]
          and "operatore_di_sito" in ins.dichiarazione["avviso_non_tempestivo_per"],
          {"v1": {"d_avv": round(v1_d), "portata": round(v1_port)}, "v2_aeroporto": aer, "v2_sito": sito,
           "v2_non_tempestivo_per": ins.dichiarazione["avviso_non_tempestivo_per"]})


def _griglia(mod, par=RADAR, n_az=360, r_max=3000.0, dr=100.0, **k):
    s = mod.Sensore("radar", [0, 0, 10], dict(par))
    return s, mod.GrigliaPolare(s, r_max, dr, n_az, **k)


def prova_X4():
    hover = {"rcs_m2": 0.01, "v_max": 19.0}
    p1 = m1.Sensore("r", [0, 0, 10], RADAR).portata(0.01, 0.99, 5)
    p2 = m2.Sensore("r", [0, 0, 10], RADAR).portata(0.01, 0.99, 5)
    _, g1 = _griglia(m1, n_az=36)
    _, g2 = _griglia(m2, n_az=36, mappa_certificata=True)
    for k in range(5):
        g1.passata(float(k))
        g2.passata(float(k))
    q = np.array([2250.0, 0.0, 10.0])   # cella 2200-2300 m: le vicine a 2150 e 2350 m reggono in v1
    s1, s2 = m1.NOMI_STATO[g1.stato_punto(q, 4.0, hover)], m2.NOMI_STATO[g2.stato_punto(q, 4.0, hover)]
    s2v = m2.NOMI_STATO[g2.stato_punto(np.array([700.0, 0, 10]), 4.0, hover)]   # cella 700-800 m, vicine entro 877 m
    pd1_880 = float(m2.Sensore("r", [0, 0, 10], RADAR).pd(p2, 0.01))
    # limite: con correlazione qualunque P(5 mancate) = E[(1-pd)^5] <= E[1-pd] = 1 - Pd media: n_eff = 1 e' prudente
    esito("X4 passate correlate", s1 == "libero", s2 != "libero" and s2v == "libero" and p2 < 900 and pd1_880 >= 0.99 - 1e-9,
          {"portata_v1_m": round(p1), "portata_v2_m": round(p2), "Pd_1_passata_alla_portata_v2": round(pd1_880, 4),
           "stato_2250m_v1": s1, "stato_2250m_v2": s2, "stato_700m_v2": s2v})


def prova_X5():
    cls = [R2["classi"][c] for c in R2["scenari"]["aeroporto_e_droni"]["classi_ammesse"]]
    cls1 = [R1["classi"][c] for c in R1["scenari"]["aeroporto_e_droni"]["classi_ammesse"]]
    p = np.array([600.0, 0.0, 10.0])
    _, g1 = _griglia(m1)
    for k in range(5):
        g1.passata(float(k))
    st1 = m1.NOMI_STATO[g1.stato_punto(p, 4.0, cls1)]
    out = {"v1_senza_edificio_in_pianta": st1}
    # (a) nessuna certificazione
    _, g = _griglia(m2)
    for k in range(5):
        g.passata(float(k))
    out["v2_senza_certificazione"] = m2.NOMI_STATO[g.stato_punto(p, 4.0, cls)]
    # (b) sfondo atteso a 1500 m, misurato a 400 m nei raggi dell'edificio ignoto (az -5..5 gradi)
    att = np.full((360, 1), 1500.0)
    _, g = _griglia(m2, sfondo_atteso=att)
    mis = att.copy()
    az = np.degrees(g.az)
    mis[(az > -5) & (az < 5), 0] = 400.0
    for k in range(5):
        g.passata(float(k), sfondo_misurato=mis)
    out["v2_sfondo_piu_vicino"] = m2.NOMI_STATO[g.stato_punto(p, 4.0, cls)]
    out["v2_ostacoli_nuovi_annotati"] = len(g.ostacoli_nuovi) > 0
    # (c) sfondo atteso e mancato (nan): raggio non certificato
    _, g = _griglia(m2, sfondo_atteso=att)
    mis_c = att.copy()
    mis_c[(az > -5) & (az < 5), 0] = np.nan
    for k in range(5):
        g.passata(float(k), sfondo_misurato=mis_c)
    out["v2_sfondo_mancante"] = m2.NOMI_STATO[g.stato_punto(p, 4.0, cls)]
    # (d) sfondo misurato come atteso: linea di vista certificata
    _, g = _griglia(m2, sfondo_atteso=att)
    for k in range(5):
        g.passata(float(k), sfondo_misurato=att)
    out["v2_sfondo_come_atteso"] = m2.NOMI_STATO[g.stato_punto(p, 4.0, cls)]
    ok = (out["v2_senza_certificazione"] != "libero" and out["v2_sfondo_piu_vicino"] == "in_ombra"
          and out["v2_sfondo_mancante"] != "libero" and out["v2_sfondo_come_atteso"] == "libero")
    esito("X5 edificio non in pianta", st1 == "libero", ok, out)


def prova_X6():
    out, ok = {}, True
    for sc, intruso, nome in (("strada", {"rcs_m2": 0.5, "v_max": 2.5}, "pedone"),
                              ("aeroporto_e_droni", {"rcs_m2": 1.6e-4, "v_max": 19.0}, "multirotore_C0")):
        cls = [R2["classi"][c] for c in R2["scenari"][sc]["classi_ammesse"]]
        _, g = _griglia(m2, r_max=12000.0, mappa_certificata=True)
        for k in range(5):
            g.passata(float(k))
        st = g.stati(4.0, cls)
        bad = (st == m2.LIBERO) & (g.pd_cumulata(4.0, intruso) < 0.99)
        i = np.argwhere(bad)
        if len(i) == 0:
            out[sc] = "nessuna cella libera non verificata per %s" % nome
            continue
        p = g.centri[tuple(i[0])]
        d = m2.dichiara_punto([g], p, 4.0, R2, sc)
        out[sc] = {"celle_libere_non_verificate_per_intruso": int(bad.sum()), "parola": d["parola"], "non_verificata": d["parola_non_verificata"]}
        ok &= d["stato"] == "libero" and nome in d["zona_non_verificata_per"] and d["parola"].startswith("libero per ")
    # v1: nessuna parola per le classi escluse (l'uscita dice solo 'libero')
    esito("X6 classi non ammesse", "classi_escluse" not in R1["scenari"]["strada"], ok, out)


def _inseguitore_con_traccia(mod, R, scen, g, s, p):
    ins = mod.Inseguitore(R, scen, [g])
    for t in (0.0, 1.0):
        g.passata(t, [p])
        ins.aggiorna([mod.Misura(t, p, 25.0 * np.eye(3), s.nome)])
    tr = ins.tracce[0]
    assert tr.confermata
    return ins, tr


def prova_validazione1():
    p = np.array([500.0, 0.0, 10.0])
    meta = None
    res = {}
    for nome, mod, R, scen, kw in (("v1", m1, R1, "aeroporto_e_droni", {}), ("v2", m2, R2, "sito_droni_rullaggio", {"mappa_certificata": True})):
        s, g = _griglia(mod, **kw)
        ins, tr = _inseguitore_con_traccia(mod, R, scen, g, s, p)
        meta = np.zeros(g.forma, bool)
        meta[:, g.az < 0, :] = True                     # guardata solo meta' dell'insieme (az < 0)
        g.passata(2.0, [], settore=meta)
        ins.mancato(2.0, s, tr.id)
        chiusa_meta = all(x.id != tr.id for x in ins.tracce)
        res[nome + "_chiusa_con_meta_guardata"] = chiusa_meta
        if not chiusa_meta:
            g.passata(3.0, [])
            ins.mancato(3.0, s, tr.id)
            res[nome + "_chiusa_con_tutto_guardato"] = all(x.id != tr.id for x in ins.tracce)
    esito("validazione-1 nel nucleo", res["v1_chiusa_con_meta_guardata"],
          (not res["v2_chiusa_con_meta_guardata"]) and res.get("v2_chiusa_con_tutto_guardato", False), res)


def prova_validazione2():
    par = dict(RADAR, sigma_az_rad=0.03)
    hover = [{"rcs_m2": 0.01, "v_max": 19.0}]
    p = np.array([500 * math.cos(math.radians(0.5)), 500 * math.sin(math.radians(0.5)), 10.0])
    q = np.array([500 * math.cos(math.radians(2.6)), 500 * math.sin(math.radians(2.6)), 10.0])   # ritorno a 2 celle
    st = {}
    for nome, mod, kw in (("v1", m1, {}), ("v2", m2, {"mappa_certificata": True})):
        _, g = _griglia(mod, par=par, **kw)
        for k in range(5):
            g.passata(float(k), [q])
        st[nome] = mod.NOMI_STATO[g.stato_punto(p, 4.0, hover)]
    # Doppler: radar con v_rad_min, bersaglio fermo
    pd_ = dict(RADAR, v_rad_min=0.3)
    s, g = _griglia(m2, par=pd_, mappa_certificata=True)
    for k in range(5):
        g.passata(float(k))
    lib_doppler = int((g.stati(4.0, hover) == m2.LIBERO).sum())
    s, g = _griglia(m2, par=pd_, mappa_certificata=True)
    ins, tr = _inseguitore_con_traccia(m2, R2, "sito_droni_rullaggio", g, s, np.array([500.0, 0, 10.0]))
    for t in (2.0, 3.0, 4.0):
        g.passata(t, [])
        ins.mancato(t, s, tr.id)
    chiusa = all(x.id != tr.id for x in ins.tracce)
    s1, g1 = _griglia(m1, par=pd_)
    for k in range(5):
        g1.passata(float(k))
    lib_doppler_v1 = int((g1.stati(4.0, hover) == m1.LIBERO).sum())
    esito("validazione-2 cella vicina e Doppler", st["v1"] == "libero" or lib_doppler_v1 > 0,
          st["v2"] != "libero" and lib_doppler == 0 and not chiusa,
          {"cella_oggetto_v1": st["v1"], "cella_oggetto_v2": st["v2"], "celle_libere_doppler_v1": lib_doppler_v1,
           "celle_libere_doppler_v2": lib_doppler, "traccia_chiusa_dal_doppler_v2": chiusa})


def prova_compat():
    """Un passaggio A1 'prudente' di prove_lp con v2 al posto del nucleo (regole v1 di prove_lp)."""
    sim = os.path.join(F15, "10-simulatore")
    sys.modules["movi_lp_import"] = types.SimpleNamespace(nucleo=m2)
    sys.path.insert(0, sim)
    import prove_lp as P
    t0 = time.perf_counter()
    R = P.passaggio("A1", "alta", 0, chiamante="prudente")
    esito("compatibilita' prove_lp A1 (1 passaggio)", False, True,
          {"s": round(time.perf_counter() - t0, 1), "chiavi": sorted(R)[:12]})


if __name__ == "__main__":
    t0 = time.perf_counter()
    for f in (prova_X1, prova_X3, prova_X4, prova_X5, prova_X6, prova_validazione1, prova_validazione2):
        f()
    if "--compat" in sys.argv:
        prova_compat()
    dur = time.perf_counter() - t0
    tutte = all(e["v2_regge"] for e in ESITI)
    print("tutte reggono:", tutte, " durata %.1f s" % dur)
    with open(os.path.join(QUI, "prove_v2_esito.json" if "--compat" not in sys.argv else "prove_v2_compat_esito.json"), "w", encoding="utf-8") as f:
        json.dump({"durata_s": round(dur, 1), "tutte_reggono": tutte, "esiti": ESITI}, f, ensure_ascii=False, indent=1, default=float)
    sys.exit(0 if tutte else 1)
