"""Cose comuni agli attacchi di 22-avversario: percorsi e importazione (sola lettura) di catena, simulatore, validazione."""
import os
import sys

for _n in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_n, "1")
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
F10 = os.path.dirname(QUI)
CATENA = os.path.join(F10, "10-catena")
SIM = os.path.join(F10, "11-simulatore")
VAL = os.path.join(F10, "20-validazione")
SEQ_SIM = os.path.join(SIM, "sequenze")
TRACCE = os.path.join(F10, "12-dati-veri", "tracce")
USCITE = os.path.join(QUI, "uscite")
for p in (CATENA,):
    if p not in sys.path:
        sys.path.insert(0, p)
