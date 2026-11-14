"""Modo a LUNGA PORTATA multisensore (aerei, droni, auto, treni). Il nucleo arriva da un altro ruolo come `movi_lp.py`
(celle a quattro stati per sensore, inseguitore a più sensori, insieme di possibile presenza, regione di previsione
per classe) con il suo simulatore di sensori: qui c'è SOLO l'adattatore verso l'interfaccia comune e il registro.

movi_lp.py si copia in riuso/lunga_portata/ tale e quale (con la provenienza in README.md) e si aggiunge a
movi.riuso.PEZZI. Se la sua interfaccia è diversa da quella attesa qui sotto, si cambia QUESTO file, non movi_lp.py.

Atteso da movi_lp (da confermare all'arrivo): una classe con `passo(t, misure_per_sensore, salute_per_sensore)`
che renda celle per sensore e fuse, tracce (id, stato, posizione, regione), insieme di possibile presenza.
Ambito: sola osservazione e avviso; nessuna funzione di ingaggio, puntamento o contrasto."""
from . import nucleo


class NucleoLungo(nucleo.Nucleo):
    modo = "lungo"

    def __init__(self, cfg, meta):
        raise NotImplementedError("passo 2: all'arrivo di movi_lp.py")

    def passo(self, fotogramma, verita=None):
        """movi_lp.passo -> fotogramma del registro (stesse parole del modo corto; `celle.per_sensore` pieno;
        regioni e avvisi come poligoni o insiemi di celle; la classe a mano sceglie SOLO il modello della regione)."""
        raise NotImplementedError("passo 2")
