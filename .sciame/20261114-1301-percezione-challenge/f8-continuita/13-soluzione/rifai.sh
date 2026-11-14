#!/bin/sh
# Rifa' la prova di sciame-scene-dinamiche (f8, fase f3). Da eseguire in questa cartella; un lancio alla volta, ognuno <= 120 s.
# comp.c = banco.c di 11-misure (sha256 e158c7a9...) + applica_modifiche.py (gia' applicato: non rilanciarlo su comp.c).
set -e
gcc -O2 -Wall -Wno-misleading-indentation -Wno-maybe-uninitialized -o comp comp.c -lm
mkdir -p ris
for g in D T L; do timeout 120 ./comp prova $g 0.9 0 0.20 0 12000 400 0123456 ${g}12k > ris/prova_${g}.tsv; done
for g in T L; do for n in 1 10; do timeout 120 ./comp tempo $g $n; done; done > ris/tempi.txt
PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 leggi.py > ris/LETTURA.txt
