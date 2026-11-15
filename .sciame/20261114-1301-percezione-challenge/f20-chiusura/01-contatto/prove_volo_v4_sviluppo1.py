"""prove_volo_v4.py - NUCLEO v4 = copia di f19-volo/10-prove/prove_volo.py in modalita' v3i (inviluppo 210 m/s nel
nucleo), piu' la regola di contatto v4c (f20-chiusura/01-contatto). Doppler SIMULATO sui ritorni radar (ipotesi).
Origine: prove F1-F6 (volo ad alta velocita') sul nucleo MoVi v3 e sullo strato eventi v3 (sciame-validazione,
f19-volo/10-prove). Nessun file esistente e' modificato: eventi_v3.py, movi_lp_v3.py, sim_lp.py, eventi_lp.py ed
eventi_volo.py sono SOLO importati. Il passaggio di eventi_v3 e' riusato tale e quale (sorgente letta con inspect) con
UN gancio aggiunto a ogni ciclo, che misura continuita', calibrazione della confidenza, avviso di prossimita', 'libero'
sul vero e, a richiesta, scrive il registro per fotogramma.

Uso:  python -I -B prove_volo.py N N6 [processi]        -> passaggi_volo.jsonl, risultati_volo.json
      python -I -B prove_volo.py --registro DIR          -> un registro per scenario (idx 0, cfg sda), seme dichiarato prima
Configurazioni: att = sensori f15 + latenza CPU; sda = radar AESA 10 Hz + camere 10 Hz + latenza dedicata (STIMA).
Tutto e' SIMULAZIONE. Stesso simulatore degli scenari: il controllo non e' indipendente dalla fisica ipotizzata.
"""
import copy
import inspect
import json
import math
import os
import sys
import time

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(QUI))
F19 = os.path.join(RADICE, "f19-volo")
sys.path.insert(0, os.path.join(RADICE, "f15-lunga-portata", "60-fase2c", "01-correzioni"))
sys.path.insert(0, os.path.join(F19, "04-scenari"))
sys.path.insert(0, os.path.join(F19, "03-confidenza"))
import numpy as np  # noqa: E402

import eventi_v3 as EV  # noqa: E402
import eventi_volo as EVV  # noqa: E402
import stima_v4 as SV  # noqa: E402

m, S, EL, FR = EV.m, EV.S, EV.EL, EV.FR
SCV = {x["id"]: x for x in json.load(open(os.path.join(F19, "04-scenari", "scenari_volo.json"), encoding="utf-8"))["scenari"]}
PV = json.load(open(os.path.join(F19, "02-sensori-hw", "parametri_volo.json"), encoding="utf-8"))
LAT = json.load(open(os.path.join(F19, "02-sensori-hw", "latenza.json"), encoding="utf-8"))

# ---- classi nuove (etichette a mano) -> classi delle regole f15 e RCS (I)
EL.CLASSE.update({"aereo_volo": "aereo_linea_avvicinamento", "drone_veloce": "drone_ala_fissa"})
EL.RCS.update({"aereo_volo": 20.0, "drone_veloce": 0.05})
PORTA_G = {"aereo_volo": 50.0, "aereo_leggero": 50.0, "drone_veloce": 30.0, "multirotore": 30.0}   # I (conti_volo.json)
T_FINE = {"F1": 92.0, "F2": 75.0, "F3": 45.0, "F4": 60.0, "F5": 52.0, "F6": 40.0}                # I: finestra utile
K99_3D = 11.3449                                                                                   # chi2_3(0,99)

# ---- latenze (s): scheda + elaborazione. CPU: somma dei massimi CPU degli stadi trasferimento, segnale, plot,
# inseguimento, bus di latenza.json = 2 + 20 + 2 + 55 + 1 = 80 ms. Dedicato: 0,01 + 0,5 + 0,1 + 0,5 + 0,1 = 1,2 ms (STIMA).
def _somma_stadi(chiave):
    tot = 0.0
    for st in LAT["stadi"]:
        if st["stadio"].startswith(("trasferimento", "elaborazione segnale", "rilevamento", "associazione", "uscita: verso macchina")):
            tot += st["ms"][chiave][1]
    return tot / 1000.0


ELAB = {"att": _somma_stadi("cpu"), "sda": _somma_stadi("dedicato")}
USCITA = {"operatore": 0.050, "bordo": 0.001}                  # latenza.json: schermo 60 Hz (max 50 ms); bus (I)
RISPOSTA = {"operatore": LAT["risposte_s"]["umano_con_avviso_che_da_direzione"], "bordo": LAT["risposte_s"]["macchina"]}
RIT_MEZZO = LAT["ritardo_mezzo_s"]


