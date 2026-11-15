"""eventi_v3.py - fase 2c (60-fase2c/01-correzioni, sciame-tracciamento), da eventi_v2.py. Cambi v3 (voce 4 del
par. 6 di VERDETTO_2B), tutti marcati "v3":
  * avversario-1: l'evento si apre solo con tracce d'origine viste da al piu' ETA_MAX_ORIGINE_S, e t_a non va prima
    del primo ritorno nuovo meno un giro meno ETA_MAX_ORIGINE_S (un contatto lungo non sposta t_a di 14 s);
  * fusione dei duplicati: due tracce confermate in contatto da piu' di T_DUPLICATO_S con velocita' relativa
    < DV_DUPLICATO sono UNA traccia (duplicato): non fanno coppia d'origine;
  * avversario-2, ispezione dell'impronta: campioni in pianta (anelli x azimut); un campione esce dall'impronta
    residua solo se, dopo t_a + T_c (tutti i frammenti a terra, tempo di volo prudente), e' 'libero' per il frammento
    minimo (Pd cumulata 0,99) sui sensori affidabili e non accecati. Fuori dalle griglie: mai ispezionato;
  * avviso ai mezzi solo se il percorso previsto entra nell'impronta RESIDUA;
  * nucleo v3 (60-fase2c/01-correzioni/movi_lp_v3.py) per difetto; mappa degli scenari E (nessun ostacolo) dichiarata
    completa con EVENTI_MAPPA_CERT=1 (predefinito qui, IPOTESI): col v2 non lo era, e il 'libero' era vuoto.
--- intestazione del v2 ---
eventi_v2.py - strato degli EVENTI IMPROVVISI (EV-A, EV-B, EV-C, EV-E) sopra il nucleo MoVi a lunga portata.

Uso:  python -I -B eventi_v2.py N12 N4 N5 [processi]     (passaggi per E1 ed E2, per E4, per E5 a 5 m)
Scrive risultati_v2.json (aggregati, Wilson 95 % PER PASSAGGIO) e passaggi_v2.jsonl (un record per passaggio).

Che cosa realizza (regole in ../../40-eventi/02-regole/regole_eventi.json; le scelte mie sono marcate "v2"):
- EV-A frammentazione o contatto, sempre "dedotto":
  * ritorno NUOVO = misura fuori dalla porta di ogni traccia confermata (3 sigma combinata + 5 m, come f15-04);
  * innesco: nella finestra di 2,0 s, entro r_porta = 150 m da una traccia confermata, >= 3 ritorni nuovi da >= 2
    record distinti (giri o sensori) E almeno un record con >= 2 ritorni nuovi (v2: "grappolo"; il disturbo e i
    falsi allarmi di scheda sono indipendenti cella per cella, la frammentazione da' ritorni simultanei);
  * contatto: se due tracce confermate sono state a d <= ingombri/2 + 3 (sigma1 + sigma2) nei 4 s prima, l'origine
    e' la coppia e t_a e' l'inizio del contatto; la sola fusione di due tracce NON e' un evento (v2: tolto
    l'indizio "traccia chiusa entro 2 s", che da solo dava falsi eventi in E5);
  * v2, innesco "fiammata sulla traccia": una camera passa da quadro buono a saturato e il baricentro della
    saturazione (rilevamento, ipotesi I: la camera lo da'; rumore 2 mrad) cade entro 2 gradi da una traccia
    confermata -> evento "avaria (dedotto)" su quella traccia, profilo avaria_motore_a_terra se z < 10 m.
  * t_a prudente = min(inizio contatto, primo ritorno nuovo - un giro del sensore, ultimo quadro buono);
    r0 = 3 sigma + meta' dell'ingombro massimo DELLO SCENARIO (nessuna etichetta) + a_max (t_b - t_a)^2 / 2.
  * volume V(tau) e impronta: frammenti.py (02-regole), inviluppo PRUDENTE.
- EV-E detriti a terra: impronta = disco R_imp (dichiarato intero da subito, piu' prudente del S(tau) intersecato)
  piu', se l'origine si muove a terra, la striscia a valle fino all'arresto (v^2 / (2 * 1,5 m/s^2), raggio 45 m: I).
  Stato "zona non verificata: possibili detriti" finche' ogni punto non e' 'libero' per il frammento minimo
  ammesso (Pd cumulata 0,99, rcs 1,96e-4 m^2) sui sensori affidabili e non accecati. AVVISO all'operatore per ogni
  traccia confermata il cui percorso previsto (velocita' costante per H = max(10, 140/|v|) s, ingrossato di
  min(a_max tau^2/2, (v_max+|v|) tau) + 3 sigma, inviluppo dello scenario con v_max >= 210 m/s) entra nell'impronta.
- EV-B nube: per ogni griglia, un punto dentro o dietro una nube opaca per QUEL tipo di sensore non conta (stato
  combinato sui soli sensori non accecati). La nube e' presa dallo scenario, NON stimata dallo sfondo: ottimista.
- EV-C abbagliamento: >= 3 quadri saturi di fila -> "affidabilita' persa: <sensore>"; le sue passate non contano.
Solo osservazione e avviso. Tutto e' simulazione; stesso autore e stesso simulatore della misura: non indipendente.
"""
import json
import math
import os
import sys
import time

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
F15 = os.path.dirname(os.path.dirname(QUI))
SIM = os.path.join(F15, "10-simulatore")
sys.path.insert(0, SIM)
import numpy as np  # noqa: E402

import eventi_lp as EL  # noqa: E402  (solo per caricare scenari, catalogo e funzioni del simulatore; nessuna scrittura)

