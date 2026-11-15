"""Modo a CORTO RAGGIO: camera di profondità ferma, fino a 3 m, persone a piedi. Tutto il codice esiste: qui si compone.

  riuso/catena (Catena.ciclo, con il predittore scelto)  ->  registro.da_catena  ->  salute del sensore
  ->  griglia DICHIARATA (regola del libero di riuso/libero, affidabilità)  ->  livelli per settore
  ->  regione di previsione (celle al 90 % o «previsto ampio»)  ->  eventi del registro  ->  etichette a mano
Le correzioni di f12 sono campi di parametri.Parametri («correzioni f12»): si accendono da cfg.regole().
Il nucleo non legge MAI la verità per decidere: la ricopia nel registro (e la usano solo le etichette a `id_vero`,
che simulano il classificatore assente)."""
import hashlib
import math
import time

import numpy as np

from . import etichette as E
from . import eventi_registro, livelli, nucleo, registro, riuso

# Campi di riuso/catena/parametri.Parametri accesi dall'interruttore «correzioni_f12» (letti il 15-11-2026, righe 55-64).
CORREZIONI_F12 = ("soglia_proporzionale", "gruppi_per_picco", "tagliato_su_componente", "riaggancio_rifiuta_tagliati",
                  "riaggancio_rifiuta_occlusore", "riparti_al_riaggancio", "strato_resta")
NON_REALIZZATI = ("c7_identita_al_ritorno", "fascia_di_scenario", "regione_per_classe")
K_LIBERO = {"nominale": 0.004, "limite": 0.0100}     # SOLUZIONE_V3 §1.2 (k del margine del suolo)
FOTOGRAMMI_AVVIO = 5


def parametri_da_config(cfg):
    """parametri.Parametri della catena dalla configurazione: interruttori -> campi booleani; cfg.parametri li scavalca."""
    par = riuso.modulo("catena", "parametri").Parametri()
    if cfg.regole()["correzioni_f12"]:
        for nome in CORREZIONI_F12:
            setattr(par, nome, True)
    for nome, valore in cfg.parametri.items():
        if not hasattr(par, nome):
            raise ValueError(f"parametro sconosciuto della catena: {nome}")
        setattr(par, nome, valore)
    return par


class SaluteSensore:
    """SOLUZIONE_V3 §1.9: NON IN SALUTE se nessun fotogramma nuovo per 0,13 s o tre identici di fila, o pixel validi
    sotto metà della taratura per 0,2 s. Controllo all'avvio: la taratura è la mediana dei pixel validi dei primi
    5 fotogrammi; se è sotto il 30 % dell'immagine il controllo non è superato e l'affidabilità resta persa.
    IMU e piano del suolo: fuori dal prototipo (camera ferma simulata, posa da meta.json): lo dice l'intestazione."""

    def __init__(self, n_pixel):
        self.n_pixel, self.avvio, self.taratura = n_pixel, [], None
        self.t_prec, self.impronta_prec, self.identici, self.t_basso = None, None, 0, None

    def passo(self, t, prof, validi):
        causa, salute = "", "in_salute"
        imp = hashlib.blake2b(np.ascontiguousarray(prof).tobytes(), digest_size=8).digest()
        self.identici = self.identici + 1 if imp == self.impronta_prec else 0
        self.impronta_prec = imp
        buco = self.t_prec is not None and t - self.t_prec > 0.13 + 1e-6
        self.t_prec = t
        if self.taratura is None:
            self.avvio.append(validi)
            if len(self.avvio) < FOTOGRAMMI_AVVIO:
                salute, causa = "degradato", f"controllo all'avvio in corso ({len(self.avvio)}/{FOTOGRAMMI_AVVIO})"
            elif float(np.median(self.avvio)) >= 0.30 * self.n_pixel:
                self.taratura = float(np.median(self.avvio))
            else:
                self.avvio.pop(0)
                salute, causa = "affidabilita_persa", "controllo all'avvio non superato (pochi pixel validi)"
        if self.taratura is not None:
            if validi < 0.5 * self.taratura:
                self.t_basso = t if self.t_basso is None else self.t_basso
                if t - self.t_basso >= 0.2 - 1e-6:
                    salute, causa = "affidabilita_persa", "pixel validi sotto metà della taratura da 0,2 s"
                else:
                    salute, causa = "degradato", "pixel validi sotto metà della taratura"
            else:
                self.t_basso = None
        if self.identici >= 2:
            salute, causa = "affidabilita_persa", "tre fotogrammi identici di fila"
        if buco:
            salute, causa = "affidabilita_persa", "nessun fotogramma nuovo per 0,13 s"
        return {"id": "profondita", "tipo": "camera di profondità (simulata)", "salute": salute, "causa": causa,
                "validi": int(validi), "taratura": self.taratura, "eta_dato_s": 0.0}


