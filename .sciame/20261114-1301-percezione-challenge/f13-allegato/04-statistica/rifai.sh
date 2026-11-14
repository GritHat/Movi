#!/bin/sh
# rifai.sh -- rifa' i riconteggi e i conti del fascicolo (sola lettura dei file dello sciame; scrive solo in questa cartella).
# Uso: sh rifai.sh     Durata: pochi secondi. Nessuna rete, nessun git.
set -eu
QUI="$(cd "$(dirname "$0")" && pwd)"
PY="$QUI/../../f10-dati/ambiente/venv/bin/python"
timeout 120 "$PY" -I -B "$QUI/riconta.py" > "$QUI/ricontato.txt"
timeout 300 "$PY" -I -B "$QUI/conti.py" > "$QUI/conti.txt"
grep -c "^\[NON TORNA\]" "$QUI/ricontato.txt" || true
tail -2 "$QUI/ricontato.txt"
