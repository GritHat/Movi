"""Prove a mano di movi_lp.py. Uso: python -I prove_movi_lp.py   (scrive risultati.json accanto).
Tutto simulato: sensori SEGNAPOSTO dal file delle regole, traiettorie generate. Semi fissi."""
import json
import math
import os
import sys
import time

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import movi_lp as m  # noqa: E402

t0 = time.time()
REG = m.carica_regole(os.path.join(QUI, "regole_lunga_portata.json"))
SP = REG["sensori_segnaposto"]
RIS, ESITI = {}, {}


def esito(pid, ok, nota):
    ESITI[pid] = {"esito": "regge" if ok else "SMENTITA", "nota": nota}
    print(("regge    " if ok else "SMENTITA ") + pid + ": " + nota)


# ---------------------------------------------------------------- P1-P3: celle e regola del libero
C01, C20 = {"rcs_m2": 0.01, "v_max": 19.0}, {"rcs_m2": 20.0, "v_max": 90.0}
CL = lambda sc: [REG["classi"][c] for c in REG["scenari"][sc]["classi_ammesse"]]  # noqa: E731
radar = m.Sensore("radar", [0, 0, 10], SP["radar_sorveglianza"])
hangar = ((1000.0, -200.0), (1000.0, 200.0), 30.0)
g = m.GrigliaPolare(radar, r_max=6000, dr=100, n_az=72, ostacoli=[hangar], t_cumulo=5.0)
prima = g.stati(0.0, C20)
for k in range(5):
    g.passata(float(k), rilevamenti=[[2000.0, 2000.0, 10.0]])
p4km = [0.0, 4050.0, 10.0]
s_piccolo, s_grande = g.stato_punto(p4km, 4.0, C01), g.stato_punto(p4km, 4.0, C20)
esito("P1", s_piccolo == m.NON_OSSERVATO and s_grande == m.LIBERO,
      "cella a 4 km in vista dopo 5 passate: per 0,01 m2 '%s', per 20 m2 '%s'" % (m.NOMI_STATO[s_piccolo], m.NOMI_STATO[s_grande]))
r5, r1 = radar.portata(0.01, 0.99, 5), radar.portata(0.01, 0.99, 1)
st = g.stati(4.0, C01)
r_gr = float(g.r[np.where((st == m.LIBERO).any(axis=(1, 2)))[0].max()] + g.dr / 2)
esito("P2", abs(r5 / 2360 - 1) < 0.05 and abs(r1 / 877 - 1) < 0.05 and -2 * g.dr <= r_gr - r5 <= 0,
      "portata del 'libero' per 0,01 m2: 5 passate %.0f m (a mano 2360), 1 passata %.0f m (a mano 877); dalla griglia %.0f m" % (r5, r1, r_gr))
scad = g.stati(4.0 + 5.01, C20)
n_viol = int((prima == m.LIBERO).sum() + (st[g.ombra] == m.LIBERO).sum() + (g.stati(4.0, C20)[g.ombra] == m.LIBERO).sum() + (scad == m.LIBERO).sum())
occ = g.stato_punto([2000.0, 2000.0, 10.0], 4.0, C20)
omb = g.stato_punto([3000.0, 0.0, 10.0], 4.0, C20)
scen = g.stati(4.0, CL('aeroporto_e_droni'))
RIS['celle_scenario_aeroporto'] = {m.NOMI_STATO[k]: int((scen == k).sum()) for k in range(4)}
assert ((scen == m.LIBERO) <= (st == m.LIBERO)).all() and ((scen == m.LIBERO) <= (g.stati(4.0, C20) == m.LIBERO)).all()
g2 = m.GrigliaPolare(radar, r_max=6000, dr=100, n_az=72, t_cumulo=5.0)
g2.passata(0.0)
dopo_ok = g2.stato_punto([1500.0, 0.0, 10.0], 0.5, C20, dopo=0.2) == m.NON_OSSERVATO and g2.stato_punto([1500.0, 0.0, 10.0], 0.5, C20) == m.LIBERO
esito("P3", n_viol == 0 and occ == m.OCCUPATO and omb == m.IN_OMBRA and dopo_ok,
      "celle 'libere' senza diritto: %d su %d (mai illuminate, in ombra %d, scadute); ritorno -> '%s'; dietro l'hangar -> '%s'; passate prima della perdita non contano: %s"
      % (n_viol, 3 * prima.size, int(g.ombra.sum()), m.NOMI_STATO[occ], m.NOMI_STATO[omb], dopo_ok))
