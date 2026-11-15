"""Modo a LUNGA PORTATA multisensore (aerei e droni; poi auto e treni). SOLO SIMULAZIONE: nessun sensore fisico.

Il codice di f15 è copiato TALE E QUALE in riuso/lunga_portata/ (README.md, IMPRONTE.txt):
  04-moto/movi_lp.py         nucleo: celle a quattro stati per sensore, inseguitore, possibile presenza, regioni
  10-simulatore/sim_lp.py    simulatore dei sensori dalle schede
  10-simulatore/prove_lp.py  un passaggio di A1–A4, S1, S2 (configurazioni «min» e «alta», chiamante di mancato())
  10-simulatore/eventi_lp.py un passaggio di E1–E5 (eventi improvvisi e visibilità degradata)
In quel codice simulatore e nucleo girano insieme dentro `passaggio()`: qui NON li si separa (si dovrebbe cambiarlo).
Si osserva da fuori con due sostituzioni a tempo d'esecuzione, tolte alla fine:
  movi_lp.Inseguitore -> _InseguitoreOsservato  (registra, a ogni uscite(), tracce, avvisi e la pianta delle celle;
                                                 a ogni mancato() che chiude una traccia, se l'avviso era spegnibile)
  sim_lp.SensoreSim   -> _SensoreOsservato      (tiene i sensori, per la visibilità vera nel registro)
La prova che non cambiano niente: prove/prova_lunga.py confronta i cicli con gli esemplari di f15 (devono coincidere).

Condizioni (voce "condizione" della configurazione): configurazione "min" (sensore singolo) | "alta" (multisensore),
cooperante sì/no, perdita di un sensore, pioggia forte, drone piccolo (C0), etichette "a_mano" | "nessuna".
prove_lp le lega all'indice del passaggio (idx % 3 cooperazione, % 10 salute, % 7 drone C0, % 5 comportamento): qui si
sceglie il primo indice che le soddisfa e lo si dichiara, con il comportamento che ne segue.
Ambito: sola osservazione e avviso; nessuna funzione d'ingaggio, puntamento o contrasto."""
import json
import math
import os
import sys
import time

import numpy as np

from . import nucleo, riuso

LP = riuso.percorso("lunga_portata")
SIM = os.path.join(LP, "10-simulatore")
STATO_LP_A_REG = {0: 1, 1: 2, 2: 3, 3: 0}        # movi_lp (libero, occupato, ombra, non oss.) -> registro.STATI_CELLA
QUOTA_VISTA = {"A1": 30.0, "A2": 3.0, "A3": 60.0, "A4": 30.0, "S1": 1.0, "S2": 2.0,
               "E1": 80.0, "E2": 3.0, "E3": 80.0, "E4": 60.0, "E5": 80.0}   # ipotesi: solo per disegnare la pianta
_M = {}


def moduli():
    """prove_lp, eventi_lp, sim_lp, movi_lp dalla copia in riuso/ (senza scrivere __pycache__)."""
    if not _M:
        sys.dont_write_bytecode = True
        if SIM not in sys.path:
            sys.path.insert(0, SIM)
        import prove_lp
        import sim_lp
        from movi_lp_import import nucleo as m
        _M.update(prove=prove_lp, sim=sim_lp, m=m)
    if "eventi" not in _M:
        import eventi_lp
        _M["eventi"] = eventi_lp
    return _M


def scegli_indice(scen, cond):
    """Il primo passaggio di prove_lp con le condizioni chieste (vedi il docstring del modulo)."""
    coop = 0 if cond.get("cooperante", True) else 1
    for idx in range(0, 5000):
        if idx % 3 != coop:
            continue
        r10 = idx % 10
        if bool(cond.get("perdita_sensore")) != (r10 == 9) or bool(cond.get("pioggia")) != (r10 == 8):
            continue
        if scen in ("A1", "A4") and bool(cond.get("drone_piccolo")) != (idx % 7 == 3):
            continue
        if cond.get("comportamento") and moduli()["prove"].COMPORTAMENTI[idx % 5] != cond["comportamento"]:
            continue
        return idx
    raise ValueError(f"nessun passaggio con le condizioni {cond}")


