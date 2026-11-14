#!/bin/sh
# rifai.sh — rifa' i conti e i rilanci del fascicolo «rappresentazioni dello spazio e costo di calcolo».
# Uso:  sh rifai.sh conti          (pochi secondi: rilegge i file d'origine e i rilanci gia' presenti in uscite/)
#       sh rifai.sh banchi [N]     (circa 8 minuti: ricompila e rilancia i banchi in C sul nucleo N, predefinito 2; poi i conti)
# Un processo alla volta, ognuno sotto timeout. Scrive solo in questa cartella. I sorgenti in banco_*/ sono copie
# non modificate dei file d'origine (elenco e impronte in uscite/impronte_sorgenti.txt).
cd "$(dirname "$0")" || exit 1
PY=../../f10-dati/ambiente/venv/bin/python
C=${2:-2}; mkdir -p uscite
if [ "$1" = banchi ]; then
  ( cd banco_strutture && timeout 120 sh compila.sh ) || exit 1
  ( cd banco_strutture && timeout 420 sh lancia.sh "$C" ../uscite/strutture_breve_core2.txt 300 breve )
  timeout 900 sh rilancia_sicurezza.sh "$C"
fi
timeout 120 "$PY" -I -B conti.py > uscite/conti.txt 2> uscite/conti_avvisi.txt; echo "conti: esito $?"
tail -n 25 uscite/conti.txt
