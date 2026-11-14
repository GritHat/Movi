#!/bin/sh
# Rifa' l'analisi di sciame-statistico (f8, fase f4). Da eseguire in questa cartella; un lancio alla volta, ognuno <= 120 s (il piu' lungo misurato: 68 s).
set -e
CC="gcc -O2 -Wall -Wno-misleading-indentation -Wno-maybe-uninitialized"
mkdir -p ris
# 1. codice delle modifiche copiato (13-soluzione/comp.c, gen.h, taratura.txt): controllo sui semi del banco, semi nuovi, dieci blocchi
(cd codice && $CC -o comp comp.c -lm && gcc -O2 -o prova_semi prova_semi.c -lm && timeout 20 ./prova_semi > ../ris/prova_semi.txt
 timeout 120 ./comp prova D 0.9 0 0.20 0 9000 400 0123456 D09 > ../ris/controllo_D_9000.tsv
 timeout 120 ./comp prova D 0.9 0 0.20 0 20000 1200 0123456 D20k > ../ris/nuovi_D_20000x1200.tsv
 timeout 120 ./comp prova T 0.9 0 0.20 0 20000 800 0123456 T20k > ../ris/nuovi_T_20000x800.tsv
 timeout 120 ./comp prova L 0.9 0 0.20 0 20000 400 0123456 L20k > ../ris/nuovi_L_20000x400.tsv
 timeout 120 ./comp prova L 0.9 0 0.20 0 20400 400 0123456 L20k4 > ../ris/nuovi_L_20400x400.tsv
 for s in 40000 45000 50000 55000 60000 65000 70000 75000; do timeout 120 ./comp prova D 0.9 0 0.20 0 $s 400 0123456 D$s > ../ris/blocco_D_${s}x400.tsv; done)
# 2. generatore spostato (velocita' 15 %, rotta 8 gradi, rotta entro +-30 gradi), taratura ferma
(cd codice_spostato && $CC -o comp comp.c -lm && for g in D T L; do timeout 120 ./comp prova $g 0.9 0 0.20 0 30000 400 0123456 ${g}sp > ../ris/spostato_${g}_30000x400.tsv; done)
# 3. semi riparati (stato iniziale mescolato), taratura rifatta
(cd codice_semi && $CC -o comp comp.c -lm && timeout 120 ./comp tara > ../ris/semi_taratura_esito.txt
 for s in 80000 80400 80800 81200 81600; do timeout 120 ./comp prova D 0.9 0 0.20 0 $s 400 0123456 Dr$s > ../ris/semi_D_${s}x400.tsv; done
 for g in T L; do for s in 80000 80400; do timeout 120 ./comp prova $g 0.9 0 0.20 0 $s 400 0123456 ${g}r$s > ../ris/semi_${g}_${s}x400.tsv; done; done)
# 4. semi riparati + generatore spostato, taratura riparata ferma (copiata da codice_semi)
(cd codice_semi_spostato && cp ../codice_semi/taratura.txt . && $CC -o comp comp.c -lm && for g in D T L; do timeout 120 ./comp prova $g 0.9 0 0.20 0 90000 400 0123456 ${g}rs > ../ris/semi_spostato_${g}_90000x400.tsv; done)
# 5. riconteggio, con le due definizioni del denominatore
for m in griglia tutti; do PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 riconta.py $m > ris/TABELLE_STATISTICO_$m.txt; done
