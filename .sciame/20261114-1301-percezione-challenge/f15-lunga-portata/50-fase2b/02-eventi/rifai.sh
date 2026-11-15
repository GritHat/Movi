#!/bin/sh
# Rifa' le misure di eventi_v2 (simulazione; circa 17 minuti con 7 processi figli e il padre). Scrive risultati_v2.json e passaggi_v2.jsonl.
# Nucleo: 04-moto/movi_lp.py (difetto). Per il nucleo v2: EVENTI_NUCLEO=v2 sh rifai.sh
cd "$(dirname "$0")" || exit 1
PY=../../../f10-dati/ambiente/venv/bin/python
timeout 2400 "$PY" -I -B eventi_v2.py 60 60 300 7 > rifai_esito.txt 2>&1
