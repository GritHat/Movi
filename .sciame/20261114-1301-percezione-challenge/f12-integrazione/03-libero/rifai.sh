#!/bin/sh
# rifai.sh — rifa tutto in circa 2 minuti (un filo). Scrive solo in questa cartella. Nessun git, nessun sudo, nessuna rete.
set -e
cd "$(dirname "$0")"
PY=../../f10-dati/ambiente/venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
timeout 400 $PY -I -B banco_libero.py 30            # semi del lancio 1 -> risultati_banco.txt, banco.json
timeout 60  $PY -I -B riepilogo.py                  # -> riepilogo_banco.txt
timeout 400 $PY -I -B banco_libero.py 30 x semi2    # semi nuovi -> risultati_banco_semi2.txt, banco_semi2.json
timeout 60  $PY -I -B riepilogo.py semi2            # -> riepilogo_banco_semi2.txt
timeout 120 $PY -I -B banco_libero.py 30 tempi      # -> tempi.txt
timeout 120 $PY -I -B fotogrammi_f10.py             # -> risultati_f10.txt (legge f10-dati in sola lettura)
timeout 60  $PY -I -B diagnosi_f10.py                 # -> diagnosi_f10.txt