# fusione di due sensori: nessuno basta da solo, insieme si'
ra, rb = m.Sensore("ra", [0, 0, 10], SP["radar_sorveglianza"]), m.Sensore("rb", [0, 100, 10], SP["radar_sorveglianza"])
ga, gb = (m.GrigliaPolare(s, 6000, 100, 72, n_passate_max=3) for s in (ra, rb))
for k in range(3):
    ga.passata(float(k)), gb.passata(float(k))
pt = [2250.0, 50.0, 10.0]
RIS["fusione_celle"] = {"solo_a": m.NOMI_STATO[ga.stato_punto(pt, 2.0, C01)], "solo_b": m.NOMI_STATO[gb.stato_punto(pt, 2.0, C01)],
                        "insieme": m.NOMI_STATO[m.stato_fuso([ga, gb], pt, 2.0, C01)]}
assert RIS["fusione_celle"] == {"solo_a": "non_osservato", "solo_b": "non_osservato", "insieme": "libero"}, RIS["fusione_celle"]


# ---------------------------------------------------------------- P4-P5: inseguitore a piu' sensori
def volo(T, dt, p0, v0, virate=()):
    """Verita': velocita' costante con virate coordinate (t_ini, t_fin, omega)."""
    n = int(round(T / dt)) + 1
    P, V = np.zeros((n, 3)), np.zeros((n, 3))
    P[0], V[0] = p0, v0
    for i in range(1, n):
        t = (i - 1) * dt
        om = sum(w for (a, b, w) in virate if a <= t < b)
        c, s = math.cos(om * dt), math.sin(om * dt)
        V[i] = [c * V[i - 1, 0] - s * V[i - 1, 1], s * V[i - 1, 0] + c * V[i - 1, 1], V[i - 1, 2]]
        P[i] = P[i - 1] + 0.5 * (V[i - 1] + V[i]) * dt
    return P, V


def misure_di(sens, classe, veri, rcs, T, dt, rng, coop_fino=None, usa=("radar", "ottico", "coop")):
    out = []
    n = int(round(T / dt)) + 1
    for i in range(n):
        t = round(i * dt, 6)
        for nome, s in sens.items():
            if nome not in usa:
                continue
            per = s.par["periodo_s"] if nome != "coop" else SP["cooperativa"]["periodo_s"]
            if abs(t / per - round(t / per)) > 1e-6:
                continue
            for k, (P, V) in enumerate(veri):
                if nome == "coop":
                    if k != 0 or (coop_fino is not None and t > coop_fino):
                        continue
                    sp, sv = SP["cooperativa"]["sigma_pos_m"], SP["cooperativa"]["sigma_vel_ms"]
                    out.append(m.Misura(t, P[i] + sp * rng.standard_normal(3), sp ** 2 * np.eye(3), "coop", classe,
                                        vel=V[i] + sv * rng.standard_normal(3), R_vel=sv ** 2 * np.eye(3), id_coop="ICAO-A"))
                elif rng.random() < float(s.pd(np.linalg.norm(P[i] - s.pos), rcs)):
                    z, R = s.misura(P[i], rng)
                    out.append(m.Misura(t, z, R, nome, classe))
    return out


def segui(ms, veri, T, dt, scenario="aeroporto_e_droni"):
    ins = m.Inseguitore(REG, scenario)
    n = int(round(T / dt)) + 1
    per_t = {}
    for x in ms:
        per_t.setdefault(x.t, []).append(x)
    err, ids = [], [[] for _ in veri]
    for i in range(n):
        t = round(i * dt, 6)
        if t in per_t:
            ins.aggiorna(per_t[t])
        conf = [tr for tr in ins.tracce if tr.confermata]
        if abs(t - round(t)) < 1e-6 and t >= 10 and conf:
            for k, (P, V) in enumerate(veri):
                d = []
                for tr in conf:
                    x = tr.x[:3] + tr.x[3:] * (t - tr.t)
                    d.append(np.linalg.norm(x - P[i]))
                j = int(np.argmin(d))
                ids[k].append(conf[j].id)
                if k == 0:
                    err.append(d[j])
    scambi = sum(sum(1 for a, b in zip(s[:-1], s[1:]) if a != b) for s in ids)
    return math.sqrt(float(np.mean(np.square(err)))), scambi, ins


