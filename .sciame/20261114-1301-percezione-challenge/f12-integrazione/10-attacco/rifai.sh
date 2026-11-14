#!/bin/sh
# rifai.sh — rifa' gli attacchi di 10-attacco (circa 4 minuti; processi leggeri, un filo l'uno, al piu' 2 alla volta).
# Scrive solo in questa cartella. Niente git, sudo, rete. Le copie dei banchi stanno in libero_rifatto/ e insieme_rifatto/ (impronte in ris/IMPRONTE.txt).
set -e
cd "$(dirname "$0")"
PY=/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f10-dati/ambiente/venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p ris
gcc -O2 -Wno-misleading-indentation -o insieme_rifatto/insieme insieme_rifatto/insieme.c -lm
( cd libero_rifatto && timeout 400 $PY -I -B banco_libero.py 30 && timeout 60 $PY -I -B riepilogo.py >/dev/null \
  && timeout 400 $PY -I -B banco_libero.py 30 x avv && timeout 60 $PY -I -B riepilogo.py avv >/dev/null )      # P1, P2
cmp libero_rifatto/riepilogo_banco.txt ../03-libero/riepilogo_banco.txt && echo "riepilogo identico a 03-libero"
timeout 240 $PY -I -B a_libero.py > ris/a_libero.txt                                                            # P3, P4, P7
timeout 60 $PY -I -B a_coperto.py > ris/a_coperto.txt                                                           # P10
timeout 200 $PY -I -B a_c7_fantasmi.py ../../f10-dati/20-validazione/uscite/sim > ris/a_c7_fantasmi.txt         # P11
for f in ris/comandi_insieme.txt ris/comandi_p12.txt; do                                                        # P5, P8, P12, sessione
  xargs -P 2 -L 1 sh -c 'out=$0; timeout 280 ./insieme_rifatto/insieme "$@" nome=$out > ris/$out.txt || echo "FALLITO $out" >> ris/falliti.txt' < $f
done
echo fatto