# ---- adattatore al nucleo: v2 se esiste, altrimenti movi_lp.py di 04-moto
_V2 = os.path.join(F15, "50-fase2b", "01-nucleo", "movi_lp_v2.py")
_V3 = os.path.join(F15, "60-fase2c", "01-correzioni", "movi_lp_v3.py")
if os.path.exists(_V3) and os.environ.get("EVENTI_NUCLEO", "v3") == "v3":        # v3: predefinito
    sys.path.insert(0, os.path.dirname(_V3))
    import movi_lp_v3 as m  # noqa: E402
    m.MAPPA_CERTIFICATA_PREDEFINITA = os.environ.get("EVENTI_MAPPA_CERT", "1") == "1"
    NUCLEO = "60-fase2c/01-correzioni/movi_lp_v3.py"
elif os.path.exists(_V2) and os.environ.get("EVENTI_NUCLEO", "v1") == "v2":   # v2 in scrittura durante la misura: v1 per difetto
    sys.path.insert(0, os.path.dirname(_V2))
    import movi_lp_v2 as m  # noqa: E402
    NUCLEO = "50-fase2b/01-nucleo/movi_lp_v2.py"
else:
    m = EL.m
    NUCLEO = "04-moto/movi_lp.py"
S, FR = EL.S, EL.FR
REG, SE, CAT, FRAM = EL.REG, EL.SE, EL.CAT, EL.FRAM
INV = FRAM["inviluppo"]
PAR_COLL = dict(INV["collisione_multirotori"]["prudente"], k_tc=FRAM["k_tc"], r_rimbalzo=FRAM["r_rimbalzo_m"])
PAR_AVAR = dict(INV["avaria_motore_a_terra"]["prudente"], k_tc=FRAM["k_tc"], r_rimbalzo=FRAM["r_rimbalzo_m"])
RCS_FR = FRAM["frammento_minimo_ammesso"]["rcs_m2"]
G = 9.81
FAM = "aeroporto_e_droni"
CLASSI_D = [REG["classi"][c] for c in REG["scenari"][FAM]["classi_ammesse"]]
CL_FR = CLASSI_D + [{"rcs_m2": RCS_FR, "v_max": 1.0}]
INV_S = dict(m.inviluppo(REG, REG["scenari"][FAM]["classi_ammesse"]))
INV_S["v_max"] = max(INV_S["v_max"], 210.0)            # decisione del coordinatore: inviluppo corretto a 210 m/s
SOGLIE = {"n_nuovi_min": FRAM["innesco_separazione"]["n_ritorni_nuovi_min"], "finestra_s": 2.0, "r_porta_m": 150.0,
          "grappolo_min": 2, "contatto_memoria_s": 4.0, "fiammata_angolo_rad": math.radians(2.0),
          "rumore_rilevamento_saturazione_rad": 0.002, "a_arresto_m_s2": 1.5, "raggio_striscia_m": 45.0,
          "d_avv_mezzo_m": 140.0, "H_min_s": 10.0, "ciclo_s": 0.1,
          "eta_max_origine_s": 2.0, "eta_min_origine_s": 3.0, "t_duplicato_s": 4.0, "dv_duplicato_m_s": 3.0, "imp_anelli": 24, "imp_azimut": 48}   # v3


def frammenti_vett(ev, rng, t_fine_rel=60.0, dt=0.05):
    """Come eventi_lp.frammenti ma vettoriale: v0 = v_c + u (|u| <= dv_max), resistenza quadratica, vento costante."""
    n = ev["n_frammenti"]
    p0 = np.asarray(ev["p"], float)
    vc = np.asarray(ev.get("vc", [0, 0, 0]), float)
    w = np.asarray(ev.get("vento", [0, 0, 0]), float)
    u = rng.standard_normal((n, 3))
    u = u / np.linalg.norm(u, axis=1, keepdims=True) * ev["dv_max_m_s"] * rng.random((n, 1)) ** (1 / 3)
    vt = np.exp(rng.uniform(math.log(ev["v_t_m_s"][0]), math.log(ev["v_t_m_s"][1]), n))
    k = (G / vt ** 2)[:, None]
    p, v = np.tile(p0, (n, 1)), vc + u
    T = np.arange(0.0, t_fine_rel + 1e-9, dt)
    P = np.empty((len(T), n, 3))
    P[0] = p
    for i in range(1, len(T)):
        va = v - w
        a = np.array([0, 0, -G]) - k * np.linalg.norm(va, axis=1, keepdims=True) * va
        v = v + a * dt
        p = p + v * dt
        terra = p[:, 2] <= 0
        p[terra, 2] = 0.0
        v[terra] = 0.0
        P[i] = p
    return T, P, vt, np.linalg.norm(u, axis=1)


LONTANO = np.array([1e7, 1e7, -1e4])                     # v2: i frammenti non esistono prima dell'evento


