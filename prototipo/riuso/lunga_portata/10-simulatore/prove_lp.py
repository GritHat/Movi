"""prove_lp.py - prove del nucleo movi_lp.py (NON modificato) sui sei scenari A1-A4, S1, S2, con due configurazioni.

Uso:  python -I -B prove_lp.py [n_passaggi] [n_processi] [scenari separati da virgola]
Scrive ../11-prove/risultati_lp.json ed esemplari/<scenario>.json. Semi: SeedSequence(20261115, spawn_key).
Tutto e' simulazione: nessuna prova su un sensore fisico. Etichette di classe assegnate a mano dalla verita'.
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
REG = m.carica_regole(os.path.join(F15, "04-moto", "regole_lunga_portata.json"))
SCEN = {s["id"]: s for s in json.load(open(os.path.join(F15, "03-scenari", "scenari.json"), encoding="utf-8"))["scenari"]}
CAT = S.catalogo()
ENTROPIA = 20261115

CLASSE = {"multirotore": "multirotore_piccolo", "aereo_rullaggio": "aereo_rullaggio", "aereo_avvicinamento": "aereo_linea_avvicinamento",
          "auto_strada_urbana": "auto_strada_urbana", "treno_banchina": "treno_banchina", "aereo_leggero": "aereo_leggero",
          "mezzo_piazzale": None, "persona_a_piedi": None}
RCS = {"multirotore": 0.01, "aereo_rullaggio": 20.0, "aereo_avvicinamento": 20.0, "auto_strada_urbana": 10.0, "treno_banchina": 100.0,
       "mezzo_piazzale": 10.0, "persona_a_piedi": 0.5, "aereo_leggero": 2.0}      # regole_lunga_portata.json; mezzo e persona: I
RCS_C0 = 1.6e-4        # conto di 02-sensori dalla scheda IRIS (drone C0 da 0,249 kg visto a 1,1 km)
FAMIGLIA = {"A1": "aeroporto_e_droni", "A2": "aeroporto_e_droni", "A3": "aeroporto_e_droni", "A4": "aeroporto_e_droni",
            "S1": "strada", "S2": "ferrovia"}
# punto protetto (dove serve l'avviso): ipotesi mia, dichiarata in PROVE_LUNGA_PORTATA.md
PROTETTO = {"A1": [0, 0, 10], "A2": "mezzo1", "A3": "aereo2", "A4": [0, 0, 30], "S1": [0, 9, 0.75], "S2": [0, 12, 2]}
COMPORTAMENTI = ["nominale", "rallenta", "ferma", "vira", "indietro"]


def sens(tipo, pos, **kw):
    return (tipo, pos, kw)


CONFIG = {
    "A1": {"min": [sens("radar_sorveglianza_droni", [0, 0, 10])],
           "alta": [sens("radar_sorveglianza_droni", [0, 0, 10]), sens("radar_drone_pannello", [200, 650, 10], az0=-90.0),
                    sens("camera_eo_ottica_lunga", [0, 0, 12]), sens("identificazione_remota", [0, 0, 10])]},
    "A2": {"min": [sens("radar_movimento_a_terra", [0, 0, 25])],
           "alta": [sens("radar_movimento_a_terra", [0, 0, 25]), sens("lidar_auto_campo_largo", [200, 330, 10], az0=-90.0),
                    sens("ads_b", [0, 0, 25])]},
    "A3": {"min": [sens("radar_aeroporto", [0, 0, 10]), sens("ads_b", [0, 0, 10])],
           "alta": [sens("radar_aeroporto", [0, 0, 10]), sens("ads_b", [0, 0, 10]), sens("radar_sorveglianza_droni", [500, -2000, 15]),
                    sens("camera_eo_ottica_lunga", [500, -2000, 17]), sens("identificazione_remota", [500, -2000, 15])]},
    "A4": {"min": [sens("radar_4d_auto", [0, 0, 30], az0=0.0)],
           "alta": [sens("radar_4d_auto", [0, 0, 30], az0=0.0), sens("lidar_auto_campo_largo", [0, 0, 30], az0=0.0),
                    sens("camera_eo_ottica_lunga", [0, 0, 30])]},
    "S1": {"min": [sens("radar_4d_auto", [0, 0, 6], az0=0.0)],
           "alta": [sens("radar_4d_auto", [0, 0, 6], az0=0.0), sens("lidar_auto_campo_largo", [0, 0, 6], az0=0.0),
                    sens("radar_4d_auto", [-15, 20, 6], az0=-20.0)]},
    "S2": {"min": [sens("lidar_tele", [0, 0, 5], az0=5.0)],
           "alta": [sens("lidar_tele", [0, 0, 5], az0=5.0), sens("radar_4d_auto", [0, 0, 5], az0=0.0),
                    sens("lidar_auto_campo_largo", [300, 20, 5], az0=-120.0)]},
}


# ----------------------------------------------------------------------------- regioni dai dati pubblici
def tara_regioni(scarta_meta=True):
    """Raggio della regione per classe dagli errori della previsione a velocita' costante su traiettorie PUBBLICHE
    (01-dati/traiettorie): scene pari per tarare, dispari per provare (divisione per scena, non per campione)."""
    base = os.path.join(F15, "01-dati", "traiettorie")
    fonti = {"multirotore_piccolo": ("droni", "multirotore"), "aereo_rullaggio": ("aerei", "aereo_rullaggio"),
             "aereo_linea_avvicinamento": ("aerei", "aereo_avvicinamento"), "auto_strada_urbana": ("auto", "auto"),
             "treno_banchina": ("treni", "treno"), "aereo_leggero": ("aerei", "aereo_aviazione_generale_circuito")}
    ORZ, LIV = REG["previsione"]["orizzonti_s"], REG["previsione"]["livello"]
    reg, tab = {}, {}
    for cl, (cart, tipo) in fonti.items():
        scene = []
        for nome in sorted(os.listdir(os.path.join(base, cart))):
            d = os.path.join(base, cart, nome)
            try:
                sc = json.load(open(os.path.join(d, "scena.json"), encoding="utf-8"))
            except Exception:
                continue
            if sc["oggetti"][0].get("tipo") != tipo:
                continue
            A = np.genfromtxt(os.path.join(d, "verita.csv"), delimiter=",", skip_header=1, usecols=(0, 2, 3, 4, 5, 6, 7))
            if A.ndim != 2 or len(A) < 5:
                continue
            scene.append(A)
        E = {0: [[] for _ in ORZ], 1: [[] for _ in ORZ]}
        for k, A in enumerate(scene):
            t = A[:, 0]
            passo = 2.0 if t[-1] - t[0] < 600 else 10.0
            for t0 in np.arange(t[0], t[-1] - ORZ[-1], passo):
                p0 = np.array([np.interp(t0, t, A[:, c]) for c in (1, 2, 3)])
                v0 = np.array([np.interp(t0, t, A[:, c]) for c in (4, 5, 6)])
                for j, h in enumerate(ORZ):
                    p1 = np.array([np.interp(t0 + h, t, A[:, c]) for c in (1, 2, 3)])
                    E[k % 2][j].append(float(np.linalg.norm(p1 - (p0 + v0 * h))))
        if not E[0][0]:
            continue
        raggi = [m.tara_regione(E[0][j], LIV) for j in range(len(ORZ))]
        reg[cl] = m.RegionePrevisione(ORZ, raggi, LIV)
        cop = []
        for j in range(len(ORZ)):
            e = np.asarray(E[1][j])
            k = int((e <= raggi[j]).sum())
            lo, hi = m.wilson(k, len(e))
            cop.append({"orizzonte_s": ORZ[j], "raggio_m": round(raggi[j], 1), "n_tara": len(E[0][j]), "n_prova": len(e),
                        "copertura_prova": round(k / max(len(e), 1), 4), "wilson95": [round(lo, 4), round(hi, 4)]})
        tab[cl] = {"scene": len(scene), "orizzonti": cop}
    return reg, tab


# ----------------------------------------------------------------------------- un passaggio
def _griglia(nome, tipo, pos, par_g, ost, ver_tutte):
    """Griglia del nucleo per un sensore a distanza (radar, lidar), con la stessa geometria del simulatore."""
    sn = m.Sensore(nome, pos, dict(par_g, tipo=tipo if tipo != "lidar" else "lidar"))
    pts = np.concatenate([P for (_, P, _) in ver_tutte.values()])
    d = pts - np.asarray(pos, float)
    rr = np.linalg.norm(d, axis=1)
    r_max = min(par_g["r_max_m"], float(rr.max()) * 1.15 + 50.0)
    dr = max(r_max / 70.0, 2.0)
    h0, h1 = par_g["az_campo"]
    a0 = math.radians(max(-180.0, par_g.get("az0", 0.0) + h0))
    a1 = math.radians(min(180.0, par_g.get("az0", 0.0) + h1))
    n_az = max(8, int(round((a1 - a0) / (2 * math.pi) * 180)))
    if par_g.get("due_d"):
        el = (0.0,)
    else:
        e = np.degrees(np.arcsin(np.clip(d[:, 2] / np.maximum(rr, 1e-6), -1, 1)))
        lo = max(par_g["el_campo"][0], float(e.min()) - 2.0)
        hi = min(par_g["el_campo"][1], float(e.max()) + 2.0)
        el = tuple(np.radians(np.linspace(lo, hi, 5)))
    g = m.GrigliaPolare(sn, r_max, dr, n_az, el=el, ostacoli=ost, t_cumulo=REG["libero"]["t_cumulo_max_s"],
                        n_passate_max=REG["libero"]["n_passate_max"], pd_cum_min=REG["libero"]["pd_cumulata_min"], az_lim=(a0, a1))
    # orizzonte e quota minima del radar: celle coperte (vanno in 'in_ombra', mai 'libero')
    if tipo == "radar":
        Z = g.centri[..., 2]
        g.ombra |= (g.dist > np.vectorize(lambda z: S.orizzonte_m(pos[2], z))(np.maximum(Z, 0))) | (Z < par_g.get("z_min", 0.0))
    return sn, g


CHIAMANTE = os.environ.get("MOVI_CHIAMANTE", "interfaccia")


def passaggio(scen, cfg, idx, esemplare=False, regioni=None, meteo=1.0, meteo_prudente=None, chiamante=None):
    chiamante = chiamante or CHIAMANTE
    t_calc0 = time.perf_counter()
    sc = SCEN[scen]
    ss_ver = np.random.SeedSequence(ENTROPIA, spawn_key=(list(SCEN).index(scen), 0, idx))        # verita': appaiata fra config.
    ss_sen = np.random.SeedSequence(ENTROPIA, spawn_key=(list(SCEN).index(scen), 1 + ("min", "alta").index(cfg), idx))
    rv, rs = np.random.default_rng(ss_ver), np.random.default_rng(ss_sen)
    prima_estrazione = float(np.random.default_rng(ss_sen).random())
    comp = COMPORTAMENTI[idx % len(COMPORTAMENTI)]
    if sc["oggetti"][0]["classe"] == "treno_banchina" and comp == "vira":
        comp = "rallenta"                                    # un treno non vira: sostituito (dichiarato)
    coop_modo = ["presente", "assente", "intermittente"][idx % 3]
    c0 = scen in ("A1", "A4") and idx % 7 == 3
    fv = float(rv.uniform(0.7, 1.2))
    ost = S.ostacoli_da_poligoni(sc["ostacoli"])
    bers = sc["avviso"]["bersaglio"]
    primo = CONFIG[scen]["min"][0]
    par0 = dict(CAT[primo[0]], **primo[2])
    s0 = S.SensoreSim("p", primo[1], par0, ostacoli=ost)
    ver = {}
    t_fine = max(o["durata_s"] + o.get("t0", 0) for o in sc["oggetti"]) * 1.3 + 25
    for o in sc["oggetti"]:
        cl = REG["classi"].get(CLASSE.get(o["classe"]) or "", {})
        ver[o["id"]] = S.genera_verita(o, comp if o["id"] == bers else "nominale", fv if o["id"] == bers else 1.0, rv,
                                        t_fine=t_fine, nascosto=lambda p, t: not s0.visibile(p, t), a_lat=cl.get("a_lat"),
                                        v_retro=cl.get("v_retro_max"))
    ogg = {o["id"]: o for o in sc["oggetti"]}

    def rcs(oid, tipo):
        o = ogg[oid]
        if tipo == "camera":
            return 0.2 if (c0 and o["classe"] == "multirotore") else max(o["ingombro"])
        return RCS_C0 if (c0 and o["classe"] == "multirotore") else RCS[o["classe"]]

    fase_coop = float(rv.uniform(0, 20))

    def coop(oid, t):
        o = ogg[oid]
        if o["classe"] not in ("multirotore", "aereo_rullaggio", "aereo_avvicinamento", "aereo_leggero"):
            return False
        return coop_modo == "presente" or (coop_modo == "intermittente" and ((t + fase_coop) % 20.0) < 10.0)

    # salute: idx % 10 == 9 -> sensore principale spento 15 s; idx % 10 == 8 -> pioggia forte (radar) / abbagliamento
    lista = CONFIG[scen][cfg]
    salute_ev = None
    t_sal = float(rv.uniform(0.3, 0.6)) * (t_fine - 25) / 1.3
    if idx % 10 == 9:
        salute_ev = (0, (t_sal, t_sal + 15.0, "spento"))
    elif idx % 10 == 8:
        j = next((i for i, x in enumerate(lista) if CAT[x[0]]["tipo"] == "radar"), None)
        k = "pioggia_forte"
        if j is None:
            j = next((i for i, x in enumerate(lista) if CAT[x[0]]["tipo"] == "camera"), None)
            k = "abbagliamento"
        if j is not None:
            salute_ev = (j, (t_sal, t_sal + 15.0, k))
    sensori, griglie, nuc, recs = [], [], {}, []
    radar_ril = {}
    for i, (tipo, pos, kw) in enumerate(lista):
        nome = "%s#%d" % (tipo, i)
        par = dict(CAT[tipo], **kw)
        sal = [salute_ev[1]] if (salute_ev and salute_ev[0] == i) else []
        s = S.SensoreSim(nome, pos, par, meteo=meteo, ostacoli=ost, salute=sal)
        sensori.append(s)
        if par["tipo"] in ("radar", "lidar"):
            sn, g = _griglia(nome, par["tipo"], pos, S.scala_meteo(par, meteo_prudente or meteo), ost, ver)
            griglie.append(g)
            nuc[nome] = (sn, g)
    for s in sensori:                                          # prima i radar: servono a orientare le camere
        if s.tipo == "camera":
            continue
        r = s.scansioni(ver, t_fine, rs, rcs, coop_stato=coop)
        recs += r
        if s.tipo == "radar":
            for rc in r:
                for (oid, *_rest) in rc["ril"]:
                    if oid is not None:
                        radar_ril.setdefault(oid, []).append(rc["t"])
    for s in sensori:
        if s.tipo == "camera":
            tt = {k: np.array(sorted(v)) for k, v in radar_ril.items()}
            recs += s.scansioni(ver, t_fine, rs, rcs, cue=lambda oid, t: oid in tt and np.any((tt[oid] <= t) & (tt[oid] >= t - 5.0)))
    recs.sort(key=lambda r: (r["t_consegna"], r["sensore"]))
    t_sim = time.perf_counter() - t_calc0
    # ------------------------------------------------------------- nucleo
    ins = m.Inseguitore(REG, FAMIGLIA[scen], griglie)
    classi_d = [REG["classi"][c] for c in REG["scenari"][FAMIGLIA[scen]]["classi_ammesse"]]
    binario = np.array([[600, 12, 2], [50, 12, 2]], float) if scen == "S2" else None
    per = {s.nome: s.par["periodo_s"] for s in sensori}
    lat = {s.nome: s.par.get("latenza_s", 0.0) for s in sensori}
    ultimo, dichiarato, cattivi, buoni = {s.nome: 0.0 for s in sensori}, {}, {s.nome: 0 for s in sensori}, {s.nome: 0 for s in sensori}
    ritardo_salute = None
    dt_tick = 0.5
    ticks = np.arange(1.0, t_fine, dt_tick)
    R = {"chiamante": chiamante, "comportamento": comp, "coop": coop_modo, "c0": c0, "fattore_v": round(fv, 3), "seme": list(ss_sen.spawn_key),
         "prima_estrazione": prima_estrazione, "salute": salute_ev[1][2] if salute_ev else None}
    assoc, storia_id, t_conf, d_conf, d_ril, t_ril = {}, {k: [] for k in ver}, None, None, None, None
    nasc_senza, nasc_fuori, nasc_tot, lib_viol, lib_tot = 0, 0, 0, {}, {}
    prec = {}           # (orizzonte) -> [dentro, n, senza_zona]
    gia_nascosto, ritorno = {k: False for k in ver}, {}
    id_falsi, id_veri = set(), set()
    costo, ir = [], 0
    log = [] if esemplare else None
    ins_reg = regioni or {}
    pos_s = [(s, s.tipo) for s in sensori if s.tipo != "cooperativa"]

    def pos_vera(oid, t):
        T, P, _ = ver[oid]
        i = min(max(int(round(t / (T[1] - T[0]))), 0), len(T) - 1)
        return P[i], i

    for tk in ticks:
        c0t = time.perf_counter()
        while ir < len(recs) and recs[ir]["t_consegna"] <= tk:
            rc = recs[ir]
            ir += 1
            nm = rc["sensore"]
            ultimo[nm] = rc["t_consegna"]
            # salute: indicatori della scheda (fondo > +6 dB, pixel saturi > 0,05) per 3 record di fila
            if rc["salute"]["fondo_db"] > 6.0 or rc["salute"]["saturi"] > 0.05:
                cattivi[nm] += 1
                buoni[nm] = 0
                if cattivi[nm] >= 3 and nm not in dichiarato:
                    dichiarato[nm] = rc["t_consegna"]
                    if nm in nuc:
                        ins.affidabilita_persa(rc["t_consegna"], nuc[nm][0])
                    ritardo_salute = rc["t_consegna"] - salute_ev[1][0]
            else:
                cattivi[nm] = 0
                buoni[nm] += 1
                if nm in dichiarato and buoni[nm] >= 10:
                    del dichiarato[nm]
                    if nm in nuc:
                        nuc[nm][1].ripristina()
            misure = []
            for (oid, z, Rm, ex) in rc["ril"]:
                lab = CLASSE.get(ogg[oid]["classe"]) if oid is not None else None
                misure.append(m.Misura(ex["t_ril"], z, Rm, nm, lab, vel=ex.get("vel"), R_vel=ex.get("R_vel"), id_coop=ex.get("id_coop")))
            if nm in nuc and nm not in dichiarato:
                # antenna rotante: la passata si data all'INIZIO del giro (lato prudente: l'illuminazione piu' vecchia)
                tp = rc["t"] - per[nm] if CAT[nm.split("#")[0]].get("rotante") else rc["t"]
                nuc[nm][1].passata(tp, [x.z for x in misure])
            if misure:
                ins.aggiorna(misure)
            if nm in nuc and nm not in dichiarato:
                sn, g = nuc[nm]
                tmin = min([x.t for x in misure], default=rc["t"])
                for tr in list(ins.tracce):
                    if tr.t_vista < tmin - 1e-9 and g.indice(tr.x[:3]) is not None:
                        if chiamante == "prudente" and tr.confermata:
                            # variante: l'evidenza d'assenza conta solo se TUTTO l'insieme di presenza e' guardato libero
                            ip = m.insieme_presenza(tr, rc["t"], REG, REG["scenari"][FAMIGLIA[scen]]["classi_ammesse"], binario)
                            ok, _ = m.avviso_spegnibile([g], ip, rc["t"], classi_d, n_punti=32, rng=np.random.default_rng(tr.id))
                            if not ok:
                                continue
                        ins.mancato(rc["t"], sn, tr.id)
        # sensore spento: nessun record per 3 periodi -> affidabilita' persa
        for s in sensori:
            nm = s.nome
            if nm not in dichiarato and tk - ultimo[nm] > 3 * per[nm] + lat[nm] and ultimo[nm] > 0:
                dichiarato[nm] = tk
                if nm in nuc:
                    ins.affidabilita_persa(tk, nuc[nm][0])
                if salute_ev and salute_ev[1][2] == "spento":
                    ritardo_salute = tk - salute_ev[1][0]
            if nm in dichiarato and salute_ev and salute_ev[1][2] == "spento" and tk - ultimo[nm] < per[nm] + lat[nm] + 1e-9 and tk > salute_ev[1][1]:
                del dichiarato[nm]
                if nm in nuc:
                    nuc[nm][1].ripristina()
        out = ins.uscite(tk, ins_reg, binario)
        per_id = {o["id"]: o for o in out}
        costo.append(time.perf_counter() - c0t)
        # ---------------------------------------------------------- misure sulla verita'
        conf = [o for o in out]
        for oid in ver:
            p, i = pos_vera(oid, tk)
            if tk < ogg[oid].get("t0", 0):
                continue
            nascosto = not any(s.visibile(p, tk) for (s, _) in pos_s)
            if conf:
                dd = [np.linalg.norm(o["pos"] - p) for o in conf]
                j = int(np.argmin(dd))
                gate = max(60.0, 0.03 * float(np.linalg.norm(p - sensori[0].pos)))
                if not nascosto and dd[j] < gate and conf[j]["parola"].startswith("vista"):
                    if gia_nascosto[oid] and oid not in ritorno:
                        ritorno[oid] = (assoc.get(oid), conf[j]["id"])
                    assoc[oid] = conf[j]["id"]
                    storia_id[oid].append(conf[j]["id"])
                    id_veri.add(conf[j]["id"])
                    if oid == bers and t_conf is None:
                        t_conf = tk
                        q = PROTETTO[scen]
                        pq = pos_vera(q, tk)[0] if isinstance(q, str) else np.asarray(q, float)
                        d_conf = float(np.linalg.norm(p - pq))
            # sicurezza del 'libero' sulla cella vera (ogni secondo)
            if abs(tk - round(tk)) < 1e-6:
                k = ogg[oid]["classe"] + ("_C0" if (c0 and ogg[oid]["classe"] == "multirotore") else "")
                st = m.stato_fuso([g for g in griglie if g.affidabile], p, tk, classi_d)
                lib_tot[k] = lib_tot.get(k, 0) + 1
                lib_viol[k] = lib_viol.get(k, 0) + int(st == m.LIBERO)
            if nascosto and oid in assoc:
                gia_nascosto[oid] = True
                nasc_tot += 1
                o = per_id.get(assoc[oid])
                if o is None:
                    nasc_senza += 1
                    nasc_fuori += 1
                elif "possibile_presenza" in o:
                    ins_ = o["possibile_presenza"]
                    if ins_["tipo"] == "sfera":
                        fuori = np.linalg.norm(p - ins_["centro"]) > ins_["raggio"]
                    else:
                        tr = next(x for x in ins.tracce if x.id == o["id"])
                        u = tr.v_ultima / max(np.linalg.norm(tr.v_ultima), 1e-6)
                        s_ = float((p - ins_["centro"]) @ u)
                        fuori = not (ins_["s_min"] - 1e-6 <= s_ <= ins_["s_max"] + 1e-6)
                    nasc_fuori += int(fuori)
                    if fuori and os.environ.get("MOVI_DIAG"):
                        tr = next(x for x in ins.tracce if x.id == o["id"])
                        print("DIAG fuori", scen, oid, round(float(tk), 1), "id", o["id"], "tau", round(o["da_s"], 1), "raggio", round(ins_["raggio"], 1),
                              "dist", round(float(np.linalg.norm(p - ins_["centro"])), 1), "t_vista", tr.t_vista, "t", tr.t, "sens", tr.sensori, file=sys.stderr)
                    tau = o["da_s"]
                    for h in (2, 5, 10, 20):
                        if abs(tau - h) <= dt_tick / 2 + 1e-9:
                            c = prec.setdefault(str(h), [0, 0, 0])
                            if "zona" in o:
                                c[0] += int(np.linalg.norm(p - o["zona"]["centro"]) <= o["zona"]["raggio"])
                                c[1] += 1
                            else:
                                c[2] += 1
                elif o["da_s"] > 2.5 + max(per.values()):
                    nasc_senza += 1
            if oid == bers and d_ril is None:
                pass
        for o in conf:
            if o["id"] not in id_veri:
                if min(np.linalg.norm(o["pos"] - pos_vera(k, tk)[0]) for k in ver) > 200.0:
                    id_falsi.add(o["id"])
        if log is not None:
            log.append({"t": round(float(tk), 2),
                        "verita": {k: [round(float(x), 2) for x in pos_vera(k, tk)[0]] for k in ver},
                        "uscite": [{"id": o["id"], "classe": o["classe"], "parola": o["parola"], "pos": [round(float(x), 1) for x in o["pos"]],
                                    "possibile_presenza_raggio_m": round(float(o["possibile_presenza"]["raggio"]), 1) if "possibile_presenza" in o else None,
                                    "zona": ({"centro": [round(float(x), 1) for x in o["zona"]["centro"]], "raggio_m": round(float(o["zona"]["raggio"]), 1)} if "zona" in o else None)}
                                   for o in out],
                        "affidabilita_persa": sorted(dichiarato)})
    # primo rilevamento (qualunque sensore non cooperativo) del bersaglio
    for rc in sorted(recs, key=lambda r: r["t"]):
        if CAT[rc["sensore"].split("#")[0]]["tipo"] == "cooperativa":
            continue
        if any(oid == bers for (oid, *_r) in rc["ril"]):
            t_ril = rc["t"]
            q = PROTETTO[scen]
            pq = pos_vera(q, t_ril)[0] if isinstance(q, str) else np.asarray(q, float)
            d_ril = float(np.linalg.norm(pos_vera(bers, t_ril)[0] - pq))
            break
    scambi = 0
    if len(ver) > 1:
        for oid, s in storia_id.items():
            altri = set(x for k, v in storia_id.items() if k != oid for x in v)
            scambi += sum(1 for a, b in zip(s[:-1], s[1:]) if a != b and b in altri)
    lat_max = max(lat.values())
    R.update({"t_conf": t_conf, "d_conf_m": d_conf, "d_ril_m": d_ril, "t_ril": t_ril,
              "tempestivo": bool(d_conf is not None and d_conf >= sc["avviso"]["d_richiesta_m"]),
              "nasc_tot": nasc_tot, "nasc_senza_regione": nasc_senza, "nasc_fuori_avviso": nasc_fuori, "precisione": prec,
              "libero_viol": lib_viol, "libero_tot": lib_tot, "falsi_confermati": len(id_falsi), "durata_s": float(ticks[-1]),
              "scambi": scambi, "ritorno": {k: (v[0] == v[1]) for k, v in ritorno.items()}, "ritardo_salute_s": ritardo_salute,
              "costo_ciclo_ms_mediana": 1000 * float(np.median(costo)), "costo_ciclo_ms_p95": 1000 * float(np.percentile(costo, 95)),
              "t_simulatore_s": t_sim, "eventi_nucleo": {k: sum(1 for e in ins.eventi if e[1] == k) for k in set(e[1] for e in ins.eventi)}, "n_record": len(recs), "lat_max_s": lat_max})
    if esemplare:
        R["esemplare"] = {"scenario": scen, "configurazione": cfg, "sensori": [{"nome": s.nome, "pos": s.pos.tolist(), "fonte": s.base.get("fonte")} for s in sensori],
                          "ostacoli": sc["ostacoli"], "verita_passo_0_1s": {k: {"t": ver[k][0][::5].round(2).tolist(), "p": ver[k][1][::5].round(2).tolist()} for k in ver},
                          "rilevazioni": [{"t": rc["t"], "t_consegna": rc["t_consegna"], "sensore": rc["sensore"], "salute": rc["salute"],
                                           "ril": [{"vero": oid, "z": [round(float(x), 2) for x in z]} for (oid, z, _R, _e) in rc["ril"]]} for rc in recs],
                          "cicli": log, "avvertenza": "SIMULAZIONE dalle schede: nessun dato di un sensore fisico; etichette a mano"}
    return R


# ----------------------------------------------------------------------------- aggregazione
def _lavoro(a):
    scen, cfg, idx = a
    global _REGIONI
    try:
        return (scen, cfg, idx, passaggio(scen, cfg, idx, esemplare=False, regioni=_REGIONI))
    except Exception as e:                      # un passaggio fallito si conta, non si nasconde
        import traceback
        return (scen, cfg, idx, {"errore": repr(e), "traccia": traceback.format_exc()[-1500:]})


_REGIONI = None


def _init():
    global _REGIONI
    _REGIONI, _ = tara_regioni()


def wl(k, n):
    lo, hi = m.wilson(k, n)
    return [k, n, round(k / n, 4) if n else None, round(lo, 4), round(hi, 4)]


def aggrega(righe):
    out = {}
    for scen in SCEN:
        for cfg in ("min", "alta"):
            rr = [r for (s, c, i, r) in righe if s == scen and c == cfg]
            if not rr:
                continue
            err = [r for r in rr if "errore" in r]
            rr = [r for r in rr if "errore" not in r]
            A = {"n_passaggi": len(rr), "errori": len(err), "esempio_errore": err[0]["traccia"] if err else None}
            A["tempestivo"] = wl(sum(r["tempestivo"] for r in rr), len(rr))
            A["confermato"] = wl(sum(r["t_conf"] is not None for r in rr), len(rr))
            dc = [r["d_conf_m"] for r in rr if r["d_conf_m"] is not None]
            dr = [r["d_ril_m"] for r in rr if r["d_ril_m"] is not None]
            A["d_conf_m_mediana_p5"] = [round(float(np.median(dc)), 1), round(float(np.percentile(dc, 5)), 1)] if dc else None
            A["d_ril_m_mediana_p5"] = [round(float(np.median(dr)), 1), round(float(np.percentile(dr, 5)), 1)] if dr else None
            A["d_richiesta_m"] = SCEN[scen]["avviso"]["d_richiesta_m"]
            A["cicli_nascosti"] = sum(r["nasc_tot"] for r in rr)
            A["cicli_nascosti_senza_regione"] = wl(sum(r["nasc_senza_regione"] for r in rr), max(A["cicli_nascosti"], 1))
            A["passaggi_con_ciclo_senza_regione"] = wl(sum(r["nasc_senza_regione"] > 0 for r in rr), len(rr))
            A["cicli_nascosti_fuori_avviso"] = wl(sum(r["nasc_fuori_avviso"] for r in rr), max(A["cicli_nascosti"], 1))
            prec = {}
            for comp in COMPORTAMENTI:
                for h in ("2", "5", "10", "20"):
                    d = [r["precisione"].get(h, [0, 0, 0]) for r in rr if r["comportamento"] == comp]
                    k, n, nz = sum(x[0] for x in d), sum(x[1] for x in d), sum(x[2] for x in d)
                    prec.setdefault(comp, {})[h] = {"dentro": wl(k, n) if n else [0, 0, None, None, None], "senza_zona": nz}
            A["precisione"] = prec
            lv, lt = {}, {}
            for r in rr:
                for k, v in r["libero_viol"].items():
                    lv[k] = lv.get(k, 0) + v
                    lt[k] = lt.get(k, 0) + r["libero_tot"][k]
            A["libero_su_oggetto"] = {k: wl(lv[k], lt[k]) for k in lt}
            ore = sum(r["durata_s"] for r in rr) / 3600.0
            nf = sum(r["falsi_confermati"] for r in rr)
            A["falsi_avvisi"] = {"n": nf, "ore": round(ore, 3), "per_ora": round(nf / ore, 3) if ore else None,
                                 "sup95_per_ora": round((nf + 1.96 * math.sqrt(max(nf, 1)) + 2) / ore, 3) if ore else None}
            A["scambi"] = wl(sum(r["scambi"] > 0 for r in rr), len(rr))
            rit = [v for r in rr for v in r["ritorno"].values()]
            A["stessa_identita_al_ritorno"] = wl(sum(rit), len(rit)) if rit else None
            sal = {}
            for r in rr:
                if r["salute"]:
                    sal.setdefault(r["salute"], []).append(r["ritardo_salute_s"])
            A["salute"] = {k: {"n": len(v), "dichiarata": sum(x is not None for x in v),
                               "ritardo_s_max": (round(max(x for x in v if x is not None), 2) if any(x is not None for x in v) else None)} for k, v in sal.items()}
            A["costo_ciclo_ms"] = {"mediana": round(float(np.median([r["costo_ciclo_ms_mediana"] for r in rr])), 2),
                                   "p95_peggiore": round(float(np.max([r["costo_ciclo_ms_p95"] for r in rr])), 2)}
            A["per_cooperazione"] = {mo: wl(sum(r["tempestivo"] for r in rr if r["coop"] == mo), sum(1 for r in rr if r["coop"] == mo)) for mo in ("presente", "assente", "intermittente")}
            A["C0_tempestivo"] = wl(sum(r["tempestivo"] for r in rr if r["c0"]), sum(1 for r in rr if r["c0"]))
            out["%s/%s" % (scen, cfg)] = A
    return out


def main():
    from multiprocessing import Pool
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    NP = min(int(sys.argv[2]) if len(sys.argv) > 2 else 8, 8)
    sel = sys.argv[3].split(",") if len(sys.argv) > 3 else list(SCEN)
    t0 = time.time()
    reg, tab = tara_regioni()
    lavori = [(s, c, i) for s in sel for c in ("min", "alta") for i in range(N)]
    with Pool(NP, initializer=_init) as pool:
        righe = pool.map(_lavoro, lavori, chunksize=4)
    # semi: tutti distinti, prime estrazioni tutte diverse (V6)
    ok = [r for (_, _, _, r) in righe if "errore" not in r]
    semi = set(tuple(r["seme"]) for r in ok)
    prime = set(r["prima_estrazione"] for r in ok)
    agg = aggrega(righe)
    # esemplari: passaggio 0 in configurazione alta
    os.makedirs(os.path.join(QUI, "esemplari"), exist_ok=True)
    for s in sel:
        R = passaggio(s, "alta", 0, esemplare=True, regioni=reg)
        with open(os.path.join(QUI, "esemplari", "%s_alta_0_%s.json" % (s, CHIAMANTE)), "w", encoding="utf-8") as f:
            json.dump(R["esemplare"], f, ensure_ascii=False, default=lambda x: x.tolist() if hasattr(x, "tolist") else float(x))
    ris = {"avvertenza": "SIMULAZIONE dalle schede e dati pubblici di moto; nessuna prova su sensori fisici; etichette a mano",
           "chiamante": CHIAMANTE, "n_per_scenario_config": N, "processi": NP, "durata_s": round(time.time() - t0, 1),
           "semi": {"passaggi_ok": len(ok), "semi_distinti": len(semi), "prime_estrazioni_distinte": len(prime)},
           "regioni_da_dati_pubblici": tab, "scenari": agg}
    os.makedirs(os.path.join(F15, "11-prove"), exist_ok=True)
    nome = os.path.join(F15, "11-prove", "risultati_lp_%s%s.json" % (CHIAMANTE, "" if len(sel) == len(SCEN) else "_" + "_".join(sel)))
    with open(nome, "w", encoding="utf-8") as f:
        json.dump(ris, f, ensure_ascii=False, indent=1, default=float)
    print(json.dumps({"durata_s": ris["durata_s"], "semi": ris["semi"]}), nome)


if __name__ == "__main__":
    main()