T, DT = 60.0, 0.1
sens = {"radar": radar, "ottico": m.Sensore("ottico", [0, 500, 5], SP["ottico_ir"])}
sens["coop"] = None
sens = {k: v for k, v in sens.items() if v is not None}
sens_c = dict(sens, coop=m.Sensore("coop", [0, 0, 0], dict(SP["radar_sorveglianza"], tipo="cooperativa", periodo_s=0.5)))
om = 4.6 / 70.0
vero = volo(T, DT, [6000.0, -1500.0, 600.0], [-70.0, 0.0, -3.0], virate=[(20.0, 35.0, om)])
rm_r, rm_f, sc_tot, n_tracce = [], [], 0, []
SEMI4 = list(range(20)) + list(range(1000, 1020))      # 0-19: quelli della previsione; 1000-1019: nuovi, dopo la correzione
for seme in SEMI4:
    e_r, _, _ = segui(misure_di(sens_c, "aereo_linea_avvicinamento", [vero], 20.0, T, DT, np.random.default_rng(seme), usa=("radar",)), [vero], T, DT)
    e_f, sc, ins = segui(misure_di(sens_c, "aereo_linea_avvicinamento", [vero], 20.0, T, DT, np.random.default_rng(seme), coop_fino=30.0), [vero], T, DT)
    rm_r.append(e_r), rm_f.append(e_f)
    sc_tot += sc
    n_tracce.append(sum(tr.confermata for tr in ins.tracce))
RIS["P4"] = {"rmse_solo_radar_m": [round(float(np.mean(rm_r)), 1), round(float(np.max(rm_r)), 1)], "rmse_fuso_m": [round(float(np.mean(rm_f)), 1), round(float(np.max(rm_f)), 1)],
             "semi_fuso_migliore": int(sum(f < r for f, r in zip(rm_f, rm_r))), "n_semi": len(SEMI4), "cambi_identita": sc_tot, "tracce_confermate_per_seme": sorted(set(n_tracce))}
esito("P4", RIS["P4"]["semi_fuso_migliore"] == len(SEMI4) and sc_tot == 0 and set(n_tracce) == {1},
      "RMSE medio (max) su 40 semi: solo radar %.1f (%.1f) m, fuso %.1f (%.1f) m; fuso migliore in %d semi su 40; cambi d'identita' con la cooperativa spenta a 30 s: %d; tracce confermate: %s"
      % (*RIS["P4"]["rmse_solo_radar_m"], *RIS["P4"]["rmse_fuso_m"], RIS["P4"]["semi_fuso_migliore"], sc_tot, sorted(set(n_tracce))))

a = volo(T, DT, [3000.0, -1200.0, 300.0], [0.0, 40.0, 0.0])
b = volo(T, DT, [1800.0, 0.0, 400.0], [40.0, 0.0, 0.0])
sc5, semi_sc = 0, 0
for seme in list(range(20)) + list(range(2000, 2020)):
    _, sc, _ = segui(misure_di(sens, None, [a, b], 2.0, T, DT, np.random.default_rng(100 + seme), usa=("radar", "ottico")), [a, b], T, DT)
    sc5 += sc
    semi_sc += sc > 0
lo, hi = m.wilson(semi_sc, 40)
RIS["P5"] = {"scambi": sc5, "semi_con_scambio": semi_sc, "n": 40, "wilson95": [round(lo, 3), round(hi, 3)]}
ESITI["P5"] = {"esito": "regge" if sc5 == 0 else ("non risolta" if sc5 == 1 else "SMENTITA"), "nota": "incrocio a 100 m di quota di separazione, radar + ottico, senza etichetta: %d scambi, %d semi su 40 con scambio (Wilson 95 %%: %.3f-%.3f)" % (sc5, semi_sc, lo, hi)}
print(ESITI["P5"]["esito"].ljust(9) + "P5: " + ESITI["P5"]["nota"])

