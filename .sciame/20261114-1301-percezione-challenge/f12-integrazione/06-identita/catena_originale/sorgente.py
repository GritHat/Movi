"""Sorgenti di fotogrammi di profondità. La catena conosce solo l'interfaccia `Sorgente`: oggi una cartella nel
formato comune (03-infrastruttura/formato_sequenza.md) o una lista in memoria, domani un sensore vero.

Un fotogramma è (indice, tempo in secondi, matrice uint16 in millimetri lungo l'asse ottico, 0 = nessun dato)."""
import csv
import json
import os

import numpy as np


class Sorgente:
    """Interfaccia: `meta` (dizionario del formato comune) e l'iterazione sui fotogrammi."""
    meta: dict

    def __iter__(self):
        raise NotImplementedError


def controlla_fotogramma(prof, meta):
    if prof.dtype != np.uint16 or prof.shape != (meta["altezza"], meta["larghezza"]):
        raise ValueError(f"fotogramma: atteso uint16 {(meta['altezza'], meta['larghezza'])}, "
                         f"trovato {prof.dtype} {prof.shape}")
    return prof


class SorgenteMemoria(Sorgente):
    """Fotogrammi già in memoria (le prove, o un adattatore di un sensore che li accoda)."""

    def __init__(self, meta, tempi, fotogrammi):
        self.meta, self.tempi, self.fotogrammi = meta, list(tempi), fotogrammi

    def __iter__(self):
        for i, (t, f) in enumerate(zip(self.tempi, self.fotogrammi)):
            yield i, float(t), controlla_fotogramma(np.asarray(f), self.meta)


class SorgenteCartella(Sorgente):
    """Una sequenza su disco nel formato comune. Dati non fidati: i .npy si leggono sempre senza pickle.

    `ogni` = N elabora un fotogramma ogni N (per portare 30 fps ai 15 Hz del nucleo)."""

    def __init__(self, cartella, ogni=1, primo=0, ultimo=None):
        self.cartella = cartella
        with open(os.path.join(cartella, "meta.json"), encoding="utf-8") as f:
            self.meta = json.load(f)
        self.indici, self.tempi = [], []
        with open(os.path.join(cartella, "tempi.csv"), encoding="utf-8", newline="") as f:
            for riga in csv.reader(f):
                riga = [c.strip() for c in riga]
                if len(riga) != 2 or riga[0] == "indice":
                    continue                                   # intestazione o riga vuota
                self.indici.append(int(riga[0]))
                self.tempi.append(float(riga[1]))
        scelti = range(primo, len(self.indici) if ultimo is None else min(ultimo + 1, len(self.indici)), ogni)
        self.scelti = list(scelti)

    def __len__(self):
        return len(self.scelti)

    def __iter__(self):
        for k in self.scelti:
            i = self.indici[k]
            prof = np.load(os.path.join(self.cartella, "profondita", f"{i:06d}.npy"), allow_pickle=False)
            yield i, self.tempi[k], controlla_fotogramma(prof, self.meta)