def par_sensore(tipo, cfg):
    par = dict(EV.CAT[tipo])
    if cfg == "att":
        par["latenza_s"] = par.get("latenza_s", 0.1) + ELAB["att"]
        return par
    a = PV["sensori"]
    if par["tipo"] == "radar":                                 # radar AESA (EchoShield, brochure NON APERTA) a 4 pannelli (I)
        r = a["radar_aesa_traccia_droni"]
        par.update(periodo_s=r["rivisita_s"][0], rotante=False, sigma_az_rad=math.radians(r["accuratezza_ang_deg"][0]),
                   sigma_el_rad=math.radians(r["accuratezza_ang_deg"][0]), latenza_s=r["latenza_s"][0] + ELAB["sda"],
                   r_rif_m=1400.0, rcs_rif_m2=0.01, pd_rif=0.5, el_campo=[-10.0, 80.0], falsi_per_passata=0.05,
                   fonte="sda: rivisita e accuratezza da parametri_volo.json (EchoShield, NON APERTA); r_rif 1400 m per 0,01 m2 a "
                         "Pd 0,5 (I, prudente: Matrice 600 tipica 1400 m); 360 gradi con 4 pannelli (I); falsi 0,05 per rivisita (I)")
    elif par["tipo"] == "camera":                              # torretta EO/MWIR (CM202A/SupIR, classe), a 10 Hz nel simulatore
        c = a["eo_ir_brandeggio_veloce"]
        par.update(periodo_s=0.1, latenza_s=c["latenza_s"][0] + ELAB["sda"],
                   fonte="sda: latenza 0,05 s (I, parametri_volo.json); 10 Hz (la scheda dice 30 Hz: ridotto per il passo del simulatore)")
    return par


