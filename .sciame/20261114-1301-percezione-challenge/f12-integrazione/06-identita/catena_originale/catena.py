"""La catena di riferimento: profondità → mappa a quattro stati → gruppi → tracce e stati → possibile presenza →
uscita per fotogramma. È codice di VALIDAZIONE del nucleo (f4/H-012/05-correzioni/SOLUZIONE_V2.md), non il prototipo.

Uso da codice:
    catena = Catena(meta, Parametri())            # la posa viene da meta.json; se manca, passarla (stima_suolo)
    for indice, t, prof in sorgente:
        uscita = catena.ciclo(indice, t, prof)    # dizionario pronto per una riga JSON
        catena.mappa_ciclo.stati                  # (azimut, distanza) uint8, per chi confronta con la verità
        catena.possibile_presenza                 # maschera delle celle con possibile presenza
Oppure `esegui(sorgente, cartella_uscita)`, che scrive fotogrammi.jsonl e riassunto.json."""
import json
import math
import os
import time

import numpy as np

from geometria import Proiezione, posa_da_meta, stima_suolo
from gruppi import trova_gruppi
from inseguimento import Inseguitore
from mappa import InvarianteViolato, Mappa
from parametri import LIBERO, NOMI_STATI, Parametri
from presenza import PredittoreVelocitaCostante

FOTOGRAMMI_PER_LA_POSA = 5


def _a(v, cifre=4):
    return round(float(v), cifre)