class _Osservatore:
    def __init__(self, piano, quota):
        self.piano, self.quota, self.istanti, self.sensori, self.chiusure, self.ins = piano, quota, {}, [], [], None
        self.t_pianta, self.ogni_s = 0.0, 2.0

    def pianta(self, ins, t):
        """Stato fuso (movi_lp.stato_fuso, regola del nucleo) su una griglia in pianta alla quota della vista."""
        m = moduli()["m"]
        x0, x1, y0, y1, n = self.piano
        classi = [ins.reg["classi"][c] for c in ins.classi]
        gr = [g for g in ins.griglie if g.affidabile]
        out = np.full((n, n), 0, np.int8)
        if not gr:
            return out
        xs, ys = np.linspace(x0, x1, n), np.linspace(y0, y1, n)
        for j, y in enumerate(ys):
            for i, x in enumerate(xs):
                out[j, i] = STATO_LP_A_REG[m.stato_fuso(gr, np.array([x, y, self.quota]), t, classi)]
        return out


def _osservato(osv, base):
    m = moduli()["m"]

    class _InseguitoreOsservato(base):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            osv.ins = self

        def uscite(self, t, regioni=None, binario=None, eta_vista=None):
            out = super().uscite(t, regioni, binario, eta_vista)
            tracce = {tr.id: tr for tr in self.tracce}
            ist = {"t": float(t), "binario": binario is not None, "tracce": [], "eventi_nucleo": list(self.eventi),
                   "griglie": [{"sensore": g.s.nome, "affidabile": bool(g.affidabile),
                                "conteggi": np.bincount(g.stati(t, [self.reg["classi"][c] for c in self.classi]).ravel(),
                                                        minlength=4).tolist()} for g in self.griglie]}
            for o in out:
                tr = tracce.get(o["id"])
                pp = o.get("possibile_presenza")
                ist["tracce"].append({
                    "id": o["id"], "classe": o["classe"], "parola": o["parola"], "da_s": float(o["da_s"]),
                    "pos": [float(x) for x in o["pos"]], "sensori": sorted(tr.sensori) if tr else [],
                    "zona": None if "zona" not in o else {"centro": [float(x) for x in o["zona"]["centro"]],
                                                          "raggio": float(o["zona"]["raggio"])},
                    "presenza": None if pp is None else {
                        "tipo": pp["tipo"], "centro": [float(x) for x in pp["centro"]], "raggio": float(pp["raggio"]),
                        "s_min": float(pp.get("s_min", 0.0)), "s_max": float(pp.get("s_max", 0.0)),
                        "u": ([float(x) for x in (tr.v_ultima / max(np.linalg.norm(tr.v_ultima), 1e-6))] if tr else None)}})
            if osv.piano and abs(t / osv.ogni_s - round(t / osv.ogni_s)) < 1e-6:
                c0 = time.perf_counter()
                ist["pianta"] = osv.pianta(self, t)
                osv.t_pianta += time.perf_counter() - c0
            osv.istanti[round(float(t), 2)] = ist           # E1–E5 chiamano uscite() due volte per ciclo: vale l'ultima
            return out

        def mancato(self, t, sensore, traccia_id):
            tr = next((x for x in self.tracce if x.id == traccia_id), None)
            spegnibile = None
            if tr is not None and tr.confermata:
                ip = m.insieme_presenza(tr, t, self.reg, self.classi)
                classi = [self.reg["classi"][c] for c in self.classi]
                spegnibile = bool(m.avviso_spegnibile(self.griglie, ip, t, classi, n_punti=32,
                                                      rng=np.random.default_rng(tr.id))[0])
            super().mancato(t, sensore, traccia_id)
            if tr is not None and tr.confermata and all(x.id != traccia_id for x in self.tracce):
                osv.chiusure.append({"t": float(t), "traccia": traccia_id, "sensore": sensore.nome,
                                     "spegnibile": spegnibile})

    return _InseguitoreOsservato


