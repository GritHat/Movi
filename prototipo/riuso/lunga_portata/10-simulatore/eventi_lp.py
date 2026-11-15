"""eventi_lp.py - scenari d'incidente E1-E5 (40-eventi/02-regole/scenari_eventi.json) sul simulatore e sul nucleo.

Uso: python -I -B eventi_lp.py [n] [processi]. Scrive ../11-prove/risultati_eventi.json ed esemplari/E*_0.json.
Lo strato degli eventi (innesco, volume V, impronta, regola della salute) e' scritto QUI dalle regole di
regole_eventi.json, perche' il nucleo movi_lp.py non lo contiene: e' una realizzazione mia di quelle regole, non
la loro prova indipendente (stesso autore della prova). Il volume V e l'impronta usano frammenti.py di 02-regole.
Tutto e' simulazione: nessuna prova su un sensore fisico. Solo osservazione e avviso.
"""
import json
import math
import os
import sys
import time

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import numpy as np  # noqa: E402

import sim_lp as S  # noqa: E402
from movi_lp_import import nucleo as m  # noqa: E402

F15 = os.path.dirname(QUI)
sys.path.insert(0, os.path.join(F15, "40-eventi", "02-regole"))
import frammenti as FR  # noqa: E402

REG = m.carica_regole(os.path.join(F15, "04-moto", "regole_lunga_portata.json"))
RE = json.load(open(os.path.join(F15, "40-eventi", "02-regole", "regole_eventi.json"), encoding="utf-8"))
SE = {s["id"]: s for s in json.load(open(os.path.join(F15, "40-eventi", "02-regole", "scenari_eventi.json"), encoding="utf-8"))["scenari"]}
EFF = json.load(open(os.path.join(F15, "40-eventi", "01-effetti", "effetti_eventi.json"), encoding="utf-8"))["effetti"]
CAT = S.catalogo()
FRAM = RE["EV-A_frammentazione"]
INV = FRAM["inviluppo"]
PAR_COLL = dict(INV["collisione_multirotori"]["prudente"], k_tc=FRAM["k_tc"], r_rimbalzo=FRAM["r_rimbalzo_m"])
PAR_AVAR = dict(INV["avaria_motore_a_terra"]["prudente"], k_tc=FRAM["k_tc"], r_rimbalzo=FRAM["r_rimbalzo_m"])
RCS_FR = RE["EV-A_frammentazione"]["frammento_minimo_ammesso"]["rcs_m2"]
CLASSE = {"multirotore": "multirotore_piccolo", "aereo_rullaggio": "aereo_rullaggio", "aereo_leggero": "aereo_leggero",
          "mezzo_piazzale": None, "persona_a_piedi": None, "frammento": None}
RCS = {"multirotore": 0.01, "aereo_rullaggio": 20.0, "aereo_leggero": 2.0, "mezzo_piazzale": 10.0, "persona_a_piedi": 0.5, "frammento": RCS_FR}
G = 9.81


def fattore(cond, tipo, quale):
    """Fattore di portata da 01-effetti: quale = 0 nominale, 1 prudente."""
    if cond is None:
        return 1.0
    ps = EFF[cond].get("per_sensore", {})
    if tipo not in ps:
        return 1.0
    return float(ps[tipo]["fattore_portata"][0][quale])


def frammenti(ev, rng, dt=0.05):
    """Frammenti puntiformi: v0 = v_c + u (|u| <= dv_max), resistenza quadratica con v_t, vento costante."""
    p0 = np.asarray(ev["p"], float)
    vc = np.asarray(ev.get("vc", [0, 0, 0]), float)
    w = np.asarray(ev.get("vento", [0, 0, 0]), float)
    out = []
    for _ in range(ev["n_frammenti"]):
        u = rng.standard_normal(3)
        u = u / np.linalg.norm(u) * ev["dv_max_m_s"] * rng.random() ** (1 / 3)
        vt = math.exp(rng.uniform(math.log(ev["v_t_m_s"][0]), math.log(ev["v_t_m_s"][1])))
        p, v, T, P = p0.copy(), vc + u, [0.0], [p0.copy()]
        t = 0.0
        while t < 60.0:
            va = v - w
            a = np.array([0, 0, -G]) - G / vt ** 2 * np.linalg.norm(va) * va
            v = v + a * dt
            p = p + v * dt
            t += dt
            if p[2] <= 0:
                p[2] = 0.0
                v = np.zeros(3)
            T.append(t)
            P.append(p.copy())
        out.append((np.array(T), np.array(P), vt, float(np.linalg.norm(u))))
    return out


