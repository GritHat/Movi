#!/bin/sh
# rifai.sh — rifa' il controllo statistico (sciame-statistico, f12) in meno di un minuto. Legge 02-prova-insieme/ris e 03-libero; scrive solo qui.
set -e
cd "$(dirname "$0")"
PY=../../f10-dati/ambiente/venv/bin/python
timeout 120 $PY -I -B riconta_insieme.py ../02-prova-insieme/ris > riconta_insieme.txt
timeout 120 $PY -I -B semi_insieme.py > semi_insieme.txt
timeout 120 $PY -I -B riconta_libero.py ../03-libero > riconta_libero.txt
timeout 300 $PY -I -B confronti.py ../02-prova-insieme/ris > confronti.txt
timeout 60 $PY -I -B dettagli.py ../03-libero > dettagli.txt
timeout 60 $PY -I -B potenza.py > potenza.txt
ls -la --time-style=full-iso ../02-prova-insieme/PREVISIONI.md ../02-prova-insieme/fumo ../03-libero/PREVISIONI.md ../03-libero/*lancio1* ../CONTRATTO_INTEGRAZIONE.md > ore_dei_file.txt
sha256sum ../02-prova-insieme/PREVISIONI.md ../03-libero/PREVISIONI.md >> ore_dei_file.txt
timeout 60 $PY -I -B confronta_tabelle.py ../02-prova-insieme/ris > confronta_tabelle.txt