def esegui_passaggio(cfg):
    """Esegue il passaggio della configurazione e rende (R di prove_lp/eventi_lp, osservatore, dichiarazione)."""
    M = moduli()
    P, S, m = M["prove"], M["sim"], M["m"]
    s = cfg.sorgente
    scen, cond = s["scenario"], dict(s.get("condizione", {}))
    conf = cond.get("configurazione", "alta")
    piano = tuple(s.get("piano", (-1000, 1000, -1000, 1000))) + (int(s.get("celle_lato", 24)),)
    osv = _Osservatore(piano, float(s.get("quota_vista_m", QUOTA_VISTA.get(scen, 10.0))))
    orig_ins, orig_sen, orig_mis, orig_gv = m.Inseguitore, S.SensoreSim, m.Misura, S.genera_verita
    orig_scen = P.SCEN.get(scen)

    class _SensoreOsservato(orig_sen):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            osv.sensori.append(self)

    m.Inseguitore, S.SensoreSim = _osservato(osv, orig_ins), _SensoreOsservato
    if cond.get("etichette", "a_mano") == "nessuna":
        def _senza(t, z, R, sensore, classe=None, **k):        # stessa misura, etichetta tolta
            return orig_mis(t, z, R, sensore, None, **k)
        m.Misura = _senza
    dich = {"scenario": scen, "configurazione": conf, "condizione": cond}
    try:
        if s.get("pubblica"):
            dich["registrazione_pubblica"] = _prepara_pubblica(P, S, scen, s["pubblica"], orig_gv)
        if scen.startswith("E"):
            E = M["eventi"]
            sep = s.get("separazione_m", 5.0 if scen == "E5" else None)
            idx = int(s.get("passaggio", 0))
            R = E.passaggio(scen, conf, idx, sep, esemplare=True)
            dich.update(passaggio=idx, chiamante="eventi_lp (strato eventi di f15)", separazione_m=sep)
        else:
            idx = int(s["passaggio"]) if "passaggio" in s else scegli_indice(scen, cond)
            chiamante = s.get("chiamante", "prudente")
            c0 = time.perf_counter()
            reg, _ = P.tara_regioni()
            dich["t_taratura_s"] = round(time.perf_counter() - c0, 1)
            R = P.passaggio(scen, conf, idx, esemplare=True, regioni=reg, chiamante=chiamante)
            dich.update(passaggio=idx, chiamante=chiamante, comportamento=R["comportamento"], cooperazione=R["coop"],
                        drone_C0=R["c0"], salute_simulata=R["salute"], fattore_velocita=R["fattore_v"])
    finally:
        m.Inseguitore, S.SensoreSim, m.Misura, S.genera_verita = orig_ins, orig_sen, orig_mis, orig_gv
        if orig_scen is not None:
            P.SCEN[scen] = orig_scen
    return R, osv, dich


def _prepara_pubblica(P, S, scen, pub, orig_gv):
    """Sorgente «registrazione pubblica»: il bersaglio dello scenario segue una traiettoria VERA di 01-dati (moto
    pubblico), ruotata e traslata; un ostacolo VIRTUALE a metà percorso la nasconde al sensore principale.
    Le rilevazioni restano simulate (in 01-dati non ci sono rilevazioni reali)."""
    cart = pub["cartella"] if os.path.isabs(pub["cartella"]) else os.path.join(LP, "01-dati", "traiettorie", pub["cartella"])
    meta = json.load(open(os.path.join(cart, "scena.json"), encoding="utf-8"))
    A = np.genfromtxt(os.path.join(cart, "verita.csv"), delimiter=",", skip_header=1, usecols=(0, 2, 3, 4))
    t0, t1 = float(pub.get("da_s", A[0, 0])), float(pub.get("a_s", A[-1, 0]))
    A = A[(A[:, 0] >= t0) & (A[:, 0] <= t1)]
    T = A[:, 0] - A[0, 0]
    XY = A[:, 1:3] - A[0, 1:3]
    th = math.radians(pub.get("rotazione_gradi", 0.0))
    Rm = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    XY = XY @ Rm.T + np.asarray(pub["origine"][:2], float)
    Z = np.maximum(A[:, 3] - A[0, 3], 0) + pub["origine"][2]
    sc = json.loads(json.dumps(P.SCEN[scen]))
    bers = sc["avviso"]["bersaglio"]
    ob = next(o for o in sc["oggetti"] if o["id"] == bers)
    ob["durata_s"], ob["t0"] = float(T[-1]), 0.0
    sc["oggetti"] = [ob]
    ps = np.asarray(P.CONFIG[scen]["min"][0][1], float)
    k = len(T) // 2
    pm = np.array([XY[k, 0], XY[k, 1]])
    d = pm - ps[:2]
    dist = float(np.linalg.norm(d))
    u, n_ = d / dist, np.array([-d[1], d[0]]) / dist
    c = ps[:2] + 0.6 * d
    w = max(0.25 * dist, 60.0)
    h = float(ps[2] + (Z.max() - ps[2]) * 0.6 + 20.0)
    sc["ostacoli"] = [{"id": "ostacolo_virtuale", "altezza": round(h, 1),
                       "poligono": [list(map(float, c - n_ * w / 2 - u * 5)), list(map(float, c + n_ * w / 2 - u * 5)),
                                    list(map(float, c + n_ * w / 2 + u * 5)), list(map(float, c - n_ * w / 2 + u * 5))]}]
    P.SCEN[scen] = sc

    def gv(o, comportamento, fattore_v, rng, dt=0.1, t_fine=None, **kw):
        if o["id"] != bers:
            return orig_gv(o, comportamento, fattore_v, rng, dt=dt, t_fine=t_fine, **kw)
        Tn = np.arange(int(round((t_fine or T[-1]) / dt)) + 1) * dt
        Pn = np.stack([np.interp(Tn, T, XY[:, 0]), np.interp(Tn, T, XY[:, 1]), np.interp(Tn, T, Z)], 1)
        Vn = np.gradient(Pn, dt, axis=0)
        return Tn, Pn, Vn

    S.genera_verita = gv
    return {"cartella": os.path.relpath(cart, LP), "fonte": meta.get("fonte"), "licenza": meta.get("licenza"),
            "intervallo_s": [t0, t1], "ostacolo": "VIRTUALE (non esiste nella registrazione)",
            "rilevazioni": "simulate dalle schede (la registrazione dà solo il moto)"}


