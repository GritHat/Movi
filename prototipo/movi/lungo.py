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


# ---- nucleo v2 (fase 2b, sciame-sviluppatore, 15-11-2026). AGGIUNTO: il v1 resta e si sceglie con --nucleo v1 o
# con la voce "nucleo": "v1" della sorgente. v2 = riuso/lunga_portata_v2/ (movi_lp_v2.py, regole v2, eventi_v2.py;
# PROVENIENZA.md). Con v2: regole v2; A1 e A2 nella famiglia sito_droni_rullaggio (caso centrale, inviluppo dei droni
# e dei mezzi di terra), A3 in aeroporto_e_droni (aerei in volo a 210 m/s: limite dichiarato); mappa DICHIARATA
# completa (il simulatore conosce gli ostacoli: ipotesi, scritta nell'intestazione); E1, E2, E4, E5 con lo strato
# eventi_v2 (E3 non c'è: eventi_lp col nucleo v2).
LP2 = riuso.percorso("lunga_portata_v2")
# ---- nucleo v3 (fase 2c, sciame-tracciamento, 15-11-2026). AGGIUNTO, PREDEFINITO: v1 e v2 restano (--nucleo v1|v2).
# v3 = riuso/lunga_portata_v3/ (movi_lp_v3.py: finestra W_c dalla v_max vera dell'inviluppo e ritenuta del ritorno;
# eventi_v3.py: eta' della traccia d'origine, duplicati fusi, ispezione dell'impronta). MAPPA: col v3 la mappa NON e'
# dichiarata completa per predefinito (MAPPA_CERTIFICATA_PREDEFINITA del nucleo resta False): nessuna cella 'libera'.
# La si dichiara solo con la voce "mappa_certificata": true della sorgente o con MOVI_MAPPA_CERTIFICATA=1, ed e'
# scritta nell'intestazione. Il v2 conserva il suo comportamento (mappa dichiarata completa), come prima.
LP3 = riuso.percorso("lunga_portata_v3")
NUCLEI = ("v1", "v2", "v3")
NUCLEO_LP = os.environ.get("MOVI_NUCLEO_LP", "v3")
MAPPA_V3 = {"certificata": os.environ.get("MOVI_MAPPA_CERTIFICATA", "0") == "1", "da": "MOVI_MAPPA_CERTIFICATA"}


def _v2piu(n):
    """v2 e v3 hanno gli stessi campi del registro e lo stesso strato eventi (in versioni diverse)."""
    return n in ("v2", "v3")
FAMIGLIA_V2 = {"A1": "sito_droni_rullaggio", "A2": "sito_droni_rullaggio"}
EVENTI_V2 = ("E1", "E2", "E4", "E5")
NUCLEO_DA_RIGA_DI_COMANDO = False
PASSO_REG_EV_S = 0.5              # eventi_v2 gira a 0,1 s: il registro ne tiene uno ogni 0,5 s (come gli altri modi lunghi)


def scegli_nucleo(nome):
    """Sceglie il nucleo del modo lungo prima di caricare i moduli (in un processo vale uno solo)."""
    global NUCLEO_LP
    if nome not in NUCLEI:
        raise ValueError(f"nucleo sconosciuto: {nome} (ammessi: {NUCLEI})")
    if _M and _M.get("nucleo") != nome:
        raise RuntimeError(f"moduli già caricati col nucleo {_M.get('nucleo')}: un processo, un nucleo")
    NUCLEO_LP = nome


