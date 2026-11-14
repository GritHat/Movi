#!/bin/sh
# Rifa' tutto il banco. Ogni lancio: un processo, al piu' 120 s, semi fissati. Da eseguire in questa cartella.
set -e
gcc -O2 -Wall -Wno-misleading-indentation -Wno-maybe-uninitialized -o banco banco.c -lm
mkdir -p risultati
timeout 120 ./banco tara > risultati/taratura_esito.txt                       # semi 1000-1199, D e T
# lisciatura di C-004 (3 passate) scelta cosi': per g in D T, per sm in 1 2 3 4:
#   C4_SM=$sm ONLY_C004=1 ./banco prova $g 0.9 0 0.20 0 1000 200 0123456 x   -> il minimo sm con ogni cella sul percorso >= 0,88 (file tara_c004_*.tsv)
# prova: semi 9000-9399, 400 per comportamento (0-6) e geometria
for g in D T L; do
  timeout 120 ./banco prova $g 0.9 0 0.20 0 9000 400 0123456 ${g}09 > risultati/prova_${g}_pd09.tsv
  timeout 120 ./banco prova $g 1.0 0 0.20 0 9000 400 0123456 ${g}10 > risultati/prova_${g}_pd10.tsv
done
# bracci (solo T): ombra stimata a -20 cm con e senza fascia; rilevamento 0,7; rumore 4/9/16 cm
timeout 120 ./banco prova T 0.9 -0.20 0.20 0 9000 400 0123456 Tm20 > risultati/braccio_T_ombra-20_fascia.tsv
timeout 120 ./banco prova T 0.9 -0.20 0.00 0 9000 400 0123456 Tm20nf > risultati/braccio_T_ombra-20_senzafascia.tsv
timeout 120 ./banco prova T 0.7 0 0.20 0 9000 400 0123456 T07 > risultati/braccio_T_pd07.tsv
timeout 120 ./banco prova T 0.9 0 0.20 1 9000 400 0123456 Tcurva > risultati/braccio_T_rumore_curva.tsv
RCURVE=1 timeout 120 ./banco tara > risultati/taratura_curva_esito.txt       # scrive taratura_curva.txt
RCURVE=1 timeout 120 ./banco prova T 0.9 0 0.20 1 9000 400 0123456 TcurvaNota > risultati/braccio_T_rumore_curva_noto.tsv
# attacchi della preproposta: 1 (sosta improvvisa, semi 9500-9699), 2 (tripla e due, semi 9700-9899)
for g in D T; do
  timeout 120 ./banco prova $g 0.9 0 0.20 0 9500 200 7 ${g}att1 > risultati/attacco1_${g}.tsv
  timeout 120 ./banco prova $g 0.9 0 0.20 0 9700 200 89 ${g}att2 > risultati/attacco2_${g}.tsv
done
# tempi
for g in T L; do for n in 1 10; do timeout 120 ./banco tempo $g $n; done; done > risultati/tempi.txt
PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 tabelle.py > risultati/TABELLE.txt