class SorgenteLungaPortata:
    """Esegue il passaggio (simulatore + nucleo riusati) e rende un fotogramma per ciclo d'uscita (0,5 s)."""

    def __init__(self, cfg):
        t = time.perf_counter()
        self.R, self.osv, self.dich = esegui_passaggio(cfg)
        self.durata_s = time.perf_counter() - t
        self.es = self.R["esemplare"]
        self.ostacoli = [{"id": o["id"], "punti": o["poligono"], "genere": "ostacolo", "altezza_m": o.get("altezza")}
                         for o in (self.es["ostacoli"] if "ostacoli" in self.es else P_ostacoli(cfg))]
        self.meta = {"modo": "lungo", "simulato": True, "sensori": self.es["sensori"], "passaggio": self.dich,
                     "sorgente_obj": self}

    def __iter__(self):
        from .sorgenti import Fotogramma
        for i, c in enumerate(self.es["cicli"]):
            yield Fotogramma(i, c["t"], {"ciclo": c, "istante": self.osv.istanti.get(round(c["t"], 2))})

    def verita(self, indice):
        c = self.es["cicli"][indice]
        sens = [s for s in self.osv.sensori if s.tipo != "cooperativa" and s.nome != "p"]
        ogg = []
        for k, p in c["verita"].items():
            p = np.asarray(p, float)
            ogg.append({"id": k, "classe": None, "pos": [float(p[0]), float(p[1]), float(p[2])],
                        "visibile": bool(any(s.visibile(p, c["t"]) for s in sens))})
        return {"oggetti": ogg}


def P_ostacoli(cfg):
    return moduli()["eventi"].SE[cfg.sorgente["scenario"]].get("ostacoli", [])


