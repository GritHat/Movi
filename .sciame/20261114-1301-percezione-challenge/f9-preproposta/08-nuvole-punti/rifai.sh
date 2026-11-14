#!/bin/sh
# Rifa le prove di nuvole-punti-f9 (S10). Un lancio alla volta, ognuno al piu' due minuti.
# Uso: sh rifai.sh   (dalla cartella 08-nuvole-punti; scrive solo qui)
set -e
cd "$(dirname "$0")"
gcc -O2 -o fasce fasce.c -lm
timeout 120 ./fasce > risultati_2.txt 2>&1            # montaggio del nucleo: 87x58 gradi, 1,2 m, 15 gradi
gcc -O2 -DHFOV=58.0 -DVFOV=87.0 -o fasce_vert fasce.c -lm
timeout 120 ./fasce_vert > risultati_verticale.txt 2>&1  # camera ruotata di 90 gradi: 58x87 gradi
# risultati_1.txt e' il primo lancio (fasce_v1.c, prima delle aggiunte): gcc -O2 -o fasce_v1 fasce_v1.c -lm && timeout 120 ./fasce_v1
