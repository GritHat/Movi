#!/bin/sh
# Rifa' tutte le prove di sciame-inferenza (f8). Un lancio alla volta, ognuno al piu' 120 s. Semi fissati negli script.
# Nota: risultati_det.txt, risultati_copertura_ist.txt e risultati2_ist025.txt sono nati PRIMA della correzione
# dell'inizializzazione dell'istogramma: si rifanno con IST_VECCHIO=1.
cd "$(dirname "$0")" || exit 1
export PYTHONDONTWRITEBYTECODE=1
timeout 120 python3 inf.py tempi
NORA=120000 timeout 120 python3 inf.py oracolo          # scrive oracolo.json (circa 85 s)
IST_VECCHIO=1 timeout 120 python3 inf.py det
timeout 120 python3 inf.py pf
timeout 120 python3 inf.py copertura
timeout 120 python3 inf.py falso
IST_VECCHIO=1 timeout 120 python3 inf.py copertura_ist
for c in mgx pf2 falso2 pezzi; do timeout 120 python3 inf2.py $c; done
IST_VECCHIO=1 timeout 120 python3 inf2.py ist025
timeout 120 python3 inf.py det                           # istogramma corretto (risultati3_det_ist_corretto.txt)
timeout 120 python3 inf2.py ist025                       # risultati3_ist025_corretto.txt
for c in ellisse dieci; do timeout 120 python3 inf3.py $c; done
