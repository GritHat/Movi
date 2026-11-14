#!/bin/sh
# Rifa' tutti i ricalcoli del fascicolo (circa 1 minuto). Scrive ricalcoli.txt accanto.
cd "$(dirname "$0")" || exit 1
PY=/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f10-dati/ambiente/venv/bin/python
[ -x "$PY" ] || PY=python3
timeout 300 "$PY" -I -B ricalcoli.py > ricalcoli.txt 2>&1; echo "uscita: $?"; tail -n 1 ricalcoli.txt
