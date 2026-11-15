#!/bin/sh
cd "$(dirname "$0")/../.."
PY=../.sciame/20261114-1301-percezione-challenge/f10-dati/ambiente/venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
xargs -P 6 -L 1 sh -c 'f=uscite/misure/$0_$1_$2.json; [ -f $f ] || timeout 300 '"$PY"' -I -B prove/misura_corto.py $0 $1 $2 $f 2>/dev/null' < uscite/misure/lista.txt
