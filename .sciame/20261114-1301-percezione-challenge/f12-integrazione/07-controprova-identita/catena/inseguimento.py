"""Inseguimento e stati dell'oggetto (blocchi B3, B4, B5 del nucleo).

Stati di una traccia in uscita:
  in_conferma         nata, non ancora 3 rilevamenti su 5 (non dà garanzie);
  osservato           confermata, con una misura in porta in questo ciclo (invariante 3);
  previsto            entrata in ombra: la previsione è mostrata (strato 2) e lo strato 1 è acceso;
  perso               il cerchio al 95 % copre almeno metà del cuneo: resta solo la possibile presenza (assorbente);
  non_confermato      senza misura in campo aperto, per al più 3 fotogrammi; poi la traccia si chiude;
  affidabilita_persa  senza misura, e la cella dell'ultima misura è «non osservato» (un buco)."""
import math
from collections import deque

import numpy as np

from kalman import Kalman, rumore_misura, ungherese
from parametri import CHI2_95, CHI2_99, NON_OSSERVATO
from presenza import PredittoreVelocitaCostante, StatoIngresso, Strato, cuneo_d_ingresso, riaggancio_ammesso

FUORI_PORTA = 1e9


class Traccia:
    def __init__(self, ident, gruppo, t, r, par):
        self.id, self.par = ident, par
        self.kf = Kalman(gruppo.x, gruppo.z, r, par.v_iniziale_m_s)
        self.stato, self.t_stato, self.confermata = "in_conferma", t, False
        self.storia = deque([True], maxlen=par.conferma_n)      # rilevata / non rilevata negli ultimi cicli
        self.ha_misura, self.misura_tagliata = True, False
        self.ultima_misura = (gruppo.x, gruppo.z, t)
        self.senza_misura = 0
        self.larghezza_m = gruppo.larghezza_m
        self.campioni = deque(maxlen=par.media_moto_fotogrammi)  # (ciclo, t, x, z) delle misure non tagliate
        self.medie = deque()                                     # (ciclo, t, x, z) medie di 3 fotogrammi di fila
        self.si_muove, self.t_moto = None, None
        self.strato = self.predittore = self.previsione = None
        self.attesa_misura_piena = False
        self.appena_ripartito = False            # f12 (F-408)

    def cambia_stato(self, nuovo, t):
        if nuovo != self.stato:
            self.stato, self.t_stato = nuovo, t

    def aggiorna_moto(self, k, t, x, z):
        """Regola «si muove» (B3, C8, V1): spostamento fra due medie di 3 fotogrammi distanti al più 1 s (la
        finestra cresce: si confronta con la media più vecchia che c'è), oltre 5·sigma(z)·sqrt(2) lungo l'asse
        radiale o quello tangenziale."""
        par, n = self.par, self.par.media_moto_fotogrammi
        self.campioni.append((k, t, x, z))
        if len(self.campioni) < n or self.campioni[-1][0] - self.campioni[0][0] != n - 1:
            return
        mx = sum(c[2] for c in self.campioni) / n
        mz = sum(c[3] for c in self.campioni) / n
        self.medie.append((k, t, mx, mz))
        while t - self.medie[0][1] > par.finestra_moto_s + 1e-6:
            self.medie.popleft()
        k0, _, x0, z0 = self.medie[0]
        if k - k0 < n:                                 # le due medie non devono condividere fotogrammi
            return
        d0, d1 = math.hypot(x0, z0), math.hypot(mx, mz)
        lontana = max(d0, d1)
        cx, cz = (x0 + mx) / 2.0, (z0 + mz) / 2.0
        c = math.hypot(cx, cz) or 1.0
        radiale = abs((mx - x0) * cx + (mz - z0) * cz) / c
        tangenziale = abs((mx - x0) * cz - (mz - z0) * cx) / c
        fattore = par.soglia_moto_sigma * math.sqrt(2.0) * par.fattore_media_moto
        self.si_muove = (radiale > fattore * par.sigma_radiale(lontana)
                         or tangenziale > fattore * par.sigma_tangenziale(lontana))
        self.t_moto = t