def moduli():
    """prove_lp, eventi_lp, sim_lp, movi_lp dalla copia in riuso/ (senza scrivere __pycache__)."""
    if not _M:
        sys.dont_write_bytecode = True
        if SIM not in sys.path:
            sys.path.insert(0, SIM)
        if NUCLEO_LP == "v2":
            import types
            if LP2 not in sys.path:
                sys.path.insert(0, LP2)
            import movi_lp_v2
            movi_lp_v2.MAPPA_CERTIFICATA_PREDEFINITA = True
            sys.modules["movi_lp_import"] = types.SimpleNamespace(nucleo=movi_lp_v2)
        elif NUCLEO_LP == "v3":
            import types
            if LP3 not in sys.path:
                sys.path.insert(0, LP3)
            import movi_lp_v3
            movi_lp_v3.MAPPA_CERTIFICATA_PREDEFINITA = bool(MAPPA_V3["certificata"])
            sys.modules["movi_lp_import"] = types.SimpleNamespace(nucleo=movi_lp_v3)
        import prove_lp
        import sim_lp
        from movi_lp_import import nucleo as m
        if NUCLEO_LP == "v3":
            prove_lp.REG = m.carica_regole(os.path.join(LP3, "regole_lunga_portata_v3.json"))
            prove_lp.FAMIGLIA.update(FAMIGLIA_V2)
        if NUCLEO_LP == "v2":
            prove_lp.REG = m.carica_regole(os.path.join(LP2, "regole_lunga_portata_v2.json"))
            prove_lp.FAMIGLIA.update(FAMIGLIA_V2)
        _M.update(prove=prove_lp, sim=sim_lp, m=m, nucleo=NUCLEO_LP)
    if "eventi" not in _M:
        import eventi_lp
        if NUCLEO_LP == "v3":
            eventi_lp.REG = _M["prove"].REG
            os.environ.setdefault("EVENTI_NUCLEO", "prototipo")      # eventi_v3 prende il nucleo da eventi_lp (= v3)
            import eventi_v3
            eventi_v3.NUCLEO = "riuso/lunga_portata_v3/movi_lp_v3.py"
            _M["eventi_v2"] = eventi_v3                             # stesso aggancio del registratore
        if NUCLEO_LP == "v2":
            eventi_lp.REG = _M["prove"].REG
            import eventi_v2
            eventi_v2.NUCLEO = "riuso/lunga_portata_v2/movi_lp_v2.py"
            _M["eventi_v2"] = eventi_v2
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

    def libere_per_classe(self, ins, t, stato=None, n_lato=12):
        """v2: per ogni classe ammessa, quante celle della pianta (n_lato × n_lato, più rada della vista) sono «libere»
        PER QUELLA CLASSE (stato_fuso con la sola classe; per gli eventi: stato_v2, che toglie i sensori accecati).
        0 celle libere -> «zona non verificata per <classe>» nel registro."""
        m = moduli()["m"]
        x0, x1, y0, y1, _ = self.piano
        gr = [g for g in ins.griglie if g.affidabile]
        out = {}
        for c in ins.classi:
            cl = [ins.reg["classi"][c]]
            k = 0
            if gr:
                for y in np.linspace(y0, y1, n_lato):
                    for x in np.linspace(x0, x1, n_lato):
                        p = np.array([x, y, self.quota])
                        s = stato(p, t, cl) if stato else m.stato_fuso(gr, p, t, cl)
                        k += int(s == m.LIBERO)
            out[c] = [k, n_lato * n_lato]
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
                if _v2piu(moduli()["nucleo"]):
                    ist["libere_per_classe"] = osv.libere_per_classe(self, t)
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
    if cfg.sorgente.get("nucleo") and not _M and not NUCLEO_DA_RIGA_DI_COMANDO:
        scegli_nucleo(cfg.sorgente["nucleo"])              # la scena chiede un nucleo; --nucleo la scavalca
    if "mappa_certificata" in cfg.sorgente and not _M:     # v3: dichiarazione esplicita della scena
        MAPPA_V3.update(certificata=bool(cfg.sorgente["mappa_certificata"]), da="voce mappa_certificata della scena")
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
    dich["nucleo"] = M["nucleo"]
    try:
        if s.get("pubblica"):
            dich["registrazione_pubblica"] = _prepara_pubblica(P, S, scen, s["pubblica"], orig_gv)
        if scen.startswith("E") and _v2piu(M["nucleo"]) and scen in EVENTI_V2:
            sep = s.get("separazione_m", 5.0 if scen == "E5" else None)
            idx = int(s.get("passaggio", 0))
            R = passaggio_eventi_v2(M, scen, conf, idx, sep, osv)
            dich.update(passaggio=idx, chiamante=("eventi_v3 (strato eventi della fase 2c" if M["nucleo"] == "v3" else
                                                  "eventi_v2 (strato eventi della fase 2b") + ", semi 20261116)",
                        separazione_m=sep)
        elif scen.startswith("E"):
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
        if M["nucleo"] == "v3":
            esc = P.REG["scenari"][fam].get("classi_escluse", [])
            testa["lunga_portata"].update(
                nucleo="v3", nucleo_file="riuso/lunga_portata_v3/movi_lp_v3.py",
                regole_file="riuso/lunga_portata_v3/regole_lunga_portata_v3.json",
                provenienza="riuso/lunga_portata_v3/PROVENIENZA.md", classi_escluse=esc,
                mappa_certificata=("dichiarata completa (" + MAPPA_V3["da"] + "; il simulatore conosce gli ostacoli: ipotesi)")
                if MAPPA_V3["certificata"] else "NON dichiarata: nessuna cella può essere 'libera'",
                tempestivita_conto=m.tempestivita(P.REG, fam), nota_famiglia=P.REG["scenari"][fam].get("nota"))
        elif M["nucleo"] == "v2":
            esc = P.REG["scenari"][fam].get("classi_escluse", [])
            testa["lunga_portata"].update(
                nucleo="v2", nucleo_file="riuso/lunga_portata_v2/movi_lp_v2.py",
                regole_file="riuso/lunga_portata_v2/regole_lunga_portata_v2.json",
                provenienza="riuso/lunga_portata_v2/PROVENIENZA.md", classi_escluse=esc,
                mappa_certificata="dichiarata completa (il simulatore conosce gli ostacoli: ipotesi)",
                tempestivita_conto=m.tempestivita(P.REG, fam), nota_famiglia=P.REG["scenari"][fam].get("nota"))
        else:
            testa["lunga_portata"]["nucleo"] = "v1"
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
        elif _v2piu(self.src.dich.get("nucleo")) and self.src.dich.get("nucleo") == "v3":
            # fase 2c (VERDETTO_2B par. 5): prima della prima pianta il visore mostra n×n celle «non osservato»
            # (griglia_stati); i conteggi ora dicono la stessa cosa invece di essere vuoti
            conteggi = {"non_osservato": int(np.asarray(self.griglia_stati()).size)}
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
        riga = {"tipo": "fotogramma", "modo": "lungo", "indice": fot.indice, "t": c["t"],
                "dichiarazioni": self.cfg.dichiarazioni(), "verita": verita, "sensori": sensori, "affidabilita": aff,
                "celle": {"griglia": "pianta_lp", "conteggi": conteggi, "per_sensore": per_sens},
                "settori": settori, "tracce": tracce, "avvisi": avvisi, "eventi": eventi, "tempo_ciclo_ms": None}
        if _v2piu(self.src.dich.get("nucleo")):
            campi_v2(self, riga, c, ist)
        if self.src.dich.get("nucleo") == "v3":
            _maschera_v3(self, riga)
        return riga

    def griglia_stati(self):
        if getattr(self, "_mostrata", None) is not None:          # v3: la griglia mostrata è quella mascherata
            return self._mostrata
        # collaudo (sciame-tester, 15-11-2026): prima della prima pianta (t < 2 s) la griglia intera è «non osservato»
        # della misura dichiarata nell'intestazione, non una griglia 1×1 (il registro la dava di 1 cella su n×n)
        if self._griglia is None:
            piano = getattr(getattr(self.src, "osv", None), "piano", None)
            n = piano[4] if piano else 1
            return np.zeros((n, n), np.int8)
        return np.asarray(self._griglia)