def unisci_non_risolti(rc, ver, par):
    """Due ritorni nella stessa cella di risoluzione (2 sigma in distanza e in angolo) diventano UNO (centroide)."""
    ril = rc["ril"]
    if len(ril) < 2 or par["tipo"] not in ("radar",):
        return rc
    usati, nuovi = set(), []
    for i in range(len(ril)):
        if i in usati:
            continue
        gruppo = [i]
        for j in range(i + 1, len(ril)):
            if j in usati or "pol" not in ril[i][3] or "pol" not in ril[j][3]:
                continue
            a, b = ril[i][3]["pol"], ril[j][3]["pol"]
            if abs(a[0] - b[0]) < 2 * par["sigma_r_m"] and abs(a[1] - b[1]) < 2 * par["sigma_az_rad"] and abs(a[2] - b[2]) < 2 * par["sigma_el_rad"]:
                gruppo.append(j)
        usati.update(gruppo)
        if len(gruppo) == 1:
            nuovi.append(ril[i])
        else:
            z = np.mean([ril[k][1] for k in gruppo], 0)
            nuovi.append((ril[gruppo[0]][0], z, ril[gruppo[0]][2], dict(ril[gruppo[0]][3], unito=len(gruppo))))
    rc = dict(rc, ril=nuovi)
    return rc