def prepara(eid, cfg, idx, sep=None, seme_base=20261116):
    """Verita' e record dei sensori (dal simulatore f15, semi NUOVI: base 20261116)."""
    sc = SE[eid]
    ss_v = np.random.SeedSequence(seme_base, spawn_key=(100 + int(eid[1]), 0, idx, int(1000 * (sep or 0))))
    ss_s = np.random.SeedSequence(seme_base, spawn_key=(100 + int(eid[1]), 1 + ("min", "alta").index(cfg), idx, int(1000 * (sep or 0))))
    rv, rs = np.random.default_rng(ss_v), np.random.default_rng(ss_s)
    ogg = {o["id"]: json.loads(json.dumps(o)) for o in sc["oggetti"]}
    if eid == "E5" and sep is not None:
        for q in ogg["droneB"]["punti"]:
            q[2] = 80 + sep
    eventi = sc.get("eventi", [])
    t_fine = {"E1": 32.0, "E2": 45.0, "E4": 50.0, "E5": 45.0}[eid]      # v2: E1, E2 accorciati per il tempo di calcolo
    ver = {k: S.genera_verita(o, "nominale", 1.0, rv, t_fine=t_fine) for k, o in ogg.items()}
    t_ev, p_ev = None, None
    for e in eventi:
        if e["tipo"] in ("collisione", "avaria_motore"):
            t_ev = e["t"]
            pe = dict(e["parametri"])
            p_ev = np.asarray(pe["p"], float)
            src = pe["oggetti"] if "oggetti" in pe else [pe["oggetto"]]
            i_ev = int(round(t_ev / 0.1))
            pe["vc"] = np.mean([ver[s][2][i_ev] for s in src], 0)
            T, P, vt, un = frammenti_vett(pe, rv)
            Tf = np.arange(0, t_fine + 0.05, 0.1)
            for j in range(P.shape[1]):
                Pi = np.stack([np.interp(Tf - t_ev, T, P[:, j, c]) for c in range(3)], 1)
                Pf = np.where((Tf >= t_ev)[:, None], Pi, LONTANO)
                Vf = np.gradient(Pf, 0.1, axis=0)
                Vf[Tf < t_ev + 0.1] = 0.0
                ver["fr%02d" % j] = (Tf, Pf, Vf)
                ogg["fr%02d" % j] = {"classe": "frammento", "ingombro": [0.05], "t0": t_ev,
                                     "conforme": bool(vt[j] >= (PAR_COLL if eid == "E1" else PAR_AVAR)["v_t_min"] and un[j] <= (PAR_COLL if eid == "E1" else PAR_AVAR)["dv"])}
            if eid == "E1":                                   # B: caduta balistica dopo l'urto (come eventi_lp)
                T, P, V = ver["droneB"]
                i0 = int(round(t_ev / 0.1))
                for i in range(i0 + 1, len(T)):
                    va = V[i - 1]
                    a = np.array([0, 0, -G]) - G / 15.0 ** 2 * np.linalg.norm(va) * va
                    V[i] = V[i - 1] + a * 0.1 if P[i - 1, 2] > 0 else 0 * V[i - 1]
                    P[i] = np.maximum(P[i - 1] + V[i] * 0.1, [-1e9, -1e9, 0])
    nubi = []
    for n in sc.get("nubi", []) or []:
        fpos = None
        if "centro_segue" in n:
            T, P, _ = ver["aereo1"]
            fpos = (lambda t, T=T, P=P: P[min(int(round(t / 0.1)), len(T) - 1)])
        nubi.append((n, fpos))
    salute_cam, t_fiam = {}, None
    for e in eventi:
        if e["tipo"] == "fiammata":
            p = e["parametri"]
            t_fiam = e["t"]
            salute_cam = {"camera_eo_ottica_lunga": (e["t"], p["cieca_eo_fino_a_t"]), "camera_termica_ottica_lunga": (e["t"], p["cieca_termica_fino_a_t"])}
    lista = sc["sensori"]
    if cfg == "min":
        radar = [s for s in lista if CAT[s["tipo"]]["tipo"] == "radar"]
        lista = radar[:1] if (radar and eid != "E4") else [s for s in lista if CAT[s["tipo"]]["tipo"] == "camera"]
    sensori, griglie, nuc = [], [], {}
    for i, sd in enumerate(lista):
        par = dict(CAT[sd["tipo"]])
        nome = "%s#%d" % (sd["tipo"], i)
        sal = [(salute_cam[sd["tipo"]][0], salute_cam[sd["tipo"]][1], "abbagliamento")] if sd["tipo"] in salute_cam else []
        s = S.SensoreSim(nome, sd["pos"], par, meteo=1.0, ostacoli=[], nubi=nubi, salute=sal)
        sensori.append(s)
        if par["tipo"] in ("radar", "lidar"):
            r_max = min(par["r_max_m"], 1500.0)
            sn = m.Sensore(nome, sd["pos"], par)
            el = (0.0,) if par.get("due_d") else tuple(np.radians(np.linspace(-2, 20, 6)))
            g = m.GrigliaPolare(sn, r_max, r_max / 80.0, 180, el=el, t_cumulo=5.0, n_passate_max=5, pd_cum_min=0.99)
            griglie.append(g)
            nuc[nome] = (sn, g, par)

    def rcs(oid, tipo):
        o = ogg[oid]
        return max(o["ingombro"]) if tipo == "camera" else EL.RCS[o["classe"]]

    recs, radar_ril = [], {}
    for s in sensori:
        if s.tipo == "camera":
            continue
        r = s.scansioni(ver, t_fine, rs, rcs, coop_stato=lambda oid, t: False)
        if s.tipo == "radar":
            r = [EL.unisci_non_risolti(rc, ver, s.par) for rc in r]
            for rc in r:
                for (oid, *_x) in rc["ril"]:
                    if oid is not None:
                        radar_ril.setdefault(oid, []).append(rc["t"])
        recs += r
    tt = {k: np.array(sorted(v)) for k, v in radar_ril.items()}
    senza_radar = not any(x.tipo == "radar" for x in sensori)
    for s in sensori:
        if s.tipo == "camera":
            recs += s.scansioni(ver, t_fine, rs, rcs, cue=(None if senza_radar else (lambda oid, t: oid in tt and np.any((tt[oid] <= t) & (tt[oid] >= t - 5.0)))))
    recs.sort(key=lambda r: (r["t_consegna"], r["sensore"]))
    ing_max = max(max(o["ingombro"]) for o in ogg.values() if o["classe"] != "frammento")
    return dict(sc=sc, ogg=ogg, ver=ver, t_ev=t_ev, p_ev=p_ev, t_fiam=t_fiam, sensori=sensori, griglie=griglie, nuc=nuc,
                recs=recs, t_fine=t_fine, nubi=nubi, rng_bear=np.random.default_rng(ss_s.spawn(1)[0]), ing_max=ing_max)