# ---------------------------------------------------------------------------------------------- verita' e sensori
def prepara_volo(eid, cfg, idx, sep=None, seme_base=20261119):
    sc = SCV[eid]
    ss_v = np.random.SeedSequence(seme_base, spawn_key=(200 + int(eid[1]), 0, idx))
    ss_s = np.random.SeedSequence(seme_base, spawn_key=(200 + int(eid[1]), 1 + ("att", "sda").index(cfg), idx))
    rv, rs = np.random.default_rng(ss_v), np.random.default_rng(ss_s)
    ogg = {o["id"]: json.loads(json.dumps(o)) for o in sc["oggetti"]}
    eventi = sc.get("eventi", [])
    t_fine = T_FINE[eid]
    if sep is not None and eid == "F5":                       # variante della durata della cecita'
        eventi = json.loads(json.dumps(eventi))
        for e in eventi:
            if e["tipo"] == "perdita_ottici_totale":
                e["parametri"]["durata_s"] = sep
    ver = {k: S.genera_verita(o, "nominale", 1.0, rv, t_fine=t_fine) for k, o in ogg.items()}
    t_ev, p_ev, t_terra = None, None, None
    for e in eventi:
        if e["tipo"] in ("collisione", "avaria_motore"):
            t_ev = e["t"]
            pe = dict(e["parametri"])
            p_ev = np.asarray(pe["p"], float)
            src = pe["oggetti"] if "oggetti" in pe else [pe["oggetto"]]
            i_ev = int(round(t_ev / 0.1))
            pe["vc"] = np.mean([ver[s][2][i_ev] for s in src], 0)
            pe["p"] = np.mean([ver[s][1][i_ev] for s in src], 0)
            p_ev = pe["p"]
            fr = EVV.frammenti_volo(pe, rv, dt=0.05, t_max=t_fine - t_ev)        # semi-implicito (stabile)
            prof = EV.PAR_COLL if eid == "F3" else EV.PAR_AVAR
            Tf = np.arange(0, t_fine + 0.05, 0.1)
            tt = []
            for j, (T, P, vt, un) in enumerate(fr):
                Pi = np.stack([np.interp(Tf - t_ev, T, P[:, c]) for c in range(3)], 1)
                Pf = np.where((Tf >= t_ev)[:, None], Pi, EV.LONTANO)
                Vf = np.gradient(Pf, 0.1, axis=0)
                Vf[Tf < t_ev + 0.1] = 0.0
                ver["fr%02d" % j] = (Tf, Pf, Vf)
                ogg["fr%02d" % j] = {"classe": "frammento", "ingombro": [0.05], "t0": t_ev,
                                     "conforme": bool(vt >= prof["v_t_min"] and un <= prof["dv"])}
                g = np.nonzero(P[:, 2] <= 0)[0]
                if len(g):
                    tt.append(T[g[0]])
            t_terra = (t_ev + min(tt)) if tt else None
            if eid == "F3":                                    # droneB: caduta balistica (come E1)
                T, P, V = ver["droneB"]
                for i in range(i_ev + 1, len(T)):
                    va = V[i - 1]
                    a = np.array([0, 0, -EV.G]) - EV.G / 15.0 ** 2 * np.linalg.norm(va) * va
                    V[i] = V[i - 1] + a * 0.1 if P[i - 1, 2] > 0 else 0 * V[i - 1]
                    P[i] = np.maximum(P[i - 1] + V[i] * 0.1, [-1e9, -1e9, 0])
    salute_cam = {}
    for e in eventi:
        if e["tipo"] == "fiammata":
            p = e["parametri"]
            salute_cam = {"camera_eo_ottica_lunga": [(e["t"], p["cieca_eo_fino_a_t"], "abbagliamento")],
                          "camera_termica_ottica_lunga": [(e["t"], p["cieca_termica_fino_a_t"], "abbagliamento")]}
    lista = [s for s in sc["sensori"] if EV.CAT[s["tipo"]]["tipo"] in ("radar", "camera")]     # ADS-B spento (I prudente)
    sensori, griglie, nuc = [], [], {}
    for i, sd in enumerate(lista):
        par = par_sensore(sd["tipo"], cfg)
        nome = "%s#%d" % (sd["tipo"], i)
        cec = EVV.finestre_cecita([e for e in eventi if e["tipo"] == "perdita_ottici_totale"], sd["tipo"]) + salute_cam.get(sd["tipo"], [])
        s = EVV.SensoreVolo(nome, sd["pos"], par, sd["tipo"], nubi_quota=sc.get("nubi_quota", []), cecita=cec, meteo=1.0, ostacoli=[], nubi=[])
        sensori.append(s)
        if par["tipo"] in ("radar", "lidar"):
            r_max = min(par["r_max_m"], 1500.0)
            sn = m.Sensore(nome, sd["pos"], par)
            el = tuple(np.radians(np.linspace(-2, 20, 6)))
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
        r = [EL.unisci_non_risolti(rc, ver, s.par) for rc in r]
        for rc in r:
            for (oid, *_x) in rc["ril"]:
                if oid is not None:
                    radar_ril.setdefault(oid, []).append(rc["t"])
        recs += r
    tt = {k: np.array(sorted(v)) for k, v in radar_ril.items()}
    for s in sensori:
        if s.tipo == "camera":
            recs += s.scansioni(ver, t_fine, rs, rcs, cue=(lambda oid, t: oid in tt and np.any((tt[oid] <= t) & (tt[oid] >= t - 5.0))))
    recs.sort(key=lambda r: (r["t_consegna"], r["sensore"]))
    # v4c: velocita' radiale (Doppler) SIMULATA su ogni ritorno radar: v_r = v_vera . los + N(0, SIGMA_VR) (ipotesi)
    rd = np.random.default_rng(ss_s.spawn(2)[1])
    pos_s = {s.nome: np.asarray(s.pos, float) for s in sensori}
    D_dop = []
    for rc in recs:
        if not any(s.nome == rc["sensore"] and s.tipo == "radar" for s in sensori):
            continue
        for (oid, z, Rm, ex) in rc["ril"]:
            los = np.asarray(z, float) - pos_s[rc["sensore"]]
            los /= max(np.linalg.norm(los), 1e-9)
            if oid is not None:
                Tv, Pv, Vv = ver[oid]
                vv = Vv[min(int(round(ex["t_ril"] / 0.1)), len(Tv) - 1)]
                vr = float(vv @ los) + rd.normal(0, CONTATTO["sigma_vr"])
            else:
                vr = float(rd.normal(0, 3.0))
            D_dop.append((round(float(ex["t_ril"]), 3), np.asarray(z, float), vr, los))
    ing_max = max(max(o["ingombro"]) for o in ogg.values() if o["classe"] != "frammento")
    D = dict(sc=sc, ogg=ogg, ver=ver, t_ev=t_ev, p_ev=p_ev, t_fiam=None, sensori=sensori, griglie=griglie, nuc=nuc,
             recs=recs, t_fine=t_fine, nubi=[], rng_bear=np.random.default_rng(ss_s.spawn(1)[0]), ing_max=ing_max)
    D["t_terra"], D["eventi_sc"], D["eid"], D["cfg"] = t_terra, eventi, eid, cfg
    D["doppler"] = D_dop
    D["periodo_radar"] = min(s.par["periodo_s"] for s in sensori if s.tipo == "radar")
    _G["D"] = D
    return D


# ---------------------------------------------------------------------------------------------- gancio per ciclo
_G = {}


def _pos(D, k, t):
    T, P, _ = D["ver"][k]
    return P[min(int(round(t / 0.1)), len(T) - 1)]


def _oggetto_di(D, tr, princ):
    best, dmin = None, 1e18
    for k in princ:
        d = float(np.linalg.norm(tr.p_ultima - _pos(D, k, tr.t_vista)))
        if d < dmin:
            best, dmin = k, d
    soglia = 3 * tr.sigp_ultima + 0.5 * max(D["ogg"][best]["ingombro"]) + 30.0 if best else 0
    return best if (best is not None and dmin <= soglia) else None


def _cpa(p1, v1, p2, v2):
    dp, dv = p2 - p1, v2 - v1
    tc = 0.0 if float(dv @ dv) < 1e-9 else max(0.0, -float(dp @ dv) / float(dv @ dv))
    return tc, float(np.linalg.norm(dp + dv * tc))