def passaggio(eid, cfg, idx, sep=None, esemplare=False):
    sc = SE[eid]
    ss_v = np.random.SeedSequence(20261115, spawn_key=(100 + int(eid[1]), 0, idx, int(1000 * (sep or 0))))
    ss_s = np.random.SeedSequence(20261115, spawn_key=(100 + int(eid[1]), 1 + ("min", "alta").index(cfg), idx, int(1000 * (sep or 0))))
    rv, rs = np.random.default_rng(ss_v), np.random.default_rng(ss_s)
    variante = "abc"[idx % 3] if eid == "E3" else None
    ogg = {o["id"]: dict(o) for o in sc["oggetti"]}
    if eid == "E3":
        ogg = {k: v for k, v in ogg.items() if (k == "leggero1") == (variante in "ac")}
    if eid == "E5" and sep is not None:
        for q in ogg["droneB"]["punti"]:
            q[2] = 80 + sep
    eventi = sc.get("eventi", [])
    meteo = None
    for e in eventi:
        if e["tipo"] == "meteo":
            meteo = e["parametri"]["variante_b" if variante == "b" else "variante_a"]
    t_fine = {"E1": 45.0, "E2": 70.0, "E3": 160.0, "E4": 50.0, "E5": 45.0}[eid]
    ver = {}
    for k, o in ogg.items():
        ver[k] = S.genera_verita(o, "nominale", 1.0, rv, t_fine=t_fine)
    # collisione o avaria: frammenti (oggetti in piu' nella verita'), drone B balistico dopo l'evento
    t_ev, frs = None, []
    for e in eventi:
        if e["tipo"] in ("collisione", "avaria_motore"):
            t_ev = e["t"]
            pe = dict(e["parametri"])
            src = pe["oggetti"] if "oggetti" in pe else [pe["oggetto"]]
            i_ev = int(round(t_ev / 0.1))
            pe["vc"] = np.mean([ver[s][2][i_ev] for s in src], 0)
            frs = frammenti(pe, rv)
            for j, (T, P, vt, un) in enumerate(frs):
                Tf = np.arange(0, t_fine + 0.05, 0.1)
                Pf = np.full((len(Tf), 3), np.nan)
                Pi = np.stack([np.interp(Tf - t_ev, T, P[:, c]) for c in range(3)], 1)
                Pf[Tf >= t_ev] = Pi[Tf >= t_ev]
                Pf[Tf < t_ev] = np.asarray(pe["p"], float)
                Vf = np.gradient(Pf, 0.1, axis=0)
                ver["fr%02d" % j] = (Tf, Pf, Vf)
                ogg["fr%02d" % j] = {"classe": "frammento", "ingombro": [0.05], "t0": t_ev}
            if eid == "E1":                                   # B: caduta balistica dopo l'urto
                T, P, V = ver["droneB"]
                i0 = int(round(t_ev / 0.1))
                for i in range(i0 + 1, len(T)):
                    va = V[i - 1]
                    vt = 15.0
                    a = np.array([0, 0, -G]) - G / vt ** 2 * np.linalg.norm(va) * va
                    V[i] = V[i - 1] + a * 0.1 if P[i - 1, 2] > 0 else 0 * V[i - 1]
                    P[i] = np.maximum(P[i - 1] + V[i] * 0.1, [-1e9, -1e9, 0])
    nubi = []
    for n in sc.get("nubi", []) or []:
        fpos = None
        if "centro_segue" in n:
            T, P, _ = ver["aereo1"]
            fpos = (lambda t, T=T, P=P: P[min(int(round(t / 0.1)), len(T) - 1)])
        nubi.append((n, fpos))
    salute_cam = {}
    for e in eventi:
        if e["tipo"] == "fiammata":
            p = e["parametri"]
            salute_cam = {"camera_eo_ottica_lunga": (e["t"], p["cieca_eo_fino_a_t"]), "camera_termica_ottica_lunga": (e["t"], p["cieca_termica_fino_a_t"])}
    lista = sc["sensori"]
    if cfg == "min":
        radar = [s for s in lista if CAT[s["tipo"]]["tipo"] == "radar"]
        lista = radar[:1] if (radar and eid != "E4") else [s for s in lista if CAT[s["tipo"]]["tipo"] == "camera"]
    else:
        lista = [s for s in lista if not (eid == "E4" and False)]
    sensori, griglie, nuc = [], [], {}
    for i, sd in enumerate(lista):
        par = dict(CAT[sd["tipo"]])
        nome = "%s#%d" % (sd["tipo"], i)
        sal = []
        if sd["tipo"] in salute_cam:
            sal.append((salute_cam[sd["tipo"]][0], salute_cam[sd["tipo"]][1], "abbagliamento"))
        for e in eventi:
            if e["tipo"] == "sensore_non_affidabile" and variante == "c" and sd["id"] == e["parametri"]["sensore"]:
                sal.append((e["t"], e["t"] + e["parametri"]["durata_s"], "spento"))
        s = S.SensoreSim(nome, sd["pos"], par, meteo=fattore(meteo, sd["tipo"], 0), ostacoli=[], nubi=nubi, salute=sal)
        sensori.append(s)
        if par["tipo"] in ("radar", "lidar"):
            pg = S.scala_meteo(par, fattore(meteo, sd["tipo"], 1))
            r_max = min(pg["r_max_m"], 6000.0 if eid == "E3" else 1500.0)
            sn = m.Sensore(nome, sd["pos"], pg)
            el = (0.0,) if par.get("due_d") else tuple(np.radians(np.linspace(-2, 20 if eid != "E3" else 10, 6)))
            g = m.GrigliaPolare(sn, r_max, r_max / 80.0, 180, el=el, t_cumulo=5.0, n_passate_max=5, pd_cum_min=0.99)
            griglie.append(g)
            nuc[nome] = (sn, g, pg)

    def rcs(oid, tipo):
        o = ogg[oid]
        return max(o["ingombro"]) if tipo == "camera" else RCS[o["classe"]]

    def coop(oid, t):
        return False                                          # E1-E5: nessun mezzo coopera (scenari_eventi.json)

    recs, radar_ril = [], {}
    for s in sensori:
        if s.tipo == "camera":
            continue
        r = s.scansioni(ver, t_fine, rs, rcs, coop_stato=coop)
        if s.tipo == "radar":
            r = [unisci_non_risolti(rc, ver, s.par) for rc in r]
            for rc in r:
                for (oid, *_x) in rc["ril"]:
                    if oid is not None:
                        radar_ril.setdefault(oid, []).append(rc["t"])
        recs += r
    for s in sensori:
        if s.tipo == "camera":
            tt = {k: np.array(sorted(v)) for k, v in radar_ril.items()}
            senza_radar = not any(x.tipo == "radar" for x in sensori)
            recs += s.scansioni(ver, t_fine, rs, rcs, cue=(None if senza_radar else (lambda oid, t: oid in tt and np.any((tt[oid] <= t) & (tt[oid] >= t - 5.0)))))
    recs.sort(key=lambda r: (r["t_consegna"], r["sensore"]))
    fam = "aeroporto_e_droni"
    ins = m.Inseguitore(REG, fam, griglie)
    classi_d = [REG["classi"][c] for c in REG["scenari"][fam]["classi_ammesse"]]
    per = {s.nome: s.par["periodo_s"] for s in sensori}
    cattivi, dichiarato, ritardo_cicli = {s.nome: 0 for s in sensori}, {}, {}
    ultimo = {s.nome: 0.0 for s in sensori}
    evento, cand, nuovi = None, None, []
    R = {"variante": variante, "sep": sep, "seme": list(ss_s.spawn_key), "meteo": meteo}
    persi, nasc_tot, fuori_av = 0, 0, 0
    lib_imp, lib_imp_tot, dentro_V, tot_V = 0, 0, 0, 0
    lib_oltre, lib_oltre_tot, lib_ogg, lib_ogg_tot = 0, 0, 0, 0
    assoc = {}
    log = [] if esemplare else None
    ir = 0
    principali = [k for k in ogg if ogg[k]["classe"] != "frammento"]
    for tk in np.arange(0.5, t_fine, 0.5):
        while ir < len(recs) and recs[ir]["t_consegna"] <= tk:
            rc = recs[ir]
            ir += 1
            nm = rc["sensore"]
            ultimo[nm] = rc["t_consegna"]
            if rc["salute"]["saturi"] > 0.05 or rc["salute"]["fondo_db"] > 6:
                cattivi[nm] += 1
                if cattivi[nm] >= 3 and nm not in dichiarato:
                    dichiarato[nm] = rc["t_consegna"]
                    ritardo_cicli[nm] = cattivi[nm]
                    if nm in nuc:
                        ins.affidabilita_persa(rc["t_consegna"], nuc[nm][0])
                continue                                       # quadro saturo: non e' un'osservazione
            cattivi[nm] = 0
            ms = [m.Misura(ex["t_ril"], z, Rm, nm, CLASSE.get(ogg[oid]["classe"]) if oid else None) for (oid, z, Rm, ex) in rc["ril"]]
            if nm in nuc and nm not in dichiarato:
                tp = rc["t"] - per[nm] if nuc[nm][2].get("rotante") else rc["t"]
                nuc[nm][1].passata(tp, [x.z for x in ms])
            conf = [tr for tr in ins.tracce if tr.confermata]
            # ---- innesco degli eventi (EV-A): ritorni nuovi lontani dalle tracce, vicino a una coppia o a una traccia
            for x in ms:
                lontano = all(np.linalg.norm(x.z - tr.x[:3]) > 3 * math.sqrt(np.trace(tr.P[:3, :3]) + np.trace(x.R)) + 5 for tr in conf)
                if lontano and conf:
                    vicino = min(conf, key=lambda tr: np.linalg.norm(x.z - tr.x[:3]))
                    if np.linalg.norm(x.z - vicino.x[:3]) < 150.0:
                        nuovi.append((x.t, nm, vicino.id))
            if ms:
                ins.aggiorna(ms)
            if nm in nuc and nm not in dichiarato:
                sn, g, _pg = nuc[nm]
                for tr in list(ins.tracce):
                    if tr.t_vista < min([x.t for x in ms], default=rc["t"]) - 1e-9 and g.indice(tr.x[:3]) is not None:
                        ip = m.insieme_presenza(tr, rc["t"], REG, REG["scenari"][fam]["classi_ammesse"]) if tr.confermata else None
                        if ip is not None:
                            ok, _ = m.avviso_spegnibile([g], ip, rc["t"], classi_d, n_punti=32, rng=np.random.default_rng(tr.id))
                            if not ok:
                                continue
                        ninz = len(ins.chiuse)
                        ins.mancato(rc["t"], sn, tr.id)
        # salute: nessun record per 3 periodi
        for s in sensori:
            if s.nome not in dichiarato and ultimo[s.nome] > 0 and tk - ultimo[s.nome] > 3 * per[s.nome] + 0.2:
                dichiarato[s.nome] = tk
                if s.nome in nuc:
                    ins.affidabilita_persa(tk, nuc[s.nome][0])
        conf = [tr for tr in ins.tracce if tr.confermata]
        # coppia in contatto (EV-A innesco_contatto): distanza <= ingombri/2 + 3 (sigma1 + sigma2)
        if evento is None:
            for a in range(len(conf)):
                for b in range(a + 1, len(conf)):
                    A, B = conf[a], conf[b]
                    sa, sb = math.sqrt(np.trace(A.P[:3, :3]) / 3), math.sqrt(np.trace(B.P[:3, :3]) / 3)
                    if np.linalg.norm(A.x[:3] - B.x[:3]) <= 0.35 + 3 * (sa + sb):
                        cand = (tk, A, B)
            recenti = [x for x in nuovi if tk - 2.0 <= x[0] <= tk]
            regs = set((x[1], round(x[0], 1)) for x in recenti)
            persa = cand is not None and any(tr in ins.chiuse for tr in (cand[1], cand[2])) and tk - cand[0] <= 2.0
            if (len(recenti) >= FRAM["innesco_separazione"]["n_ritorni_nuovi_min"] and len(regs) >= 2) or persa:
                orig = [cand[1], cand[2]] if (cand is not None and tk - cand[0] <= 4.0) else ([next((tr for tr in conf if tr.id == recenti[-1][2]), None)] if recenti else [])
                orig = [o for o in orig if o is not None]
                if orig:
                    t_a = cand[0] if (cand is not None and tk - cand[0] <= 4.0) else min(x[0] for x in recenti)
                    p0 = np.mean([o.p_ultima for o in orig], 0)
                    r0 = 3 * max(o.sigp_ultima for o in orig) + 0.5 * 0.35
                    evento = {"t_b": float(tk), "t_a": float(t_a), "tipo": "contatto" if len(orig) == 2 else "separazione",
                              "ev": {"p0": p0.tolist(), "vc": [o.v_ultima.tolist() for o in orig], "r0": r0},
                              "par": PAR_COLL if eid in ("E1", "E5", "E4") else PAR_AVAR}
        # ---------------------------------------------------- misure
        if evento is not None and frs:
            tau = tk - evento["t_a"]
            r, tq, zmin, zmax, Tc = FR.inviluppo(tau, evento["ev"], evento["par"])
            for k in ver:
                if not k.startswith("fr"):
                    continue
                T, P, _ = ver[k]
                p = P[min(int(round(tk / 0.1)), len(T) - 1)]
                if np.any(np.isnan(p)):
                    continue
                tot_V += 1
                dentro_V += int(FR.dentro_pianta(p[0], p[1], tau, evento["ev"], evento["par"]) <= 1e-9 and zmin - 1e-6 <= p[2] <= zmax + 1e-6)
            R_imp, _ = FR.impronta(evento["ev"], evento["par"])
            if abs(tk - round(tk)) < 1e-6 and griglie:
                rr = np.random.default_rng(int(tk * 10))
                c = np.asarray(evento["ev"]["p0"][:2])
                for _ in range(32):
                    a, d = rr.uniform(0, 2 * math.pi), R_imp * math.sqrt(rr.random())
                    q = [c[0] + d * math.cos(a), c[1] + d * math.sin(a), 1.0]
                    lib_imp_tot += 1
                    lib_imp += int(m.stato_fuso([g for g in griglie if g.affidabile], q, tk, classi_d + [{"rcs_m2": RCS_FR, "v_max": 1.0}]) == m.LIBERO)
        for k in principali:
            T, P, _ = ver[k]
            p = P[min(int(round(tk / 0.1)), len(T) - 1)]
            vis = any(s.visibile(p, tk) and (s.tipo != "camera" or (meteo is None) or True) for s in sensori if s.tipo != "cooperativa")
            out = {o["id"]: o for o in ins.uscite(tk, None, None)}
            if out:
                best = min(out.values(), key=lambda o: np.linalg.norm(o["pos"] - p))
                if vis and np.linalg.norm(best["pos"] - p) < 60:
                    assoc[k] = best["id"]
            if k in assoc and (not vis or (eid == "E4")):
                o = out.get(assoc[k])
                inside_cloud = any(np.linalg.norm(p[:2] - c) <= r and p[2] <= h for (c, r, h, _op) in sensori[0].nubi_al(tk)) if nubi else False
                if (not vis) or inside_cloud:
                    nasc_tot += 1
                    if o is None:
                        persi += 1
                        fuori_av += 1
                    elif "possibile_presenza" in o:
                        fuori_av += int(np.linalg.norm(p - o["possibile_presenza"]["centro"]) > o["possibile_presenza"]["raggio"])
            if abs(tk - round(tk)) < 1e-6 and griglie:
                lib_ogg_tot += 1
                lib_ogg += int(m.stato_fuso([g for g in griglie if g.affidabile], p, tk, classi_d) == m.LIBERO)
        if eid == "E3" and abs(tk - round(tk)) < 1e-6 and griglie:
            g = griglie[0]
            if g.affidabile:
                Ru = nuc[g.s.nome][0].portata(min(c["rcs_m2"] for c in classi_d), 0.99, 5)
                st = g.stati(tk, classi_d)
                oltre = (g.dist > Ru + g.dr) & ~g.ombra
                lib_oltre_tot += int(oltre.sum())
                lib_oltre += int((st[oltre] == m.LIBERO).sum())
        if log is not None:
            log.append({"t": round(float(tk), 2), "verita": {k: [round(float(x), 2) for x in ver[k][1][min(int(round(tk / 0.1)), len(ver[k][0]) - 1)]] for k in principali},
                        "uscite": [{"id": o["id"], "parola": o["parola"], "pos": [round(float(x), 1) for x in o["pos"]],
                                    "possibile_presenza_raggio_m": round(float(o["possibile_presenza"]["raggio"]), 1) if "possibile_presenza" in o else None}
                                   for o in ins.uscite(tk, None, None)],
                        "evento": None if evento is None else {"tipo": evento["tipo"], "t_b": evento["t_b"], "impronta_raggio_m": round(FR.impronta(evento["ev"], evento["par"])[0], 1)},
                        "affidabilita_persa": sorted(dichiarato)})
    # portata utile (E3): conto contro griglia
    pu = {}
    if eid == "E3":
        for nm, (sn, g, pg) in nuc.items():
            for cl in ("multirotore_piccolo", "aereo_leggero"):
                rc_ = REG["classi"][cl]["rcs_m2"]
                conto = fattore(meteo, nm.split("#")[0], 1) * m.Sensore("x", [0, 0, 0], CAT[nm.split("#")[0]]).portata(rc_, 0.99, 5)
                pu[cl] = {"conto_m": round(conto, 1), "nucleo_m": round(sn.portata(rc_, 0.99, 5), 1),
                          "d_avv_m": round(m.distanza_avviso(REG, ["multirotore_piccolo"] if cl == "multirotore_piccolo" else REG["scenari"][fam]["classi_ammesse"], "operatore_di_sito"), 1)}
    R.update({"evento": None if evento is None else {k: evento[k] for k in ("t_b", "t_a", "tipo")},
              "ritardo_evento_s": None if (evento is None or t_ev is None) else evento["t_b"] - t_ev,
              "falso_evento": bool(evento is not None and t_ev is None),
              "frammenti_dentro_V": [dentro_V, tot_V], "libero_in_impronta_nucleo_solo": [lib_imp, lib_imp_tot],
              "nasc_tot": nasc_tot, "tracce_perse_senza_avviso": persi, "fuori_avviso": fuori_av,
              "libero_su_oggetto": [lib_ogg, lib_ogg_tot], "libero_oltre_portata_utile": [lib_oltre, lib_oltre_tot],
              "ritardo_salute_cicli": ritardo_cicli, "portata_utile": pu})
    if esemplare:
        R["esemplare"] = {"scenario": eid, "configurazione": cfg, "variante": variante,
                          "sensori": [{"nome": s.nome, "pos": s.pos.tolist()} for s in sensori],
                          "verita_passo_0_5s": {k: ver[k][1][::5].round(2).tolist() for k in principali},
                          "frammenti_passo_0_5s": {k: np.nan_to_num(ver[k][1][::5], nan=-1).round(2).tolist() for k in ver if k.startswith("fr")},
                          "rilevazioni": [{"t": rc["t"], "sensore": rc["sensore"], "salute": rc["salute"], "ril": [{"vero": oid, "z": [round(float(x), 2) for x in z]} for (oid, z, _r, _e) in rc["ril"]]} for rc in recs],
                          "cicli": log, "avvertenza": "SIMULAZIONE: nessun dato di un sensore fisico; scenario d'incidente scritto a mano"}
    return R