class Catena:
    def __init__(self, meta, par=None, posa=None, fabbrica_predittore=PredittoreVelocitaCostante):
        self.par = par or Parametri()
        self.posa = posa or posa_da_meta(meta)
        if self.posa is None:
            raise ValueError("posa assente in meta.json: stimarla con geometria.stima_suolo e passarla")
        self.mappa = Mappa(self.par, Proiezione(meta, self.posa, self.par))
        self.griglia = self.mappa.griglia
        self.inseguitore = Inseguitore(self.par, self.griglia, fabbrica_predittore)
        self.mappa_ciclo, self.gruppi, self.etichette = None, [], None
        self.possibile_presenza = np.zeros((self.par.n_azimut, self.par.n_distanza), dtype=bool)
        per_settore = max(1, int(round(self.par.settore_gradi / self.par.passo_azimut_gradi)))
        self._settori = [(a, min(a + per_settore, self.par.n_azimut))
                         for a in range(0, self.par.n_azimut, per_settore)]

    def ciclo(self, indice, t, prof):
        """Elabora un fotogramma e restituisce l'uscita del ciclo (un dizionario serializzabile in JSON)."""
        self.mappa_ciclo = self.mappa.aggiorna(prof, t)
        self.gruppi, self.etichette = trova_gruppi(self.mappa_ciclo, self.par)
        eventi = self.inseguitore.passo(t, self.mappa_ciclo, self.gruppi, self.etichette)
        strati = [tr.strato for tr in self.inseguitore.tracce if tr.strato is not None]
        self.possibile_presenza = np.zeros_like(self.possibile_presenza)
        for s in strati:
            self.possibile_presenza |= s.maschera
        if self.par.verifica_invarianti:
            self.verifica(strati)
        conteggi = self.mappa_ciclo.conteggi()
        return {
            "indice": int(indice), "t": _a(t, 6),
            "contatore_sensore": int(indice),                    # invariante 8: ogni uscita porta il contatore
            "celle": {NOMI_STATI[s]: int(conteggi[s]) for s in range(4)},
            "libero_per_eta": [int(v) for v in np.bincount(                 # età in fotogrammi: 0 = visto ora
                self.mappa_ciclo.eta[self.mappa_ciclo.stati == LIBERO], minlength=self.par.memoria_fotogrammi)],
            "pixel_validi": self.mappa_ciclo.pixel_validi,
            "suolo_visto_in_ombra": self.mappa_ciclo.suolo_visto_in_ombra,
            "celle_ambigue": int(self.mappa_ciclo.ambigua.sum()),
            "settori": self._uscita_settori(),
            "gruppi": [{"x": _a(g.x), "z": _a(g.z), "larghezza_m": _a(g.larghezza_m), "celle": int(len(g.ia)),
                        "punti": g.n_punti, "tagliato": g.tagliato} for g in self.gruppi],
            "tracce": [self._uscita_traccia(tr, t) for tr in self.inseguitore.tracce],
            "possibili_presenze": [self._uscita_strato(s, t) for s in strati],
            "eventi": eventi,
        }

    # ------------------------------------------------------------------ invarianti (3, 4, 7 del nucleo)
    def verifica(self, strati):
        for tr in self.inseguitore.tracce:
            if tr.stato == "osservato" and not tr.ha_misura:
                raise InvarianteViolato(f"invariante 3: traccia {tr.id} «osservato» senza misura nel ciclo")
            if (tr.stato in ("previsto", "perso")) != (tr.strato is not None):
                raise InvarianteViolato(f"traccia {tr.id}: «{tr.stato}» e strato di possibile presenza non coerenti")
        libero = self.mappa_ciclo.stati == LIBERO
        for s in strati:
            if s.fine is not None:
                raise InvarianteViolato("invariante 7: uno strato finito è ancora in uscita")
            ia, ir = np.nonzero(s.maschera & libero)         # invariante 4: sul «libero» solo entro la fascia
            na, nr = np.nonzero(s.nucleo)
            if len(ia) and len(na):
                d2 = ((self.griglia.x[ia, ir][:, None] - self.griglia.x[na, nr][None, :]) ** 2
                      + (self.griglia.z[ia, ir][:, None] - self.griglia.z[na, nr][None, :]) ** 2)
                if float(d2.min(axis=1).max()) > (self.par.fascia_m + 1e-4) ** 2:
                    raise InvarianteViolato("invariante 4: possibile presenza su «libero» oltre la fascia")

    # ------------------------------------------------------------------ uscita
    def _uscita_settori(self):
        c, passo = self.mappa_ciclo, self.par.passo_distanza_m
        fuori = []
        for a0, a1 in self._settori:
            n = np.bincount(c.stati[a0:a1].ravel(), minlength=4)
            primo = int(c.primo[a0:a1].min())
            fuori.append({"azimut_gradi": [_a(self.griglia.azimut[a0] - self.par.passo_azimut_gradi / 2, 1),
                                           _a(self.griglia.azimut[a1 - 1] + self.par.passo_azimut_gradi / 2, 1)],
                          "celle": [int(v) for v in n],          # nell'ordine di NOMI_STATI
                          "primo_occupato_m": _a(primo * passo, 2) if primo < self.par.n_distanza else None,
                          "possibile_presenza": int(self.possibile_presenza[a0:a1].sum())})
        return fuori

    def _uscita_traccia(self, tr, t):
        u = {"id": tr.id, "stato": tr.stato, "eta_stato_s": _a(t - tr.t_stato), "misura_nel_ciclo": tr.ha_misura,
             "misura_tagliata": bool(tr.ha_misura and tr.misura_tagliata),
             "ultima_misura": [_a(tr.ultima_misura[0]), _a(tr.ultima_misura[1]), _a(tr.ultima_misura[2], 6)],
             "larghezza_m": _a(tr.larghezza_m)}
        moto_fresco = tr.t_moto is not None and t - tr.t_moto <= self.par.finestra_moto_s + 1e-6
        u["si_muove"] = tr.si_muove if moto_fresco else None      # None = non valutabile ora
        if tr.strato is None:                                    # stato del filtro (con misura tagliata: non aggiornato)
            x, p = tr.kf.x, tr.kf.p
            u.update(x=_a(x[0]), z=_a(x[1]), vx=_a(x[2]), vz=_a(x[3]),
                     covarianza=[_a(p[0, 0], 6), _a(p[0, 1], 6), _a(p[1, 1], 6)],
                     chi2_velocita=_a(tr.kf.chi2_velocita(), 3))
            return u
        prev = tr.previsione
        diagnostica = {"x": _a(prev.x), "z": _a(prev.z), "raggio95_m": _a(prev.raggio95),
                       "covarianza": [_a(prev.p[0, 0], 6), _a(prev.p[0, 1], 6), _a(prev.p[1, 1], 6)]}
        if tr.stato == "previsto":                               # «perso» non porta posizione (invariante 9)
            area = tr.strato.area_nucleo()
            u.update(x=diagnostica["x"], z=diagnostica["z"], covarianza=diagnostica["covarianza"])
            u["regione_prevista"] = {"x": diagnostica["x"], "z": diagnostica["z"],
                                     "raggio95_m": diagnostica["raggio95_m"],
                                     "frazione_del_cuneo": _a(tr.strato.area_coperta(prev) / area if area else 1.0)}
        u["previsione_diagnostica"] = diagnostica                # solo per la validazione: non è un'uscita del prototipo
        return u

    def _uscita_strato(self, s, t):
        ia, ir = np.nonzero(s.maschera)
        return {"id_traccia": s.id_traccia, "eta_s": _a(t - s.t_ingresso), "celle": int(len(ia)),
                "celle_nucleo": int(s.nucleo.sum()), "celle_rilasciate": s.celle_rilasciate,
                "area_m2": _a(self.griglia.area[s.maschera].sum()),
                "azimut_gradi": [_a(self.griglia.azimut[ia.min()], 1), _a(self.griglia.azimut[ia.max()], 1)],
                "distanza_m": [_a(self.griglia.distanza[ir.min()], 2), _a(self.griglia.distanza[ir.max()], 2)]}