# ============================================================================ v3: «libero» mai dentro un avviso
def _dentro_forma(X, Y, f):
    """Maschera dei punti (X, Y) dentro la forma del registro (cerchio o poligono)."""
    if f["tipo"] == "cerchio":
        return (X - f["centro"][0]) ** 2 + (Y - f["centro"][1]) ** 2 <= f["raggio_m"] ** 2
    P = f["punti"]
    c = np.zeros(X.shape, bool)
    for i in range(len(P)):
        x1, y1 = P[i][:2]
        x2, y2 = P[i - 1][:2]
        if y1 == y2:
            continue
        c ^= ((y1 > Y) != (y2 > Y)) & (X < (x2 - x1) * (Y - y1) / (y2 - y1) + x1)
    return c


def _maschera_v3(nuc, riga):
    """v3 (fase 2c, VERDETTO_2B par. 5 e K-611): nella griglia MOSTRATA una cella «libero» il cui centro cade dentro un
    avviso di possibile presenza o dentro volume e impronta dei detriti del fotogramma diventa «non_osservato». Motivo:
    con passate correlate (n_eff = 1) una passata senza ritorno non esclude l'oggetto che l'avviso dice possibile lì.
    Il nucleo non cambia: cambia ciò che il registro dichiara. Conteggi ricalcolati sulla griglia mostrata; quante
    celle sono state tolte è scritto in celle.libere_tolte_dentro_avviso."""
    from . import registro
    g = np.asarray(nuc.griglia_stati() if getattr(nuc, "_griglia", None) is None else nuc._griglia).copy()
    x0, x1, y0, y1, n = nuc.src.osv.piano
    X, Y = np.meshgrid(np.linspace(x0, x1, n), np.linspace(y0, y1, n))
    forme = [a["forma"] for a in riga.get("avvisi", [])]
    d = riga.get("detriti") or {}
    for k in ("volume", "impronta"):
        v = d.get(k) or []
        forme += v if isinstance(v, list) else [v]
    lib = registro.STATI_CELLA.index("libero")
    via = np.zeros(g.shape, bool)
    for f in forme:
        via |= _dentro_forma(X, Y, f) & (g == lib)
    g[via] = registro.STATI_CELLA.index("non_osservato")
    nuc._mostrata = g
    if riga["celle"]["conteggi"] and riga.get("affidabilita") != "persa":
        b = np.bincount(g.ravel(), minlength=4)
        riga["celle"]["conteggi"] = {registro.STATI_CELLA[i]: int(b[i]) for i in range(4)}
    riga["celle"]["libere_tolte_dentro_avviso"] = int(via.sum())