REGOLA = os.environ.get("VOLO_REGOLA", "v4c")
IDX0 = int(os.environ.get("VOLO_IDX0", "0"))     # v4c: primo indice di passaggio (semi nuovi per la valutazione)
if REGOLA in ("v4", "v3i", "v4c"):     # v3i = regole eventi v3 + solo questa correzione dell'inviluppo
    # v4 (A POSTERIORI, dopo F6/att e F4: vero fuori dall'insieme di presenza): l'insieme di presenza del NUCLEO usava
    # l'inviluppo delle classi (v_max 90 m/s), non la correzione a 210 m/s del coordinatore, che stava solo nello strato
    # eventi. Qui la si porta anche nel nucleo (senza toccare movi_lp_v3.py: si avvolge m.inviluppo).
    _inv_orig = m.inviluppo

    def _inv_210(regole, classi):
        d = dict(_inv_orig(regole, classi))
        d["v_max"] = max(d["v_max"], 210.0)
        return d
    m.inviluppo = _inv_210
CONTATTO = {"sigma_vr": 0.5,          # m/s, Doppler simulato (ipotesi)
            "n_risolta": 3,           # aggiornamenti con la coppia separata oltre la risoluzione, prima
            "dv_rel_min": 10.0,       # m/s, velocita' relativa minima della coppia (tabella 4 del verdetto)
            "orizzonte_s": 10.0,      # CPA previsto entro questo tempo
            "finestra_s": 4.0,        # dopo il contatto previsto, finestra per (a) e (b)
            "n_dop": 3,               # aggiornamenti Doppler consecutivi fuori norma
            "dvr_min": 5.0, "k_vr": 4.0,
            "r_nuove_m": 150.0, "n_nuove": 2, "gate_dop_m": 30.0}
V4 = {"memoria_contatto_s": 4.0, "dv_min_m_s": 10.0, "k_sigv": 4.0, "finestra_prima_s": 2.0}


def regola_v4(D, ins, tk, evento, A):
    """v4 (A POSTERIORI, dopo il passaggio F3 idx 0 senza evento): 'contatto con impulso cinematico'. Si apre l'evento
    'contatto (dedotto)' se due tracce confermate sono state in contatto (d <= ingombro massimo dello scenario +
    3 (sigma_a + sigma_b)) negli ultimi 4 s E, dopo l'inizio del contatto, almeno una delle due ha cambiato velocita'
    di |dv| >= max(10 m/s, 4 sigma_v) rispetto alla media dei 2 s prima del contatto. Nessuna etichetta usata."""
    st = A.setdefault("v4", {"storia": {}, "contatti": {}})
    conf = [tr for tr in ins.tracce if tr.confermata]
    for tr in conf:
        h = st["storia"].setdefault(tr.id, [])
        if not h or h[-1][0] != tr.t_vista:
            h.append((tr.t_vista, tr.v_ultima.copy(), tr.sigv_ultima))
            del h[:-80]
    if evento is not None or len(conf) < 2:
        return None
    X = np.array([tr.x[:3] for tr in conf])
    sg = np.array([math.sqrt(np.trace(tr.P[:3, :3]) / 3) for tr in conf])
    dd = np.linalg.norm(X[None] - X[:, None], axis=2) - (D["ing_max"] + 3 * (sg[None] + sg[:, None]))
    for a, b in zip(*np.nonzero(np.triu(dd <= 0, 1))):
        k = (conf[a].id, conf[b].id)
        c = st["contatti"].setdefault(k, [tk, tk])
        if tk - c[1] > 0.6:
            c[0] = tk
        c[1] = tk
    for (ia, ib), (t0, t1) in list(st["contatti"].items()):
        if tk - t1 > V4["memoria_contatto_s"]:
            continue
        pair = [tr for tr in conf if tr.id in (ia, ib)]
        if len(pair) < 1:
            continue
        for tr in pair:
            h = st["storia"].get(tr.id, [])
            prima = [v for (t, v, s) in h if t0 - V4["finestra_prima_s"] <= t < t0]
            if len(prima) < 2 or tr.t_vista <= t0:
                continue
            vm = np.mean(prima, 0)
            dv = float(np.linalg.norm(tr.v_ultima - vm))
            if dv >= max(V4["dv_min_m_s"], V4["k_sigv"] * tr.sigv_ultima):
                orig = [x for x in pair if tk - x.t_vista <= EV.SOGLIE["eta_max_origine_s"]] or [tr]
                ev = EV.apri_evento(D, tk, t0, orig, "contatto (impulso, v4)", EV.PAR_COLL)
                return ev
    return None


def _risoluzione(D, p):
    """Cella di risoluzione del radar piu' fine (2 sigma in distanza e in angolo, come unisci_non_risolti), in metri."""
    best = 1e18
    for s in D["sensori"]:
        if s.tipo != "radar":
            continue
        r = float(np.linalg.norm(np.asarray(p, float) - np.asarray(s.pos, float)))
        best = min(best, max(2 * s.par["sigma_r_m"], 2 * r * s.par["sigma_az_rad"], 2 * r * s.par.get("sigma_el_rad", s.par["sigma_az_rad"])))
    return best