# ----------------------------------------------------------------------------- strato eventi v2
def griglie_valide(D, p, t):
    """EV-B + EV-C: griglie affidabili e non accecate da una nube opaca per il loro tipo di sensore."""
    out = []
    for g in D["griglie"]:
        if not g.affidabile:
            continue
        s = next(x for x in D["sensori"] if x.nome == g.s.nome)
        if not S.in_vista(s.pos, p, (), s.nubi_al(t), t, s.nome_tipo):
            continue
        out.append(g)
    return out


def stato_v2(D, p, t, classi):
    gs = griglie_valide(D, p, t)
    return m.stato_fuso(gs, p, t, classi) if gs else m.NON_OSSERVATO


def campioni_impronta(Z):
    """v3: campioni dell'impronta in pianta (centri di settori di anello di area simile) e loro mezza spaziatura."""
    na, nz = SOGLIE["imp_anelli"], SOGLIE["imp_azimut"]
    rr = Z["R"] * np.sqrt((np.arange(na) + 0.5) / na)
    aa = (np.arange(nz) + 0.5) * 2 * math.pi / nz
    P = np.array([[Z["c"][0] + r * math.cos(a), Z["c"][1] + r * math.sin(a)] for r in rr for a in aa])
    return P, Z["R"] * max(1.0 / na, math.pi / nz)


def ispeziona(D, Z, tk):
    """v3: un campione e' ispezionato se una griglia affidabile, non accecata li', lo dice 'libero' per OGNI classe
    ammessa e per il frammento minimo, e nessuna lo dice 'occupato' (piu' prudente di stato_fuso: niente Pd congiunta)."""
    idx = np.nonzero(~Z["isp"])[0]
    if not len(idx):
        return
    lib = np.zeros(len(idx), bool)
    occ = np.zeros(len(idx), bool)
    for g in D["griglie"]:
        if not g.affidabile:
            continue
        st = g.stati(tk, CL_FR)
        s = next(x for x in D["sensori"] if x.nome == g.s.nome)
        for n, j in enumerate(idx):
            q = [float(Z["camp"][j, 0]), float(Z["camp"][j, 1]), 1.0]
            i = g.indice(q)
            if i is None or not S.in_vista(s.pos, q, (), s.nubi_al(tk), tk, s.nome_tipo):
                continue
            lib[n] |= st[i] == m.LIBERO
            occ[n] |= st[i] == m.OCCUPATO
    Z["isp"][idx[lib & ~occ]] = True


def zona_dist(Z, q):
    """Distanza in pianta di q dall'impronta (<= 0 dentro): disco R_imp ed eventuale striscia a valle.
    v3: se Z ha i campioni ispezionati, la distanza e' dall'impronta RESIDUA (campioni non ispezionati, ingrossati
    della mezza spaziatura); la striscia a valle resta intera."""
    d = math.hypot(q[0] - Z["c"][0], q[1] - Z["c"][1]) - Z["R"]
    if Z.get("isp") is not None:
        resto = Z["camp"][~Z["isp"]]
        d = (float(np.min(np.hypot(resto[:, 0] - q[0], resto[:, 1] - q[1]))) - Z["h"]) if len(resto) else math.inf
    if Z.get("striscia") is not None:
        a, b, r = Z["striscia"]
        d = min(d, FR.dist_segmento(q[0], q[1], a[0], a[1], b[0], b[1]) - r)
    return d


def apri_evento(D, tk, t_a, orig, tipo, par):
    p0 = np.mean([o.p_ultima for o in orig], 0)
    a_max = INV_S["a_max"]
    r0 = 3 * max(o.sigp_ultima for o in orig) + 0.5 * D["ing_max"] + 0.5 * a_max * (tk - t_a) ** 2
    ev = {"p0": p0.tolist(), "vc": [o.v_ultima.tolist() for o in orig], "r0": float(r0)}
    R_imp, _ = FR.impronta(ev, par)
    Z = {"c": p0[:2].copy(), "R": float(R_imp), "striscia": None}
    Z["camp"], Z["h"] = campioni_impronta(Z)                         # v3: ispezione dell'impronta
    Z["isp"] = np.zeros(len(Z["camp"]), bool)
    Z["Tc"] = float(FR.inviluppo(0.0, ev, par)[4])
    vh = np.mean([o.v_ultima[:2] for o in orig], 0)
    if p0[2] < 10.0 and np.linalg.norm(vh) > 1.0:          # origine a terra in moto: striscia a valle
        L = float(np.linalg.norm(vh)) ** 2 / (2 * SOGLIE["a_arresto_m_s2"])
        Z["striscia"] = (p0[:2].copy(), p0[:2] + vh / np.linalg.norm(vh) * L, SOGLIE["raggio_striscia_m"])
    return {"t_b": float(tk), "t_a": float(t_a), "tipo": tipo, "ev": ev, "par": par, "Z": Z,
            "origine": [o.id for o in orig], "stato": "dedotto"}


