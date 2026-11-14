#!/bin/sh
# Rifa' le prove di sciame-interfacce (f12, 05-schermo). Da eseguire in questa cartella; un lancio alla volta, ognuno <= 120 s (misurato: 18 s).
# prova_geometria/{comp.c,gen.h,taratura.txt} sono copie di f8-continuita/15-statistica/codice_semi, con due righe in piu' in gen.h
# (geometria E; banda di velocita' VLO..VHI): diff f8-continuita/15-statistica/codice_semi/gen.h prova_geometria/gen.h
set -e
S=../../f8-continuita/15-statistica
cd prova_geometria && mkdir -p ris
gcc -O2 -Wall -Wno-misleading-indentation -Wno-maybe-uninitialized -o comp comp.c -lm
timeout 120 ./comp prova D 0.9 0 0.20 0 80000 400 0123456 Dr80000 > ris/controllo_D_80000x400.tsv
echo "controllo (deve dare 1: solo la riga del tempo): $(diff ris/controllo_D_80000x400.tsv ../$S/ris/semi_D_80000x400.tsv | grep -c '^<')"
VLO=0.8  VHI=1.0  timeout 120 ./comp prova E 0.9 0 0.20 0 120000 400 0123456 Elarga > ris/E_larga_08-10.tsv
VLO=0.45 VHI=0.55 timeout 120 ./comp prova D 0.9 0 0.20 0 120000 400 0123456 Dlento > ris/D_lento_045-055.tsv
VLO=1.0  VHI=1.4  timeout 120 ./comp prova D 0.9 0 0.20 0 120000 400 0123456 Dnorm  > ris/D_normale_10-14.tsv
VLO=0.45 VHI=0.55 timeout 120 ./comp prova E 0.9 0 0.20 0 120000 400 0123456 Elento > ris/E_lento_045-055.tsv
cd .. && timeout 60 /usr/bin/python3 -I -B conti_schermo.py > risultati_schermo.txt
sh controlla_frasi.sh > esito_frasi.txt; cat esito_frasi.txt