def _lavoro(a):
    try:
        return a, passaggio(*a)
    except Exception as e:
        import traceback
        return a, {"errore": repr(e), "traccia": traceback.format_exc()[-1500:]}


def main():
    from multiprocessing import Pool
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    NP = min(int(sys.argv[2]) if len(sys.argv) > 2 else 8, 8)
    N5 = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    N12 = int(sys.argv[4]) if len(sys.argv) > 4 else 20          # E1, E2: 40-70 s a passaggio (frammenti)
    NS = int(sys.argv[5]) if len(sys.argv) > 5 else 100
    t0 = time.time()
    lav = [(e, c, i) for e in ("E1", "E2") for c in ("min", "alta") for i in range(N12)]
    lav += [(e, c, i) for e in ("E3", "E4") for c in ("min", "alta") for i in range(N)]
    lav += [("E5", "alta", i, 5.0) for i in range(N5)] + [("E5", "alta", i, s) for s in (2.0, 1.0, 0.5) for i in range(NS)]
    with Pool(NP) as p:
        righe = p.map(_lavoro, lav, chunksize=1)
    agg = {}
    for (a, r) in righe:
        key = "%s/%s" % (a[0], a[1]) + ("/sep%.1f" % a[3] if len(a) > 3 else "")
        agg.setdefault(key, []).append(r)
    out = {}
    for key, rr in agg.items():
        err = [r for r in rr if "errore" in r]
        rr = [r for r in rr if "errore" not in r]
        n = len(rr)
        A = {"n": n, "errori": len(err), "esempio_errore": err[0]["traccia"] if err else None}
        if not rr:
            out[key] = A
            continue
        rit = [r["ritardo_evento_s"] for r in rr if r["ritardo_evento_s"] is not None]
        A["evento_dichiarato"] = list(m.wilson(sum(r["evento"] is not None for r in rr), n)) + [sum(r["evento"] is not None for r in rr), n]
        A["entro_2s"] = [sum(x <= 2.0 for x in rit), n, *m.wilson(sum(x <= 2.0 for x in rit), n)]
        A["ritardo_s_mediana_max"] = [round(float(np.median(rit)), 2), round(float(np.max(rit)), 2)] if rit else None
        A["falsi_eventi"] = [sum(r["falso_evento"] for r in rr), n, *m.wilson(sum(r["falso_evento"] for r in rr), n)]
        dv = [sum(r["frammenti_dentro_V"][0] for r in rr), sum(r["frammenti_dentro_V"][1] for r in rr)]
        A["frammenti_dentro_V"] = [*dv, *(m.wilson(*dv) if dv[1] else (None, None))]
        li = [sum(r["libero_in_impronta_nucleo_solo"][0] for r in rr), sum(r["libero_in_impronta_nucleo_solo"][1] for r in rr)]
        A["libero_in_impronta_senza_strato_eventi"] = li
        A["cicli_nascosti"] = sum(r["nasc_tot"] for r in rr)
        A["tracce_perse_senza_avviso"] = sum(r["tracce_perse_senza_avviso"] for r in rr)
        A["fuori_avviso"] = sum(r["fuori_avviso"] for r in rr)
        lo = [sum(r["libero_su_oggetto"][0] for r in rr), sum(r["libero_su_oggetto"][1] for r in rr)]
        A["libero_su_oggetto"] = lo
        A["libero_oltre_portata_utile"] = [sum(r["libero_oltre_portata_utile"][0] for r in rr), sum(r["libero_oltre_portata_utile"][1] for r in rr)]
        cic = [v for r in rr for v in r["ritardo_salute_cicli"].values()]
        A["salute_cicli_max"] = max(cic) if cic else None
        A["salute_dichiarata"] = len(cic)
        if key.startswith("E3"):
            A["portata_utile_esempio"] = {r["variante"]: r["portata_utile"] for r in rr[:3]}
        out[key] = A
    os.makedirs(os.path.join(QUI, "esemplari"), exist_ok=True)
    for e in ("E1", "E2", "E3", "E4", "E5"):
        R = passaggio(e, "alta", 0, 5.0 if e == "E5" else None, True)
        with open(os.path.join(QUI, "esemplari", "%s_alta_0.json" % e), "w", encoding="utf-8") as f:
            json.dump(R["esemplare"], f, ensure_ascii=False, default=lambda x: x.tolist() if hasattr(x, "tolist") else float(x))
    ris = {"avvertenza": "SIMULAZIONE; strato eventi scritto da me dalle regole di regole_eventi.json (non indipendente)",
           "durata_s": round(time.time() - t0, 1), "n_E3_E4": N, "n_E1_E2": N12, "n_E5_5m": N5, "n_E5_altre": NS, "risultati": out}
    with open(os.path.join(F15, "11-prove", "risultati_eventi.json"), "w", encoding="utf-8") as f:
        json.dump(ris, f, ensure_ascii=False, indent=1, default=float)
    print(json.dumps(ris, ensure_ascii=False, default=float)[:6000])


if __name__ == "__main__":
    main()