class NucleoLungo(nucleo.Nucleo):
    """Adattatore: ciclo di movi_lp (registrato dall'osservatore) -> riga del registro, stesse parole del modo corto."""
    modo = "lungo"

    def __init__(self, cfg, meta):
        self.cfg, self.meta, self.src = cfg, meta, meta["sorgente_obj"]
        self._griglia = None
        self._accesi, self._chiuse_viste = {}, 0
        self._n_ev = 0

    def intestazione(self):
        from . import registro
        M = moduli()
        m, P = M["m"], M["prove"]
        s = self.cfg.sorgente
        scen = s["scenario"]
        fam = (P.FAMIGLIA.get(scen) if not scen.startswith("E") else M["eventi"].SE[scen].get("famiglia")) \
            or "aeroporto_e_droni"
        classi = P.REG["scenari"][fam]["classi_ammesse"]
        prof = self.cfg.profilo_ricevente or "operatore_di_sito"
        if prof not in P.REG["avviso"]["profili_ricevente"]:
            raise ValueError(f"profilo ricevente sconosciuto: {prof}")
        d_conto = float(m.distanza_avviso(P.REG, classi, prof))
        sc = P.SCEN.get(scen) or M["eventi"].SE.get(scen, {})
        x0, x1, y0, y1, n = self.src.osv.piano
        griglie = {"pianta_lp": {"tipo": "cartesiana", "x": [x0, x1], "y": [y0, y1], "n": [n, n],
                                 "quota_m": self.src.osv.quota, "stati": list(registro.STATI_CELLA),
                                 "nota": "stato fuso di movi_lp.stato_fuso alla quota indicata, ogni 2 s (fra due: l'ultima)"}}
        sens = [{"id": x["nome"], "tipo": x["nome"].split("#")[0], "pos": x["pos"], "fonte": x.get("fonte")}
                for x in self.src.es["sensori"]]
        cop = {}
        for g in (self.src.osv.ins.griglie if self.src.osv.ins else []):
            cop[g.s.nome] = {"r_max_m": float(g.r[-1] + g.dr / 2), "az_gradi": [math.degrees(g.az_lim[0]),
                                                                               math.degrees(g.az_lim[1])]}
        for x in sens:
            x["copertura"] = cop.get(x["id"])
        testa = registro.intestazione(self.cfg, griglie, {"tipo": "ENU locale del sito", "origine": [0, 0, 0]},
                                      sensori=sens, nota="lunga portata: simulatore e nucleo di f15 riusati tali e quali")
        testa["lunga_portata"] = {"passaggio": self.src.dich, "famiglia": fam, "classi_ammesse": classi,
                                  "profilo_ricevente": prof, "distanza_avviso_conto_m": round(d_conto, 1),
                                  "distanza_avviso_scenario_m": (sc.get("avviso") or {}).get("d_richiesta_m"),
                                  "a_chi": (sc.get("avviso") or {}).get("a_chi"),
                                  "bersaglio": (sc.get("avviso") or {}).get("bersaglio"),
                                  "punto_protetto": P.PROTETTO.get(scen, [0, 0, 0]),
                                  "metriche_del_passaggio": {k: v for k, v in self.src.R.items() if k != "esemplare"},
                                  "durata_esecuzione_s": round(self.src.durata_s, 1),
                                  "durata_vista_in_pianta_s": round(self.src.osv.t_pianta, 1)}
        return testa

    def passo(self, fot, verita=None):
        from . import registro
        c, ist = fot.dati["ciclo"], fot.dati["istante"] or {"tracce": [], "griglie": []}
        persi = set(c.get("affidabilita_persa", []))
        sensori = []
        for x in self.src.es["sensori"]:
            p = x["nome"] in persi
            sensori.append({"id": x["nome"], "tipo": x["nome"].split("#")[0],
                            "salute": "affidabilita_persa" if p else "in_salute",
                            "causa": "dichiarata dal controllo di salute di prove_lp/eventi_lp" if p else None,
                            "validi": None, "eta_dato_s": None})
        non_coop = [x for x in sensori if x["tipo"] not in ("ads_b", "identificazione_remota")]
        aff = "persa" if non_coop and all(x["salute"] == "affidabilita_persa" for x in non_coop) else "ok"
        if "pianta" in ist:
            self._griglia = ist["pianta"]
        conteggi = {}
        if self._griglia is not None:
            b = np.bincount(np.asarray(self._griglia).ravel(), minlength=4)
            conteggi = {registro.STATI_CELLA[i]: int(b[i]) for i in range(4)}
        if aff == "persa":
            conteggi = {"non_osservato": int(sum(conteggi.values()))}
        per_sens = {g["sensore"]: {"conteggi": {registro.STATI_CELLA[STATO_LP_A_REG[i]]: int(g["conteggi"][i])
                                                for i in range(4)}, "affidabile": g["affidabile"]} for g in ist["griglie"]}
        tracce, avvisi, eventi = [], [], []
        per_id = {o["id"]: o for o in ist["tracce"]}
        for o in c["uscite"]:
            d = per_id.get(o["id"], {})
            par = o["parola"]
            stato = "vista" if par.startswith("vista") else ("previsto_ampio" if par == "previsto ampio" else "non_vista")
            cl = o.get("classe") or d.get("classe") or "non_classificato"
            z = d.get("zona")
            tracce.append({"id": o["id"], "classe": cl, "origine_etichetta": "assente" if cl == "non_classificato" else "a_mano",
                           "stato": stato, "parola": par, "non_vista_da_s": None if stato == "vista" else d.get("da_s"),
                           "identita": None, "pos": None if stato == "previsto_ampio" else o["pos"][:2],
                           "quota_m": o["pos"][2], "ultima_pos": o["pos"],
                           "regione": None if not z else {"tipo": "cerchio", "centro": z["centro"][:2],
                                                          "raggio_m": z["raggio"], "livello": 0.9},
                           "sensori": d.get("sensori", []),
                           "solo_cooperativa": "solo cooperativa" in par})
            pp = d.get("presenza")
            if pp:
                if pp["tipo"] == "sfera":
                    forma = {"tipo": "cerchio", "centro": pp["centro"][:2], "raggio_m": pp["raggio"]}
                else:
                    u = np.asarray(pp["u"][:2]) / max(np.linalg.norm(pp["u"][:2]), 1e-6)
                    nn, c0 = np.array([-u[1], u[0]]) * 6.0, np.asarray(pp["centro"][:2])
                    a, b = c0 + u * pp["s_min"], c0 + u * pp["s_max"]
                    forma = {"tipo": "poligono", "punti": [list(map(float, q)) for q in (a - nn, b - nn, b + nn, a + nn)],
                             "nota": "tratto di binario"}
                avvisi.append({"tipo": "possibile_presenza", "id_traccia": o["id"], "eta_s": d.get("da_s"),
                               "forma": forma, "raggio_m": pp["raggio"]})
        ora = {a["id_traccia"] for a in avvisi}
        viste = {t_["id"] for t_ in tracce if t_["stato"] == "vista"}
        for i in sorted(set(self._accesi) - ora):
            if i in viste:
                eventi.append({"t": c["t"], "tipo": "traccia_rivista", "come_lo_so": "osservato", "traccia": i,
                               "tolto_guardando": True})
        for ch in [x for x in self.src.osv.chiusure if x["t"] <= c["t"] and not x.get("_usata")]:
            ch["_usata"] = True
            if ch["spegnibile"]:
                eventi.append({"t": ch["t"], "tipo": "avviso_tolto_guardando", "come_lo_so": "osservato",
                               "traccia": ch["traccia"], "tolto_guardando": True, "sensore": ch["sensore"]})
            else:
                eventi.append({"t": ch["t"], "tipo": "traccia_chiusa_senza_guardare_tutto_l_insieme",
                               "come_lo_so": "dedotto", "traccia": ch["traccia"], "sensore": ch["sensore"]})
        evn = ist.get("eventi_nucleo", [])
        for e in evn[self._n_ev:]:
            if e[1] in ("affidabilita' persa",):
                eventi.append({"t": float(e[0]), "tipo": "affidabilita_persa", "come_lo_so": "osservato", "sensore": e[2]})
        self._n_ev = max(self._n_ev, len(evn))
        if c.get("evento"):
            eventi.append({"t": c["t"], "tipo": "evento_" + c["evento"]["tipo"], "come_lo_so": "dedotto",
                           "da_s": c["evento"]["t_b"], "impronta_raggio_m": c["evento"]["impronta_raggio_m"]})
        self._accesi = {a["id_traccia"]: True for a in avvisi}
        settori = []
        for x in self.src.es["sensori"]:
            p = x["nome"] in persi
            settori.append({"id": x["nome"], "azimut_gradi": None, "d_m": None,
                            "livello": "affidabilita_persa" if p else ("attenzione" if (tracce or avvisi) else "zona_non_verificata"),
                            "motivo": "sensore senza affidabilità" if p else "livello prudente (il modo lungo non scrive «visto libero fino a d»)"})
        return {"tipo": "fotogramma", "modo": "lungo", "indice": fot.indice, "t": c["t"],
                "dichiarazioni": self.cfg.dichiarazioni(), "verita": verita, "sensori": sensori, "affidabilita": aff,
                "celle": {"griglia": "pianta_lp", "conteggi": conteggi, "per_sensore": per_sens},
                "settori": settori, "tracce": tracce, "avvisi": avvisi, "eventi": eventi, "tempo_ciclo_ms": None}

    def griglia_stati(self):
        # collaudo (sciame-tester, 15-11-2026): prima della prima pianta (t < 2 s) la griglia intera è «non osservato»
        # della misura dichiarata nell'intestazione, non una griglia 1×1 (il registro la dava di 1 cella su n×n)
        if self._griglia is None:
            piano = getattr(getattr(self.src, "osv", None), "piano", None)
            n = piano[4] if piano else 1
            return np.zeros((n, n), np.int8)
        return np.asarray(self._griglia)