def percorso_entra(tr, Z, t):
    """EV-E: il percorso previsto della traccia (velocita' costante, ingrossato dall'inviluppo) entra nell'impronta?"""
    v = float(np.linalg.norm(tr.x[3:5]))
    H = max(SOGLIE["H_min_s"], SOGLIE["d_avv_mezzo_m"] / max(v, 0.1))
    sig = math.sqrt(np.trace(tr.P[:3, :3]))
    for tau in np.arange(0.0, H + 1e-9, 0.5):
        q = tr.x[:3] + tr.x[3:] * tau
        dev = min(0.5 * INV_S["a_max"] * tau ** 2, (INV_S["v_max"] + v) * tau) + 3 * sig
        if zona_dist(Z, q) <= dev:
            return True
    return False


def passaggio(eid, cfg, idx, sep=None):
    D = prepara(eid, cfg, idx, sep)
    ver, recs, sensori, griglie, nuc = D["ver"], D["recs"], D["sensori"], D["griglie"], D["nuc"]
    ins = m.Inseguitore(REG, FAM, griglie)
    per = {s.nome: s.par["periodo_s"] for s in sensori}
    pos_s = {s.nome: s.pos for s in sensori}
    cattivi, dichiarato, ritardo_cicli = {s.nome: 0 for s in sensori}, {}, {}
    ultimo_buono = {s.nome: None for s in sensori}
    ultimo = {s.nome: 0.0 for s in sensori}
    nuovi, contatti, fiamme = [], {}, []
    duplicati = set()                                        # v3
    evento = None
    avvisati = {}                                            # id traccia -> t del primo avviso
    principali = [k for k in D["ogg"] if D["ogg"][k]["classe"] != "frammento"]
    dentro_V = tot_V = 0
    lib_imp = lib_imp_tot = lib_fr = lib_fr_tot = 0
    ir = 0
    for tk in np.arange(SOGLIE["ciclo_s"], D["t_fine"], SOGLIE["ciclo_s"]):
        tk = round(float(tk), 3)
        while ir < len(recs) and recs[ir]["t_consegna"] <= tk:
            rc = recs[ir]
            ir += 1
            nm = rc["sensore"]
            ultimo[nm] = rc["t_consegna"]
            if rc["salute"]["saturi"] > 0.05 or rc["salute"]["fondo_db"] > 6:      # EV-C
                if cattivi[nm] == 0 and ultimo_buono[nm] is not None and rc["salute"]["saturi"] > 0.05 and D["p_ev"] is not None:
                    d = D["p_ev"] - pos_s[nm]                 # baricentro della saturazione (I), con rumore
                    az = math.atan2(d[1], d[0]) + D["rng_bear"].normal(0, SOGLIE["rumore_rilevamento_saturazione_rad"])
                    fiamme.append((rc["t_consegna"], nm, az, ultimo_buono[nm]))
                cattivi[nm] += 1
                if cattivi[nm] >= 3 and nm not in dichiarato:
                    dichiarato[nm] = rc["t_consegna"]
                    ritardo_cicli[nm] = cattivi[nm]
                    if nm in nuc:
                        ins.affidabilita_persa(rc["t_consegna"], nuc[nm][0])
                continue
            cattivi[nm] = 0
            ultimo_buono[nm] = rc["t"]
            ms = [m.Misura(ex["t_ril"], z, Rm, nm, EL.CLASSE.get(D["ogg"][oid]["classe"]) if oid else None) for (oid, z, Rm, ex) in rc["ril"]]
            if nm in nuc and nm not in dichiarato:
                tp = rc["t"] - per[nm] if nuc[nm][2].get("rotante") else rc["t"]
                nuc[nm][1].passata(tp, [x.z for x in ms])
            conf = [tr for tr in ins.tracce if tr.confermata]
            if evento is None and conf and ms:                 # EV-A: ritorni in ECCESSO sulle tracce (v2)
                X = np.array([tr.x[:3] for tr in conf])
                Zm = np.array([x.z for x in ms])
                rp = SOGLIE["r_porta_m"]
                kz = (np.linalg.norm(Zm[None, :, :] - X[:, None, :], axis=2) < rp).sum(1)
                jt = (np.linalg.norm(X[None, :, :] - X[:, None, :], axis=2) < rp).sum(1)
                ecc = kz - jt
                i = int(np.argmax(ecc))
                for _ in range(int(max(ecc[i], 0))):
                    nuovi.append((ms[0].t, nm, rc["t"], conf[i].id))
            if ms:
                ins.aggiorna(ms)
            if nm in nuc and nm not in dichiarato:              # mancati, chiamata PRUDENTE (come eventi_lp)
                sn, g, _ = nuc[nm]
                for tr in list(ins.tracce):
                    if tr.t_vista < min([x.t for x in ms], default=rc["t"]) - 1e-9 and g.indice(tr.x[:3]) is not None:
                        ip = m.insieme_presenza(tr, rc["t"], REG, REG["scenari"][FAM]["classi_ammesse"]) if tr.confermata else None
                        if ip is not None:
                            ok, _ = m.avviso_spegnibile([g], ip, rc["t"], CLASSI_D, n_punti=32, rng=np.random.default_rng(tr.id))
                            if not ok:
                                continue
                        ins.mancato(rc["t"], sn, tr.id)
        for s in sensori:                                      # salute: silenzio per 3 periodi
            if s.nome not in dichiarato and ultimo[s.nome] > 0 and tk - ultimo[s.nome] > 3 * per[s.nome] + 0.2:
                dichiarato[s.nome] = tk
                if s.nome in nuc:
                    ins.affidabilita_persa(tk, nuc[s.nome][0])
        conf = [tr for tr in ins.tracce if tr.confermata]
        if evento is None and len(conf) >= 2 and abs(tk * 2 - round(tk * 2)) < 1e-6:   # contatto, ogni 0,5 s
            X = np.array([tr.x[:3] for tr in conf])
            sg = np.array([math.sqrt(np.trace(tr.P[:3, :3]) / 3) for tr in conf])
            dd = np.linalg.norm(X[None] - X[:, None], axis=2) - (D["ing_max"] + 3 * (sg[None] + sg[:, None]))
            for a, b in zip(*np.nonzero(np.triu(dd <= 0, 1))):
                k = (min(conf[a].id, conf[b].id), max(conf[a].id, conf[b].id))
                if k in contatti and tk - contatti[k][1] > 0.6:              # v3: contatto interrotto, riparte
                    contatti[k] = [tk, tk]
                contatti.setdefault(k, [tk, tk])[1] = tk
                dv = float(np.linalg.norm(conf[a].x[3:] - conf[b].x[3:]))  # v3: fusione dei duplicati
                if tk - contatti[k][0] >= SOGLIE["t_duplicato_s"] and dv < SOGLIE["dv_duplicato_m_s"]:
                    duplicati.add(k)
        if evento is None:
            # (1) fiammata sulla traccia (v2)
            for (tf, nm, az, tbuono) in fiamme:
                if tk - tf > 1.0:
                    continue
                cand = []
                for tr in conf:
                    d = tr.x[:3] - pos_s[nm]
                    da = abs((math.atan2(d[1], d[0]) - az + math.pi) % (2 * math.pi) - math.pi)
                    if da <= SOGLIE["fiammata_angolo_rad"]:
                        cand.append((da, tr))
                if cand:
                    tr = min(cand, key=lambda c: c[0])[1]
                    par = PAR_AVAR if tr.x[2] < 10.0 else PAR_COLL
                    evento = apri_evento(D, tk, min(tbuono, tr.t_vista), [tr], "avaria o fiammata", par)
                    break
        if evento is None:
            # (2) frammentazione / contatto
            rec = [x for x in nuovi if tk - SOGLIE["finestra_s"] <= x[0] <= tk]
            if len(rec) >= SOGLIE["n_nuovi_min"]:
                per_rec = {}
                for x in rec:
                    per_rec.setdefault((x[1], x[2]), []).append(x)
                if len(per_rec) >= 2 and max(len(v) for v in per_rec.values()) >= SOGLIE["grappolo_min"]:
                    vic = max(set(x[3] for x in rec), key=lambda i: sum(x[3] == i for x in rec))
                    tr = next((t for t in conf if t.id == vic), None)
                    if tr is not None and (tk - tr.t_vista > SOGLIE["eta_max_origine_s"]          # v3: avversario-1
                                           or tk - tr.t_nascita < SOGLIE["eta_min_origine_s"]):  # v3 (dopo il pilota, passaggio 31)
                        tr = None
                    if tr is not None:
                        pair = [k for k, (t0, t1) in contatti.items() if vic in k and tk - t1 <= SOGLIE["contatto_memoria_s"]
                                and k not in duplicati]                              # v3: i duplicati non fanno coppia
                        t_a = min(x[2] for x in rec) - max(per[x[1]] for x in rec)
                        t_a_min = t_a - SOGLIE["eta_max_origine_s"]                  # v3: t_a solo da origini recenti
                        orig = [tr]
                        if pair:
                            k = max(pair, key=lambda k: contatti[k][1])
                            orig = [t for t in ins.tracce if t.id in k and tk - t.t_vista <= SOGLIE["eta_max_origine_s"]] or [tr]
                            t_a = min(t_a, max(contatti[k][0], t_a_min))
                        par = PAR_AVAR if tr.x[2] < 10.0 else PAR_COLL
                        evento = apri_evento(D, tk, t_a, orig, "contatto" if len(orig) == 2 else "separazione", par)
        if evento is not None:
            Z = evento["Z"]
            for tr in conf:                                     # EV-E avviso
                if tr.id not in avvisati and (zona_dist(Z, tr.x[:3]) <= 0 or percorso_entra(tr, Z, tk)):
                    avvisati[tr.id] = tk
            tau = tk - evento["t_a"]
            if abs(tk * 2 - round(tk * 2)) < 1e-6:              # ogni 0,5 s: frammenti dentro V
                r, tq, zmin, zmax, Tc = FR.inviluppo(tau, evento["ev"], evento["par"])
                for k in ver:
                    if not k.startswith("fr") or not D["ogg"][k]["conforme"]:
                        continue
                    T, P, _ = ver[k]
                    p = P[min(int(round(tk / 0.1)), len(T) - 1)]
                    if p[2] < -1:
                        continue
                    tot_V += 1
                    dentro_V += int(FR.dentro_pianta(p[0], p[1], tau, evento["ev"], evento["par"]) <= 1e-9 and zmin - 1e-6 <= p[2] <= zmax + 1e-6)
            if abs(tk - round(tk)) < 1e-6 and griglie and tk >= evento["t_a"] + Z["Tc"]:   # v3: ispezione
                ispeziona(D, Z, tk)
            if abs(tk - round(tk)) < 1e-6 and griglie:          # ogni 1 s: "libero" dentro l'impronta
                rr = np.random.default_rng(int(tk * 10) + 7 * idx)
                for _ in range(32):
                    a, d = rr.uniform(0, 2 * math.pi), Z["R"] * math.sqrt(rr.random())
                    q = [Z["c"][0] + d * math.cos(a), Z["c"][1] + d * math.sin(a), 1.0]
                    lib_imp_tot += 1
                    lib_imp += int(stato_v2(D, q, tk, CL_FR) == m.LIBERO)
                for k in ver:
                    if not k.startswith("fr"):
                        continue
                    p = ver[k][1][min(int(round(tk / 0.1)), len(ver[k][0]) - 1)]
                    if p[2] < -1 or zona_dist(Z, p) > 0:
                        continue
                    lib_fr_tot += 1
                    lib_fr += int(stato_v2(D, p, tk, CL_FR) == m.LIBERO)
    # ---- esiti per passaggio
    t_ev = D["t_ev"]
    R = {"scenario": eid, "cfg": cfg, "idx": idx, "sep": sep, "nucleo": NUCLEO,
         "evento": None if evento is None else {k: evento[k] for k in ("t_b", "t_a", "tipo", "origine", "stato")} | {"R_imp_m": round(evento["Z"]["R"], 1), "striscia": evento["Z"]["striscia"] is not None,
                   "Tc_s": round(evento["Z"]["Tc"], 1), "ispezionati": [int(evento["Z"]["isp"].sum()), len(evento["Z"]["isp"])],
                   "R_residuo_m": round(float(max([math.hypot(*(q - evento["Z"]["c"])) for q in evento["Z"]["camp"][~evento["Z"]["isp"]]], default=0.0) + evento["Z"]["h"]), 1)},
         "duplicati_fusi": len(duplicati),
         "ritardo_evento_s": None if (evento is None or t_ev is None) else round(evento["t_b"] - t_ev, 2),
         "falso_evento": bool(evento is not None and t_ev is None),
         "frammenti_dentro_V": [dentro_V, tot_V], "libero_in_impronta_punti": [lib_imp, lib_imp_tot],
         "libero_su_frammento_in_impronta": [lib_fr, lib_fr_tot], "salute_cicli": ritardo_cicli,
         "affidabilita_persa": sorted(dichiarato), "n_nuovi": len(nuovi),
         "nuovi_dopo_evento_vero": None if t_ev is None else [round(x[0], 2) for x in nuovi if x[0] >= t_ev][:12],
         "contatti": {"%d-%d" % k: [round(a, 1), round(b, 1)] for k, (a, b) in list(contatti.items())[:6]}}
    # avviso ai mezzi: traccia associata all'oggetto (la piu' vicina entro 30 m all'istante dell'avviso)
    if evento is not None:
        tracce_all = {tr.id: tr for tr in ins.tracce + ins.chiuse}
        for k in principali:
            if D["ogg"][k]["classe"] in ("multirotore", "aereo_rullaggio", "aereo_leggero") and k not in ("persona1", "mezzo1"):
                continue
            T, P, _ = ver[k]
            best = None
            for tid, ta in sorted(avvisati.items(), key=lambda x: x[1]):
                tr = tracce_all.get(tid)
                if tr is None:
                    continue
                p = P[min(int(round(ta / 0.1)), len(T) - 1)]
                # la traccia e' quella dell'oggetto se l'ultima stima nota e' vicina alla verita' a quell'istante
                q = tr.p_ultima if tr in ins.chiuse else tr.x[:3]
                pq = P[min(int(round(tr.t_vista / 0.1)), len(T) - 1)]
                if np.linalg.norm(q - pq) < 30.0 or np.linalg.norm(q - p) < 30.0:
                    fr = [ver[f][1][min(int(round(ta / 0.1)), len(T) - 1)] for f in ver if f.startswith("fr")]
                    dfr = min([float(np.hypot(*(q2[:2] - p[:2]))) for q2 in fr if q2[2] > -1], default=None)
                    best = (ta, float(zona_dist(evento["Z"], p)), dfr)
                    break
            # distanza minima vera dell'oggetto dall'impronta dopo l'evento
            dmin = min(zona_dist(evento["Z"], P[i]) for i in range(len(T)) if T[i] >= evento["t_b"])
            R["avviso_" + k] = {"t": None if best is None else best[0], "dist_zona_al_avviso_m": None if best is None else round(best[1], 1),
                                "ritardo_dal_vero_s": None if (best is None or t_ev is None) else round(best[0] - t_ev, 2),
                                "dist_min_dopo_m": round(float(dmin), 1),
                                "dist_dal_frammento_vero_piu_vicino_al_avviso_m": None if (best is None or best[2] is None) else round(best[2], 1)}
        R["tracce_avvisate"] = len(avvisati)
    return R