# ============================================================================ nucleo v2: campi del registro e eventi
def _cerchio(c, r, n=32):
    return {"tipo": "poligono", "punti": [[float(c[0] + r * math.cos(a)), float(c[1] + r * math.sin(a))]
                                          for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]}


def _capsula(a, b, r, n=16):
    """Poligono del segmento [a, b] ingrossato di r (pianta)."""
    a, b = np.asarray(a, float)[:2], np.asarray(b, float)[:2]
    d = b - a
    th = math.atan2(d[1], d[0]) if np.linalg.norm(d) > 1e-9 else 0.0
    pts = [[float(b[0] + r * math.cos(th + f)), float(b[1] + r * math.sin(th + f))]
           for f in np.linspace(-math.pi / 2, math.pi / 2, n)]
    pts += [[float(a[0] + r * math.cos(th + f)), float(a[1] + r * math.sin(th + f))]
            for f in np.linspace(math.pi / 2, 3 * math.pi / 2, n)]
    return {"tipo": "poligono", "punti": pts}


def campi_v2(nuc, riga, c, ist):
    """I campi che il nucleo v2 aggiunge a ogni fotogramma (il validatore li controlla, registro.valida_riga):
      affidabilita_per_sensore  [{sensore, stato: affidabile | persa | accecato, griglia, motivo}]
      zona_non_verificata_per_classe [{classe, motivo, forma, celle_libere}]  (escluse dallo scenario, o 0 celle
                                libere per quella classe nell'ultima pianta: il sensore non la può dichiarare)
      libero_per_classi         le classi con almeno una cella libera nell'ultima pianta
      detriti                   null | {stato, volume: [poligoni], impronta: [poligoni], come_lo_so: dedotto, …}"""
    lp = nuc.src.dich
    fam = nuc._fam_v2()
    reg = moduli()["prove"].REG
    esc = reg["scenari"][fam].get("classi_escluse", [])
    persi = set(c.get("affidabilita_persa", []))
    acc = set(c.get("accecati", []))
    per_s = riga["celle"].get("per_sensore", {})
    aff = []
    for s in riga["sensori"]:
        g = per_s.get(s["id"])
        st = "accecato" if s["id"] in acc else ("persa" if (s["id"] in persi or (g is not None and not g["affidabile"]))
                                                else "affidabile")
        if st != "affidabile" and g is not None:      # una griglia senza affidabilità non dichiara niente
            g["conteggi"] = {"non_osservato": int(sum(g["conteggi"].values()))}
        aff.append({"sensore": s["id"], "stato": st, "griglia": g is not None,
                    "motivo": {"accecato": "quadri saturi o nube opaca (EV-B, EV-C)",
                               "persa": "controllo di salute (silenzio, saturazione, fondo)"}.get(st)})
    riga["affidabilita_per_sensore"] = aff
    if "libere_per_classe" in ist:
        nuc._libere_v2 = ist["libere_per_classe"]
    lib = getattr(nuc, "_libere_v2", None) or {}
    x0, x1, y0, y1, _ = nuc.src.osv.piano
    tutto = {"tipo": "poligono", "punti": [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]}
    znv = [{"classe": e, "motivo": "classe esclusa dallo scenario: «libero» non vale mai per lei", "forma": tutto,
            "celle_libere": None} for e in esc]
    for cl, (k, n) in sorted(lib.items()):
        if k == 0:
            znv.append({"classe": cl, "motivo": "nessuna cella «libera» per questa classe nella vista (Pd insufficiente "
                        "o nessun sensore affidabile): zona non verificata", "forma": tutto, "celle_libere": [k, n]})
    if riga["affidabilita"] == "persa":
        znv = [{"classe": cl, "motivo": "affidabilità persa", "forma": tutto, "celle_libere": None}
               for cl in list(lib) + list(esc)]
    riga["zona_non_verificata_per_classe"] = znv
    riga["libero_per_classi"] = sorted(cl for cl, (k, n) in lib.items() if k > 0) if riga["affidabilita"] == "ok" else []
    R = nuc.src.R
    if R.get("meteo") is not None and nuc.src.osv.ins is not None:   # E3: portata dichiarata con il meteo
        if not hasattr(nuc, "_portata_v2"):
            E, m, cat = moduli()["eventi"], moduli()["m"], moduli()["eventi"].CAT
            pd_ = []
            for g in nuc.src.osv.ins.griglie:
                tipo = g.s.nome.split("#")[0]
                for cl in ("multirotore_piccolo", "aereo_leggero"):
                    rc_ = reg["classi"][cl]["rcs_m2"]
                    nom = float(m.Sensore("x", [0, 0, 0], cat[tipo]).portata(rc_, 0.99, 5))
                    pd_.append({"sensore": g.s.nome, "classe": cl, "nominale_m": round(nom, 1),
                                "con_meteo_conto_m": round(float(E.fattore(R["meteo"], tipo, 1)) * nom, 1),
                                "dichiarata_nucleo_m": round(float(g.s.portata(rc_, 0.99, 5)), 1)})
            nuc._portata_v2 = pd_
        riga["portata_dichiarata"] = nuc._portata_v2
    det = c.get("detriti_v2")
    riga["detriti"] = det
    if det:
        nuovi = [i for i in det["tracce_avvisate"] if i not in nuc.__dict__.setdefault("_avvisati_v2", set())]
        for i in nuovi:
            nuc._avvisati_v2.add(i)
            riga["eventi"].append({"t": c["t"], "tipo": "avviso_detriti", "come_lo_so": "dedotto", "traccia": i,
                                   "motivo": "il percorso previsto entra nell'impronta dei detriti (EV-E)"})
        if not nuc.__dict__.get("_evento_v2_scritto"):
            nuc._evento_v2_scritto = True
            riga["eventi"].append({"t": c["t"], "tipo": "evento_" + det["tipo"].replace(" ", "_"), "come_lo_so": "dedotto",
                                   "da_s": det["t_b"], "t_a": det["t_a"], "origine": det["origine"],
                                   "volume": det["volume"], "impronta": det["impronta"]})
    return riga


