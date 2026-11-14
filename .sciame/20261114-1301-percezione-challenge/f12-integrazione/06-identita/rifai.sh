#!/bin/sh
# f12, 06-identita — rifà tutto. Da lanciare da questa cartella: sh rifai.sh   (circa 15 minuti, al più 8 processi).
# Non scrive fuori da questa cartella; legge f10-dati (catena, simulatore, validazione, sequenze) in sola lettura.
# Le sequenze a 848×480 e i semi nuovi NON stanno su disco: si rigenerano in memoria dal nome (seme = nome), qui dentro.
set -u
cd "$(dirname "$0")"
F10=../../f10-dati
PY="$F10/ambiente/venv/bin/python -I -B"
# 1) la copia: l'originale di f10 più DIFFERENZE.diff deve dare `catena/` (ogni riga cambiata è lì)
rm -rf catena_originale catena_rifatta tmp
cp -r $F10/10-catena catena_originale && rm -rf catena_originale/uscite catena_originale/__pycache__
cp -r catena_originale catena_rifatta && (cd catena_rifatta && patch -p1 -s < ../DIFFERENZE.diff)
diff -r catena catena_rifatta > /dev/null && echo "copia: catena/ = originale + DIFFERENZE.diff" || echo "ATTENZIONE: catena/ non coincide con originale + DIFFERENZE.diff"
rm -rf catena_rifatta
# 2) le 25 prove di f10 sulla copia, a interruttori spenti (2 falliscono solo perché cercano ../03-infrastruttura)
(cd catena && timeout 120 ../$PY prove.py 2>&1 | grep -E "^(Ran|OK|FAILED|ERROR)") > risultati/prove_copia.txt
# 3) le misure: otto configurazioni per sequenza (prima, f401, f401p, f402, f408, f409, tutte, tutte_p)
timeout 400 $PY prova.py disco 8        # (a) 424×240, le 130 sequenze di f10 con pannello, pavimento, scatola: TARATURA
timeout 500 $PY prova.py nuovi424 8     # (a, c) semi nuovi k = 100…: la cifra finale a 424
timeout 900 $PY prova.py nuovi848 8     # (b, c) gli stessi semi a 848×480
timeout 200 $PY prova.py due424 8       # (d) chi cammina più una persona ferma mai vista nell'ombra
timeout 300 $PY prova.py due848 8
timeout 200 $PY prova.py z21_424 8      # attacco A8 dell'avversario: linea a 2,1 m
timeout 300 $PY prova.py z21_848 8
F12_CONFIG=tutte_p,tutte_p2 F12_ETICHETTA=_p2 timeout 200 $PY prova.py z21_424 8   # tracciamento-2 (smentita)
F12_CONFIG=tutte_p,tutte_p2 F12_ETICHETTA=_p2 timeout 300 $PY prova.py z21_848 8
timeout 120 $PY p8_f408.py | tail -6 > risultati/p8_f408.txt   # F-408 sulla prova P8 a mano
timeout 280 $PY estraneo.py > risultati/estraneo.txt          # (d) scena A3 dell'avversario e 11 varianti
for b in disco nuovi424 nuovi848 due424 due848 z21_424 z21_848; do python3 riassumi.py risultati/$b.jsonl > risultati/$b.tabelle.md; done
# un passaggio fotogramma per fotogramma:  $PY diagnosi.py d435i_nom__pannello_a05__s00 tutte_p 14 60
# i punti per cella (ponte, scatola):      $PY diag_celle.py d435i_nom__pannello_a05__s00 16 68 80 16 24