def _lavoro(a):
    try:
        return a, passaggio(*a)
    except Exception as e:
        import traceback
        return a, {"errore": repr(e), "traccia": traceback.format_exc()[-1500:]}


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round((c - h) / d, 4), round((c + h) / d, 4))


def aggrega(rr):
    n = len(rr)
    A = {"n": n}
    rit = [r["ritardo_evento_s"] for r in rr]
    k2 = sum(x is not None and x <= 2.0 for x in rit)
    A["evento_dichiarato"] = [sum(r["evento"] is not None for r in rr), n]
    A["entro_2s"] = [k2, n, *wilson(k2, n)]
    ok = [x for x in rit if x is not None]
    A["ritardo_s_min_mediana_max"] = [min(ok), float(np.median(ok)), max(ok)] if ok else None
    kf = sum(r["falso_evento"] for r in rr)
    A["falsi_eventi"] = [kf, n, *wilson(kf, n)]
    dv = [sum(r["frammenti_dentro_V"][0] for r in rr), sum(r["frammenti_dentro_V"][1] for r in rr)]
    A["frammenti_dentro_V_campioni"] = [*dv, round(dv[0] / dv[1], 5) if dv[1] else None]
    kp = sum(r["frammenti_dentro_V"][1] > 0 and r["frammenti_dentro_V"][0] == r["frammenti_dentro_V"][1] for r in rr)
    A["passaggi_con_tutti_i_frammenti_in_V"] = [kp, n, *wilson(kp, n)]
    A["libero_in_impronta_punti"] = [sum(r["libero_in_impronta_punti"][0] for r in rr), sum(r["libero_in_impronta_punti"][1] for r in rr)]
    kl = sum(r["libero_su_frammento_in_impronta"][0] > 0 for r in rr)
    A["passaggi_con_libero_su_frammento"] = [kl, n, *wilson(kl, n)]
    A["libero_su_frammento_istanti"] = [sum(r["libero_su_frammento_in_impronta"][0] for r in rr), sum(r["libero_su_frammento_in_impronta"][1] for r in rr)]
    for k in ("avviso_persona1", "avviso_mezzo1"):
        xs = [r.get(k) for r in rr if r.get(k) is not None]
        if not xs and not any(k in r for r in rr):
            continue
        if k == "avviso_persona1":
            ka = sum(x["ritardo_dal_vero_s"] is not None and x["ritardo_dal_vero_s"] <= 2.0 for x in xs)
        else:
            ka = sum(x["dist_zona_al_avviso_m"] is not None and x["dist_zona_al_avviso_m"] >= SOGLIE["d_avv_mezzo_m"] for x in xs)
        A[k + "_riuscito"] = [ka, n, *wilson(ka, n)]
        kf = sum(x.get("dist_dal_frammento_vero_piu_vicino_al_avviso_m") is not None and x["dist_dal_frammento_vero_piu_vicino_al_avviso_m"] >= SOGLIE["d_avv_mezzo_m"] for x in xs)
        A[k + "_a_140m_dai_frammenti_veri"] = [kf, n, *wilson(kf, n)]
        A[k + "_ritardo_dal_vero_max_s"] = max([x["ritardo_dal_vero_s"] for x in xs if x["ritardo_dal_vero_s"] is not None], default=None)
        A[k + "_dati"] = {"avvisati": sum(x["t"] is not None for x in xs),
                          "dist_al_avviso_min": min([x["dist_zona_al_avviso_m"] for x in xs if x["dist_zona_al_avviso_m"] is not None], default=None),
                          "dist_min_dopo_min": min([x["dist_min_dopo_m"] for x in xs], default=None)}
    kc = [max(r["salute_cicli"].values()) for r in rr if r["salute_cicli"]]
    A["salute_cicli_max"] = max(kc) if kc else None
    A["passaggi_camere_dichiarate_entro_3"] = sum(len([v for v in r["salute_cicli"].values() if v <= 3]) >= 2 for r in rr)
    A["tipi_evento"] = sorted(set(r["evento"]["tipo"] for r in rr if r["evento"]))
    return A