# ---------------------------------------------------------------- P6: insieme raggiungibile
TAU = [5.0, 10.0, 30.0]
fuori, tot, cresc = 0, 0, {}
for nome, cfg in REG["classi"].items():
    cresc[nome] = {"da_fermo_m": [round(float(m.raggio_raggiungibile(t, 0.0, cfg["v_max"], cfg["a_max"]))) for t in TAU],
                   "da_v_max_m": [round(float(m.raggio_raggiungibile(t, cfg["v_max"], cfg["v_max"], cfg["a_max"]))) for t in TAU]}
    rng = np.random.default_rng(7)
    if cfg["vincolo"] == "binario":
        for _ in range(2000):
            v, s, dt, acc, resta = rng.uniform(0, cfg["v_max"]), 0.0, 0.1, 0.0, 0.0
            v0 = v
            for i in range(1, 301):
                if resta <= 0:
                    acc, resta = rng.uniform(-cfg["dec_max"], cfg["a_max"]), rng.exponential(5.0)
                    if rng.random() < 0.3:
                        acc = -cfg["dec_max"]
                resta -= dt
                a_eff = acc if v > 0 or acc > 0 else max(acc, -cfg["dec_max"])
                vn = float(np.clip(v + a_eff * dt, -cfg["v_retro_max"], cfg["v_max"]))
                s += 0.5 * (v + vn) * dt
                v = vn
                if i in (50, 100, 300):
                    lo_, hi_ = m.intervallo_binario(i * dt, v0, cfg)
                    tot += 1
                    fuori += not (lo_ - 1e-6 <= s <= hi_ + 1e-6)
        cresc[nome]["binario_da_v_max_m"] = [[round(x) for x in m.intervallo_binario(t, cfg["v_max"], cfg)] for t in TAU]
    else:
        P, V = m.genera_traiettorie(cfg, rng, 2000, piano=cfg["vincolo"] != "libero_3d")
        for k in range(2000):
            for t in TAU:
                tot += 1
                fuori += np.linalg.norm(P[k, int(round(t / 0.1))]) > float(m.raggio_raggiungibile(t, np.linalg.norm(V[k, 0]), cfg["v_max"], cfg["a_max"])) + 1e-6
RIS["crescita_insieme"] = cresc
esito("P6", fuori == 0, "traiettorie simulate fuori dall'insieme raggiungibile a 5, 10, 30 s: %d su %d (10 classi x 2000 x 3)" % (fuori, tot))

# ---------------------------------------------------------------- P7: regione di previsione
ORZ = REG["previsione"]["orizzonti_s"]
LIV = REG["previsione"]["livello"]
tab, peggiore, REGIONI = {}, 1.0, {}
for nome, cfg in REG["classi"].items():
    if cfg["vincolo"] == "binario":
        continue
    rng = np.random.default_rng(11)
    P, V = m.genera_traiettorie(cfg, rng, 4000, piano=cfg["vincolo"] != "libero_3d")
    E = np.stack([np.linalg.norm(P[:, int(round(t / 0.1))] - V[:, 0] * t, axis=1) for t in ORZ], 1)
    raggi = [m.tara_regione(E[:2000, j], LIV) for j in range(len(ORZ))]
    REGIONI[nome] = m.RegionePrevisione(ORZ, raggi, LIV)
    riga = {"raggio_m": [round(r, 1) for r in raggi], "copertura_prova": [], "wilson_inf": [],
            "raggio_su_raggiungibile_da_v_tip": []}
    for j, t in enumerate(ORZ):
        kk = int((E[2000:, j] <= raggi[j]).sum())
        lo_, _ = m.wilson(kk, 2000)
        riga["copertura_prova"].append(round(kk / 2000, 4))
        riga["wilson_inf"].append(round(lo_, 4))
        peggiore = min(peggiore, lo_)
        riga["raggio_su_raggiungibile_da_v_tip"].append(round(raggi[j] / float(m.raggio_raggiungibile(t, 0.6 * cfg["v_max"], cfg["v_max"], cfg["a_max"])), 3))
    tab[nome] = riga
