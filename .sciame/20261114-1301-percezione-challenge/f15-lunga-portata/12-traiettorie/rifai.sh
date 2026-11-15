#!/bin/sh
# Rifà le prove sulle traiettorie (f15/12-traiettorie). Solo conti su dati pubblici: nessun sensore fisico.
set -e
QUI=$(cd "$(dirname "$0")" && pwd)
F15=$(cd "$QUI/.." && pwd)
PY=$F15/../f10-dati/ambiente/venv/bin/python
timeout 900 "$PY" -I -u "$QUI/prove_traiettorie.py" "$F15" "$QUI" | tee "$QUI/prove.log"
timeout 300 "$PY" -I -u "$QUI/riassunto.py" "$F15" "$QUI" | tee "$QUI/riassunto.txt"