def _dop_di(D, tr):
    """Ritorno radar (con v_r) dell'aggiornamento piu' recente della traccia: stesso istante, entro gate_dop_m."""
    tv = round(float(tr.t_vista), 3)
    idx = D.setdefault("_dop_idx", {})
    if not idx:
        for (t, z, vr, los) in D["doppler"]:
            idx.setdefault(t, []).append((z, vr, los))
    cand = idx.get(tv, [])
    if not cand:
        return None
    dz = [float(np.linalg.norm(z - tr.p_ultima)) for (z, _, _) in cand]
    j = int(np.argmin(dz))
    return cand[j] if dz[j] <= CONTATTO["gate_dop_m"] + 3 * tr.sigp_ultima else None


def regola_v4c(D, ins, tk, evento, A):
    """v4c - collisione/frammentazione in volo per CONTATTO. Nessuna lettura della verita'.
    1. coppia di tracce confermate RISOLTA: separata oltre R_c = ing_max + 3(sa+sb) + cella di risoluzione per almeno
       n_risolta aggiornamenti comuni (i doppioni, sempre dentro R_c, non diventano mai coppia);
    2. CONVERGENTE: |v_b - v_a| >= dv_rel_min e punto di massimo avvicinamento (velocita' costante) entro orizzonte_s
       sotto R_c; si memorizzano t_c, p_c e le velocita' di prima;
    3. entro finestra_s da t_c: (a) la coppia si fonde (d <= R_c) o una traccia sparisce (non aggiornata da 1,5 periodi)
       E (b) almeno n_nuove tracce nuove confermate nate dopo t_c - 1 s entro r_nuove_m da p_c, OPPURE per n_dop
       aggiornamenti consecutivi di una delle due tracce la v_r misurata e' incompatibile con ENTRAMBE le velocita' di
       prima (|v_r - v_pre.los| > max(dvr_min, k_vr sigma_vr)): cosi' lo scambio d'identita' non basta."""
    C = CONTATTO
    st = A.setdefault("v4c", {"coppie": {}, "dop": {}, "ultimo": {}})
    if evento is not None:
        return None
    conf = [tr for tr in ins.tracce if tr.confermata]
    per = D["periodo_radar"]
    tutte = {tr.id: tr for tr in ins.tracce + ins.chiuse}
    for i in range(len(conf)):
        for j in range(i + 1, len(conf)):
            a, b = conf[i], conf[j]
            k = (min(a.id, b.id), max(a.id, b.id))
            c = st["coppie"].setdefault(k, {"ris": 0, "t_ult": -1.0, "conv": None, "fusa": False})
            tcom = min(a.t_vista, b.t_vista)
            if tcom <= c["t_ult"] + 1e-9:
                continue
            c["t_ult"] = tcom
            sa = math.sqrt(np.trace(a.P[:3, :3]) / 3)
            sb = math.sqrt(np.trace(b.P[:3, :3]) / 3)
            pm = 0.5 * (a.x[:3] + b.x[:3])
            Rc = D["ing_max"] + 3 * (sa + sb) + _risoluzione(D, pm)
            d = float(np.linalg.norm(a.x[:3] - b.x[:3]))
            if c["conv"] is None or tk < c["conv"]["t_c"] - 0.3:
                if d > Rc:
                    c["ris"] += 1
                dv = b.x[3:] - a.x[3:]
                tc, dmin = _cpa(a.x[:3], a.x[3:], b.x[:3], b.x[3:])
                if c["ris"] >= C["n_risolta"] and d > Rc and float(np.linalg.norm(dv)) >= C["dv_rel_min"] and tc <= C["orizzonte_s"] and dmin <= Rc:
                    c["conv"] = {"t_c": tk + tc, "p_c": 0.5 * (a.x[:3] + b.x[:3] + (a.x[3:] + b.x[3:]) * tc),
                                 "vpre": [a.x[3:].copy(), b.x[3:].copy()], "Rc": Rc}
                elif c["conv"] is not None and dmin > 2 * Rc:
                    c["conv"] = None                              # non converge piu'
            if c["conv"] is not None and d <= max(Rc, c["conv"]["Rc"]) and tk >= c["conv"]["t_c"] - 1.0:
                c["fusa"] = True
    for k, c in st["coppie"].items():
        cv = c["conv"]
        if cv is None or not (cv["t_c"] - 0.5 <= tk <= cv["t_c"] + C["finestra_s"]):
            continue
        ta, tb = tutte.get(k[0]), tutte.get(k[1])
        spar = any(t is None or t in ins.chiuse or tk - t.t_vista > 1.5 * per for t in (ta, tb))
        a_ok = c["fusa"] or spar
        if not a_ok:
            continue
        nuove = [t for t in conf if t.id not in k and t.t_nascita >= cv["t_c"] - 1.0
                 and float(np.linalg.norm(t.x[:3] - cv["p_c"])) <= C["r_nuove_m"]]
        b_ok = len(nuove) >= C["n_nuove"]
        perche = "tracce nuove vicino al punto" if b_ok else None
        if not b_ok:
            for t in (ta, tb):
                if t is None or t.t_vista < cv["t_c"] - 0.05:
                    continue
                q = st["dop"].setdefault((k, t.id), {"t": -1.0, "n": 0})
                if t.t_vista <= q["t"] + 1e-9:
                    if q["n"] >= C["n_dop"]:
                        b_ok, perche = True, "cambio di velocita' sostenuto (Doppler)"
                    continue
                q["t"] = t.t_vista
                m_ = _dop_di(D, t)
                if m_ is None:
                    continue
                z, vr, los = m_
                soglia = max(C["dvr_min"], C["k_vr"] * C["sigma_vr"])
                if all(abs(vr - float(vp @ los)) > soglia for vp in cv["vpre"]):
                    q["n"] += 1
                else:
                    q["n"] = 0
                if q["n"] >= C["n_dop"]:
                    b_ok, perche = True, "cambio di velocita' sostenuto (Doppler)"
        if b_ok:
            orig = [t for t in (ta, tb) if t is not None] or nuove
            ev = EV.apri_evento(D, tk, min(cv["t_c"], tk), orig, "collisione/frammentazione in volo (contatto v4c: %s)" % perche, EV.PAR_COLL)
            A["v4c_innesco"] = {"t": round(tk, 2), "coppia": list(k), "t_c_previsto": round(cv["t_c"], 2), "perche": perche}
            return ev
    return None


