#!/bin/sh
# f12, 07-controprova-identita — rifà tutto. Da lanciare da questa cartella: sh rifai.sh  (circa 12 minuti, al più 8 processi).
# Scrive solo qui (risultati/, tmp/, tmp_att/ cancellate alla fine). Legge f10-dati e 06-identita in sola lettura.
# Nessuna sequenza su disco: quelle a 640 e 848 px e tutti i semi nuovi si rigenerano in memoria dal nome (0 GB).
set -u
cd "$(dirname "$0")"
F10=../../f10-dati
PY="$F10/ambiente/venv/bin/python -I -B"
mkdir -p risultati
# 0) la copia della catena è quella di 06-identita (già corretta dall'autore), senza righe mie
diff -r -x __pycache__ ../06-identita/catena catena > /dev/null && echo "copia: catena/ = 06-identita/catena" || echo "ATTENZIONE: catena/ diversa da 06-identita/catena"
cmp -s ../06-identita/prova.py prova_autore.py && echo "prova_autore.py = 06-identita/prova.py" || echo "ATTENZIONE: prova_autore.py diverso"
# 1) rifacimento delle misure principali dell'autore (semi k = 100…) e replica su semi mai usati (k = 200…)
F12_CONFIG=prima,tutte,tutte_p F12_ETICHETTA=_rifatto timeout 400 $PY prova_autore.py nuovi424 8
F12_CONFIG=tutte_p F12_ETICHETTA=_rifatto timeout 500 $PY prova_autore.py nuovi848 8
F12_CONFIG=tutte_p F12_ETICHETTA=_replica timeout 400 $PY prova_autore.py ultimi424 8
F12_CONFIG=tutte_p F12_ETICHETTA=_replica timeout 600 $PY prova_autore.py ultimi848 8
python3 -I -B riconta.py > risultati/RICONTO.md
# 2) gli attacchi (semi k = 300…): «prima» e «tutte_p» per ogni sequenza
for b in estraneo geometria persona rumore rotto bordo2; do timeout 500 $PY attacco.py $b 8; done
python3 -I -B riassumi.py > risultati/ATTACCHI.md
# un solo attacco:  $PY attacco.py persona 8   (gruppi in lavori() di attacco.py);  diagnosi:  $PY diag.py rimozione 300  |  $PY diag.py bordo 300
