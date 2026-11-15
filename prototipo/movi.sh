#!/bin/sh
# movi.sh — lancia «python -m movi» con l'ambiente dello sciame in modo isolato (-I): con -I la cartella corrente
# non è nel percorso dei moduli, quindi la si aggiunge qui in modo esplicito. Uso: sh movi.sh esegui … (come -m movi)
QUI=$(cd "$(dirname "$0")" && pwd)
# Interprete: $PY se dato; altrimenti l'ambiente di lavoro dello sciame se esiste; altrimenti .venv creato da setup.sh;
# altrimenti python3 di sistema.
if [ -z "$PY" ]; then
  if [ -x "$QUI/../.sciame/20261114-1301-percezione-challenge/f10-dati/ambiente/venv/bin/python" ]; then
    PY="$QUI/../.sciame/20261114-1301-percezione-challenge/f10-dati/ambiente/venv/bin/python"
  elif [ -x "$QUI/../.venv/bin/python" ]; then PY="$QUI/../.venv/bin/python"
  else PY=python3; fi
fi
MOVI_RADICE="$QUI" exec "$PY" -I -B -c 'import os, runpy, sys; sys.path.insert(0, os.environ["MOVI_RADICE"]); sys.argv[0] = "movi"; runpy.run_module("movi", run_name="__main__", alter_sys=True)' "$@"