class _Libero:
    """La regola del «libero» di riuso/libero/libero.py (PR4 = `nuvole-1`: metà dell'impronta della cella e delle 8
    vicine legge il suolo, dal solo fotogramma) portata sulla griglia della catena. La griglia di libero.py ha
    l'azimut centrato sul campo della camera: ogni sua cella va nella cella della catena che ne contiene il centro;
    una cella della catena è «libero» solo se TUTTE le celle di libero.py che vi cadono lo sono (lettura prudente)."""

    def __init__(self, meta, par, livello):
        Lb = riuso.modulo("libero", "libero")
        posa = meta["posa"]
        cam = Lb.Camera(meta["larghezza"], meta["altezza"], meta["fx"], meta["fy"], meta["cx"], meta["cy"],
                        posa["altezza_m"], posa["inclinazione_gradi"])
        self.R = Lb.Regole(cam, K_LIBERO.get(livello, K_LIBERO["limite"]))
        a, r = np.meshgrid(np.arange(self.R.NA), np.arange(Lb.NR), indexing="ij")
        az = a + 0.5 - cam.AZ0
        self.ia = np.floor((az + par.azimut_max_gradi) / par.passo_azimut_gradi).astype(int)
        self.ir = r
        self.forma = (par.n_azimut, par.n_distanza)

    def maschera(self, prof_mm):
        out, _, _, _ = self.R.tutte(prof_mm.astype(np.float64) / 1000.0)
        si = np.zeros(self.forma, int)
        tutte = np.zeros(self.forma, int)
        np.add.at(tutte, (self.ia, self.ir), 1)
        np.add.at(si, (self.ia, self.ir), out["PR4"].astype(int))
        return (tutte > 0) & (si == tutte)


