"""Accesso al codice riusato (cartella `riuso/`, copiato tale e quale dallo sciame: vedi README.md e IMPRONTE.txt).

Il codice riusato usa importazioni piatte (`from geometria import …`): qui si mette la sua cartella nel percorso e si
restituisce il modulo. NON si modifica niente dentro `riuso/`: le aggiunte stanno in `movi/`."""
import importlib
import os
import sys

RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "riuso"))

# nome logico -> (cartella dentro riuso/, moduli che contiene)
PEZZI = {
    "catena": ("catena", ("catena", "parametri", "sorgente", "geometria", "mappa", "gruppi", "inseguimento",
                          "kalman", "presenza", "scene_a_mano")),
    "simulatore": ("11-simulatore", ("simsens", "catalogo", "genera")),
    "infrastruttura": ("03-infrastruttura", ("controlla_sequenza",)),
    "libero": ("libero", ("libero",)),
    "eventi": ("eventi", ("eventi",)),
}


def modulo(pezzo, nome):
    """Restituisce il modulo `nome` del pezzo riusato `pezzo` (per esempio modulo("catena", "catena"))."""
    cartella, nomi = PEZZI[pezzo]
    if nome not in nomi:
        raise KeyError(f"{nome} non è fra i moduli riusati di «{pezzo}»: {nomi}")
    percorso = os.path.join(RADICE, cartella)
    if percorso not in sys.path:
        sys.path.insert(0, percorso)
    if pezzo == "simulatore":                       # genera.py cerca controlla_sequenza in ../03-infrastruttura
        infra = os.path.join(RADICE, "03-infrastruttura")
        if infra not in sys.path:
            sys.path.insert(1, infra)
    return importlib.import_module(nome)


def percorso(*parti):
    """Percorso di un file dentro `riuso/` (profili, sorgenti C, parametri dei sensori)."""
    return os.path.join(RADICE, *parti)