def gancio(D, ins, tk, evento, dichiarato):
    A = _G.setdefault("A", {"calib": [], "buchi": {}, "campioni": {}, "prox": None, "lib_vero": [0, 0], "assoc": {},
                            "registro": [] if _G.get("registro") else None})
    nuovo = regola_v4(D, ins, tk, evento, A) if REGOLA == "v4" else (regola_v4c(D, ins, tk, evento, A) if REGOLA == "v4c" else None)
    if nuovo is not None:
        evento = nuovo
    _gancio_misure(D, ins, tk, evento, dichiarato, A)
    return nuovo


def _gancio_misure(D, ins, tk, evento, dichiarato, A):
    reg = A["registro"] is not None
    if not reg and abs(tk * 2 - round(tk * 2)) > 1e-6:          # ogni 0,5 s (ogni 0,1 s nel registro)
        return
    princ = [k for k in D["ogg"] if D["ogg"][k]["classe"] != "frammento"]
    conf = [tr for tr in ins.tracce if tr.confermata]
    soglia_perdita = 1.5 * D["periodo_radar"]
    righe = []
    prev = {}
    for tr in conf:
        c = copy.deepcopy(tr)
        c.prevedi(tk)
        prev[tr.id] = c
    copertura = {k: False for k in princ}
    # v3b (correzione della MISURA, non del nucleo): un campione di perdita conta solo se NESSUNA traccia confermata
    # vede l'oggetto (tau <= soglia) e si prende la traccia piu' recente dell'oggetto; i doppioni stantii non contano.
    assoc = {tr.id: _oggetto_di(D, tr, princ) for tr in conf}
    visti = {assoc[tr.id] for tr in conf if tk - tr.t_vista <= soglia_perdita}
    ultima = {}
    for tr in conf:
        k = assoc[tr.id]
        if k is not None and (k not in ultima or tr.t_vista > ultima[k].t_vista):
            ultima[k] = tr
    for tr in conf:
        c = prev[tr.id]
        k = assoc[tr.id]
        tau = tk - tr.t_vista
        Sg = c.P[:3, :3]
        cl = D["ogg"][k]["classe"] if k else None
        g = PORTA_G.get(cl, 30.0)
        Cg = float(SV.prob_gauss_ellissoide(c.x[:3], Sg, c.x[:3], g * g * np.eye(3), n=24)) if (tau > soglia_perdita or reg) else None
        ip = m.insieme_presenza(tr, tk, EV.REG, EV.REG["scenari"][EV.FAM]["classi_ammesse"])
        if k is not None:
            pv = _pos(D, k, tk)
            e = pv - c.x[:3]
            d2 = float(e @ np.linalg.solve(Sg, e))
            in99 = d2 <= K99_3D
            in_ip = float(np.linalg.norm(pv - ip["centro"])) <= ip["raggio"]
            copertura[k] = copertura[k] or in99 or in_ip
            if tau > soglia_perdita and k not in visti and ultima.get(k) is tr:
                A["calib"].append((round(tk, 2), round(tau, 2), round(Cg, 4), bool(float(np.linalg.norm(e)) <= g), bool(in99), bool(in_ip), k, cl, round(float(np.linalg.norm(e)), 1), round(math.sqrt(max(np.linalg.eigvalsh(Sg)[-1], 0.0)), 1)))
            if abs(tk - 38.5) < 1e-6 or abs(tk - 46.0) < 1e-6:        # F5: chi e' chi prima e dopo la cecita'
                A["assoc"].setdefault(round(tk, 1), {})
                best = min(princ, key=lambda q: float(np.linalg.norm(c.x[:3] - _pos(D, q, tk))))
                A["assoc"][round(tk, 1)][tr.id] = best
        if reg:
            sig = math.sqrt(max(np.linalg.eigvalsh(Sg)[-1], 0.0))
            righe.append({"id": tr.id, "oggetto_vero": k, "classe_mano": cl, "pos": [round(float(x), 1) for x in c.x[:3]],
                          "vel": [round(float(x), 1) for x in c.x[3:]], "non_vista_da_s": round(tau, 2),
                          "parola": "vista" if tau <= soglia_perdita else ("previsto ampio" if tr.ampio else "non vista da %.1f s con zona" % tau),
                          "confidenza_C": None if Cg is None else round(Cg, 4), "porta_m": g, "r99_m": round(3.368 * sig, 1),
                          "insieme_presenza_r_m": round(float(ip["raggio"]), 1)})
    # oggetti a terra dentro l'impronta dichiarata: coperti (possibile presenza di detriti)
    if evento is not None:
        for k in princ:
            if not copertura[k] and EV.zona_dist(evento["Z"], _pos(D, k, tk)) <= 0:
                copertura[k] = True
    for k in princ:
        A["campioni"].setdefault(k, 0)
        A["buchi"].setdefault(k, 0)
        visto = any(_oggetto_di(D, tr, princ) == k for tr in ins.tracce + ins.chiuse if tr.confermata)
        if not visto:
            continue
        if _pos(D, k, tk)[2] <= 0.5 and D["ogg"][k].get("dopo_evento") and evento is None:
            continue
        A["campioni"][k] += 1
        A["buchi"][k] += int(not copertura[k])
    # avviso di prossimita' (CPA previsto < 150 m, CV, orizzonte 120 s) fra tracce confermate
    if A["prox"] is None:
        for i in range(len(conf)):
            for j in range(i + 1, len(conf)):
                a, b = prev[conf[i].id], prev[conf[j].id]
                tc, d = _cpa(a.x[:3], a.x[3:], b.x[:3], b.x[3:])
                d_ora = float(np.linalg.norm(a.x[:3] - b.x[:3]))
                if tc <= 120.0 and d < 150.0 and d_ora > 300.0:      # I: le coppie gia' vicine (doppioni) non contano
                    A["prox"] = (round(tk, 2), round(tc, 2), round(d, 1))
    # 'libero' sul vero (ogni 1 s): il punto dove l'oggetto E' dichiarato libero?
    if abs(tk - round(tk)) < 1e-6 and D["griglie"]:
        for k in princ:
            p = _pos(D, k, tk)
            A["lib_vero"][1] += 1
            A["lib_vero"][0] += int(EV.stato_v2(D, list(p), tk, EV.CL_FR) == m.LIBERO)
    if reg:
        fr_aria = sum(1 for k in D["ver"] if k.startswith("fr") and _pos(D, k, tk)[2] > 0 and _pos(D, k, tk)[0] < 1e6)
        ev = None
        if evento is not None:
            tau = tk - evento["t_a"]
            r, tq, zmin, zmax, Tc = FR.inviluppo(tau, evento["ev"], evento["par"])
            ev = {"tipo": evento["tipo"] + " (dedotto)", "t_dichiarato": evento["t_b"], "t_a": evento["t_a"],
                  "volume_V": {"r_pianta_m": round(float(r), 1), "z_min_m": round(float(zmin), 1), "z_max_m": round(float(zmax), 1)},
                  "impronta": {"centro": [round(float(x), 1) for x in evento["Z"]["c"]], "R_m": round(evento["Z"]["R"], 1),
                               "ispezionati": [int(evento["Z"]["isp"].sum()), len(evento["Z"]["isp"])]},
                  "parola": "possibile presenza di detriti nel volume e nell'impronta: zona non verificata"}
        aff = {s.nome: ("affidabilita' persa" if s.nome in dichiarato else "affidabile") for s in D["sensori"]}
        A["registro"].append({"t": round(tk, 2), "tracce": righe, "evento": ev, "affidabilita_sensori": aff,
                              "verita": {k: [round(float(x), 1) for x in _pos(D, k, tk)] for k in princ},
                              "frammenti_veri_in_aria": fr_aria, "avviso_prossimita": A["prox"]})