class NucleoCorto(nucleo.Nucleo):
    modo = "corto"

    def __init__(self, cfg, meta):
        regole = cfg.regole()
        accesi = [n for n in NON_REALIZZATI if regole[n]]
        if accesi:
            raise NotImplementedError(f"interruttori non realizzati nel modo corto: {accesi}")
        C = riuso.modulo("catena", "catena")
        P = riuso.modulo("catena", "presenza")
        self.cfg, self.meta, self.regole = cfg, meta, regole
        self.par = parametri_da_config(cfg)
        if regole["predittore_zona"]:
            from .predittore_zona import PredittoreZona
            fabbrica = lambda ingresso, par: PredittoreZona(ingresso, par, seme=cfg.seme)   # noqa: E731
        else:
            fabbrica = P.PredittoreVelocitaCostante
        self.catena = C.Catena(meta, self.par, fabbrica_predittore=fabbrica)
        livello = (meta.get("simulazione") or {}).get("livello", "nominale")
        self.libero = _Libero(meta, self.par, livello) if regole["libero_dal_fotogramma"] else None
        self.salute = SaluteSensore(meta["larghezza"] * meta["altezza"])
        self.eventi = eventi_registro.EventiDelRegistro()
        self.etichette = E.carica(cfg.etichette, cfg.classi_ammesse)
        g, p = self.catena.griglia, self.par
        self.settori = [(a0, a1, [round(float(g.azimut[a0] - p.passo_azimut_gradi / 2), 1),
                                  round(float(g.azimut[a1 - 1] + p.passo_azimut_gradi / 2), 1)])
                        for a0, a1 in self.catena._settori]
        self._stati = None
        self._classi = {}          # etichetta a mano già data a una traccia: resta con la sua identità

    def intestazione(self):
        p = self.par
        griglie = {"polare_corto": {"tipo": "polare", "passo_azimut_gradi": p.passo_azimut_gradi,
                                    "passo_distanza_m": p.passo_distanza_m, "azimut_max_gradi": p.azimut_max_gradi,
                                    "portata_m": p.portata_m, "n_azimut": p.n_azimut, "n_distanza": p.n_distanza,
                                    "indice": "ia * n_distanza + ir; azimut = -azimut_max + (ia + 0,5) passo"}}
        sensori = [{"id": "profondita", "tipo": "camera di profondità (simulata)",
                    "origine": self.meta.get("sensore"), "licenza": self.meta.get("licenza")}]
        nota = ("camera ferma simulata: posa da meta.json, IMU e stima del piano del suolo fuori dal prototipo; "
                "etichette a mano" + (" (le regole a id_vero usano la verità SOLO per simulare il classificatore "
                                      "assente)" if self.etichette else "") +
                "; predittore: " + ("zona (porto semplificato di sd-1, non confrontato col banco in C)"
                                    if self.regole["predittore_zona"] else "velocità costante (disco che cresce, "
                                                                            "poi tutta l'ombra)"))
        return registro.intestazione(self.cfg, griglie, {"origine": "sensore", "assi": "x a destra, y in avanti"},
                                     sensori=sensori, nota=nota)

    def griglia_stati(self):
        return self._stati

    def passo(self, fotogramma, verita=None):
        t0 = time.perf_counter()
        L = riuso.modulo("catena", "parametri")
        prof, t = fotogramma.dati["profondita"], fotogramma.t
        uscita = self.catena.ciclo(fotogramma.indice, t, prof)
        sal = self.salute.passo(t, prof, uscita["pixel_validi"])
        persa = sal["salute"] == "affidabilita_persa"
        # --- griglia dichiarata: mai più «libero» della catena, solo meno
        st = self.catena.mappa_ciclo.stati.copy()
        if self.libero is not None:
            ok = self.libero.maschera(prof)
            st[(st == L.LIBERO) & ~ok] = L.NON_OSSERVATO
        if persa:
            st[:] = L.NON_OSSERVATO
        self._stati = st
        # --- traccia -> registro, con le etichette a mano
        pos = [(tr["id"], tr.get("x"), tr.get("z")) for tr in uscita["tracce"]]
        if self.etichette:
            for i, c in E.risolvi(self.etichette, pos, t, verita).items():
                self._classi.setdefault(i, c)
        lab = {i: self._classi[i] for i, _, _ in pos if i in self._classi}
        riga = registro.da_catena(uscita, self.cfg, etichette=lab, salute=sal)
        riga["verita"] = verita
        nr = self.par.n_distanza
        riga["celle"]["conteggi"] = {registro.STATI_CELLA[s]: int((st == s).sum()) for s in range(4)}
        riga["settori"] = livelli.per_settore(st, self.catena.possibile_presenza, self.settori,
                                              self.par.passo_distanza_m, riga["affidabilita"])
        strati = [tr.strato for tr in self.catena.inseguitore.tracce if tr.strato is not None] \
            + list(self.catena.inseguitore.orfani)
        for a, s in zip(riga["avvisi"], strati):
            ia, ir = np.nonzero(s.maschera)
            a["indici"] = (ia * nr + ir).tolist()
        # --- regione di previsione dal predittore della zona
        per_id = {tr["id"]: tr for tr in riga["tracce"]}
        for tr in self.catena.inseguitore.tracce:          # «non vista da»: dall'ingresso in ombra, non dall'ultimo stato
            if tr.strato is not None and tr.id in per_id:
                per_id[tr.id]["non_vista_da_s"] = round(t - tr.strato.t_ingresso, 4)
        for tr in self.catena.inseguitore.tracce:
            pr = getattr(tr, "predittore", None)
            if tr.stato != "previsto" or pr is None or not hasattr(pr, "ampio"):
                continue
            r = per_id[tr.id]
            if pr.ampio or pr.regione_celle is None:
                r.update(stato="previsto_ampio", pos=None, regione=None)
            else:
                ia, ir = np.nonzero(pr.regione_celle)
                r["regione"] = {"tipo": "celle", "griglia": "polare_corto", "indici": (ia * nr + ir).tolist(),
                                "livello": 0.90,
                                "livello_verificato": False}     # porto semplificato: vedi CORTO_RAGGIO.md
        # --- strato_finito = celle viste «libero»: è osservato
        for ev in riga["eventi"]:
            if ev.get("tipo") == "strato_finito":
                ev.update(come_lo_so="osservato", tolto_guardando=True)
        if persa:
            for r in riga["tracce"]:
                if r["stato"] != "in_conferma":
                    r.update(stato="previsto_ampio", pos=None, regione=None, identita=None)
        riga["eventi"] += self.eventi.passo(riga)
        riga["tempo_ciclo_ms"] = round((time.perf_counter() - t0) * 1000.0, 3)
        return riga


def dentro(riga, x, y, griglia):
    """La persona vera in (x, y) è dentro ciò che il sistema mostra? (regione di una traccia, o le celle
    dell'avviso per le tracce «previsto ampio»). Rende (dentro_mostrato, dentro_regione_stretta | None)."""
    p = griglia
    ia = math.floor((math.degrees(math.atan2(x, y)) + p["azimut_max_gradi"]) / p["passo_azimut_gradi"])
    ir = math.floor(math.hypot(x, y) / p["passo_distanza_m"])
    cella = ia * p["n_distanza"] + ir if 0 <= ia < p["n_azimut"] and 0 <= ir < p["n_distanza"] else None
    stretta, mostrato, ampie = None, False, set()
    for tr in riga["tracce"]:
        reg = tr.get("regione")
        if tr["stato"] == "previsto_ampio":
            ampie.add(tr["id"])
        if reg is None:
            continue
        if reg["tipo"] == "celle":
            d = cella is not None and cella in set(reg["indici"])
        else:
            d = math.hypot(x - reg["centro"][0], y - reg["centro"][1]) <= reg["raggio_m"]
        stretta = bool(stretta) or d
        mostrato = mostrato or d
    for a in riga["avvisi"]:
        if a["id_traccia"] in ampie and cella is not None and cella in set(a.get("indici", ())):
            mostrato = True
    return mostrato, stretta