def main():
    from multiprocessing import Pool
    N12 = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    N4 = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    N5 = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    NP = min(int(sys.argv[4]) if len(sys.argv) > 4 else 7, 7)              # 7 figli + il padre = 8 processi
    t0 = time.time()
    N2 = int(os.environ.get("EVENTI_N_E2", N12))                         # v3: n per E2 a parte
    lav = [("E2", "alta", i) for i in range(N2)] + [("E1", "alta", i) for i in range(N12)]
    lav += [("E4", c, i) for c in ("alta", "min") for i in range(N4)]
    lav += [("E5", "alta", i, 5.0) for i in range(N5)]
    with Pool(NP) as p:
        righe = p.map(_lavoro, lav, chunksize=1)
    agg = {}
    with open(os.path.join(QUI, "passaggi_v3.jsonl"), "w", encoding="utf-8") as f:
        for (a, r) in righe:
            f.write(json.dumps({"lavoro": list(a), **r}, ensure_ascii=False, default=float) + "\n")
            key = "%s/%s" % (a[0], a[1]) + ("/sep%.1f" % a[3] if len(a) > 3 else "")
            agg.setdefault(key, []).append(r)
    out = {}
    for key, rr in agg.items():
        err = [r for r in rr if "errore" in r]
        ok = [r for r in rr if "errore" not in r]
        out[key] = dict(aggrega(ok) if ok else {}, errori=len(err), esempio_errore=err[0]["traccia"] if err else None)
    ris = {"avvertenza": "SIMULAZIONE; strato eventi v2 scritto da me; stesso simulatore e stesso autore della misura (non indipendente)",
           "nucleo": NUCLEO, "soglie": SOGLIE, "inviluppo_scenario": INV_S, "semi": "SeedSequence(20261116, ...) nuovi",
           "durata_s": round(time.time() - t0, 1), "n": {"E1_E2": N12, "E4": N4, "E5_5m": N5}, "risultati": out}
    with open(os.path.join(QUI, "risultati_v3.json"), "w", encoding="utf-8") as f:
        json.dump(ris, f, ensure_ascii=False, indent=1, default=float)
    print(json.dumps(ris, ensure_ascii=False, default=float)[:8000])


if __name__ == "__main__":
    main()