_src = inspect.getsource(EV.passaggio)
_marca = "        conf = [tr for tr in ins.tracce if tr.confermata]\n        if evento is None and len(conf) >= 2"
assert _src.count(_marca) == 1
_src = _src.replace("def passaggio(", "def passaggio_g(").replace(
    _marca, "        _ev4 = _GANCIO(D, ins, tk, evento, dichiarato)\n        if evento is None and _ev4 is not None:\n"
            "            evento = _ev4\n" + _marca)
EV._GANCIO = gancio
EV.prepara = prepara_volo
exec(compile(_src, "eventi_v3.passaggio+gancio", "exec"), EV.__dict__)


def passaggio_volo(eid, cfg, idx, sep=None, registro=False):
    _G.clear()
    _G["registro"] = registro
    EV.PAR_COLL = dict(EV.INV["collisione_multirotori"]["prudente"], k_tc=EV.FRAM["k_tc"], r_rimbalzo=EV.FRAM["r_rimbalzo_m"])
    if eid == "F4":                                             # avaria in volo: profilo dell'avaria anche sopra 10 m
        EV.PAR_COLL = EV.PAR_AVAR
    t0 = time.time()
    R = EV.passaggio_g(eid, cfg, idx, sep)
    D, A = _G["D"], _G["A"]
    R["cfg"] = cfg
    R["regola"] = REGOLA
    R["durata_calcolo_s"] = round(time.time() - t0, 2)
    R["t_primo_frammento_a_terra"] = D["t_terra"]
    R["calib"] = A["calib"]
    R["buchi_continuita"] = A["buchi"]
    R["campioni_continuita"] = A["campioni"]
    R["avviso_prossimita"] = A["prox"]
    R["libero_sul_vero"] = A["lib_vero"]
    R["innesco_v4c"] = A.get("v4c_innesco")
    R["assoc_F5"] = {str(k): v for k, v in A["assoc"].items()}
    if D["t_terra"] is not None and R["evento"] is not None:
        for chi in ("bordo", "operatore"):
            mezzo = RIT_MEZZO["drone"] if eid == "F3" else RIT_MEZZO["aereo"]
            R["margine_" + chi + "_s"] = round(D["t_terra"] - (R["evento"]["t_b"] + USCITA[chi] + RISPOSTA[chi] + mezzo), 2)
    return R, (A["registro"] if registro else None)


