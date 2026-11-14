"""Predittore della zona (sd-1: 400 membri, fronte + scia, lisciatura, regione al 90 %, soglia «ampio»).

DECISIONE: PORTO IN PYTHON del solo nucleo del predittore di riuso/c/insieme.c (righe 162–205: Pred, mpos,
pred_init, smooth, hdr, pred_step: 43 righe di C) più la libreria dei percorsi (build_lib, traj). Il resto di
insieme.c è banco (generatore, statistiche, main): non si porta, si CHIAMA come programma dal tabellone.
Motivo: insieme.c è un programma con stato globale, non una libreria; la catena ha già l'aggancio
(`fabbrica_predittore`, riuso/catena/presenza.py righe 42–56) e chiede solo `passo(t, ciclo, griglia) -> Previsione`.

Interruttore «predittore_zona»: PARTE SPENTO. Si accende solo dopo `prove/prova_predittore.py`: stessi percorsi,
stessa geometria T, quota «dentro la zona» del porto entro l'intervallo di Wilson al 95 % del banco in C."""


class PredittoreZona:
    """Stessa forma di presenza.PredittoreVelocitaCostante: costruito con (ingresso: StatoIngresso, par)."""

    def __init__(self, ingresso, par):
        raise NotImplementedError("passo 1 (dopo la composizione; facoltativo per la prima consegna)")

    def passo(self, t, ciclo, griglia):
        """Rende presenza.Previsione; in più tiene `self.celle` (maschera della regione al 90 %) e `self.ampio`."""
        raise NotImplementedError

    def regione(self):
        """La regione nella forma del registro: {"tipo": "celle", "griglia": …, "indici": […]} oppure, se ampio, None
        (la traccia esce «previsto ampio», senza punto)."""
        raise NotImplementedError
