#!/bin/sh
# Rifa' tutti i ricalcoli del fascicolo (circa 10 s). Un processo alla volta, ciascuno con il suo tempo massimo.
set -e
QUI="$(cd "$(dirname "$0")" && pwd)"
PY="$QUI/../../f10-dati/ambiente/venv/bin/python"
mkdir -p "$QUI/uscite"
timeout 120 "$PY" -I -B "$QUI/ricalcoli.py" > "$QUI/uscite/ricalcoli.txt"
timeout 120 "$PY" -I -B "$QUI/mobile_mc.py" 20000 > "$QUI/uscite/mobile_mc.txt"
echo "fatto: $QUI/uscite/ricalcoli.txt, $QUI/uscite/mobile_mc.txt"