def _fam_v2(self):
    M = moduli()
    scen = self.cfg.sorgente["scenario"]
    return (M["prove"].FAMIGLIA.get(scen) if not scen.startswith("E") else M["eventi"].SE[scen].get("famiglia")) \
        or "aeroporto_e_droni"


NucleoLungo._fam_v2 = _fam_v2


def passaggio_eventi_v2(M, eid, cfg, idx, sep, osv):
    """Un passaggio di eventi_v2.passaggio (copia in riuso/lunga_portata_v2, NON modificata) con un registratore
    per ciclo. La funzione è ricompilata dal suo sorgente con UNA riga in più alla fine del corpo del ciclo
    («_REG_CICLO(locals())»), che legge senza scrivere: tracce, insieme di presenza, sensori persi o accecati, evento,
    volume e impronta. Rende R di eventi_v2 con R["esemplare"] nella forma che usa SorgenteLungaPortata."""
    import inspect
    E2, m, FR = M["eventi_v2"], M["m"], M["eventi_v2"].FR
    src = inspect.getsource(E2.passaggio)
    marca = "    # ---- esiti per passaggio"
    if src.count(marca) != 1:
        raise RuntimeError("eventi_v2.passaggio è cambiato: il registratore non sa dove agganciarsi")
    src = src.replace(marca, "        _REG_CICLO(locals())\n" + marca, 1).replace("def passaggio(", "def _passaggio_reg(", 1)
    cicli, stato = [], {"griglie_viste": False}
    amm = E2.REG["scenari"][E2.FAM]["classi_ammesse"]

    def reg_ciclo(L):
        tk, D, ins, ev = L["tk"], L["D"], L["ins"], L["evento"]
        if abs(tk / PASSO_REG_EV_S - round(tk / PASSO_REG_EV_S)) > 1e-6:
            return
        if not stato["griglie_viste"]:
            osv.ins, osv.sensori, stato["griglie_viste"] = ins, list(D["sensori"]), True
        uscite, ist = [], {"t": tk, "binario": False, "tracce": [], "eventi_nucleo": list(ins.eventi), "griglie": []}
        for tr in ins.tracce:
            if not tr.confermata:
                continue
            tau = tk - tr.t_vista
            o = {"id": tr.id, "classe": tr.classe or "non_classificato", "pos": [float(x) for x in tr.x[:3]],
                 "parola": "vista" if tau <= 2.0 else "non vista da %.0f s" % tau}
            uscite.append(o)
            d = {"id": tr.id, "classe": o["classe"], "parola": o["parola"], "da_s": float(tau), "pos": o["pos"],
                 "sensori": sorted(tr.sensori), "zona": None, "presenza": None}
            if tau > 2.0:
                pp = m.insieme_presenza(tr, tk, E2.REG, amm)
                d["presenza"] = {"tipo": pp["tipo"], "centro": [float(x) for x in pp["centro"]],
                                 "raggio": float(pp["raggio"]), "s_min": 0.0, "s_max": 0.0, "u": None}
            ist["tracce"].append(d)
        cl_all = [E2.REG["classi"][c] for c in amm]
        for g in ins.griglie:
            ist["griglie"].append({"sensore": g.s.nome, "affidabile": bool(g.affidabile),
                                   "conteggi": np.bincount(g.stati(tk, cl_all).ravel(), minlength=4).tolist()})
        if abs(tk / osv.ogni_s - round(tk / osv.ogni_s)) < 1e-6 and osv.piano:
            c0 = time.perf_counter()
            x0, x1, y0, y1, n = osv.piano
            pl = np.zeros((n, n), np.int8)
            for j, y in enumerate(np.linspace(y0, y1, n)):
                for i, x in enumerate(np.linspace(x0, x1, n)):
                    pl[j, i] = STATO_LP_A_REG[E2.stato_v2(D, [x, y, osv.quota], tk, cl_all)]
            ist["pianta"] = pl
            ist["libere_per_classe"] = osv.libere_per_classe(ins, tk, stato=lambda p, t, cl: E2.stato_v2(D, p, t, cl))
            osv.t_pianta += time.perf_counter() - c0
        osv.istanti[round(float(tk), 2)] = ist
        i_t = int(round(tk / 0.1))
        ver = {}
        for k, (T, P, _) in D["ver"].items():
            p = P[min(i_t, len(T) - 1)]
            if k.startswith("fr") and (p[2] < -1 or abs(p[0]) > 1e6 or len([x for x in ver if x.startswith("fr")]) >= 40):
                continue
            ver[k] = [float(x) for x in p]
        acc = sorted(nm for nm, k in L["cattivi"].items() if k > 0)
        cy = {"t": tk, "uscite": uscite, "verita": ver, "affidabilita_persa": sorted(L["dichiarato"]), "accecati": acc}
        if ev is not None:
            tau = tk - ev["t_a"]
            r, tq, zmin, zmax, _ = FR.inviluppo(tau, ev["ev"], ev["par"])
            vol = [_capsula(ev["ev"]["p0"], np.asarray(ev["ev"]["p0"][:2]) + np.asarray(v[:2]) * tq, r)
                   for v in ev["ev"]["vc"]]
            Z = ev["Z"]
            imp = [_cerchio(Z["c"], Z["R"], 48)]
            if Z["striscia"] is not None:
                imp.append(_capsula(Z["striscia"][0], Z["striscia"][1], Z["striscia"][2]))
            cy["detriti_v2"] = {"stato": "zona_non_verificata_possibili_detriti", "come_lo_so": "dedotto",
                                "tipo": ev["tipo"], "t_b": ev["t_b"], "t_a": round(ev["t_a"], 2),
                                "origine": list(ev["origine"]), "volume": vol, "quota_volume_m": [float(zmin), float(zmax)],
                                "raggio_volume_m": float(r), "impronta": imp, "impronta_raggio_m": float(Z["R"]),
                                "tracce_avvisate": sorted(L["avvisati"]),
                                "nota": "volume V(tau) in pianta (capsule) e impronta (disco R_imp + striscia): "
                                        "frammenti.py, inviluppo prudente; nessuna etichetta"}
            # l'evento entra nel registro da campi_v2 (una volta, con volume e impronta): qui niente cy["evento"]
        cicli.append(cy)

    ns = dict(vars(E2))
    ns["_REG_CICLO"] = reg_ciclo
    exec(compile(src, E2.__file__ + " [con registratore]", "exec"), ns)
    R = ns["_passaggio_reg"](eid, cfg, idx, sep)
    sens = [{"nome": s.nome, "pos": s.pos.tolist(), "fonte": s.base.get("fonte")} for s in osv.sensori]
    R["esemplare"] = {"scenario": eid, "configurazione": cfg, "sensori": sens, "cicli": cicli,
                      "ostacoli": E2.SE[eid].get("ostacoli", []), "strato": "eventi_v2"}
    return R