def _con_posa(sorgente, meta, posa, par, fabbrica_predittore):
    """Costruisce la catena; se la posa manca la stima dai primi fotogrammi, che poi vengono elaborati lo stesso."""
    fotogrammi = iter(sorgente)
    attesa = []
    if posa is None and posa_da_meta(meta) is None:
        for _ in range(FOTOGRAMMI_PER_LA_POSA):
            try:
                attesa.append(next(fotogrammi))
            except StopIteration:
                break
        posa, _ = stima_suolo([f for _, _, f in attesa], meta)
    catena = Catena(meta, par, posa, fabbrica_predittore)

    def tutti():
        yield from attesa
        yield from fotogrammi
    return catena, tutti()


def esegui(sorgente, cartella_uscita=None, par=None, posa=None, salva_griglie=False,
           fabbrica_predittore=PredittoreVelocitaCostante):
    """Passa tutta la sorgente nella catena. Scrive, se c'è la cartella, `fotogrammi.jsonl` (una riga per
    fotogramma), `riassunto.json` e, a richiesta, `griglie.npz`. Restituisce il riassunto."""
    par = par or Parametri()
    catena, fotogrammi = _con_posa(sorgente, sorgente.meta, posa, par, fabbrica_predittore)
    righe = None
    if cartella_uscita is not None:
        os.makedirs(cartella_uscita, exist_ok=True)
        righe = open(os.path.join(cartella_uscita, "fotogrammi.jsonl"), "w", encoding="utf-8")
    tempi_ms, celle, eventi, identita = [], np.zeros(4, dtype=np.int64), {}, set()
    diagnostici = {"suolo_visto_in_ombra": 0, "celle_ambigue": 0}
    griglie, eta, presenze, indici, istanti = [], [], [], [], []
    try:
        for indice, t, prof in fotogrammi:
            t0 = time.perf_counter()
            uscita = catena.ciclo(indice, t, prof)
            tempi_ms.append((time.perf_counter() - t0) * 1000.0)
            uscita["tempo_ciclo_ms"] = round(tempi_ms[-1], 3)
            celle += catena.mappa_ciclo.conteggi()
            for nome in diagnostici:
                diagnostici[nome] += uscita[nome]
            for e in uscita["eventi"]:
                eventi[e["tipo"]] = eventi.get(e["tipo"], 0) + 1
            identita.update(tr["id"] for tr in uscita["tracce"] if tr["stato"] != "in_conferma")
            if righe is not None:
                righe.write(json.dumps(uscita, ensure_ascii=False, separators=(",", ":")) + "\n")
            if salva_griglie:
                griglie.append(catena.mappa_ciclo.stati.copy())
                eta.append(np.minimum(catena.mappa_ciclo.eta, 255).astype(np.uint8))
                presenze.append(catena.possibile_presenza.copy())
                indici.append(indice)
                istanti.append(t)
    finally:
        if righe is not None:
            righe.close()
    n = len(tempi_ms)
    ordinati = sorted(tempi_ms)
    posa_usata = catena.posa
    riassunto = {
        "fotogrammi": n,
        "sensore": sorgente.meta.get("sensore"),
        "posa": {"altezza_m": _a(posa_usata.altezza_m), "inclinazione_gradi": _a(posa_usata.inclinazione_gradi, 3),
                 "rollio_gradi": _a(posa_usata.rollio_gradi, 3), "stimata": posa_usata.stimata, "nota": posa_usata.nota},
        "parametri": {k: v for k, v in vars(par).items()},
        "griglia": {"azimut": par.n_azimut, "distanza": par.n_distanza, "celle": par.n_azimut * par.n_distanza},
        "celle_per_stato": {NOMI_STATI[s]: int(celle[s]) for s in range(4)},
        "frazione_per_stato": {NOMI_STATI[s]: _a(celle[s] / max(1, celle.sum())) for s in range(4)},
        "diagnostici": diagnostici,
        "tracce_confermate": len(identita),
        "eventi": eventi,
        "tempo_ciclo_ms": {"media": _a(sum(tempi_ms) / n, 3), "p95": _a(ordinati[math.ceil(0.95 * n) - 1], 3),
                           "massimo": _a(ordinati[-1], 3),
                           "nota": "solo elaborazione (lettura e scrittura escluse), invarianti "
                                   + ("accesi" if par.verifica_invarianti else "spenti")} if n else None,
    }
    if cartella_uscita is not None:
        with open(os.path.join(cartella_uscita, "riassunto.json"), "w", encoding="utf-8") as f:
            json.dump(riassunto, f, ensure_ascii=False, indent=2)
            f.write("\n")
        if salva_griglie:
            np.savez_compressed(os.path.join(cartella_uscita, "griglie.npz"), stati=np.array(griglie, dtype=np.uint8),
                                eta_fotogrammi=np.array(eta, dtype=np.uint8),
                                possibile_presenza=np.array(presenze, dtype=bool),
                                indici=np.array(indici), tempi=np.array(istanti),
                                azimut_gradi=catena.griglia.azimut, distanza_m=catena.griglia.distanza)
    return riassunto