RIS["regione_previsione"] = {"orizzonti_s": ORZ, "livello": LIV, "n_taratura": 2000, "n_prova": 2000, "classi": tab}
esito("P7", peggiore >= 0.87, "copertura sulla prova (n=2000 per cella, %d celle): limite inferiore di Wilson peggiore %.4f (soglia 0,87)" % (len(tab) * len(ORZ), peggiore))

# ---------------------------------------------------------------- P8: nessuna etichetta riduce l'avviso
viol, casi = 0, 0
for sc, d in REG["scenari"].items():
    inv = m.inviluppo(REG, d["classi_ammesse"])
    for c in d["classi_ammesse"]:
        cfg = REG["classi"][c]
        for v0 in np.linspace(0, inv["v_max"], 21):
            tau = np.arange(0, 60.01, 0.5)
            r_inv = m.raggio_raggiungibile(tau, v0, inv["v_max"], inv["a_max"])
            r_c = m.raggio_raggiungibile(tau, min(v0, cfg["v_max"]), cfg["v_max"], cfg["a_max"])
            casi += tau.size
            viol += int((r_c > r_inv + 1e-9).sum())
esito("P8", viol == 0, "casi in cui il raggio della classe supera quello dell'inviluppo: %d su %d" % (viol, casi))

# ---------------------------------------------------------------- uscite e vita delle tracce (controlli, non previsioni)
gr = m.GrigliaPolare(radar, r_max=6000, dr=100, n_az=72, ostacoli=[hangar], t_cumulo=5.0)
ins = m.Inseguitore(REG, "aeroporto_e_droni", [gr])
rng = np.random.default_rng(3)
parole = []
for k in range(60):                                   # multirotore che va dietro l'hangar a 15 m/s
    t = float(k)
    p = np.array([700.0 + 15.0 * t, -100.0, 20.0])
    in_vista = not gr.ombra[gr.indice(p)]
    if in_vista:
        z, R = radar.misura(p, rng)
        ins.aggiorna([m.Misura(t, z, R, "radar", "multirotore_piccolo")])
    elif ins.tracce:
        ins.mancato(t, radar, ins.tracce[0].id)
    gr.passata(t, [p] if in_vista else [])
    u = ins.uscite(t, REGIONI)
    parole.append(u[0]["parola"] if u else "-")
seq = [parole[0]] + [b for a, b in zip(parole[:-1], parole[1:]) if a.split(" da ")[0] != b.split(" da ")[0]]
u = ins.uscite(59.0, REGIONI)[0]
sp_ok, fr = m.avviso_spegnibile([gr], u["possibile_presenza"], 59.0, CL("aeroporto_e_droni"))
RIS["uscite"] = {"sequenza_parole": seq, "tracce_vive": len(ins.tracce), "chiuse": len(ins.chiuse),
                 "raggio_possibile_presenza_m": round(u["possibile_presenza"]["raggio"]), "avviso_spegnibile": sp_ok, "frazione_guardata_libera": round(fr, 3)}
assert seq[0] in ("-", "vista") and "previsto ampio" in seq and seq.index("previsto ampio") == len(seq) - 1, seq
assert any(s.startswith("non vista da") for s in seq), seq
assert len(ins.tracce) == 1 and not ins.chiuse and not sp_ok
# in vista, senza piu' ritorni e con Pd alta: 'non piu' rilevata'; il silenzio della cooperativa non chiude
ins2 = m.Inseguitore(REG, "aeroporto_e_droni", [m.GrigliaPolare(radar, 6000, 100, 72)])
for k in range(4):
    z, R = radar.misura([500.0, 500.0 + 10 * k, 30.0], rng)
    ins2.aggiorna([m.Misura(float(k), z, R, "radar", "multirotore_piccolo")])
coop = m.Sensore("coop", [0, 0, 0], dict(SP["radar_sorveglianza"], tipo="cooperativa"))
for k in range(4, 10):
    ins2.mancato(float(k), coop, 1)