class Inseguitore:
    def __init__(self, par, griglia, fabbrica_predittore=PredittoreVelocitaCostante):
        self.par, self.griglia, self.fabbrica_predittore = par, griglia, fabbrica_predittore
        self.tracce, self.prossimo_id = [], 1
        self.t_prec, self.k = None, -1
        self.orfani = []                         # f12 (F-409): strati rimasti dopo un riaggancio

    # ------------------------------------------------------------------ misure
    def _r(self, x, z, tagliato=False, larghezza=0.0):
        d = math.hypot(x, z)
        r = rumore_misura(x, z, self.par.sigma_radiale(d), self.par.sigma_tangenziale(d))
        if tagliato:      # lettura: il centro di un gruppo tagliato può sbagliare fino a metà larghezza dell'oggetto
            r = r + np.eye(2) * (max(larghezza, self.par.larghezza_min_m) / 2.0) ** 2
        return r

    def _misura(self, tr, g, t, eventi):
        """La traccia riceve il gruppo g come misura del ciclo. Un gruppo tagliato tiene viva la traccia ma non
        aggiorna il filtro e non entra nella regola «si muove» (C6)."""
        tr.ha_misura, tr.misura_tagliata = True, g.tagliato
        tr.ultima_misura = (g.x, g.z, t)
        tr.storia.append(True)
        tr.senza_misura = 0
        if tr.appena_ripartito:                    # f12 (F-408): il filtro è appena ripartito da questa misura
            tr.appena_ripartito = False
            tr.larghezza_m = max(tr.larghezza_m, g.larghezza_m)
        elif g.tagliato and self.par.riparti_al_riaggancio and tr.attesa_misura_piena:
            tr.kf.aggiorna((g.x, g.z), self._r(g.x, g.z, True, tr.larghezza_m))   # tagliata dopo un riaggancio: R gonfiato
        elif not g.tagliato:
            r = self._r(g.x, g.z)
            d2 = tr.kf.innovazione((g.x, g.z), r)[2]
            if tr.attesa_misura_piena:
                tr.attesa_misura_piena = False
                eventi.append({"tipo": "prima_misura_piena", "id": tr.id, "d2": round(d2, 3),
                               "in95": d2 <= CHI2_95, "in99": d2 <= CHI2_99})
            if d2 <= CHI2_99:
                tr.kf.aggiorna((g.x, g.z), r)
            else:                                   # può accadere solo dopo un riaggancio (la porta non c'entra)
                tr.kf.riparti(g.x, g.z, r, self.par.v_iniziale_m_s)
            tr.larghezza_m = g.larghezza_m
            tr.aggiorna_moto(self.k, t, g.x, g.z)
        if not tr.confermata and sum(tr.storia) >= self.par.conferma_m:
            tr.confermata = True
            eventi.append({"tipo": "conferma", "id": tr.id})
        tr.cambia_stato("osservato" if tr.confermata else "in_conferma", t)

    def _associa(self, tracce, gruppi, liberi, t, eventi):
        """Porta al 99 % e assegnazione ungherese fra le tracce date e i gruppi ancora liberi."""
        if not tracce or not liberi:
            return liberi
        costo = np.full((len(tracce), len(liberi)), FUORI_PORTA)
        for i, tr in enumerate(tracce):
            for j, gi in enumerate(liberi):
                g = gruppi[gi]
                d2 = tr.kf.innovazione((g.x, g.z), self._r(g.x, g.z, g.tagliato, tr.larghezza_m))[2]
                if d2 <= CHI2_99:
                    costo[i, j] = d2
        presi = set()
        for i, j in ungherese(costo):
            if costo[i, j] < FUORI_PORTA:
                self._misura(tracce[i], gruppi[liberi[j]], t, eventi)
                presi.add(j)
        return [gi for j, gi in enumerate(liberi) if j not in presi]

    # ------------------------------------------------------------------ ritorno dall'ombra
    def _riagganci(self, gruppi, liberi, ciclo, etichette, t, eventi):
        restano = []
        for gi in liberi:
            g = gruppi[gi]
            pendenti = [tr for tr in self.tracce if tr.strato is not None]
            esiti = [(tr,) + riaggancio_ammesso(g, tr.strato, ciclo, etichette, self.griglia, self.par)
                     for tr in pendenti]
            ammesse = [tr for tr, ok, _ in esiti if ok]
            in_gara = len(pendenti) if self.par.pendenti_ambito == "globale" else len(ammesse)
            if len(ammesse) == 1 and in_gara == 1:
                self._riaggancia(ammesse[0], g, ciclo, t, eventi)
                continue
            for tr, ok, motivo in esiti:            # il rilevamento tocca uno strato ma non ne prende l'identità
                if ok or motivo is not None:
                    eventi.append({"tipo": "identita_ambigua", "id": tr.id,
                                   "motivo": motivo or f"{in_gara} tracce pendenti"})
            restano.append(gi)
        return restano

    def _riaggancia(self, tr, g, ciclo, t, eventi):
        prev = tr.predittore.passo(t, ciclo, self.griglia)
        y = np.array([g.x - prev.x, g.z - prev.z])
        d2 = float(y @ np.linalg.solve(prev.p + self._r(g.x, g.z, g.tagliato, tr.larghezza_m), y))
        eventi.append({"tipo": "riaggancio", "id": tr.id, "stato_prima": tr.stato,
                       "durata_s": round(t - tr.strato.t_ingresso, 4), "buio_s": round(t - tr.ultima_misura[2], 4),
                       "errore_previsione_m": round(float(np.hypot(*y)), 4), "raggio95_m": round(prev.raggio95, 4),
                       "d2": round(d2, 3), "in95": d2 <= CHI2_95, "misura_tagliata": g.tagliato})
        if self.par.strato_resta:                  # f12 (F-409): l'avviso resta finché le celle non sono viste libere
            tr.strato.orfano = True
            self.orfani.append(tr.strato)
            eventi[-1]["identita"] = "presunta"
        else:
            tr.strato.fine = "riaggancio"
        tr.strato = tr.predittore = tr.previsione = None
        tr.attesa_misura_piena = True
        if self.par.riparti_al_riaggancio:         # f12 (F-408): riparte dalla misura, R gonfiato di metà larghezza
            tr.kf.riparti(g.x, g.z, self._r(g.x, g.z, True, max(tr.larghezza_m, g.larghezza_m)),
                          self.par.v_iniziale_m_s)
            tr.campioni.clear()
            tr.medie.clear()
            tr.appena_ripartito = True
        self._misura(tr, g, t, eventi)

    # ------------------------------------------------------------------ cicli senza misura
    def _pendente(self, tr, ciclo, t, eventi):
        """Traccia in ombra: aggiorna la previsione, decide previsto → perso, rilascia le celle viste libere."""
        par = self.par
        tr.previsione = tr.predittore.passo(t, ciclo, self.griglia)
        if tr.strato.aggiorna(ciclo):
            tr.strato.fine = "celle_libere"
            eventi.append({"tipo": "strato_finito", "id": tr.id, "motivo": "celle_libere",
                           "eta_s": round(t - tr.strato.t_ingresso, 4)})
            return self._chiudi(tr, "non_piu_rilevato", eventi)
        if tr.stato == "previsto":
            meta_cuneo = par.frazione_perso * tr.strato.area_nucleo()
            if (math.pi * tr.previsione.raggio95 ** 2 >= meta_cuneo
                    and tr.strato.area_coperta(tr.previsione) >= meta_cuneo):
                eventi.append({"tipo": "perso", "id": tr.id, "previsto_s": round(t - tr.strato.t_ingresso, 4)})
                tr.cambia_stato("perso", t)
        return True

    def _senza_misura(self, tr, ciclo, gruppi, etichette, t, eventi):
        """Restituisce False se la traccia va tolta."""
        par = self.par
        tr.ha_misura = False
        tr.storia.append(False)
        if not tr.confermata:                        # non può più arrivare a 3 su 5: scartata in silenzio
            return list(tr.storia).count(False) <= par.conferma_n - par.conferma_m
        if tr.strato is not None:
            return self._pendente(tr, ciclo, t, eventi)
        x, z, _ = tr.ultima_misura                   # B5: si guarda l'ultima misura, non il punto previsto
        nucleo = cuneo_d_ingresso(ciclo, gruppi, etichette, self.griglia, x, z, par)
        if nucleo is not None:
            ingresso = StatoIngresso(tr.id, t, tr.kf.x.copy(), tr.kf.p.copy(), tr.ultima_misura, tr.larghezza_m,
                                     nucleo)
            tr.strato = Strato(ingresso, self.griglia, par)
            tr.predittore = self.fabbrica_predittore(ingresso, par)
            tr.cambia_stato("previsto", t)
            eventi.append({"tipo": "ingresso_in_ombra", "id": tr.id, "celle_nucleo": int(nucleo.sum()),
                           "area_nucleo_m2": round(tr.strato.area_nucleo(), 4)})
            return self._pendente(tr, ciclo, t, eventi)
        cella = self.griglia.cella(x, z)
        if cella is None or ciclo.stati[cella] == NON_OSSERVATO:
            tr.cambia_stato("affidabilita_persa", t)  # lettura: resta finché quella cella non si rivede
            return True
        tr.senza_misura += 1
        if tr.senza_misura > par.non_confermato_fotogrammi:
            return self._chiudi(tr, "non_piu_rilevato", eventi)
        tr.cambia_stato("non_confermato", t)
        return True

    def _chiudi(self, tr, motivo, eventi):
        eventi.append({"tipo": "chiusura", "id": tr.id, "motivo": motivo})
        return False

    # ------------------------------------------------------------------ un ciclo
    def passo(self, t, ciclo, gruppi, etichette):
        """Aggiorna le tracce con i gruppi del ciclo. Restituisce la lista degli eventi."""
        self.k += 1
        eventi = []
        dt = 0.0 if self.t_prec is None else t - self.t_prec
        self.t_prec = t
        for tr in self.tracce:
            tr.ha_misura = False
            if dt > 0:
                tr.kf.predici(dt, self.par.q)
        liberi = list(range(len(gruppi)))
        attive = [tr for tr in self.tracce if tr.strato is None]
        liberi = self._associa([tr for tr in attive if tr.confermata], gruppi, liberi, t, eventi)   # priorità
        liberi = self._associa([tr for tr in attive if not tr.confermata], gruppi, liberi, t, eventi)
        liberi = self._riagganci(gruppi, liberi, ciclo, etichette, t, eventi)
        self.tracce = [tr for tr in self.tracce
                       if tr.ha_misura or self._senza_misura(tr, ciclo, gruppi, etichette, t, eventi)]
        for gi in liberi:                            # lettura: un gruppo tagliato non fa nascere una traccia
            g = gruppi[gi]
            if not g.tagliato:
                self.tracce.append(Traccia(self.prossimo_id, g, t, self._r(g.x, g.z), self.par))
                self.tracce[-1].aggiorna_moto(self.k, t, g.x, g.z)
                eventi.append({"tipo": "nascita", "id": self.prossimo_id})
                self.prossimo_id += 1
        vivi = []                                    # f12 (F-409): gli strati orfani si rilasciano cella per cella
        for s in self.orfani:
            if s.aggiorna(ciclo):
                eventi.append({"tipo": "strato_finito", "id": s.id_traccia, "motivo": "celle_libere_dopo_riaggancio",
                               "eta_s": round(t - s.t_ingresso, 4)})
            else:
                vivi.append(s)
        self.orfani = vivi
        return eventi