def _lavoro(a):
    try:
        return a, passaggio_volo(*a)[0]
    except Exception as e:
        import traceback
        return a, {"errore": repr(e), "traccia": traceback.format_exc()[-2000:]}


def main():
    from multiprocessing import Pool
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    N6 = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    NP = min(int(sys.argv[3]) if len(sys.argv) > 3 else 7, 7)   # al piu' 7 lavoratori + il principale = 8 processi
    scen = os.environ.get("VOLO_SCENARI", "F1,F2,F3,F4,F5,F6").split(",")
    lav = []
    for e in scen:
        for c in ("att", "sda"):
            n = N6 if e == "F6" else N
            if e == "F5":
                lav += [(e, c, i, (2.0, 3.0, 4.0)[i % 3]) for i in range(IDX0, IDX0 + n)]
            else:
                lav += [(e, c, i) for i in range(IDX0, IDX0 + n)]
    lav.sort(key=lambda a: -T_FINE[a[0]])
    t0 = time.time()
    out = os.environ.get("VOLO_USCITA", "passaggi_volo.jsonl")
    with Pool(NP) as p, open(os.path.join(QUI, out), "w", encoding="utf-8") as f:
        for a, r in p.imap_unordered(_lavoro, lav, chunksize=1):
            f.write(json.dumps({"lavoro": list(a), **r}, ensure_ascii=False, default=float) + "\n")
            f.flush()
    print("fatto in %.1f s" % (time.time() - t0))


def registri(cartella):
    os.makedirs(cartella, exist_ok=True)
    for e in ("F1", "F2", "F3", "F4", "F5", "F6"):
        R, reg = passaggio_volo(e, "sda", 0, 3.0 if e == "F5" else None, registro=True)
        with open(os.path.join(cartella, "registro_%s.jsonl" % e), "w", encoding="utf-8") as f:
            f.write(json.dumps({"intestazione": {"scenario": e, "nome": SCV[e]["nome"], "configurazione": "sda (stato dell'arte, latenze STIMATE)",
                                                 "seme": "SeedSequence(20261119, spawn_key=(%d, 0|2, 0))" % (200 + int(e[1])), "idx": 0,
                                                 "stato": "simulato; nessun sensore fisico; etichette a mano",
                                                 "riassunto": {k: R[k] for k in ("evento", "ritardo_evento_s", "falso_evento", "avviso_prossimita",
                                                                                 "t_primo_frammento_a_terra", "affidabilita_persa", "salute_cicli") if k in R}}},
                               ensure_ascii=False, default=float) + "\n")
            for riga in reg:
                f.write(json.dumps(riga, ensure_ascii=False, default=float) + "\n")
        print(e, len(reg), "fotogrammi", R.get("ritardo_evento_s"), R.get("avviso_prossimita"))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--registro":
        registri(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == "--uno":
        r, _ = passaggio_volo(sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5]) if len(sys.argv) > 5 else None)
        r = dict(r)
        r["calib"] = r["calib"][:5] + ["... %d" % len(r["calib"])]
        print(json.dumps(r, ensure_ascii=False, default=float)[:4000])
    else:
        main()