vive_dopo_coop = len(ins2.tracce)
kk = 4
while ins2.tracce and kk < 20:
    ins2.mancato(float(kk), radar, 1)
    kk += 1
RIS["chiusura"] = {"vive_dopo_6_silenzi_cooperativi": vive_dopo_coop, "passate_radar_in_vista_per_chiudere": kk - 4, "evento": ins2.eventi[-1][1] if ins2.eventi else None}
assert vive_dopo_coop == 1 and not ins2.tracce and ins2.eventi[-1][1] == "non piu' rilevata"
# affidabilita' persa: griglia tutta non osservata, traccia 'previsto ampio'
ins3 = m.Inseguitore(REG, "aeroporto_e_droni", [m.GrigliaPolare(radar, 6000, 100, 72)])
for k in range(4):
    z, R = radar.misura([500.0, 500.0 + 10 * k, 30.0], rng)
    ins3.aggiorna([m.Misura(float(k), z, R, "radar", "multirotore_piccolo")])
    ins3.griglie[0].passata(float(k))
ins3.affidabilita_persa(4.0, radar)
assert (ins3.griglie[0].stati(4.0, C20) == m.NON_OSSERVATO).all() and ins3.uscite(4.0, REGIONI)[0]["parola"] == "previsto ampio"
z, R = radar.misura([500.0, 540.0, 30.0], rng)
ins3.griglie[0].ripristina()
ins3.aggiorna([m.Misura(5.0, z, R, "radar", "multirotore_piccolo")])
ins3.mancato(8.0, coop, 1)
RIS["affidabilita"] = {"dopo_la_perdita": "previsto ampio", "rivista": ins3.uscite(5.0, REGIONI)[0]["parola"], "persa_di_nuovo": ins3.uscite(9.0, REGIONI)[0]["parola"]}
assert RIS["affidabilita"]["rivista"] == "vista" and RIS["affidabilita"]["persa_di_nuovo"] == "previsto ampio", RIS["affidabilita"]
print("controlli sulle uscite: passati —", json.dumps(RIS["uscite"], ensure_ascii=False))

# ---------------------------------------------------------------- avviso tempestivo (conto)
avv, DR, PER = {}, 100.0, SP["radar_sorveglianza"]["periodo_s"]


def n_passate(cfg):
    """Passate cumulabili per la classe con celle da DR metri: finestra min(t_cumulo, DR / v_max)."""
    W = min(REG["libero"]["t_cumulo_max_s"], DR / cfg["v_max"])
    return max(1, min(REG["libero"]["n_passate_max"], int(W / PER + 1e-9) + 1))


PORT = {c: {"n_passate": n_passate(cfg), "portata_libero_m": round(radar.portata(cfg["rcs_m2"], 0.99, n_passate(cfg)))} for c, cfg in REG["classi"].items()}
for sc, d in REG["scenari"].items():
    inv = m.inviluppo(REG, d["classi_ammesse"])
    lim = min(d["classi_ammesse"], key=lambda c: PORT[c]["portata_libero_m"])
    avv[sc] = {"v_max_inviluppo": inv["v_max"], "classe_che_limita": lim, "portata_libero_radar_segnaposto_m": PORT[lim]["portata_libero_m"],
               "d_avviso_m": {p: round(m.distanza_avviso(REG, d["classi_ammesse"], p)) for p in REG["avviso"]["profili_ricevente"]}}
    avv[sc]["tempestivo"] = {p: avv[sc]["portata_libero_radar_segnaposto_m"] >= dd for p, dd in avv[sc]["d_avviso_m"].items()}
RIS["avviso"] = avv
RIS["portata_libero_radar_segnaposto_celle_100m"] = PORT

dur = time.time() - t0
esito("P9", dur < 20, "durata delle prove %.1f s" % dur)
RIS["esiti"] = ESITI
with open(os.path.join(QUI, "risultati.json"), "w", encoding="utf-8") as f:
    json.dump(RIS, f, ensure_ascii=False, indent=1)
sys.exit(0 if all(e["esito"] == "regge" for e in ESITI.values()) else 1)
